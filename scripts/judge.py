"""Programmatic judge for the eval.

Compares candidates (predictions) against ground truth (target_tool).
Computes:
  - tool_hit_rate  : candidate.tool == target_tool
  - param_hit_rate : required params present + types coerce
  - both_correct   : tool_hit AND param_hit

Aggregates by persona, by tool, by category. Writes report.md.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def load_candidates() -> dict[str, dict]:
    """Merge all candidate batches into a {prompt_id -> candidate} dict.

    Normalizes key names — some subagents emit `tool`/`params`, others
    `candidate_tool`/`candidate_params`.
    """
    out: dict[str, dict] = {}
    for i in range(1, 7):
        path = TESTS / f"candidates_batch_{i}.json"
        if not path.exists():
            raise SystemExit(f"Missing {path}")
        data = json.loads(path.read_text())
        for c in data:
            out[c["prompt_id"]] = {
                "prompt_id": c["prompt_id"],
                "candidate_tool": c.get("candidate_tool") or c.get("tool"),
                "candidate_params": c.get("candidate_params") or c.get("params") or {},
            }
    return out


def load_schemas() -> dict[str, dict]:
    bundle = json.loads((TESTS / "tool_schemas.json").read_text())
    return {t["name"]: t for t in bundle}


def param_hit(candidate_params: dict, target_schema: dict) -> tuple[bool, list[str]]:
    """Return (passed, reasons)."""
    reasons: list[str] = []
    required = set(target_schema.get("required", []))
    candidate_keys = set(candidate_params.keys())

    missing = required - candidate_keys
    if missing:
        reasons.append(f"missing required: {sorted(missing)}")

    # Type coherence (lightweight) — only check declared properties.
    props = target_schema.get("properties", {})
    for k, v in candidate_params.items():
        if k not in props:
            # Extra param outside schema is tolerable IF anyOf/additional allowed,
            # but for OpenAPI-strict schemas it's a deviation.
            if not target_schema.get("additionalProperties", False):
                reasons.append(f"extra param: {k}")
            continue
        decl = props[k]
        # The Pydantic-derived schema uses anyOf with null for Optional. Unwrap.
        decl_types: set[str] = set()
        if "anyOf" in decl:
            for opt in decl["anyOf"]:
                t = opt.get("type")
                if t and t != "null":
                    decl_types.add(t)
        elif "type" in decl:
            decl_types.add(decl["type"])

        # Map Python type of v to JSON Schema type
        py_t = (
            "null" if v is None else
            "boolean" if isinstance(v, bool) else
            "integer" if isinstance(v, int) else
            "number" if isinstance(v, float) else
            "string" if isinstance(v, str) else
            "array" if isinstance(v, list) else
            "object" if isinstance(v, dict) else
            "unknown"
        )
        # Permissive: placeholders like "<deal_id>" count as string (which is the right type).
        if decl_types and py_t not in decl_types and py_t != "null":
            # integer/number leniency (number accepts integer)
            if not (py_t == "integer" and "number" in decl_types):
                reasons.append(f"type mismatch on {k}: got {py_t}, want {sorted(decl_types)}")

    return (not reasons), reasons


def main() -> None:
    candidates = load_candidates()
    schemas = load_schemas()
    prompts = json.loads((TESTS / "prompts.json").read_text())

    rows = []
    for p in prompts:
        c = candidates.get(p["prompt_id"])
        if not c:
            rows.append({**p, "missing_candidate": True})
            continue
        tool_hit = c["candidate_tool"] == p["target_tool"]
        target_schema = schemas[p["target_tool"]]["parameters"]
        params_ok, reasons = param_hit(c.get("candidate_params") or {}, target_schema)
        rows.append({
            **p,
            "candidate_tool": c["candidate_tool"],
            "candidate_params": c.get("candidate_params") or {},
            "tool_hit": tool_hit,
            "param_hit": params_ok,
            "both": tool_hit and params_ok,
            "fail_reasons": reasons,
        })

    # Aggregate
    n = len(rows)
    tool_hits = sum(r.get("tool_hit", False) for r in rows)
    param_hits = sum(r.get("param_hit", False) for r in rows)
    both = sum(r.get("both", False) for r in rows)

    by_persona: dict[str, dict[str, int]] = defaultdict(lambda: {"n": 0, "tool": 0, "param": 0, "both": 0})
    for r in rows:
        b = by_persona[r["persona"]]
        b["n"] += 1
        b["tool"] += int(r.get("tool_hit", False))
        b["param"] += int(r.get("param_hit", False))
        b["both"] += int(r.get("both", False))

    by_tool: dict[str, dict[str, int]] = defaultdict(lambda: {"n": 0, "tool": 0, "param": 0, "both": 0})
    for r in rows:
        b = by_tool[r["target_tool"]]
        b["n"] += 1
        b["tool"] += int(r.get("tool_hit", False))
        b["param"] += int(r.get("param_hit", False))
        b["both"] += int(r.get("both", False))

    # Build report
    out_lines = [
        "# Clint MCP — Eval Report",
        "",
        f"Total prompts: {n}",
        f"Tool hit rate:  {tool_hits / n:.1%}  ({tool_hits}/{n})",
        f"Param hit rate: {param_hits / n:.1%}  ({param_hits}/{n})",
        f"Both correct:   {both / n:.1%}  ({both}/{n})",
        "",
        f"**Threshold (skill): both_correct ≥ 0.95** — {'✅ PASS' if both/n >= 0.95 else '❌ FAIL'}",
        "",
        "## By persona",
        "",
        "| Persona | n | tool_hit | param_hit | both |",
        "|---|---|---|---|---|",
    ]
    for persona, b in sorted(by_persona.items()):
        out_lines.append(
            f"| {persona} | {b['n']} | {b['tool']/b['n']:.1%} | {b['param']/b['n']:.1%} | {b['both']/b['n']:.1%} |"
        )

    out_lines += ["", "## By tool (sorted by worst both)", "", "| Tool | n | tool_hit | param_hit | both |", "|---|---|---|---|---|"]
    sorted_tools = sorted(by_tool.items(), key=lambda x: x[1]["both"] / x[1]["n"])
    for tool, b in sorted_tools:
        if b["both"] / b["n"] < 1.0:
            out_lines.append(
                f"| {tool} | {b['n']} | {b['tool']/b['n']:.1%} | {b['param']/b['n']:.1%} | {b['both']/b['n']:.1%} |"
            )

    out_lines += ["", "## Failures (sample, max 30)", ""]
    failures = [r for r in rows if not r.get("both")]
    for r in failures[:30]:
        out_lines.append(f"- **{r['prompt_id']}**")
        out_lines.append(f"  - prompt: \"{r['prompt']}\"")
        out_lines.append(f"  - target: `{r['target_tool']}`  |  candidate: `{r.get('candidate_tool')}`")
        if r.get("fail_reasons"):
            out_lines.append(f"  - param fails: {r['fail_reasons']}")

    (ROOT / "tests" / "report.md").write_text("\n".join(out_lines) + "\n")
    (ROOT / "tests" / "results.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    print(f"Total: {n} | tool={tool_hits/n:.1%} | param={param_hits/n:.1%} | both={both/n:.1%}")
    print(f"Threshold (0.95 both): {'PASS' if both/n >= 0.95 else 'FAIL'}")
    print(f"Reports -> tests/report.md, tests/results.json")


if __name__ == "__main__":
    main()

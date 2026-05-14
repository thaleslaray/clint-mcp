# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FastMCP server exposing the Clint CRM API (https://api.clint.digital) — 46 endpoints across 14 categories. Tool functions are **code-generated** from `specs/openapi.json` (OpenAPI 3.0.2) — do not hand-edit files in `src/clint_mcp/tools/`.

Architecture: FastMCP + Code Mode (3 meta-tools `search`/`get_schema`/`execute`) via `MontySandboxProvider`. Pin `pydantic-monty==0.0.7` — newer versions broke CodeMode.

## Common commands

```bash
# Install (editable) — creates the `clint-mcp` console script
uv pip install -e .

# Regenerate tool modules from the OpenAPI spec
python -m clint_mcp.generator

# Run the MCP server (stdio)
clint-mcp
# or
python -m clint_mcp.server

# Smoke tests (require CLINT_API_TOKEN)
python scripts/smoke_test.py   # 5 read-only GETs
python scripts/smoke_write.py  # 1 template HSM to authorized number

# Eval (requires precomputed candidates in scripts/candidates/)
python scripts/judge.py
```

No test suite, linter, or formatter is configured beyond Pyright type-check.

## Required environment

- `CLINT_API_TOKEN` (required) — sent as `api-token` header
- `CLINT_MAX_RPS` (optional, default `5`) — client-side rate limit

The `ClintClient` constructor raises `RuntimeError` if `CLINT_API_TOKEN` is missing.

## Code generation flow

1. **Inputs:**
   - `specs/openapi.json` — consolidated OpenAPI (built from the 46 per-endpoint markdown files in `specs/endpoints/` that were scraped from clint-api.readme.io)
   - `TOOL_NAMES` map in `generator.py` — maps `(method, path)` → short tool name
2. **`python -m clint_mcp.generator`** rewrites `src/clint_mcp/tools/*.py` (one file per category) and `src/clint_mcp/tools/__init__.py` (`ALL_TOOLS` registry).
3. **`server.py`** registers each tool via `mcp.tool(fn)`, then applies `CodeMode` transform.

## Naming conventions (inviolável)

- Tool names: `clint_{resource}_{verb}` with the canonical verb taxonomy (`list`/`get`/`create`/`update`/`delete`/`add`/`remove`/`send`). Never sinônimos (no `fetch`, `retrieve`, `find`).
- Path param `id` is renamed to `<entity>_id` based on the preceding path segment (e.g. `/v1/contacts/{id}` → `contact_id`, not `id_`). See `derive_entity_from_path()`.
- CamelCase path params are converted to snake_case in function signatures, with substitution back to camelCase in the URL build.
- Body fields with known LLM-confusing names get **anti-vocab hints with ⚠️**:
  - `message` → "⚠️ Field name is EXACTLY `message`. Do NOT pass `text`"
  - `url` → "⚠️ Field name is EXACTLY `url` ... Do NOT pass `audio_url`/`image_url`/`document_url`"
  - `template_id` → "⚠️ Do NOT pass `template_name` or `message_template_id`"

## Hints architecture (SEP-1382)

- **Tool-level docstring** = WHAT/WHEN only (summary + description + endpoint reference). NO per-param hints — those get truncated.
- **Per-parameter `Annotated[T, Field(description=...)]`** = FORMAT/VALIDATION. Reaches `inputSchema.properties[].description` via FastMCP. LLM clients read this reliably regardless of docstring length.
- Hint coverage: 181/181 params (100%) at last regen.

## Eval pipeline

Quality is validated with 414-prompt eval (3 personas × 46 tools × 3 variations):

1. **Personas** (`scripts/personas-infoprodutor.json`) — Iniciante coloquial (Carla), Intermediário operacional (Felipe), Avançado corporativo (Renata). ICP-grounded via `/pesquisa-rapida` against real Clint customer profiles.
2. **Prompts** (`scripts/prompts-persona-{A,B,C}.json` per persona, merged into `scripts/eval-cases.json`) — 138 prompts/persona.
3. **Candidates** (`scripts/candidates/*.json`, gitignored) — 6 subagents simulate LLM clients picking tool + params for each prompt.
4. **Judge** (`scripts/judge.py`) — programmatic comparison. Computes `tool_hit_rate`, `param_hit_rate`, `both_correct`. Threshold: `both_correct ≥ 0.95`.

Last result: **97.3% both_correct** (above threshold).

## Editing the generator

When changing parameter naming, hints, or the rename map:
1. Edit `generator.py`
2. Run `python -m clint_mcp.generator`
3. Inspect changes in `src/clint_mcp/tools/` (git diff)
4. If touching anything LLM-facing, re-run the eval pipeline before bumping the version

## Versioning

Bump rules:
- **Patch** (0.1.X) — bug fixes, doc updates, single-tool changes
- **Minor** (0.X.0) — new tools, new categories, hint improvements that don't rename anything
- **Major** (X.0.0) — tool renames (BREAKING), removed tools, breaking schema changes

CHANGELOG.md is curated by hand from the eval delta + git log between tags.

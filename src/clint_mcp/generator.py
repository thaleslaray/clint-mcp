"""Generate tool modules from the consolidated OpenAPI spec.

Run with: python -m clint_mcp.generator
Writes one file per tag under src/clint_mcp/tools/.
"""
from __future__ import annotations

import json
import keyword
import re
from collections import defaultdict
from pathlib import Path
from textwrap import indent

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "specs" / "openapi.json"
TOOLS_DIR = Path(__file__).resolve().parent / "tools"

# --- Tool naming map ---------------------------------------------------------
# (method, path) -> tool function name (without `clint_` prefix; prefix added later)
TOOL_NAMES: dict[tuple[str, str], str] = {
    # Contacts
    ("GET", "/v1/contacts"): "contacts_list",
    ("POST", "/v1/contacts"): "contacts_create",
    ("GET", "/v1/contacts/{id}"): "contacts_get",
    ("POST", "/v1/contacts/{id}"): "contacts_update",
    ("DELETE", "/v1/contacts/{id}"): "contacts_delete",
    ("GET", "/v1/contacts/{id}/attachments"): "contacts_attachments_list",
    ("POST", "/v1/contacts/{id}/tags"): "contacts_tags_add",
    ("DELETE", "/v1/contacts/{id}/tags"): "contacts_tags_remove",
    # Deals
    ("GET", "/v1/deals"): "deals_list",
    ("POST", "/v1/deals"): "deals_create",
    ("GET", "/v1/deals/{id}"): "deals_get",
    ("POST", "/v1/deals/{id}"): "deals_update",
    ("DELETE", "/v1/deals/{id}"): "deals_delete",
    # Tags
    ("GET", "/v1/tags"): "tags_list",
    ("POST", "/v1/tags"): "tags_create",
    ("GET", "/v1/tags/{id}"): "tags_get",
    ("DELETE", "/v1/tags/{id}"): "tags_delete",
    # Organizations
    ("GET", "/v1/organizations/{id}"): "organizations_get",
    ("POST", "/v1/organizations/{id}"): "organizations_update",
    # Groups
    ("GET", "/v1/groups"): "groups_list",
    ("GET", "/v1/groups/{id}"): "groups_get",
    # Lost Status
    ("GET", "/v1/lost-status"): "lost_status_list",
    ("GET", "/v1/lost-status/{id}"): "lost_status_get",
    # Origins
    ("GET", "/v1/origins"): "origins_list",
    ("GET", "/v1/origins/{id}"): "origins_get",
    # Users
    ("GET", "/v1/users"): "users_list",
    ("GET", "/v1/users/{id}"): "users_get",
    # Account
    ("GET", "/v1/account/fields"): "account_fields_list",
    # Channel Accounts (v2)
    ("GET", "/v2/channel-accounts"): "channel_accounts_list",
    ("GET", "/v2/channel-accounts/{id}"): "channel_accounts_get",
    # Message Templates (v2)
    ("GET", "/v2/message-templates"): "message_templates_list",
    ("GET", "/v2/message-templates/{id}"): "message_templates_get",
    # Chats (v2)
    ("GET", "/v2/chats/contact/{contactId}"): "chats_by_contact_list",
    ("GET", "/v2/chats/channel-account/{channelAccountId}"): "chats_by_channel_account_list",
    ("GET", "/v2/chats/{id}"): "chats_get",
    # Messages (v2)
    ("GET", "/v2/messages/chat/{chatId}"): "messages_by_chat_list",
    ("GET", "/v2/messages/{id}"): "messages_get",
    ("POST", "/v2/messages/text"): "messages_text_send",
    ("POST", "/v2/messages/image"): "messages_image_send",
    ("POST", "/v2/messages/audio"): "messages_audio_send",
    ("POST", "/v2/messages/document"): "messages_document_send",
    ("POST", "/v2/messages/template"): "messages_template_send",
    # Dashboards / Charts (v2)
    ("GET", "/v2/dashboards"): "dashboards_list",
    ("GET", "/v2/dashboards/{id}"): "dashboards_get",
    ("GET", "/v2/dashboards/{id}/data"): "dashboards_data_get",
    ("GET", "/v2/charts/{id}/data"): "charts_data_get",
}

# Module grouping — tag from OpenAPI normalized to a python module name.
TAG_TO_MODULE = {
    "Contacts": "contacts",
    "Deals": "deals",
    "Tags": "tags",
    "Organizations": "organizations",
    "Groups": "groups",
    "Lost Status": "lost_status",
    "Origins": "origins",
    "Users": "users",
    "Channel Accounts": "channel_accounts",
    "Message Templates": "message_templates",
    "Chats": "chats",
    "Messages": "messages",
    "Dashboards": "dashboards",
}

# Fallback module when tag is missing (e.g. /v1/account/fields).
DEFAULT_MODULE = "account"


# --- Helpers -----------------------------------------------------------------

PT_TO_EN_DESC = {
    "Recuperar uma lista paginada": "Retrieve a paginated list",
}


def safe_name(name: str) -> str:
    """Make a parameter name a valid, non-reserved Python identifier."""
    n = re.sub(r"\W", "_", name)
    # Convert camelCase to snake_case (e.g. contactId -> contact_id).
    n = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", n).lower()
    if keyword.iskeyword(n) or n in {"id", "type"}:
        n = n + "_"
    return n


# Entity inferred from path segment for `{id}` rename.
# E.g. /v1/contacts/{id} -> entity "contact" -> param renamed to "contact_id".
# Note: `message-templates` -> `template` (not `message_template`) to match the
# body field name `template_id` used by /v2/messages/template send. This avoids
# inconsistency where the same logical entity has two param names.
_PATH_ENTITY_OVERRIDES = {
    "lost-status": "lost_status",
    "channel-accounts": "channel_account",
    "message-templates": "template",
}


def derive_entity_from_path(path: str, for_param: str = "id") -> str | None:
    """Find the segment immediately preceding `{for_param}` and return its singular form.

    Examples:
      /v1/contacts/{id}/attachments, for_param="id"      -> "contact"
      /v1/contacts/{id}, for_param="id"                  -> "contact"
      /v2/chats/contact/{contactId}, for_param="contactId" -> "chat" (param already semantic)
      /v1/account/fields, for_param="id"                 -> None (no {id} segment)
    """
    segs = path.strip("/").split("/")
    target = "{" + for_param + "}"
    if target not in segs:
        return None
    idx = segs.index(target)
    # find the previous non-version segment
    for j in range(idx - 1, -1, -1):
        s = segs[j]
        if s in ("v1", "v2") or s.startswith("{"):
            continue
        if s in _PATH_ENTITY_OVERRIDES:
            return _PATH_ENTITY_OVERRIDES[s]
        if s.endswith("ies"):
            return s[:-3] + "y"
        if s.endswith("s") and not s.endswith("ss"):
            return s[:-1]
        return s
    return None


def resolve(spec: dict, node):
    """Recursively dereference $ref pointers (#/components/...)."""
    if isinstance(node, dict):
        if "$ref" in node:
            ref = node["$ref"].lstrip("#/").split("/")
            target = spec
            for part in ref:
                target = target[part]
            return resolve(spec, target)
        return {k: resolve(spec, v) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(spec, v) for v in node]
    return node


def render_hint(prop_name: str, schema: dict) -> str:
    """Return a hint string (per quality standards) for a single property."""
    hint_parts: list[str] = []
    desc = schema.get("description", "").strip()
    if desc:
        # Translate common PT-BR phrases.
        for pt, en in PT_TO_EN_DESC.items():
            desc = desc.replace(pt, en)
        hint_parts.append(desc.rstrip("."))

    ptype = schema.get("type")
    fmt = schema.get("format")
    enum = schema.get("enum")
    example = schema.get("example")
    name_lower = prop_name.lower()

    # UUID
    if fmt == "uuid" or (ptype == "string" and "uuid" in name_lower):
        hint_parts.append("Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000')")
    # Date/timestamp
    elif any(k in name_lower for k in ("_at", "date", "timestamp")) and ptype in ("integer", "number"):
        hint_parts.append(
            "Unix timestamp in **milliseconds** (not seconds, not ISO). "
            "Ex: 1730419200000 = 2024-11-01 00:00 UTC"
        )
    # Discount/percentage as fraction
    elif any(k in name_lower for k in ("discount", "pct", "percentage", "rate")) and ptype in ("number", "integer"):
        hint_parts.append("**Fraction 0 to 1 (NOT percent)**. Ex: 0.25 = 25%")

    # Enums
    if enum:
        quoted = ", ".join(f"'{v}'" for v in enum)
        if len(enum) <= 3:
            hint_parts.append(f"Allowed values: {quoted}")
        else:
            bullets = "\n  - ".join(f"'{v}'" for v in enum)
            hint_parts.append(
                f"Allowed values (case-sensitive, pass EXACTLY as listed):\n  - {bullets}"
            )

    # Array
    if ptype == "array":
        items = schema.get("items", {})
        item_type = items.get("type", "string")
        if items.get("enum"):
            quoted = ", ".join(f"'{v}'" for v in items["enum"])
            hint_parts.append(f"Pass a JSON array of values: [{quoted}]")
        else:
            hint_parts.append(f"Pass a JSON array of {item_type} values")

    # Example
    if example is not None and not enum:
        if isinstance(example, str):
            hint_parts.append(f"Example: '{example}'")
        else:
            hint_parts.append(f"Example: {example}")

    if not hint_parts:
        hint_parts.append(f"Type: {ptype or 'string'}")

    # Anti-vocab notes for body fields that LLMs often guess wrong.
    # (Observed in eval iterations: 'text' for `message`, 'audio_url/image_url/document_url' for `url`.)
    if prop_name == "message":
        hint_parts.append(
            "⚠️ Field name is EXACTLY `message`. Do NOT pass `text` — that field does not exist"
        )
    elif prop_name == "url":
        hint_parts.append(
            "⚠️ Field name is EXACTLY `url` (single field, regardless of media type). "
            "Do NOT pass `audio_url`, `image_url`, or `document_url` — none of those exist"
        )
    elif prop_name == "template_id":
        hint_parts.append(
            "⚠️ Field name is EXACTLY `template_id`. Do NOT pass `template_name` or `message_template_id`"
        )

    return ". ".join(hint_parts).strip()


def collect_op_params(spec: dict, op: dict) -> tuple[list[dict], dict | None]:
    """Return (parameters, body_schema) for an operation, with refs resolved."""
    params = [resolve(spec, p) for p in op.get("parameters", [])]
    # Skip the api-token header param — handled in client.py.
    params = [p for p in params if not (p.get("in") == "header" and p.get("name") == "api-token")]
    body_schema = None
    if "requestBody" in op:
        content = op["requestBody"].get("content", {}).get("application/json", {})
        body_schema = resolve(spec, content.get("schema"))
    return params, body_schema


def build_function(
    *,
    py_name: str,
    method: str,
    path: str,
    summary: str,
    description: str,
    params: list[dict],
    body_schema: dict | None,
) -> str:
    """Render a single async function as a string.

    Per SEP-1382: tool-level docstring describes WHAT/WHEN, while per-parameter
    Field(description=...) carries FORMAT/VALIDATION hints. Both reach the
    MCP client (docstring -> tool description; Field -> inputSchema.properties).
    """
    path_params = [p for p in params if p["in"] == "path"]
    query_params = [p for p in params if p["in"] == "query"]

    body_props: dict[str, dict] = {}
    body_required: set[str] = set()
    if body_schema:
        body_props = body_schema.get("properties") or {}
        body_required = set(body_schema.get("required") or [])

    def annotated(ptype: str, hint: str, required: bool) -> str:
        # Escape the hint for a Python string literal (raw multi-line string).
        safe = hint.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        if required:
            return f'Annotated[{ptype}, Field(description="""{safe}""")]'
        return f'Annotated[{ptype} | None, Field(description="""{safe}""")] = None'

    # Rename path params: `id` -> `<entity>_id`; camelCase already handled by safe_name.
    path_param_rename: dict[str, str] = {}
    for p in path_params:
        original = p["name"]
        if original == "id":
            entity = derive_entity_from_path(path, for_param="id")
            path_param_rename[original] = f"{entity}_id" if entity else "id_"
        else:
            path_param_rename[original] = safe_name(original)

    sig_parts: list[str] = []
    # Required: path params + required body fields.
    for p in path_params:
        h = render_hint(p["name"], p.get("schema") or {})
        py_name_p = path_param_rename[p["name"]]
        sig_parts.append(f"{py_name_p}: {annotated('str', h, True)}")
    for fname in body_required:
        h = render_hint(fname, body_props[fname])
        ptype = py_type_of(body_props[fname])
        sig_parts.append(f"{safe_name(fname)}: {annotated(ptype, h, True)}")
    # Optional: query params + non-required body fields.
    for p in query_params:
        ptype = py_type_of(p.get("schema", {}))
        desc_extra = p.get("description", "")
        h = render_hint(p["name"], p.get("schema") or {})
        if desc_extra and desc_extra not in h:
            h = f"{desc_extra.rstrip('.')}. {h}"
        sig_parts.append(f"{safe_name(p['name'])}: {annotated(ptype, h, False)}")
    for fname in body_props:
        if fname in body_required:
            continue
        h = render_hint(fname, body_props[fname])
        ptype = py_type_of(body_props[fname])
        sig_parts.append(f"{safe_name(fname)}: {annotated(ptype, h, False)}")

    sig = ", ".join(sig_parts)

    # Tool-level docstring (what/when only — no per-param hints; those live in Field).
    summary_clean = summary.strip()
    desc_clean = (description or summary).strip()
    if desc_clean and desc_clean != summary_clean:
        doc = f"{summary_clean}\n\n    {desc_clean}"
    else:
        doc = summary_clean
    doc += f"\n\n    Endpoint: {method} {path}"

    # Body of function: build path with substitutions, build params dict, build body dict.
    path_subst = path
    for p in path_params:
        path_subst = path_subst.replace("{" + p["name"] + "}", "{" + path_param_rename[p["name"]] + "}")

    body_lines: list[str] = []
    body_lines.append(f'    """{doc}\n    """')

    if query_params:
        body_lines.append("    _params = {")
        for p in query_params:
            sn = safe_name(p["name"])
            body_lines.append(f'        "{p["name"]}": {sn},')
        body_lines.append("    }")
    else:
        body_lines.append("    _params = None")

    if body_props:
        body_lines.append("    _body = {")
        for fname in body_props:
            sn = safe_name(fname)
            body_lines.append(f'        "{fname}": {sn},')
        body_lines.append("    }")
    else:
        body_lines.append("    _body = None")

    body_lines.append(
        f'    return await request("{method}", f"{path_subst}", params=_params, json_body=_body)'
    )

    return f"async def clint_{py_name}({sig}) -> Any:\n" + "\n".join(body_lines) + "\n"


def py_type_of(schema: dict) -> str:
    """Map an OpenAPI schema to a python type hint string."""
    t = schema.get("type")
    if t == "integer":
        return "int"
    if t == "number":
        return "float"
    if t == "boolean":
        return "bool"
    if t == "array":
        return "list"
    if t == "object":
        return "dict"
    return "str"


# --- Main --------------------------------------------------------------------

def main() -> None:
    spec = json.loads(SPEC_PATH.read_text())

    # Group operations by module name.
    by_module: dict[str, list[tuple[str, str, str, str, dict]]] = defaultdict(list)
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            method_u = method.upper()
            tool_name = TOOL_NAMES.get((method_u, path))
            if tool_name is None:
                raise SystemExit(f"Unmapped endpoint: {method_u} {path}")
            tag = (op.get("tags") or [DEFAULT_MODULE])[0]
            module = TAG_TO_MODULE.get(tag, DEFAULT_MODULE)
            by_module[module].append(
                (method_u, path, op.get("summary", ""), op.get("description", ""), op)
            )

    TOOLS_DIR.mkdir(parents=True, exist_ok=True)

    all_exports: list[str] = []
    for module, ops in sorted(by_module.items()):
        funcs: list[str] = []
        ops_sorted = sorted(ops, key=lambda x: TOOL_NAMES[(x[0], x[1])])
        for method, path, summary, description, op in ops_sorted:
            params, body = collect_op_params(spec, op)
            py_name = TOOL_NAMES[(method, path)]
            all_exports.append(f"clint_{py_name}")
            funcs.append(
                build_function(
                    py_name=py_name,
                    method=method,
                    path=path,
                    summary=summary,
                    description=description,
                    params=params,
                    body_schema=body,
                )
            )
        header = (
            f'"""Auto-generated tools for {module}. DO NOT EDIT — run generator."""\n'
            "from __future__ import annotations\n\n"
            "from typing import Annotated, Any\n\n"
            "from pydantic import Field\n\n"
            "from clint_mcp._shared import request\n\n\n"
        )
        (TOOLS_DIR / f"{module}.py").write_text(header + "\n\n".join(funcs))

    # Write __init__.py exporting everything.
    init_lines = ['"""Auto-generated tool registry."""']
    for module in sorted(by_module):
        init_lines.append(f"from clint_mcp.tools import {module} as _{module}  # noqa: F401")
    init_lines.append("")
    init_lines.append("ALL_TOOLS = [")
    for name in sorted(all_exports):
        # find which module owns it: scan modules
        for module in sorted(by_module):
            mod_tools = [TOOL_NAMES[(m, p)] for m, p, *_ in by_module[module]]
            if name.replace("clint_", "", 1) in mod_tools:
                init_lines.append(f"    _{module}.{name},")
                break
    init_lines.append("]")
    (TOOLS_DIR / "__init__.py").write_text("\n".join(init_lines) + "\n")

    print(f"Generated {len(all_exports)} tools across {len(by_module)} modules:")
    for module, ops in sorted(by_module.items()):
        print(f"  {module}: {len(ops)} tools")


if __name__ == "__main__":
    main()

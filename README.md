# clint-mcp

MCP server for the [Clint CRM API](https://clint-api.readme.io/reference/) (Brazilian, `https://api.clint.digital`).

**46 endpoints across 14 categories** — Contacts, Deals, Tags, Organizations, Groups, Lost Status, Origins, Users, Account, Channel Accounts, Message Templates, Chats, Messages (WhatsApp Official), Dashboards.

Built with [FastMCP](https://github.com/jlowin/fastmcp) + Code Mode (3 meta-tools: `search` / `get_schema` / `execute`).

## Quality

Validated with **414-prompt eval** (3 personas × 46 tools × 3 variations, programmatic judge):

| Metric | Value |
|---|---|
| Tool selection accuracy | **100%** (414/414) |
| Parameter shape accuracy | **97.3%** (403/414) |
| Both correct | **97.3%** |
| Threshold (skill standard ≥ 0.95) | ✅ PASS |

Personas covered: iniciante coloquial (Carla, mentoria solo), intermediário operacional (Felipe, SDR/Closer), avançado corporativo (Renata, Head Comercial). See `tests/personas.json` for full ICP-grounded profiles.

## Setup

```bash
uv venv && uv pip install -e .
export CLINT_API_TOKEN=<your-token>
clint-mcp
```

## Register in Claude Code

Edit `~/.claude.json`:

```json
{
  "mcpServers": {
    "clint": {
      "type": "stdio",
      "command": "/absolute/path/to/clint-mcp/.venv/bin/clint-mcp",
      "args": [],
      "env": {
        "CLINT_API_TOKEN": "<your-token>"
      }
    }
  }
}
```

Then `/exit` and reopen Claude Code.

## Configuration

| Env var | Default | Purpose |
|---|---|---|
| `CLINT_API_TOKEN` | (required) | API token sent as `api-token` header |
| `CLINT_MAX_RPS` | `5` | Client-side rate limit (requests/second) |

## Coverage

| Category | Tools | Notes |
|---|---|---|
| Contacts | 8 | list / get / create / update / delete + attachments + tags add/remove |
| Deals | 5 | list / get / create / update / delete |
| Tags | 4 | list / get / create / delete |
| Organizations | 2 | get / update |
| Groups | 2 | list / get |
| Lost Status | 2 | list / get |
| Origins | 2 | list / get |
| Users | 2 | list / get |
| Account | 1 | list custom fields |
| Channel Accounts | 2 | list / get — WhatsApp Official |
| Message Templates | 2 | list / get — HSM templates |
| Chats | 3 | get + list by contact + list by channel |
| Messages | 7 | list by chat + get + send (text/image/audio/document/template) |
| Dashboards | 4 | list / get / data + single chart data |
| **Total** | **46** | |

## Regenerating tools

```bash
python -m clint_mcp.generator
```

Reads `specs/openapi.json` (consolidated from 46 ReadMe `.md` pages in `specs/endpoints/`) and rewrites `src/clint_mcp/tools/*.py`.

## Re-running the eval

```bash
python scripts/judge.py
```

Regenerating candidates requires re-dispatching subagents (manual). See `tests/` for current prompts/candidates/results.

## Design notes

- **Code Mode by default** — All 46 tools collapsed into 3 meta-tools (`search`/`get_schema`/`execute`) regardless of fleet size, scales better with token budget.
- **Hints in `inputSchema.properties[].description`** (SEP-1382 compliant), not in tool-level docstring — agents read per-param descriptions reliably; truncated docstrings would drop them.
- **Anti-vocab hints with ⚠️** for body fields where LLM intuition diverges from API truth (`message` vs `text`, `url` vs `audio_url`/`image_url`, `template_id` vs `template_name`). These single-handedly moved param accuracy from 73% → 97% in iteration 3 of the eval.
- **Path `id` renamed semantically** — `/v1/contacts/{id}` exposes `contact_id` (not `id_`). LLMs guess entity-prefixed names; aligning saved ~110 failure modes.
- **CamelCase paths → snake_case params** — `/v2/chats/contact/{contactId}` accepts `contact_id` in the Python signature; substitution back to `contactId` happens in URL build.

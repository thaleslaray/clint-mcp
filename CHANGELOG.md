# Changelog

## 0.2.0 — 2026-05-14

Alignment with the established `<name>-mcp` project layout (matches hotmart-mcp conventions) + Prefab Apps.

### Added

- **`src/clint_mcp/apps/`** — Prefab Apps directory with `clint_dashboard_view(dashboard_id)` tool that fetches Clint dashboard metadata + data and renders charts visually (KPIs as Metric, time series as LineChart, bars as BarChart, tables as DataTable).
- **`src/clint_mcp/_shared.py`** — lazy `ClintClient` singleton isolated from `client.py`, mirroring the hotmart pattern. Tools now `from clint_mcp._shared import request`.
- **`CLAUDE.md`** — project conventions, regen flow, naming rules, hint architecture, eval pipeline.
- **`uv.lock`** — committed lockfile for reproducible builds (76 packages resolved).

### Changed

- **`docs/` → `specs/`** — OpenAPI spec dir renamed to match the convention.
- **Eval data moved to `scripts/`** — `personas-infoprodutor.json`, `prompts-persona-{A,B,C}.json`, `eval-cases.json`, `eval-results.json`, `eval-report.md` now live alongside `judge.py`.
- **`client.py` refactored** — `ClintClient` is now a proper class (was free functions + module globals). Backwards-compatible via `_shared.request`.
- **`pyproject.toml`** — bumped to `fastmcp[apps]` to pull `prefab-ui` for the new dashboard app.

### Migration notes

If you had `clint-mcp` v0.1.0 installed, upgrade is a no-op for tool callers — the 46 tool signatures and names are unchanged. Only internal imports moved (`clint_mcp.client.request` → `clint_mcp._shared.request`); the public CLI binary `clint-mcp` and `/clint:configure` flow are identical.

---

## 0.1.0 — 2026-05-14

Initial release.

### Features

- **46 endpoints** across 14 categories covering Contacts, Deals, Tags, Organizations, Groups, Lost Status, Origins, Users, Account, Channel Accounts, Message Templates, Chats, Messages (WhatsApp Official: text/image/audio/document/template), Dashboards.
- **FastMCP + Code Mode** — All tools collapsed into 3 meta-tools (`search`/`get_schema`/`execute`) via `MontySandboxProvider`.
- **Async HTTP client** with client-side rate limiting (default 5 req/s, configurable via `CLINT_MAX_RPS`).
- **Per-parameter hints** in `inputSchema.properties[].description` — UUID format, date timestamps, enums, fraction-vs-percent, anti-vocab warnings for body fields.

### Quality

- **414-prompt eval passed** (3 personas × 46 tools × 3 variations) with `both_correct = 97.3%`, above the `≥ 0.95` skill threshold.
- 100% tool selection accuracy across all personas.
- Personas grounded in real ICP research (iniciante coloquial / intermediário operacional / avançado corporativo).

### Generator iterations during dev

| Iter | both_correct | Key change |
|---|---|---|
| 1 | 59.2% | Raw OpenAPI spec, `id_` for path params |
| 2 | 73.4% | Path `id` → entity-semantic name (`contact_id`/`deal_id`/etc); camelCase → snake_case |
| 3 | 97.3% | ⚠️ Anti-vocab hints on body fields (`url` not `audio_url`, `message` not `text`, `template_id` not `template_name`) |

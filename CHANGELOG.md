# Changelog

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

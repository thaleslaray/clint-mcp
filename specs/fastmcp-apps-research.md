# FastMCP Apps + Prefab UI — Research Report

**Date:** 2026-05-14
**Versions inspected (installed locally):** `fastmcp` (current main), `prefab-ui==0.19.1`
**Local install path:** `/Users/thaleslaray/code/projetos/mcp/clint-mcp/.venv/lib/python3.13/site-packages/`
**Upstream docs:** https://github.com/PrefectHQ/fastmcp/tree/main/docs/apps
**Upstream examples:** https://github.com/PrefectHQ/fastmcp/tree/main/examples/apps
**Note:** The `gofastmcp.com/servers/apps` URL given in the brief 404s — the live docs live under `gofastmcp.com/apps/*` (overview, prefab, fastmcp-app, generative, low-level, providers, examples). Source-of-truth for this report is the installed Python code plus the `.mdx` docs in the PrefectHQ/fastmcp repo.

---

## 1. The big picture

FastMCP "Apps" is FastMCP's implementation of the **MCP Apps extension** (`io.modelcontextprotocol/ui`). A tool returns an interactive UI instead of a text blob, and the host renders it inline in the conversation.

There are **four paths**, increasing in complexity:

| Path | Decorator/API | Use when |
|---|---|---|
| **Interactive Tool** | `@mcp.tool(app=True)` | Read-only viz: chart, table, dashboard, single-screen UI with client-side state only |
| **FastMCPApp** | `FastMCPApp("name")` + `@app.ui()` + `@app.tool()` | UI calls back to backend (forms, CRUD, search) and you want stable identifiers under composition |
| **Generative UI** | `mcp.add_provider(GenerativeUI())` | LLM writes Prefab Python at runtime, sandbox executes it, user watches UI stream in |
| **Custom HTML** | Register a resource with raw HTML | You need a map, 3D scene, your own framework — Prefab isn't enough |

Install: `pip install "fastmcp[apps]"` (pulls `prefab-ui`). **Pin `prefab-ui` yourself** — FastMCP only sets a lower bound and the lib has frequent breaking changes (per official PrefabPinWarning snippet).

---

## 2. Wire-level architecture

### Tool meta
Every Prefab tool carries `meta["ui"]` (camelCase on the wire under key `ui` per the `io.modelcontextprotocol/ui` extension). Two flavors:

1. Bare placeholder `{"resourceUri": "ui://prefab/renderer.html"}` — set by `app=True` or by a return-type annotation of `PrefabApp`/`Component`. The server's `_rewrite_prefab_uris` rewrites this at list-tools time to a per-tool hashed URI `ui://prefab/tool/<hash>/renderer.html`, and `synthesize_prefab_resources` lazily generates the HTML + CSP on demand.
2. Fully-formed dict from `PrefabAppConfig`, with merged CSP/permissions/visibility.

### Renderer
The renderer is a self-contained HTML page (`prefab_ui/renderer/app.html`) that loads either inline-bundled JS/CSS or a CDN stub. Initial wire payload is baked in as a JSON `<script id="prefab:initial-data">` blob.

### Tool result
When a Prefab tool returns a `Component` or `PrefabApp`, `fastmcp.tools.base._prefab_to_tool_result` wraps it: the wire `structuredContent` carries the serialized component tree; the textual `content` defaults to `"[Rendered Prefab UI]"`. For models that need data, return a `ToolResult(content=..., structured_content=view)` explicitly.

---

## 3. `@mcp.tool(app=True)` — the decorator

Defined in `fastmcp/server/server.py:1586`. Signature accepts:

```python
app: AppConfig | dict[str, Any] | bool | None = None
```

Behavior:
- `app=True` → stamps `meta["ui"] = True`, the LocalProvider's `_maybe_apply_prefab_ui` then sets the placeholder URI.
- `app=PrefabAppConfig(...)` → auto-wires the Prefab renderer URI **and** merges the renderer's required `connect_domains` / `resource_domains` into the CSP you supply.
- `app=AppConfig(...)` → manual control (resource_uri, visibility, csp, permissions, domain, prefersBorder).
- `app=False` / `None` → no UI (regular tool).
- **Return-type inference**: if `app` is unset but the return type annotation is `PrefabApp`, `Component`, or any union containing them, FastMCP infers `app=True` automatically (`_has_prefab_return_type` in `local_provider/decorators/tools.py:66`).

**Bypass of CodeMode?** Not a special bypass mechanism — Prefab tools are tagged via meta and re-dispatched by the server (`_rewrite_prefab_uris`, hashed backend names). When a server uses CodeMode transforms, the wrapped Prefab tools are still routed via the regular tool path. There's no documented incompatibility, but the renderer/CSP needs the original tool meta intact, so wrapping a Prefab tool inside CodeMode would lose its UI metadata. **For our `clint-mcp` (Code Mode enabled): Prefab tools must be exposed directly, outside the Code Mode transform.**

**Self-calling pattern:** A Prefab tool that calls itself via `CallTool` to refresh state, gated on visibility, is the natural pattern for "open dashboard → user clicks refresh → re-render with new data".

---

## 4. Complete component catalog (prefab-ui 0.19.1)

Discovered from `prefab_ui/components/__init__.py`. Every name is importable directly from `prefab_ui.components` unless noted.

### Layout / containers
| Name | Notes |
|---|---|
| `Column` | Vertical stack, `gap` arg |
| `Row` | Horizontal flex, `gap`, `align` |
| `Grid` / `GridItem` | Auto-flow grid with `columns`, `gap` |
| `Dashboard` / `DashboardItem` | **Explicit 1-indexed grid placement** (`col`, `row`, `col_span`, `row_span`) — for true dashboard layouts vs. auto Grid |
| `Container` | Generic constrained-width wrapper |
| `Div` / `Span` / `Link` | Primitive HTML wrappers |
| `Card` / `CardHeader` / `CardTitle` / `CardDescription` / `CardContent` / `CardFooter` | shadcn-style card composition |
| `Separator` | Horizontal rule |
| `Slot` | Named slot for `Define`/`Use` reusable components |

### Typography / text
| Name | Notes |
|---|---|
| `Heading` | level 1–4 |
| `H1` `H2` `H3` `H4` | direct heading shortcuts |
| `Text` | inline text, `css_class` for tailwind |
| `P` `Lead` `Large` `Small` `Muted` `BlockQuote` | semantic text |
| `Code` | inline code / code block |
| `Markdown` | renders MD |
| `Kbd` | keyboard glyph |

### Inputs / forms
| Name | Notes |
|---|---|
| `Form` | Container, `on_submit`, `Form.from_model(PydanticModel)` auto-generates fields |
| `Field` / `FieldTitle` / `FieldDescription` / `FieldContent` / `FieldError` / `ChoiceCard` | Manual form field composition |
| `Input` | text/email/number/password/url/tel/date/datetime-local — type auto-inferred from Pydantic |
| `Textarea` | multi-line |
| `Select` / `SelectOption` / `SelectGroup` / `SelectLabel` / `SelectSeparator` | Dropdown |
| `Combobox` / `ComboboxOption` / `ComboboxGroup` / `ComboboxLabel` / `ComboboxSeparator` | Searchable select |
| `Checkbox` | boolean |
| `Switch` | toggle |
| `Radio` / `RadioGroup` | single-choice |
| `Slider` | range, `min`, `max`, `value`, `name` |
| `DatePicker` | calendar popover |
| `Calendar` | inline calendar |
| `Label` | form label |
| `DropZone` | drag-drop file upload |

### Display / data
| Name | Notes |
|---|---|
| `DataTable` / `DataTableColumn` / `ExpandableRow` | TanStack Table — sort/search/paginate, accepts `pd.DataFrame`, components allowed as cell values, expandable rows with `detail=Component` |
| `Table` / `TableHeader` / `TableBody` / `TableFooter` / `TableRow` / `TableHead` / `TableCell` / `TableCaption` | Raw shadcn Table |
| `Metric` | KPI card — `label`, `value`, `delta`, `trend`, `trend_sentiment` (auto-color) |
| `Badge` | pill, `variant` |
| `Dot` | status dot |
| `Progress` | linear progress bar |
| `Ring` | circular progress |
| `Loader` | spinner |

### Charts (`prefab_ui.components.charts`)
Built on Recharts + shadcn ChartContainer. All accept `data` as `list[dict]` or `Rx`.

| Name | Notes |
|---|---|
| `BarChart` | `series=[ChartSeries(...)]`, `stacked`, `horizontal`, `bar_radius`, `y_axis_format="compact"` |
| `LineChart` | `curve="linear"/"smooth"/"step"`, `show_dots` |
| `AreaChart` | Combines line + fill, `stacked` |
| `PieChart` | `data_key`, `name_key`, `inner_radius` (>0 = donut) |
| `RadarChart` | `axis_key`, `filled` |
| `RadialChart` | concentric rings, `start_angle`/`end_angle` |
| `ScatterChart` | `x_axis`, `y_axis`, optional `z_axis` (bubble) |
| `Sparkline` | Compact inline trend — flat `list[int\|float]`, `variant`, `fill`, `mode="line"\|"bar"` |
| `Histogram` | Distribution chart (top-level component, not under charts) |
| `ChartSeries` | `data_key`, `label`, `color` |

### Media
| Name | Notes |
|---|---|
| `Image` | `src`, `alt` |
| `Video` | HTML5 video |
| `Audio` | HTML5 audio |
| `Icon` | Lucide icon by name |
| `Svg` | inline SVG |
| `Mermaid` | diagram rendering |
| `Embed` | iframe / inline HTML (used in `map_server.py` for Leaflet) |
| `Carousel` | image carousel |

### Overlays / interactive
| Name | Notes |
|---|---|
| `Dialog` | modal |
| `Popover` | floating panel |
| `Tooltip` | hover tooltip |
| `HoverCard` | rich hover card |
| `Alert` / `AlertTitle` / `AlertDescription` | banner |
| `Accordion` / `AccordionItem` | collapsible sections |
| `Tabs` / `Tab` | tabbed panels |
| `Pages` / `Page` | multi-page navigation (stateful, holds current page) |
| `Button` / `ButtonGroup` | `variant="default"/"outline"/"destructive"/"success"/"info"/"secondary"`, `on_click=Action(s)` |

### Control flow (`prefab_ui.components.control_flow`)
| Name | Notes |
|---|---|
| `If(condition)` | Conditional — accepts a string expr, an `Rx`, or comparison: `If(STATE.x > 0)`, `If(~STATE.decided)` |
| `Elif(...)` / `Else()` | Sibling branches |
| `ForEach("items")` | Loop; supports `with ForEach("x") as (idx, item):` destructuring → `ITEM`/`INDEX` reactive refs |

**Counts:** ~85 distinct component classes (excluding mere subparts). The brief listed Column/Row/Heading/Text/Metric/BarChart/LineChart/DataTable/Tabs/Tab/Card/Form/Button/Image/Markdown/Mermaid — all present. Notable additions: **Dashboard/DashboardItem (explicit placement), Sparkline, Ring, Carousel, Accordion, Combobox, DropZone, Pages, Embed**.

---

## 5. State, reactivity, and actions

### `STATE` proxy & `Rx`
```python
from prefab_ui.rx import STATE, Rx, ITEM, INDEX, EVENT, ERROR, RESULT

STATE.region              # == Rx("region")
STATE.user.email          # dot-path → Rx("user.email")
Rx("count") + 1           # → {{ count + 1 }} (Python operators compile to template expressions)
(Rx("count") > 0).then("yes", "no")  # ternary
Rx("revenue").currency()  # pipes: currency, percent, number, round, compact, abs, date, time, datetime, upper, lower, truncate, pluralize, length, join, first, last, selectattr, rejectattr, default
```

Five built-in reactive vars:
- `ITEM` / `INDEX` — current `ForEach` item and index (`$item`, `$index`)
- `EVENT` — value in `on_change`/`on_submit` (`$event`)
- `ERROR` — error message in `on_error` (`$error`)
- `RESULT` — return value in `on_success` (`$result`)

### Actions (`prefab_ui.actions`)
**Client-side (no round-trip):**
- `SetState(key, value)`
- `ToggleState(key)`
- `AppendState(key, value)`
- `PopState(key, index)`
- `ShowToast(message, variant="success"/"error"/"info"/...)`
- `CloseOverlay()`
- `OpenLink(url)`
- `OpenFilePicker(...)` / `FileUpload(...)`
- `SetInterval(action, ms)` — periodic re-fire (used by system_monitor for auto-refresh)
- `Fetch(url, ...)` — direct browser fetch to allowed domains
- `CallHandler(name)` — invoke a custom `js_actions`/`js_pipes` registered on `PrefabApp`

**MCP transport (`prefab_ui.actions.mcp`):**
- `CallTool(tool, arguments={}, on_success=[...], on_error=[...], result_key="...")` — accepts a string name OR a direct function reference (resolved to a hashed global name at serialize time)
- `SendMessage(content)` — push a message into the chat as if the user typed it (this is how Approval/Choice flow user decisions back to the LLM)
- `UpdateContext(content=..., structured_content=...)` — feed model context without triggering a response
- `RequestDisplayMode("inline"/"fullscreen"/"pip")` — ask host to change display mode (host may refuse)

**Composing:** any handler accepts a single action or a list. Lists execute in order and short-circuit on error.

### `let` bindings
The `with Column(let={"data": "{{ region == 'south' ? south : north }}"})` pattern in the reactive demo creates a local derived binding scoped to the subtree — like a computed/memo. Children read `Rx("data")` and it recomputes when its inputs change.

### Keyboard shortcuts
`PrefabApp(key_bindings={"Ctrl+Enter": SubmitAction, ...})` — handled by the renderer, supports `Shift+`/`Ctrl+`/`Alt+`/`Meta+` modifiers on any `KeyboardEvent.key`.

### `on_mount`
`PrefabApp(on_mount=action)` runs at app boot — e.g. fire `CallTool("refresh_data")` to populate state on open.

---

## 6. `FastMCPApp` — when the UI calls back

```python
from fastmcp import FastMCP, FastMCPApp
app = FastMCPApp("Contacts")

@app.tool()                     # visibility=["app"] (UI-only)
def save_contact(data: ContactModel) -> list[dict]: ...

@app.tool(model=True)           # visibility=["app", "model"]
def list_contacts() -> list[dict]: ...

@app.ui()                       # visibility=["model"] — entry point
def contact_manager() -> PrefabApp: ...

mcp = FastMCP("Contacts Server", providers=[app])
```

Why use it over `@mcp.tool(app=True)` + plain `@mcp.tool` for backends:

1. **Visibility defaults** are correct out of the box — model sees only `@app.ui` entry points.
2. **Tool resolver**: when `PrefabApp.to_json` serializes, a context-scoped resolver rewrites function references to hashed names like `<hash>_save_contact`. That means `CallTool(save_contact)` keeps working even when you mount the provider under a namespace (`fastmcp_dashboard___save_contact` would have broken).
3. **Composition safety**: providers can be added to multiple servers, mounted with prefixes, etc.

The full contact-manager example (`examples/apps/contacts/contacts_server.py`) demonstrates: `Form.from_model(ContactModel, on_submit=CallTool(save_contact, on_success=[SetState("contacts", RESULT), ShowToast(...)]))` — the entire CRUD loop in ~50 lines.

---

## 7. Built-in providers (`fastmcp.apps.*`)

These are pre-built `FastMCPApp` subclasses you `mcp.add_provider(...)`:

| Provider | Tool exposed | Purpose |
|---|---|---|
| `Approval()` | `request_approval(summary, details=None, ...)` | Human-in-the-loop OK/cancel card. Buttons send `SendMessage('"<summary>" — I selected: Approve/Reject')` into chat. Tool description includes strong instruction: *"After calling this tool, you MUST stop and wait"*. |
| `Choice()` | `choose(prompt, options: list[str])` | Pick one of N. Same SendMessage pattern. |
| `FormInput(model=PydanticModel)` | `collect_<model>` | Auto-generates form from Pydantic. `on_submit` callback receives validated instance, returns string to LLM. |
| `FileUpload(...)` | file picker / drag-drop |
| `GenerativeUI()` | `generate_prefab_ui(code)` + `search_prefab_components(query)` | LLM writes Prefab code, runs in Pyodide sandbox, UI streams in via `ontoolinputpartial`. |

---

## 8. CSP, permissions, display modes

### CSP (`fastmcp.apps.ResourceCSP`)
- `connect_domains` — fetch/XHR/WebSocket (Fetch action)
- `resource_domains` — script-src, img-src, style-src, font-src
- `frame_domains` — frame-src (nested iframes / Embed component)
- `base_uri_domains` — base-uri

`PrefabAppConfig` auto-merges Prefab renderer's own required domains with yours.

### Permissions (`fastmcp.apps.ResourcePermissions`)
Iframe sandbox feature requests (host may honor or deny):
- `camera`, `microphone`, `geolocation`, `clipboard_write`

### Display modes
Via `RequestDisplayMode` action — `"inline"` (default in chat), `"fullscreen"`, `"pip"` (picture-in-picture). Host decides.

---

## 9. Limitations and gotchas

1. **`prefab-ui` is unstable** — pin in your `pyproject.toml` (FastMCP only sets lower bound). 0.19.1 today is what we have.
2. **Bundle size**: in `"bundled"` renderer mode the entire JS/CSS is inlined into every tool's HTML response. For `"cdn"` mode a stub loads from jsDelivr pinned to your installed prefab-ui version — much smaller wire payload but needs network access from the host iframe.
3. **Code Mode interaction**: Prefab tools must be exposed outside any CatalogTransform that rewrites tool meta (CodeMode, etc.) — their `meta["ui"]` and synthesized resource URIs need to survive to the wire.
4. **Float / NaN sanitization**: `_sanitize_floats` replaces non-finite floats with `null` for JSON safety — keep that in mind if you push raw numpy/pandas data.
5. **State keys starting with `$` are reserved** (`$item`, `$index`, `$event`, `$error`, `$result`) — `PrefabApp` raises if you try.
6. **No `add_resource` on `FastMCPApp`** without going through `_local` directly — design is tool-centric.
7. **Tool result text for the model** defaults to literal `"[Rendered Prefab UI]"`. If the model needs to reason about what was shown, return `ToolResult(content="...summary...", structured_content=view)`.
8. **Client compat**: Apps require a host that implements the `io.modelcontextprotocol/ui` extension. Claude Desktop supports it via the MCP Apps spec; bare `npx @modelcontextprotocol/inspector` shows the structured content as JSON. Claude Code (CLI) — at time of writing — does **not** render Prefab UIs interactively. `fastmcp dev apps <server.py>` ships a local dev renderer for previewing.
9. **Form submit + checkboxes**: HTML omits unchecked boxes entirely; `FormInput._backfill_boolean_defaults` patches this server-side, but if you build forms manually you need to handle it.
10. **Top-level Pydantic models in `Form.from_model`**: nested models (`Address` field on `Contact`) are not auto-rendered as nested form sections in 0.19.

---

## 10. Best practices (from official docs + example code)

- **Start with the smallest upgrade**: replace a JSON-dump tool with `@mcp.tool(app=True)` returning a `DataTable`. Single-line win.
- **Compose in Python with context managers**: indentation = layout. `with PrefabApp() as app: with Column(): with Row(): Metric(...)`. The `__enter__`/`__exit__` machinery captures children into the parent.
- **Use `Card` to group**: shadcn-style `Card > CardHeader/CardContent/CardFooter` is the canonical "panel" unit.
- **Reactive over server-call when possible**: filtering, hide/show, tabs — keep client-side via `Rx`/`STATE`/`let`. Only `CallTool` when you need persistence or fresh data.
- **`Dashboard` vs `Grid`**: use `Dashboard` for newsroom-style explicit placements (chart spans cols 1-8, KPI sits at col 9-12). Use `Grid` for uniform N-up cards.
- **Auto-refresh**: `PrefabApp(on_mount=SetInterval(CallTool("refresh"), 5000))` — see `system_monitor`.
- **Tabs vs separate apps**: Tabs are great for sibling views of the same dataset (Overview / Details / Logs). Separate apps when the model legitimately needs separate entry points (= separate user intents).
- **Accessibility / dark mode**: themes are pre-built (`prefab_ui.themes`: `base`, `basic`, `minimal`, `presentation`). The renderer respects `prefers-color-scheme` and Tailwind tokens. Cards/buttons/badges use shadcn variants which are dark-mode aware.

---

## 11. Real-world examples (PrefectHQ/fastmcp `examples/apps/`)

| Example | File | Pattern |
|---|---|---|
| **sales_dashboard** | `sales_dashboard/sales_dashboard_server.py` | Single `@mcp.tool(app=True)` returns `Column` with `Grid(columns=4)` of `Metric` cards + 2-column `Grid` with `AreaChart` (col-span-2) + `PieChart` + `DataTable` of deals. KPIs computed server-side. **Strongest reference for a CRM dashboard.** |
| **contacts** | `contacts/contacts_server.py` | Full `FastMCPApp` with `@app.tool` (save/search) + `@app.ui` entry. `Form.from_model(ContactModel)`. `ForEach("contacts")` list. Manual search form. **Strongest reference for CRUD.** |
| **quiz** | `quiz/quiz_server.py` | Multi-turn client-side state. LLM passes questions, UI tracks score across answers, `SendMessage` returns final score to LLM. Buttons + `Progress` + conditional `If(Rx)` cards. |
| **system_monitor** | `system_monitor/system_monitor_server.py` | `SetInterval` auto-refresh, `psutil` backend, line chart accumulates ~100 points. |
| **map** | `map/map_server.py` | `Embed` with inline Leaflet HTML — proof Prefab can break out for niche viz. |
| **chart_server.py** | `examples/apps/chart_server.py` | Minimal — Heading + Muted + BarChart in <30 lines. |
| **greet_server.py** | `examples/apps/greet_server.py` | Two `@mcp.tool(app=True)` showing `Literal[...]` arg → renders Badge + Heading. |
| **patterns_server.py** | `examples/apps/patterns_server.py` | 14kb showcase of every pattern: Alert / Accordion / Tabs / Form / DataTable / charts. |
| **showcase_server.py** | `examples/apps/showcase_server.py` | 17kb mega-demo (basis of the hero docs iframe). |
| **inspector_demo.py** | `examples/apps/inspector_demo.py` | Buttons that exercise CallTool / SendMessage / UpdateContext + server logs — for verifying dev tooling. |
| **generative_ui.py** | `examples/apps/generative_ui.py` | 5 lines — just `mcp.add_provider(GenerativeUI())`. |

Plus dir-only examples: `approval/`, `approvals/`, `choice/`, `file_upload/`, `form/`, `explorer/`, `inventory/`, `qr_server/`.

---

## 12. App ideas for `clint-mcp` (CRM MCP)

Mapped to Clint's 14 endpoint categories. Each one fits the "single Prefab tool" pattern unless noted.

1. **Pipeline dashboard** (`pipeline_overview`) — Top-level `Dashboard(columns=12)`: 4 `Metric` KPIs (deals open, deals won MTD, conversion, ticket médio) across cols 1–12, `AreaChart` (stacked deals/stage over time) col-span 8, `PieChart` (won/lost/in-progress) col-span 4, `DataTable` of recent deals at the bottom. **Pure `@mcp.tool(app=True)` returning a Column.**
2. **Contact 360** (`contact_card`) — Single `Tabs`: Overview (Metric cards: total deals, ltv, last touchpoint), Deals (DataTable), Tags (Badge wall), Chats (timeline). Use `FastMCPApp` so editing tags / adding note can `CallTool("update_contact")`.
3. **Deal Kanban** (`deals_board`) — `Row` of `Column`s (one per stage) with `ForEach` over deals in each. Each card is a `Card` with `Metric` for value. Drag-drop would need custom JS — keep it click-to-advance with `Button` + `CallTool("move_deal_stage")`.
4. **WhatsApp inbox** (`whatsapp_chats`) — Split layout: left `Column` of chats (`ForEach`), right `Card` with conversation timeline + `Form` (Textarea + Button) → `CallTool("send_message")`. Classic FastMCPApp.
5. **Tag/Origin/Lost-status admin** (`taxonomy_editor`) — `Tabs` per taxonomy. Each tab: `DataTable` + `Form.from_model(TagModel)`. Approval action on delete via `Approval()` provider.
6. **New deal wizard** (`create_deal`) — `FormInput(model=DealModel)` with multi-step via `Pages`. On submit: validate, then `CallTool("create_deal")` → toast success.
7. **Bulk message composer** (`send_campaign`) — Audience filter (Select tag, date range), preview count `Metric` (live via `CallTool("estimate_audience")` on change), `Textarea` for template, `Button("Send")` gated by `Approval()`.
8. **Channel-account health** (`accounts_status`) — `Grid(columns=3)` of `Card`s per channel account, each with `Dot` for status, `Sparkline` of last 24h send volume, `Button("Reconnect")` only when disconnected.
9. **Lost-reason analytics** (`lost_analysis`) — `BarChart` horizontal with reasons, `DataTable` of recent lost deals filterable by reason via `Select` writing to `STATE.reason` and `let` filtering. Pure reactive — no `CallTool`.
10. **Daily briefing** (`brief_today`) — Returns a `ToolResult` with `content="<text summary for LLM>"` + `structured_content=view`. View has 3 cards: New leads, Deals at risk, Tasks due. **Sets the pattern for giving the model context while showing the user a UI.**

For an MCP that currently uses Code Mode (3 meta-tools), these would be **additional `app=True` tools registered directly on the FastMCP instance, outside the Code Mode transform**, so they keep their `meta["ui"]` intact through to the wire.

---

## 13. Quick-reference imports

```python
# Top-level
from fastmcp import FastMCP, FastMCPApp
from fastmcp.apps import AppConfig, PrefabAppConfig, ResourceCSP, ResourcePermissions
from fastmcp.apps.approval import Approval
from fastmcp.apps.choice import Choice
from fastmcp.apps.form import FormInput
from fastmcp.apps.generative import GenerativeUI

# Prefab
from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Column, Row, Grid, Card, CardContent, Heading, Text, Muted,
    Metric, Badge, Button, DataTable, DataTableColumn,
    Form, Input, Select, SelectOption, Switch,
    ForEach, If, Else,
)
from prefab_ui.components.charts import (
    BarChart, LineChart, AreaChart, PieChart, ChartSeries, Sparkline,
)
from prefab_ui.components.dashboard import Dashboard, DashboardItem
from prefab_ui.actions import SetState, AppendState, ShowToast, SetInterval
from prefab_ui.actions.mcp import CallTool, SendMessage, RequestDisplayMode
from prefab_ui.rx import STATE, Rx, ITEM, INDEX, EVENT, RESULT, ERROR
```

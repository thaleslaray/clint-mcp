"""Visual dashboard renderer for Clint CRM dashboards.

The Clint API returns dashboards as collections of typed charts (`number`,
`area`, `bar`, `pie`, `table`, etc.). This app fetches the full dashboard
payload and renders each chart with the matching Prefab component, so the
user sees the same visualization the Clint web UI shows.

Chart-type → component mapping:
  number  → Metric (single KPI value)
  area    → LineChart (time series, sorted by date asc)
  bar     → BarChart
  pie     → BarChart (Prefab doesn't ship Pie; bar gives same info)
  table   → DataTable
  other   → Heading + raw JSON in a Code block (fallback)
"""
from __future__ import annotations

from typing import Annotated, Any

from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Column,
    DataTable,
    DataTableColumn,
    Heading,
    Metric,
    Row,
    Text,
)
from prefab_ui.components.charts import BarChart, ChartSeries, LineChart
from pydantic import Field

from clint_mcp._shared import request


def _render_number(chart: dict) -> None:
    value = (chart.get("result") or {}).get("value")
    Metric(label=chart.get("name", "—"), value=str(value if value is not None else "—"))


def _render_area(chart: dict) -> None:
    result = chart.get("result") or []
    if not result:
        Text(f"{chart.get('name', '—')}: (sem dados)")
        return
    series = result[0]
    raw = sorted(series.get("data") or [], key=lambda x: x.get("date", ""))
    data = [{"date": p.get("date", "")[:10], "value": p.get("value", 0)} for p in raw]
    Heading(chart.get("name", "—"), level=3)
    LineChart(
        data=data,
        xAxis="date",
        series=[ChartSeries(dataKey="value", name=series.get("name", "Quantidade"))],
    )


def _render_bar(chart: dict) -> None:
    result = chart.get("result") or []
    if not result:
        Text(f"{chart.get('name', '—')}: (sem dados)")
        return
    # Clint shape varies; accept both [{label, value}] and series-style.
    if isinstance(result, list) and result and "label" in result[0]:
        data = [{"label": r.get("label", ""), "value": r.get("value", 0)} for r in result]
        Heading(chart.get("name", "—"), level=3)
        BarChart(data=data, xAxis="label", series=[ChartSeries(dataKey="value", name="Total")])
        return
    # Fallback to series shape.
    series = result[0]
    rows = series.get("data") or []
    data = [{"label": str(r.get("name") or r.get("date") or ""), "value": r.get("value", 0)} for r in rows]
    Heading(chart.get("name", "—"), level=3)
    BarChart(data=data, xAxis="label", series=[ChartSeries(dataKey="value", name=series.get("name", "Total"))])


def _render_table(chart: dict) -> None:
    result = chart.get("result") or []
    if not result or not isinstance(result, list):
        Text(f"{chart.get('name', '—')}: (sem dados)")
        return
    keys = list(result[0].keys()) if isinstance(result[0], dict) else []
    Heading(chart.get("name", "—"), level=3)
    DataTable(
        rows=result,
        columns=[DataTableColumn(header=k, accessor=k) for k in keys],
    )


def _render_fallback(chart: dict) -> None:
    Heading(chart.get("name", "—"), level=3)
    Text(f"Tipo `{chart.get('type', 'unknown')}` ainda não renderizado visualmente.")


CHART_RENDERERS = {
    "number": _render_number,
    "area": _render_area,
    "line": _render_area,
    "bar": _render_bar,
    "pie": _render_bar,
    "table": _render_table,
}


async def clint_dashboard_view_app(
    dashboard_id: Annotated[
        str,
        Field(description="UUID of the Clint dashboard to render. Use clint_dashboards_list to discover IDs."),
    ],
) -> PrefabApp:
    """Render a Clint dashboard visually with all its charts (KPIs, time series, tables).

    Fetches dashboard metadata + data in one call, then maps each chart by type
    to the appropriate Prefab component. Useful when the user wants to *see*
    a dashboard rather than read JSON.

    Endpoint: GET /v2/dashboards/{id} + GET /v2/dashboards/{id}/data
    """
    meta = await request("GET", f"/v2/dashboards/{dashboard_id}")
    data = await request("GET", f"/v2/dashboards/{dashboard_id}/data")
    title = (meta.get("data") or meta).get("name", "Clint Dashboard")
    pages = (data.get("data") or {}).get("pages") or []

    with Column(gap=6, cssClass="p-6") as view:
        Heading(title, level=1)
        # Metrics first (small chips in a row), then everything else stacked.
        all_charts = [c for page in pages for c in (page.get("charts") or [])]
        metrics = [c for c in all_charts if c.get("type") == "number"]
        others = [c for c in all_charts if c.get("type") != "number"]

        if metrics:
            with Row(gap=4, cssClass="flex-wrap"):
                for c in metrics:
                    CHART_RENDERERS["number"](c)

        for c in others:
            renderer = CHART_RENDERERS.get(c.get("type", ""), _render_fallback)
            renderer(c)

    return PrefabApp(view=view)

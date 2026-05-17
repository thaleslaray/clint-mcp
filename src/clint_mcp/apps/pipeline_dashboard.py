"""Pipeline Dashboard — KPIs do funil de vendas + breakdown por stage + top deals.

Difere do `clint_dashboard_view_app` (que renderiza um dashboard salvo no Clint):
este sintetiza um briefing operacional cruzando deals/origens/users, sem
depender de dashboard pré-configurado. Pra "como tá meu funil agora?".
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Annotated

from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Column,
    DataTable,
    DataTableColumn,
    Heading,
    Metric,
    Muted,
    Row,
)
from prefab_ui.components.charts import BarChart, ChartSeries, PieChart
from pydantic import Field

from clint_mcp._shared import request


async def _fetch_all_deals(
    *, status: str | None, since: datetime, until: datetime, hard_limit: int = 5000
) -> list[dict]:
    params: dict = {
        "created_at_start": since.isoformat(),
        "created_at_end": until.isoformat(),
        "limit": 1000,
    }
    if status:
        params["status"] = status
    out: list[dict] = []
    page = 1
    while True:
        chunk = await request("GET", "/v1/deals", params={**params, "page": page})
        data = chunk.get("data") or []
        out.extend(data)
        if not chunk.get("hasNext") or len(out) >= hard_limit:
            break
        page += 1
    return out


async def clint_pipeline_dashboard_app(
    days: Annotated[
        int,
        Field(description="Janela em dias retroativos. 7=semana, 30=mês, 90=trimestre. Default 30."),
    ] = 30,
) -> PrefabApp:
    """Pipeline Dashboard — briefing operacional do funil.

    KPIs (deals abertos, ganhos, perdidos, win rate, ticket médio), distribuição
    por etapa, breakdown ganho/perdido por origem, e top 10 deals em aberto por
    valor. Cobertura: criados na janela.
    """
    until = datetime.now(timezone.utc)
    since = until - timedelta(days=days)

    # Concurrent-ish fetch
    all_deals = await _fetch_all_deals(status=None, since=since, until=until)
    origins_resp = await request("GET", "/v1/origins", params={"limit": 200})
    origins = {o["id"]: o["name"] for o in (origins_resp.get("data") or [])}

    # Aggregations
    by_status: dict[str, int] = defaultdict(int)
    by_stage: dict[str, int] = defaultdict(int)
    won_value = 0.0
    lost_value = 0.0
    won_count = 0
    open_deals: list[dict] = []
    by_origin_won: dict[str, float] = defaultdict(float)
    by_origin_lost: dict[str, float] = defaultdict(float)

    for d in all_deals:
        status = d.get("status", "?")
        by_status[status] += 1
        stage = d.get("stage") or "(sem etapa)"
        by_stage[stage] += 1
        val = float(d.get("value") or 0)
        if status == "WON":
            won_value += val
            won_count += 1
            origin_name = origins.get(d.get("origin_id") or "", "(sem origem)")
            by_origin_won[origin_name] += val
        elif status == "LOST":
            lost_value += val
            origin_name = origins.get(d.get("origin_id") or "", "(sem origem)")
            by_origin_lost[origin_name] += val
        else:
            open_deals.append({
                "name": (d.get("contact") or {}).get("name") or d.get("title") or d["id"][:8],
                "value": val,
                "stage": stage,
                "origin": origins.get(d.get("origin_id") or "", "—"),
                "updated_at": d.get("updated_at", "")[:10],
            })

    open_deals.sort(key=lambda x: x["value"], reverse=True)

    total = sum(by_status.values())
    win_rate = (won_count / (won_count + by_status.get("LOST", 0))) if (won_count + by_status.get("LOST", 0)) else 0
    ticket_avg = (won_value / won_count) if won_count else 0

    stage_chart = [{"stage": s, "count": n} for s, n in sorted(by_stage.items(), key=lambda x: x[1], reverse=True)]
    status_pie = [{"name": s, "value": n} for s, n in by_status.items()]
    origin_won_chart = [{"origin": o, "won": v} for o, v in sorted(by_origin_won.items(), key=lambda x: x[1], reverse=True)[:10]]

    with Column(gap=6, cssClass="p-6") as view:
        Heading(f"Pipeline — últimos {days}d", level=1)
        Muted(f"{since.date().isoformat()} → {until.date().isoformat()}  •  {total} deals criados na janela")

        with Row(gap=4, cssClass="flex-wrap"):
            Metric(label="Abertos", value=str(by_status.get("OPEN", 0)))
            Metric(label="Ganhos", value=str(won_count))
            Metric(label="Perdidos", value=str(by_status.get("LOST", 0)))
            Metric(label="Win rate", value=f"{win_rate*100:.0f}%")
            Metric(label="Receita ganha", value=f"R$ {won_value:,.0f}")
            Metric(label="Ticket médio", value=f"R$ {ticket_avg:,.0f}")

        Heading("Distribuição por etapa", level=3)
        if stage_chart:
            BarChart(
                data=stage_chart,
                xAxis="stage",
                series=[ChartSeries(dataKey="count", name="Deals", color="#3b82f6")],
            )
        else:
            Muted("Sem dados.")

        with Row(gap=6):
            with Column(gap=2, cssClass="flex-1"):
                Heading("Status mix", level=3)
                if status_pie:
                    PieChart(data=status_pie, dataKey="value", nameKey="name")
                else:
                    Muted("Sem dados.")
            with Column(gap=2, cssClass="flex-1"):
                Heading("Receita por origem (ganhos)", level=3)
                if origin_won_chart:
                    BarChart(
                        data=origin_won_chart,
                        xAxis="origin",
                        series=[ChartSeries(dataKey="won", name="R$ ganho", color="#22c55e")],
                    )
                else:
                    Muted("Sem deals ganhos.")

        Heading("Top 10 deals abertos por valor", level=3)
        if open_deals:
            DataTable(
                rows=open_deals[:10],
                columns=[
                    DataTableColumn(key="name", header="Contato/Deal", sortable=True),
                    DataTableColumn(key="value", header="Valor", format="currency:BRL", sortable=True, align="right"),
                    DataTableColumn(key="stage", header="Etapa", sortable=True),
                    DataTableColumn(key="origin", header="Origem", sortable=True),
                    DataTableColumn(key="updated_at", header="Última atividade", sortable=True),
                ],
            )
        else:
            Muted("Sem deals abertos na janela.")

    return PrefabApp(view=view)

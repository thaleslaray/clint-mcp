"""Sales Performance leaderboard — KPIs + ranking per user (SDR/Closer).

Aggregates deals won/lost in a configurable window (default last 30 days)
grouped by `won_by` / `lost_by`. Renders as: KPI row, BarChart of revenue per
user, DataTable leaderboard with metrics, and Tabs for "By closer" / "By SDR
origin".
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Badge,
    Column,
    DataTable,
    DataTableColumn,
    Heading,
    Metric,
    Muted,
    Row,
    Tab,
    Tabs,
)
from prefab_ui.components.charts import BarChart, ChartSeries
from pydantic import Field

from clint_mcp._shared import request


async def _fetch_deals_in_window(
    *, status: str, since: datetime, until: datetime, hard_limit: int = 5000
) -> list[dict]:
    """Pull deals won or lost in [since, until], handling pagination."""
    key_start = "won_at_start" if status == "WON" else "lost_at_start"
    key_end = "won_at_end" if status == "WON" else "lost_at_end"
    params = {
        "status": status,
        key_start: since.isoformat(),
        key_end: until.isoformat(),
        "limit": 1000,
    }
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


def _fmt_money(n: float) -> str:
    if n >= 1_000_000:
        return f"R$ {n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"R$ {n/1_000:.0f}k"
    return f"R$ {n:,.0f}"


async def clint_sales_performance_app(
    days: Annotated[
        int,
        Field(description="Window in days to look back. Examples: 7 = última semana, 30 = último mês, 90 = trimestre. Default 30."),
    ] = 30,
) -> PrefabApp:
    """Sales performance leaderboard — ranking de closers por revenue e win rate.

    Mostra quem fechou mais (R$ e # deals) numa janela configurável.
    Útil pra:
      - Briefing semanal de gestor comercial.
      - Comparar SDR/Closer ranking pra calibragem de meta.
      - Ver se tem rep com win rate destoante.
    """
    # Time window
    until = datetime.now(timezone.utc)
    since = until - timedelta(days=days)

    # Fetch users + won/lost deals in parallel-ish (sequential here for client simplicity)
    users_resp = await request("GET", "/v1/users", params={"limit": 200})
    users = {u["id"]: u for u in (users_resp.get("data") or [])}

    won_deals = await _fetch_deals_in_window(status="WON", since=since, until=until)
    lost_deals = await _fetch_deals_in_window(status="LOST", since=since, until=until)

    # Aggregate per user
    won_count: dict[str, int] = defaultdict(int)
    won_value: dict[str, float] = defaultdict(float)
    lost_count: dict[str, int] = defaultdict(int)
    lost_value: dict[str, float] = defaultdict(float)

    for d in won_deals:
        uid = d.get("won_by") or "_unknown_"
        won_count[uid] += 1
        won_value[uid] += float(d.get("value") or 0)
    for d in lost_deals:
        uid = d.get("lost_by") or "_unknown_"
        lost_count[uid] += 1
        lost_value[uid] += float(d.get("value") or 0)

    # Build leaderboard rows
    user_ids = set(won_count) | set(lost_count)
    user_ids.discard("_unknown_")
    rows: list[dict] = []
    for uid in user_ids:
        u = users.get(uid, {})
        name = f"{u.get('first_name','')} {u.get('last_name','')}".strip() or u.get("email") or uid[:8]
        won_n = won_count.get(uid, 0)
        lost_n = lost_count.get(uid, 0)
        total_n = won_n + lost_n
        rows.append({
            "user": name,
            "won": won_n,
            "lost": lost_n,
            "revenue": won_value.get(uid, 0),
            "lost_value": lost_value.get(uid, 0),
            "win_rate": (won_n / total_n) if total_n else 0,
            "ticket_avg": (won_value.get(uid, 0) / won_n) if won_n else 0,
        })
    rows.sort(key=lambda r: r["revenue"], reverse=True)

    # No need to pre-format — DataTableColumn `format` handles currency/percent.

    # KPIs aggregated
    total_revenue = sum(r["revenue"] for r in rows)
    total_won = sum(r["won"] for r in rows)
    total_lost = sum(r["lost"] for r in rows)
    overall_win_rate = (total_won / (total_won + total_lost)) if (total_won + total_lost) else 0
    overall_ticket = (total_revenue / total_won) if total_won else 0

    chart_data = [{"user": r["user"], "revenue": r["revenue"]} for r in rows[:10]]

    with Column(gap=6, cssClass="p-6") as view:
        Heading(f"Sales Performance — últimos {days}d", level=1)
        Muted(f"Janela: {since.date().isoformat()} → {until.date().isoformat()}")

        with Row(gap=4, cssClass="flex-wrap"):
            Metric(label="Revenue total", value=_fmt_money(total_revenue))
            Metric(label="Deals fechados", value=str(total_won))
            Metric(label="Deals perdidos", value=str(total_lost))
            Metric(label="Win rate geral", value=f"{overall_win_rate*100:.0f}%")
            Metric(label="Ticket médio", value=_fmt_money(overall_ticket))

        with Tabs():
            with Tab(title="Ranking"):
                Heading("Revenue por rep (top 10)", level=3)
                if chart_data:
                    BarChart(
                        data=chart_data,
                        xAxis="user",
                        series=[ChartSeries(dataKey="revenue", name="Revenue", color="#22c55e")],
                    )
                else:
                    Muted("Nenhum deal fechado na janela.")
            with Tab(title="Leaderboard"):
                if rows:
                    DataTable(
                        rows=rows,
                        columns=[
                            DataTableColumn(key="user", header="Rep", sortable=True),
                            DataTableColumn(key="won", header="Won", sortable=True, align="right"),
                            DataTableColumn(key="lost", header="Lost", sortable=True, align="right"),
                            DataTableColumn(key="revenue", header="Revenue", format="currency:BRL", sortable=True, align="right"),
                            DataTableColumn(key="win_rate", header="Win rate", format="percent:0", sortable=True, align="right"),
                            DataTableColumn(key="ticket_avg", header="Ticket médio", format="currency:BRL", sortable=True, align="right"),
                            DataTableColumn(key="lost_value", header="$ perdido", format="currency:BRL", sortable=True, align="right"),
                        ],
                    )
                else:
                    Muted("Sem dados na janela escolhida.")

    return PrefabApp(view=view)

"""Deal Inbox — triagem visual de oportunidades (SDR/Closer).

Lista deals OPEN com filtros operacionais (owner, origem, tag, valor mínimo,
janela temporal). DataTable sortável + KPIs do recorte filtrado. Read-only
nesta versão; edição inline virá em v0.5+ via FastMCPApp.
"""
from __future__ import annotations

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
from pydantic import Field

from clint_mcp._shared import request


async def clint_deal_inbox_app(
    owner_email: Annotated[
        str | None,
        Field(description="Filtra por dono do deal via email do user (case-sensitive). Ex: 'thales@laray.com.br'. Omita pra ver todos."),
    ] = None,
    origin_id: Annotated[
        str | None,
        Field(description="Filtra por origem (UUID). Use clint_origins_list pra descobrir IDs."),
    ] = None,
    tag_names: Annotated[
        str | None,
        Field(description="Filtra por tag(s), separadas por vírgula. Ex: 'lead-quente,vip'."),
    ] = None,
    min_value: Annotated[
        float | None,
        Field(description="Valor mínimo do deal (R$). Filtrado client-side após fetch."),
    ] = None,
    days: Annotated[
        int,
        Field(description="Janela em dias retroativos baseada em updated_at. Default 30."),
    ] = 30,
    limit: Annotated[
        int,
        Field(description="Máximo de deals a retornar (já filtrados). Default 100, máx 500."),
    ] = 100,
) -> PrefabApp:
    """Deal Inbox — caixa de entrada de oportunidades em aberto.

    Use cases:
      - "Quais leads do Hotmart estão abertos há mais de 7 dias?"
      - "Meus deals com tag VIP ordenados por valor."
      - "O que tá em aberto acima de R$10k essa semana?"
    """
    until = datetime.now(timezone.utc)
    since = until - timedelta(days=days)

    params: dict = {
        "status": "OPEN",
        "updated_at_start": since.isoformat(),
        "updated_at_end": until.isoformat(),
        "limit": min(max(limit, 1), 500),
    }
    if owner_email:
        params["user_email"] = owner_email
    if origin_id:
        params["origin_id"] = origin_id
    if tag_names:
        params["tag_names"] = tag_names

    resp = await request("GET", "/v1/deals", params=params)
    deals = resp.get("data") or []
    total = resp.get("totalCount") or len(deals)

    # Fetch origin/user names for display
    origins_resp = await request("GET", "/v1/origins", params={"limit": 200})
    origins = {o["id"]: o["name"] for o in (origins_resp.get("data") or [])}
    users_resp = await request("GET", "/v1/users", params={"limit": 200})
    users = {u["id"]: f"{u.get('first_name','')} {u.get('last_name','')}".strip() or u.get("email") or u["id"][:8] for u in (users_resp.get("data") or [])}

    rows: list[dict] = []
    for d in deals:
        val = float(d.get("value") or 0)
        if min_value is not None and val < min_value:
            continue
        owner_uid = d.get("user_id") or ""
        contact = d.get("contact") or {}
        rows.append({
            "contact": contact.get("name") or "(sem nome)",
            "phone": contact.get("fullPhone") or contact.get("phone") or "—",
            "value": val,
            "stage": d.get("stage") or "—",
            "origin": origins.get(d.get("origin_id") or "", "—"),
            "owner": users.get(owner_uid, "—"),
            "updated_at": d.get("updated_at", "")[:10],
        })
    rows.sort(key=lambda x: x["value"], reverse=True)

    total_value = sum(r["value"] for r in rows)
    avg_value = (total_value / len(rows)) if rows else 0

    filter_chips: list[str] = []
    if owner_email:
        filter_chips.append(f"owner={owner_email}")
    if origin_id:
        filter_chips.append(f"origin={origins.get(origin_id, origin_id[:8])}")
    if tag_names:
        filter_chips.append(f"tags={tag_names}")
    if min_value:
        filter_chips.append(f"≥ R$ {min_value:,.0f}")
    filter_chips.append(f"últimos {days}d")
    filter_summary = "  •  ".join(filter_chips)

    with Column(gap=6, cssClass="p-6") as view:
        Heading("Deal Inbox", level=1)
        Muted(filter_summary)

        with Row(gap=4, cssClass="flex-wrap"):
            Metric(label="Deals filtrados", value=str(len(rows)))
            Metric(label="Valor somado", value=f"R$ {total_value:,.0f}")
            Metric(label="Ticket médio", value=f"R$ {avg_value:,.0f}")
            Metric(label="Total no período", value=str(total))

        if rows:
            DataTable(
                rows=rows,
                columns=[
                    DataTableColumn(key="contact", header="Contato", sortable=True),
                    DataTableColumn(key="phone", header="Telefone"),
                    DataTableColumn(key="value", header="Valor", format="currency:BRL", sortable=True, align="right"),
                    DataTableColumn(key="stage", header="Etapa", sortable=True),
                    DataTableColumn(key="origin", header="Origem", sortable=True),
                    DataTableColumn(key="owner", header="Owner", sortable=True),
                    DataTableColumn(key="updated_at", header="Última atualização", sortable=True),
                ],
            )
        else:
            Muted("Nenhum deal aberto bate com esses filtros.")

    return PrefabApp(view=view)

"""Contact 360 — visão consolidada de um contato.

Combina dados do contato + deals associados + chats WhatsApp + attachments.
Tabs separam Overview / Deals / Conversas / Anexos. Read-only nesta versão.
"""
from __future__ import annotations

from typing import Annotated

from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    Badge,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Code,
    Column,
    DataTable,
    DataTableColumn,
    Heading,
    Metric,
    Muted,
    Row,
    Tab,
    Tabs,
    Text,
)
from pydantic import Field

from clint_mcp._shared import request


async def clint_contact_360_app(
    contact_id: Annotated[
        str,
        Field(description="UUID do contato. Use clint_contacts_list pra descobrir. Format: UUID."),
    ],
) -> PrefabApp:
    """Contact 360 — perfil completo do contato com deals, conversas e anexos.

    Útil pra:
      - "Abre o perfil do João antes da call" — uma tela com tudo que precisa.
      - "Quero ver histórico do lead Maria — deals, conversas, arquivos."
    """
    # Fetch in sequence (could be parallel but client is rate-limited)
    contact_resp = await request("GET", f"/v1/contacts/{contact_id}")
    contact = contact_resp.get("data") or contact_resp

    deals_resp = await request("GET", "/v1/deals", params={"contact_id": contact_id, "limit": 100})
    deals = deals_resp.get("data") or []

    try:
        chats_resp = await request("GET", f"/v2/chats/contact/{contact_id}", params={"limit": 20})
        chats = chats_resp.get("data") or []
    except Exception:
        chats = []

    try:
        atts_resp = await request("GET", f"/v1/contacts/{contact_id}/attachments", params={"limit": 50})
        attachments = atts_resp.get("data") or []
    except Exception:
        attachments = []

    # Aggregates for KPIs
    deal_total = len(deals)
    won_deals = [d for d in deals if d.get("status") == "WON"]
    open_deals = [d for d in deals if d.get("status") == "OPEN"]
    lost_deals = [d for d in deals if d.get("status") == "LOST"]
    ltv = sum(float(d.get("value") or 0) for d in won_deals)

    # Pretty fields
    name = contact.get("name") or "(sem nome)"
    phone = contact.get("fullPhone") or contact.get("phone") or "—"
    email = contact.get("email") or "—"
    created = (contact.get("created_at") or "")[:10]
    tags = contact.get("tags") or []
    org = (contact.get("organization") or {}).get("name") or "—"

    # Rows
    deal_rows = [
        {
            "stage": d.get("stage") or "—",
            "value": float(d.get("value") or 0),
            "status": d.get("status", "—"),
            "updated_at": (d.get("updated_at") or "")[:10],
        }
        for d in deals
    ]
    deal_rows.sort(key=lambda x: x["updated_at"], reverse=True)

    chat_rows = [
        {
            "channel": (c.get("channel_account") or {}).get("name") or "—",
            "last_message_at": (c.get("last_message_at") or "")[:16].replace("T", " "),
            "status": c.get("status", "—"),
            "unread": c.get("unread_count", 0),
        }
        for c in chats
    ]
    chat_rows.sort(key=lambda x: x["last_message_at"], reverse=True)

    att_rows = [
        {
            "filename": a.get("name") or a.get("filename") or "—",
            "type": a.get("type") or a.get("content_type") or "—",
            "created_at": (a.get("created_at") or "")[:10],
            "url": a.get("url") or a.get("public_url") or "—",
        }
        for a in attachments
    ]

    with Column(gap=6, cssClass="p-6") as view:
        Heading(name, level=1)
        Muted(f"{phone}  •  {email}  •  Org: {org}  •  Cadastro: {created}")

        if tags:
            with Row(gap=2, cssClass="flex-wrap"):
                for t in tags:
                    tag_name = t.get("name") if isinstance(t, dict) else str(t)
                    Badge(tag_name)

        with Row(gap=4, cssClass="flex-wrap"):
            Metric(label="LTV (ganhos)", value=f"R$ {ltv:,.0f}")
            Metric(label="Deals totais", value=str(deal_total))
            Metric(label="Abertos", value=str(len(open_deals)))
            Metric(label="Ganhos", value=str(len(won_deals)))
            Metric(label="Perdidos", value=str(len(lost_deals)))
            Metric(label="Chats", value=str(len(chats)))
            Metric(label="Anexos", value=str(len(attachments)))

        with Tabs():
            with Tab(title=f"Overview"):
                with Card():
                    with CardHeader():
                        CardTitle("Dados básicos")
                    with CardContent():
                        Text(f"Nome: {name}")
                        Text(f"Telefone: {phone}")
                        Text(f"E-mail: {email}")
                        Text(f"Organização: {org}")
                        Text(f"Cadastro: {created}")
                fields = contact.get("fields") or {}
                if fields:
                    with Card():
                        with CardHeader():
                            CardTitle("Campos customizados")
                        with CardContent():
                            Code(str(fields), language="json")

            with Tab(title=f"Deals ({deal_total})"):
                if deal_rows:
                    DataTable(
                        rows=deal_rows,
                        columns=[
                            DataTableColumn(key="stage", header="Etapa", sortable=True),
                            DataTableColumn(key="value", header="Valor", format="currency:BRL", sortable=True, align="right"),
                            DataTableColumn(key="status", header="Status", sortable=True),
                            DataTableColumn(key="updated_at", header="Atualizado", sortable=True),
                        ],
                    )
                else:
                    Muted("Sem deals.")

            with Tab(title=f"Conversas ({len(chats)})"):
                if chat_rows:
                    DataTable(
                        rows=chat_rows,
                        columns=[
                            DataTableColumn(key="channel", header="Canal", sortable=True),
                            DataTableColumn(key="last_message_at", header="Última msg", sortable=True),
                            DataTableColumn(key="unread", header="Não lidas", sortable=True, align="right"),
                            DataTableColumn(key="status", header="Status"),
                        ],
                    )
                else:
                    Muted("Sem conversas registradas.")

            with Tab(title=f"Anexos ({len(attachments)})"):
                if att_rows:
                    DataTable(
                        rows=att_rows,
                        columns=[
                            DataTableColumn(key="filename", header="Arquivo", sortable=True),
                            DataTableColumn(key="type", header="Tipo"),
                            DataTableColumn(key="created_at", header="Adicionado", sortable=True),
                            DataTableColumn(key="url", header="URL"),
                        ],
                    )
                else:
                    Muted("Sem anexos.")

    return PrefabApp(view=view)

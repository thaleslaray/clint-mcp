"""WhatsApp Inbox — chats recentes de um channel account com preview de thread.

Default mostra os N chats mais recentes do channel; opcional `chat_id` foca em
uma conversa específica com a thread completa de mensagens. Read-only nesta
versão; envio de mensagens (composer) vem em v0.5+ via FastMCPApp.
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
    Column,
    DataTable,
    DataTableColumn,
    Heading,
    Metric,
    Muted,
    Row,
    Text,
)
from pydantic import Field

from clint_mcp._shared import request


async def clint_whatsapp_inbox_app(
    channel_account_id: Annotated[
        str | None,
        Field(description="UUID do channel account (WhatsApp Official). Se omitido, usa o primeiro disponível. Use clint_channel_accounts_list pra ver opções."),
    ] = None,
    chat_id: Annotated[
        str | None,
        Field(description="UUID de um chat específico pra abrir a thread completa de mensagens. Se omitido, mostra só a lista de chats recentes."),
    ] = None,
    limit: Annotated[
        int,
        Field(description="Quantos chats listar. Default 20, máx 100."),
    ] = 20,
) -> PrefabApp:
    """WhatsApp Inbox — caixa de entrada do WhatsApp Official.

    Lista chats recentes ordenados por última mensagem. Quando `chat_id` é
    passado, mostra também a thread completa de mensagens.
    """
    limit = min(max(limit, 1), 100)

    # Resolve channel account
    if not channel_account_id:
        ca_resp = await request("GET", "/v2/channel-accounts", params={"limit": 5})
        ca_list = ca_resp.get("data") or []
        if not ca_list:
            return PrefabApp(view=Column().__enter__().__class__())  # type: ignore[arg-type]
        channel_account_id = ca_list[0]["id"]
        channel_name = ca_list[0].get("name") or "(sem nome)"
    else:
        ca = await request("GET", f"/v2/channel-accounts/{channel_account_id}")
        channel_name = (ca.get("data") or ca).get("name") or "(sem nome)"

    # Chats list
    chats_resp = await request(
        "GET",
        f"/v2/chats/channel-account/{channel_account_id}",
        params={"limit": limit},
    )
    chats = chats_resp.get("data") or []

    # KPIs
    total_unread = sum(c.get("unseen_count", 0) for c in chats)
    not_seen = sum(1 for c in chats if not c.get("seen"))
    closed = sum(1 for c in chats if c.get("closed_at"))

    chat_rows = [
        {
            "contact": (c.get("contact") or {}).get("name") or "(sem nome)",
            "phone": (c.get("contact") or {}).get("fullPhone") or "—",
            "last_message_at": (c.get("last_message_at") or "")[:16].replace("T", " "),
            "unread": c.get("unseen_count", 0),
            "status": "fechado" if c.get("closed_at") else ("respondido" if c.get("replied") else "aberto"),
            "chat_id": c.get("id"),
        }
        for c in chats
    ]
    chat_rows.sort(key=lambda x: x["last_message_at"], reverse=True)

    # Optional thread
    thread_rows: list[dict] = []
    thread_chat = None
    if chat_id:
        msgs_resp = await request("GET", f"/v2/messages/chat/{chat_id}", params={"limit": 50})
        msgs = msgs_resp.get("data") or []
        msgs.sort(key=lambda m: m.get("created_at") or "")
        for m in msgs:
            ctype = m.get("content_type") or "TEXT"
            preview = m.get("content") or f"[{ctype}]"
            if ctype != "TEXT" and m.get("content_url"):
                preview = f"[{ctype}] {m.get('content_url')[:60]}..."
            thread_rows.append({
                "when": (m.get("created_at") or "")[:16].replace("T", " "),
                "from": "🤖 sistema/agent" if m.get("user_id") else "👤 cliente",
                "type": ctype,
                "preview": preview[:200],
            })
        thread_chat = next((c for c in chats if c.get("id") == chat_id), None)

    with Column(gap=6, cssClass="p-6") as view:
        Heading(f"WhatsApp Inbox", level=1)
        Muted(f"Canal: {channel_name}  •  {len(chats)} chats listados")

        with Row(gap=4, cssClass="flex-wrap"):
            Metric(label="Chats", value=str(len(chats)))
            Metric(label="Não lidos (msgs)", value=str(total_unread))
            Metric(label="Não vistos (chats)", value=str(not_seen))
            Metric(label="Fechados", value=str(closed))

        if thread_chat:
            contact = (thread_chat.get("contact") or {})
            with Card():
                with CardHeader():
                    CardTitle(f"💬 {contact.get('name', '(sem nome)')} — {contact.get('fullPhone', '')}")
                with CardContent():
                    if thread_rows:
                        DataTable(
                            rows=thread_rows,
                            columns=[
                                DataTableColumn(key="when", header="Quando", sortable=True),
                                DataTableColumn(key="from", header="De"),
                                DataTableColumn(key="type", header="Tipo"),
                                DataTableColumn(key="preview", header="Conteúdo"),
                            ],
                        )
                    else:
                        Muted("Sem mensagens nessa thread.")

        Heading("Chats recentes", level=3)
        if chat_rows:
            DataTable(
                rows=chat_rows,
                columns=[
                    DataTableColumn(key="contact", header="Contato", sortable=True),
                    DataTableColumn(key="phone", header="Telefone"),
                    DataTableColumn(key="last_message_at", header="Última msg", sortable=True),
                    DataTableColumn(key="unread", header="Não lidas", sortable=True, align="right"),
                    DataTableColumn(key="status", header="Status", sortable=True),
                    DataTableColumn(key="chat_id", header="Chat ID"),
                ],
            )
        else:
            Muted("Nenhum chat encontrado nesse channel.")

    return PrefabApp(view=view)

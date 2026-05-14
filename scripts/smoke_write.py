"""Smoke test of WRITE operation: send 1 text message to authorized phone."""
from __future__ import annotations

import asyncio

from clint_mcp._shared import aclose
from clint_mcp.tools.channel_accounts import clint_channel_accounts_list
from clint_mcp.tools.contacts import clint_contacts_list
from clint_mcp.tools.messages import clint_messages_text_send


AUTHORIZED_PHONE = "21982219966"
AUTHORIZED_DDI = "55"
MESSAGE = "🤖 [smoke test do clint-mcp] — pode ignorar, é só pra validar que send_text funciona end-to-end via MCP."


async def main() -> None:
    print("=" * 60)
    print("SMOKE WRITE — sends 1 message to 5521982219966")
    print("=" * 60)

    # 1. Find a channel account
    print("\n[1/3] Listing channel accounts...")
    ca = await clint_channel_accounts_list(limit=5)
    accounts = ca.get("data", [])
    if not accounts:
        print("✗ No channel accounts available — cannot send.")
        return
    channel = accounts[0]
    print(f"  ✓ {len(accounts)} account(s). Using: {channel.get('name', '(unnamed)')} -> {channel['id']}")

    # 2. Find the authorized contact by phone
    print(f"\n[2/3] Searching contact by phone ddi={AUTHORIZED_DDI} phone={AUTHORIZED_PHONE}...")
    cs = await clint_contacts_list(ddi=AUTHORIZED_DDI, phone=AUTHORIZED_PHONE, limit=5)
    contacts = cs.get("data", [])
    if not contacts:
        print(f"  ✗ No contact found with phone {AUTHORIZED_DDI}{AUTHORIZED_PHONE}.")
        print(f"     totalCount={cs.get('totalCount')}, raw={cs}")
        return
    contact = contacts[0]
    print(f"  ✓ Contact: {contact.get('name', '(unnamed)')} -> {contact['id']}")
    print(f"     fullPhone: {contact.get('fullPhone')}  email: {contact.get('email')}")

    # 3. Send the message
    print(f"\n[3/3] Sending message...")
    result = await clint_messages_text_send(
        channel_account_id=channel["id"],
        contact_id=contact["id"],
        message=MESSAGE,
    )
    print(f"  ✓ Sent. Response: {result}")
    await aclose()


if __name__ == "__main__":
    asyncio.run(main())

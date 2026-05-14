"""Auto-generated tools for chats. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_chats_by_channel_account_list(channel_account_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440000'""")], limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List chats by channel account

    Retrieve a paginated list of chats for a specific channel account. Results are sorted by last_message_at descending.

    Endpoint: GET /v2/chats/channel-account/{channelAccountId}
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v2/chats/channel-account/{channel_account_id}", params=_params, json_body=_body)


async def clint_chats_by_contact_list(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440000'""")], limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List chats by contact

    Retrieve a paginated list of chats for a specific contact. Results are sorted by last_message_at descending.

    Endpoint: GET /v2/chats/contact/{contactId}
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v2/chats/contact/{contact_id}", params=_params, json_body=_body)


async def clint_chats_get(chat_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get chat

    Retrieve a single chat by ID. Only returns chats belonging to the authenticated owner.

    Endpoint: GET /v2/chats/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v2/chats/{chat_id}", params=_params, json_body=_body)

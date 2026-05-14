"""Auto-generated tools for channel_accounts. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_channel_accounts_get(channel_account_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get channel account

    Retrieve a single WhatsApp Official channel account by ID

    Endpoint: GET /v2/channel-accounts/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v2/channel-accounts/{channel_account_id}", params=_params, json_body=_body)


async def clint_channel_accounts_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List channel accounts

    Retrieve a paginated list of WhatsApp Official channel accounts. Only returns channels with type WHATSAPP_OFFICIAL that are not deleted.

    Endpoint: GET /v2/channel-accounts
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v2/channel-accounts", params=_params, json_body=_body)

"""Auto-generated tools for message_templates. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_message_templates_get(template_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get message template

    Retrieve a single message template by ID. Validates that the template belongs to a WhatsApp Official channel account owned by the authenticated user.

    Endpoint: GET /v2/message-templates/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v2/message-templates/{template_id}", params=_params, json_body=_body)


async def clint_message_templates_list(channel_account_id: Annotated[str | None, Field(description="""UUID of the channel account (required). Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '550e8400-e29b-41d4-a716-446655440000'""")] = None, limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List message templates

    Retrieve a paginated list of message templates linked to a WhatsApp Official channel account. The channel_account_id query parameter is required and must belong to the authenticated owner.

    Endpoint: GET /v2/message-templates
    """
    _params = {
        "channel_account_id": channel_account_id,
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v2/message-templates", params=_params, json_body=_body)

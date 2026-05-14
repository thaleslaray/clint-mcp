"""Auto-generated tools for origins. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_origins_get(origin_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get origin

    Retrieve a single origin by ID

    Endpoint: GET /v1/origins/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/origins/{origin_id}", params=_params, json_body=_body)


async def clint_origins_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, group_id: Annotated[str | None, Field(description="""Filter by group ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None) -> Any:
    """List origins

    Retrieve a paginated list of origins

    Endpoint: GET /v1/origins
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
        "group_id": group_id,
    }
    _body = None
    return await request("GET", f"/v1/origins", params=_params, json_body=_body)

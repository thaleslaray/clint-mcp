"""Auto-generated tools for groups. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp.client import request


async def clint_groups_get(group_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get group

    Retrieve a single group by ID

    Endpoint: GET /v1/groups/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/groups/{group_id}", params=_params, json_body=_body)


async def clint_groups_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List groups

    Retrieve a paginated list of groups

    Endpoint: GET /v1/groups
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v1/groups", params=_params, json_body=_body)

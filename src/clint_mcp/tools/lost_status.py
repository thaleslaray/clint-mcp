"""Auto-generated tools for lost_status. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp.client import request


async def clint_lost_status_get(lost_status_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get lost status

    Retrieve a single lost status by ID

    Endpoint: GET /v1/lost-status/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/lost-status/{lost_status_id}", params=_params, json_body=_body)


async def clint_lost_status_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List lost status

    Retrieve a paginated list of lost status

    Endpoint: GET /v1/lost-status
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v1/lost-status", params=_params, json_body=_body)

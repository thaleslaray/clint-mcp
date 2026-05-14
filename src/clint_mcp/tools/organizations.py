"""Auto-generated tools for organizations. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_organizations_get(organization_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get organization

    Retrieve a single organization by ID

    Endpoint: GET /v1/organizations/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/organizations/{organization_id}", params=_params, json_body=_body)


async def clint_organizations_update(organization_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], name: Annotated[str | None, Field(description="""Example: 'Organization name'""")] = None, fields: Annotated[dict | None, Field(description="""Type: object""")] = None) -> Any:
    """Update organization

    Update a single organization

    Endpoint: POST /v1/organizations/{id}
    """
    _params = None
    _body = {
        "name": name,
        "fields": fields,
    }
    return await request("POST", f"/v1/organizations/{organization_id}", params=_params, json_body=_body)

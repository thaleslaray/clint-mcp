"""Auto-generated tools for tags. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_tags_create(name: Annotated[str, Field(description="""Example: 'Tag name'""")], color: Annotated[str, Field(description="""Allowed values (case-sensitive, pass EXACTLY as listed):
  - '#f44336'
  - '#e91e63'
  - '#9c27b0'
  - '#673ab7'
  - '#3f51b5'
  - '#2196f3'
  - '#03a9f4'
  - '#00bcd4'
  - '#009688'
  - '#4caf50'
  - '#8bc34a'
  - '#faa200'
  - '#ff9800'
  - '#ff5722'
  - '#795548'
  - '#607d8b'""")]) -> Any:
    """Create tag

    Create a new tag

    Endpoint: POST /v1/tags
    """
    _params = None
    _body = {
        "name": name,
        "color": color,
    }
    return await request("POST", f"/v1/tags", params=_params, json_body=_body)


async def clint_tags_delete(tag_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Remove tag

    Remove a single tag by ID

    Endpoint: DELETE /v1/tags/{id}
    """
    _params = None
    _body = None
    return await request("DELETE", f"/v1/tags/{tag_id}", params=_params, json_body=_body)


async def clint_tags_get(tag_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get tag

    Retrieve a single tag by ID

    Endpoint: GET /v1/tags/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/tags/{tag_id}", params=_params, json_body=_body)


async def clint_tags_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, name: Annotated[str | None, Field(description="""Filter by tag name. Example: 'Tag name'""")] = None) -> Any:
    """List tags

    Retrieve a paginated list of tags

    Endpoint: GET /v1/tags
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
        "name": name,
    }
    _body = None
    return await request("GET", f"/v1/tags", params=_params, json_body=_body)

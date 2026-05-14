"""Auto-generated tools for deals. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_deals_create(origin_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], name: Annotated[str | None, Field(description="""Example: 'Contact name'""")] = None, phone: Annotated[str | None, Field(description="""Example: '48999999999'""")] = None, email: Annotated[str | None, Field(description="""Example: 'contact@email.com'""")] = None, username: Annotated[str | None, Field(description="""Example: 'Instagram ID'""")] = None, value: Annotated[float | None, Field(description="""Example: '200.5'""")] = None, stage_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, user_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, contact_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, fields: Annotated[dict | None, Field(description="""Type: object""")] = None) -> Any:
    """Create deal

    Create a new Deal

    Endpoint: POST /v1/deals
    """
    _params = None
    _body = {
        "origin_id": origin_id,
        "name": name,
        "phone": phone,
        "email": email,
        "username": username,
        "value": value,
        "stage_id": stage_id,
        "user_id": user_id,
        "contact_id": contact_id,
        "fields": fields,
    }
    return await request("POST", f"/v1/deals", params=_params, json_body=_body)


async def clint_deals_delete(deal_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Remove deal

    Remove a single deal by ID

    Endpoint: DELETE /v1/deals/{id}
    """
    _params = None
    _body = None
    return await request("DELETE", f"/v1/deals/{deal_id}", params=_params, json_body=_body)


async def clint_deals_get(deal_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get deal

    Retrieve a single deal by ID

    Endpoint: GET /v1/deals/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/deals/{deal_id}", params=_params, json_body=_body)


async def clint_deals_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, origin_id: Annotated[str | None, Field(description="""Filter by origin ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, created_at_start: Annotated[str | None, Field(description="""Filter by created_at using GTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, created_at_end: Annotated[str | None, Field(description="""Filter by created_at using LTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, updated_at_start: Annotated[str | None, Field(description="""Filter by updated_at using GTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, updated_at_end: Annotated[str | None, Field(description="""Filter by updated_at using LTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, user_id: Annotated[str | None, Field(description="""Filter by user ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, user_email: Annotated[str | None, Field(description="""Filter by user e-mail. Example: 'user@email.com'""")] = None, contact_id: Annotated[str | None, Field(description="""Filter by contact ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, phone: Annotated[str | None, Field(description="""Filter by contact phone. Example: '999999999'""")] = None, email: Annotated[str | None, Field(description="""Filter by contact e-mail. Example: 'contact@email.com'""")] = None, tag_ids: Annotated[str | None, Field(description="""Filter by tag IDs using OR operator. Separated by ','. Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8,99999999-d77b-4e8b-9d35-fd43e972b999'""")] = None, tag_names: Annotated[str | None, Field(description="""Filter by tag names using OR operator. Separated by ','. Example: 'tag1,tag2,tag3'""")] = None, status: Annotated[str | None, Field(description="""Filter by status. Allowed values: 'OPEN', 'WON', 'LOST'""")] = None, stage_id: Annotated[str | None, Field(description="""Filter by stage ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, updated_stage_at_start: Annotated[str | None, Field(description="""Filter by updated_stage_at using GTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, updated_stage_at_end: Annotated[str | None, Field(description="""Filter by updated_stage_at using LTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, fields: Annotated[dict | None, Field(description="""Filter by deal fields. Can be used multiple times for each field. Type: object""")] = None, won_at_start: Annotated[str | None, Field(description="""Filter by won_at using GTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, won_at_end: Annotated[str | None, Field(description="""Filter by won_at using LTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, lost_at_start: Annotated[str | None, Field(description="""Filter by lost_at using GTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None, lost_at_end: Annotated[str | None, Field(description="""Filter by lost_at_at using LTE operator. Example: '2020-01-01T14:15:00.000000+00:00'""")] = None) -> Any:
    """List deals

    Retrieve a paginated list of deals

    Endpoint: GET /v1/deals
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
        "origin_id": origin_id,
        "created_at_start": created_at_start,
        "created_at_end": created_at_end,
        "updated_at_start": updated_at_start,
        "updated_at_end": updated_at_end,
        "user_id": user_id,
        "user_email": user_email,
        "contact_id": contact_id,
        "phone": phone,
        "email": email,
        "tag_ids": tag_ids,
        "tag_names": tag_names,
        "status": status,
        "stage_id": stage_id,
        "updated_stage_at_start": updated_stage_at_start,
        "updated_stage_at_end": updated_stage_at_end,
        "fields": fields,
        "won_at_start": won_at_start,
        "won_at_end": won_at_end,
        "lost_at_start": lost_at_start,
        "lost_at_end": lost_at_end,
    }
    _body = None
    return await request("GET", f"/v1/deals", params=_params, json_body=_body)


async def clint_deals_update(deal_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], name: Annotated[str | None, Field(description="""Example: 'Contact name'""")] = None, phone: Annotated[str | None, Field(description="""Example: '48999999999'""")] = None, email: Annotated[str | None, Field(description="""Example: 'contact@email.com'""")] = None, value: Annotated[float | None, Field(description="""Example: '200.5'""")] = None, stage_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, status: Annotated[str | None, Field(description="""Allowed values: 'OPEN', 'WON', 'LOST'""")] = None, user_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, origin_id: Annotated[str | None, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, fields: Annotated[dict | None, Field(description="""Type: object""")] = None) -> Any:
    """Update deal

    Update a single deal

    Endpoint: POST /v1/deals/{id}
    """
    _params = None
    _body = {
        "name": name,
        "phone": phone,
        "email": email,
        "value": value,
        "stage_id": stage_id,
        "status": status,
        "user_id": user_id,
        "origin_id": origin_id,
        "fields": fields,
    }
    return await request("POST", f"/v1/deals/{deal_id}", params=_params, json_body=_body)

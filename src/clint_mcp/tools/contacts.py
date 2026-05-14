"""Auto-generated tools for contacts. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp._shared import request


async def clint_contacts_attachments_list(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List contact attachments

    Retrieve a paginated list of attachments (documents) for a specific contact. Each attachment includes a public document URL that can be used directly for download or rendering.

    Endpoint: GET /v1/contacts/{id}/attachments
    """
    _params = {
        "limit": limit,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v1/contacts/{contact_id}/attachments", params=_params, json_body=_body)


async def clint_contacts_create(name: Annotated[str | None, Field(description="""Example: 'Contact name'""")] = None, ddi: Annotated[str | None, Field(description="""Example: '+55'""")] = None, phone: Annotated[str | None, Field(description="""Example: '48999999999'""")] = None, email: Annotated[str | None, Field(description="""Example: 'contact@email.com'""")] = None, username: Annotated[str | None, Field(description="""Example: 'Instagram ID'""")] = None, fields: Annotated[dict | None, Field(description="""Type: object""")] = None) -> Any:
    """Create contact

    Create a new Contact

    Endpoint: POST /v1/contacts
    """
    _params = None
    _body = {
        "name": name,
        "ddi": ddi,
        "phone": phone,
        "email": email,
        "username": username,
        "fields": fields,
    }
    return await request("POST", f"/v1/contacts", params=_params, json_body=_body)


async def clint_contacts_delete(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Remove contact

    Remove a single contact by ID

    Endpoint: DELETE /v1/contacts/{id}
    """
    _params = None
    _body = None
    return await request("DELETE", f"/v1/contacts/{contact_id}", params=_params, json_body=_body)


async def clint_contacts_get(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Get contact

    Retrieve a single contact by ID

    Endpoint: GET /v1/contacts/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/contacts/{contact_id}", params=_params, json_body=_body)


async def clint_contacts_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, origin_id: Annotated[str | None, Field(description="""Filter by origin ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, name: Annotated[str | None, Field(description="""Filter by contact name. Example: 'Contact name'""")] = None, ddi: Annotated[str | None, Field(description="""Filter by contact ddi. Example: '55'""")] = None, phone: Annotated[str | None, Field(description="""Filter by contact phone. Example: '999999999'""")] = None, email: Annotated[str | None, Field(description="""Filter by contact e-mail. Example: 'contact@email.com'""")] = None, tag_ids: Annotated[str | None, Field(description="""Filter by contact tag IDs using OR operator. Separated by ','. Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8,99999999-d77b-4e8b-9d35-fd43e972b999'""")] = None, tag_names: Annotated[str | None, Field(description="""Filter by contact tag names using OR operator. Separated by ','. Example: 'tag1,tag2,tag3'""")] = None, fields: Annotated[dict | None, Field(description="""Filter by contact fields. Can be used multiple times for each field. Type: object""")] = None) -> Any:
    """List contacts

    Retrieve a paginated list of contacts

    Endpoint: GET /v1/contacts
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
        "origin_id": origin_id,
        "name": name,
        "ddi": ddi,
        "phone": phone,
        "email": email,
        "tag_ids": tag_ids,
        "tag_names": tag_names,
        "fields": fields,
    }
    _body = None
    return await request("GET", f"/v1/contacts", params=_params, json_body=_body)


async def clint_contacts_tags_add(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Add tags

    Add tags to a single contact

    Endpoint: POST /v1/contacts/{id}/tags
    """
    _params = None
    _body = None
    return await request("POST", f"/v1/contacts/{contact_id}/tags", params=_params, json_body=_body)


async def clint_contacts_tags_remove(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], tag_id: Annotated[str | None, Field(description="""The ID of the tag to be removed. Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, tag_name: Annotated[str | None, Field(description="""The name of the tag to be removed. Example: 'my-tag'""")] = None) -> Any:
    """Remove tag

    Remove a tag from a contact

    Endpoint: DELETE /v1/contacts/{id}/tags
    """
    _params = None
    _body = {
        "tag_id": tag_id,
        "tag_name": tag_name,
    }
    return await request("DELETE", f"/v1/contacts/{contact_id}/tags", params=_params, json_body=_body)


async def clint_contacts_update(contact_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], name: Annotated[str | None, Field(description="""Example: 'Contact name'""")] = None, ddi: Annotated[str | None, Field(description="""Example: '+55'""")] = None, phone: Annotated[str | None, Field(description="""Example: '48999999999'""")] = None, email: Annotated[str | None, Field(description="""Example: 'contact@email.com'""")] = None, username: Annotated[str | None, Field(description="""Example: 'Instagram ID'""")] = None, fields: Annotated[dict | None, Field(description="""Type: object""")] = None) -> Any:
    """Update contact

    Update a single contact

    Endpoint: POST /v1/contacts/{id}
    """
    _params = None
    _body = {
        "name": name,
        "ddi": ddi,
        "phone": phone,
        "email": email,
        "username": username,
        "fields": fields,
    }
    return await request("POST", f"/v1/contacts/{contact_id}", params=_params, json_body=_body)

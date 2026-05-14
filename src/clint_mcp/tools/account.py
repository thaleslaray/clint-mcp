"""Auto-generated tools for account. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp.client import request


async def clint_account_fields_list() -> Any:
    """List fields

    Retrieve a list of fields

    Endpoint: GET /v1/account/fields
    """
    _params = None
    _body = None
    return await request("GET", f"/v1/account/fields", params=_params, json_body=_body)

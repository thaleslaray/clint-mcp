"""Auto-generated tools for dashboards. DO NOT EDIT — run generator."""
from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field

from clint_mcp.client import request


async def clint_charts_data_get(chart_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], date_start: Annotated[str | None, Field(description="""Start date filter (inclusive). Example: '2026-01-01'""")] = None, date_end: Annotated[str | None, Field(description="""End date filter (inclusive). Example: '2026-12-31'""")] = None, user_id: Annotated[str | None, Field(description="""Filter by user ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, origin_id: Annotated[str | None, Field(description="""Filter by origin ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, origin_group_id: Annotated[str | None, Field(description="""Filter by origin group ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, tag_id: Annotated[str | None, Field(description="""Filter by tag ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, timezone: Annotated[str | None, Field(description="""Timezone for date calculations. Example: 'America/Sao_Paulo'""")] = None, limit: Annotated[int | None, Field(description="""Limit rows returned (applies to table/list chart types). Type: integer""")] = None) -> Any:
    """Get single chart data

    Execute a single chart query and return its data.

    Endpoint: GET /v2/charts/{id}/data
    """
    _params = {
        "date_start": date_start,
        "date_end": date_end,
        "user_id": user_id,
        "origin_id": origin_id,
        "origin_group_id": origin_group_id,
        "tag_id": tag_id,
        "timezone": timezone,
        "limit": limit,
    }
    _body = None
    return await request("GET", f"/v2/charts/{chart_id}/data", params=_params, json_body=_body)


async def clint_dashboards_data_get(dashboard_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")], page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None, date_start: Annotated[str | None, Field(description="""Start date filter (inclusive). Example: '2026-01-01'""")] = None, date_end: Annotated[str | None, Field(description="""End date filter (inclusive). Example: '2026-12-31'""")] = None, user_id: Annotated[str | None, Field(description="""Filter by user ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, origin_id: Annotated[str | None, Field(description="""Filter by origin ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, origin_group_id: Annotated[str | None, Field(description="""Filter by origin group ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, tag_id: Annotated[str | None, Field(description="""Filter by tag ID. Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")] = None, timezone: Annotated[str | None, Field(description="""Timezone for date calculations. Example: 'America/Sao_Paulo'""")] = None, limit: Annotated[int | None, Field(description="""Limit rows returned per chart (applies to table/list chart types). Type: integer""")] = None, chart_ids: Annotated[str | None, Field(description="""Comma-separated list of chart IDs to fetch (returns only these charts instead of all). Example: 'uuid-1,uuid-2'""")] = None) -> Any:
    """Get dashboard chart data

    Execute dashboard chart queries and return data. Charts are paginated at 10 per page. Individual chart failures are handled gracefully and return an error message instead of failing the entire request.

    Endpoint: GET /v2/dashboards/{id}/data
    """
    _params = {
        "page": page,
        "date_start": date_start,
        "date_end": date_end,
        "user_id": user_id,
        "origin_id": origin_id,
        "origin_group_id": origin_group_id,
        "tag_id": tag_id,
        "timezone": timezone,
        "limit": limit,
        "chart_ids": chart_ids,
    }
    _body = None
    return await request("GET", f"/v2/dashboards/{dashboard_id}/data", params=_params, json_body=_body)


async def clint_dashboards_get(dashboard_id: Annotated[str, Field(description="""Format: UUID (e.g. '550e8400-e29b-41d4-a716-446655440000'). Example: '8feade82-d77b-4e8b-9d35-fd43e972b5c8'""")]) -> Any:
    """Retrieve a dashboard

    Retrieve a single dashboard with its list of charts.

    Endpoint: GET /v2/dashboards/{id}
    """
    _params = None
    _body = None
    return await request("GET", f"/v2/dashboards/{dashboard_id}", params=_params, json_body=_body)


async def clint_dashboards_list(limit: Annotated[int | None, Field(description="""Max number of rows returned. Type: integer""")] = None, offset: Annotated[int | None, Field(description="""Number of rows skipped of the result. Type: integer""")] = None, page: Annotated[int | None, Field(description="""Select the page of the result. Type: integer""")] = None) -> Any:
    """List dashboards

    Retrieve a paginated list of dashboards.

    Endpoint: GET /v2/dashboards
    """
    _params = {
        "limit": limit,
        "offset": offset,
        "page": page,
    }
    _body = None
    return await request("GET", f"/v2/dashboards", params=_params, json_body=_body)

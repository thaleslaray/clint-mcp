"""Shared lazy singleton for the Clint API client.

Auto-generated tool modules import `request` from here, never instantiate
`ClintClient` directly. This isolates the singleton lifecycle and makes
it trivial to mock for tests.
"""
from __future__ import annotations

from typing import Any

from clint_mcp.client import ClintClient

_client: ClintClient | None = None


def get_client() -> ClintClient:
    global _client
    if _client is None:
        _client = ClintClient()
    return _client


async def request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> Any:
    """Module-level convenience wrapper around the singleton client."""
    return await get_client().request(method, path, params=params, json_body=json_body)


async def aclose() -> None:
    """Close the singleton client (e.g. at process exit). Safe if never opened."""
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None

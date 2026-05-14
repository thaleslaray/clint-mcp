"""Async HTTP client for Clint CRM API."""
from __future__ import annotations

import asyncio
import os
import time
from typing import Any

import httpx

BASE_URL = "https://api.clint.digital"
DEFAULT_TIMEOUT = 30.0


class ClintError(RuntimeError):
    """Raised when the Clint API returns a non-2xx response."""

    def __init__(self, status: int, body: Any, method: str, path: str) -> None:
        super().__init__(f"Clint API {method} {path} -> {status}: {body!r}")
        self.status = status
        self.body = body
        self.method = method
        self.path = path


class _RateLimiter:
    """Simple per-second sliding window — keeps under N requests/sec."""

    def __init__(self, rps: float) -> None:
        self.rps = rps
        self._interval = 1.0 / rps if rps > 0 else 0.0
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def acquire(self) -> None:
        if self._interval == 0:
            return
        async with self._lock:
            now = time.monotonic()
            wait = self._interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()


_client: httpx.AsyncClient | None = None
_limiter: _RateLimiter | None = None


def _get_token() -> str:
    token = os.environ.get("CLINT_API_TOKEN")
    if not token:
        raise RuntimeError("CLINT_API_TOKEN env var not set")
    return token


def _get_limiter() -> _RateLimiter:
    global _limiter
    if _limiter is None:
        rps = float(os.environ.get("CLINT_MAX_RPS", "5"))
        _limiter = _RateLimiter(rps)
    return _limiter


async def _get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=DEFAULT_TIMEOUT,
            headers={"accept": "application/json"},
        )
    return _client


async def request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> Any:
    """Perform an authenticated request against the Clint API.

    `params` and `json_body` may contain None values — they're stripped here.
    """
    limiter = _get_limiter()
    await limiter.acquire()
    client = await _get_client()

    clean_params = {k: v for k, v in (params or {}).items() if v is not None}
    clean_body = (
        {k: v for k, v in (json_body or {}).items() if v is not None}
        if json_body is not None
        else None
    )

    resp = await client.request(
        method,
        path,
        params=clean_params or None,
        json=clean_body,
        headers={"api-token": _get_token()},
    )

    if resp.status_code >= 400:
        try:
            body = resp.json()
        except Exception:
            body = resp.text
        raise ClintError(resp.status_code, body, method, path)

    if resp.status_code == 204 or not resp.content:
        return None
    ctype = resp.headers.get("content-type", "")
    if "json" in ctype:
        return resp.json()
    return resp.text


async def aclose() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None

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


class ClintClient:
    """Async client for the Clint CRM API.

    Reads CLINT_API_TOKEN and (optionally) CLINT_MAX_RPS at first use.
    Use the module-level `get_client()` from `_shared.py` to access the
    lazy singleton — tools never instantiate this directly.
    """

    def __init__(self) -> None:
        token = os.environ.get("CLINT_API_TOKEN")
        if not token:
            raise RuntimeError("CLINT_API_TOKEN env var not set")
        rps = float(os.environ.get("CLINT_MAX_RPS", "5"))

        self._token = token
        self._limiter = _RateLimiter(rps)
        self._http = httpx.AsyncClient(
            base_url=BASE_URL,
            timeout=DEFAULT_TIMEOUT,
            headers={"accept": "application/json"},
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> Any:
        """Perform an authenticated request against the Clint API.

        `params` and `json_body` may contain None values — they're stripped here.
        """
        await self._limiter.acquire()
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        clean_body = (
            {k: v for k, v in (json_body or {}).items() if v is not None}
            if json_body is not None
            else None
        )

        resp = await self._http.request(
            method,
            path,
            params=clean_params or None,
            json=clean_body,
            headers={"api-token": self._token},
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

    async def aclose(self) -> None:
        await self._http.aclose()

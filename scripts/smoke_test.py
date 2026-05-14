"""Live smoke test against the real Clint API. Read-only calls only."""
from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Awaitable

from clint_mcp._shared import aclose
from clint_mcp.tools.contacts import clint_contacts_list
from clint_mcp.tools.users import clint_users_list
from clint_mcp.tools.tags import clint_tags_list
from clint_mcp.tools.origins import clint_origins_list
from clint_mcp.tools.account import clint_account_fields_list


async def time_call(label: str, coro_fn: Callable[[], Awaitable[Any]]) -> None:
    t0 = time.monotonic()
    try:
        result = await coro_fn()
        dt = (time.monotonic() - t0) * 1000
        # Shape: keys at top level + first item shape if it's a paginated response.
        if isinstance(result, dict):
            top_keys = list(result.keys())
            data = result.get("data") or result.get("results") or []
            data_shape = list(data[0].keys()) if data else "(empty)"
            print(f"  ✓ {label}  {dt:6.0f}ms  keys={top_keys}  data[0]={data_shape}")
        else:
            print(f"  ✓ {label}  {dt:6.0f}ms  type={type(result).__name__}")
    except Exception as e:
        dt = (time.monotonic() - t0) * 1000
        print(f"  ✗ {label}  {dt:6.0f}ms  {type(e).__name__}: {e}")


async def main() -> None:
    print("Smoke test — Clint API")
    print("-" * 60)
    await time_call("contacts_list(limit=2)", lambda: clint_contacts_list(limit=2))
    await time_call("users_list(limit=2)", lambda: clint_users_list(limit=2))
    await time_call("tags_list(limit=2)", lambda: clint_tags_list(limit=2))
    await time_call("origins_list(limit=2)", lambda: clint_origins_list(limit=2))
    await time_call("account_fields_list()", lambda: clint_account_fields_list())
    await aclose()


if __name__ == "__main__":
    asyncio.run(main())

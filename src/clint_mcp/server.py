"""Clint MCP Server — FastMCP entry point.

Architecture (per hotmart-mcp pattern):
- Tools (46 auto-generated from OpenAPI spec) are auto-discovered from `clint_mcp.tools`.
- Apps (Prefab UI dashboards) are auto-discovered from `clint_mcp.apps`. Convention:
  any async function whose name ends with `_app` is registered with `app=True`.
- Code Mode is **opt-in** via env var `CLINT_MCP_CODE_MODE=1`. Default is off because
  CodeMode collapses ALL tools (including apps) into 3 meta-tools, which breaks
  Prefab UI rendering in Claude Desktop. Apps only render when exposed as individual
  tools to the client.

Use cases:
- **Claude Desktop / .mcpb**: do NOT set the env var → 46 tools + N apps exposed
  directly, apps render visually as Prefab UI.
- **Claude Code (CLI)**: set `CLINT_MCP_CODE_MODE=1` in `~/.claude.json` env →
  collapses everything to 3 meta-tools (`search`/`get_schema`/`execute`),
  saving context window at the cost of UI rendering.
"""
from __future__ import annotations

import importlib
import inspect
import os
import pkgutil
from asyncio import iscoroutinefunction

from fastmcp import FastMCP

from clint_mcp import apps as apps_pkg
from clint_mcp import tools as tools_pkg

INSTRUCTIONS = """
MCP server for the Clint CRM API (Brazilian, https://api.clint.digital).

Coverage: 46 endpoints across 14 categories — Contacts, Deals, Tags, Organizations,
Groups, Lost Status, Origins, Users, Account, Channel Accounts, Message Templates,
Chats, Messages (WhatsApp Official), Dashboards.

Apps with names ending in `_app` (e.g. `clint_dashboard_view_app`) return interactive
Prefab UI (charts, DataTables) and only render in clients that support the
io.modelcontextprotocol/ui extension (e.g. Claude Desktop, `fastmcp dev`).

Auth: header `api-token` from env var CLINT_API_TOKEN.
Rate: client-side throttle, default 5 req/s (override with CLINT_MAX_RPS).
Code Mode: opt-in via CLINT_MCP_CODE_MODE=1 (collapses to 3 meta-tools — sacrifices apps).
""".strip()


mcp = FastMCP("clint", instructions=INSTRUCTIONS)


# Module-import-time registration (matches hotmart-mcp v0.6+).
# Tools and apps must be registered on the FastMCP instance before any
# `mcp.list_tools()` / `mcp.call_tool()` works. Doing it here (rather than
# only in main()) means smoke tests and external Python imports just work.


def _discover_and_register_tools() -> int:
    """Auto-discover async functions under clint_mcp.tools and register them as tools.

    Only registers functions DEFINED in the inspected module — not imports
    pulled in via `from clint_mcp._shared import request` etc.
    """
    registered = 0
    for module_info in pkgutil.iter_modules(tools_pkg.__path__, prefix=f"{tools_pkg.__name__}."):
        if module_info.name.endswith("__init__"):
            continue
        module = importlib.import_module(module_info.name)
        for name, obj in inspect.getmembers(module, iscoroutinefunction):
            if name.startswith("_"):
                continue
            if obj.__module__ != module.__name__:
                continue  # imported, not defined here
            mcp.tool()(obj)
            registered += 1
    return registered


def _discover_and_register_apps() -> int:
    """Auto-discover async functions under clint_mcp.apps ending in `_app`.

    Each one is registered with `app=True` so it carries `meta["ui"]` and the
    client renders it as Prefab UI instead of returning JSON.
    """
    registered = 0
    for module_info in pkgutil.iter_modules(apps_pkg.__path__, prefix=f"{apps_pkg.__name__}."):
        if module_info.name.endswith("__init__"):
            continue
        module = importlib.import_module(module_info.name)
        for name, obj in inspect.getmembers(module, iscoroutinefunction):
            if name.startswith("_") or not name.endswith("_app"):
                continue
            if obj.__module__ != module.__name__:
                continue  # imported, not defined here
            mcp.tool(app=True)(obj)
            registered += 1
    return registered


def _apply_code_mode() -> None:
    """Apply Code Mode transform — OPT-IN via CLINT_MCP_CODE_MODE env var.

    Disabled by default because CodeMode collapses ALL tools (including apps
    registered with `app=True`) into just `search`+`get_schema`+`execute`,
    which destroys the `meta["ui"]` needed for Prefab UI rendering in
    Claude Desktop. Apps only render as native UI when exposed as
    individual tools to the client.

    Set `CLINT_MCP_CODE_MODE=1` if you want the collapse — useful for
    clients that don't render Prefab UI (e.g. Claude Code CLI) and want
    context-window savings (3 entries vs. 46+ tools+apps).
    """
    if os.environ.get("CLINT_MCP_CODE_MODE", "").lower() not in ("1", "true", "yes"):
        return
    try:
        from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider

        sandbox = MontySandboxProvider(
            limits={"max_duration_secs": 30, "max_memory": 100_000_000},
        )
        mcp.add_transform(CodeMode(sandbox_provider=sandbox))
    except ImportError:
        pass  # Code Mode not available in this fastmcp version


# Register at module import time so external Python (smoke tests, asyncio
# inspection, fastmcp dev) sees the full tool list immediately.
_TOOLS_COUNT = _discover_and_register_tools()
_APPS_COUNT = _discover_and_register_apps()
_apply_code_mode()


def main() -> None:
    """CLI entry point — bound to the `clint-mcp` script."""
    code_mode_active = os.environ.get("CLINT_MCP_CODE_MODE", "").lower() in ("1", "true", "yes")
    mode_label = (
        "Code Mode (3 meta-tools)" if code_mode_active
        else f"{_TOOLS_COUNT} tool(s) + {_APPS_COUNT} app(s)"
    )
    print(f"clint-mcp: {mode_label}, starting server...")
    mcp.run()


if __name__ == "__main__":
    main()

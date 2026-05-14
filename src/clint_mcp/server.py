"""FastMCP server for the Clint CRM API.

All 46 tools auto-generated from the OpenAPI spec at docs/openapi.json
are collapsed into 3 meta-tools (search/get_schema/execute) via CodeMode.
"""
from __future__ import annotations

from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider

from clint_mcp.tools import ALL_TOOLS

INSTRUCTIONS = """
MCP server for the Clint CRM API (Brazilian, https://api.clint.digital).

Coverage: 46 endpoints across 14 categories — Contacts, Deals, Tags, Organizations,
Groups, Lost Status, Origins, Users, Account, Channel Accounts, Message Templates,
Chats, Messages (WhatsApp Official), Dashboards.

Auth: header `api-token` from env var CLINT_API_TOKEN.
Rate: client-side throttle, default 5 req/s (override with CLINT_MAX_RPS).

Code Mode is enabled — interact via the 3 meta-tools:
  search(query)         find relevant tools
  get_schema(tool_name) inspect parameters and enums
  execute(code)         run async Python that calls tools
""".strip()


mcp = FastMCP("clint", instructions=INSTRUCTIONS)

for fn in ALL_TOOLS:
    mcp.tool(fn)

sandbox = MontySandboxProvider(
    limits={"max_duration_secs": 30, "max_memory": 100_000_000},
)
mcp.add_transform(CodeMode(sandbox_provider=sandbox))


def main() -> None:
    """CLI entry point — bound to the `clint-mcp` script."""
    mcp.run()


if __name__ == "__main__":
    main()

"""Prefab Apps — interactive UIs rendered inside the MCP client.

Apps are auto-discovered by `server.py`: any async function in this package
whose name ends with `_app` is registered with `mcp.tool(app=True)`.
Don't maintain a manual ALL_APPS list — just create files here.
"""

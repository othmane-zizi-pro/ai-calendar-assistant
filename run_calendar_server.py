#!/usr/bin/env python3
"""
Launcher script for the Google Calendar MCP Server.
This script ensures the MCP server runs correctly with proper module imports.
"""

if __name__ == "__main__":
    from calendar_assistant.mcp_server import calendar_server
    import asyncio

    asyncio.run(calendar_server.main())

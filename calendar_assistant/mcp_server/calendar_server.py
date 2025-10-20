"""MCP Server for Google Calendar.

This server exposes Google Calendar functionality through the Model Context Protocol.
"""

import json
from datetime import datetime, timedelta
from typing import Any, Sequence
from pathlib import Path

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

from ..utils.google_calendar import GoogleCalendarClient


# Initialize server
app = Server("google-calendar-assistant")

# Initialize Google Calendar client
calendar_client = None


def get_calendar_client():
    """Lazy initialization of calendar client."""
    global calendar_client
    if calendar_client is None:
        calendar_client = GoogleCalendarClient()
    return calendar_client


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available Google Calendar tools."""
    return [
        Tool(
            name="list_events",
            description="List upcoming calendar events",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of events to return (default: 10)",
                        "default": 10
                    },
                    "days_ahead": {
                        "type": "integer",
                        "description": "Number of days ahead to look (default: 7)",
                        "default": 7
                    }
                }
            }
        ),
        Tool(
            name="get_today_events",
            description="Get all events scheduled for today",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="create_event",
            description="Create a new calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Event title/summary"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO format (e.g., 2024-01-15T10:00:00)"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO format (e.g., 2024-01-15T11:00:00)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Event description (optional)",
                        "default": ""
                    },
                    "location": {
                        "type": "string",
                        "description": "Event location (optional)",
                        "default": ""
                    },
                    "attendees": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of attendee emails (optional)"
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        ),
        Tool(
            name="search_events",
            description="Search for events by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results (default: 10)",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="delete_event",
            description="Delete a calendar event by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "ID of the event to delete"
                    }
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="update_event",
            description="Update an existing calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "ID of the event to update"
                    },
                    "summary": {
                        "type": "string",
                        "description": "New event title (optional)"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "New start time in ISO format (optional)"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "New end time in ISO format (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)"
                    }
                },
                "required": ["event_id"]
            }
        ),
        Tool(
            name="check_availability",
            description="Check if a time slot is free or busy",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO format"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO format"
                    }
                },
                "required": ["start_time", "end_time"]
            }
        )
    ]


def format_event(event: dict) -> str:
    """Format an event for display."""
    summary = event.get('summary', 'No title')
    start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
    end = event.get('end', {}).get('dateTime', event.get('end', {}).get('date', ''))
    location = event.get('location', '')
    description = event.get('description', '')

    output = f"**{summary}**\n"
    output += f"Start: {start}\n"
    output += f"End: {end}\n"

    if location:
        output += f"Location: {location}\n"
    if description:
        output += f"Description: {description}\n"

    output += f"Event ID: {event.get('id', '')}\n"

    return output


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    client = get_calendar_client()

    if name == "list_events":
        max_results = arguments.get("max_results", 10)
        days_ahead = arguments.get("days_ahead", 7)

        time_min = datetime.utcnow()
        time_max = time_min + timedelta(days=days_ahead)

        events = client.list_events(
            max_results=max_results,
            time_min=time_min,
            time_max=time_max
        )

        if not events:
            return [TextContent(type="text", text="No upcoming events found.")]

        output = f"Found {len(events)} upcoming event(s):\n\n"
        for i, event in enumerate(events, 1):
            output += f"--- Event {i} ---\n"
            output += format_event(event)
            output += "\n"

        return [TextContent(type="text", text=output)]

    elif name == "get_today_events":
        events = client.get_today_events()

        if not events:
            return [TextContent(type="text", text="No events scheduled for today.")]

        output = f"Today's events ({len(events)} total):\n\n"
        for i, event in enumerate(events, 1):
            output += f"--- Event {i} ---\n"
            output += format_event(event)
            output += "\n"

        return [TextContent(type="text", text=output)]

    elif name == "create_event":
        summary = arguments["summary"]
        start_time = datetime.fromisoformat(arguments["start_time"])
        end_time = datetime.fromisoformat(arguments["end_time"])
        description = arguments.get("description", "")
        location = arguments.get("location", "")
        attendees = arguments.get("attendees", [])

        event = client.create_event(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
            attendees=attendees
        )

        if event:
            output = "✅ Event created successfully!\n\n"
            output += format_event(event)
            return [TextContent(type="text", text=output)]
        else:
            return [TextContent(type="text", text="❌ Failed to create event.")]

    elif name == "search_events":
        query = arguments["query"]
        max_results = arguments.get("max_results", 10)

        events = client.search_events(query=query, max_results=max_results)

        if not events:
            return [TextContent(type="text", text=f"No events found matching '{query}'.")]

        output = f"Found {len(events)} event(s) matching '{query}':\n\n"
        for i, event in enumerate(events, 1):
            output += f"--- Event {i} ---\n"
            output += format_event(event)
            output += "\n"

        return [TextContent(type="text", text=output)]

    elif name == "delete_event":
        event_id = arguments["event_id"]
        success = client.delete_event(event_id=event_id)

        if success:
            return [TextContent(type="text", text=f"✅ Event {event_id} deleted successfully.")]
        else:
            return [TextContent(type="text", text=f"❌ Failed to delete event {event_id}.")]

    elif name == "update_event":
        event_id = arguments["event_id"]
        summary = arguments.get("summary")
        description = arguments.get("description")
        start_time = None
        end_time = None

        if "start_time" in arguments:
            start_time = datetime.fromisoformat(arguments["start_time"])
        if "end_time" in arguments:
            end_time = datetime.fromisoformat(arguments["end_time"])

        event = client.update_event(
            event_id=event_id,
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description
        )

        if event:
            output = "✅ Event updated successfully!\n\n"
            output += format_event(event)
            return [TextContent(type="text", text=output)]
        else:
            return [TextContent(type="text", text="❌ Failed to update event.")]

    elif name == "check_availability":
        start_time = datetime.fromisoformat(arguments["start_time"])
        end_time = datetime.fromisoformat(arguments["end_time"])

        result = client.get_free_busy(time_min=start_time, time_max=end_time)

        busy_periods = result.get('calendars', {}).get('primary', {}).get('busy', [])

        if not busy_periods:
            return [TextContent(
                type="text",
                text=f"✅ You are FREE from {start_time} to {end_time}"
            )]
        else:
            output = f"❌ You have {len(busy_periods)} conflict(s):\n\n"
            for period in busy_periods:
                output += f"Busy: {period['start']} to {period['end']}\n"
            return [TextContent(type="text", text=output)]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

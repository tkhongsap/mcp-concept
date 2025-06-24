# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides weather forecasting tools using the National Weather Service API. The server implements the FastMCP framework and exposes weather tools for AI assistants to query US weather conditions, forecasts, and alerts.

## Development Commands

**Install dependencies:** `pip install -r requirements.txt` (add `--break-system-packages` flag if required by system)

**Run the server:** `python src/weather_server.py`

**Test server startup:** `timeout 5s python src/weather_server.py` (kills after 5s to test initialization)

## Architecture

### Core Components

**FastMCP Server:** Single-file server (`src/weather_server.py`) using FastMCP framework with `@mcp.tool()` decorators to register tools.

**Two-Stage Weather Data Flow:**
1. **Geocoding:** Convert location strings to coordinates using OpenStreetMap Nominatim API
2. **Weather Fetching:** Use NWS two-step process: `/points/{lat},{lon}` → get forecast URLs → fetch actual weather data

**Tool Functions:**
- `get_weather()`: Main weather tool with optional alerts
- `get_weather_alerts_only()`: Dedicated alerts tool

### API Integration

**National Weather Service API:** No authentication required, uses proper User-Agent header (`mcp-weather-server/1.0`)

**Request Pattern:** All external API calls go through `make_nws_request()` with error handling and 30s timeout

**Location Handling:** Supports both city names ("Seattle, WA") and coordinates ("47.6062,-122.3321") via regex pattern matching

### Configuration

**IDE Integration:** Configuration templates in `config/` directory:
- `claude_desktop_config.json`: For Claude Desktop integration (update absolute path)
- `vscode_mcp_config.json`: For VS Code/Cursor integration (uses `${workspaceFolder}`)

**Environment:** Optional `.env` file (no API keys required), LOG_LEVEL configurable

## Key Patterns

**Error Handling:** All API failures return `None`, tools return formatted error messages to users

**US-Only Coverage:** NWS API limited to US territories, geocoding restricted with `countrycodes: "us"`

**Async/Await:** All external API calls are async, main server uses `mcp.run()` (not `asyncio.run()`)

## Important Notes

- Server must be restarted after code changes for testing
- Keep weather_server.py under 300 lines (currently ~260 lines)
- Dependencies: Only `mcp>=1.0.0` and `httpx>=0.27.0` required
- NWS API has reasonable rate limits, no need for caching
- Always kill existing servers before starting new ones during development
- Focus on iterating existing patterns rather than introducing new technologies
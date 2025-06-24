# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of MCP (Model Context Protocol) servers providing various tools and capabilities for AI assistants. The repository serves as a development workspace for building and testing multiple MCP servers in a modular structure.

### Current Servers
- **Weather Server** (`servers/weather/`): Provides weather forecasting tools using the National Weather Service API

## Development Commands

**Install global dependencies:** `pip install -r requirements.txt` (add `--break-system-packages` flag if required by system)

**Install server-specific dependencies:** `pip install -r servers/[server-name]/requirements.txt`

**Run weather server:** `python servers/weather/weather_server.py`

**Test weather server startup:** `timeout 5s python servers/weather/weather_server.py` (kills after 5s to test initialization)

**Run any server:** `python servers/[server-name]/[server-name]_server.py`

**Debug server:** Set `LOG_LEVEL=DEBUG` in environment or config files for verbose logging

**Kill existing servers:** Always kill existing servers before starting new ones during development to avoid port conflicts

## Architecture

### Project Structure

```
mcp-concept/
├── servers/                    # Individual MCP servers
│   ├── weather/               # Weather forecasting server
│   │   ├── weather_server.py  # Main server implementation
│   │   ├── requirements.txt   # Server-specific dependencies
│   │   ├── README.md         # Server documentation
│   │   └── __init__.py       # Package initialization
│   └── [future-servers]/     # Additional servers
├── config/                   # IDE configuration templates
├── requirements.txt          # Global dependencies
└── CLAUDE.md                # This file
```

### Weather Server Components

**FastMCP Server:** Single-file server (`servers/weather/weather_server.py`) using FastMCP framework with `@mcp.tool()` decorators to register tools.

**Two-Stage Weather Data Flow:**
1. **Geocoding:** Convert location strings to coordinates using OpenStreetMap Nominatim API
2. **Weather Fetching:** Use NWS two-step process: `/points/{lat},{lon}` → get forecast URLs → fetch actual weather data

**Tool Functions:**
- `get_weather()`: Main weather tool with optional alerts (shows current + 8 forecast periods)
- `get_weather_alerts_only()`: Dedicated alerts tool (shows up to active alerts)
- Helper functions: `geocode_location()`, `get_nws_forecast_data()`, `get_weather_alerts()`, `format_alert()`, `format_forecast_period()`

### API Integration

**National Weather Service API:** No authentication required, uses proper User-Agent header (`mcp-weather-server/1.0`)

**Request Pattern:** All external API calls go through `make_nws_request()` with error handling and 30s timeout

**Location Handling:** Supports both city names ("Seattle, WA") and coordinates ("47.6062,-122.3321") via regex pattern matching in `geocode_location()` function

### Configuration

**IDE Integration:** Configuration templates in `config/` directory:
- `claude_desktop_config.json`: For Claude Desktop integration (update absolute path to point to `servers/weather/weather_server.py`)
- `vscode_mcp_config.json`: For VS Code/Cursor integration (uses `${workspaceFolder}/servers/weather/weather_server.py`)

**Environment:** Optional `.env` file (no API keys required), LOG_LEVEL configurable

## Key Patterns

**Error Handling:** All API failures return `None`, tools return formatted error messages to users

**US-Only Coverage:** NWS API limited to US territories, geocoding restricted with `countrycodes: "us"`

**Async/Await:** All external API calls are async, main server uses `mcp.run()` (not `asyncio.run()`)

## Development Patterns

### Adding New Servers
1. Create new directory under `servers/[server-name]/`
2. Follow established patterns from weather server
3. Use FastMCP framework with `@mcp.tool()` decorators
4. Create server-specific `requirements.txt`, `README.md`, and `__init__.py`
5. Update config files to include new server
6. Keep individual servers focused on specific capabilities

### Important Notes
- Servers must be restarted after code changes for testing
- Keep individual server files under 300 lines when possible (weather server currently ~259 lines)
- Each server should focus on a specific set of related capabilities
- Always kill existing servers before starting new ones during development
- Follow existing error handling and async patterns from weather server
- Include comprehensive documentation for each server
- MCP servers use stdio transport and require proper FastMCP initialization with `mcp.run()`
- All external API calls should be async with proper timeout handling (30s default)
- Configuration files in `config/` directory need absolute paths updated for new servers
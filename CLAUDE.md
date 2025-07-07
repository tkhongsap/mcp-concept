# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a collection of MCP (Model Context Protocol) servers providing various tools and capabilities for AI assistants. The repository serves as a development workspace for building and testing multiple MCP servers in a modular structure.

### Current Servers
- **Weather Server** (`servers/weather/`): Provides weather forecasting tools using the National Weather Service API
- **Simple Weather Server** (`servers/weather/simple_weather_server.py`): Minimal implementation example (~150 lines)

### Prerequisites
- Python 3.10 or higher
- Internet connection for API calls

## Development Commands

### Environment Setup
**Create virtual environment:** `python -m venv venv`

**Activate virtual environment:** 
- Linux/Mac: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Install dependencies:**
```bash
pip install -r requirements.txt  # Global dependencies (add --break-system-packages if needed)
pip install -r servers/[server-name]/requirements.txt  # Server-specific
```

### Server Operations
**Run weather server:** `python servers/weather/weather_server.py`

**Run simple weather server:** `python servers/weather/simple_weather_server.py`

**Test server startup:** `timeout 5s python servers/weather/weather_server.py` (kills after 5s to test initialization)

**Debug mode:** `LOG_LEVEL=DEBUG python servers/weather/weather_server.py`

**Kill existing servers:** Always kill existing servers before starting new ones during development - use `Ctrl+C` or `pkill -f python` if needed

### Validation & Testing
**Test server tools:** After starting a server, test its tools through Claude Desktop or VS Code

**Validate API responses:** Check that external API calls (NWS, OpenStreetMap) are working correctly

**No automated tests:** Currently no unit/integration tests - all testing is manual through IDE integrations

## Architecture

### Project Structure
```
mcp-concept/
├── servers/                    # Individual MCP servers
│   ├── weather/               # Weather forecasting server
│   │   ├── weather_server.py  # Main server implementation (~259 lines)
│   │   ├── simple_weather_server.py  # Minimal example (~150 lines)
│   │   ├── requirements.txt   # Server-specific dependencies
│   │   ├── README.md         # Server documentation
│   │   └── __init__.py       # Package initialization
│   └── [future-servers]/     # Additional servers
├── config/                   # IDE configuration templates
├── requirements.txt          # Global dependencies (mcp>=1.0.0, httpx>=0.27.0)
├── .env.example             # Environment template
└── CLAUDE.md                # This file
```

### Weather Server Components

**FastMCP Server:** Single-file server using FastMCP framework with `@mcp.tool()` decorators to register tools

**Two-Stage Weather Data Flow:**
1. **Geocoding:** Convert location strings to coordinates using OpenStreetMap Nominatim API
2. **Weather Fetching:** Use NWS two-step process: `/points/{lat},{lon}` → get forecast URLs → fetch actual weather data

**Tool Functions:**
- `get_weather()`: Main weather tool with optional alerts (current conditions + 7-day forecast with 12-hour periods)
- `get_weather_alerts_only()`: Dedicated alerts tool (shows active warnings, watches, advisories)
- Helper functions: `geocode_location()`, `get_nws_forecast_data()`, `get_weather_alerts()`, `format_alert()`, `format_forecast_period()`

**Weather Output Includes:**
- Current conditions: temperature, wind speed/direction, conditions
- 7-day forecast: 12-hour periods with detailed weather information
- Weather alerts: severe weather warnings, watches, advisories

### API Integration

**National Weather Service API:** 
- No authentication required
- Uses proper User-Agent header (`mcp-weather-server/1.0`)
- Reasonable rate limits for normal usage

**Request Pattern:** All external API calls go through `make_nws_request()` with error handling and 30s timeout

**Location Handling:** Supports both city names ("Seattle, WA") and coordinates ("47.6062,-122.3321") via regex pattern matching

### Configuration

**IDE Integration:** Configuration templates in `config/` directory:
- `claude_desktop_config.json`: For Claude Desktop integration (requires absolute path)
- `vscode_mcp_config.json`: For VS Code/Cursor integration (uses `${workspaceFolder}` relative path)

**Environment Configuration:** 
- Copy `.env.example` to `.env` if needed (no API keys required)
- Configure `LOG_LEVEL` (INFO, DEBUG, WARNING, ERROR)
- Environment variables take precedence over config file settings

**Path Requirements:**
- Claude Desktop configs require absolute paths - update `/absolute/path/to/mcp-concept/` to your actual path
- VS Code/Cursor configs use workspace-relative paths with `${workspaceFolder}`
- Always verify paths exist before testing integration

## Key Patterns

**Error Handling:** All API failures return `None`, tools return formatted error messages to users

**US-Only Coverage:** NWS API limited to US territories, geocoding restricted with `countrycodes: "us"`

**Async/Await:** All external API calls are async, main server uses `mcp.run()` (not `asyncio.run()`)

**Transport:** MCP servers use stdio transport for communication with AI assistants

## Development Patterns

### Adding New Servers
1. Create new directory under `servers/[server-name]/`
2. Follow established patterns from weather server as template
3. Use FastMCP framework with `@mcp.tool()` decorators
4. Create server-specific `requirements.txt`, `README.md`, and `__init__.py`
5. Update both config files in `config/` directory
6. Keep individual servers focused on specific capabilities
7. Test integration with AI assistants before committing

### Development Workflow
1. Make code changes
2. Kill existing server (`Ctrl+C`)
3. Restart server
4. Test in Claude Desktop/VS Code
5. Check logs for issues
6. Iterate

### Code Standards
- Keep individual server files under 300 lines when possible
- Each server should focus on a specific set of related capabilities
- Follow existing error handling and async patterns
- All external API calls should be async with proper timeout handling (30s default)
- Return user-friendly error messages, not raw exceptions
- Use consistent logging with proper log levels
- No build process - pure Python with minimal dependencies

### Troubleshooting

**Common Issues:**
- **"Could not find coordinates for location"**: Ensure you're using US locations with state (e.g., "Denver, CO")
- **"Location may be outside the US"**: The NWS API only covers US territories
- **Connection errors**: Check your internet connection
- **Import errors**: Ensure virtual environment is activated and dependencies installed
- **Server won't start**: Check Python version (3.10+) and dependencies
- **Configuration issues**: Verify absolute paths in config files match your installation

### Future Servers (Planned)
- Database/SQL query server
- File system operations server  
- API integration server
- Custom business logic server
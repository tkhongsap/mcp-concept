# Weather MCP Server

A Model Context Protocol server that provides weather forecasting tools using the **National Weather Service API** - completely free, no API keys required!

## Overview

This MCP server implements weather tools that allow AI models to fetch current weather conditions, forecasts, and alerts for US locations. It uses the official National Weather Service API and integrates seamlessly with AI assistants.

## Features

- 🌤️ **Current weather conditions** (temperature, wind, conditions)
- 📅 **7-day detailed forecasts** with 12-hour periods
- 🚨 **Weather alerts** (severe weather warnings, watches, advisories)
- 🌍 **US location support** (city names, coordinates)
- 🆓 **Completely free** - no API keys required!
- ⚡ **FastMCP framework** for improved performance

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python weather_server.py
   ```

## Available Tools

### get_weather

Fetches current weather conditions and forecast for a US location.

**Parameters:**
- `location` (required): City name with state (e.g., "Seattle, WA") or coordinates (e.g., "47.6062,-122.3321")
- `include_alerts` (optional): Whether to include active weather alerts (default: false)

**Example usage in AI assistant:**
```
"Get the weather for Seattle, WA"
"Show me the forecast for New York, NY with alerts"
"What's the weather at coordinates 40.7128,-74.0060?"
```

### get_weather_alerts_only

Fetches only active weather alerts for a US location.

**Parameters:**
- `location` (required): City name with state or coordinates

**Example usage:**
```
"Get weather alerts for Miami, FL"
"Are there any weather warnings for 25.7617,-80.1918?"
```

## Architecture

### Two-Stage Weather Data Flow

1. **Geocoding:** Convert location strings to coordinates using OpenStreetMap Nominatim API
2. **Weather Fetching:** Use NWS two-step process:
   - `/points/{lat},{lon}` → get forecast URLs
   - Fetch actual weather data from forecast URLs

### Key Components

- **FastMCP Server:** Uses `@mcp.tool()` decorators to register tools
- **Error Handling:** All API failures return formatted error messages
- **Location Support:** Supports both city names and coordinates via regex pattern matching
- **US-Only Coverage:** NWS API limited to US territories

### Helper Functions

- `geocode_location()`: Convert location strings to coordinates
- `get_nws_forecast_data()`: Fetch forecast data from NWS API
- `get_weather_alerts()`: Fetch active weather alerts
- `format_alert()`: Format alert information for display
- `format_forecast_period()`: Format forecast periods for display
- `make_nws_request()`: Handle all external API calls with error handling

## API Integration

- **National Weather Service API:** No authentication required
- **User-Agent:** Uses proper header (`mcp-weather-server/1.0`)
- **Timeout:** 30 second timeout for all requests
- **Rate Limits:** NWS API has reasonable rate limits for normal usage

## Configuration

### Environment Variables (Optional)

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

### Integration Examples

**Claude Desktop:**
```json
{
  "mcpServers": {
    "weather": {
      "command": "python3",
      "args": ["/path/to/servers/weather/weather_server.py"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**VS Code/Cursor:**
```json
{
  "mcp.servers": [{
    "name": "weather-server",
    "command": "python3",
    "args": ["${workspaceFolder}/servers/weather/weather_server.py"],
    "env": {
      "LOG_LEVEL": "INFO"
    },
    "transport": "stdio"
  }]
}
```

## Troubleshooting

- **"Could not find coordinates for location"**: Ensure you're using US locations with state (e.g., "Denver, CO")
- **"Location may be outside the US"**: The NWS API only covers US territories
- **Connection errors**: Check your internet connection
- **Rate limiting**: The NWS API has reasonable rate limits for normal usage
- **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

## Development

### Code Structure

The server is implemented as a single file (`weather_server.py`) with:
- Tool functions decorated with `@mcp.tool()`
- Helper functions for API interactions
- Async/await patterns for all external API calls
- Comprehensive error handling

### Adding Features

To extend the server:
1. Add new tools using the `@mcp.tool()` decorator
2. Implement additional NWS API endpoints (observations, radar, etc.)
3. Add support for more location formats
4. Keep the file under 300 lines for maintainability

### Testing

```bash
# Test server startup (kills after 5s)
timeout 5s python weather_server.py

# Set debug logging
LOG_LEVEL=DEBUG python weather_server.py
```

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol framework  
- `httpx>=0.27.0` - HTTP client for API requests

## License

MIT
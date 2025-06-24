# NWS Weather MCP Server

A simple MCP (Model Context Protocol) server that provides weather forecast information using the **National Weather Service API** - completely free, no API keys required!

## Overview

This MCP server implements weather tools that allow AI models to fetch current weather conditions, forecasts, and alerts for US locations. It uses the official National Weather Service API and can be integrated with VS Code, Cursor, or Claude Desktop.

## Features

- 🌤️ **Current weather conditions** (temperature, wind, conditions)
- 📅 **7-day detailed forecasts** with 12-hour periods
- 🚨 **Weather alerts** (severe weather warnings, watches, advisories)
- 🌍 **US location support** (city names, coordinates)
- 🆓 **Completely free** - no API keys required!
- ⚡ **FastMCP framework** for improved performance

## Prerequisites

- Python 3.10 or higher
- Internet connection (no API keys needed!)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mcp-concept.git
   cd mcp-concept
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   The `.env` file is optional - no API keys required!

## Usage

### Running the Server Standalone

```bash
python src/weather_server.py
```

### Integration with Claude Desktop

1. Open Claude Desktop settings
2. Navigate to the MCP servers configuration
3. Add the weather server configuration from `config/claude_desktop_config.json`
4. Update the path to point to your installation directory
5. Restart Claude Desktop

### Integration with VS Code/Cursor

1. Install the MCP extension for VS Code/Cursor
2. Add the configuration from `config/vscode_mcp_config.json` to your settings
3. Reload the window to activate the server

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

## Development

### Project Structure
```
mcp-concept/
├── src/
│   └── weather_server.py    # Main server implementation
├── config/                  # IDE configuration examples
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

### Adding New Features

To extend the server:
1. Add new tools using the `@mcp.tool()` decorator
2. Implement additional NWS API endpoints (observations, radar, etc.)
3. Add support for more location formats

## Troubleshooting

- **"Could not find coordinates for location"**: Ensure you're using US locations with state (e.g., "Denver, CO")
- **"Location may be outside the US"**: The NWS API only covers US territories
- **Connection errors**: Check your internet connection
- **Rate limiting**: The NWS API has reasonable rate limits for normal usage

## License

MIT
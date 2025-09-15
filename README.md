# Weather MCP Server

A minimal Model Context Protocol (MCP) server that provides US weather forecasts and alerts using the National Weather Service (NWS) API. No API keys required.

## Features

- Current conditions and multi-period forecasts
- Active weather alerts
- US locations via city/state or coordinates
- Async `httpx` + FastMCP; simple, single-file server

## Quick Start

Prerequisites
- Python 3.10+
- Internet connection

Setup
- Create and activate a virtualenv
  - `python -m venv venv && source venv/bin/activate` (Windows: `venv\\Scripts\\activate`)
- Install dependencies
  - `pip install -r requirements.txt`

Run
- `python servers/weather/weather_server.py`

## MCP Tools

- `get_weather(location, include_alerts=False)`
  - Returns current conditions and forecast; optionally includes active alerts
- `get_weather_alerts_only(location)`
  - Returns only active weather alerts

Location examples: `"Seattle, WA"`, `"47.6062,-122.3321"`

## Integration

Claude Desktop
- Edit `config/claude_desktop_config.json` and replace the placeholder absolute path with your local path to `servers/weather/weather_server.py`

VS Code/Cursor
- Use `config/vscode_mcp_config.json` (workspace-relative path)

Optional
- `LOG_LEVEL=DEBUG` for verbose logging (see `.env.example`)

## Project Structure

```
servers/
  weather/
    weather_server.py
    README.md
    requirements.txt
config/
  claude_desktop_config.json
  vscode_mcp_config.json
requirements.txt
README.md
```

## License

MIT

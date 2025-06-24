# MCP Server Collection

A collection of custom MCP (Model Context Protocol) servers providing various tools and capabilities for AI assistants. This repository serves as a development workspace for building and testing multiple MCP servers.

## Overview

This repository contains multiple MCP servers, each providing specialized tools and capabilities. The servers are organized in a modular structure, allowing for easy development, testing, and deployment of individual components.

## Available Servers

### 🌤️ Weather Server
**Location:** `servers/weather/`

Provides weather forecasting tools using the National Weather Service API - completely free, no API keys required!

**Features:**
- Current weather conditions and 7-day forecasts
- Weather alerts and warnings
- US location support (city names or coordinates)
- Built with FastMCP framework

**Tools:**
- `get_weather()` - Get weather conditions and forecasts
- `get_weather_alerts_only()` - Get active weather alerts

### 🚧 Future Servers

Additional MCP servers will be added to this collection:
- Database/SQL query server
- File system operations server  
- API integration server
- Custom business logic server

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Internet connection

### Installation

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

3. Install global dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Individual Servers

Each server can be run independently:

```bash
# Weather server
python servers/weather/weather_server.py

# Future servers
python servers/[server-name]/[server-name]_server.py
```

## Integration

### Claude Desktop Integration

1. Update the configuration in `config/claude_desktop_config.json`
2. Replace `/absolute/path/to/mcp-concept` with your actual installation path
3. Add the configuration to Claude Desktop settings
4. Restart Claude Desktop

### VS Code/Cursor Integration

1. Install the MCP extension
2. Use the configuration from `config/vscode_mcp_config.json`
3. Reload the window to activate servers

## Project Structure

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
│   ├── claude_desktop_config.json
│   └── vscode_mcp_config.json
├── requirements.txt          # Global dependencies
├── CLAUDE.md                # Development instructions
└── README.md               # This file
```

## Development

### Adding New Servers

1. Create a new directory under `servers/`
2. Follow the established patterns from existing servers
3. Use FastMCP framework with `@mcp.tool()` decorators
4. Create server-specific documentation and requirements
5. Update configuration files to include the new server

### Best Practices

- Each server should focus on a specific set of related capabilities
- Use proper error handling and return meaningful error messages
- Follow the existing code style and patterns
- Include comprehensive documentation for each server
- Test servers individually and in combination

## Configuration Management

The `config/` directory contains templates for integrating with various tools:

- **claude_desktop_config.json**: For Claude Desktop integration
- **vscode_mcp_config.json**: For VS Code/Cursor integration

Update the absolute paths in these files to match your installation directory.

## Troubleshooting

- **Server won't start**: Check Python version (3.10+) and dependencies
- **Configuration issues**: Verify absolute paths in config files
- **Import errors**: Ensure virtual environment is activated
- **Server-specific issues**: Check individual server documentation

## Contributing

When adding new servers:
1. Follow the established directory structure
2. Include proper documentation
3. Add configuration examples
4. Test integration with AI assistants
5. Update this README with server information

## License

MIT
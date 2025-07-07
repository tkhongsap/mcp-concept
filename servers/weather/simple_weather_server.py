#!/usr/bin/env python3
"""
Simple Weather MCP Server
A simplified weather server using the National Weather Service API
"""

import logging
from typing import Any, Dict, Optional, Tuple

import httpx
from mcp.server.fastmcp import FastMCP

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simple-weather")
mcp = FastMCP("simple-weather")

# Constants
NWS_BASE = "https://api.weather.gov"
GEOCODING_API = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "simple-weather-mcp/1.0"


async def get_coordinates(location: str) -> Optional[Tuple[float, float]]:
    """Convert location name to lat/lon coordinates."""
    # If already coordinates, parse them
    if ',' in location and location.replace('-', '').replace('.', '').replace(',', '').isdigit():
        try:
            lat, lon = map(float, location.split(','))
            return lat, lon
        except ValueError:
            pass
    
    # Otherwise, geocode the location
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "us"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                GEOCODING_API, 
                params=params, 
                headers={"User-Agent": USER_AGENT},
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
                
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
    
    return None


async def fetch_weather_data(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """Fetch weather data from NWS API."""
    headers = {"User-Agent": USER_AGENT}
    
    async with httpx.AsyncClient() as client:
        try:
            # Get point data first
            point_response = await client.get(
                f"{NWS_BASE}/points/{lat},{lon}",
                headers=headers,
                timeout=30.0
            )
            point_response.raise_for_status()
            point_data = point_response.json()
            
            # Get forecast URL
            forecast_url = point_data["properties"]["forecast"]
            
            # Get forecast data
            forecast_response = await client.get(forecast_url, headers=headers, timeout=30.0)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            return {
                "location": point_data["properties"],
                "forecast": forecast_data["properties"]["periods"]
            }
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return None


@mcp.tool()
async def get_weather(location: str) -> str:
    """
    Get weather forecast for a US location.
    
    Args:
        location: City name and state (e.g., "Seattle, WA") or coordinates (e.g., "47.6,-122.3")
    
    Returns:
        Weather forecast as formatted text
    """
    # Get coordinates
    coords = await get_coordinates(location)
    if not coords:
        return f"❌ Could not find location: {location}"
    
    lat, lon = coords
    
    # Get weather data
    weather_data = await fetch_weather_data(lat, lon)
    if not weather_data:
        return f"❌ Could not get weather data for {location}"
    
    # Format response
    location_info = weather_data["location"]
    forecast_periods = weather_data["forecast"]
    
    # Get location name
    rel_location = location_info.get("relativeLocation", {}).get("properties", {})
    city = rel_location.get("city", "Unknown")
    state = rel_location.get("state", "Unknown")
    
    result = f"🌤️ **Weather for {city}, {state}**\n"
    result += f"📍 {lat:.2f}, {lon:.2f}\n\n"
    
    # Show current and next few periods
    for i, period in enumerate(forecast_periods[:6]):
        name = period.get("name", "Unknown")
        temp = period.get("temperature", "?")
        unit = period.get("temperatureUnit", "F")
        forecast = period.get("shortForecast", "No data")
        
        if i == 0:
            result += f"**Current: {name}**\n"
        else:
            result += f"**{name}**\n"
            
        result += f"🌡️ {temp}°{unit} - {forecast}\n\n"
    
    return result.strip()


if __name__ == "__main__":
    logger.info("Starting Simple Weather MCP Server...")
    mcp.run() 
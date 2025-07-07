#!/usr/bin/env python3
"""
NWS Weather MCP Server
Provides weather forecast information using the National Weather Service API
"""

import re
import logging
from typing import Any, Dict, Optional

import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nws-weather-server")

# Initialize FastMCP server
mcp = FastMCP("nws-weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "mcp-weather-server/1.0"
GEOCODING_API = "https://nominatim.openstreetmap.org/search"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"NWS API request failed: {e}")
            return None


async def geocode_location(location: str) -> tuple[float, float] | None:
    """Convert location name to coordinates using OpenStreetMap Nominatim."""
    # Check if location is already coordinates (lat,lon format)
    coord_pattern = r'^-?\d+\.?\d*,-?\d+\.?\d*$'
    if re.match(coord_pattern, location):
        try:
            lat, lon = map(float, location.split(','))
            return lat, lon
        except ValueError:
            return None
    
    # Geocode location name
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "us"  # NWS only covers US
    }
    headers = {"User-Agent": USER_AGENT}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GEOCODING_API, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]["lat"])
                lon = float(data[0]["lon"])
                return lat, lon
            return None
        except Exception as e:
            logger.error(f"Geocoding failed: {e}")
            return None


async def get_nws_forecast_data(lat: float, lon: float) -> dict[str, Any] | None:
    """Get forecast data from NWS API using coordinates."""
    # Step 1: Get point data to find the forecast office and grid
    point_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    point_data = await make_nws_request(point_url)
    
    if not point_data:
        return None
    
    properties = point_data.get("properties", {})
    forecast_url = properties.get("forecast")
    forecast_hourly_url = properties.get("forecastHourly")
    
    if not forecast_url:
        return None
    
    # Step 2: Get the actual forecast
    forecast_data = await make_nws_request(forecast_url)
    if not forecast_data:
        return None
    
    # Step 3: Get current conditions (from hourly forecast)
    current_data = None
    if forecast_hourly_url:
        current_data = await make_nws_request(forecast_hourly_url)
    
    return {
        "location": properties,
        "forecast": forecast_data,
        "current": current_data
    }


async def get_weather_alerts(lat: float, lon: float) -> list[dict] | None:
    """Get active weather alerts for the location."""
    alerts_url = f"{NWS_API_BASE}/alerts/active?point={lat},{lon}"
    alerts_data = await make_nws_request(alerts_url)
    
    if not alerts_data:
        return None
    
    return alerts_data.get("features", [])


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
🚨 **{props.get('event', 'Weather Alert')}**
📍 Area: {props.get('areaDesc', 'Unknown')}
⚠️ Severity: {props.get('severity', 'Unknown')}
📝 Description: {props.get('description', 'No description available')}
📋 Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


def format_forecast_period(period: dict) -> str:
    """Format a forecast period into a readable string."""
    name = period.get("name", "Unknown")
    temp = period.get("temperature", "Unknown")
    temp_unit = period.get("temperatureUnit", "F")
    short_forecast = period.get("shortForecast", "No forecast available")
    detailed_forecast = period.get("detailedForecast", "")
    
    result = f"**{name}**: {temp}°{temp_unit} - {short_forecast}"
    if detailed_forecast and detailed_forecast != short_forecast:
        result += f"\n   Details: {detailed_forecast}"
    
    return result


@mcp.tool()
async def get_weather(location: str, include_alerts: bool = False) -> str:
    """
    Get weather forecast for a US location using the National Weather Service API.
    
    Args:
        location: City name, state (e.g., "Seattle, WA") or coordinates (e.g., "47.6062,-122.3321")
        include_alerts: Whether to include active weather alerts
    
    Returns:
        Weather forecast information as a formatted string
    """
    try:
        # Geocode the location
        coords = await geocode_location(location)
        if not coords:
            return f"❌ Could not find coordinates for location: {location}. Please ensure it's a valid US location."
        
        lat, lon = coords
        logger.info(f"Getting weather for {location} at coordinates {lat}, {lon}")
        
        # Get forecast data
        weather_data = await get_nws_forecast_data(lat, lon)
        if not weather_data:
            return f"❌ Could not retrieve weather data for {location}. The location may be outside the US or the NWS service may be unavailable."
        
        # Extract location information
        location_props = weather_data["location"]
        location_name = f"{location_props.get('relativeLocation', {}).get('properties', {}).get('city', 'Unknown')}, {location_props.get('relativeLocation', {}).get('properties', {}).get('state', 'Unknown')}"
        
        # Build response
        result = f"🌤️ **Weather Forecast for {location_name}**\n"
        result += f"📍 Coordinates: {lat:.4f}, {lon:.4f}\n"
        result += f"🏢 NWS Office: {location_props.get('cwa', 'Unknown')}\n\n"
        
        # Current conditions (from first hourly forecast)
        if weather_data.get("current") and weather_data["current"].get("properties", {}).get("periods"):
            current_period = weather_data["current"]["properties"]["periods"][0]
            result += "**Current Conditions:**\n"
            result += f"🌡️ Temperature: {current_period.get('temperature', 'Unknown')}°{current_period.get('temperatureUnit', 'F')}\n"
            result += f"🌤️ Conditions: {current_period.get('shortForecast', 'Unknown')}\n"
            result += f"💨 Wind: {current_period.get('windSpeed', 'Unknown')} {current_period.get('windDirection', '')}\n\n"
        
        # Forecast periods
        forecast_periods = weather_data["forecast"].get("properties", {}).get("periods", [])
        if forecast_periods:
            result += "**Forecast:**\n"
            for period in forecast_periods[:8]:  # Show next 8 periods (about 4 days)
                result += f"{format_forecast_period(period)}\n"
        
        # Weather alerts
        if include_alerts:
            alerts = await get_weather_alerts(lat, lon)
            if alerts:
                result += "\n**🚨 Active Weather Alerts:**\n"
                for alert in alerts[:3]:  # Show up to 3 most recent alerts
                    result += format_alert(alert)
            else:
                result += "\n✅ No active weather alerts for this area.\n"
        
        return result.strip()
        
    except Exception as e:
        logger.error(f"Error in get_weather: {str(e)}")
        return f"❌ Error retrieving weather data: {str(e)}"


@mcp.tool()
async def get_weather_alerts_only(location: str) -> str:
    """
    Get active weather alerts for a US location.
    
    Args:
        location: City name, state (e.g., "Seattle, WA") or coordinates (e.g., "47.6062,-122.3321")
    
    Returns:
        Active weather alerts as a formatted string
    """
    try:
        # Geocode the location
        coords = await geocode_location(location)
        if not coords:
            return f"❌ Could not find coordinates for location: {location}. Please ensure it's a valid US location."
        
        lat, lon = coords
        logger.info(f"Getting weather alerts for {location} at coordinates {lat}, {lon}")
        
        # Get weather alerts
        alerts = await get_weather_alerts(lat, lon)
        if not alerts:
            return f"✅ No active weather alerts for {location}."
        
        result = f"🚨 **Active Weather Alerts for {location}**\n"
        result += f"📍 Coordinates: {lat:.4f}, {lon:.4f}\n\n"
        
        for i, alert in enumerate(alerts, 1):
            result += f"**Alert {i}:**"
            result += format_alert(alert)
            result += "\n"
        
        return result.strip()
        
    except Exception as e:
        logger.error(f"Error in get_weather_alerts_only: {str(e)}")
        return f"❌ Error retrieving weather alerts: {str(e)}"


if __name__ == "__main__":
    logger.info("Starting NWS Weather MCP Server...")
    mcp.run()
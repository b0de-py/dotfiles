#!/usr/bin/env python3
import json
import urllib.request
import os
import sys
import time
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from waybar_logging import (
    get_logger,
    safe_execute,
    PerformanceTimer,
    log_script_start,
    log_script_end,
)

# Configuration
CONFIG_DIR = os.path.expanduser("~/.config/waybar")
CONFIG_FILE = os.path.join(CONFIG_DIR, "weather_config.json")
CACHE_FILE = "/tmp/waybar_weather_cache"

# Default configuration
DEFAULT_CONFIG = {
    "location": {
        "name": "Guará, DF",
        "latitude": "-15.82",
        "longitude": "-47.98",
        "timezone": "America/Sao_Paulo",
    },
    "units": {
        "temperature": "celsius",  # celsius or fahrenheit
        "wind_speed": "kmh",
    },
    "display": {
        "show_location": True,
        "show_forecast": True,
        "forecast_hours": [6, 9, 11, 12, 15, 17, 19, 22, 24],
        "cache_duration": 1800,  # 30 minutes in seconds
        "update_interval": 1800,  # 30 minutes
    },
    "alerts": {
        "enabled": True,
        "temperature_threshold": 35,  # Alert if temperature above this
        "air_quality": {
            "enabled": False,  # Air quality monitoring (requires additional API data)
            "threshold": 100,  # Alert if AQI above this level
        },
    },
}


def load_config():
    """Load configuration from file or create default"""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Merge with defaults
                return {**DEFAULT_CONFIG, **config}
        except:
            return DEFAULT_CONFIG
    else:
        # Create default config file
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG


def get_cached_data(cache_duration):
    """Get weather data from cache if valid"""
    if not os.path.exists(CACHE_FILE):
        return None

    try:
        with open(CACHE_FILE, "r") as f:
            cache_data = json.load(f)

        # Check if cache is still valid
        if time.time() - cache_data["timestamp"] < cache_duration:
            return cache_data["data"]
    except:
        pass

    return None


def cache_data(data):
    """Cache weather data with timestamp"""
    try:
        cache_entry = {"timestamp": time.time(), "data": data}
        with open(CACHE_FILE, "w") as f:
            json.dump(cache_entry, f)
    except:
        pass


def convert_temperature(temp_celsius, unit):
    """Convert temperature based on unit"""
    if unit.lower() == "fahrenheit":
        return round(temp_celsius * 9 / 5 + 32)
    return round(temp_celsius)


def get_temperature_unit_symbol(unit):
    """Get temperature unit symbol"""
    return "°F" if unit.lower() == "fahrenheit" else "°C"


def get_weather_data(config):
    """Fetch weather data from API with caching"""
    cache_duration = config["display"]["cache_duration"]

    # Try to get from cache first
    cached = get_cached_data(cache_duration)
    if cached:
        return cached

    # Build URL with all needed parameters
    location = config["location"]
    base_url = "https://api.open-meteo.com/v1/forecast"

    # Base parameters
    params = [
        f"latitude={location['latitude']}",
        f"longitude={location['longitude']}",
        "current_weather=true",
        "hourly=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m",
        f"timezone={location['timezone']}",
    ]

    # Add air quality if enabled
    if config["alerts"].get("air_quality", {}).get("enabled", False):
        params.extend(["hourly=pm10,pm2_5,aqi", "domains=air_quality"])

    url = f"{base_url}?{'&'.join(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())

            # Cache the successful response
            cache_data(data)
            return data

    except Exception as e:
        # If network fails, try to return stale cache
        stale_cache = get_cached_data(cache_duration * 10)  # Allow 10x older cache
        if stale_cache:
            return stale_cache
        raise e


def format_weather_data(config):
    """Format weather data for display"""
    try:
        data = get_weather_data(config)
        location = config["location"]
        units = config["units"]
        display = config["display"]
        alerts = config["alerts"]

        # Weather icons
        icons = {
            0: "󰖙",
            1: "󰖐",
            2: "󰖐",
            3: "󰖐",  # Clear/sunny
            45: "󰖑",
            48: "󰖑",  # Foggy
            51: "󰖗",
            53: "󰖗",
            55: "󰖗",  # Drizzle
            61: "󰖖",
            63: "󰖖",
            65: "󰖖",  # Rain
            80: "󰖖",
            81: "󰖖",
            82: "󰖖",  # Rain showers
            95: "󰖓",  # Thunderstorm
            71: "󰖘",
            73: "󰖘",
            75: "󰖘",
            77: "󰖘",
            85: "󰖘",
            86: "󰖘",  # Snow
        }

        current = data["current_weather"]
        hourly = data["hourly"]

        # Current temperature with unit conversion
        temp_c = current["temperature"]
        temp = convert_temperature(temp_c, units["temperature"])
        temp_symbol = get_temperature_unit_symbol(units["temperature"])

        # Current weather icon
        icon = icons.get(current["weathercode"], "")

        # Air quality data
        aqi_data = None
        if alerts.get("air_quality", {}).get("enabled", False):
            if "air_quality" in hourly:
                aqi_hourly = hourly["air_quality"]
                if aqi_hourly and len(aqi_hourly) > 0:
                    aqi_data = aqi_hourly[0]  # Current AQI
                    if aqi_data == 0:  # 0 often means no data
                        aqi_data = None

        # Build display text
        if display["show_location"]:
            text = f"- {location['name']}. {temp}{temp_symbol}  {icon}  "
        else:
            text = f"{temp}{temp_symbol}  {icon}  "

        # Build tooltip
        tooltip_parts = []
        tooltip_parts.append(f"Status: {icon}  {temp}{temp_symbol}")
        tooltip_parts.append("-" * 40)

        # Current details
        humidity = (
            hourly["relativehumidity_2m"][0]
            if "relativehumidity_2m" in hourly
            else "N/A"
        )
        wind_speed = hourly["windspeed_10m"][0] if "windspeed_10m" in hourly else 0

        tooltip_parts.append(f"Humidity: {humidity}%")
        tooltip_parts.append(f"Wind: {wind_speed} {units['wind_speed']}")
        tooltip_parts.append("")

        # Forecast periods
        if display["show_forecast"]:
            temps = hourly["temperature_2m"]
            codes = hourly["weathercode"]
            hours = display["forecast_hours"]

            # Morning (6-11h)
            morning_hours = [h for h in hours if 6 <= h <= 11]
            if morning_hours:
                morning_parts = []
                for h in morning_hours:
                    t = convert_temperature(temps[h], units["temperature"])
                    i = icons.get(codes[h], "")
                    morning_parts.append(f"{h:02d}h: {t}{temp_symbol} {i}")
                tooltip_parts.append(f"󰖙 Manhã:  {'   '.join(morning_parts)}")

            # Afternoon (12-17h)
            afternoon_hours = [h for h in hours if 12 <= h <= 17]
            if afternoon_hours:
                afternoon_parts = []
                for h in afternoon_hours:
                    t = convert_temperature(temps[h], units["temperature"])
                    i = icons.get(codes[h], "")
                    afternoon_parts.append(f"{h:02d}h: {t}{temp_symbol} {i}")
                tooltip_parts.append(f"󰖐 Tarde:  {'   '.join(afternoon_parts)}")

            # Evening/Night (19-24h)
            evening_hours = [h for h in hours if h >= 19]
            if evening_hours:
                evening_parts = []
                for h in evening_hours:
                    t = convert_temperature(temps[h], units["temperature"])
                    i = icons.get(codes[h], "")
                    evening_parts.append(f"{h:02d}h: {t}{temp_symbol} {i}")
                tooltip_parts.append(f"󰖔 Noite:  {'   '.join(evening_parts)}")

        # Air quality section
        if aqi_data is not None:
            aqi_level = aqi_data
            aqi_config = alerts.get("air_quality", {})
            aqi_threshold = aqi_config.get("threshold", 100)

            # AQI categories and colors
            if aqi_level <= 50:
                aqi_desc = "Good"
                aqi_icon = "🟢"
            elif aqi_level <= 100:
                aqi_desc = "Moderate"
                aqi_icon = "🟡"
            elif aqi_level <= 150:
                aqi_desc = "Unhealthy for Sensitive"
                aqi_icon = "🟠"
            elif aqi_level <= 200:
                aqi_desc = "Unhealthy"
                aqi_icon = "🔴"
            else:
                aqi_desc = "Very Unhealthy"
                aqi_icon = "🟣"

            tooltip_parts.append("")
            tooltip_parts.append(f"Air Quality: {aqi_level} ({aqi_desc}) {aqi_icon}")

            if aqi_level > aqi_threshold:
                tooltip_parts.append(f"⚠️  High AQI alert: {aqi_level}")

        # Alerts section
        if alerts["enabled"] and alerts["temperature_threshold"]:
            if temp_c > alerts["temperature_threshold"]:
                tooltip_parts.append("")
                tooltip_parts.append(f"⚠️  High temperature alert: {temp}{temp_symbol}")

        tooltip_text = "\n".join(tooltip_parts)

        output = {"text": text, "tooltip": tooltip_text, "class": "weather-widget"}

        return json.dumps(output)

    except Exception as e:
        error_msg = f"Weather API Error: {str(e)}"
        return json.dumps(
            {"text": "󰖙 --°C", "tooltip": error_msg, "class": "weather-error"}
        )


def main():
    """Main function"""
    start_time = time.time()

    # Initialize logging
    logger = get_logger("weather")
    log_script_start(logger, sys.argv)

    try:
        # Load configuration
        config = load_config()
        logger.info(f"Weather config loaded: location={config['location']['name']}")

        # Handle command line arguments
        if len(sys.argv) > 1:
            arg = sys.argv[1]
            if arg == "--refresh":
                logger.info("Force refresh requested - clearing cache")
                if os.path.exists(CACHE_FILE):
                    os.remove(CACHE_FILE)
                    logger.info("Cache cleared successfully")
                else:
                    logger.debug("No cache file found to clear")
            elif arg == "--config":
                print(f"Config file: {CONFIG_FILE}")
                logger.info("Config file location requested")
                return

        # Format and display weather data
        result = format_weather_data(config)
        print(result)

    except Exception as e:
        logger.error(f"Weather script failed: {str(e)}")
        print(
            '{"text": "󰖙 --°C", "tooltip": "Weather Error", "class": "weather-error"}'
        )

    finally:
        duration = time.time() - start_time
        log_script_end(logger, duration)


if __name__ == "__main__":
    main()

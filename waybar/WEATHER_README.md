# Enhanced Waybar Weather Widget

The enhanced weather script adds configuration support, caching, and multiple unit options to your waybar.

## Features Added

### ✅ Location Configuration File
- Configurable location via `weather_config.json`
- Support for latitude, longitude, timezone, and location name
- Easy to change location without editing script

### ✅ Intelligent Caching
- 30-minute cache to reduce API calls
- Falls back to stale cache if network fails
- Manual refresh with `--refresh` flag

### ✅ Unit Configuration  
- Celsius/Fahrenheit temperature support
- Wind speed unit configuration
- Automatic conversion and symbol display

### ✅ Enhanced Display Options
- Toggle location display in bar
- Configurable forecast hours
- Detailed tooltip with humidity and wind
- Temperature alerts

## Configuration

Edit `~/.config/waybar/weather_config.json`:

```json
{
  "location": {
    "name": "Guará, DF",                    // Display name
    "latitude": "-15.82",                   // Latitude
    "longitude": "-47.98",                  // Longitude  
    "timezone": "America/Sao_Paulo"          // Timezone
  },
  "units": {
    "temperature": "celsius",               // celsius or fahrenheit
    "wind_speed": "kmh"                     // Wind speed unit
  },
  "display": {
    "show_location": true,                   // Show location in bar
    "show_forecast": true,                   // Show forecast in tooltip
    "forecast_hours": [6, 9, 11, 12, 15, 17, 19, 22, 24],
    "cache_duration": 1800,                  // Cache duration (seconds)
    "update_interval": 1800                  // Update interval (seconds)
  },
  "alerts": {
    "enabled": true,                         // Enable alerts
    "temperature_threshold": 35               // High temp alert threshold
  }
}
```

## Usage

### Waybar Configuration

Update your `waybar/config.jsonc`:

```json
{
  "custom/weather": {
    "format": "{}",
    "tooltip": true,
    "interval": 1800,
    "exec": "/usr/bin/python ~/.config/waybar/weather.py",
    "return-type": "json",
    "on-click": "/usr/bin/python ~/.config/waybar/weather.py --refresh",
    "tooltip-format": "{}"
  }
}
```

### Command Line Options

```bash
# Normal execution (uses cache)
python ~/.config/waybar/weather.py

# Force refresh (ignores cache)
python ~/.config/waybar/weather.py --refresh

# Show config file location
python ~/.config/waybar/weather.py --config
```

## Features

### Caching System
- Reduces API calls from every execution to every 30 minutes
- Prevents rate limiting
- Faster responses
- Graceful fallback to old data if network fails

### Multi-Unit Support
- Automatic temperature conversion between Celsius and Fahrenheit
- Proper unit symbols (°C/°F)
- Configurable wind speed units

### Enhanced Tooltip
- Current conditions with humidity and wind
- Organized forecast periods (Morning/Afternoon/Evening)
- Temperature alerts for extreme conditions
- Clean, readable formatting

### Error Handling
- Network timeouts handled gracefully
- Stale cache fallback
- Clear error messages in tooltip
- JSON output always valid

## Example Cities

To change location, update `weather_config.json`:

**São Paulo:**
```json
"location": {
  "name": "São Paulo, SP",
  "latitude": "-23.55",
  "longitude": "-46.63",
  "timezone": "America/Sao_Paulo"
}
```

**New York:**
```json
"location": {
  "name": "New York, NY", 
  "latitude": "40.71",
  "longitude": "-74.01",
  "timezone": "America/New_York"
}
```

**London:**
```json
"location": {
  "name": "London, UK",
  "latitude": "51.51", 
  "longitude": "-0.13",
  "timezone": "Europe/London"
}
```

## Dependencies

The script uses only Python standard library modules:
- `json` - Configuration and API parsing
- `urllib.request` - HTTP requests to weather API
- `os` - File operations
- `time` - Cache timestamping
- `pathlib` - Path handling

No external dependencies required!
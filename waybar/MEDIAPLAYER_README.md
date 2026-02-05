# Enhanced Waybar MediaPlayer

The enhanced media player adds configuration support, volume display, click actions, and robust logging to your waybar.

## Features Added

### ✅ Configuration File Support
- Customizable icons for different players
- Adjustable text length and formatting
- Volume display options
- Click action configuration
- Player prioritization system

### ✅ Click Actions
- Left click: Play/pause toggle
- Right click: Show menu (customizable)
- Scroll up: Next track
- Scroll down: Previous track
- Command line support for scripts

### ✅ Volume Control & Display
- Real-time volume monitoring
- Dynamic volume icons (muted/low/medium/high)
- Optional percentage display
- Configurable thresholds

### ✅ Advanced Player Management
- Smart player prioritization
- Prefer playing players option
- Custom priority order
- Graceful fallback system

### ✅ Robust Error Handling & Logging
- Unified logging system integration
- Process restart on failure
- Graceful shutdown handling
- Performance monitoring

## Configuration

Edit `~/.config/waybar/mediaplayer_config.json`:

```json
{
  "display": {
    "max_length": 43,
    "show_volume": true,
    "show_player_name": false,
    "paused_prefix": "󰏤 ",
    "format": "{icon} {artist} - {title}"
  },
  "icons": {
    "spotify": " ",
    "firefox": " ",
    "chromium": " ",
    "default": " "
  },
  "volume": {
    "enabled": true,
    "show_percentage": true,
    "low_threshold": 30,
    "medium_threshold": 70,
    "icons": {
      "muted": "󰝟 ",
      "low": "󰖀 ",
      "medium": "󰕾 ",
      "high": "󰕾 "
    }
  },
  "click_actions": {
    "left_click": "play_pause",
    "right_click": "show_menu",
    "scroll_up": "next",
    "scroll_down": "previous"
  },
  "prioritization": {
    "prefer_playing": true,
    "priority_order": ["spotify", "firefox", "chromium", "default"]
  }
}
```

## Configuration Options

### Display Options
- `max_length`: Maximum characters before truncation
- `show_volume`: Enable/disable volume display
- `show_player_name`: Show player name in output
- `paused_prefix`: Prefix for paused tracks
- `format`: Custom format string with variables

### Volume Options
- `enabled`: Enable volume monitoring
- `show_percentage`: Show volume percentage
- `low_threshold`: Volume level for "low" icon
- `medium_threshold`: Volume level for "medium" icon
- `icons`: Custom volume icons

### Click Actions
- `left_click`: Action for left mouse click
- `right_click`: Action for right mouse click  
- `scroll_up`: Action for scroll up
- `scroll_down`: Action for scroll down

**Available Actions:**
- `play_pause`: Toggle play/pause
- `next`: Skip to next track
- `previous`: Go to previous track
- `show_menu`: Show player menu (customizable)

### Player Prioritization
- `prefer_playing`: Prioritize playing players over paused
- `priority_order`: List of player types in preference order

## Waybar Configuration

Update your `waybar/config.jsonc`:

```json
{
  "custom/media": {
    "format": "{}",
    "return-type": "json",
    "exec": "python ~/.config/waybar/mediaplayer.py",
    "on-click": "python ~/.config/waybar/mediaplayer.py play_pause",
    "on-click-right": "python ~/.config/waybar/mediaplayer.py show_menu",
    "on-scroll-up": "python ~/.config/waybar/mediaplayer.py next",
    "on-scroll-down": "python ~/.config/waybar/mediaplayer.py previous"
  }
}
```

## Command Line Usage

```bash
# Normal execution (continuous monitoring)
python ~/.config/waybar/mediaplayer.py

# Execute specific actions
python ~/.config/waybar/mediaplayer.py play_pause
python ~/.config/waybar/mediaplayer.py next
python ~/.config/waybar/mediaplayer.py previous
```

## Output Format

The script outputs JSON with the following structure:

```json
{
  "text": "🎵 Artist - Song Title 🔊85%",
  "class": "playing",
  "tooltip": "spotify: Playing\nArtist - Song Title"
}
```

### Classes
- `playing`: Currently playing
- `paused`: Currently paused  
- `stopped`: Currently stopped
- `empty`: No active player
- `error`: Error occurred

## Features Details

### Smart Player Detection
- Automatically detects all running media players
- Prioritizes based on configurable rules
- Smooth switching between players
- Maintains state for all players

### Volume Integration
- Real-time volume monitoring via playerctl
- Intelligent icon selection based on volume level
- Optional percentage display
- Works with any playerctl-supported player

### Error Resilience
- Automatic process restart on failure
- Graceful degradation when playerctl unavailable
- Comprehensive error logging
- Timeout protection for all subprocess calls

### Performance
- Efficient state management
- Minimal system resource usage
- Fast response to player changes
- Optimized logging levels

## Supported Players

Works with any playerctl-compatible media player:
- Spotify (Desktop/Web)
- Firefox/Chrome audio
- VLC
- MPD
- Rhythmbox
- And many more...

## Logging

Uses the unified waybar logging system:
- Main log: `~/.config/waybar/waybar.log`
- Debug log: `~/.config/waybar/mediaplayer.debug.log`
- Configurable log levels
- Performance tracking

## Dependencies

- `playerctl` - Media player controller
- Python 3.6+
- No additional Python dependencies required
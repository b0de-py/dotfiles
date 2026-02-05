# Enhanced Waybar Calendar

The enhanced calendar script adds timezone support, event integration, and click actions to your waybar.

## Features Added

### ✅ Timezone Configuration
- Customizable timezone via config file
- Default: America/Sao_Paulo
- Supports any pytz timezone

### ✅ Event Integration
- Reads events from `~/.config/waybar/calendar_events.txt`
- Supports specific dates: `2024-12-25 Christmas Day`
- Supports yearly recurring: `12-25 Christmas`
- Supports timed events: `2024-12-31 23:59 New Year's Eve`
- Events shown in tooltip with underline on calendar

### ✅ Click Actions
- **Left click**: Reset to current month
- **Scroll up**: Next month
- **Scroll down**: Previous month
- **Command line**: `way_calendar.py next/prev/reset` (backward compatibility)

## Configuration

Edit `~/.config/waybar/calendar_config.json`:

```json
{
  "timezone": "America/Sao_Paulo",           // Your timezone
  "date_format": "%d %b, %a",                // Bar display format
  "first_weekday": 6,                        // 0=Monday, 6=Sunday
  "highlight_today": true,                   // Bold today's date
  "show_week_numbers": false,                 // Show week numbers
  "events_file": "~/.config/waybar/calendar_events.txt",
  "max_events_tooltip": 10                    // Max events to show
}
```

## Events File Format

Create `~/.config/waybar/calendar_events.txt`:

```
# Comments start with #
2024-12-25 Christmas Day                     // Specific date
2024-12-31 23:59 New Year's Eve Party        // With time
02-14 Valentine's Day                        // Yearly recurring
07-04 Independence Day                       // Yearly recurring
```

## Waybar Configuration

Add to your `waybar/config.jsonc`:

```json
{
  "custom/calendar": {
    "format": "{}",
    "tooltip": true,
    "interval": 60,
    "exec": "~/.config/waybar/way_calendar.py",
    "on-click": "~/.config/waybar/way_calendar.py 1",
    "on-scroll-up": "~/.config/waybar/way_calendar.py 4", 
    "on-scroll-down": "~/.config/waybar/way_calendar.py 5"
  }
}
```

## Dependencies

Install required Python package:
```bash
pip3 install pytz
```

## Usage

- Hover over the calendar to see the full month view with events
- Click to navigate between months
- Add your events to the events file
- Dates with events are underlined
- Today's date is bold (if enabled)
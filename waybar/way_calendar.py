#!/usr/bin/env python3
import json
import sys
import os
import re
from datetime import datetime, timedelta
import calendar as cal_lib
import pytz
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
CONFIG_FILE = os.path.join(CONFIG_DIR, "calendar_config.json")
OFFSET_FILE = "/tmp/waybar_cal_offset"
EVENTS_FILE = os.path.expanduser("~/.config/waybar/calendar_events.txt")

# Default configuration
DEFAULT_CONFIG = {
    "timezone": "America/Sao_Paulo",
    "date_format": "%d %b, %a",
    "first_weekday": 6,  # Sunday
    "highlight_today": True,
    "show_week_numbers": False,
    "events_file": "~/.config/waybar/calendar_events.txt",
    "max_events_tooltip": 10,
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


def get_offset():
    """Get current month offset"""
    if not os.path.exists(OFFSET_FILE):
        return 0
    try:
        with open(OFFSET_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0


def set_offset(val):
    """Set month offset"""
    with open(OFFSET_FILE, "w") as f:
        f.write(str(val))


def parse_event_line(line):
    """Parse a single event line"""
    # Expected formats:
    # YYYY-MM-DD Event description
    # YYYY-MM-DD HH:MM Event description
    # MM-DD Event description (recurring yearly)

    line = line.strip()
    if not line or line.startswith("#"):
        return None

    # Try to extract date and description
    parts = line.split(" ", 2)
    if len(parts) < 2:
        return None

    date_part = parts[0]
    time_part = parts[1] if len(parts) > 2 and ":" in parts[1] else None
    description = parts[2] if len(parts) > 2 else parts[1]

    try:
        if "-" in date_part and len(date_part.split("-")) == 3:
            # Full date YYYY-MM-DD
            event_date = datetime.strptime(date_part, "%Y-%m-%d").date()
            event_time = (
                datetime.strptime(time_part, "%H:%M").time() if time_part else None
            )
        elif "-" in date_part and len(date_part.split("-")) == 2:
            # Monthly recurring MM-DD
            month, day = date_part.split("-")
            today = datetime.now()
            event_date = datetime(today.year, int(month), int(day)).date()
            event_time = (
                datetime.strptime(time_part, "%H:%M").time() if time_part else None
            )
        else:
            return None

        return {"date": event_date, "time": event_time, "description": description}
    except:
        return None


def get_events_for_date(target_date, events_file):
    """Get all events for a specific date"""
    events = []

    if not os.path.exists(events_file):
        return events

    try:
        with open(events_file, "r", encoding="utf-8") as f:
            for line in f:
                event = parse_event_line(line)
                if event and event["date"] == target_date:
                    events.append(event)
    except:
        pass

    return sorted(events, key=lambda x: (x["time"] or datetime.min.time()))


def get_current_events(config):
    """Get events for current month view"""
    events_file = os.path.expanduser(config["events_file"])
    if not os.path.exists(events_file):
        return []

    offset = get_offset()
    now = datetime.now(pytz.timezone(config["timezone"]))

    # Calculate target month
    target_month = (now.month + offset - 1) % 12 + 1
    target_year = now.year + (now.month + offset - 1) // 12

    events = []
    try:
        with open(events_file, "r", encoding="utf-8") as f:
            for line in f:
                event = parse_event_line(line)
                if event:
                    # Check if event is in target month/year
                    if (
                        event["date"].month == target_month
                        and event["date"].year == target_year
                    ):
                        events.append(event)
    except:
        pass

    return events


def handle_click(button, config):
    """Handle mouse clicks"""
    if button == 1:  # Left click - reset to current month
        set_offset(0)
    elif button == 4:  # Scroll up - next month
        offset = get_offset()
        set_offset(offset + 1)
    elif button == 5:  # Scroll down - previous month
        offset = get_offset()
        set_offset(offset - 1)


def generate_calendar_html(target_date, config):
    tz = pytz.timezone(config["timezone"])
    now = datetime.now(tz)
    c = cal_lib.TextCalendar(config["first_weekday"])

    year = target_date.year
    month = target_date.month

    # formatmonth gera uma string onde cada dia ocupa 3 espaços (2 dígitos + 1 espaço)
    month_text = c.formatmonth(year, month)
    lines = month_text.split("\n")

    # Headers com 3 letras para alinhar perfeitamente (Sun, Mon...)
    weekday_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    if config["first_weekday"] == 0:
        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    events_file = os.path.expanduser(config["events_file"])
    html_parts = []

    # Título do mês
    month_name = cal_lib.month_name[month]
    html_parts.append(f"<b>◀ {month_name} {year} ▶</b>")
    html_parts.append("")

    for i, line in enumerate(lines):
        if not line.strip() or i == 0:
            continue

        if i == 1:  # Linha Sun Mon Tue...
            # f"{wd:>3}" garante 3 espaços + 1 do join = 4 por coluna
            html_parts.append(" ".join([f"{wd:>3}" for wd in weekday_names]))
        else:
            week_parts = []
            # Forçamos a linha a ter 20 caracteres (tamanho padrão do calendar.py)
            # para o slicing não quebrar no final da linha
            full_line = line.ljust(20)

            # Slicing de 3 em 3 (o grid nativo do Python)
            for j in range(0, 20, 3):
                day_str = full_line[j : j + 3].strip()

                if not day_str:
                    week_parts.append(
                        "   "
                    )  # 3 espaços para manter o lugar do dia vazio
                    continue

                try:
                    day_num = int(day_str)
                    current_date = datetime(year, month, day_num).date()
                    is_today = current_date == now.date()
                    has_events = len(get_events_for_date(current_date, events_file)) > 0

                    # Número com largura 3
                    txt = f"{day_num:>3}"

                    # Tags Pango (únicas que o Waybar aceita de fato)
                    if is_today and config["highlight_today"]:
                        txt = f"<b>{txt}</b>"
                    if has_events:
                        txt = f"<u>{txt}</u>"

                    week_parts.append(txt)
                except ValueError:
                    week_parts.append(f"{day_str:>3}")

            html_parts.append(" ".join(week_parts))

    # Seção de Eventos (limitada pelo config)
    events = get_current_events(config)
    if events:
        html_parts.append("\n<b>Events this month:</b>")
        for event in events[: config["max_events_tooltip"]]:
            time_str = f" {event['time'].strftime('%H:%M')}" if event["time"] else ""
            html_parts.append(
                f"• {event['date'].strftime('%m-%d')}{time_str}: {event['description']}"
            )

    return "\n".join(html_parts)


def main():
    import time

    start_time = time.time()

    # Initialize logging
    logger = get_logger("calendar")
    log_script_start(logger, sys.argv)

    try:
        # Load configuration
        config = load_config()
        logger.info(f"Calendar config loaded: timezone={config['timezone']}")

        # Handle arguments
        if len(sys.argv) > 1:
            arg = sys.argv[1]

            # Handle click events
            try:
                button = int(arg)
                logger.debug(f"Handling click action: button={button}")
                handle_click(button, config)
            except ValueError:
                # Handle navigation commands
                if arg == "next":
                    offset = get_offset()
                    set_offset(offset + 1)
                    logger.info("Calendar advanced to next month")
                elif arg == "prev":
                    offset = get_offset()
                    set_offset(offset - 1)
                    logger.info("Calendar moved to previous month")
                elif arg == "reset":
                    set_offset(0)
                    logger.info("Calendar reset to current month")

        # Calculate current date and timezone
        offset = get_offset()
        tz = pytz.timezone(config["timezone"])
        now = datetime.now(tz)
        target_date = now.replace(day=1) + timedelta(days=32 * offset)
        target_date = target_date.replace(day=1)

        # Format output
        bar_text = now.strftime(config["date_format"])
        calendar_html = generate_calendar_html(target_date, config)

        output = {
            "text": bar_text,
            "tooltip": f"<tt>{calendar_html}</tt>",
            "class": "calendar-widget",
        }

        print(json.dumps(output))

    except Exception as e:
        logger.error(f"Calendar script failed: {str(e)}")
        print('{"text": "Error", "tooltip": "Calendar Error"}')

    finally:
        duration = time.time() - start_time
        log_script_end(logger, duration)


if __name__ == "__main__":
    main()

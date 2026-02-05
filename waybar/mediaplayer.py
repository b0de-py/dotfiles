#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import time
import signal
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from waybar_logging import get_logger, log_script_start, log_script_end

# Initialize logging
logger = get_logger("mediaplayer")
log_script_start(logger, sys.argv)


class MediaPlayer:
    def __init__(self):
        self.config = self.load_config()
        self.players = {}
        self.active_player = None
        self.process = None
        self.running = True

        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        logger.info("MediaPlayer initialized")

    def load_config(self):
        """Load configuration from file"""
        config_dir = os.path.expanduser("~/.config/waybar")
        config_file = os.path.join(config_dir, "mediaplayer_config.json")

        # Default configuration
        default_config = {
            "display": {
                "max_length": 43,
                "show_volume": True,
                "show_player_name": False,
                "paused_prefix": "󰏤 ",
                "format": "{icon} {artist} - {title}",
            },
            "icons": {
                "spotify": " ",
                "vivaldi": " ",
                "chromium": " ",
                "firefox": " ",
                "brave": " ",
                "edge": "󰇩 ",
                "safari": "裏 ",
                "default": " ",
            },
            "volume": {
                "enabled": True,
                "show_percentage": True,
                "low_threshold": 30,
                "medium_threshold": 70,
                "icons": {"muted": "󰝟 ", "low": "󰖀 ", "medium": "󰕾 ", "high": "󰕾 "},
            },
            "click_actions": {
                "left_click": "play_pause",
                "right_click": "show_menu",
                "scroll_up": "next",
                "scroll_down": "previous",
            },
            "prioritization": {
                "prefer_playing": True,
                "priority_order": [
                    "spotify",
                    "firefox",
                    "chromium",
                    "vivaldi",
                    "brave",
                    "default",
                ],
            },
        }

        try:
            if os.path.exists(config_file):
                with open(config_file, "r") as f:
                    config = json.load(f)
                # Merge with defaults
                merged = {**default_config, **config}
                logger.info("Configuration loaded from file")
                return merged
            else:
                # Create default config file
                os.makedirs(config_dir, exist_ok=True)
                with open(config_file, "w") as f:
                    json.dump(default_config, f, indent=2)
                logger.info("Created default configuration file")
                return default_config
        except Exception as e:
            logger.error(f"Failed to load config: {str(e)}")
            return default_config

    def get_icon(self, player_name):
        """Get icon for player"""
        player_lower = player_name.lower()
        for key in self.config["icons"]:
            if key in player_lower:
                return self.config["icons"][key]
        return self.config["icons"]["default"]

    def get_volume_icon(self, volume):
        """Get volume icon based on level"""
        if volume <= 0:
            return self.config["volume"]["icons"]["muted"]
        elif volume < self.config["volume"]["low_threshold"]:
            return self.config["volume"]["icons"]["low"]
        elif volume < self.config["volume"]["medium_threshold"]:
            return self.config["volume"]["icons"]["medium"]
        else:
            return self.config["volume"]["icons"]["high"]

    def get_volume_info(self):
        """Get current volume information"""
        if not self.config["volume"]["enabled"] or not self.active_player:
            return None

        try:
            # Try to get volume using playerctl
            result = subprocess.run(
                ["playerctl", "volume"], capture_output=True, text=True, timeout=2
            )
            if result.returncode == 0:
                try:
                    volume = float(result.stdout.strip())
                    return {
                        "level": int(volume * 100),
                        "icon": self.get_volume_icon(volume * 100),
                    }
                except ValueError:
                    pass
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass

        return None

    def handle_click_action(self, action):
        """Handle click actions"""
        logger.info(f"Handling click action: {action}")

        try:
            if action == "play_pause":
                subprocess.run(["playerctl", "play-pause"], timeout=2)
            elif action == "next":
                subprocess.run(["playerctl", "next"], timeout=2)
            elif action == "previous":
                subprocess.run(["playerctl", "previous"], timeout=2)
            elif action == "show_menu":
                # You could implement a menu here
                pass
            else:
                logger.warning(f"Unknown action: {action}")
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout executing action: {action}")
        except subprocess.SubprocessError as e:
            logger.error(f"Error executing action {action}: {str(e)}")

    def find_active_player(self):
        """Find the best active player based on prioritization"""
        if not self.players:
            return None

        config = self.config["prioritization"]

        # If we prefer playing and there's a playing player, use it
        if config["prefer_playing"]:
            for p_name, data in self.players.items():
                if data["status"] == "Playing":
                    logger.debug(f"Found playing player: {p_name}")
                    return (p_name, data)

        # Otherwise, use priority order
        priority = config["priority_order"]
        for player_type in priority:
            for p_name, data in self.players.items():
                if player_type == "default" or player_type in p_name.lower():
                    if data["status"] != "Stopped":
                        logger.debug(f"Found priority player: {p_name}")
                        return (p_name, data)

        # Fallback to any non-stopped player
        for p_name, data in self.players.items():
            if data["status"] != "Stopped":
                logger.debug(f"Found fallback player: {p_name}")
                return (p_name, data)

        return None

    def format_output(self, player_name, player_data):
        """Format player data for display"""
        try:
            config = self.config["display"]
            icon = self.get_icon(player_name)

            # Build content using format string
            format_vars = {
                "icon": icon,
                "player": player_name,
                "artist": player_data.get("artist", "Unknown Artist"),
                "title": player_data.get("title", "Unknown Title"),
            }

            content = config["format"].format(**format_vars)

            # Add paused prefix if needed
            if player_data.get("status") == "Paused" and config.get("paused_prefix"):
                content = config["paused_prefix"] + content

            # Add volume if enabled
            volume_info = self.get_volume_info()
            if volume_info and config.get("show_volume"):
                volume_config = config.get("volume", {})
                if volume_config.get("show_percentage"):
                    content += (
                        f" {volume_info.get('icon', '')}{volume_info.get('level', 0)}%"
                    )
                else:
                    content += f" {volume_info.get('icon', '')}"

            # Add player name if enabled
            if config.get("show_player_name"):
                content += f" [{player_name}]"

            # Truncate if too long
            max_len = config.get("max_length", 43)
            if len(content) > max_len:
                content = content[: max_len - 3] + "..."

            return content

        except Exception as e:
            logger.error(f"Error in format_output: {str(e)}")
            raise e

    def start_playerctl_process(self):
        """Start playerctl monitoring process"""
        try:
            self.process = subprocess.Popen(
                [
                    "playerctl",
                    "-a",
                    "metadata",
                    "--format",
                    "{{status}}||{{playerName}}||{{artist}}||{{title}}",
                    "--follow",
                ],
                stdout=subprocess.PIPE,
                text=True,
            )
            logger.info("playerctl process started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start playerctl: {str(e)}")
            return False

    def process_line(self, line):
        """Process a line from playerctl output"""
        if not line:
            return

        parts = line.strip().split("||")
        if len(parts) != 4:
            logger.debug(f"Invalid line format: {line.strip()}")
            return

        status, name, artist, title = parts
        self.players[name] = {"status": status, "artist": artist, "title": title}
        logger.debug(f"Updated player state: {name} - {status}")

        # Update active player
        new_active = self.find_active_player()
        if new_active:
            self.active_player = new_active

    def generate_output(self):
        """Generate waybar output"""
        if self.active_player:
            name, data = self.active_player
            try:
                content = self.format_output(name, data)

                # Safely build tooltip
                status = data.get("status", "Unknown")
                artist = data.get("artist", "Unknown Artist")
                title = data.get("title", "Unknown Title")

                output = {
                    "text": content,
                    "class": status.lower(),
                    "tooltip": f"{name}: {status}\n{artist} - {title}",
                }
                logger.debug(f"Generated output: {content}")
                return json.dumps(output)
            except Exception as e:
                logger.error(f"Error formatting output: {str(e)}")
                return json.dumps({"text": "Error", "class": "error"})
        else:
            logger.debug("No active player")
            return json.dumps({"text": "", "class": "empty"})

    def main_loop(self):
        """Main monitoring loop"""
        logger.info("Starting main loop")

        while self.running:
            try:
                # Start playerctl if not running
                if not self.process:
                    if not self.start_playerctl_process():
                        time.sleep(5)  # Wait before retry
                        continue

                # Read line from process
                if self.process and self.process.stdout:
                    line = self.process.stdout.readline()
                    if not line:
                        # Process ended
                        logger.warning("playerctl process ended")
                        if self.process.poll() is not None:
                            self.process = None
                        continue

                    # Process the line
                    self.process_line(line)

                    # Generate and output
                    print(self.generate_output())
                    sys.stdout.flush()
                else:
                    # No process, wait and retry
                    time.sleep(1)

            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(1)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def run(self):
        """Run the media player"""
        try:
            # Handle command line arguments for actions
            if len(sys.argv) > 1 and sys.argv[1] in ["play_pause", "next", "previous"]:
                action = sys.argv[1]
                self.handle_click_action(action)
                return

            self.main_loop()
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
        except Exception as e:
            logger.error(f"MediaPlayer failed: {str(e)}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                try:
                    self.process.kill()
                except:
                    pass
        log_script_end(logger)


# Main entry point
if __name__ == "__main__":
    player = MediaPlayer()
    player.run()

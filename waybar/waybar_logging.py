#!/usr/bin/env python3
"""
Unified logging system for Waybar scripts
Provides consistent logging across all waybar modules
"""

import os
import sys
import time
from datetime import datetime
import json


class WaybarLogger:
    """Unified logger for waybar scripts"""

    def __init__(self, script_name, log_level="INFO"):
        self.script_name = script_name
        self.log_level = log_level.upper()
        self.log_file = os.path.expanduser("~/.config/waybar/waybar.log")
        self.debug_file = os.path.expanduser(
            f"~/.config/waybar/{script_name}.debug.log"
        )

        # Create log directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Log levels
        self.levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}

    def _should_log(self, level):
        """Check if we should log this level"""
        return self.levels.get(level, 1) >= self.levels.get(self.log_level, 1)

    def _format_message(self, level, message):
        """Format log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{level}] [{self.script_name}] {message}"

    def _write_log(self, level, message, to_debug_file=False):
        """Write message to log file"""
        if not self._should_log(level):
            return

        formatted_msg = self._format_message(level, message)

        # Write to main log file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(formatted_msg + "\n")
        except:
            pass  # Silent fail for logging errors

        # Write to debug-specific file if requested
        if to_debug_file:
            try:
                with open(self.debug_file, "a", encoding="utf-8") as f:
                    f.write(formatted_msg + "\n")
            except:
                pass

    def debug(self, message, to_debug_file=True):
        """Debug level logging"""
        self._write_log("DEBUG", message, to_debug_file=True)

    def info(self, message):
        """Info level logging"""
        self._write_log("INFO", message)

    def warning(self, message):
        """Warning level logging"""
        self._write_log("WARNING", message)

    def error(self, message):
        """Error level logging"""
        self._write_log("ERROR", message)

    def critical(self, message):
        """Critical level logging"""
        self._write_log("CRITICAL", message)

    def log_function_call(self, func_name, args=None, kwargs=None):
        """Log function calls for debugging"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        msg = f"CALL {func_name}("
        if args:
            msg += f"args={args}"
        if kwargs:
            if args:
                msg += ", "
            msg += f"kwargs={kwargs}"
        msg += ")"

        self.debug(msg, to_debug_file=True)

    def log_performance(self, operation, duration):
        """Log performance metrics"""
        self.info(f"PERF {operation}: {duration:.3f}s")

    def log_api_call(self, url, status_code=None, response_time=None):
        """Log API calls"""
        msg = f"API_CALL {url}"
        if status_code:
            msg += f" status={status_code}"
        if response_time:
            msg += f" time={response_time:.3f}s"
        self.info(msg)

    def log_config_change(self, key, old_value, new_value):
        """Log configuration changes"""
        self.info(f"CONFIG_CHANGE {key}: {old_value} -> {new_value}")

    def log_cache_operation(self, operation, cache_file, hit=False):
        """Log cache operations"""
        status = "HIT" if hit else "MISS"
        self.debug(f"CACHE_{operation}_{status} {cache_file}")

    def cleanup_old_logs(self, days=7):
        """Clean up old log files"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)

            # Clean main log
            if os.path.exists(self.log_file):
                if os.path.getmtime(self.log_file) < cutoff_time:
                    os.remove(self.log_file)

            # Clean debug log
            if os.path.exists(self.debug_file):
                if os.path.getmtime(self.debug_file) < cutoff_time:
                    os.remove(self.debug_file)

        except:
            pass


def safe_execute(logger, func, default_value=None, error_message="Operation failed"):
    """
    Safely execute a function with error handling and logging

    Args:
        logger: WaybarLogger instance
        func: Function to execute
        default_value: Value to return on error
        error_message: Error message to log

    Returns:
        Function result or default_value on error
    """
    try:
        return func()
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        logger.debug(
            f"Full error details: {type(e).__name__}: {str(e)}", to_debug_file=True
        )
        return default_value


def log_script_start(logger, args=None):
    """Log script startup"""
    logger.info(f"Script started with args: {args}")
    logger.debug(f"Python version: {sys.version}")
    logger.debug(f"Working directory: {os.getcwd()}")


def log_script_end(logger, duration=None):
    """Log script completion"""
    if duration:
        logger.info(f"Script completed in {duration:.3f}s")
    else:
        logger.info("Script completed")


class PerformanceTimer:
    """Context manager for timing operations"""

    def __init__(self, logger, operation_name):
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.logger.log_performance(self.operation_name, duration)


# Default logger for backward compatibility
def get_logger(script_name, log_level="INFO"):
    """Get logger instance for a script"""

    # Try to get log level from environment or config
    env_level = os.environ.get("WAYBAR_LOG_LEVEL")
    if env_level:
        log_level = env_level

    # Try to get from global config if available
    config_file = os.path.expanduser("~/.config/waybar/logging_config.json")
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                log_level = config.get("log_level", log_level)
        except:
            pass

    return WaybarLogger(script_name, log_level)


# Configuration creator
def create_default_logging_config():
    """Create default logging configuration"""
    config_dir = os.path.expanduser("~/.config/waybar")
    config_file = os.path.join(config_dir, "logging_config.json")

    if not os.path.exists(config_file):
        default_config = {
            "log_level": "INFO",
            "cleanup_days": 7,
            "enable_debug_files": True,
            "max_log_size_mb": 10,
        }

        try:
            os.makedirs(config_dir, exist_ok=True)
            with open(config_file, "w") as f:
                json.dump(default_config, f, indent=2)
        except:
            pass

    return config_file

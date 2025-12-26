import logging
import sys
from logging.handlers import RotatingFileHandler


# ANSI escape codes for colored output in the terminal
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def __init__(self, fmt, datefmt=None):
        super().__init__(fmt, datefmt)

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        # Apply color to the level name part of the message
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logger(name="app", log_file=None, level=logging.INFO):
    """
    Sets up a logger with:
    1. Console output (Colored)
    2. File output (Rotation enabled - 5MB limit, keeps 3 backups)
    """

    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate logs if function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define the output format
    # Example: 2023-10-27 10:00:00 | INFO | Your message here
    log_fmt = "%(asctime)s | %(name)s |%(levelname)-8s | %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    # --- 1. Console Handler (Stdout) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(log_fmt, date_fmt))
    logger.addHandler(console_handler)

    # --- 2. File Handler (Optional) ---
    if log_file:
        # RotatingFileHandler: New file after 5MB, keeps last 3 files
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        # Use standard formatter for files (no ANSI colors)
        file_handler.setFormatter(logging.Formatter(log_fmt, date_fmt))
        logger.addHandler(file_handler)

    return logger

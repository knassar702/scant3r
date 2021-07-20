#!/usr/bin/env python3

import logging
from .colors import Colors

class CustomFormatter(logging.Formatter):
    colors = Colors()
    magenta = colors.magenta
    reset = colors.rest
    grey = colors.grey
    bold_red = colors.bred
    red = colors.red
    green = colors.green
    yellow = colors.yellow
    """Logging Formatter to add colors and count warning / errors"""
    debug_format = "%(asctime)s - %(module)s - %(levelname)s - %(message)s (%(filename)s:%(funcName)s:%(lineno)d)"
    normal_format = f"[{green}%(levelname)s{reset}][{colors.bwhite}%(asctime)s{reset}] {colors.byellow}%(module)s{reset} -> %(message)s"
    FORMATS = {
        logging.DEBUG: magenta + debug_format + reset,
        logging.INFO: grey + normal_format + reset,
        logging.WARNING: yellow + normal_format + reset,
        logging.ERROR: red + normal_format + reset,
        logging.CRITICAL: bold_red + normal_format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

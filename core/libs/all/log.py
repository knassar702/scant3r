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
    yellow = colors.yellow
    """Logging Formatter to add colors and count warning / errors"""
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {
        logging.DEBUG: magenta + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

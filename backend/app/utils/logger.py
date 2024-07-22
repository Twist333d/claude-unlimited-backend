import logging
import os
from logging.handlers import RotatingFileHandler
import colorlog

def setup_logger(name='backend', log_file='app.log', level=logging.DEBUG):
    # Create logs directory if it doesn't exist
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create logger
    logger = colorlog.getLogger(name)
    logger.setLevel(level)

    # Create console handler with color
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)

    # Create file handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, log_file),
        maxBytes=1024*1024,
        backupCount=5
    )
    file_handler.setLevel(level)

    # Create color formatter
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s[%(name)s]%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # Create standard formatter for file handler
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set formatters for handlers
    console_handler.setFormatter(color_formatter)
    file_handler.setFormatter(file_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create a global logger instance
logger = setup_logger()

def log_with_prefix(level, prefix, message):
    getattr(logger, level.lower())(f"[{prefix}] {message}")
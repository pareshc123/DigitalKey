import os
import sys
import logging
from datetime import datetime


LOG_FORMAT = "[%(asctime)s.%(msecs)3d] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # create Logs directory if not exists
    os.makedirs("logs", exist_ok=True)

    # file name with timestamp
    file_name = datetime.now().strftime("logs/run_%Y-%m-%d_%H-%M-%S.log")

    # Handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(file_name, encoding="utf-8")

    # Format
    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

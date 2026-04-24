import sys
import logging
from pathlib import Path
from datetime import datetime


def _find_project_root(start_path: Path) -> Path:
    for parent in [start_path] + list(start_path.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root not found")


BASE_DIR = _find_project_root(Path(__file__).resolve())
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"


class MicrosecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


LOG_FORMAT = "[%(asctime)s] [%(levelname)s]%(level_pad)s[%(shortname)s]%(name_pad)s%(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",       # Cyan
        "INFO": "\033[32m",        # Green
        "WARNING": "\033[33m",     # Yellow
        "ERROR": "\033[31m",       # Red
        "CRITICAL": "\033[31;1m",  # Bold Red
    }
    RESET = "\033[0m"

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    def format(self, record):
        # Save original levelname
        original_levelname = record.levelname

        # Apply color ONLY to levelname
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        # Format the message
        message = super().format(record)

        # Restore original levelname (VERY IMPORTANT)
        record.levelname = original_levelname

        return message


def setup_logger(log_level: str = "INFO") -> None:
    """
    Initialize logging configuration once in main
    e.g.:

    from digitalkey.reporting.logger import setup_logger
    setup_logger("DEBUG")
    """

    # create Logs directory if not exists
    LOG_DIR.mkdir(exist_ok=True)

    # file name with timestamp
    log_file = LOG_DIR / datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S.log")

    # create root logger
    level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Avoid duplicate handlers
    if root_logger.handlers:
        root_logger.handlers.clear()

    # prevents duplicates in case our modules uses its own handler or external libs configure logging
    root_logger.propagate = False

    # Format
    formatter = MicrosecondFormatter(
        LOG_FORMAT,
        DATE_FORMAT
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter(LOG_FORMAT, DATE_FORMAT))

    # File Handle
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    import logger in all other files:

    from digitalkey.reporting.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Validation started")
    """

    logger = logging.getLogger(name)

    shortname = name.split(".")[-1]

    def add_extra(record: logging.LogRecord) -> bool:

        record.shortname = shortname

        # align level column
        record.level_pad = " " * max(1, 8 - len(record.levelname))

        # align module/name column
        record.name_pad = " " * max(1, 18 - len(record.shortname))

        return True

    logger.addFilter(add_extra)

    return logger

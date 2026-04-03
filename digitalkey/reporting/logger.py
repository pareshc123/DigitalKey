import sys
import logging
from pathlib import Path
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def _find_project_root(start_path: Path) -> Path:
    for parent in [start_path] + list(start_path.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise RuntimeError("Project root not found")


BASE_DIR = _find_project_root(Path(__file__).resolve())
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"

LOG_FORMAT = "[%(asctime)s.%(msecs)3d] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _setup_logger(log_level: str = "INFO") -> None:

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
        return

    # Format
    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File Handler with rotation (daily)
    file_handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=7,  # keep last 7 days
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


# if __name__ == "__main__":
#
#     lg = get_logger(__name__)

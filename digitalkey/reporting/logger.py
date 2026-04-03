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

LOG_FORMAT = "[%(asctime)s.%(msecs)3d] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:

    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # create Logs directory if not exists
    LOG_DIR.mkdir(exist_ok=True)

    # file name with timestamp
    file_name = LOG_DIR / datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S.log")

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


if __name__ == "__main__":

    lg = get_logger(__name__)

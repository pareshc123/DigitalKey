import re
from typing import List
from pathlib import Path
from datetime import datetime

from .event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class LogParser:
    LOG_PATTERN = re.compile(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+\[(\w+)\]\s+\[(\w+)\]\s+(.*)"
    )

    META_PATTERN = re.compile(
        r"\((.*?)\)"
    )

    COMP_PATTERN = re.compile(
        r"(\w+)\s*([<>])\s*(.+)"
    )

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self._events = None
        logger.debug(f"LogParser initialized with file: {self.filepath}")

    def read_logs(self) -> List[str]:
        try:
            logger.info(f"reading log file: {self.filepath}")

            with self.filepath.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    yield line

        except FileNotFoundError:
            logger.exception(f"Log file not found: {self.filepath}")
            return []

        except Exception:          # noqa
            logger.exception(f"Failed to read log file: {self.filepath}")
            return []

    # Extract MetaData from Message
    def extract_metadata(self, message: str) -> dict:
        metadata = {}

        matches = self.META_PATTERN.findall(message)

        for content in matches:
            parts = [part.strip() for part in content.split(",")]

            for part in parts:

                if "=" in part:
                    key, value = part.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key in metadata:
                        if not isinstance(metadata[key], list):
                            metadata[key] = [metadata[key]]
                        metadata[key].append(value)
                    else:
                        metadata[key] = value

                elif "<" in part or ">" in part:
                    comp_match = self.COMP_PATTERN.match(part)
                    if comp_match:
                        key = comp_match.group(1)
                        op = comp_match.group(2)
                        value = comp_match.group(3)

                        metadata[key] = {
                            "operator": op,
                            "value": value
                        }

                else:
                    metadata[part] = True

        return metadata

    # Parse single line safely
    def parse_line(self, line: str) -> Event | None:

        match = self.LOG_PATTERN.search(line)

        if not line.strip() or line.strip().startswith("#"):
            return None

        if not match:
            logger.warning(f"Malformed log line skipped: {line.strip()}")
            return None  # malformed line

        try:
            timestamp = datetime.strptime(
                match.group(1), "%Y-%m-%d %H:%M:%S.%f"
            )
            level = match.group(2)
            module = match.group(3)
            message = match.group(4).strip()

            metadata = self.extract_metadata(message)

            return Event(
                timestamp=timestamp,
                level=level,
                module=module,
                message=message,
                attributes=metadata,
            )
        except Exception:  # noqa
            logger.exception(f"Failed to parse line: {line.strip()}")
            return None

    # Parse all ECU_Traces
    def extract_events(self):
        if self._events is not None:
            logger.debug("Returning cached parsed events")
            return self._events

        logger.info("Extracting events from log file")

        events = []
        for line in self.read_logs():
            event = self.parse_line(line)
            if event:
                events.append(event)

        self._events = events
        logger.info(f"Extracted {len(events)} valid events")
        return events

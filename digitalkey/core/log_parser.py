import re
from typing import List
from datetime import datetime

from .event_model import Event


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

    def __init__(self, filepath: str):
        self.filepath = filepath
        self._events = None

    def read_logs(self) -> List[str]:
        with open(self.filepath) as f:
            return f.readlines()

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

        if not match:
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
        except Exception as e:
            print(f"Failed to parse line: {line.strip()} | Error: {e}")
            return None

    # Parse all Traces
    def extract_events(self):
        if self._events is not None:
            return self._events

        events = []
        for line in self.read_logs():
            event = self.parse_line(line)
            if event:
                events.append(event)

        self._events = events
        return events

    # Filters
    def filter_by_error(self) -> List[Event]:
        return [err for err in self.extract_events() if err.level == "ERROR"]

    def filter_by_module(self, module_name: str) -> List[Event]:
        return [mod for mod in self.extract_events() if mod.module == module_name]

    def filter_by_time(self, start: datetime, end: datetime) -> List[Event]:
        return [t for t in self.extract_events() if start <= t.timestamp <= end]

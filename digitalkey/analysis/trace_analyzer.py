from datetime import datetime
from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class Analyzer:

    def __init__(self, events: List[Event]) -> None:
        self.events = events
        logger.debug(f"TraceAnalyzer initialized with {len(events)} events")

    # Filters
    def filter_by_error(self) -> List[Event]:
        errors = [err for err in self.events if err.level == "ERROR"]
        logger.debug(f"Found {len(errors)} ERROR events")
        return errors

    def filter_by_module(self, module_name: str) -> List[Event]:
        events = [mod for mod in self.events if mod.module == module_name]
        logger.debug(f"Found {len(events)} events for module: {module_name}")
        return events

    def filter_by_time(self, start: datetime, end: datetime) -> List[Event]:
        events = [t for t in self.events if start <= t.timestamp <= end]
        logger.debug(f"Found {len(events)} events between {start} and {end}")
        return events

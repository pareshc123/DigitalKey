from datetime import datetime
from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class TraceAnalyzer:

    def __init__(self, events: List[Event]) -> None:
        self.events = events
        logger.debug(f"TraceAnalyzer initialized with {len(events)} events")

    def filter_by_error(self) -> List[Event]:
        errors = [err for err in self.events if err.level == "ERROR"]
        logger.debug(f"Found {len(errors)} ERROR events")
        return errors

    def filter_by_module(self, module_name: str) -> List[Event]:
        module_name = module_name.upper()
        mod_events = [event for event in self.events if event.module.upper() == module_name]
        logger.debug(f"Found {len(mod_events)} events for module: {module_name}")
        return mod_events

    def filter_by_time(self, start: datetime, end: datetime) -> List[Event]:
        time_events = [event for event in self.events if start <= event.timestamp <= end]
        logger.debug(f"Found {len(time_events)} events between {start} and {end}")
        return time_events

    def find_by_keyword(self, keyword: str) -> List[Event]:
        keyword_lower = keyword.lower()
        events = [event for event in self.events if keyword_lower in event.message.lower()]
        logger.debug(f"Found {len(events)} events matching keyword: {keyword}")
        return events

    def get_events_between(self, start_keyword: str, end_keyword: str) -> List[Event]:

        start_index = None
        end_index = None

        start_lower = start_keyword.lower()
        end_lower = end_keyword.lower()

        for index, event in enumerate(self.events):
            message = event.message.lower()

            if start_index is None and start_lower in message:
                start_index = index

            if start_index is not None and end_lower in message:
                end_index = index
                break

        if start_index is None:
            logger.debug(f"Start keyword not found: {start_keyword}")
            return []

        if end_index is None:
            logger.debug(f"End keyword not found after start: {end_keyword}")
            return []

        events = self.events[start_index:end_index + 1]

        logger.debug(f"Found {len(events)} events between {start_keyword}' and '{end_keyword}'")

        return events

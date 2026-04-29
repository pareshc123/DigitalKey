from typing import List
from datetime import datetime

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class MetricsCalculator:

    def __init__(self, events: List[Event]):
        self.events = events
        logger.debug(f"MetricsCalculator initialized with {len(events)} events")

    def find_event_time(self, keyword: str) -> datetime | None:
        keyword_lower = keyword.lower()

        for event in self.events:
            if keyword_lower in event.message.lower():
                logger.debug(f"Found event for keyword '{keyword}': {event.timestamp}")
                return event.timestamp

        logger.debug(f"No event found for keyword: {keyword}")
        return None

    @staticmethod
    def compute_delta_ms(t1: datetime, t2: datetime) -> float:
        return (t2 - t1).total_seconds() * 1000

    def calculate_latency(self, start_keyword: str, end_keyword: str) -> float | None:
        pass

from typing import List

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class MetricsCalculator:

    def __init__(self, events: List[Event]):
        self.events = events
        logger.debug(f"MetricsCalculator initialized with {len(events)} events")
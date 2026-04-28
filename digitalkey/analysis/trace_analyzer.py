from typing import Any, List

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class Analyzer:

    def __init__(self, events: Event) -> None:
        self.events = events

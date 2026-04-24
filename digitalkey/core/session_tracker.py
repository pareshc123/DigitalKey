from typing import List, Dict
from collections import defaultdict

from .event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class SessionTracker:

    def __init__(self, events: List[Event]):
        self.events = events
        logger.debug(f"SessionTracker initialized with {len(events)} events")

        self.sessions = self.group_by_session()
        logger.info(f"Grouped events into {len(self.sessions)} sessions")

    def group_by_session(self) -> Dict[str, List[Event]]:
        sessions = defaultdict(list)

        logger.info("Grouping events by session_id")

        for event in self.events:
            if not event.has("session_id"):
                session_id = "NO_SESSION"
                logger.debug(f"Event without session_id assigned to NO_SESSION: {event.message}")
            else:
                session_id = event.get("session_id")

            sessions[session_id].append(event)

        return dict(sessions)

    def get_session_summary(self) -> Dict[str, dict]:
        logger.info("Generating session summary")
        summary = {}

        for s_id, s_events in self.sessions.items():

            if not s_events:
                logger.warning(f"Session {s_id} has no events")
                continue

            has_error = any(event.level == "ERROR" for event in s_events)
            start_time = min(event.timestamp for event in s_events)
            end_time = max(event.timestamp for event in s_events)
            duration_ms = (end_time - start_time).total_seconds() * 1000

            summary[s_id] = {
                "event_count": len(s_events),
                "has_error": has_error,
                "modules": list({event.module for event in s_events}),
                "start_time": start_time,
                "end_time": end_time,
                "duration_sec": duration_ms,
                "status": "FAILED" if has_error else "SUCCESS"
            }

            logger.debug(
                f"Session {s_id}: "
                f"{len(s_events)} events, "
                f"duration={duration_ms} ms, "
                f"status={summary[s_id]['status']}"
            )

            logger.info(f"Generated summaries for {len(summary)} sessions")

        return summary

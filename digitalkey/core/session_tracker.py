from typing import List, Dict
from collections import defaultdict

from .event_model import Event


class SessionTracker:

    def __init__(self, events: List[Event]):
        self.events = events
        self.sessions = self.group_by_session()

    def group_by_session(self) -> Dict[str, List[Event]]:
        sessions = defaultdict(list)

        for event in self.events:
            if not event.has("session_id"):
                session_id = "NO_SESSION"
            else:
                session_id = event.get("session_id")

            sessions[session_id].append(event)

        return dict(sessions)

    def get_session_summary(self) -> Dict[str, dict]:

        summary = {}
        for s_id, s_events in self.sessions.items():

            has_error = any(event.level == "ERROR" for event in s_events)
            start_time = min(event.timestamp for event in s_events)
            end_time = max(event.timestamp for event in s_events)

            summary[s_id] = {
                "event_count": len(s_events),
                "has_error": has_error,
                "modules": list({event.module for event in s_events}),
                "start_time": start_time,
                "end_time": end_time,
                "duration_sec": (end_time - start_time).total_seconds() * 1000,
                "status": "FAILED" if has_error else "SUCCESS"
            }
        return summary

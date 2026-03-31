from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from .utlities_validator import STATE, STATE_TRANSITION_MAP


class StateMachine:

    def __init__(self, events: List[Event]):
        self.events = events
        self.current_state = STATE.IDLE
        self.visited_states = [self.current_state]  # to track all the visited states

    # Public API
    def validate_state(self) -> Dict[str, Any]:

        for event in self.events:
            next_state = self._map_event_to_state(event)

            if not next_state:
                continue

            if not self.is_valid_transition(self.current_state, next_state):
                return self._fail(
                    f"Invalid transition: {self.current_state.name} → {next_state.name}",
                    event.message
                )

            # Valid transition
            self.current_state = next_state
            self.visited_states.append(next_state)

        return self._pass()

    # Event to State Mapping
    @staticmethod
    def _map_event_to_state(event: Event) -> STATE | None:
        msg = event.message

        if "Digital Key device detected" in msg:
            return STATE.DETECTED

        if "Session initiated" in msg:
            return STATE.AUTHENTICATING

        if "Authentication successful" in msg:
            return STATE.AUTHENTICATED

        if "Ranging session started" in msg:
            return STATE.RANGING

        if "Proximity validated" in msg:
            return STATE.PROXIMITY_CONFIRMED

        if "Door unlock command issued" in msg:
            return STATE.ACCESS_REQUESTED

        if "Door unlock confirmed" in msg:
            return STATE.ACCESS_GRANTED

        if "Session terminated" in msg:
            return STATE.TERMINATED

        return None

    # Transition Validation
    @staticmethod
    def is_valid_transition(current: STATE, next_state: STATE) -> bool:
        allowed = STATE_TRANSITION_MAP.get(current, [])
        return next_state in allowed or next_state == STATE.TERMINATED

    # Helper Functions
    def _pass(self) -> Dict[str, Any]:
        return {
            "name": "state_machine",
            "status": "PASS",
            "details": "All transitions valid",
            "metrics": {
                "final_state": self.current_state.name,
                "states_visited": [s.name for s in self.visited_states]
            }
        }

    def _fail(self, reason: str, event: str) -> Dict[str, Any]:
        return {
            "name": "state_machine",
            "status": "FAIL",
            "details": reason,
            "metrics": {
                "failed_event": event,
                "current_state": self.current_state.name,
                "states_visited": [s.name for s in self.visited_states]
            }
        }

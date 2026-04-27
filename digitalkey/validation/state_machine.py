from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger
from .utilities_validator import STATE, STATE_TRANSITION_MAP, STEP_TO_STATE, match_step

logger = get_logger(__name__)


class StateMachine:

    def __init__(self, events: List[Event]):
        self.events = events
        self.current_state = STATE.IDLE
        self.visited_states = [self.current_state]  # to track all the visited states

        logger.debug(f"StateMachine initialized with {len(events)} events")
        logger.debug(f"Initial state: {self.current_state.name}")

    # Public API
    def validate_state(self) -> Dict[str, Any]:
        logger.info("Running state machine validation")

        for event in self.events:
            next_state = self._map_event_to_state(event)

            if not next_state:
                continue

            logger.debug(f"Event mapped to state: {event.message} -> {next_state.name}")

            if not self.is_valid_transition(self.current_state, next_state):
                reason = (
                    f"Invalid transition: "
                    f"{self.current_state.name} -> {next_state.name}"
                )
                logger.warning(reason)
                return self._fail(reason, event.message)

            logger.debug(f"Valid transition: {self.current_state.name} -> {next_state.name}")

            # Valid transition
            self.current_state = next_state
            self.visited_states.append(next_state)

        logger.info("State machine validation passed")

        return self._pass()

    # Event to State Mapping
    @staticmethod
    def _map_event_to_state(event: Event) -> STATE | None:
        step = match_step(event.message)

        if step is None:
            return None

        return STEP_TO_STATE.get(step)

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
                "states_visited": [s.name for s in self.visited_states],
            },
        }

    def _fail(self, reason: str, event: str) -> Dict[str, Any]:
        return {
            "name": "state_machine",
            "status": "FAIL",
            "details": reason,
            "metrics": {
                "failed_event": event,
                "current_state": self.current_state.name,
                "states_visited": [s.name for s in self.visited_states],
            },
        }

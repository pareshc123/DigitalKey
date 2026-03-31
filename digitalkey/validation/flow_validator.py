from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from .utlities_validator import Steps, STEP_MAPPING


class FlowValidator:

    def __init__(self, events: List[Event]):

        self.events = events

    @classmethod
    def _required_steps(cls) -> List[Steps]:
        return [
            Steps.DEVICE_DETECTED,
            Steps.AUTH_STARTED,
            Steps.AUTH_SUCCESS,
            Steps.RANGING_STARTED,
            Steps.PROXIMITY_VALIDATED,
            Steps.UNLOCK_REQUESTED,
            Steps.UNLOCK_CONFIRMED,
            Steps.SESSION_TERMINATED,
        ]

    # Public API
    def validate_full_flow(self) -> Dict[str, Any]:

        event_steps = self._extract_steps()

        # 1. Dependency validation (most meaningful errors)
        dependency_error = self._check_dependencies(event_steps)
        if dependency_error:
            return self._fail(dependency_error)

        # 2. Order validation
        if not self._check_order(event_steps):
            return self._fail("Invalid step order detected")

        # 3. Missing steps
        missing_steps_error = self._check_missing_steps(event_steps)
        if missing_steps_error:
            return self._fail(missing_steps_error)

        # Return success result
        return {
            "name": "full_flow",
            "status": "PASS",
            "details": "Valid full unlock sequence",
            "metrics": {
                "total_steps": len(event_steps),
                "steps": event_steps
            }
        }

    # Step Extraction
    def _extract_steps(self) -> List[Steps]:
        steps = []

        for event in self.events:
            step = self._map_event_to_steps(event)
            if step:
                steps.append(step)

        return steps

    @staticmethod
    def _map_event_to_steps(event: Event) -> Steps | None:

        for key, step in STEP_MAPPING.items():
            if key in event.message:
                return step

        return None

    # Missing Step Validation
    def _check_missing_steps(self, steps: List[Steps]) -> str | None:

        required_steps = self._required_steps()

        missing = [step for step in required_steps if step not in steps]
        if missing:
            return f"Missing Step: {missing}"

        return None

    # Order Validation
    def _check_order(self, steps: List[Steps]) -> bool:

        expected_order = self._required_steps()

        indices = {}
        for step in expected_order:
            if step in steps:
                indices[step] = steps.index(step)

            # Ensure increasing order
        last_index = -1
        for step in expected_order:
            if step in indices:
                if indices[step] < last_index:
                    return False
                last_index = indices[step]

        return True

    @staticmethod
    # Dependency Validation
    def _check_dependencies(steps: List[Steps]) -> str | None:

        def exists(step):
            return step in steps

        # AUTH requires detection
        if exists(Steps.AUTH_STARTED) and not exists(Steps.DEVICE_DETECTED):
            return "AUTH started without device detection"

        # AUTH success requires AUTH start
        if exists(Steps.AUTH_SUCCESS) and not exists(Steps.AUTH_STARTED):
            return "AUTH success without AUTH start"

        # Ranging requires auth success
        if exists(Steps.RANGING_STARTED) and not exists(Steps.AUTH_SUCCESS):
            return "Ranging started without authentication"

        # Proximity requires ranging
        if exists(Steps.PROXIMITY_VALIDATED) and not exists(Steps.RANGING_STARTED):
            return "Proximity validated without ranging"

        # Unlock requires proximity
        if exists(Steps.UNLOCK_REQUESTED) and not exists(Steps.PROXIMITY_VALIDATED):
            return "Unlock requested without proximity validation"

        # Unlock confirmation requires Unlock request
        if exists(Steps.UNLOCK_CONFIRMED) and not exists(Steps.UNLOCK_REQUESTED):
            return "Unlock confirmed without unlock request"

        return None

    # Helper function
    @staticmethod
    def _fail(message: str) -> Dict[str, Any]:
        return {
            "name": "full_flow",
            "status": "FAIL",
            "details": message,
            "metrics": {}
        }

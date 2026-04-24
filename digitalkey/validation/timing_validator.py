from datetime import datetime
from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class TimingValidator:

    def __init__(self, events: List[Event], threshold: Dict[str, Any]):

        self.events = events
        self.threshold = threshold

        self.timing = threshold.get("timing", {})
        self.uwb = threshold.get("uwb", {})
        self.system = threshold.get("system", {})
        self.security = threshold.get("security", {})

        logger.debug(f"TimingValidator initialized with {len(events)} events")

    # public API
    def validate_auth_timing(self) -> Dict[str, Any]:
        logger.info("Validating AUTH timing")

        t_req = self._find_event_time("AUTH_REQUEST")
        r_res = self._find_event_time("AUTH_RESPONSE")

        if not t_req or not r_res:
            return self._fail("auth_timing", "Missing AUTH_REQUEST or AUTH_RESPONSE")

        latency = self._compute_delta_ms(t_req, r_res)
        threshold = self.timing["auth_response_ms"]

        if latency <= threshold:
            return self._pass("auth_timing",
                              "Auth response withing threshold",
                              {"auth_latency_ms": latency})

        return self._fail(
            "auth_timing",
            f"AUTH response too slow ({latency} ms > {threshold} ms)",
            {"auth_latency_ms": latency, "threshold_ms": threshold}
        )

    def validate_detection_to_auth(self) -> Dict[str, Any]:
        logger.info("Validating detection to AUTH timing")

        t_detect = self._find_event_time("Digital Key device detected")
        r_auth = self._find_event_time("Session initiated")

        if not t_detect or not r_auth:
            return self._fail("detection_to_auth", "Missing detection or auth start")

        latency = self._compute_delta_ms(t_detect, r_auth)
        threshold = self.timing["detection_to_auth_ms"]

        if latency <= threshold:
            return self._pass("detection_to_auth",
                              "Detection to AUTH within threshold",
                              {"detection_to_auth_ms": latency})

        return self._fail(
            "detection_to_auth",
            f"AUTH start response too slow ({latency} ms > {threshold} ms)",
            {"detection_to_auth_ms": latency, "threshold_ms": threshold}
        )

    def validate_unlock_timing(self):
        logger.info("Validating proximity to unlock timing")

        t_prox = self._find_event_time("Proximity validated")
        t_unlock = self._find_event_time("Door unlock command issued")

        if not t_prox or not t_unlock:
            return self._fail("unlock_timing", "Missing proximity or unlock event")

        latency = self._compute_delta_ms(t_prox, t_unlock)
        threshold = self.timing["proximity_to_unlock_ms"]

        if latency <= threshold:
            return self._pass(
                "unlock_timing",
                "Proximity to unlock within threshold",
                {"proximity_to_unlock_ms": latency}
            )

        return self._fail(
            "unlock_timing",
            f"Unlock too slow ({latency} ms > {threshold} ms)",
            {"proximity_to_unlock_ms": latency, "threshold_ms": threshold}
        )

    def validate_unlock_confirmation(self):
        logger.info("Validating unlock confirmation timing")

        t_req = self._find_event_time("Door unlock command issued")
        t_conf = self._find_event_time("Door unlock confirmed")

        if not t_req or not t_conf:
            return self._fail("unlock_confirmation", "Missing unlock request or confirmation")

        latency = self._compute_delta_ms(t_req, t_conf)
        threshold = self.timing["unlock_confirmation_ms"]

        if latency <= threshold:
            return self._pass(
                "unlock_confirmation",
                "Unlock confirmation within threshold",
                {"unlock_confirmation_ms": latency}
            )

        return self._fail(
            "unlock_confirmation",
            f"Confirmation too slow ({latency} ms > {threshold} ms)",
            {"unlock_confirmation_ms": latency, "threshold_ms": threshold}
        )

    def validate_session_duration(self):
        logger.info("Validating session duration")

        t_start = self._find_event_time("Session initiated")
        t_end = self._find_event_time("Session terminated successfully")

        if not t_start or not t_end:
            return self._fail("session_duration", "Missing start or end of session")

        latency = self._compute_delta_ms(t_start, t_end)
        threshold = self.system["session_timeout_ms"]

        if latency <= threshold:
            return self._pass(
                "session_duration",
                "session within threshold",
                {"session_duration_ms": latency}
            )

        return self._fail(
            "session_duration",
            f"Session too slow ({latency} ms > {threshold} ms)",
            {"session_duration_ms": latency, "threshold_ms": threshold}
        )

    # Helper Functions
    def _find_event_time(self, keyword: str) -> datetime | None:

        for event in self.events:
            if keyword in event.message:
                logger.debug(f"Found event for keyword '{keyword}': {event.timestamp}")
                return event.timestamp

        logger.debug(f"No event found for keyword: {keyword}")
        return None

    @staticmethod
    def _compute_delta_ms(t1: datetime, t2: datetime) -> float:
        return (t2 - t1).total_seconds() * 1000

    @staticmethod
    def _fail(name: str, details: str, metrics: Dict[str, Any] = None) -> Dict[str, Any]:
        logger.warning(f"{name} failed: {details}")

        return {
            "name": name,
            "status": "FAIL",
            "details": details,
            "metrics": metrics or {},
        }

    @staticmethod
    def _pass(name: str, details: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug(f"{name} passed: {details}")

        return {
            "name": name,
            "status": "PASS",
            "details": details,
            "metrics": metrics
        }

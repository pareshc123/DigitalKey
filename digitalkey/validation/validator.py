from typing import List, Dict, Any

from digitalkey.core.event_model import Event
from digitalkey.reporting.logger import get_logger

from .state_machine import StateMachine
from .flow_validator import FlowValidator
from .timing_validator import TimingValidator

logger = get_logger(__name__)


class Validator:

    def __init__(self, events: List[Event], config: Dict[str, Any], thresholds: Dict[str, Any]):
        self.events = events
        self.config = config

        # Validation config
        self.validation_config = self.config.get("validation", {})

        logger.debug(f"Validator initialized with {len(events)} events")
        logger.debug(f"Validation config: {self.validation_config}")

        # initialize validator
        self.flow_validator = FlowValidator(events)
        self.timing_validator = TimingValidator(events, thresholds)
        self.state_machine = StateMachine(events)

    # public API
    def run_all_validators(self, test_name: str = "Unnamed_test") -> Dict[str, Any]:
        logger.info(f"Running validators for test: {test_name}")

        # basic check
        results = [self._check_no_errors()]

        # Flow Validation
        if self.validation_config.get("enable_flow", True):
            logger.info("Flow validation enabled")
            results.append(self.flow_validator.validate_full_flow())
        else:
            logger.info("Flow validation disabled")

        # Timing Validation
        if self.validation_config.get("enable_timing", True):
            logger.info("Timing validation enabled")
            results.extend(self._run_timing_validations())
        else:
            logger.info("Timing validation disabled")

        # State Machine Validation
        if self.validation_config.get("enable_state_machine", True):
            logger.info("State machine validation enabled")
            results.append(self.state_machine.validate_state())
        else:
            logger.info("State machine validation disabled")

        # Final Aggregation
        overall_status = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"

        logger.info(f"Overall validation status: {overall_status}")

        return {
            "test_name": test_name,
            "status": overall_status,
            "results": results,
            "metrics": self._collect_metrics(results)
        }

    # Basic Check
    def _check_no_errors(self) -> Dict[str, Any]:

        logger.info("Checking for ERROR events")

        errors = [err for err in self.events if err.level == "ERROR"]

        if errors:
            logger.warning(f"{len(errors)} ERROR events found")

            return {
                "name": "no_errors",
                "status": "FAIL",
                "details": f"{len(errors)} error events found",
                "metrics": {
                    "error_count": len(errors)
                }
            }

        logger.info("No ERROR events detected")

        return {
            "name": "no_errors",
            "status": "PASS",
            "details": "No error in the traces detected",
            "metrics": {"error_count": 0}
        }

    # Timing Runner
    def _run_timing_validations(self) -> List[Dict[str, Any]]:
        logger.info("Running timing validations")

        return [
            self.timing_validator.validate_auth_timing(),
            self.timing_validator.validate_detection_to_auth(),
            self.timing_validator.validate_unlock_timing(),
            self.timing_validator.validate_unlock_confirmation(),
            self.timing_validator.validate_session_duration(),
        ]

    # Metrics Aggregation
    @staticmethod
    def _collect_metrics(results: List[Dict[str, Any]]) -> Dict[str, Any]:
        metrics = {}

        for result in results:
            metrics.update(result.get("metrics", {}))

        logger.debug(f"Collected metrics: {metrics}")
        return metrics

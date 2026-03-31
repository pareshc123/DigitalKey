from typing import List, Dict, Any

from digitalkey.core.event_model import Event

from .state_machine import StateMachine
from .flow_validator import FlowValidator
from .timing_validator import TimingValidator


class Validator:

    def __init__(self, events: List[Event], config: Dict[str, Any], thresholds: Dict[str, Any]):
        self.events = events
        self.config = config

        # Validation config
        self.validation_config = self.config.get("validation", {})

        # initialize validator
        self.flow_validator = FlowValidator(events)
        self.timing_validator = TimingValidator(events, thresholds)
        self.state_machine = StateMachine(events)

    # public API
    def run_all_validators(self, test_name: str = "Unnamed_test") -> Dict[str, Any]:

        # basic check
        results = [self._check_no_errors()]

        # Flow Validation
        if self.validation_config.get("enable_flow", True):
            results.append(self.flow_validator.validate_full_flow())

        # Timing Validation
        if self.validation_config.get("enable_timing", True):
            results.extend(self._run_timing_validations())

        # State Machine Validation
        if self.validation_config.get("enable_state_machine", True):
            results.append(self.state_machine.validate_state())

        # Final Aggregation
        overall_status = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
        return {
            "test_name": test_name,
            "status": overall_status,
            "results": results,
            "metrics": self._collect_metrics(results)
        }

    # Basic Check
    def _check_no_errors(self) -> Dict[str, Any]:

        errors = [err for err in self.events if err.level == "ERROR"]

        if errors:
            return {
                "name": "no_errors",
                "status": "FAIL",
                "details": f"{len(errors)} error events found",
                "metrics": {
                    "error_count": len(errors)
                }
            }

        return {
            "name": "no_errors",
            "status": "PASS",
            "details": "No error logs detected",
            "metrics": {"error_count": 0}
        }

    # Timing Runner
    def _run_timing_validations(self) -> List[Dict[str, Any]]:
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

        return metrics

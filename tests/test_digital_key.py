import pytest
from digitalkey.core.log_parser import LogParser
from digitalkey.validation.validator import Validator


@pytest.fixture()
def validator():
    parser = LogParser(r"Python/AutomationTesting/Automotive/DigitalKey/logs/failed_dk_log.txt")
    events = parser.extract_events()
    return Validator(events)


def test_auth_success(validator):
    assert validator.check_auth_flow()


def test_no_errors(validator):
    assert validator.check_no_errors()

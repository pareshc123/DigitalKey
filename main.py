import yaml
from pathlib import Path

from digitalkey.core.log_parser import LogParser
from digitalkey.validation.validator import Validator
from digitalkey.reporting.logger import setup_logger, get_logger
from digitalkey.reporting.report_generator import ReportGenerator


# Utilities
def load_yaml(path: Path):
    logger = get_logger(__name__)

    try:
        with open(path, "r") as file:
            logger.debug(f"{path.name}.yaml opened successfully.")
            return yaml.safe_load(file)
    except Exception as e:
        logger.exception(f"Failed to open {path.name} file. Exception: ", e)
        return None


def main():
    # setup logger
    setup_logger("DEBUG")
    logger = get_logger(__name__)

    logger.info("Starting Digital Key validation framework")

    base_dir = Path(__file__).resolve().parent

    # load config and thresholds
    logger.info("Loading configuration files")

    config = load_yaml(base_dir / "config/test_config.yaml")

    # load threshold
    thresholds = load_yaml(base_dir / "config/thresholds.yaml")

    # parser
    parser = LogParser(r"Traces/success.log")
    events = parser.extract_events()

    # validator
    validator = Validator(events, config, thresholds)
    result = validator.run_all_validators(test_name=config["test"]["name"])

    # report
    reporter = ReportGenerator(config)
    reporter.generate(result)


if __name__ == "__main__":
    main()

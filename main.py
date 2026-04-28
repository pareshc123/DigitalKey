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
            logger.debug(f"{path.name} opened successfully.")
            return yaml.safe_load(file)
    except Exception:
        logger.exception(f"Failed to open {path.name} file")
        return None


def main():
    # setup logger
    setup_logger("DEBUG")
    logger = get_logger(__name__)

    logger.info("Starting Digital Key validation framework")

    base_dir = Path(__file__).resolve().parent

    try:

        # load config and thresholds
        logger.info("Loading configuration files")

        config_file = base_dir / "config/test_config.yaml"
        thresholds_file = base_dir / "config/thresholds.yaml"

        config = load_yaml(config_file)
        thresholds = load_yaml(thresholds_file)

        if not config or not thresholds:
            logger.error("Missing configuration. Abort execution.")
            return

        # Parse traces into events
        logger.info("Parsing input logs")
        log_path = base_dir / "ECU_Traces/success.log"

        parser = LogParser(log_path)
        events = parser.extract_events()

        if not events:
            logger.error("No events parsed. Aborting execution.")
            return

        logger.debug(f"Parsed {len(events)} events")

        # validation
        logger.info("Running validation")
        validator = Validator(events, config, thresholds)
        result = validator.run_all_validators(test_name=config["test"]["name"])
        logger.info("Validation completed")

        # Reporting
        logger.info("Generating report")
        reporter = ReportGenerator(config)
        reporter.generate(result)
        logger.info("Report generation completed")

    except Exception:
        logger.exception("Unexpected error during execution")

    finally:
        logger.info("Digital Key Validation finished")


if __name__ == "__main__":
    main()

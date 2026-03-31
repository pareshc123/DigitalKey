import yaml

from digitalkey.core.log_parser import LogParser
from digitalkey.validation.validator import Validator
from digitalkey.reporting.report_generator import ReportGenerator


# function to load .yaml
def load_yaml(path: str):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def main():

    # load config
    config = load_yaml(r"config/test_config.yaml")

    # load threshold
    thresholds = load_yaml(r"config/thresholds.yaml")

    # parser
    parser = LogParser(r"logs/success.log")
    events = parser.extract_events()

    # validator
    validator = Validator(events, config, thresholds)
    result = validator.run_all_validators(test_name=config["test"]["name"])

    # report
    reporter = ReportGenerator(config)
    reporter.generate(result)


if __name__ == "__main__":
    main()

# A System-Level Digital Key Validation Framework

### Project Structure:

DigitalKey/

    ├── config/                  # Configurable parameters
    │   ├── thresholds.yaml      # timing limits, distance thresholds
    │   └── test_config.yaml     # test execution settings
    │
    ├── Traces/                    # Raw Traces (input)
    │   ├── happy_path.log
    │   ├── delayed_auth.log
    │   ├── uwb_failure.log
    │   ├── auth_failure.log
    │   └── noisy_environment.log
    │
    ├── test_data/               # Data-driven test definitions
    │   └── test_scenarios.json
    │
    ├── digitalkey/
    │   ├── core/
    │   │   ├── log_parser.py        # parsing
    │   │   ├── event_model.py       # structured event object
    │   │   └── session_tracker.py   # session correlation
    │   │
    │   ├── validation/
    │   │   ├── validator.py         # validator runner
    │   │   ├── timing_validator.py  # (timing checks)
    │   │   ├── flow_validator.py    # (scenario validation)
    │   │   └── state_machine.py     # (state validator)
    │   │
    │   ├── analysis/
    │   │   ├── trace_analyzer.py    # todo: filtering, debugging
    │   │   └── metrics.py           # todo: latency, stats
    │   │
    │   ├── reporting/
    │   │   ├── report_generator.py  # reporting
    │   │   ├── logger.py            # execution logger
    │   │   └── export.py            # CSV/JSON output
    │
    ├── tests/
    │   ├── unit/
    │   ├── integration/             # todo: scenario-level tests
    │   └── regression/              # todo: data-driven tests
    │
    ├── reports/
    │   ├── latest/
    │   └── history/
    │
    ├── main.py                      # test runner
    ├── cli.py                       # todo: optional CLI entry
    ├── pyproject.toml
    └── README.md

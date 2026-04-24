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
    │   │   ├── log_parser.py        # parsing (keep, improve)
    │   │   ├── event_model.py       # structured event object (NEW)
    │   │   └── session_tracker.py   # session correlation (NEW)
    │   │
    │   ├── validation/
    │   │   ├── validator.py         # extend heavily
    │   │   ├── timing_validator.py  # NEW (timing checks)
    │   │   ├── flow_validator.py    # NEW (scenario validation)
    │   │   └── state_machine.py     # NEW (critical)
    │   │
    │   ├── analysis/
    │   │   ├── trace_analyzer.py    # filtering, debugging (NEW)
    │   │   └── metrics.py           # latency, stats (NEW)
    │   │
    │   ├── reporting/
    │   │   ├── report_generator.py  # improved reporting
    │   │   ├── logger.py            # execution logger (NEW)
    │   │   └── export.py            # CSV/JSON output (NEW)
    │
    ├── tests/
    │   ├── unit/
    │   ├── integration/             # scenario-level tests
    │   └── regression/              # data-driven tests
    │
    ├── reports/
    │   ├── latest/
    │   └── history/
    │
    ├── main.py                      # test runner
    ├── cli.py                       # optional CLI entry (NEW)
    ├── pyproject.toml
    └── README.md

import csv
import json
import os
from typing import Dict, Any
from datetime import datetime

from digitalkey.reporting.logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.reporting_config = config.get("reporting", {})
        logger.debug("ReportGenerator initialized")

    # public API
    def generate(self, result: Dict[str, Any]) -> None:

        logger.info(f"Generating report for test: {result.get('test_name')}")

        self._print_summary(result)

        if self.reporting_config.get("save_report", False):
            self._save(result)
        else:
            logger.info("Report saving disabled in configuration")

    # Console Output
    @staticmethod
    def _print_summary(result: Dict[str, Any]) -> None:
        logger.info("=" * 60)
        logger.info(f"TEST: {result['test_name']}")
        logger.info(f"STATUS: {result['status']}")
        logger.info("=" * 60)

        for res in result["results"]:
            logger.info(f"{res['name']} -> {res['status']}")
            logger.info(f"    {res['details']}")

        logger.info("-" * 60)
        logger.info("METRICS:")

        for key, value in result.get("metrics", {}).items():
            logger.info(f"  {key}: {value}")

        logger.info("=" * 60)

    # save reports
    def _save(self, results: Dict[str, Any]) -> None:

        formats = self.reporting_config.get("output_format", ["json"])
        output_dir = self._get_output_dir(results["test_name"])

        logger.info(f"Saving report in formats: {formats}")
        logger.debug(f"Report output directory: {output_dir}")

        if "json" in formats:
            self._save_json(results, output_dir)

        if "csv" in formats:
            self._save_csv(results, output_dir)

    # json export
    @staticmethod
    def _save_json(results: Dict[str, Any], output_dir: str) -> None:
        path = os.path.join(output_dir, "_report.json")

        try:
            with open(path, "w") as f:
                json.dump(results, f, indent=4, default=str)

            logger.info(f"JSON report saved: {path}")

        except Exception:    # noqa
            logger.exception(f"Failed to save JSON report: {path}")

    @staticmethod
    def _save_csv(results: Dict[str, Any], output_dir: str) -> None:
        path = os.path.join(output_dir, "_report.csv")

        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "status", "details"])

                for res in results["results"]:
                    writer.writerow([res["name"], res["status"], res["details"]])

            logger.info(f"CSV report saved: {path}")

        except Exception:    # noqa
            logger.exception(f"Failed to save CSV report: {path}")

    # Output Directory
    @staticmethod
    def _get_output_dir(test_name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{test_name}_{timestamp}"

        base_dir = "reports"
        output_dir = os.path.join(base_dir, folder_name)

        os.makedirs(output_dir, exist_ok=True)

        logger.debug(f"Created report directory: {output_dir}")
        return output_dir

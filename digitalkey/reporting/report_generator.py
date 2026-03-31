import csv
import json
import os
from typing import Dict, Any
from datetime import  datetime


class ReportGenerator:

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.reporting_config = config.get("reporting", {})

    # public API
    def generate(self, result: Dict[str, Any]) -> None:

        self._print_summary(result)

        if self.reporting_config.get("save_report", False):
            self._save(result)

    # Console Output
    @staticmethod
    def _print_summary(result: Dict[str, Any]) -> None:
        print("\n" + "=" * 60)
        print(f"TEST: {result['test_name']}")
        print(f"STATUS: {result['status']}")
        print("=" * 60)

        for res in result["results"]:
            print(f"{res['name']} -> {res['status']}")
            print(f"    {res['details']}")

        print("-" * 60)
        print("METRICS:")
        for key, value in result.get("metrics", {}).items():
            print(f"  {key}: {value}")

        print("=" * 60 + "\n")

    # save reports
    def _save(self, results: Dict[str, Any]) -> None:

        formats = self.reporting_config.get("output_format", ["json"])

        output_dir = self._get_output_dir(results["test_name"])

        if "json" in formats:
            self._save_json(results, output_dir)

        if "csv" in formats:
            self._save_csv(results, output_dir)

    # json export
    @staticmethod
    def _save_json(results: Dict[str, Any], output_dir: str) -> None:
        path = os.path.join(output_dir, "_report.json")

        with open(path, "w") as f:
            json.dump(results, f, indent=4)

        print(f"[INFO] JSON report saved: {path}")

    # csv reports
    @staticmethod
    def _save_csv(results: Dict[str, Any], output_dir: str) -> None:

        path = os.path.join(output_dir, "_report.csv")

        with open(path, "w", newline="") as f:
            writer = csv.writer(f)

            # header
            writer.writerow(["name", "status", "details"])

            for res in results["results"]:
                writer.writerow([res["name"], res["status"], res["details"]])

        print(f"[INFO] CSV report saved: {path}")

    # Output Directory
    @staticmethod
    def _get_output_dir(test_name: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"{test_name}_{timestamp}"

        base_dir = "reports"
        output_dir = os.path.join(base_dir, folder_name)

        os.makedirs(output_dir, exist_ok=True)

        return output_dir

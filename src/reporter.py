"""Write parsed scan data as a JSON report."""

import json
from pathlib import Path


def write_json_report(data: dict, output_path: Path) -> None:
    """Create parent directories and write an indented UTF-8 JSON report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as report_file:
        json.dump(data, report_file, indent=4)
        report_file.write("\n")

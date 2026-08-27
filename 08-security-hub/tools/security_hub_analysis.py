"""
Analyze AWS Security Hub findings with Pandas.

uv run tools/security_hub_analysis.py
"""

import json
from pathlib import Path
import pandas as pd


def save_findings(findings: list[dict], path: Path) -> None:
    """Save raw Security Hub findings to a local JSON snapshot."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2, default=str)


def load_findings(path: Path) -> list[dict]:
    """Load Security Hub findings from a local JSON snapshot."""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def create_findings_dataframe(findings: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(findings)


def main() -> None:
    path = Path("data/security_hub_findings.json")
    findings = load_findings(path)
    findings_df = create_findings_dataframe(findings)

    print("Security Hub Findings Analysis")
    print("=" * 50)
    print()
    print(f"Findings: {len(findings_df)}")
    print(f"Columns : {len(findings_df.columns)}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

import pandas as pd


TABLES_DIR = Path("outputs/tables")
DEFAULT_PRIORITY_PATH = TABLES_DIR / "customer_priority_table.csv"
DEFAULT_TOP20_PATH = TABLES_DIR / "top_20_retention_targets.csv"


def compute_priority_score(
    df: pd.DataFrame,
    probability_column: str = "churn_probability",
    value_column: str = "MonthlyCharges",
    output_column: str = "priority_score",
) -> pd.DataFrame:
    """Compute retention priority score from churn probability and value proxy."""
    prioritized = df.copy()
    prioritized[output_column] = prioritized[probability_column] * prioritized[value_column]
    return prioritized


def assign_priority_segments(
    df: pd.DataFrame,
    probability_column: str = "churn_probability",
    value_column: str = "MonthlyCharges",
) -> pd.DataFrame:
    """Assign risk, value, and priority levels using quantile-based segmentation."""
    segmented = df.copy()
    risk_cutoff = segmented[probability_column].quantile(0.75)
    value_cutoff = segmented[value_column].median()

    segmented["risk_segment"] = segmented[probability_column].apply(
        lambda x: "High Risk" if x >= risk_cutoff else "Low Risk"
    )
    segmented["value_segment"] = segmented[value_column].apply(
        lambda x: "High Value" if x >= value_cutoff else "Low Value"
    )

    def map_priority(row: pd.Series) -> str:
        if row["risk_segment"] == "High Risk" and row["value_segment"] == "High Value":
            return "Top Priority"
        if row["risk_segment"] == "High Risk" and row["value_segment"] == "Low Value":
            return "Secondary Priority"
        if row["risk_segment"] == "Low Risk" and row["value_segment"] == "High Value":
            return "Monitor"
        return "Low Priority"

    segmented["priority_level"] = segmented.apply(map_priority, axis=1)
    return segmented


def build_priority_table(
    df: pd.DataFrame,
    customer_id_column: str = "customerID",
    probability_column: str = "churn_probability",
    value_column: str = "MonthlyCharges",
) -> pd.DataFrame:
    """Create a sorted retention priority table."""
    priority_df = compute_priority_score(
        df,
        probability_column=probability_column,
        value_column=value_column,
    )
    priority_df = assign_priority_segments(
        priority_df,
        probability_column=probability_column,
        value_column=value_column,
    )

    preferred_columns = [
        customer_id_column,
        probability_column,
        value_column,
        "priority_score",
        "risk_segment",
        "value_segment",
        "priority_level",
    ]
    available_columns = [column for column in preferred_columns if column in priority_df.columns]
    return priority_df[available_columns].sort_values(by="priority_score", ascending=False).reset_index(drop=True)


def save_priority_outputs(
    priority_df: pd.DataFrame,
    priority_path: str | Path = DEFAULT_PRIORITY_PATH,
    top20_path: str | Path = DEFAULT_TOP20_PATH,
) -> tuple[Path, Path]:
    """Persist the full priority table and its top-20 subset."""
    priority_destination = Path(priority_path)
    top20_destination = Path(top20_path)
    priority_destination.parent.mkdir(parents=True, exist_ok=True)
    top20_destination.parent.mkdir(parents=True, exist_ok=True)

    priority_df.to_csv(priority_destination, index=False)
    priority_df.head(20).to_csv(top20_destination, index=False)
    return priority_destination, top20_destination

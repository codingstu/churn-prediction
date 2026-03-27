from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


RAW_DATA_PATH = Path("data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = Path("data/processed/cleaned_churn.csv")
TARGET_COLUMN = "Churn"
ID_COLUMN = "customerID"
TOTAL_CHARGES_COLUMN = "TotalCharges"


@dataclass(frozen=True)
class CleaningSummary:
    input_rows: int
    output_rows: int
    dropped_rows: int


def load_raw_data(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw Telco churn dataset from disk."""
    return pd.read_csv(path)


def normalize_blank_strings(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Replace blank-string values with pandas NA for the specified columns."""
    cleaned = df.copy()
    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].replace(r"^\s*$", pd.NA, regex=True)
    return cleaned


def clean_telco_data(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningSummary]:
    """Clean the IBM Telco churn dataset for downstream analysis."""
    cleaned = normalize_blank_strings(df, [TOTAL_CHARGES_COLUMN])

    if TOTAL_CHARGES_COLUMN in cleaned.columns:
        cleaned[TOTAL_CHARGES_COLUMN] = pd.to_numeric(cleaned[TOTAL_CHARGES_COLUMN], errors="coerce")

    if TARGET_COLUMN in cleaned.columns:
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].map({"Yes": 1, "No": 0})

    input_rows = len(cleaned)
    cleaned = cleaned.dropna(subset=[TOTAL_CHARGES_COLUMN, TARGET_COLUMN]).copy()
    output_rows = len(cleaned)

    summary = CleaningSummary(
        input_rows=input_rows,
        output_rows=output_rows,
        dropped_rows=input_rows - output_rows,
    )
    return cleaned, summary


def prepare_model_frame(df: pd.DataFrame, drop_identifier: bool = True) -> pd.DataFrame:
    """Return a modeling-ready dataframe with target retained and identifier optionally removed."""
    model_df = df.copy()
    if drop_identifier and ID_COLUMN in model_df.columns:
        model_df = model_df.drop(columns=[ID_COLUMN])
    return model_df


def save_processed_data(df: pd.DataFrame, path: str | Path = PROCESSED_DATA_PATH) -> None:
    """Persist cleaned data to disk, creating parent directories when needed."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)


if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df, cleaning_summary = clean_telco_data(raw_df)
    save_processed_data(cleaned_df)
    print(cleaning_summary)

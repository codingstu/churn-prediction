from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


EXPECTED_COLUMNS = (
    "customerID",
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
    "Churn",
)


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
    blank_total_charges_before: int
    blank_total_charges_after_normalization: int
    target_missing_before_drop: int
    invalid_target_values: int
    duplicate_customer_ids: int


def load_raw_data(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw Telco churn dataset from disk."""
    return pd.read_csv(path)


def validate_raw_schema(df: pd.DataFrame) -> None:
    """Validate the raw IBM Telco dataset schema before cleaning."""
    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    unexpected_columns = [column for column in df.columns if column not in EXPECTED_COLUMNS]

    if missing_columns or unexpected_columns or len(df.columns) != len(EXPECTED_COLUMNS):
        raise ValueError(
            "Raw dataset schema mismatch. "
            f"missing_columns={missing_columns}, "
            f"unexpected_columns={unexpected_columns}, "
            f"observed_column_count={len(df.columns)}, "
            f"expected_column_count={len(EXPECTED_COLUMNS)}"
        )


def validate_customer_ids(df: pd.DataFrame) -> int:
    """Validate that customer identifiers are present and unique."""
    if ID_COLUMN not in df.columns:
        raise ValueError(f"Missing required identifier column: {ID_COLUMN}")

    missing_customer_ids = int(df[ID_COLUMN].isna().sum())
    if missing_customer_ids:
        raise ValueError(f"customerID contains {missing_customer_ids} missing values")

    duplicate_customer_ids = int(df[ID_COLUMN].duplicated().sum())
    if duplicate_customer_ids:
        raise ValueError(f"customerID contains {duplicate_customer_ids} duplicate values")

    return duplicate_customer_ids


def validate_target_values(df: pd.DataFrame) -> int:
    """Validate that raw churn labels only contain expected values."""
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Missing required target column: {TARGET_COLUMN}")

    normalized_target = df[TARGET_COLUMN].astype("string").str.strip()
    invalid_mask = normalized_target.notna() & ~normalized_target.isin(["Yes", "No"])
    invalid_target_values = int(invalid_mask.sum())
    if invalid_target_values:
        invalid_examples = sorted(normalized_target[invalid_mask].dropna().unique().tolist())
        raise ValueError(
            f"Churn contains {invalid_target_values} invalid values: {invalid_examples}"
        )

    return invalid_target_values


def normalize_blank_strings(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Replace blank-string values with pandas NA for the specified columns."""
    cleaned = df.copy()
    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].replace(r"^\s*$", pd.NA, regex=True)
    return cleaned


def clean_telco_data(df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningSummary]:
    """Clean the IBM Telco churn dataset for downstream analysis."""
    validate_raw_schema(df)
    duplicate_customer_ids = validate_customer_ids(df)
    invalid_target_values = validate_target_values(df)

    blank_total_charges_before = 0
    if TOTAL_CHARGES_COLUMN in df.columns:
        total_charges_as_string = df[TOTAL_CHARGES_COLUMN].astype("string")
        blank_total_charges_before = int(total_charges_as_string.str.strip().eq("").fillna(False).sum())

    cleaned = normalize_blank_strings(df, [TOTAL_CHARGES_COLUMN])

    blank_total_charges_after_normalization = 0
    if TOTAL_CHARGES_COLUMN in cleaned.columns:
        blank_total_charges_after_normalization = int(cleaned[TOTAL_CHARGES_COLUMN].isna().sum())
        cleaned[TOTAL_CHARGES_COLUMN] = pd.to_numeric(cleaned[TOTAL_CHARGES_COLUMN], errors="coerce")

    target_missing_before_drop = 0
    if TARGET_COLUMN in cleaned.columns:
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].astype("string").str.strip()
        target_missing_before_drop = int(cleaned[TARGET_COLUMN].isna().sum())
        cleaned[TARGET_COLUMN] = cleaned[TARGET_COLUMN].map({"Yes": 1, "No": 0})

    input_rows = len(cleaned)
    cleaned = cleaned.dropna(subset=[TOTAL_CHARGES_COLUMN, TARGET_COLUMN]).copy()
    output_rows = len(cleaned)

    summary = CleaningSummary(
        input_rows=input_rows,
        output_rows=output_rows,
        dropped_rows=input_rows - output_rows,
        blank_total_charges_before=blank_total_charges_before,
        blank_total_charges_after_normalization=blank_total_charges_after_normalization,
        target_missing_before_drop=target_missing_before_drop,
        invalid_target_values=invalid_target_values,
        duplicate_customer_ids=duplicate_customer_ids,
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


def save_cleaning_audit(summary: CleaningSummary, path: str | Path = "outputs/tables/data_cleaning_audit.csv") -> Path:
    """Persist a stable audit table for the preprocessing stage."""
    audit = pd.DataFrame(
        {
            "metric": [
                "input_rows",
                "output_rows",
                "dropped_rows",
                "blank_total_charges_before",
                "blank_total_charges_after_normalization",
                "target_missing_before_drop",
                "invalid_target_values",
                "duplicate_customer_ids",
            ],
            "value": [
                summary.input_rows,
                summary.output_rows,
                summary.dropped_rows,
                summary.blank_total_charges_before,
                summary.blank_total_charges_after_normalization,
                summary.target_missing_before_drop,
                summary.invalid_target_values,
                summary.duplicate_customer_ids,
            ],
        }
    )
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    audit.to_csv(destination, index=False)
    return destination


if __name__ == "__main__":
    raw_df = load_raw_data()
    cleaned_df, cleaning_summary = clean_telco_data(raw_df)
    save_processed_data(cleaned_df)
    audit_path = save_cleaning_audit(cleaning_summary)
    print(cleaning_summary)
    print(f"cleaning_audit={audit_path}")

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROCESSED_DATA_PATH = Path("data/processed/cleaned_churn.csv")
FIGURES_DIR = Path("outputs/figures")
TABLES_DIR = Path("outputs/tables")
TARGET_COLUMN = "Churn"


def load_processed_data(path: str | Path = PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Load the cleaned churn dataset."""
    return pd.read_csv(path)


def ensure_output_dirs() -> None:
    """Create output directories required for EDA artifacts."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def save_dataset_overview(df: pd.DataFrame, path: str | Path = TABLES_DIR / "dataset_overview.csv") -> Path:
    """Save a compact dataset overview table for reporting."""
    overview = pd.DataFrame(
        {
            "metric": ["row_count", "column_count", "churn_rate"],
            "value": [len(df), df.shape[1], float(df[TARGET_COLUMN].mean()) if TARGET_COLUMN in df.columns else None],
        }
    )
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    overview.to_csv(destination, index=False)
    return destination


def save_numeric_summary(df: pd.DataFrame, path: str | Path = TABLES_DIR / "numeric_summary.csv") -> Path:
    """Save descriptive statistics for numeric columns."""
    numeric_summary = df.describe(include=["number"]).T.reset_index().rename(columns={"index": "feature"})
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    numeric_summary.to_csv(destination, index=False)
    return destination


def _save_figure(fig: plt.Figure, filename: str) -> Path:
    output_path = FIGURES_DIR / filename
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_churn_distribution(df: pd.DataFrame) -> Path:
    """Plot churn class distribution."""
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x=TARGET_COLUMN, ax=ax)
    ax.set_title("Churn Class Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Count")
    return _save_figure(fig, "churn_class_distribution.png")


def plot_tenure_vs_churn(df: pd.DataFrame) -> Path:
    """Plot tenure distribution by churn."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df, x=TARGET_COLUMN, y="tenure", ax=ax)
    ax.set_title("Tenure vs Churn")
    return _save_figure(fig, "tenure_vs_churn.png")


def plot_contract_vs_churn(df: pd.DataFrame) -> Path:
    """Plot contract type against churn."""
    summary = (
        df.groupby("Contract", as_index=False)[TARGET_COLUMN]
        .mean()
        .sort_values(by=TARGET_COLUMN, ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=summary, x="Contract", y=TARGET_COLUMN, ax=ax)
    ax.set_title("Contract Type vs Churn Rate")
    ax.set_ylabel("Churn Rate")
    return _save_figure(fig, "contract_type_vs_churn_rate.png")


def plot_monthly_charges_vs_churn(df: pd.DataFrame) -> Path:
    """Plot monthly charges distribution by churn."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df, x=TARGET_COLUMN, y="MonthlyCharges", ax=ax)
    ax.set_title("Monthly Charges vs Churn")
    return _save_figure(fig, "monthly_charges_vs_churn.png")


def plot_total_charges_vs_churn(df: pd.DataFrame) -> Path:
    """Plot total charges distribution by churn."""
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.boxplot(data=df, x=TARGET_COLUMN, y="TotalCharges", ax=ax)
    ax.set_title("Total Charges vs Churn")
    return _save_figure(fig, "total_charges_vs_churn.png")


def plot_payment_method_vs_churn(df: pd.DataFrame) -> Path:
    """Plot payment method against churn rate."""
    summary = (
        df.groupby("PaymentMethod", as_index=False)[TARGET_COLUMN]
        .mean()
        .sort_values(by=TARGET_COLUMN, ascending=False)
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=summary, x="PaymentMethod", y=TARGET_COLUMN, ax=ax)
    ax.set_title("Payment Method vs Churn Rate")
    ax.set_ylabel("Churn Rate")
    ax.tick_params(axis="x", rotation=20)
    return _save_figure(fig, "payment_method_vs_churn.png")


def plot_internet_service_vs_churn(df: pd.DataFrame) -> Path:
    """Plot internet service type against churn rate."""
    summary = (
        df.groupby("InternetService", as_index=False)[TARGET_COLUMN]
        .mean()
        .sort_values(by=TARGET_COLUMN, ascending=False)
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=summary, x="InternetService", y=TARGET_COLUMN, ax=ax)
    ax.set_title("Internet Service vs Churn Rate")
    ax.set_ylabel("Churn Rate")
    return _save_figure(fig, "internet_service_vs_churn.png")


def plot_correlation_heatmap(df: pd.DataFrame) -> Path:
    """Plot a correlation heatmap for numeric variables."""
    numeric_df = df.select_dtypes(include=["number"])
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues", fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    return _save_figure(fig, "correlation_heatmap.png")


def run_eda(df: pd.DataFrame) -> dict[str, Path]:
    """Generate the required EDA tables and figures."""
    ensure_output_dirs()
    artifacts = {
        "dataset_overview": save_dataset_overview(df),
        "numeric_summary": save_numeric_summary(df),
        "churn_distribution": plot_churn_distribution(df),
        "tenure_vs_churn": plot_tenure_vs_churn(df),
        "contract_vs_churn": plot_contract_vs_churn(df),
        "monthly_charges_vs_churn": plot_monthly_charges_vs_churn(df),
        "total_charges_vs_churn": plot_total_charges_vs_churn(df),
        "payment_method_vs_churn": plot_payment_method_vs_churn(df),
        "internet_service_vs_churn": plot_internet_service_vs_churn(df),
        "correlation_heatmap": plot_correlation_heatmap(df),
    }
    return artifacts


if __name__ == "__main__":
    dataset = load_processed_data()
    artifact_paths = run_eda(dataset)
    for name, path in artifact_paths.items():
        print(f"{name}: {path}")

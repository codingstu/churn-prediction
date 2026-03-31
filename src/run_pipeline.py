from __future__ import annotations

from pathlib import Path

from sklearn.model_selection import train_test_split

from src.eda import load_processed_data, run_eda
from src.evaluate import (
    build_performance_table,
    evaluate_binary_classifier,
    plot_confusion_matrix,
    plot_roc_curves,
    save_performance_table,
)
from src.explain import run_explainability
from src.preprocess import (
    clean_telco_data,
    load_raw_data,
    prepare_model_frame,
    save_cleaning_audit,
    save_processed_data,
)
from src.prioritize import build_priority_table, save_priority_outputs
from src.train import save_model, train_models


RAW_DATA_PATH = Path("data/raw/Telco Customer Churn (IBM)/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = Path("data/processed/cleaned_churn.csv")
TARGET_COLUMN = "Churn"
ID_COLUMN = "customerID"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def run_cleaning_stage() -> Path:
    """Load raw data, clean it, and persist the processed dataset."""
    raw_df = load_raw_data(RAW_DATA_PATH)
    cleaned_df, summary = clean_telco_data(raw_df)
    save_processed_data(cleaned_df, PROCESSED_DATA_PATH)
    audit_path = save_cleaning_audit(summary)
    print(f"cleaning_summary={summary}")
    print(f"cleaning_audit={audit_path}")
    return PROCESSED_DATA_PATH


def run_modeling_stage(processed_df):
    """Train configured models and return split datasets with fitted pipelines."""
    modeling_df = prepare_model_frame(processed_df, drop_identifier=False)
    X = modeling_df.drop(columns=[TARGET_COLUMN])
    y = modeling_df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    train_features = X_train.drop(columns=[ID_COLUMN], errors="ignore")
    test_features = X_test.drop(columns=[ID_COLUMN], errors="ignore")

    trained_models = train_models(train_features, y_train)
    return X_train, X_test, y_train, y_test, train_features, test_features, trained_models


def run_evaluation_stage(trained_models, X_test, y_test):
    """Evaluate all trained models and save model comparison artifacts."""
    metrics = {}
    fitted_pipelines = {}

    for model_name, trained in trained_models.items():
        fitted_pipelines[model_name] = trained.pipeline
        metrics[model_name] = evaluate_binary_classifier(trained.pipeline, X_test, y_test)
        plot_confusion_matrix(trained.pipeline, X_test, y_test, model_name)

    performance_table = build_performance_table(metrics)
    save_performance_table(performance_table)
    plot_roc_curves(fitted_pipelines, X_test, y_test)
    return performance_table, fitted_pipelines


def select_best_model(performance_table, fitted_pipelines):
    """Select and persist the top-ranked model according to the evaluation table."""
    best_model_name = performance_table.iloc[0]["model"]
    best_model = fitted_pipelines[best_model_name]
    output_path = save_model(best_model, "best_model")
    print(f"best_model={best_model_name}, saved_to={output_path}")
    return best_model_name, best_model


def run_explainability_stage(best_model_name, best_model, X_reference):
    """Generate explainability artifacts for the selected best model."""
    reference_features = X_reference.drop(columns=[ID_COLUMN], errors="ignore")
    artifacts = run_explainability(best_model_name, best_model, reference_features)
    for artifact_name, artifact_path in artifacts.items():
        print(f"explainability::{artifact_name}={artifact_path}")
    return artifacts


def run_prioritization_stage(best_model, X_test):
    """Generate retention prioritization outputs for the test partition."""
    scoring_features = X_test.drop(columns=[ID_COLUMN], errors="ignore")
    scored = X_test.copy()
    scored["churn_probability"] = best_model.predict_proba(scoring_features)[:, 1]
    priority_table = build_priority_table(
        scored,
        customer_id_column=ID_COLUMN,
        probability_column="churn_probability",
        value_column="MonthlyCharges",
    )
    priority_path, top20_path = save_priority_outputs(priority_table)
    print(f"priority_table={priority_path}")
    print(f"top20_targets={top20_path}")
    return priority_table


def main() -> None:
    """Run the end-to-end churn analytics pipeline using the IBM Telco dataset."""
    run_cleaning_stage()
    processed_df = load_processed_data(PROCESSED_DATA_PATH)
    eda_artifacts = run_eda(processed_df)
    for artifact_name, artifact_path in eda_artifacts.items():
        print(f"eda::{artifact_name}={artifact_path}")

    X_train, X_test, y_train, y_test, train_features, test_features, trained_models = run_modeling_stage(processed_df)
    performance_table, fitted_pipelines = run_evaluation_stage(trained_models, test_features, y_test)
    best_model_name, best_model = select_best_model(performance_table, fitted_pipelines)
    run_explainability_stage(best_model_name, best_model, train_features)
    run_prioritization_stage(best_model, X_test)


if __name__ == "__main__":
    main()

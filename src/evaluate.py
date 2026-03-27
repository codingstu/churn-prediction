from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


FIGURES_DIR = Path("outputs/figures")
TABLES_DIR = Path("outputs/tables")


def predict_scores(model: Any, X: pd.DataFrame) -> pd.Series:
    """Return positive-class probabilities when available."""
    if hasattr(model, "predict_proba"):
        return pd.Series(model.predict_proba(X)[:, 1], index=X.index, name="score")
    raise AttributeError("Model does not support predict_proba, which is required for evaluation.")


def evaluate_binary_classifier(model: Any, X_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5) -> dict[str, float]:
    """Compute standard churn classification metrics."""
    scores = predict_scores(model, X_test)
    predictions = (scores >= threshold).astype(int)
    return {
        "roc_auc": roc_auc_score(y_test, scores),
        "f1_score": f1_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
    }


def build_performance_table(results: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Convert nested metric dictionaries into a sorted dataframe."""
    table = pd.DataFrame(results).T.reset_index().rename(columns={"index": "model"})
    return table.sort_values(by=["recall", "roc_auc"], ascending=False).reset_index(drop=True)


def save_performance_table(table: pd.DataFrame, path: str | Path = TABLES_DIR / "model_performance_comparison.csv") -> Path:
    """Write the model comparison table to disk."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(destination, index=False)
    return destination


def plot_confusion_matrix(model: Any, X_test: pd.DataFrame, y_test: pd.Series, model_name: str, threshold: float = 0.5) -> Path:
    """Save a confusion matrix figure for a trained model."""
    scores = predict_scores(model, X_test)
    predictions = (scores >= threshold).astype(int)
    matrix = confusion_matrix(y_test, predictions)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / f"confusion_matrix_{model_name}.png"

    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(confusion_matrix=matrix).plot(ax=ax, colorbar=False)
    ax.set_title(f"Confusion Matrix - {model_name}")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)
    return output_path


def plot_roc_curves(models: dict[str, Any], X_test: pd.DataFrame, y_test: pd.Series, path: str | Path = FIGURES_DIR / "roc_curve_comparison.png") -> Path:
    """Plot ROC curves for multiple fitted models."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    for model_name, model in models.items():
        scores = predict_scores(model, X_test)
        fpr, tpr, _ = roc_curve(y_test, scores)
        auc = roc_auc_score(y_test, scores)
        ax.plot(fpr, tpr, label=f"{model_name} (AUC={auc:.3f})")

    ax.plot([0, 1], [0, 1], linestyle="--", color="grey")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve Comparison")
    ax.legend()
    fig.tight_layout()
    fig.savefig(destination, dpi=300)
    plt.close(fig)
    return destination

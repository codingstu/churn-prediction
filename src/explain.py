from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    import shap
except ImportError:  # pragma: no cover - optional runtime dependency handling
    shap = None


FIGURES_DIR = Path("outputs/figures")
TABLES_DIR = Path("outputs/tables")


def ensure_output_dirs() -> None:
    """Create output directories required for explainability artifacts."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)


def _unwrap_model(model: Any) -> Any:
    """Return the estimator inside a pipeline when present."""
    if hasattr(model, "named_steps") and "model" in model.named_steps:
        return model.named_steps["model"]
    return model


def _transform_features(model: Any, X: pd.DataFrame):
    """Transform features through pipeline preprocessing when available."""
    if hasattr(model, "named_steps") and "preprocess" in model.named_steps:
        transformed = model.named_steps["preprocess"].transform(X)
        feature_names = model.named_steps["preprocess"].get_feature_names_out()
        return transformed, feature_names
    return X.values, np.array(X.columns)


def save_logistic_coefficients(model: Any, X: pd.DataFrame, path: str | Path = TABLES_DIR / "logistic_coefficients.csv") -> Path:
    """Export Logistic Regression coefficients for global interpretation."""
    estimator = _unwrap_model(model)
    transformed, feature_names = _transform_features(model, X)

    if not hasattr(estimator, "coef_"):
        raise AttributeError("The provided model does not expose coefficients.")

    coefficients = pd.DataFrame(
        {
            "feature": feature_names,
            "coefficient": estimator.coef_.ravel(),
            "abs_coefficient": np.abs(estimator.coef_.ravel()),
        }
    ).sort_values(by="abs_coefficient", ascending=False)

    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    coefficients.to_csv(destination, index=False)
    return destination


def save_tree_feature_importance(model: Any, X: pd.DataFrame, output_name: str) -> tuple[Path, Path]:
    """Export tree-based feature importance as both table and figure."""
    estimator = _unwrap_model(model)
    _, feature_names = _transform_features(model, X)

    if not hasattr(estimator, "feature_importances_"):
        raise AttributeError("The provided model does not expose tree-based feature importance.")

    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": estimator.feature_importances_,
        }
    ).sort_values(by="importance", ascending=False)

    table_path = TABLES_DIR / f"{output_name}_feature_importance.csv"
    figure_path = FIGURES_DIR / f"{output_name}_feature_importance.png"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    importance.to_csv(table_path, index=False)

    top_features = importance.head(20).sort_values(by="importance", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(top_features["feature"], top_features["importance"])
    ax.set_title(f"Feature Importance - {output_name}")
    ax.set_xlabel("Importance")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=300)
    plt.close(fig)

    return table_path, figure_path


def save_shap_summary(model: Any, X: pd.DataFrame, output_name: str = "shap_summary") -> Path:
    """Generate a SHAP summary plot for the provided fitted model."""
    if shap is None:
        raise ImportError("SHAP is not installed. Install the dependency before generating SHAP outputs.")

    transformed, feature_names = _transform_features(model, X)
    estimator = _unwrap_model(model)

    explainer = shap.Explainer(estimator, transformed)
    shap_values = explainer(transformed)

    output_path = FIGURES_DIR / f"{output_name}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    shap.summary_plot(shap_values, transformed, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path


def save_shap_local_waterfall(model: Any, X: pd.DataFrame, row_index: int = 0, output_name: str = "shap_local_waterfall") -> Path:
    """Generate a SHAP waterfall plot for one observation."""
    if shap is None:
        raise ImportError("SHAP is not installed. Install the dependency before generating SHAP outputs.")

    transformed, feature_names = _transform_features(model, X)
    estimator = _unwrap_model(model)

    explainer = shap.Explainer(estimator, transformed)
    shap_values = explainer(transformed)

    output_path = FIGURES_DIR / f"{output_name}.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure()
    shap.plots.waterfall(shap_values[row_index], show=False)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path


def run_explainability(model_name: str, model: Any, X_reference: pd.DataFrame) -> dict[str, Path]:
    """Run explainability outputs appropriate for the supplied fitted model."""
    ensure_output_dirs()
    artifacts: dict[str, Path] = {}

    estimator = _unwrap_model(model)
    lowered_name = model_name.lower()

    if "logistic" in lowered_name and hasattr(estimator, "coef_"):
        artifacts["logistic_coefficients"] = save_logistic_coefficients(model, X_reference)

    if hasattr(estimator, "feature_importances_"):
        table_path, figure_path = save_tree_feature_importance(model, X_reference, lowered_name)
        artifacts[f"{lowered_name}_importance_table"] = table_path
        artifacts[f"{lowered_name}_importance_figure"] = figure_path

    if shap is not None:
        artifacts["shap_summary"] = save_shap_summary(model, X_reference, output_name=f"{lowered_name}_shap_summary")
        artifacts["shap_local_waterfall"] = save_shap_local_waterfall(
            model,
            X_reference,
            row_index=0,
            output_name=f"{lowered_name}_shap_local_waterfall",
        )
    return artifacts

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from xgboost import XGBClassifier
except Exception:  # pragma: no cover - optional runtime dependency handling
    XGBClassifier = None


MODEL_OUTPUT_DIR = Path("outputs/models")
TARGET_COLUMN = "Churn"
RANDOM_STATE = 42


@dataclass(frozen=True)
class TrainedModel:
    name: str
    pipeline: Pipeline


def build_preprocessor(X: pd.DataFrame, scale_numeric: bool = False) -> ColumnTransformer:
    """Build a preprocessing transformer for mixed tabular data."""
    numeric_features = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = X.select_dtypes(exclude=["number", "bool"]).columns.tolist()

    numeric_steps: list[tuple[str, Any]] = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        numeric_steps.append(("scaler", StandardScaler()))

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=numeric_steps), numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )


def build_model_pipelines(X: pd.DataFrame) -> dict[str, Pipeline]:
    """Create baseline pipelines for the three selected churn models."""
    pipelines: dict[str, Pipeline] = {
        "logistic_regression": Pipeline(
            steps=[
                ("preprocess", build_preprocessor(X, scale_numeric=True)),
                ("model", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocess", build_preprocessor(X, scale_numeric=False)),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        max_depth=None,
                        min_samples_split=2,
                        min_samples_leaf=1,
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
    }

    if XGBClassifier is not None:
        pipelines["xgboost"] = Pipeline(
            steps=[
                ("preprocess", build_preprocessor(X, scale_numeric=False)),
                (
                    "model",
                    XGBClassifier(
                        n_estimators=300,
                        max_depth=4,
                        learning_rate=0.05,
                        subsample=0.9,
                        colsample_bytree=0.9,
                        objective="binary:logistic",
                        eval_metric="logloss",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        )
    return pipelines


def train_models(X_train: pd.DataFrame, y_train: pd.Series) -> dict[str, TrainedModel]:
    """Fit all configured pipelines on the provided training data."""
    trained: dict[str, TrainedModel] = {}
    for name, pipeline in build_model_pipelines(X_train).items():
        fitted = pipeline.fit(X_train, y_train)
        trained[name] = TrainedModel(name=name, pipeline=fitted)
    return trained


def save_model(model: Pipeline, model_name: str, output_dir: str | Path = MODEL_OUTPUT_DIR) -> Path:
    """Serialize a trained pipeline to disk."""
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    output_path = destination_dir / f"{model_name}.joblib"
    joblib.dump(model, output_path)
    return output_path


def split_features_target(df: pd.DataFrame, target_column: str = TARGET_COLUMN) -> tuple[pd.DataFrame, pd.Series]:
    """Split a dataframe into features and target."""
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y

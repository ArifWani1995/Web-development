from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    mean_absolute_error,
    r2_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class TrainResult:
    task_type: str
    model_name: str
    score_label: str
    score_value: float
    confusion_matrix: np.ndarray | None
    x_test: pd.DataFrame
    y_test: pd.Series
    y_pred: np.ndarray


class MLEngine:
    """Encapsulates all ML operations for the desktop app."""

    def __init__(self) -> None:
        self.dataframe: pd.DataFrame | None = None
        self.target_column: str | None = None
        self.feature_columns: list[str] = []
        self.pipeline: Pipeline | None = None
        self.result: TrainResult | None = None

    def load_csv(self, file_path: str) -> pd.DataFrame:
        self.dataframe = pd.read_csv(file_path)
        return self.dataframe

    def clean_data(self) -> pd.DataFrame:
        if self.dataframe is None:
            raise ValueError("Load a dataset first.")

        df = self.dataframe.copy()
        df.columns = [c.strip().replace(" ", "_") for c in df.columns]
        df = df.drop_duplicates().reset_index(drop=True)
        self.dataframe = df
        return df

    def infer_task_type(self, target_col: str) -> str:
        if self.dataframe is None:
            raise ValueError("Dataset missing.")
        series = self.dataframe[target_col]
        unique_count = series.nunique(dropna=True)

        if series.dtype == "object" or unique_count <= 15:
            return "classification"
        return "regression"

    def _build_model(self, model_name: str, task_type: str) -> Any:
        if task_type == "classification":
            if model_name == "Logistic Regression":
                return LogisticRegression(max_iter=1000)
            return RandomForestClassifier(n_estimators=250, random_state=42)

        return LinearRegression()

    def train_model(self, target_col: str, model_name: str) -> TrainResult:
        if self.dataframe is None:
            raise ValueError("Load and clean a dataset first.")

        self.target_column = target_col
        self.feature_columns = [c for c in self.dataframe.columns if c != target_col]

        x = self.dataframe[self.feature_columns]
        y = self.dataframe[target_col]

        task_type = self.infer_task_type(target_col)
        numeric_features = x.select_dtypes(include=[np.number]).columns.tolist()
        categorical_features = [c for c in x.columns if c not in numeric_features]

        numeric_transformer = Pipeline(
            steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
        )
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        model = self._build_model(model_name, task_type)
        self.pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y if task_type == "classification" else None,
        )

        self.pipeline.fit(x_train, y_train)
        y_pred = self.pipeline.predict(x_test)

        if task_type == "classification":
            score = accuracy_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)
            result = TrainResult(
                task_type=task_type,
                model_name=model_name,
                score_label="Accuracy",
                score_value=float(score),
                confusion_matrix=cm,
                x_test=x_test,
                y_test=y_test,
                y_pred=y_pred,
            )
        else:
            score = r2_score(y_test, y_pred)
            _ = mean_absolute_error(y_test, y_pred)
            result = TrainResult(
                task_type=task_type,
                model_name=model_name,
                score_label="R² Score",
                score_value=float(score),
                confusion_matrix=None,
                x_test=x_test,
                y_test=y_test,
                y_pred=y_pred,
            )

        self.result = result
        return result

    def predict(self, input_data: dict[str, Any]) -> Any:
        if self.pipeline is None:
            raise ValueError("Model not trained.")
        pred_df = pd.DataFrame([input_data])
        return self.pipeline.predict(pred_df)[0]

    def correlation_matrix(self) -> pd.DataFrame:
        if self.dataframe is None:
            raise ValueError("Dataset missing.")
        num_df = self.dataframe.select_dtypes(include=[np.number])
        if num_df.empty:
            raise ValueError("No numeric columns available for heatmap.")
        return num_df.corr(numeric_only=True)

    @staticmethod
    def confusion_matrix_display(cm: np.ndarray, labels: list[str]) -> ConfusionMatrixDisplay:
        return ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)

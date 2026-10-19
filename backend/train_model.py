"""Train and export the notebook's HistGradientBoosting model pipeline."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from zipfile import ZipFile

import joblib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from backend.schema import FEATURES, NUMERIC_FEATURES, COVER_TYPES

ROOT = Path(__file__).resolve().parents[1]
DATA_ZIP = ROOT / "covertype.zip"
MODEL_PATH = ROOT / "backend" / "models" / "model_bundle.joblib"
METRICS_PATH = ROOT / "docs" / "model-metrics.json"
RANDOM_STATE = 42


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    if not DATA_ZIP.exists():
        raise FileNotFoundError(f"Dataset archive not found: {DATA_ZIP}")

    columns = FEATURES + ["Cover_Type"]
    with ZipFile(DATA_ZIP) as archive:
        with archive.open("covtype.data.gz") as compressed:
            with gzip.GzipFile(fileobj=compressed) as source:
                frame = pd.read_csv(source, header=None, names=columns)
    return frame[FEATURES], frame["Cover_Type"].astype(int)


def main() -> None:
    features, target = load_training_data()
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    numeric_names = [item["name"] for item in NUMERIC_FEATURES]
    tree_preprocessor = ColumnTransformer(
        [
            ("numeric", SimpleImputer(strategy="median"), numeric_names),
            ("indicators", SimpleImputer(strategy="most_frequent"), FEATURES[10:]),
        ],
        remainder="drop",
    )
    pipeline = Pipeline(
        [
            ("preprocessor", tree_preprocessor),
            (
                "classifier",
                HistGradientBoostingClassifier(
                    max_iter=150,
                    learning_rate=0.1,
                    max_leaf_nodes=31,
                    l2_regularization=1.0,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )

    print(f"Training on {len(x_train):,} rows with {len(FEATURES)} features…", flush=True)
    pipeline.fit(x_train, y_train)
    predicted = pipeline.predict(x_test)
    metrics = {
        "model": "Histogram Gradient Boosting",
        "split": "stratified 80/20 holdout",
        "random_state": RANDOM_STATE,
        "training_rows": int(len(x_train)),
        "holdout_rows": int(len(x_test)),
        "features": len(FEATURES),
        "classes": {str(key): value for key, value in COVER_TYPES.items()},
        "accuracy": float(accuracy_score(y_test, predicted)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, predicted)),
        "macro_f1": float(f1_score(y_test, predicted, average="macro")),
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    bundle = {
        "pipeline": pipeline,
        "features": FEATURES,
        "task": "multiclass_classification",
        "model_name": "Histogram Gradient Boosting",
        "model_version": "1.0.0",
        "classes": COVER_TYPES,
        "random_state": RANDOM_STATE,
        "training_rows": int(len(x_train)),
    }
    joblib.dump(bundle, MODEL_PATH, compress=3)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    print(f"Saved model bundle to {MODEL_PATH}")


if __name__ == "__main__":
    main()

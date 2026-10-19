"""Flask JSON API for the locally hosted Covertype model."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from flask import Flask, jsonify, request

from backend.schema import (
    COVER_TYPES,
    FEATURES,
    NUMERIC_FEATURES,
    SAMPLE_INPUT,
    SOIL_FEATURES,
    WILDERNESS_FEATURES,
)

BASE = Path(__file__).resolve().parent
BUNDLE_PATH = BASE / "models" / "model_bundle.joblib"
app = Flask(__name__)


def load_bundle() -> dict[str, Any] | None:
    if not BUNDLE_PATH.is_file():
        return None
    return joblib.load(BUNDLE_PATH)


@app.get("/")
def index():
    return jsonify(
        service="Fieldnote / Forest API",
        status="ok",
        frontend="http://localhost:4200",
        endpoints={
            "health": "/health",
            "schema": "/schema",
            "predict": "POST /predict",
        },
        prediction_ready=load_bundle() is not None,
    )


@app.get("/health")
def health():
    bundle = load_bundle()
    return jsonify(
        status="ok" if bundle else "model_not_ready",
        model_loaded=bool(bundle),
        model_name=bundle.get("model_name") if bundle else None,
        features=len(FEATURES),
        classes=len(COVER_TYPES),
        task="multiclass_classification",
    )


@app.get("/schema")
def schema():
    return jsonify(
        task="multiclass_classification",
        feature_count=len(FEATURES),
        numeric_features=NUMERIC_FEATURES,
        wilderness_features=WILDERNESS_FEATURES,
        soil_features=SOIL_FEATURES,
        classes=[{"id": key, "name": name} for key, name in COVER_TYPES.items()],
        sample=SAMPLE_INPUT,
    )


def validate_payload(data: Any) -> tuple[pd.DataFrame | None, list[str]]:
    if not isinstance(data, dict):
        return None, ["Expected a JSON object containing all 54 feature values."]
    missing = [name for name in FEATURES if name not in data]
    extra = [name for name in data if name not in FEATURES]
    issues: list[str] = []
    if missing:
        issues.append(f"Missing features: {', '.join(missing)}")
    if extra:
        issues.append(f"Unexpected features: {', '.join(extra)}")
    if issues:
        return None, issues

    for definition in NUMERIC_FEATURES:
        name = definition["name"]
        value = data[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            issues.append(f"{name} must be a number.")
        elif not math.isfinite(value) or not float(value).is_integer():
            issues.append(f"{name} must be a whole number.")
        elif not definition["min"] <= value <= definition["max"]:
            issues.append(
                f"{name} must be between {definition['min']} and {definition['max']}."
            )
    for name in WILDERNESS_FEATURES + SOIL_FEATURES:
        value = data[name]
        if isinstance(value, bool):
            continue
        if value not in (0, 1):
            issues.append(f"{name} must be either 0 or 1.")
    if not issues:
        if sum(int(data[name]) for name in WILDERNESS_FEATURES) != 1:
            issues.append("Select exactly one wilderness area.")
        if sum(int(data[name]) for name in SOIL_FEATURES) != 1:
            issues.append("Select exactly one soil type.")
    if issues:
        return None, issues
    return pd.DataFrame([[data[name] for name in FEATURES]], columns=FEATURES), []


@app.post("/predict")
def predict():
    frame, issues = validate_payload(request.get_json(silent=True))
    if issues:
        return jsonify(error="Invalid input", details=issues), 400
    bundle = load_bundle()
    if bundle is None:
        return jsonify(error="Model bundle is not installed. Run python -m backend.train_model first."), 503

    try:
        model = bundle["pipeline"]
        prediction = model.predict(frame)[0]
        class_id = int(prediction)
        probabilities = model.predict_proba(frame)[0]
        probability_by_class = {
            str(int(label)): round(float(probability), 6)
            for label, probability in zip(model.classes_, probabilities)
        }
        return jsonify(
            prediction={"id": class_id, "name": COVER_TYPES[class_id]},
            probabilities=probability_by_class,
            model=bundle.get("model_name", "Covertype classifier"),
            disclaimer="Research and teaching prototype. Not a field survey or land-management recommendation.",
        )
    except (ValueError, TypeError, KeyError) as exc:
        return jsonify(error="Prediction could not be produced", details=[str(exc)]), 400
    except Exception:
        app.logger.exception("Prediction processing failed")
        return jsonify(error="Prediction processing failed"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

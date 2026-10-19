from backend.app import app
from backend.schema import FEATURES, SAMPLE_INPUT


def test_health_and_schema_explain_model_status():
    client = app.test_client()
    health = client.get("/health")
    schema = client.get("/schema")
    assert health.status_code == 200
    assert health.json["features"] == 54
    assert schema.status_code == 200
    assert schema.json["feature_count"] == 54
    assert len(schema.json["classes"]) == 7


def test_prediction_rejects_missing_or_invalid_schema():
    client = app.test_client()
    missing = client.post("/predict", json={})
    invalid = client.post("/predict", json={**SAMPLE_INPUT, "Slope": 99})
    assert missing.status_code == 400
    assert invalid.status_code == 400


def test_prediction_requires_one_of_each_indicator_group():
    client = app.test_client()
    payload = dict(SAMPLE_INPUT)
    payload["Wilderness_Area_2"] = 1
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    assert any("wilderness" in item.lower() for item in response.json["details"])


def test_payload_matches_canonical_feature_order():
    assert len(FEATURES) == 54
    assert len(SAMPLE_INPUT) == 54
    assert list(SAMPLE_INPUT) == FEATURES


def test_prediction_response_uses_model_classes_and_probabilities(monkeypatch):
    class ModelFixture:
        classes_ = [1, 2, 3, 4, 5, 6, 7]

        def predict(self, frame):
            assert list(frame.columns) == FEATURES
            return [5]

        def predict_proba(self, frame):
            return [[0.02, 0.03, 0.04, 0.05, 0.70, 0.08, 0.08]]

    monkeypatch.setattr(
        "backend.app.load_bundle",
        lambda: {"pipeline": ModelFixture(), "model_name": "Test fixture"},
    )
    response = app.test_client().post("/predict", json=SAMPLE_INPUT)
    assert response.status_code == 200
    assert response.json["prediction"] == {"id": 5, "name": "Aspen"}
    assert response.json["probabilities"]["5"] == 0.7

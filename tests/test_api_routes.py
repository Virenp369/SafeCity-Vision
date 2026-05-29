from fastapi.testclient import TestClient

from backend.api.app import app


client = TestClient(app)


def test_health_and_model_status_routes():
    health = client.get("/health")
    model_status = client.get("/models/status")

    assert health.status_code == 200
    assert model_status.status_code == 200
    assert "model_available" in health.json()
    assert "risk_model_exists" in model_status.json()


def test_data_normalize_and_quality_routes():
    records = [{
        "date": "2026-05-27",
        "lat": 28.6,
        "lon": 77.2,
        "primary_type": "THEFT",
    }]

    normalized = client.post("/data/normalize", json={"records": records})
    quality = client.post("/data/quality", json={"records": records})

    assert normalized.status_code == 200
    assert normalized.json()["records"][0]["Crime_Category"] == "THEFT"
    assert quality.status_code == 200
    assert quality.json()["quality_score"] > 0


def test_intelligence_routes(sample_records):
    endpoints = [
        ("/analytics/summary", {"records": sample_records}),
        ("/hotspots/detect", {"records": sample_records}),
        ("/alerts/evaluate", {"records": sample_records}),
        ("/forecast/crime-volume", {"records": sample_records, "horizon_days": 3}),
        ("/reports/generate", {"records": sample_records, "title": "Test", "context": "Unit"}),
        ("/anomalies/detect", {"records": sample_records, "z_threshold": 1.0, "min_count": 1}),
    ]

    for endpoint, payload in endpoints:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 200, endpoint

from backend.services.risk_service import RiskService
from ml.forecasting.anomaly_detector import AnomalyDetector


def test_risk_service_scores_late_night_transit_context():
    result = RiskService().score(hour=22, dist_to_transit=0.4, confidence=80)

    assert result["risk_score"] == 98.0
    assert result["time_context"] == "late night"
    assert result["transit_context"] == "high"


def test_anomaly_detector_flags_skewed_activity():
    records = []
    for _ in range(10):
        records.append({
            "Timestamp": "2026-05-27T22:00:00",
            "Hour": 22,
            "Crime_Category": "THEFT",
        })
    for day in range(1, 5):
        records.append({
            "Timestamp": f"2026-05-2{day}T10:00:00",
            "Hour": 10 + day,
            "Crime_Category": "ROBBERY",
        })

    result = AnomalyDetector().detect(records, z_threshold=1.0, min_count=2)

    anomaly_types = {item["type"] for item in result["anomalies"]}
    assert result["status"] == "anomalies_detected"
    assert "daily_volume" in anomaly_types
    assert "hourly_concentration" in anomaly_types

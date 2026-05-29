from typing import Any

from ml.forecasting import AnomalyDetector


class AnomalyService:
    def detect_anomalies(
        self,
        records: list[dict[str, Any]],
        z_threshold: float = 2.0,
        min_count: int = 2,
    ) -> dict[str, Any]:
        return AnomalyDetector().detect(records, z_threshold=z_threshold, min_count=min_count)

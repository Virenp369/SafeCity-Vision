from typing import Any

import pandas as pd


class AnomalyDetector:
    def detect(
        self,
        records: list[dict[str, Any]],
        z_threshold: float = 2.0,
        min_count: int = 2,
    ) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty:
            return {"anomaly_count": 0, "anomalies": [], "status": "insufficient_data"}

        anomalies = []
        anomalies.extend(self._detect_daily_volume_anomalies(df, z_threshold, min_count))
        anomalies.extend(self._detect_hourly_concentration_anomalies(df, z_threshold, min_count))
        anomalies.extend(self._detect_category_concentration_anomalies(df, z_threshold, min_count))

        anomalies = sorted(anomalies, key=lambda item: item["score"], reverse=True)
        return {
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "status": "anomalies_detected" if anomalies else "normal",
        }

    def _detect_daily_volume_anomalies(self, df: pd.DataFrame, z_threshold: float, min_count: int) -> list[dict[str, Any]]:
        if "Timestamp" not in df.columns:
            return []

        timestamps = pd.to_datetime(df["Timestamp"], errors="coerce").dropna()
        if timestamps.empty:
            return []

        counts = timestamps.dt.date.value_counts().sort_index()
        return self._series_anomalies(
            counts,
            anomaly_type="daily_volume",
            label_name="date",
            z_threshold=z_threshold,
            min_count=min_count,
        )

    def _detect_hourly_concentration_anomalies(self, df: pd.DataFrame, z_threshold: float, min_count: int) -> list[dict[str, Any]]:
        if "Hour" not in df.columns:
            return []

        hours = pd.to_numeric(df["Hour"], errors="coerce").dropna()
        if hours.empty:
            return []

        counts = hours.astype(int).value_counts().sort_index()
        return self._series_anomalies(
            counts,
            anomaly_type="hourly_concentration",
            label_name="hour",
            z_threshold=z_threshold,
            min_count=min_count,
        )

    def _detect_category_concentration_anomalies(self, df: pd.DataFrame, z_threshold: float, min_count: int) -> list[dict[str, Any]]:
        if "Crime_Category" not in df.columns:
            return []

        counts = df["Crime_Category"].dropna().astype(str).value_counts()
        return self._series_anomalies(
            counts,
            anomaly_type="category_concentration",
            label_name="category",
            z_threshold=z_threshold,
            min_count=min_count,
        )

    @staticmethod
    def _series_anomalies(
        counts: pd.Series,
        anomaly_type: str,
        label_name: str,
        z_threshold: float,
        min_count: int,
    ) -> list[dict[str, Any]]:
        if counts.empty or len(counts) < 2:
            return []

        mean = float(counts.mean())
        std = float(counts.std(ddof=0))
        if std == 0:
            return []

        anomalies = []
        for label, count in counts.items():
            count = int(count)
            z_score = (count - mean) / std
            if count >= min_count and z_score >= z_threshold:
                anomalies.append({
                    "type": anomaly_type,
                    label_name: str(label),
                    "count": count,
                    "score": round(float(z_score), 3),
                    "baseline_mean": round(mean, 3),
                    "message": f"{anomaly_type.replace('_', ' ').title()} anomaly detected for {label}.",
                })
        return anomalies

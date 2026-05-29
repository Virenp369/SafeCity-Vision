from typing import Any

import pandas as pd


class AlertService:
    def evaluate_alerts(
        self,
        records: list[dict[str, Any]],
        risk_threshold: int = 70,
        concentration_threshold: float = 0.35,
    ) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty:
            return {"alert_count": 0, "alerts": [], "overall_status": "no_data"}

        alerts = []
        night_share = self._share(df, "Hour", lambda s: (s < 5) | (s > 20))
        transit_share = self._share(df, "Dist_to_Transit", lambda s: s < 1.0)
        category_share, category = self._dominant_category_share(df)

        risk_score = min(round(30 + night_share * 30 + transit_share * 30 + category_share * 20), 100)

        if risk_score >= risk_threshold:
            alerts.append({
                "type": "risk_threshold",
                "severity": "high",
                "message": f"Overall dataset risk score reached {risk_score}/100.",
                "value": risk_score,
            })

        if night_share >= concentration_threshold:
            alerts.append({
                "type": "temporal_concentration",
                "severity": "medium",
                "message": "Late-night activity concentration exceeded threshold.",
                "value": round(float(night_share), 3),
            })

        if transit_share >= concentration_threshold:
            alerts.append({
                "type": "transit_proximity",
                "severity": "medium",
                "message": "Transit-adjacent incident concentration exceeded threshold.",
                "value": round(float(transit_share), 3),
            })

        if category and category_share >= concentration_threshold:
            alerts.append({
                "type": "category_concentration",
                "severity": "medium",
                "message": f"Incident category concentration detected for {category}.",
                "value": round(float(category_share), 3),
            })

        return {
            "alert_count": len(alerts),
            "alerts": alerts,
            "overall_status": "alert" if alerts else "normal",
            "risk_score": int(risk_score),
        }

    @staticmethod
    def _share(df: pd.DataFrame, column: str, predicate) -> float:
        if column not in df.columns:
            return 0.0
        values = pd.to_numeric(df[column], errors="coerce").dropna()
        if values.empty:
            return 0.0
        return float(predicate(values).mean())

    @staticmethod
    def _dominant_category_share(df: pd.DataFrame) -> tuple[float, str | None]:
        if "Crime_Category" not in df.columns or df["Crime_Category"].dropna().empty:
            return 0.0, None
        counts = df["Crime_Category"].astype(str).value_counts()
        category = str(counts.index[0])
        return float(counts.iloc[0] / len(df)), category

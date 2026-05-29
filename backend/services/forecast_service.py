from typing import Any

import pandas as pd


class ForecastService:
    def forecast_crime_volume(self, records: list[dict[str, Any]], horizon_days: int = 7) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty or "Timestamp" not in df.columns:
            return {"horizon_days": horizon_days, "forecast": [], "trend": "insufficient_data"}

        timestamps = pd.to_datetime(df["Timestamp"], errors="coerce").dropna()
        if timestamps.empty:
            return {"horizon_days": horizon_days, "forecast": [], "trend": "insufficient_data"}

        daily_counts = timestamps.dt.date.value_counts().sort_index()
        if daily_counts.empty:
            return {"horizon_days": horizon_days, "forecast": [], "trend": "insufficient_data"}

        baseline = float(daily_counts.tail(7).mean())
        recent = float(daily_counts.tail(3).mean())
        previous = float(daily_counts.iloc[:-3].tail(3).mean()) if len(daily_counts) > 3 else recent
        trend_delta = recent - previous
        trend = "increasing" if trend_delta > 0.5 else "decreasing" if trend_delta < -0.5 else "stable"

        start_date = pd.Timestamp(max(daily_counts.index)) + pd.Timedelta(days=1)
        forecast = []
        for day in range(horizon_days):
            projected = max(round(baseline + (trend_delta * min(day + 1, 3) / 3)), 0)
            forecast.append({
                "date": (start_date + pd.Timedelta(days=day)).strftime("%Y-%m-%d"),
                "predicted_incidents": int(projected),
            })

        return {
            "horizon_days": horizon_days,
            "trend": trend,
            "historical_daily_average": round(baseline, 2),
            "forecast": forecast,
        }

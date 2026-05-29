from typing import Any

import pandas as pd

from backend.services.data_validation_service import dataframe_to_records


class AnalyticsService:
    def summarize(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty:
            return {
                "total_records": 0,
                "unique_categories": 0,
                "top_categories": {},
                "hourly_distribution": {},
                "day_of_week_distribution": {},
                "geographic_bounds": {},
            }

        return {
            "total_records": int(len(df)),
            "unique_categories": int(df["Crime_Category"].nunique()) if "Crime_Category" in df.columns else 0,
            "top_categories": self._value_counts(df, "Crime_Category", limit=10),
            "hourly_distribution": self._value_counts(df, "Hour", limit=24),
            "day_of_week_distribution": self._value_counts(df, "DayOfWeek", limit=7),
            "geographic_bounds": self._geographic_bounds(df),
        }

    def filter_records(
        self,
        records: list[dict[str, Any]],
        categories: list[str] | None = None,
        hour_start: int | None = None,
        hour_end: int | None = None,
        limit: int = 100,
    ) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty:
            return {"total_records": 0, "returned_records": 0, "records": []}

        filtered = df.copy()
        if categories and "Crime_Category" in filtered.columns:
            filtered = filtered[filtered["Crime_Category"].astype(str).isin(categories)]

        if hour_start is not None and hour_end is not None and "Hour" in filtered.columns:
            hours = pd.to_numeric(filtered["Hour"], errors="coerce")
            filtered = filtered[hours.between(hour_start, hour_end)]

        limited = filtered.head(limit)
        return {
            "total_records": int(len(filtered)),
            "returned_records": int(len(limited)),
            "records": dataframe_to_records(limited),
        }

    @staticmethod
    def _value_counts(df: pd.DataFrame, column: str, limit: int) -> dict[str, int]:
        if column not in df.columns:
            return {}
        return {
            str(key): int(value)
            for key, value in df[column].value_counts().head(limit).to_dict().items()
        }

    @staticmethod
    def _geographic_bounds(df: pd.DataFrame) -> dict[str, float]:
        if not {"Latitude", "Longitude"}.issubset(df.columns):
            return {}

        lat = pd.to_numeric(df["Latitude"], errors="coerce").dropna()
        lon = pd.to_numeric(df["Longitude"], errors="coerce").dropna()
        if lat.empty or lon.empty:
            return {}

        return {
            "min_latitude": float(lat.min()),
            "max_latitude": float(lat.max()),
            "min_longitude": float(lon.min()),
            "max_longitude": float(lon.max()),
        }

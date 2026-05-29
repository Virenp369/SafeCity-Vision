from typing import Any

import pandas as pd


class HotspotService:
    def detect_hotspots(
        self,
        records: list[dict[str, Any]],
        precision: int = 3,
        min_count: int = 1,
        limit: int = 20,
    ) -> dict[str, Any]:
        df = pd.DataFrame.from_records(records)
        if df.empty or not {"Latitude", "Longitude"}.issubset(df.columns):
            return {"total_hotspots": 0, "hotspots": []}

        working = df.copy()
        working["Latitude"] = pd.to_numeric(working["Latitude"], errors="coerce")
        working["Longitude"] = pd.to_numeric(working["Longitude"], errors="coerce")
        working = working.dropna(subset=["Latitude", "Longitude"])
        if working.empty:
            return {"total_hotspots": 0, "hotspots": []}

        working["lat_bucket"] = working["Latitude"].round(precision)
        working["lon_bucket"] = working["Longitude"].round(precision)

        hotspots = []
        grouped = working.groupby(["lat_bucket", "lon_bucket"], dropna=True)
        for (lat_bucket, lon_bucket), group in grouped:
            count = int(len(group))
            if count < min_count:
                continue

            dominant_category = None
            if "Crime_Category" in group.columns and not group["Crime_Category"].dropna().empty:
                dominant_category = str(group["Crime_Category"].mode().iat[0])

            hotspots.append({
                "latitude": float(group["Latitude"].mean()),
                "longitude": float(group["Longitude"].mean()),
                "bucket": {"latitude": float(lat_bucket), "longitude": float(lon_bucket)},
                "incident_count": count,
                "dominant_category": dominant_category,
            })

        hotspots = sorted(hotspots, key=lambda item: item["incident_count"], reverse=True)[:limit]
        return {"total_hotspots": len(hotspots), "hotspots": hotspots}

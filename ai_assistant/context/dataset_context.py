from typing import Any

import pandas as pd


def build_dataset_context(records: list[dict[str, Any]], provided_summary: str | None = None) -> str:
    if provided_summary:
        return provided_summary

    df = pd.DataFrame.from_records(records)
    if df.empty:
        return "No dataset records were provided."

    parts = [f"Total Records Analyzed: {len(df)}"]

    if "Crime_Category" in df.columns:
        parts.append(f"Top Crime Categories: {df['Crime_Category'].value_counts().head(5).to_dict()}")

    if "City" in df.columns:
        parts.append(f"Top Locations: {df['City'].value_counts().head(5).to_dict()}")

    numeric_cols = [column for column in ["Hour", "DayOfWeek", "Dist_to_Transit", "Latitude", "Longitude"] if column in df.columns]
    if numeric_cols:
        parts.append("Numeric Tactical Summary:\n" + df[numeric_cols].describe().to_string())

    return "\n".join(parts)

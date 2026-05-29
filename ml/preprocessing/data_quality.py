from typing import Any

import pandas as pd

from ml.preprocessing.schema_normalizer import REQUIRED_CANONICAL_COLUMNS, required_missing_columns


def build_quality_report(df: pd.DataFrame) -> dict[str, Any]:
    if df.empty:
        return {
            "total_records": 0,
            "missing_columns": REQUIRED_CANONICAL_COLUMNS,
            "duplicate_records": 0,
            "null_counts": {},
            "invalid_timestamp_records": 0,
            "invalid_coordinate_records": 0,
            "out_of_range_coordinate_records": 0,
            "quality_score": 0,
        }

    missing_columns = required_missing_columns(df)
    null_counts = {column: int(value) for column, value in df.isna().sum().to_dict().items()}
    duplicate_records = int(df.duplicated().sum())

    invalid_timestamp_records = 0
    if "Timestamp" in df.columns:
        invalid_timestamp_records = int(pd.to_datetime(df["Timestamp"], errors="coerce").isna().sum())

    invalid_coordinate_records = 0
    out_of_range_coordinate_records = 0
    if {"Latitude", "Longitude"}.issubset(df.columns):
        lat = pd.to_numeric(df["Latitude"], errors="coerce")
        lon = pd.to_numeric(df["Longitude"], errors="coerce")
        invalid_coordinate_records = int((lat.isna() | lon.isna()).sum())
        out_of_range_coordinate_records = int((~lat.between(-90, 90) | ~lon.between(-180, 180)).sum())

    penalties = (
        len(missing_columns) * 20
        + duplicate_records
        + invalid_timestamp_records * 2
        + invalid_coordinate_records * 3
        + out_of_range_coordinate_records * 4
    )
    quality_score = max(100 - penalties, 0)

    return {
        "total_records": int(len(df)),
        "missing_columns": missing_columns,
        "duplicate_records": duplicate_records,
        "null_counts": null_counts,
        "invalid_timestamp_records": invalid_timestamp_records,
        "invalid_coordinate_records": invalid_coordinate_records,
        "out_of_range_coordinate_records": out_of_range_coordinate_records,
        "quality_score": int(quality_score),
    }

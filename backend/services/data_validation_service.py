from typing import Any

import pandas as pd

from ml.preprocessing.feature_enricher import DataEnricher
from ml.preprocessing.data_quality import build_quality_report
from ml.preprocessing.schema_normalizer import normalize_crime_schema, required_missing_columns


REQUIRED_DATASET_COLUMNS = ["Timestamp", "Latitude", "Longitude", "Crime_Category"]


class DataValidationService:
    def to_dataframe(self, records: list[dict[str, Any]]) -> pd.DataFrame:
        return pd.DataFrame.from_records(records)

    def validate_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        df = self.to_dataframe(records)
        if df.empty:
            return {
                "valid": False,
                "total_records": 0,
                "missing_columns": REQUIRED_DATASET_COLUMNS,
                "invalid_timestamp_records": 0,
                "invalid_coordinate_records": 0,
                "message": "Dataset is empty.",
            }

        try:
            df = normalize_crime_schema(df)
            missing_columns = []
        except ValueError:
            missing_columns = required_missing_columns(df)

        invalid_timestamp_records = 0
        invalid_coordinate_records = 0

        if "Timestamp" in df.columns:
            invalid_timestamp_records = int(pd.to_datetime(df["Timestamp"], errors="coerce").isna().sum())

        if {"Latitude", "Longitude"}.issubset(df.columns):
            lat = pd.to_numeric(df["Latitude"], errors="coerce")
            lon = pd.to_numeric(df["Longitude"], errors="coerce")
            invalid_coordinate_records = int((lat.isna() | lon.isna()).sum())

        valid = not missing_columns and invalid_timestamp_records == 0 and invalid_coordinate_records == 0
        return {
            "valid": valid,
            "total_records": int(len(df)),
            "missing_columns": missing_columns,
            "invalid_timestamp_records": invalid_timestamp_records,
            "invalid_coordinate_records": invalid_coordinate_records,
            "message": "Dataset is valid." if valid else "Dataset requires cleaning before production use.",
        }

    def normalize_records(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        df = self.to_dataframe(records)
        normalized = normalize_crime_schema(df)
        return dataframe_to_records(normalized)

    def quality_report(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        df = self.to_dataframe(records)
        try:
            df = normalize_crime_schema(df)
        except ValueError:
            pass
        return build_quality_report(df)

    def enrich_records(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        df = self.to_dataframe(records)
        enriched = DataEnricher().enrich(df)
        return dataframe_to_records(enriched)


def dataframe_to_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    output = df.copy()
    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(output[column]):
            output[column] = output[column].dt.strftime("%Y-%m-%dT%H:%M:%S")
    output = output.where(pd.notnull(output), None)
    return output.to_dict(orient="records")

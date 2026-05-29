import pandas as pd
import pytest

from ml.preprocessing.data_quality import build_quality_report
from ml.preprocessing.schema_normalizer import normalize_crime_schema


def test_normalize_crime_schema_maps_common_aliases():
    raw = pd.DataFrame([{
        "date": "2026-05-27",
        "lat": 28.6,
        "lon": 77.2,
        "primary_type": "THEFT",
    }])

    normalized = normalize_crime_schema(raw)

    assert list(normalized.columns) == [
        "Timestamp",
        "Latitude",
        "Longitude",
        "Crime_Category",
        "Description",
    ]
    assert normalized.iloc[0]["Crime_Category"] == "THEFT"
    assert normalized.iloc[0]["Description"] == "THEFT"


def test_normalize_crime_schema_rejects_missing_required_columns():
    raw = pd.DataFrame([{"date": "2026-05-27", "lat": 28.6}])

    with pytest.raises(ValueError):
        normalize_crime_schema(raw)


def test_quality_report_detects_invalid_values_after_normalization():
    raw = pd.DataFrame([
        {"date": "bad-date", "lat": "x", "lon": 77.2, "primary_type": "THEFT"},
    ])
    normalized = normalize_crime_schema(raw)

    report = build_quality_report(normalized)

    assert report["missing_columns"] == []
    assert report["invalid_timestamp_records"] == 1
    assert report["invalid_coordinate_records"] == 1

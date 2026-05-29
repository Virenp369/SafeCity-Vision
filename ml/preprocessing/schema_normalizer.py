import pandas as pd


CANONICAL_ALIASES = {
    "Timestamp": ["timestamp", "date", "datetime", "incident_date", "crime_date"],
    "Latitude": ["latitude", "lat", "y"],
    "Longitude": ["longitude", "lon", "lng", "x"],
    "Crime_Category": ["crime_category", "primary_type", "category", "crime_type", "offense", "ofns_desc"],
    "Description": ["description", "details", "pd_desc", "crm_cd_desc"],
    "City": ["city", "district", "area", "location"],
}

REQUIRED_CANONICAL_COLUMNS = ["Timestamp", "Latitude", "Longitude", "Crime_Category"]
DEFAULT_KEEP_COLUMNS = ["Timestamp", "City", "Latitude", "Longitude", "Crime_Category", "Description"]


def normalize_crime_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    normalized = df.copy()
    column_lookup = {column.lower().strip().replace(" ", "_"): column for column in normalized.columns}

    rename_map = {}
    for canonical, possible_names in CANONICAL_ALIASES.items():
        for name in possible_names:
            if name in column_lookup:
                rename_map[column_lookup[name]] = canonical
                break

    normalized = normalized.rename(columns=rename_map)
    missing = required_missing_columns(normalized)
    if missing:
        raise ValueError(f"CSV missing required columns: {', '.join(missing)}")

    if "Description" not in normalized.columns:
        normalized["Description"] = normalized["Crime_Category"].astype(str)

    keep_cols = [column for column in DEFAULT_KEEP_COLUMNS if column in normalized.columns]
    return normalized[keep_cols]


def required_missing_columns(df: pd.DataFrame) -> list[str]:
    return [column for column in REQUIRED_CANONICAL_COLUMNS if column not in df.columns]

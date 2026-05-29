import pandas as pd


def risk_score(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    night_share = _series_share(df, "Hour", lambda s: (s < 5) | (s > 20))
    transit_share = _series_share(df, "Dist_to_Transit", lambda s: s < 1.0)
    category_pressure = min(df.get("Crime_Category", pd.Series(dtype=str)).nunique() / 12, 1.0)

    score = 28 + (night_share * 32) + (transit_share * 28) + (category_pressure * 12)
    return int(min(round(score), 100))


def risk_band(score: int) -> tuple[str, str]:
    if score >= 75:
        return "Critical", "#EF4444"
    if score >= 55:
        return "Elevated", "#F59E0B"
    return "Controlled", "#10B981"


def generate_operational_summary(df: pd.DataFrame, context: str) -> str:
    if df.empty:
        return "No active records are loaded. Initialize an uplink or upload a CSV to begin analysis."

    primary = _safe_mode(df, "Crime_Category", "Unknown threat")
    location = _safe_mode(df, "City", "mapped coordinates")
    peak_hour = _safe_mode(df, "Hour", "unknown hour")
    score = risk_score(df)
    band, _ = risk_band(score)

    if "INDIA" in context:
        area_text = f"Primary reporting hub is {location}"
    else:
        area_text = "Primary activity is concentrated around the displayed coordinate clusters"

    return (
        f"{band} operating posture with risk score {score}/100. "
        f"{area_text}; dominant incident class is {primary}, with peak activity around hour {peak_hour}."
    )


def top_recommendations(df: pd.DataFrame) -> list[str]:
    if df.empty:
        return ["Load a dataset to activate tactical recommendations."]

    recommendations = []
    if _series_share(df, "Hour", lambda s: (s < 5) | (s > 20)) > 0.25:
        recommendations.append("Prioritize late-night patrol visibility around recurring clusters.")
    if _series_share(df, "Dist_to_Transit", lambda s: s < 1.0) > 0.35:
        recommendations.append("Increase monitoring near transit-adjacent hotspots during shift changes.")
    if "Crime_Category" in df.columns:
        primary = _safe_mode(df, "Crime_Category", "high-frequency incidents")
        recommendations.append(f"Prepare prevention playbooks for {primary}.")

    return recommendations[:3] or ["Maintain baseline monitoring and continue data collection."]


def filter_data(df: pd.DataFrame, categories: list[str] | None, hour_range: tuple[int, int] | None) -> pd.DataFrame:
    filtered = df.copy()
    if categories and "Crime_Category" in filtered.columns:
        filtered = filtered[filtered["Crime_Category"].isin(categories)]
    if hour_range and "Hour" in filtered.columns:
        filtered = filtered[filtered["Hour"].between(hour_range[0], hour_range[1])]
    return filtered


def _safe_mode(df: pd.DataFrame, column: str, fallback):
    if column not in df.columns or df[column].dropna().empty:
        return fallback
    return df[column].mode().iat[0]


def _series_share(df: pd.DataFrame, column: str, predicate) -> float:
    if column not in df.columns or df[column].dropna().empty:
        return 0.0
    series = pd.to_numeric(df[column], errors="coerce").dropna()
    if series.empty:
        return 0.0
    return float(predicate(series).mean())

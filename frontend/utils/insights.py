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


def classify_intent(query: str) -> str:
    query = query.lower().strip()
    
    greeting_keywords = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon", "greetings"]
    general_conv_keywords = ["who are you", "what can you do", "thank you", "thanks", "how are you"]
    general_knowledge_keywords = ["tell me about", "what is", "explain", "who is", "criminology", "ipc", "law", "regulation", "international", "compare", "difference", "history", "crime rate in", "crime in"]
    crime_data_keywords = ["top crime", "incident count", "how many", "hotspot", "count", "statistic", "number of", "dataset", "loaded data"]
    crime_analysis_keywords = ["dominant threat", "trend", "risk", "pattern", "predict", "forecast", "analyze", "analysis", "recommend", "insight"]
    local_keywords = ["here", "current dataset", "this dataset"] 
    
    if any(query == g or query.startswith(g + " ") or query.startswith(g + "!") or query.startswith(g + ",") for g in greeting_keywords):
        if len(query.split()) <= 3:
            return "GREETING"
            
    if any(k in query for k in general_conv_keywords):
        return "GENERAL_CONVERSATION"

    has_data = any(k in query for k in crime_data_keywords)
    has_analysis = any(k in query for k in crime_analysis_keywords)
    has_general_knowledge = any(k in query for k in general_knowledge_keywords)
    has_local = any(k in query for k in local_keywords)
    
    if (has_data or has_analysis or has_local) and has_general_knowledge:
        return "HYBRID_QUERY"
        
    if has_general_knowledge:
        return "GENERAL_KNOWLEDGE"
        
    if has_analysis:
        return "CRIME_ANALYSIS"
        
    if has_data or has_local:
        return "CRIME_DATA_QUERY"
        
    return "GENERAL_KNOWLEDGE"


def generate_local_intelligence(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data available for intelligence generation."
    
    primary = _safe_mode(df, "Crime_Category", "Unknown threat")
    location = _safe_mode(df, "City", "mapped coordinates")
    
    score = risk_score(df)
    band, _ = risk_band(score)
    
    recs = top_recommendations(df)
    recs_text = "\n".join(f"- {r}" for r in recs)
    
    top_crimes = df['Crime_Category'].value_counts().head(2) if 'Crime_Category' in df.columns else pd.Series()
    crime_details = " and ".join([f"{k.lower()} ({v} incidents)" for k, v in top_crimes.items()])
    
    if not crime_details:
        crime_details = "various offenses"

    return f"""### Threat Assessment
Analysis of crime patterns in {location} suggests that {crime_details} remain the most significant public safety concerns. These offenses account for a large share of reported incidents and indicate elevated risks in densely populated and commercial areas.

### Key Findings
Dominant incident class is {primary}. Statistical modeling indicates significant clustering around peak operational hours.

### Risk Level
{band} operating posture with risk score {score}/100.

### Recommended Action
{recs_text}"""

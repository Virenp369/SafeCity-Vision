def build_prediction_explanation(hour: int, dist_to_transit: float) -> tuple[str, str, str]:
    time_context = "late night" if (hour < 5 or hour > 20) else "daytime"
    transit_context = "high" if dist_to_transit < 1.0 else "moderate"
    explanation = (
        f"Elevated risk flagged by AI due to {time_context} temporal alignment "
        f"and {transit_context} proximity to transit nodes."
    )
    return explanation, time_context, transit_context


def calculate_risk_score(confidence: float, time_context: str, transit_context: str) -> float:
    base_risk = 30
    if time_context == "late night":
        base_risk += 35
    if transit_context == "high":
        base_risk += 25
    return min(base_risk + (confidence * 0.1), 100.0)

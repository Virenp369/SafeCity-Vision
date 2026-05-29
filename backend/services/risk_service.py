from typing import Any

from ml.inference.risk_scoring import build_prediction_explanation, calculate_risk_score


class RiskService:
    def score(self, hour: int, dist_to_transit: float, confidence: float) -> dict[str, Any]:
        explanation, time_context, transit_context = build_prediction_explanation(hour, dist_to_transit)
        score = calculate_risk_score(confidence, time_context, transit_context)
        return {
            "risk_score": round(float(score), 1),
            "time_context": time_context,
            "transit_context": transit_context,
            "explanation": explanation,
        }

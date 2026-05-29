from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from backend.api.routes.health import get_model_service
from backend.api.schemas.risk import RiskPredictionRequest
from backend.services.model_service import ModelService

router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("/risk")
def predict_risk(
    payload: RiskPredictionRequest,
    service: ModelService = Depends(get_model_service),
) -> dict[str, Any]:
    if not service.artifacts_available(payload.session_id):
        raise HTTPException(status_code=503, detail="Model artifacts are not available for this session. Train a model first.")

    result = service.predict_risk(payload)
    if result["prediction"] == "ERROR":
        raise HTTPException(status_code=500, detail=result["explanation"])
    return result

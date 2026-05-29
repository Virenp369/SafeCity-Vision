from typing import Any
from fastapi import APIRouter, Depends, HTTPException

from backend.api.routes.health import get_model_service
from backend.services.model_service import ModelService
from backend.api.schemas.risk import ModelTrainRequest

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/status")
def model_status(session_id: str = "default", service: ModelService = Depends(get_model_service)) -> dict[str, Any]:
    return service.model_status(session_id)

@router.post("/train")
def train_model(
    payload: ModelTrainRequest,
    service: ModelService = Depends(get_model_service)
) -> dict[str, Any]:
    try:
        success = service.train_model(payload.session_id, payload.model_type)
        if not success:
            raise HTTPException(status_code=500, detail="Training failed.")
        return {"status": "success", "model": payload.model_type, "session_id": payload.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cluster")
def cluster_hotspots(
    payload: ModelTrainRequest,
    service: ModelService = Depends(get_model_service)
) -> dict[str, Any]:
    try:
        return service.cluster_hotspots(payload.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import AnomalyDetectionRequest
from backend.services.anomaly_service import AnomalyService


router = APIRouter(prefix="/anomalies", tags=["anomalies"])


def get_anomaly_service() -> AnomalyService:
    return AnomalyService()


@router.post("/detect")
def detect_anomalies(
    payload: AnomalyDetectionRequest,
    service: AnomalyService = Depends(get_anomaly_service),
) -> dict[str, Any]:
    return service.detect_anomalies(
        records=payload.records,
        z_threshold=payload.z_threshold,
        min_count=payload.min_count,
    )

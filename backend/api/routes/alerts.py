from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import AlertEvaluationRequest
from backend.services.alert_service import AlertService


router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_alert_service() -> AlertService:
    return AlertService()


@router.post("/evaluate")
def evaluate_alerts(
    payload: AlertEvaluationRequest,
    service: AlertService = Depends(get_alert_service),
) -> dict[str, Any]:
    return service.evaluate_alerts(
        records=payload.records,
        risk_threshold=payload.risk_threshold,
        concentration_threshold=payload.concentration_threshold,
    )

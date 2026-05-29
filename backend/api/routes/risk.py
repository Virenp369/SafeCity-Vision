from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import RiskScoreRequest
from backend.services.risk_service import RiskService


router = APIRouter(prefix="/risk", tags=["risk"])


def get_risk_service() -> RiskService:
    return RiskService()


@router.post("/score")
def score_risk(
    payload: RiskScoreRequest,
    service: RiskService = Depends(get_risk_service),
) -> dict[str, Any]:
    return service.score(
        hour=payload.hour,
        dist_to_transit=payload.dist_to_transit,
        confidence=payload.confidence,
    )

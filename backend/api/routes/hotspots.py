from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import HotspotDetectionRequest
from backend.services.hotspot_service import HotspotService


router = APIRouter(prefix="/hotspots", tags=["hotspots"])


def get_hotspot_service() -> HotspotService:
    return HotspotService()


@router.post("/detect")
def detect_hotspots(
    payload: HotspotDetectionRequest,
    service: HotspotService = Depends(get_hotspot_service),
) -> dict[str, Any]:
    return service.detect_hotspots(
        records=payload.records,
        precision=payload.precision,
        min_count=payload.min_count,
        limit=payload.limit,
    )

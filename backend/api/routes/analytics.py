from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import DatasetFilterRequest, DatasetRequest
from backend.services.analytics_service import AnalyticsService


router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_analytics_service() -> AnalyticsService:
    return AnalyticsService()


@router.post("/summary")
def analytics_summary(
    payload: DatasetRequest,
    service: AnalyticsService = Depends(get_analytics_service),
) -> dict[str, Any]:
    return service.summarize(payload.records)


@router.post("/filter")
def filter_dataset(
    payload: DatasetFilterRequest,
    service: AnalyticsService = Depends(get_analytics_service),
) -> dict[str, Any]:
    return service.filter_records(
        records=payload.records,
        categories=payload.categories,
        hour_start=payload.hour_start,
        hour_end=payload.hour_end,
        limit=payload.limit,
    )

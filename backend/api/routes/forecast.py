from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import ForecastRequest
from backend.services.forecast_service import ForecastService


router = APIRouter(prefix="/forecast", tags=["forecast"])


def get_forecast_service() -> ForecastService:
    return ForecastService()


@router.post("/crime-volume")
def forecast_crime_volume(
    payload: ForecastRequest,
    service: ForecastService = Depends(get_forecast_service),
) -> dict[str, Any]:
    return service.forecast_crime_volume(records=payload.records, horizon_days=payload.horizon_days)

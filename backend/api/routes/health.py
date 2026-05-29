from typing import Any

from fastapi import APIRouter, Depends

from backend.services.model_service import ModelService


router = APIRouter(tags=["health"])


def get_model_service() -> ModelService:
    return ModelService()


@router.get("/health")
def health(service: ModelService = Depends(get_model_service)) -> dict[str, Any]:
    return service.health_status()

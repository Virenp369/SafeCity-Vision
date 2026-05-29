from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from backend.api.schemas.dataset import DatasetRequest
from backend.services.data_validation_service import DataValidationService


router = APIRouter(prefix="/data", tags=["data"])


def get_data_validation_service() -> DataValidationService:
    return DataValidationService()


@router.post("/validate")
def validate_dataset(
    payload: DatasetRequest,
    service: DataValidationService = Depends(get_data_validation_service),
) -> dict[str, Any]:
    return service.validate_records(payload.records)


@router.post("/normalize")
def normalize_dataset(
    payload: DatasetRequest,
    service: DataValidationService = Depends(get_data_validation_service),
) -> dict[str, Any]:
    try:
        records = service.normalize_records(payload.records)
        return {"total_records": len(records), "records": records}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/quality")
def dataset_quality(
    payload: DatasetRequest,
    service: DataValidationService = Depends(get_data_validation_service),
) -> dict[str, Any]:
    return service.quality_report(payload.records)


@router.post("/enrich")
def enrich_dataset(
    payload: DatasetRequest,
    service: DataValidationService = Depends(get_data_validation_service),
) -> dict[str, Any]:
    try:
        records = service.enrich_records(payload.records)
        return {"total_records": len(records), "records": records}
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

from typing import Any

from fastapi import APIRouter, Depends

from backend.api.schemas.dataset import ReportGenerationRequest
from backend.services.report_service import ReportService


router = APIRouter(prefix="/reports", tags=["reports"])


def get_report_service() -> ReportService:
    return ReportService()


@router.post("/generate")
def generate_report(
    payload: ReportGenerationRequest,
    service: ReportService = Depends(get_report_service),
) -> dict[str, Any]:
    return service.generate_report(records=payload.records, title=payload.title, context=payload.context)

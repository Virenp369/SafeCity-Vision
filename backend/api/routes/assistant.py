from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from backend.api.schemas.assistant import AssistantQueryRequest
from backend.services.assistant_service import AssistantService


router = APIRouter(prefix="/assistant", tags=["assistant"])


def get_assistant_service() -> AssistantService:
    return AssistantService()


@router.post("/query")
def query_assistant(
    payload: AssistantQueryRequest,
    service: AssistantService = Depends(get_assistant_service),
) -> dict[str, Any]:
    try:
        return service.query(
            question=payload.question,
            records=payload.records,
            data_summary=payload.data_summary,
            chat_history=[message.model_dump() for message in payload.chat_history],
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

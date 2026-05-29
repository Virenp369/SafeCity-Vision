from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"] = "user"
    content: str = Field(..., min_length=1)


class AssistantQueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    records: list[dict[str, Any]] = Field(default_factory=list)
    data_summary: str | None = None
    chat_history: list[ChatMessage] = Field(default_factory=list)

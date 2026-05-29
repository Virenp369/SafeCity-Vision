from typing import Any
import logging

from ai_assistant.context import build_dataset_context
from ai_assistant.integrations.forensic_assistant import ForensicAssistant
from backend.config.settings import Settings, get_settings


logger = logging.getLogger(__name__)


class AssistantService:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def query(
        self,
        question: str,
        records: list[dict[str, Any]],
        data_summary: str | None = None,
        chat_history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        if not self.settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is missing. Add it to .env before using AI assistant APIs.")

        context = build_dataset_context(records, data_summary)
        assistant = ForensicAssistant(self.settings.gemini_api_key)
        answer = assistant.ask_question(question, context, chat_history or [])
        return {
            "answer": answer,
            "model": self.settings.gemini_model,
            "records_analyzed": len(records),
        }

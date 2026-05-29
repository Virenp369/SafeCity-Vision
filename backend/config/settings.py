from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = "SafeCity Vision API"
    app_description: str = "Model-serving and health API for forensic crime analytics."
    app_version: str = "0.2.0"
    environment: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    project_root: Path = PROJECT_ROOT
    model_path: Path = PROJECT_ROOT / "ml" / "models" / "risk_model.pkl"
    encoder_path: Path = PROJECT_ROOT / "ml" / "models" / "label_encoder.pkl"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

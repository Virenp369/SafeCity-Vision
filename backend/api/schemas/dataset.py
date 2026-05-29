from typing import Any

from pydantic import BaseModel, Field


class DatasetRequest(BaseModel):
    records: list[dict[str, Any]] = Field(default_factory=list)


class DatasetFilterRequest(DatasetRequest):
    categories: list[str] | None = None
    hour_start: int | None = Field(default=None, ge=0, le=23)
    hour_end: int | None = Field(default=None, ge=0, le=23)
    limit: int = Field(default=100, ge=1, le=1000)


class RiskScoreRequest(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    dist_to_transit: float = Field(1.0, ge=0, le=50)
    confidence: float = Field(50.0, ge=0, le=100)


class HotspotDetectionRequest(DatasetRequest):
    precision: int = Field(default=3, ge=1, le=6)
    min_count: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=200)


class AlertEvaluationRequest(DatasetRequest):
    risk_threshold: int = Field(default=70, ge=0, le=100)
    concentration_threshold: float = Field(default=0.35, ge=0, le=1)


class ForecastRequest(DatasetRequest):
    horizon_days: int = Field(default=7, ge=1, le=30)


class ReportGenerationRequest(DatasetRequest):
    title: str = "SafeCity Vision Intelligence Report"
    context: str = "Operational dataset"


class AnomalyDetectionRequest(DatasetRequest):
    z_threshold: float = Field(default=2.0, ge=0.5, le=5.0)
    min_count: int = Field(default=2, ge=1)

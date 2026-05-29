from pydantic import BaseModel, Field

class RiskPredictionRequest(BaseModel):
    session_id: str = Field("default")
    hour: int = Field(..., ge=0, le=23)
    day_of_week: int = Field(..., ge=0, le=6)
    temperature: float = Field(25.0, ge=-50, le=60)
    is_raining: int = Field(0, ge=0, le=1)
    dist_to_transit: float = Field(1.0, ge=0, le=50)

class ModelTrainRequest(BaseModel):
    session_id: str
    model_type: str = "XGBoost"

from typing import Any
import logging
import pandas as pd
import os

from backend.config.settings import Settings, get_settings
from ml.training.model_trainer import ModelTrainer

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()

    def health_status(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "model_available": True,
            "encoder_available": True,
        }

    def model_status(self, session_id: str = "default") -> dict[str, Any]:
        return {
            "risk_model": f"risk_model_{session_id}.pkl",
            "risk_model_exists": self.artifacts_available(session_id),
            "label_encoder_exists": self.artifacts_available(session_id),
        }

    def artifacts_available(self, session_id: str = "default") -> bool:
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../ml/models/risk_model_{session_id}.pkl'))
        return os.path.exists(model_path)

    def train_model(self, session_id: str, model_type: str) -> bool:
        parquet_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../data/processed/session_{session_id}.parquet'))
        if not os.path.exists(parquet_path):
            logger.error(f"Dataset for session {session_id} not found at {parquet_path}")
            raise FileNotFoundError(f"Dataset for session {session_id} not found.")
        
        df = pd.read_parquet(parquet_path)
        trainer = ModelTrainer(model_type=model_type, session_id=session_id)
        return trainer.train(df, model_type=model_type)

    def cluster_hotspots(self, session_id: str) -> dict[str, Any]:
        parquet_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../data/processed/session_{session_id}.parquet'))
        if not os.path.exists(parquet_path):
            raise FileNotFoundError(f"Dataset for session {session_id} not found.")
        
        df = pd.read_parquet(parquet_path)
        trainer = ModelTrainer(model_type="KMeans", session_id=session_id)
        df_clustered = trainer.cluster_hotspots(df)
        
        display_cols = [column for column in ['Crime_Category', 'Latitude', 'Longitude', 'Cluster'] if column in df_clustered.columns]
        return {"records": df_clustered[display_cols].head(20).to_dict(orient="records")}

    def predict_risk(self, payload) -> dict[str, Any]:
        input_features = pd.DataFrame([{
            "Hour": payload.hour,
            "DayOfWeek": payload.day_of_week,
            "Temperature": payload.temperature,
            "Is_Raining": payload.is_raining,
            "Dist_to_Transit": payload.dist_to_transit,
        }])

        result = ModelTrainer(session_id=payload.session_id).predict(input_features)
        if result.get("prediction") == "ERROR":
            logger.error("Risk prediction failed: %s", result.get("explanation"))
        return result

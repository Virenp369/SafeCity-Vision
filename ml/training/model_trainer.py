import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
import joblib
import os
import logging

from ml.clustering.hotspot_detector import HotspotDetector, select_clustering_features
from ml.inference.prediction_service import PREDICTION_FEATURES, PredictionService
from ml.preprocessing.schema_validator import validate_columns
from ml.training.model_factory import create_model

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, model_type="XGBoost", session_id="default"):
        self.session_id = session_id
        # Use UUID-based paths to prevent multi-user collisions
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../models/risk_model_{session_id}.pkl'))
        self.encoder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../models/label_encoder_{session_id}.pkl'))
        self.le = LabelEncoder()
        self.model = create_model(model_type)

    def train(self, df, model_type="XGBoost"):
        logger.info(f"Training {model_type} Model (Session: {self.session_id})...")
        try:
            df = df.copy()
            if model_type == "KMeans":
                features = select_clustering_features(df)
                validate_columns(df, features)
                
                # CRITICAL FIX: Drop NA geospatial coordinates instead of filling with 0
                if 'Latitude' in df.columns and 'Longitude' in df.columns:
                    df = df.dropna(subset=['Latitude', 'Longitude'])
                    
                if len(df) == 0:
                    raise ValueError("No valid geospatial data available for clustering after cleaning.")

                X_cluster = df[features].fillna(df[features].median(numeric_only=True)).fillna(0)
                self.model.set_params(n_clusters=min(5, len(X_cluster)))
                self.model.fit(X_cluster)
            else:
                features = PREDICTION_FEATURES
                validate_columns(df, features + ['Crime_Category'])
                
                # Use median imputation instead of blind zero-filling
                X = df[features].fillna(df[features].median(numeric_only=True)).fillna(0)
                y = self.le.fit_transform(df['Crime_Category'].fillna("Unknown"))

                if model_type == "XGBoost":
                    sample_weights = compute_sample_weight('balanced', y)
                    self.model.fit(X, y, sample_weight=sample_weights)
                else:
                    self.model.fit(X, y)
                
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.le, self.encoder_path)
            return True
        except Exception as e:
            logger.error(f"Failed to train model: {e}")
            return False

    def predict(self, input_features):
        return PredictionService(self.model_path, self.encoder_path).predict(input_features)

    def cluster_hotspots(self, df):
        return HotspotDetector(self.model_path).cluster_hotspots(df)

    @staticmethod
    def _validate_columns(df, columns):
        validate_columns(df, columns)

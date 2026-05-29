import logging
import os
import threading

import joblib
import numpy as np

from ml.inference.risk_scoring import build_prediction_explanation, calculate_risk_score
from ml.preprocessing.schema_validator import validate_columns


logger = logging.getLogger(__name__)
PREDICTION_FEATURES = ['Hour', 'DayOfWeek', 'Temperature', 'Is_Raining', 'Dist_to_Transit']


class PredictionService:
    _model_cache = {}
    _encoder_cache = {}
    _lock = threading.Lock()

    def __init__(self, model_path: str, encoder_path: str):
        self.model_path = model_path
        self.encoder_path = encoder_path

    def _get_model(self):
        with self._lock:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model not found at {self.model_path}")
                
            mtime = os.path.getmtime(self.model_path)
            cached = self._model_cache.get(self.model_path)
            if cached is None or cached['mtime'] < mtime:
                logger.info(f"Loading ML model into memory from {self.model_path}")
                model = joblib.load(self.model_path)
                self._model_cache[self.model_path] = {'model': model, 'mtime': mtime}
            return self._model_cache[self.model_path]['model']

    def _get_encoder(self):
        with self._lock:
            if not os.path.exists(self.encoder_path):
                raise FileNotFoundError(f"Encoder not found at {self.encoder_path}")
                
            mtime = os.path.getmtime(self.encoder_path)
            cached = self._encoder_cache.get(self.encoder_path)
            if cached is None or cached['mtime'] < mtime:
                logger.info(f"Loading label encoder into memory from {self.encoder_path}")
                le = joblib.load(self.encoder_path)
                self._encoder_cache[self.encoder_path] = {'encoder': le, 'mtime': mtime}
            return self._encoder_cache[self.encoder_path]['encoder']

    def predict(self, input_features):
        try:
            model = self._get_model()
            le = self._get_encoder()
            validate_columns(input_features, PREDICTION_FEATURES)

            probas = model.predict_proba(input_features)[0]
            pred_idx = model.predict(input_features)[0]
            class_positions = np.where(model.classes_ == pred_idx)[0]
            confidence_index = int(class_positions[0]) if len(class_positions) else int(pred_idx)
            confidence = float(probas[confidence_index]) * 100

            predicted_class = le.inverse_transform([pred_idx])[0]

            hour = input_features['Hour'].iloc[0]
            dist = input_features['Dist_to_Transit'].iloc[0]
            explanation, time_context, transit_context = build_prediction_explanation(hour, dist)
            risk_score = calculate_risk_score(confidence, time_context, transit_context)

            return {
                "prediction": predicted_class,
                "confidence": round(float(confidence), 1),
                "risk_score": round(float(risk_score), 1),
                "explanation": explanation
            }
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"prediction": "ERROR", "confidence": 0.0, "risk_score": 0.0, "explanation": str(e)}

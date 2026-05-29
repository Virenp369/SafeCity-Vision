import logging

import joblib

from ml.preprocessing.schema_validator import validate_columns


logger = logging.getLogger(__name__)


def select_clustering_features(df) -> list[str]:
    return ['Latitude', 'Longitude'] if 'Latitude' in df.columns else ['Hour', 'DayOfWeek', 'Dist_to_Transit']


class HotspotDetector:
    def __init__(self, model_path: str):
        self.model_path = model_path

    def cluster_hotspots(self, df):
        try:
            model = joblib.load(self.model_path)
            features = select_clustering_features(df)
            validate_columns(df, features)
            x_cluster = df[features].fillna(0)
            clusters = model.predict(x_cluster)
            output = df.copy()
            output['Cluster'] = clusters
            return output
        except Exception as e:
            logger.error(f"Clustering failed: {e}")
            return df

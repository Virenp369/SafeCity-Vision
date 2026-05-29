from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier


def create_model(model_type: str):
    if model_type == "XGBoost":
        return XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, eval_metric='mlogloss')
    if model_type == "Random Forest":
        return RandomForestClassifier(n_estimators=100, class_weight='balanced')
    if model_type == "Logistic Regression":
        return LogisticRegression(class_weight='balanced', max_iter=1000)
    if model_type == "KMeans":
        return KMeans(n_clusters=5, random_state=42)
    raise ValueError(f"Unsupported model type: {model_type}")

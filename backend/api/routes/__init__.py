from backend.api.routes.alerts import router as alerts_router
from backend.api.routes.analytics import router as analytics_router
from backend.api.routes.anomalies import router as anomalies_router
from backend.api.routes.assistant import router as assistant_router
from backend.api.routes.data import router as data_router
from backend.api.routes.forecast import router as forecast_router
from backend.api.routes.health import router as health_router
from backend.api.routes.hotspots import router as hotspots_router
from backend.api.routes.models import router as models_router
from backend.api.routes.predictions import router as predictions_router
from backend.api.routes.reports import router as reports_router
from backend.api.routes.risk import router as risk_router

__all__ = [
    "alerts_router",
    "analytics_router",
    "anomalies_router",
    "assistant_router",
    "data_router",
    "forecast_router",
    "health_router",
    "hotspots_router",
    "models_router",
    "predictions_router",
    "reports_router",
    "risk_router",
]

from fastapi import FastAPI

from backend.api.routes import (
    alerts_router,
    analytics_router,
    anomalies_router,
    assistant_router,
    data_router,
    forecast_router,
    health_router,
    hotspots_router,
    models_router,
    predictions_router,
    reports_router,
    risk_router,
)
from backend.config.logging_config import configure_logging
from backend.config.settings import get_settings


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )
    app.include_router(health_router)
    app.include_router(models_router)
    app.include_router(predictions_router)
    app.include_router(data_router)
    app.include_router(analytics_router)
    app.include_router(risk_router)
    app.include_router(hotspots_router)
    app.include_router(alerts_router)
    app.include_router(forecast_router)
    app.include_router(reports_router)
    app.include_router(assistant_router)
    app.include_router(anomalies_router)
    return app


app = create_app()

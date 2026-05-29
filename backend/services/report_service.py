from typing import Any

from backend.services.alert_service import AlertService
from backend.services.analytics_service import AnalyticsService
from backend.services.forecast_service import ForecastService
from backend.services.hotspot_service import HotspotService


class ReportService:
    def generate_report(self, records: list[dict[str, Any]], title: str, context: str) -> dict[str, Any]:
        analytics = AnalyticsService().summarize(records)
        hotspots = HotspotService().detect_hotspots(records, min_count=1, limit=10)
        alerts = AlertService().evaluate_alerts(records)
        forecast = ForecastService().forecast_crime_volume(records, horizon_days=7)

        return {
            "title": title,
            "context": context,
            "summary": analytics,
            "hotspots": hotspots,
            "alerts": alerts,
            "forecast": forecast,
        }

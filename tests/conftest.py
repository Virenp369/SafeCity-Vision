import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_records():
    return [
        {
            "Timestamp": "2026-05-24T22:00:00",
            "Latitude": 28.6123,
            "Longitude": 77.2012,
            "Crime_Category": "THEFT",
            "Hour": 22,
            "DayOfWeek": 6,
            "Dist_to_Transit": 0.3,
        },
        {
            "Timestamp": "2026-05-25T23:00:00",
            "Latitude": 28.6126,
            "Longitude": 77.2018,
            "Crime_Category": "THEFT",
            "Hour": 23,
            "DayOfWeek": 0,
            "Dist_to_Transit": 0.4,
        },
        {
            "Timestamp": "2026-05-26T11:00:00",
            "Latitude": 28.7000,
            "Longitude": 77.3000,
            "Crime_Category": "ROBBERY",
            "Hour": 11,
            "DayOfWeek": 1,
            "Dist_to_Transit": 2.0,
        },
    ]

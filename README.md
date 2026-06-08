<<<<<<< HEAD
# SafeCity Vision

AI-powered crime pattern prediction and forensic analytics platform for hotspot analysis, risk scoring, geospatial intelligence, and analyst briefings.

## What It Does

- Ingests public crime data or user-uploaded CSV files.
- Enriches records with temporal and location-derived features.
- Visualizes high-risk areas through interactive heatmaps.
- Trains XGBoost, Random Forest, Logistic Regression, and KMeans models.
- Produces risk scores, threat summaries, and AI-generated analyst briefings.
- Exposes a small FastAPI model-serving surface for deployment readiness.

## Architecture

```text
Data Sources / CSV Upload
        |
        v
Backend Services -> ML Preprocessing -> Streamlit Intelligence Dashboard
        |                 |                 |
        |                 v                 v
        |           ML Features        Folium + Plotly
        |                 |
        v                 v
   ModelTrainer -----> ml/models/*.pkl -----> FastAPI /predict/risk
        |
        v
 Gemini / LangChain Analyst Assistant
```

## Project Structure

```text
Crime-Analytics-AI/
│
├── PROJECT_STRUCTURE.md                 # Complete repository navigation guide
│
├── docs/                                # Architecture, data dictionary, presentation guide
│
├── frontend/
│   ├── app.py                           # Streamlit entry point
│   │
│   ├── pages/                           # Dashboard, ML lab, AI assessment pages
│   ├── components/                      # Reusable UI cards, charts, sidebar
│   ├── layouts/                         # Layout shells and page composition helpers
│   ├── services/                        # Data loading, AI, map helpers
│   ├── assets/                          # Frontend visual assets
│   └── utils/                           # Insight and risk helpers
│
├── backend/
│   ├── api/
│   │   ├── main.py                      # API factory and router registration
│   │   ├── app.py                       # Uvicorn entry point
│   │   │
│   │   ├── routes/                      # Health, status, prediction endpoints
│   │   └── schemas/                     # Request/response validation models
│   │
│   ├── services/
│   │   ├── alert_service.py             # Operational alert evaluation
│   │   ├── analytics_service.py         # Dataset analytics and filtering
│   │   ├── data_validation_service.py   # Validation and enrichment
│   │   ├── forecast_service.py          # Crime forecasting
│   │   ├── hotspot_service.py           # Hotspot detection
│   │   ├── model_service.py             # Prediction orchestration
│   │   ├── report_service.py            # Intelligence reports
│   │   └── risk_service.py              # Risk score service
│   │
│   ├── controllers/                     # Request orchestration layer
│   ├── middleware/                      # Auth, logging, rate limiting
│   ├── database/                        # Database adapters/repositories
│   └── config/                          # Backend configuration
│
├── ml/
│   ├── training/
│   │   ├── model_factory.py             # Model architecture selection
│   │   └── model_trainer.py             # Training pipeline
│   │
│   ├── preprocessing/
│   │   ├── feature_enricher.py          # Feature engineering
│   │   ├── schema_normalizer.py         # Schema standardization
│   │   ├── schema_validator.py          # Dataset validation
│   │   └── data_quality.py              # Data quality reporting
│   │
│   ├── inference/
│   │   ├── prediction_service.py        # Model inference
│   │   └── risk_scoring.py              # Risk score generation
│   │
│   ├── forecasting/
│   │   └── anomaly_detector.py          # Anomaly detection
│   │
│   ├── clustering/
│   │   └── hotspot_detector.py          # Crime hotspot clustering
│   │
│   └── models/                          # Serialized ML models
│
├── ai_assistant/
│   ├── integrations/                    # Gemini/LangChain integrations
│   ├── prompts/                         # Prompt templates
│   ├── chains/                          # LLM chains
│   ├── context/                         # Dataset context builders
│   └── memory/                          # Assistant memory modules
│
├── maps/                                # Heatmaps, GeoJSON, map layers
│
├── data/
│   ├── raw/                             # Original datasets
│   ├── interim/                         # Intermediate datasets
│   ├── cleaned/                         # Cleaned datasets
│   ├── processed/                       # Feature-engineered datasets
│   └── exported/                        # Reports and exports
│
├── config/                              # Global configuration templates
│
├── scripts/                             # Automation and utility scripts
│
├── tests/                               # Unit and integration tests
│
└── reports/                             # Generated analysis reports
```

See `PROJECT_STRUCTURE.md` for the full clean folder layout.

## Run Locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run frontend\app.py
```

Optional API:

```powershell
uvicorn backend.api.app:app --reload --port 8000
```

Run tests:

```powershell
venv\Scripts\python.exe -m pytest
```

Current API surface:

```text
GET  /health
GET  /models/status
POST /predict/risk
POST /risk/score
POST /data/validate
POST /data/normalize
POST /data/quality
POST /data/enrich
POST /analytics/summary
POST /analytics/filter
POST /hotspots/detect
POST /alerts/evaluate
POST /anomalies/detect
POST /forecast/crime-volume
POST /reports/generate
POST /assistant/query
```

## CSV Upload Format

Required columns, or common aliases:

- `Timestamp`
- `Latitude`
- `Longitude`
- `Crime_Category`

Optional:

- `City`
- `Description`

## Development Roadmap

1. MVP: CSV upload, simulated India data, heatmaps, risk score, model training.
2. Advanced analytics: forecasting, anomaly detection, explainable feature importance.
3. Backend: authenticated FastAPI endpoints, PostgreSQL storage, model registry.
4. Deployment: Docker, Render/AWS hosting, CI checks, monitoring.
5. Research: CCTV anomaly detection, patrol optimization, multi-agent analyst workflows.
=======
# SafeCity-Vision
SafeCity Vision is an AI-powered crime intelligence and forensic analytics platform that analyzes historical crime data, predicts high-risk zones, identifies crime hotspots, and provides interactive dashboards, heatmaps, and AI-driven insights to support proactive public safety decision-making.
>>>>>>> 5ea88b2a7b1ee7e86b0e88da4108781d6a9ae2f7

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
PROJECT_STRUCTURE.md       Complete repository navigation guide
docs/                      Architecture, data dictionary, and presentation guide
frontend/
  app.py                  Streamlit entry point
  pages/                  Dashboard, ML lab, AI assessment pages
  components/             Reusable UI cards, charts, sidebar
  layouts/                Layout shells and page composition helpers
  services/               Data loading, AI, map helpers
  assets/                 Frontend-only visual assets
  utils/                  Insight and risk helpers
backend/
  api/                    FastAPI app and route definitions
    main.py               API factory and router registration
    app.py                Backward-compatible uvicorn entry point
    routes/               Health, model status, and prediction endpoints
    schemas/              Request/response validation models
  services/               City data harvesting and backend orchestration
    alert_service.py      Rule-based operational alert evaluation
    analytics_service.py  Dataset summaries and intelligent filtering
    data_validation_service.py Dataset validation and enrichment orchestration
    forecast_service.py   Crime-volume trend forecasting
    hotspot_service.py    Coordinate-based hotspot detection
    model_service.py      Model artifact status and prediction orchestration
    report_service.py     Aggregated intelligence report generation
    risk_service.py       Reusable risk-score API service
  controllers/            Future request orchestration layer
  middleware/             Future auth/logging/rate-limit middlewared
  database/               Future database adapters and repositories
  config/                 Backend configuration loaders
ml/
  training/               Model training and compatibility modules
    model_factory.py      Model architecture selection
    model_trainer.py      Backward-compatible training facade
  preprocessing/          Feature engineering and enrichment
    feature_enricher.py   Temporal and location-derived feature enrichment
    schema_normalizer.py  CSV alias mapping into canonical crime schema
    schema_validator.py   Reusable dataset column validation
    data_quality.py       Dataset consistency and quality reporting
  inference/              Prediction and risk scoring services
    prediction_service.py Saved model inference orchestration
    risk_scoring.py       Risk-score and explanation helpers
  forecasting/            Forecasting and anomaly detection
    anomaly_detector.py   Statistical anomaly detection for spikes and concentrations
  clustering/             Hotspot clustering helpers
    hotspot_detector.py   Cluster assignment for trained hotspot models
  models/                 Serialized model artifacts
ai_assistant/
  integrations/           Gemini/LangChain assistant integration
  prompts/                Prompt templates
  chains/                 Future LLM chains
  context/                Dataset-to-LLM context builders
  memory/                 Future assistant memory adapters
maps/                     Heatmaps, GeoJSON, and map layers
data/                     Raw, interim, cleaned, processed, exported datasets
config/                   Non-secret configuration templates
scripts/                  Utility scripts and automation helpers
tests/                    Automated test workspace
reports/                  Generated analysis outputs
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

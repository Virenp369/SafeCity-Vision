# SafeCity Vision Project Structure

This file gives a quick map of the repository so reviewers, teammates, and recruiters can understand the project at a glance.

```text
SafeCity-Vision/
  README.md                     Main project overview and run instructions
  PROJECT_ROADMAP.md            Product roadmap and implementation phases
  PROJECT_STRUCTURE.md          Repository navigation guide
  requirements.txt              Python dependencies
  Dockerfile                    Container build definition
  .env.example                  Safe environment-variable template

  frontend/                     Streamlit user interface
    app.py                      Main dashboard entry point
    pages/                      Dashboard, ML lab, and AI assessment pages
    components/                 Reusable UI blocks
    layouts/                    Layout shells and page composition helpers
    services/                   Frontend-facing service helpers
    assets/                     Frontend-only assets
    styles/                     CSS and visual styling
    utils/                      UI-side insight utilities

  backend/                      API and backend service layer
    api/                        FastAPI app and route definitions
      main.py                   API factory and router registration
      app.py                    Backward-compatible uvicorn entry point
      routes/                   Endpoint modules
      schemas/                  Pydantic request/response schemas
    services/                   Harvesting, analytics, validation, alerts, reports, forecasting, risk, and model orchestration
    controllers/                Future request orchestration layer
    middleware/                 Future API middleware
    database/                   Future database adapters and repositories
    config/                     Backend configuration loaders

  ml/                           Machine learning system
    training/                   Model factory and training facade
    preprocessing/              Feature engineering, schema normalization, validation, and quality reporting
    inference/                  Saved-model prediction and risk scoring
    forecasting/                Forecasting and anomaly detection
    clustering/                 Hotspot clustering helpers
    models/                     Serialized model artifacts

  ai_assistant/                 LLM assistant system
    integrations/               Gemini/LangChain integration
    prompts/                    Prompt templates
    chains/                     Future LLM chains
    context/                    Dataset-to-LLM context builders
    memory/                     Future assistant memory adapters

  maps/                         Geospatial outputs and map assets
    heatmaps/                   Generated hotspot maps
    geojson/                    Boundary and geospatial exchange files
    layers/                     Reusable map layers

  data/                         Dataset workspace
    raw/                        Original downloaded or uploaded data
    interim/                    Cleaned but not final data
    cleaned/                    Validated normalized data
    processed/                  Feature-ready datasets
    exports/                    User-facing exports

  notebooks/                    EDA, experiments, and research notebooks
  config/                       Non-secret configuration templates
  docs/                         Project documentation
  scripts/                      Utility commands and automation scripts
  tests/                        Test suite workspace
    conftest.py                 Shared pytest fixtures
    test_api_routes.py          FastAPI route coverage
    test_preprocessing.py       Schema normalization and quality tests
    test_risk_and_anomalies.py  Risk scoring and anomaly detection tests
  assets/                       Screenshots, diagrams, and presentation media
  reports/                      Generated analysis outputs and figures
```

## Organization Rule

- Put reusable backend application code in `backend/`.
- Put model code and artifacts in `ml/`.
- Put LLM assistant code in `ai_assistant/`.
- Put Streamlit UI code in `frontend/`.
- Put temporary experiments in `notebooks/`.
- Put generated data in `data/`, not inside source folders.
- Put secrets only in `.env`; never commit real keys.
- Put project explanation, architecture, and presentation material in `docs/`.

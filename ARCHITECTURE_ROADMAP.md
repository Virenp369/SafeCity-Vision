# SafeCity Vision Architecture Roadmap

## 1. Foundation

Goal: keep the MVP impressive, explainable, and realistic.

MVP features:
- CSV upload and public/simulated node ingestion
- Temporal and geospatial enrichment
- Interactive heatmap and threat charts
- Risk score and operational recommendations
- ML lab with XGBoost, Random Forest, Logistic Regression, and KMeans
- AI briefing with Gemini through LangChain

Advanced version:
- PostgreSQL/PostGIS persistence
- Authenticated FastAPI backend
- Forecasting service
- Explainable AI panel
- Patrol optimization simulator
- CI/CD and cloud deployment

Team roles:
- Data engineer: ingestion, cleaning, enrichment
- ML engineer: training, evaluation, model registry
- Frontend engineer: Streamlit dashboard, maps, charts
- Backend engineer: FastAPI routes, validation, deployment
- Product/demo lead: story, README, screenshots, presentation

Estimated MVP timeline: 2-3 weeks.

## 2. Data Engineering

Preferred datasets:
- Chicago public crime data
- LAPD crime data
- NYC open crime datasets
- Simulated NCRB-style India data for demo reliability
- Custom CSV upload for evaluation/demo flexibility

Pipeline:
1. Ingest source data
2. Normalize column names
3. Validate timestamp and coordinates
4. Drop invalid records
5. Add hour, day of week, month
6. Add environmental or proximity features
7. Cache enriched data for dashboard use

Beginner mistakes to avoid:
- Training directly on raw strings without encoding
- Ignoring missing coordinates
- Mixing train/test data
- Presenting predictions without confidence or explanation

## 3. Machine Learning

Tasks and models:

| Task | Recommended Model | Why |
|---|---|---|
| Crime type classification | XGBoost / Random Forest | Strong tabular performance |
| Baseline comparison | Logistic Regression | Easy to explain |
| Hotspot clustering | KMeans | Simple geographic segmentation |
| Risk score | Rule + model confidence | More explainable for demos |
| Time forecast | Prophet / ARIMA / LSTM later | Add after MVP is stable |

Evaluation:
- Accuracy and macro F1 for classification
- Confusion matrix for category mistakes
- Silhouette score for clustering
- Calibration and confidence review for predictions

## 4. Geospatial Intelligence

Implementation:
- Folium heatmap for fast visual hotspot analysis
- Plotly charts for temporal and category patterns
- Future: PostGIS for district boundaries and spatial queries

Map UX:
- Start with heatmap
- Add filters before advanced layers
- Keep color meaning consistent: green controlled, amber elevated, red critical

## 5. AI Assistant

Architecture:
1. User asks question
2. System builds compact dataset summary
3. LangChain sends summary plus prompt to Gemini
4. Assistant returns concise analyst-style answer

Safety:
- Never claim causation from correlation
- Mention when data is simulated
- Keep recommendations as decision support, not enforcement instructions
- Avoid demographic or protected-class targeting

## 6. Frontend

Dashboard layout:
- Mission header
- Metrics row
- Operational brief
- Heatmap and threat composition
- Temporal signal
- AI briefing and evidence feed

Streamlit is best for the MVP because it is fast and Python-native. React is better later if you need custom map interactions, authentication-heavy workflows, or a public SaaS-style app.

## 7. Backend

Current FastAPI routes:
- `GET /health`
- `GET /models/status`
- `POST /predict/risk`

Next backend steps:
- Add `/datasets/upload`
- Add `/analysis/summary`
- Add `/hotspots`
- Add authentication
- Add PostgreSQL/PostGIS storage

## 8. Deployment

Recommended path:
1. Streamlit Community Cloud or Render for MVP
2. Docker for reproducible deployment
3. AWS later for serious scaling

Monitoring:
- Log failed uploads
- Log model training errors
- Track prediction latency
- Track missing environment variables

## 9. Advanced Enhancements

| Enhancement | Difficulty | Impact | Feasibility |
|---|---:|---:|---:|
| Explainable AI feature importance | Medium | High | High |
| Forecasting dashboard | Medium | High | High |
| PostGIS district analytics | Medium | High | Medium |
| Real-time streaming | High | High | Medium |
| CCTV anomaly detection | Very High | Very High | Low-Medium |
| Voice assistant | Medium | Medium | Medium |
| Patrol optimization | High | Very High | Medium |

## 10. Demo Strategy

Demo flow:
1. Start on standby screen
2. Load India simulation or upload CSV
3. Show risk posture and heatmap
4. Filter by category and hour
5. Train a model in ML Lab
6. Generate a prediction
7. Ask AI assistant for a tactical summary
8. Show FastAPI docs or health endpoint for deployment readiness

Best screenshots:
- Mission dashboard with map
- ML Lab prediction output
- AI assistant answer
- FastAPI `/docs`
- README architecture diagram

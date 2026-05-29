# Architecture

SafeCity Vision is organized as an AI-powered forensic analytics platform with four main layers.

## 1. Data Layer

The data layer collects crime records from public city APIs or uploaded CSV files. The expected normalized schema is:

- `Timestamp`
- `Latitude`
- `Longitude`
- `Crime_Category`
- `Description`

## 2. Enrichment Layer

The enrichment layer converts raw records into ML-ready features:

- Hour of day
- Day of week
- Month
- Weather or weather proxy
- Transit or urban-density proxy

In production, this layer can connect to Open-Meteo and OpenStreetMap/OSMnx for richer environmental context.

## 3. Intelligence Layer

The intelligence layer trains and serves ML models:

- XGBoost
- Random Forest
- Logistic Regression

The model pipeline handles class imbalance and stores reusable artifacts in `models/`.

## 4. Experience Layer

The Streamlit dashboard gives users a visual interface for:

- Harvesting data
- Viewing maps and metrics
- Training models
- Simulating predictions
- Asking natural-language questions through the forensic AI assistant

## High-Level Flow

```text
City API / CSV Upload
        |
        v
backend.services.DataHarvester
        |
        v
ml.preprocessing.DataEnricher
        |
        v
ml.training.ModelTrainer + Dashboard Metrics
        |
        v
Streamlit Dashboard + FastAPI + AI Assistant
```

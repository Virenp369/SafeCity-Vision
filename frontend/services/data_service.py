import streamlit as st
import sys
import os
import uuid
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.city_crime_harvester import DataHarvester
from backend.services.india_crime_harvester import IndiaDataHarvester
from ml.preprocessing.feature_enricher import DataEnricher
from ml.preprocessing.schema_normalizer import normalize_crime_schema


def save_session_data(df: pd.DataFrame) -> str:
    session_id = str(uuid.uuid4())
    save_dir = os.path.join(PROJECT_ROOT, "data", "processed")
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"session_{session_id}.parquet")
    df.to_parquet(file_path, index=False)
    return session_id

def load_session_data(session_id: str) -> pd.DataFrame:
    file_path = os.path.join(PROJECT_ROOT, "data", "processed", f"session_{session_id}.parquet")
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data(node, limit):
    if "India" in node:
        harvester = IndiaDataHarvester()
        df = harvester.fetch_simulated_ncrb_data(limit=limit)
    else:
        harvester = DataHarvester()
        df = harvester.fetch_global_data(node=node, limit=limit)
        
    if df.empty:
        return None, df

    try:
        enricher = DataEnricher()
        df = enricher.enrich(df)
        session_id = save_session_data(df)
        return session_id, df
    except Exception as exc:
        st.error(f"Data enrichment failed: {exc}")
        return None, df


def load_uploaded_data(uploaded_file):
    if uploaded_file is None:
        return None, pd.DataFrame()

    raw_df = pd.read_csv(uploaded_file)
    df = normalize_uploaded_columns(raw_df)
    if df.empty:
        return None, df

    try:
        df = DataEnricher().enrich(df)
        session_id = save_session_data(df)
        return session_id, df
    except Exception as exc:
        st.error(f"Uploaded data could not be prepared: {exc}")
        return None, pd.DataFrame()


def normalize_uploaded_columns(df):
    try:
        return normalize_crime_schema(df)
    except ValueError as exc:
        st.error(str(exc))
        return pd.DataFrame()

import os
import sys
import requests
import textwrap
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

API_URL = "http://localhost:8000"


def render_ml_models(session_id, df):
    st.markdown(textwrap.dedent(f"""
        <div class="mission-header" style="margin-bottom: 32px;">
            <div>
                <span class="eyebrow">Predictive Analytics</span>
                <h1>Machine Learning Lab</h1>
                <p>Train and deploy specialized intelligence architectures to forecast threat propagation.</p>
            </div>
            <div class="mission-pill" style="color: #38BDF8; border-color: rgba(56, 189, 248, 0.5); background: rgba(56, 189, 248, 0.1);">ENGINE STANDBY</div>
        </div>
    """), unsafe_allow_html=True)

    with st.container(border=True):
        model_selection = st.selectbox("Intelligence Architecture", ["XGBoost", "Random Forest", "Logistic Regression", "KMeans"])

        if st.button(f"Compile {model_selection} Engine"):
            with st.spinner(f"Compiling {model_selection} Matrix via Core API..."):
                try:
                    res = requests.post(f"{API_URL}/models/train", json={"session_id": session_id, "model_type": model_selection})
                    res.raise_for_status()
                    st.session_state['model_trained'] = True
                    st.session_state['active_model_type'] = model_selection
                    st.success(f"Model compiled. {model_selection} online.")
                except Exception as e:
                    st.error(f"{model_selection} training failed. Ensure FastAPI backend is running. Error: {e}")

    if st.session_state.get('model_trained', False):
        if st.session_state.get('active_model_type') == "KMeans":
            st.markdown("<div style='margin-top: 32px; margin-bottom: 16px;'><span class='eyebrow'>Spatial Analysis</span><h3 style='margin: 0; font-size: 1.4rem;'>Hotspot Clustering</h3></div>", unsafe_allow_html=True)
            st.info("KMeans clustering successfully segmented high-risk crime hotspots based on geospatial coordinates.")
            
            with st.spinner("Fetching clustered dataset..."):
                try:
                    res = requests.post(f"{API_URL}/models/cluster", json={"session_id": session_id, "model_type": "KMeans"})
                    res.raise_for_status()
                    records = res.json().get("records", [])
                    st.dataframe(pd.DataFrame(records), use_container_width=True)
                except Exception as e:
                    st.error(f"Failed to fetch clustering results. Error: {e}")
        else:
            st.markdown("<div style='margin-top: 32px; margin-bottom: 16px;'><span class='eyebrow'>Simulation</span><h3 style='margin: 0; font-size: 1.4rem;'>Inference Engine Simulation</h3></div>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; margin-top: -12px; margin-bottom: 24px;'>Configure tactical simulation parameters to generate a predictive Risk Score and Hotspot forecast.</p>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1:
                test_hour = st.slider("Temporal Alignment (Hour)", 0, 23, 18)
            with c2:
                test_day = st.slider("Temporal Alignment (Day)", 0, 6, 4)
            with c3:
                dist_transit = st.slider("Transit Proximity (km)", 0.0, 5.0, 0.2)

            if st.button("Generate Forecast & Risk Score", use_container_width=True, type="primary"):
                with st.spinner("Requesting inference from API..."):
                    try:
                        payload = {
                            "session_id": session_id,
                            "hour": test_hour,
                            "day_of_week": test_day,
                            "temperature": 15.0,
                            "is_raining": 0,
                            "dist_to_transit": dist_transit
                        }
                        res = requests.post(f"{API_URL}/predict/risk", json=payload)
                        res.raise_for_status()
                        result = res.json()

                        risk_color = "#10B981" if result.get('risk_score', 0) < 50 else "#F59E0B" if result.get('risk_score', 0) < 75 else "#EF4444"

                        st.markdown(textwrap.dedent(f"""
                            <div class="cyber-card" style="border-left: 4px solid {risk_color}; margin-top: 32px;">
                                <div class="eyebrow" style="color: {risk_color} !important; margin-bottom: 12px;">Primary Threat Forecast</div>
                                <h1 style="color: #f1f5f9 !important; font-size: 3.2rem; margin: 0 0 16px 0; font-weight: 800;">{result['prediction']}</h1>
                                
                                <div style="display: flex; gap: 24px; margin-bottom: 24px;">
                                    <div>
                                        <div style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px;">System Confidence</div>
                                        <div style="color: #38BDF8; font-size: 1.5rem; font-weight: 700; font-family: 'Outfit', sans-serif;">{result['confidence']}%</div>
                                    </div>
                                    <div>
                                        <div style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px;">Risk Score</div>
                                        <div style="color: {risk_color}; font-size: 1.5rem; font-weight: 700; font-family: 'Outfit', sans-serif;">{result.get('risk_score', 50)}/100</div>
                                    </div>
                                </div>
                                
                                <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); padding: 16px; border-radius: 8px;">
                                    <span class="eyebrow" style="color: #38BDF8 !important; margin-bottom: 6px;">AI Rationale</span>
                                    <p style="color: #CBD5E1; margin: 0; font-size: 0.95rem; line-height: 1.5;">{result['explanation']}</p>
                                </div>
                            </div>
                        """), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Inference failed. Ensure FastAPI is running. Error: {e}")

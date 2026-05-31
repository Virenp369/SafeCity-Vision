import os
import sys
import pandas as pd
from pathlib import Path

import streamlit as st
import textwrap
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="SafeCity Vision | Command Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

from frontend.components.sidebar import render_sidebar
from frontend.services.data_service import load_session_data

# Page Imports
from frontend.pages.overview import render_overview
from frontend.pages.threat_intelligence import render_threat_intelligence
from frontend.pages.crime_analytics import render_crime_analytics
from frontend.pages.predictions import render_predictions
from frontend.pages.surveillance import render_surveillance
from frontend.pages.ai_assessment import render_ai_assessment
from frontend.pages.alerts import render_alerts
from frontend.pages.settings import render_settings

def load_css():
    css_path = Path(__file__).parent / "styles" / "main.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

load_css()
selected = render_sidebar()

api_key = os.getenv("GEMINI_API_KEY")

# Check if we have data or are in demo mode
has_data = 'session_id' in st.session_state
demo_mode = st.session_state.get('demo_mode', False)

if has_data or demo_mode:
    if demo_mode and not has_data:
        # Load a quick dummy dataframe for demo mode if no real data is loaded
        df = pd.DataFrame({
            "Latitude": [41.8781, 41.88, 41.89, 41.86, 41.85],
            "Longitude": [-87.6298, -87.63, -87.64, -87.62, -87.61],
            "Crime_Category": ["ASSAULT", "THEFT", "ROBBERY", "THEFT", "NARCOTICS"],
            "Hour": [22, 23, 1, 2, 14],
            "DayOfWeek": [5, 5, 6, 6, 2],
            "Dist_to_Transit": [0.1, 0.2, 0.5, 0.1, 1.2],
            "City": ["Chicago"] * 5
        })
        current_context = "GLOBAL"
        st.session_state['active_source'] = "Demo Simulation Node"
    else:
        df = load_session_data(st.session_state['session_id'])
        current_context = st.session_state.get('active_context', "Unknown")

    # Routing
    if selected == "Overview":
        render_overview(df, current_context, api_key)
    elif selected == "Threat Intelligence":
        render_threat_intelligence(df, current_context, api_key)
    elif selected == "Crime Analytics":
        render_crime_analytics(df, current_context)
    elif selected == "Predictions":
        render_predictions()
    elif selected == "Surveillance":
        render_surveillance()
    elif selected == "AI Copilot":
        render_ai_assessment(df, api_key)
    elif selected == "Alerts":
        render_alerts(df)
    elif selected == "Settings":
        render_settings()
else:
    # If "Settings" is selected while disconnected, still show it so they can turn on Demo Mode
    if selected == "Settings":
        render_settings()
    else:
        empty_state_html = """
        <section class="empty-state">
        <span class="eyebrow">Standby Mode</span>
        <h1>Initialize Command Node</h1>
        <p>Awaiting data link. Use the sidebar console to pull a live public-safety node, upload a forensic dataset, or navigate to Settings to enable Demo Mode.</p>
        </section>
        """
        st.markdown(textwrap.dedent(empty_state_html), unsafe_allow_html=True)

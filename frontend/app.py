import os
import sys
import textwrap
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="SafeCity Vision | Forensic Intelligence",
    page_icon="SC",
    layout="wide",
    initial_sidebar_state="expanded",
)

from frontend.components.sidebar import render_sidebar
from frontend.pages.ai_assessment import render_ai_assessment
from frontend.pages.intelligence_dashboard import render_dashboard
from frontend.pages.ml_lab import render_ml_models
from frontend.services.data_service import load_session_data


def load_css():
    css_path = Path(__file__).parent / "styles" / "main.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


load_css()
render_sidebar()

selected = option_menu(
    menu_title=None,
    options=["Intelligence Node", "ML Lab", "AI Assessment"],
    icons=["radar", "cpu", "chat-square-text"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "6px",
            "background-color": "rgba(13, 20, 33, 0.65)",
            "border": "1px solid rgba(45, 212, 191, 0.15)",
            "border-radius": "16px",
            "margin-bottom": "24px",
            "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.12)",
        },
        "icon": {"color": "#2DD4BF", "font-size": "18px"},
        "nav-link": {
            "font-size": "15px",
            "font-family": "'Inter', sans-serif",
            "font-weight": "500",
            "text-align": "center",
            "margin": "0px 6px",
            "--hover-color": "rgba(45, 212, 191, 0.1)",
            "color": "#94A3B8",
            "border-radius": "12px",
            "transition": "all 0.3s ease",
        },
        "nav-link-selected": {
            "background-color": "rgba(45, 212, 191, 0.15)",
            "border": "1px solid rgba(45, 212, 191, 0.4)",
            "color": "#f1f5f9",
            "font-weight": "600",
            "box-shadow": "0 0 15px rgba(45, 212, 191, 0.15)",
        },
    },
)

api_key = os.getenv("GEMINI_API_KEY")

if 'session_id' in st.session_state:
    session_id = st.session_state['session_id']
    df = load_session_data(session_id)
    current_context = st.session_state.get('active_context', "Unknown")

    if selected == "Intelligence Node":
        render_dashboard(df, current_context, api_key)
    elif selected == "ML Lab":
        render_ml_models(session_id, df)
    elif selected == "AI Assessment":
        render_ai_assessment(df, api_key)
else:
    st.markdown(
        textwrap.dedent("""
            <section class="empty-state">
                <span class="eyebrow">Standby Mode</span>
                <h1>Initialize Intelligence Node</h1>
                <p>Awaiting data link. Use the command console to pull a live public-safety node or upload a forensic CSV dataset.</p>
            </section>
        """),
        unsafe_allow_html=True,
    )

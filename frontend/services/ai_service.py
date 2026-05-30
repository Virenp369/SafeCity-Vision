import streamlit as st
import sys
import os
import requests
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from ai_assistant.integrations.forensic_assistant import ForensicAssistant

@st.cache_data(ttl=60)
def check_gemini_connection(api_key):
    if not api_key:
        return False
    try:
        response = requests.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", 
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Gemini connection check failed: {e}")
        return False

@st.cache_data
def get_ai_summary(api_key, df_summary):
    if not api_key or not check_gemini_connection(api_key):
        return None
        
    try:
        assistant = ForensicAssistant(api_key)
        return assistant.ask_question(
            "Write a strict 2-sentence highly professional intelligence briefing summarizing the primary threats based on this data. Do not say 'Here is the summary'.", 
            df_summary
        )
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}", exc_info=True)
        return None

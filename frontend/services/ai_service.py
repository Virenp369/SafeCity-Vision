import streamlit as st
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from ai_assistant.integrations.forensic_assistant import ForensicAssistant

@st.cache_data
def get_ai_summary(api_key, df_summary):
    assistant = ForensicAssistant(api_key)
    return assistant.ask_question(
        "Write a strict 2-sentence highly professional intelligence briefing summarizing the primary threats based on this data. Do not say 'Here is the summary'.", 
        df_summary
    )

import streamlit as st
import sys
import textwrap
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from ai_assistant.integrations.forensic_assistant import ForensicAssistant
from frontend.services.ai_service import check_gemini_connection
from frontend.utils.insights import generate_local_intelligence, classify_intent
import logging

logger = logging.getLogger(__name__)

def render_ai_assessment(df, api_key):
    is_connected = check_gemini_connection(api_key) if api_key else False
    
    if is_connected and not df.empty:
        status_indicator = "🟢 AI + Dataset Intelligence"
    elif not is_connected and not df.empty:
        status_indicator = "🟡 Dataset Intelligence Only"
    else:
        status_indicator = "🔴 Intelligence Services Offline"
    
    header_html = f"""
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Natural Language Interface</span>
<h1>AI Intelligence Assessment</h1>
<p>Direct interrogation link with the Palantir-Class Analyst. Query the dataset for hidden hotspots and tactical correlations.</p>
</div>
<div class="mission-pill" style="color: #F59E0B; border-color: rgba(245, 158, 11, 0.5); background: rgba(245, 158, 11, 0.1);">{status_indicator}</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    if not api_key:
        st.error("API Key not found in .env file!")
    else:
        chat_container = st.container(border=True)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! I'm Safe City Vision AI Assistant. I can help with crime analytics, hotspot analysis, city intelligence, and general questions. How can I assist you today?"}
            ]

        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if prompt := st.chat_input("Enter tactical query parameters (e.g. 'Show me dominant threats after midnight')..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    with st.spinner("Processing deep analytical query..."):
                        assistant = ForensicAssistant(api_key)
                        
                        # Generate a rich summary for context
                        top_crimes = df['Crime_Category'].value_counts().head(5).to_dict()
                        if 'City' in df.columns:
                            top_locations = df['City'].value_counts().head(3).to_dict()
                        else:
                            top_locations = "Geo-coordinates available"
                            
                        numeric_cols = [column for column in ['Hour', 'DayOfWeek', 'Dist_to_Transit'] if column in df.columns]
                        general_stats = df[numeric_cols].describe().to_string() if numeric_cols else "No numeric tactical features available."

                        detailed_summary = (
                            f"Total Records Analyzed: {len(df)}\n"
                            f"Top 5 Crime Categories: {top_crimes}\n"
                            f"Top Locations: {top_locations}\n"
                            f"General Stats:\n{general_stats}"
                        )
                        
                        try:
                            mode = classify_intent(prompt)
                            
                            if not is_connected:
                                if mode in ["GREETING", "GENERAL_CONVERSATION"]:
                                    fallback_warning = "Hello! (I am currently running in offline mode and can only provide local data insights right now.)"
                                    st.markdown(fallback_warning)
                                    st.session_state.messages.append({"role": "assistant", "content": fallback_warning})
                                elif mode in ["GENERAL_KNOWLEDGE", "HYBRID_QUERY"]:
                                    fallback_warning = "⚠️ **AI knowledge mode is unavailable.** I can only provide insights based on local dataset trends right now.\n\n"
                                    local_intel = fallback_warning + generate_local_intelligence(df)
                                    st.warning(fallback_warning)
                                    st.markdown(local_intel)
                                    st.session_state.messages.append({"role": "assistant", "content": local_intel})
                                else:
                                    local_intel = "⚠️ **Intelligence uplink failed:** Transitioning to local intelligence generation.\n\n" + generate_local_intelligence(df)
                                    st.markdown(local_intel)
                                    st.session_state.messages.append({"role": "assistant", "content": local_intel})
                            else:
                                response = assistant.ask_question(prompt, detailed_summary, st.session_state.messages[:-1], mode=mode)
                                tagged_response = f"*(Intelligence Mode: {mode})*\n\n{response}"
                                st.markdown(tagged_response)
                                st.session_state.messages.append({"role": "assistant", "content": tagged_response})
                        except Exception as e:
                            logger.error(f"Gemini API Error: {str(e)}", exc_info=True)
                            error_msg = f"⚠️ **Intelligence uplink failed:** Transitioning to local intelligence generation.\n\n" + generate_local_intelligence(df)
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})

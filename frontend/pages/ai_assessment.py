import streamlit as st
import sys
import textwrap
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from ai_assistant.integrations.forensic_assistant import ForensicAssistant

def render_ai_assessment(df, api_key):
    st.markdown(textwrap.dedent(f"""
        <div class="mission-header" style="margin-bottom: 32px;">
            <div>
                <span class="eyebrow">Natural Language Interface</span>
                <h1>AI Intelligence Assessment</h1>
                <p>Direct interrogation link with the Palantir-Class Analyst. Query the dataset for hidden hotspots and tactical correlations.</p>
            </div>
            <div class="mission-pill" style="color: #F59E0B; border-color: rgba(245, 158, 11, 0.5); background: rgba(245, 158, 11, 0.1);">LINK ACTIVE</div>
        </div>
    """), unsafe_allow_html=True)
    
    if not api_key:
        st.error("API Key not found in .env file!")
    else:
        chat_container = st.container(border=True)
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "> **🟢 Neural Link Established.**\n>\n> I am the Palantir-Class Intelligence Node. I have full access to the current geospatial dataset and temporal patterns. How may I assist your analysis?"}
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
                            response = assistant.ask_question(prompt, detailed_summary, st.session_state.messages[:-1])
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_msg = f"⚠️ **Intelligence uplink failed:** Could not connect to API model. Ensure your Gemini key has `gemini-1.5-flash` access and you have restarted the server.\n\n`Error: {str(e)}`"
                            st.error(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})

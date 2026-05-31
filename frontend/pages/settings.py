import streamlit as st
from frontend.services.data_service import load_data, load_uploaded_data

def render_settings():
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">System Configuration</span>
<h1>Settings & Diagnostics</h1>
<p>Configure Safe City Vision parameters, external integrations, and toggle presentation modes.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Presentation Mode</h3>", unsafe_allow_html=True)
        demo_mode = st.toggle("Enable Demo Mode", value=st.session_state.get('demo_mode', False))
        if demo_mode != st.session_state.get('demo_mode', False):
            st.session_state['demo_mode'] = demo_mode
            st.rerun()
            
        st.info("Demo Mode loads a high-fidelity synthetic dataset and activates placeholder UI components optimized for demonstrations to judges and stakeholders.")
    
    if not st.session_state.get('demo_mode', False):
        with st.container(border=True):
            st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Data Configuration</h3>", unsafe_allow_html=True)
            source_mode = st.radio("Data Source", ["Live Node", "Upload CSV"], horizontal=True)

            if source_mode == "Upload CSV":
                _render_upload_controls()
            else:
                _render_node_controls()

    with st.container(border=True):
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>AI Integrations</h3>", unsafe_allow_html=True)
        st.text_input("Gemini API Key", value="Loaded securely from .env", type="password", disabled=True)
        st.text_input("Model Version", value="gemini-2.5-flash", disabled=True)

def _render_node_controls():
    st.markdown("<div class='eyebrow' style='margin-top: 16px; margin-bottom: 8px;'>INTELLIGENCE UPLINK</div>", unsafe_allow_html=True)
    target_node = st.selectbox("Target Region", [
        "Chicago (USA)",
        "New York (USA)",
        "Los Angeles (USA)",
        "All India (NCRB Simulation)",
    ])

    if st.button("Initialize Uplink", type="primary"):
        with st.spinner(f"Establishing link with {target_node}..."):
            session_id, df = load_data(target_node, 1000)
            _activate_dataset(session_id, df, "INDIA" if "India" in target_node else "GLOBAL", target_node)


def _render_upload_controls():
    st.markdown("<div class='eyebrow' style='margin-top: 16px; margin-bottom: 8px;'>FORENSIC UPLOAD</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload crime CSV", type=["csv"])
    if st.button("Process Secure Upload", type="primary", disabled=uploaded_file is None):
        with st.spinner("Decrypting and enriching records..."):
            session_id, df = load_uploaded_data(uploaded_file)
            _activate_dataset(session_id, df, "CUSTOM", uploaded_file.name if uploaded_file else "Uploaded CSV")


def _activate_dataset(session_id, df, context, label):
    if session_id and not df.empty:
        st.session_state['session_id'] = session_id
        st.session_state['active_context'] = context
        st.session_state['active_source'] = label
        st.success(f"Dataset online: {len(df):,} records")
    else:
        st.error("Uplink failed. No usable data retrieved.")


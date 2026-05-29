import streamlit as st

from frontend.services.data_service import load_data, load_uploaded_data


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div class='brand-lockup' style='margin-bottom: 4px;'>SafeCity<br><span>Vision</span></div>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <div style='width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981;'></div>
                <div style='color: #94A3B8; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;'>Palantir-Node Active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='eyebrow' style='margin-bottom: 12px;'>DATA BASELINE</div>", unsafe_allow_html=True)
        source_mode = st.radio("Data Source", ["Live / Simulated Node", "Upload CSV"], label_visibility="collapsed")

        if source_mode == "Upload CSV":
            _render_upload_controls()
        else:
            _render_node_controls()

        st.markdown("---")
        st.markdown("<div class='eyebrow' style='margin-bottom: 8px;'>OPERATOR NOTES</div>", unsafe_allow_html=True)
        st.info("Required CSV fields: timestamp, latitude, longitude, and crime category. Common aliases are auto-detected.")


def _render_node_controls():
    st.markdown("<div class='eyebrow' style='margin-top: 16px; margin-bottom: 8px;'>INTELLIGENCE UPLINK</div>", unsafe_allow_html=True)
    target_node = st.selectbox("Target Region", [
        "Chicago (USA)",
        "New York (USA)",
        "Los Angeles (USA)",
        "All India (NCRB Simulation)",
    ])

    data_limit = st.slider("Record Limit", min_value=50, max_value=5000, value=1000, step=50)
    if st.button("Initialize Uplink", use_container_width=True, type="primary"):
        with st.spinner(f"Establishing link with {target_node}..."):
            session_id, df = load_data(target_node, data_limit)
            _activate_dataset(session_id, df, "INDIA" if "India" in target_node else "GLOBAL", target_node)


def _render_upload_controls():
    st.markdown("<div class='eyebrow' style='margin-top: 16px; margin-bottom: 8px;'>FORENSIC UPLOAD</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload crime CSV", type=["csv"])
    if st.button("Process Secure Upload", use_container_width=True, type="primary", disabled=uploaded_file is None):
        with st.spinner("Decrypting and enriching records..."):
            session_id, df = load_uploaded_data(uploaded_file)
            _activate_dataset(session_id, df, "CUSTOM", uploaded_file.name if uploaded_file else "Uploaded CSV")


def _activate_dataset(session_id, df, context, label):
    if session_id and not df.empty:
        st.session_state['session_id'] = session_id
        st.session_state['active_context'] = context
        st.session_state['active_source'] = label
        st.session_state['model_trained'] = False
        st.success(f"Dataset online: {len(df):,} records (Session ID: {session_id[:8]})")
    else:
        st.error("Uplink failed. No usable data retrieved.")

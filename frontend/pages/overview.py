import streamlit as st
from datetime import datetime
from frontend.services.ai_service import check_gemini_connection, get_ai_summary
from frontend.utils.insights import risk_score, generate_local_intelligence, _safe_mode

def render_overview(df, current_context, api_key):
    st.markdown("""
<style>
.mission-status-container {
    background-color: rgba(16, 185, 129, 0.1);
    border: 1px solid #10B981;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 24px;
}
.mission-status-title {
    color: #10B981;
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}
.mission-status-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
}
.mission-label { color: #94A3B8; font-size: 0.85rem; }
.mission-val { color: #F8FAFC; font-weight: 600; }
.mission-val-ok { color: #10B981; font-weight: 600; }
</style>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("No dataset loaded. Upload a CSV or enable Demo Mode in Settings.")
        return

    source = st.session_state.get("active_source", current_context)
    is_connected = check_gemini_connection(api_key) if api_key else False
    
    if is_connected:
        status_indicator = "🟢 AI + Dataset Intelligence"
    else:
        status_indicator = "🟡 Dataset Intelligence Only"

    primary_threat = _safe_mode(df, 'Crime_Category', 'Unknown')
    peak_hour = _safe_mode(df, 'Hour', 'N/A')
    hotspots = max(3, int(len(df)/100))

    mission_status_html = f"""
<div class="mission-status-container">
<h3 class="mission-status-title">MISSION STATUS</h3>
<div class="mission-status-grid">
<div><span class="mission-label">Region:</span> <span class="mission-val">{source}</span></div>
<div><span class="mission-label">Primary Threat:</span> <span class="mission-val">{primary_threat}</span></div>
<div><span class="mission-label">Active Hotspots:</span> <span class="mission-val">{hotspots}</span></div>
<div><span class="mission-label">Peak Risk Window:</span> <span class="mission-val">{peak_hour}:00 - {int(peak_hour)+1 if peak_hour != "N/A" else "N/A"}:00</span></div>
<div><span class="mission-label">System Status:</span> <span class="mission-val-ok">Operational</span></div>
</div>
</div>
"""
    st.markdown(mission_status_html, unsafe_allow_html=True)

    header_html = f"""
<section class="mission-header">
<div>
<span class="eyebrow">Real-Time Intelligence Platform</span>
<h1>Safe City Command Center</h1>
<p>Monitoring active threat vectors across {source}. AI models are continuously analyzing situational telemetry to predict and prevent critical incidents.</p>
</div>
<div style="display: flex; flex-direction: column; gap: 8px; align-items: flex-end;">
<div class="mission-pill">{status_indicator}</div>
<div style="color: #94A3B8; font-size: 0.8rem; font-weight: 500;">Last Refresh: {datetime.now().strftime('%H:%M:%S UTC')}</div>
</div>
</section>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Core Diagnostics</h3>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    total_incidents = len(df)
    r_score = risk_score(df)
    dataset_size = f"{df.memory_usage(deep=True).sum() / (1024*1024):.1f} MB"
    
    c1.metric("Total Incidents", f"{total_incidents:,}", "Active")
    c2.metric("Top Crime Type", str(primary_threat)[:12] + ("." if len(str(primary_threat))>12 else ""), "Highest freq")
    c3.metric("Hotspots Detected", f"{hotspots}", "Clusters")
    c4.metric("Peak Crime Hour", f"{peak_hour}:00", "Critical window")
    c5.metric("Selected Region", source[:12], "Target node")
    c6.metric("Dataset Size", dataset_size, "Loaded")

    st.markdown("---")
    
    col_left, col_right = st.columns([1.5, 1], gap="large")
    
    with col_left:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Executive Intelligence Brief</h3>", unsafe_allow_html=True)
        if is_connected:
            with st.spinner("Generating AI Briefing..."):
                summary_cols = [column for column in ['Crime_Category', 'Hour', 'DayOfWeek', 'Dist_to_Transit'] if column in df.columns]
                df_summary = df[summary_cols].describe(include='all').to_string() if summary_cols else "No summary columns available."
                briefing = get_ai_summary(api_key, df_summary)
                if briefing:
                    st.info(briefing)
                else:
                    st.warning("⚠️ Gemini connection lost. Entering fallback mode.")
                    st.info(generate_local_intelligence(df))
        else:
            st.warning("⚠️ AI Intelligence is unavailable. Operating in local mode.")
            st.info(generate_local_intelligence(df))
            
    with col_right:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>City Risk Scorecard</h3>", unsafe_allow_html=True)
        risk_color = "#10B981" if r_score < 50 else "#F59E0B" if r_score < 75 else "#EF4444"
        
        scorecard_html = f"""
<div class="cyber-card" style="border-top: 4px solid {risk_color}; padding: 24px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
<span class="eyebrow" style="color: {risk_color} !important;">Current Risk Level</span>
<span style="font-size: 2.5rem; font-weight: 800; font-family: 'Outfit', sans-serif; color: {risk_color};">{r_score}/100</span>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.85rem; color: #94A3B8;">Temporal Pressure</span>
<span style="font-size: 0.85rem; color: #F8FAFC; font-weight: 600;">High</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 78%; height: 100%; background: #EF4444; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.85rem; color: #94A3B8;">Spatial Clustering</span>
<span style="font-size: 0.85rem; color: #F8FAFC; font-weight: 600;">Moderate</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 54%; height: 100%; background: #F59E0B; border-radius: 4px;"></div>
</div>
</div>
<div>
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.85rem; color: #94A3B8;">Resource Strain</span>
<span style="font-size: 0.85rem; color: #F8FAFC; font-weight: 600;">Controlled</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 32%; height: 100%; background: #10B981; border-radius: 4px;"></div>
</div>
</div>
</div>
"""
        st.markdown(scorecard_html, unsafe_allow_html=True)

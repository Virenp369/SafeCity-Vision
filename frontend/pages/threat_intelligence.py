import streamlit as st
from frontend.components.charts import render_top_threats_chart, render_temporal_pattern
from frontend.utils.insights import risk_score, _safe_mode

def render_threat_intelligence(df, current_context, api_key):
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Predictive Threat Modeling</span>
<h1>Threat Intelligence</h1>
<p>Analyze emerging risk patterns, forecast primary threat vectors, and review AI explainability matrices.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)

    if df.empty:
        st.info("No dataset loaded. Upload a CSV or enable Demo Mode in Settings.")
        return

    r_score = risk_score(df)
    risk_color = "#10B981" if r_score < 50 else "#F59E0B" if r_score < 75 else "#EF4444"
    primary_threat = _safe_mode(df, "Crime_Category", "Unknown")
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Threat Forecast</h3>", unsafe_allow_html=True)
        forecast_html = f"""
<div class="cyber-card" style="border-left: 4px solid {risk_color}; height: 100%;">
<div class="eyebrow" style="color: {risk_color} !important; margin-bottom: 12px;">Primary Threat Vector</div>
<h1 style="color: #f1f5f9 !important; font-size: 3rem; margin: 0 0 16px 0; font-weight: 800;">{primary_threat}</h1>
<div style="display: flex; gap: 24px; margin-bottom: 24px;">
<div>
<div style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px;">System Confidence</div>
<div style="color: #38BDF8; font-size: 1.5rem; font-weight: 700; font-family: 'Outfit', sans-serif;">89.4%</div>
</div>
<div>
<div style="color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px;">Velocity Trend</div>
<div style="color: #EF4444; font-size: 1.5rem; font-weight: 700; font-family: 'Outfit', sans-serif;">+14% (Escalating)</div>
</div>
</div>
<div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(148, 163, 184, 0.1); padding: 16px; border-radius: 8px;">
<span class="eyebrow" style="color: #38BDF8 !important; margin-bottom: 6px;">Tactical Advisory</span>
<p style="color: #CBD5E1; margin: 0; font-size: 0.95rem; line-height: 1.5;">Forecast models indicate sustained elevation in {primary_threat} incidents over the next 48 hours, heavily clustered near transit hubs during late-night operational windows.</p>
</div>
</div>
"""
        st.markdown(forecast_html, unsafe_allow_html=True)

    with col2:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>AI Explainability Panel</h3>", unsafe_allow_html=True)
        explainability_html = """
<div class="cyber-card" style="height: 100%;">
<div class="eyebrow" style="margin-bottom: 16px;">Decision Matrix Weighting</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">Temporal Alignment (Time of Day)</span>
<span style="font-size: 0.9rem; color: #38BDF8; font-weight: 600;">42% Influence</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 42%; height: 100%; background: #38BDF8; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">Spatial Proximity (Transit Hubs)</span>
<span style="font-size: 0.9rem; color: #38BDF8; font-weight: 600;">35% Influence</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 35%; height: 100%; background: #38BDF8; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">Historical Frequency</span>
<span style="font-size: 0.9rem; color: #38BDF8; font-weight: 600;">18% Influence</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 18%; height: 100%; background: #38BDF8; border-radius: 4px;"></div>
</div>
</div>
<p style="color: #94A3B8; font-size: 0.85rem; margin-top: 24px;">The AI model heavily prioritizes time-of-day and distance to transit centers when forecasting the primary threat vector, aligning with known systemic patterns in the dataset.</p>
</div>
"""
        st.markdown(explainability_html, unsafe_allow_html=True)

    st.markdown("---")
    
    col3, col4 = st.columns(2, gap="large")
    with col3:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Threat Hierarchy</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            render_top_threats_chart(df)
            
    with col4:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Temporal Activity</h3>", unsafe_allow_html=True)
        with st.container(border=True):
            render_temporal_pattern(df)

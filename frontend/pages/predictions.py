import streamlit as st

def render_predictions():
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Advanced Machine Learning</span>
<h1>Predictive Analytics</h1>
<p>Simulating future incident probabilities using deep learning models trained on historical spatial-temporal graphs.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    st.info("Predictive Models are currently running in high-fidelity simulation mode.")
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>72-Hour Anomaly Forecast</h3>", unsafe_allow_html=True)
        forecast_html = """
<div class="cyber-card" style="padding: 24px; border-top: 4px solid #38BDF8;">
<div style="display: flex; justify-content: space-between; margin-bottom: 16px;">
<span style="font-weight: 600; color: #F8FAFC;">District 9 Sector</span>
<span style="color: #EF4444; font-weight: 700;">84% Probability</span>
</div>
<p style="color: #94A3B8; font-size: 0.9rem;">Elevated risk of coordinated theft based on incoming weather patterns and local transit schedules.</p>
<div style="margin-top: 16px; border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 16px;">
<span class="mission-pill" style="color: #38BDF8; border-color: #38BDF8; background: rgba(56, 189, 248, 0.1);">Allocate Patrols</span>
</div>
</div>
"""
        st.markdown(forecast_html, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Model Confidence Scores</h3>", unsafe_allow_html=True)
        scores_html = """
<div class="cyber-card" style="padding: 24px;">
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">Random Forest (Baseline)</span>
<span style="font-size: 0.9rem; color: #10B981; font-weight: 600;">82%</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 82%; height: 100%; background: #10B981; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">XGBoost (Optimized)</span>
<span style="font-size: 0.9rem; color: #10B981; font-weight: 600;">88%</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 88%; height: 100%; background: #10B981; border-radius: 4px;"></div>
</div>
</div>
<div style="margin-bottom: 16px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
<span style="font-size: 0.9rem; color: #F8FAFC;">Spatio-Temporal GNN (Active)</span>
<span style="font-size: 0.9rem; color: #38BDF8; font-weight: 600;">94%</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 4px;">
<div style="width: 94%; height: 100%; background: #38BDF8; border-radius: 4px;"></div>
</div>
</div>
</div>
"""
        st.markdown(scores_html, unsafe_allow_html=True)


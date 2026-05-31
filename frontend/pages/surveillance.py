import streamlit as st

def render_surveillance():
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Live Feed Integration</span>
<h1>Surveillance Hub</h1>
<p>Monitoring active CCTV nodes. Computer vision models are running in the background to detect anomalies in real-time.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    st.info("Surveillance feeds are operating in simulation mode for demonstration purposes.")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        feed1_html = """
<div style="border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; overflow: hidden; position: relative;">
<div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #10B981; border: 1px solid #10B981; display: flex; align-items: center; gap: 6px;">
<div style="width: 6px; height: 6px; background: #10B981; border-radius: 50%; box-shadow: 0 0 6px #10B981;"></div>
LIVE - NODE A4
</div>
<div style="position: absolute; bottom: 12px; right: 12px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #F8FAFC;">
14:22:15.034
</div>
<div style="height: 300px; background: repeating-linear-gradient(0deg, #0f172a, #0f172a 1px, #1e293b 1px, #1e293b 2px); display: flex; align-items: center; justify-content: center;">
<div style="color: #94A3B8; font-family: monospace; text-align: center;">
<div style="font-size: 1.5rem; margin-bottom: 8px; color: #38BDF8;">[ SIMULATED CCTV ANALYTICS ]</div>
<div style="font-size: 0.9rem; color: #94A3B8;">DEMO MODE ACTIVE</div>
</div>
</div>
</div>
"""
        st.markdown(feed1_html, unsafe_allow_html=True)
        
    with col2:
        feed2_html = """
<div style="border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; overflow: hidden; position: relative;">
<div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #10B981; border: 1px solid #10B981; display: flex; align-items: center; gap: 6px;">
<div style="width: 6px; height: 6px; background: #10B981; border-radius: 50%; box-shadow: 0 0 6px #10B981;"></div>
LIVE - NODE B7
</div>
<div style="position: absolute; top: 12px; right: 12px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8rem; color: #F59E0B; border: 1px solid #F59E0B;">
ANOMALY DETECTED: 88%
</div>
<div style="height: 300px; background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); display: flex; align-items: center; justify-content: center; position: relative; padding: 20px;">
<div style="text-align: center;">
<div style="color: #F59E0B; font-weight: bold; margin-bottom: 8px;">DEMO COMPUTER VISION MODULE</div>
<div style="color: #94A3B8; font-size: 0.9rem; max-width: 250px; margin: 0 auto;">Illustrative example of anomaly detection using CCTV streams.<br><br>(Not connected to a live model.)</div>
</div>
</div>
</div>
"""
        st.markdown(feed2_html, unsafe_allow_html=True)

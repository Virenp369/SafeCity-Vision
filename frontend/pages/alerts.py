import streamlit as st
import pandas as pd
from datetime import datetime
import random

def render_alerts(df):
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Real-Time Incident Stream</span>
<h1>Alert Center</h1>
<p>Live feed of categorized alerts and anomalous events requiring dispatcher attention.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    if df.empty:
        st.info("No dataset loaded. Upload a CSV or enable Demo Mode in Settings.")
        return

    st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Active Dispatch Queue</h3>", unsafe_allow_html=True)
    
    # We will simulate alerts by taking the first 10 rows and categorizing their severity based on crime type
    alerts_df = df.head(10).copy()
    
    for idx, row in alerts_df.iterrows():
        category = str(row.get('Crime_Category', 'UNKNOWN')).upper()
        
        # Determine Severity Color
        if any(w in category for w in ['MURDER', 'ASSAULT', 'RAPE', 'ROBBERY', 'KIDNAPPING']):
            color = "#EF4444" # Red
            severity = "CRITICAL"
            response = "Deploy armed response units. Establish 2-block perimeter."
        elif any(w in category for w in ['THEFT', 'BURGLARY', 'NARCOTICS', 'FRAUD']):
            color = "#F59E0B" # Amber
            severity = "MODERATE"
            response = "Dispatch patrol unit for investigation and report."
        else:
            color = "#38BDF8" # Blue
            severity = "ROUTINE"
            response = "Log incident and schedule community officer follow-up."
            
        location = f"{row.get('Latitude', '0.0'):.4f}, {row.get('Longitude', '0.0'):.4f}" if 'Latitude' in row and 'Longitude' in row else "Sector Unknown"
        time_str = f"{row.get('Hour', '00'):02d}:00 HRS" if 'Hour' in row else datetime.now().strftime('%H:%M HRS')
            
        alert_html = f"""
<div class="cyber-card" style="padding: 16px; margin-bottom: 0px; border-bottom-left-radius: 0; border-bottom-right-radius: 0; border-left: 4px solid {color}; display: flex; justify-content: space-between; align-items: center;">
<div>
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
<span class="eyebrow" style="color: {color} !important; margin: 0;">{severity}</span>
<span style="color: #94A3B8; font-family: monospace; font-size: 0.8rem;">{time_str}</span>
<span style="color: #10B981; font-family: monospace; font-size: 0.8rem; border: 1px solid #10B981; padding: 1px 4px; border-radius: 2px;">STATUS: OPEN</span>
</div>
<div style="font-size: 1.1rem; font-weight: 600; color: #F8FAFC;">{category} IN PROGRESS</div>
<div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Coordinates: {location}</div>
</div>
</div>
"""
        st.markdown(alert_html, unsafe_allow_html=True)
        
        with st.expander("VIEW INCIDENT DETAILS"):
            st.markdown(f"""
            **Incident Type:** {category}  
            **Severity:** {severity}  
            **Status:** OPEN  
            **Timestamp:** {time_str}  
            **Location:** {location}  
            **Recommended Response:** {response}  
            **Analyst Notes:** Simulated alert generated based on historical dataset anomalies. No active units are currently assigned.
            """)
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


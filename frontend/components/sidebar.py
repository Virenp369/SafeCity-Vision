import streamlit as st
from streamlit_option_menu import option_menu

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div class='brand-lockup' style='margin-bottom: 4px; font-size: 1.8rem;'>SAFE CITY<br><span>VISION</span></div>
            <div style='color: #94A3B8; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase;'>Safer Cities. Smarter Tomorrow.</div>
            <div style='display: flex; align-items: center; gap: 8px; margin-top: 12px;'>
                <div style='width: 8px; height: 8px; background-color: #10B981; border-radius: 50%; box-shadow: 0 0 8px #10B981;'></div>
                <div style='color: #10B981; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;'>Command Node Active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        selected = option_menu(
            menu_title=None,
            options=[
                "Overview", 
                "Threat Intelligence", 
                "Crime Analytics", 
                "Predictions", 
                "Surveillance", 
                "AI Copilot", 
                "Alerts", 
                "Settings"
            ],
            icons=[
                "house", 
                "shield-exclamation", 
                "geo-alt", 
                "graph-up-arrow", 
                "camera-video", 
                "robot", 
                "lightning", 
                "gear"
            ],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#38BDF8", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "--hover-color": "rgba(56, 189, 248, 0.1)",
                    "color": "#94A3B8"
                },
                "nav-link-selected": {
                    "background-color": "rgba(56, 189, 248, 0.15)",
                    "color": "#F8FAFC",
                    "font-weight": "600",
                    "border-left": "3px solid #38BDF8"
                },
            }
        )

        st.markdown("---")
        
        if st.session_state.get('demo_mode', False):
            st.info("Demo Mode Active: Using simulated high-fidelity data.")

        return selected


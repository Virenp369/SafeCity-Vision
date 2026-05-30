import streamlit as st
import textwrap

from frontend.components.cards import render_recommendation_card, render_tactical_metrics
from frontend.components.charts import render_temporal_pattern, render_top_threats_chart
from frontend.services.ai_service import get_ai_summary, check_gemini_connection
from frontend.services.map_service import render_heatmap
from frontend.utils.insights import filter_data, generate_operational_summary, risk_score, top_recommendations, generate_local_intelligence


def render_dashboard(df, current_context, api_key):
    source = st.session_state.get("active_source", current_context)
    
    is_connected = check_gemini_connection(api_key) if api_key else False
    
    if is_connected and not df.empty:
        status_indicator = "🟢 AI + Dataset Intelligence"
    elif not is_connected and not df.empty:
        status_indicator = "🟡 Dataset Intelligence Only"
    else:
        status_indicator = "🔴 Intelligence Services Offline"
    
    header_html = f"""
<section class="mission-header">
<div>
<span class="eyebrow">Forensic Intelligence Node</span>
<h1>SafeCity Vision</h1>
<p>Live pattern analysis for {source}. Monitor concentration, timing, and threat composition before risk becomes operational pressure.</p>
</div>
<div class="mission-pill">{status_indicator}</div>
</section>
"""
    st.markdown(header_html, unsafe_allow_html=True)

    if df.empty:
        st.info("No records available. Initialize an uplink or upload a CSV from the sidebar.")
        return

    filtered_df = _render_filters(df)
    render_tactical_metrics(filtered_df, current_context)

    summary = generate_operational_summary(filtered_df, current_context)
    recommendations = top_recommendations(filtered_df)
    render_recommendation_card(summary, recommendations, risk_score(filtered_df))

    map_col, context_col = st.columns([1.55, 1], gap="large")
    with map_col:
        st.markdown("<div style='margin-bottom: 16px;'><span class='eyebrow'>Geospatial View</span><h3 style='margin: 0; font-size: 1.4rem;'>Tactical Heatmap</h3></div>", unsafe_allow_html=True)
        render_heatmap(filtered_df, current_context, height=620)

    with context_col:
        st.markdown("<div style='margin-bottom: 12px;'><span class='eyebrow'>Composition</span><h3 style='margin: 0; font-size: 1.25rem;'>Threat Hierarchy</h3></div>", unsafe_allow_html=True)
        render_top_threats_chart(filtered_df)
        st.markdown("<div style='margin-top: 24px; margin-bottom: 12px;'><span class='eyebrow'>Timeline</span><h3 style='margin: 0; font-size: 1.25rem;'>Temporal Signal</h3></div>", unsafe_allow_html=True)
        render_temporal_pattern(filtered_df)

    st.markdown("---")
    briefing_col, data_col = st.columns([1, 1.2], gap="large")

    with briefing_col:
        st.markdown("<div style='margin-bottom: 16px;'><span class='eyebrow'>Gemini Flash-1.5</span><h3 style='margin: 0; font-size: 1.4rem;'>AI Intelligence Briefing</h3></div>", unsafe_allow_html=True)
        if api_key and is_connected:
            with st.spinner("Generating analyst summary..."):
                summary_cols = [column for column in ['Crime_Category', 'Hour', 'DayOfWeek', 'Dist_to_Transit'] if column in filtered_df.columns]
                df_summary = filtered_df[summary_cols].describe(include='all').to_string() if summary_cols else "No summary columns available."
                briefing = get_ai_summary(api_key, df_summary)
                if not briefing:
                    st.warning("⚠️ Gemini connection lost. Entering fallback mode.")
                    briefing = generate_local_intelligence(filtered_df)
                st.info(briefing)
        else:
            if not api_key:
                st.warning("Add GEMINI_API_KEY in .env to enable generated briefings.")
            else:
                st.warning("⚠️ AI Intelligence is unavailable. Operating in local mode.")
            st.info(generate_local_intelligence(filtered_df))

    with data_col:
        st.markdown("<div style='margin-bottom: 16px;'><span class='eyebrow'>Raw Intercepts</span><h3 style='margin: 0; font-size: 1.4rem;'>Evidence Feed</h3></div>", unsafe_allow_html=True)
        display_cols = ['Timestamp', 'City', 'Crime_Category', 'Latitude', 'Longitude']
        display_cols = [column for column in display_cols if column in filtered_df.columns]
        st.dataframe(filtered_df[display_cols].head(75), height=330, use_container_width=True)


def _render_filters(df):
    with st.container(border=True):
        col1, col2 = st.columns([1.3, 1])
        with col1:
            categories = []
            if "Crime_Category" in df.columns:
                category_options = sorted(df["Crime_Category"].dropna().astype(str).unique().tolist())
                categories = st.multiselect("Filter Threat Classes", category_options, default=category_options[:8])
        with col2:
            hour_range = None
            if "Hour" in df.columns:
                hour_range = st.slider("Operational Hour Window", 0, 23, (0, 23))

    return filter_data(df, categories, hour_range)

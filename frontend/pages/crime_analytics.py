import streamlit as st
import plotly.express as px
from frontend.services.map_service import render_heatmap
from frontend.utils.insights import filter_data

def render_crime_analytics(df, current_context):
    header_html = """
<div class="mission-header" style="margin-bottom: 32px;">
<div>
<span class="eyebrow">Spatial & Temporal Analysis</span>
<h1>Crime Analytics</h1>
<p>Interact with geospatial data to locate hotspots and trace temporal trends over the operational period.</p>
</div>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)

    if df.empty:
        st.info("No dataset loaded. Upload a CSV or enable Demo Mode in Settings.")
        return

    st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Geospatial Heatmap</h3>", unsafe_allow_html=True)
    
    with st.container(border=True):
        col1, col2, col3 = st.columns([1, 1, 0.5])
        with col1:
            categories = []
            if "Crime_Category" in df.columns:
                category_options = sorted(df["Crime_Category"].dropna().astype(str).unique().tolist())
                categories = st.multiselect("Threat Classes", category_options, default=category_options[:5])
        with col2:
            hour_range = None
            if "Hour" in df.columns:
                hour_range = st.slider("Operational Hour Window", 0, 23, (0, 23))
        with col3:
            map_mode = st.radio("Map Mode", ["Heatmap", "Clusters"], horizontal=True)

    filtered_df = filter_data(df, categories, hour_range)
    
    if filtered_df.empty:
        st.warning("No incidents match the current filters.")
    else:
        with st.container(border=True):
            render_heatmap(filtered_df, current_context, height=650, mode=map_mode.lower())

    st.markdown("---")
    
    st.markdown("<h3 style='margin-bottom: 16px; font-size: 1.25rem;'>Crime Trend Timeline</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        if filtered_df.empty:
            st.info("No valid records available for the selected filters.")
        elif 'Hour' in filtered_df.columns and 'Crime_Category' in filtered_df.columns:
            trend_df = filtered_df.groupby(['Hour', 'Crime_Category']).size().reset_index(name='Count')
            fig = px.line(
                trend_df, x='Hour', y='Count', color='Crime_Category',
                title="Incident Volume by Hour and Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94A3B8", family="Inter, sans-serif"),
                title_font=dict(size=16, color="#f1f5f9", family="Outfit, sans-serif"),
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis=dict(dtick=2, showgrid=False, title="Hour of Day"),
                yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)", title="Incident Count"),
                hovermode="x unified",
                legend_title_text=""
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Insufficient data to render timeline.")

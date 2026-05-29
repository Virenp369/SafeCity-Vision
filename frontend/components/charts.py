import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def render_top_threats_chart(df):
    if df.empty or 'Crime_Category' not in df.columns:
        st.info("Threat chart will appear once crime category data is available.")
        return

    top_crimes = df['Crime_Category'].value_counts().head(5).reset_index()
    top_crimes.columns = ['Crime', 'Count']
    fig = px.bar(
        top_crimes,
        x='Count',
        y='Crime',
        orientation='h',
        title="Dominant Incident Classes",
        color='Count',
        color_continuous_scale=["rgba(45, 212, 191, 0.6)", "rgba(45, 212, 191, 1)"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Inter, sans-serif"),
        title_font=dict(size=16, color="#f1f5f9", family="Outfit, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
        yaxis=dict(autorange="reversed", showgrid=False, title=""),
        xaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)", title="Incident Volume"),
        coloraxis_showscale=False,
    )
    fig.update_traces(marker_line_width=0, opacity=0.9)
    st.plotly_chart(fig, use_container_width=True)


def render_temporal_pattern(df):
    if df.empty or 'Hour' not in df.columns:
        st.info("Temporal pattern will appear once timestamp data is available.")
        return

    hourly = df.groupby('Hour').size().reset_index(name='Incidents')
    fig = px.area(hourly, x='Hour', y='Incidents', title="24-Hour Incident Rhythm")
    
    fig.update_traces(
        line_color="#38BDF8", 
        fillcolor="rgba(56, 189, 248, 0.15)",
        line=dict(width=3)
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Inter, sans-serif"),
        title_font=dict(size=16, color="#f1f5f9", family="Outfit, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(dtick=3, showgrid=False, title="Hour of Day"),
        yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)", title="Activity Level"),
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_risk_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Sector Risk Score", 'font': {'color': '#94A3B8', 'size': 16, 'family': 'Outfit, sans-serif'}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.1)"},
            'bar': {'color': "#2DD4BF"},
            'bgcolor': "rgba(15, 23, 42, 0.4)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': "rgba(16, 185, 129, 0.15)"},
                {'range': [40, 75], 'color': "rgba(245, 158, 11, 0.15)"},
                {'range': [75, 100], 'color': "rgba(239, 68, 68, 0.15)"}],
        },
        number = {'font': {'color': '#f1f5f9', 'family': 'Outfit, sans-serif', 'weight': 'bold'}}
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#94A3B8"), height=260, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

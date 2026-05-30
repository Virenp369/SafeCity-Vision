import streamlit as st
import textwrap

from frontend.utils.insights import risk_band, risk_score


def _render_custom_metric(col, label, value, delta=None):
    delta_html = f"<div style='color: var(--accent-teal); font-size: 0.85rem; margin-top: 4px; font-weight: 600;'>{delta}</div>" if delta else ""
    html = f"""
<div class="tactical-metric-card">
<div class="tactical-metric-label">{label}</div>
<div class="tactical-metric-value">{value}</div>
{delta_html}
</div>
"""
    col.markdown(html, unsafe_allow_html=True)


def render_tactical_metrics(df, current_context):
    score = risk_score(df)
    band, _ = risk_band(score)
    m1, m2, m3, m4 = st.columns(4)
    
    _render_custom_metric(m1, "Reports Analyzed", f"{len(df):,}")
    _render_custom_metric(m2, "Risk Posture", band, f"{score}/100")

    if df.empty:
        _render_custom_metric(m3, "Primary Threat", "N/A")
        _render_custom_metric(m4, "High-Risk Nodes", "0")
        return

    primary = _safe_mode(df, "Crime_Category", "Unknown")
    high_risk_nodes = len(df[df['Dist_to_Transit'] < 1.0]) if 'Dist_to_Transit' in df.columns else 0

    if "INDIA" in current_context and "City" in df.columns:
        _render_custom_metric(m3, "Priority Hub", _safe_mode(df, "City", "Unknown"))
        _render_custom_metric(m4, "Dominant IPC Class", _short(primary))
    else:
        _render_custom_metric(m3, "Primary Threat", _short(str(primary).title()))
        _render_custom_metric(m4, "High-Risk Nodes", f"{high_risk_nodes:,}")


def render_recommendation_card(summary, recommendations, score):
    band, color = risk_band(score)
    items = "".join(f"<li>{item}</li>" for item in recommendations)
    card_html = f"""
<section class="intel-brief" style="border-left-color: {color};">
<div class="brief-kicker" style="color: {color};">Operational Brief</div>
<h3 style="color: #f1f5f9;">{band} Risk Environment</h3>
<p>{summary}</p>
<ul>{items}</ul>
</section>
"""
    st.markdown(card_html, unsafe_allow_html=True)


def _safe_mode(df, column, fallback):
    if column not in df.columns or df[column].dropna().empty:
        return fallback
    return df[column].mode().iat[0]


def _short(value):
    value = str(value)
    return value[:22] + "..." if len(value) > 22 else value

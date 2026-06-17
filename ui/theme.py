import streamlit as st

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(135deg, #5c3a1e 0%, #7a4b24 45%, #996132 100%);
    color: #ffffff;
    padding: 1.75rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.25rem;
    box-shadow: 0 10px 30px rgba(61, 35, 20, 0.18);
}

.hero h1 {
    color: #fff !important;
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0 0 0.35rem 0;
}

.hero p {
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    font-size: 1rem;
    line-height: 1.5;
}

.disclaimer {
    background: color-mix(in srgb, var(--secondary-background-color) 85%, transparent);
    border: 1px solid color-mix(in srgb, var(--text-color) 18%, transparent);
    color: var(--text-color);
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
}

.kpi-card {
    background: color-mix(in srgb, var(--secondary-background-color) 88%, transparent);
    border: 1px solid color-mix(in srgb, var(--text-color) 14%, transparent);
    border-radius: 14px;
    padding: 1.25rem 1.35rem;
    text-align: center;
    height: 100%;
}

.kpi-label {
    color: color-mix(in srgb, var(--text-color) 72%, transparent);
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.kpi-value {
    color: var(--text-color);
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.1;
    margin-top: 0.35rem;
}

.kpi-sub {
    color: color-mix(in srgb, var(--text-color) 72%, transparent);
    font-size: 0.82rem;
    margin-top: 0.35rem;
}

.result-card {
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    border: 1px solid transparent;
    height: 100%;
}

.result-card.severe { background: #fff1f1; border-color: #f3b8b8; }
.result-card.moderate { background: #fff8eb; border-color: #f0d39b; }
.result-card.normal { background: #eefaf1; border-color: #b9e3c3; }

.result-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 0.35rem;
}

.result-badge {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 0.65rem;
}

.badge-severe { background: #dc3545; color: #fff; }
.badge-moderate { background: #e0a800; color: #fff; }
.badge-normal { background: #198754; color: #fff; }

.result-message {
    font-size: 0.92rem;
    color: color-mix(in srgb, var(--text-color) 84%, transparent);
    margin: 0.35rem 0 0.75rem 0;
}

.confidence-label {
    font-size: 0.8rem;
    color: color-mix(in srgb, var(--text-color) 72%, transparent);
    margin-bottom: 0.2rem;
}

.confidence-track {
    background: color-mix(in srgb, var(--secondary-background-color) 65%, transparent);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
}

.confidence-fill { height: 8px; border-radius: 999px; }
.fill-severe { background: #dc3545; }
.fill-moderate { background: #e0a800; }
.fill-normal { background: #198754; }

.agreement {
    border-radius: 12px;
    padding: 0.85rem 1rem;
    margin-top: 0.75rem;
    font-size: 0.92rem;
}

.agreement.match { background: #eefaf1; border: 1px solid #b9e3c3; color: #1f5d34; }
.agreement.mismatch { background: #eef4ff; border: 1px solid #b8cff5; color: #214f8a; }

.metric-tile {
    background: color-mix(in srgb, var(--secondary-background-color) 82%, transparent);
    border: 1px solid color-mix(in srgb, var(--text-color) 14%, transparent);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    height: 100%;
}

.metric-tile .label {
    color: color-mix(in srgb, var(--text-color) 68%, transparent);
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.metric-tile .value {
    color: var(--text-color);
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.2rem;
}

.stTabs [data-baseweb="tab-list"] { gap: 0.35rem; }

.stTabs [data-baseweb="tab"] {
    background: color-mix(in srgb, var(--secondary-background-color) 78%, transparent);
    color: color-mix(in srgb, var(--text-color) 82%, transparent) !important;
    border: 1px solid color-mix(in srgb, var(--text-color) 14%, transparent);
    border-bottom: none;
    border-radius: 10px 10px 0 0;
    padding: 0.55rem 1rem;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"] * {
    color: color-mix(in srgb, var(--text-color) 82%, transparent) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--background-color) !important;
    color: var(--text-color) !important;
    border-color: color-mix(in srgb, var(--text-color) 24%, transparent) !important;
}

.stTabs [aria-selected="true"] * {
    color: var(--text-color) !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: color-mix(in srgb, var(--background-color) 90%, transparent);
    border-color: color-mix(in srgb, var(--text-color) 14%, transparent) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6b3e1e 0%, #8b5a2b 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.7rem 1rem;
    box-shadow: 0 6px 16px rgba(107, 62, 30, 0.22);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #7a4824 0%, #9a6833 100%);
    color: white;
}

h2, h3, h4 { color: #4a2f18 !important; }

.warning-chip {
    background: color-mix(in srgb, #d98f00 12%, var(--secondary-background-color));
    border: 1px solid color-mix(in srgb, #d98f00 36%, transparent);
    color: var(--text-color);
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    font-size: 0.86rem;
    margin-top: 0.5rem;
}
"""


def inject_theme() -> None:
    st.markdown(f"<style>{BASE_CSS}</style>", unsafe_allow_html=True)

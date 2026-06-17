import streamlit as st

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #2f2419;
}

:root {
    --background-color: #f8f5f0;
    --secondary-background-color: #f4efe8;
    --text-color: #2f2419;
}

.stApp, [data-testid="stAppViewContainer"] {
    background-color: #f8f5f0;
    color: #2f2419;
}

[data-testid="stSidebar"] {
    background-color: #f4efe8;
    border-right: 1px solid #e2d4c3;
}

[data-testid="stSidebar"] * {
    color: #3e2f21 !important;
}

/* Force light widget surfaces */
[data-baseweb="input"],
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background: #fffdfa !important;
    border-color: #d8c8b6 !important;
}

[data-baseweb="input"] input,
[data-baseweb="select"] input,
[data-baseweb="select"] span {
    color: #2f2419 !important;
}

[data-testid="stNumberInput"] button,
[data-testid="stSelectbox"] button {
    color: #2f2419 !important;
}

[data-testid="stSlider"] [role="slider"] {
    background: #8b5a2b !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #d8c8b6 !important;
}

/* Force light dataframes/tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #fffdfa !important;
    color: #2f2419 !important;
    border-radius: 10px;
}

[data-testid="stDataFrame"] * ,
[data-testid="stTable"] * {
    color: #2f2419 !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(135deg, #3d2314 0%, #6b3e1e 45%, #8b5a2b 100%);
    color: #fff;
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
    background: #fff8ef;
    border: 1px solid #edd9c2;
    color: #5c3d1e;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.9rem;
    margin-bottom: 1.25rem;
}

.kpi-card {
    background: linear-gradient(180deg, #fffaf4 0%, #fff4e8 100%);
    border: 1px solid #edd9c2;
    border-radius: 14px;
    padding: 1.25rem 1.35rem;
    text-align: center;
    height: 100%;
}

.kpi-label {
    color: #7a5a3d;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.kpi-value {
    color: #3d2314;
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.1;
    margin-top: 0.35rem;
}

.kpi-sub {
    color: #8a6f55;
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
    color: #4a2f18;
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
    color: #4a3424;
    margin: 0.35rem 0 0.75rem 0;
}

.confidence-label {
    font-size: 0.8rem;
    color: #6f5a47;
    margin-bottom: 0.2rem;
}

.confidence-track {
    background: #efe6db;
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
    background: #fff;
    border: 1px solid #ece4da;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    height: 100%;
}

.metric-tile .label {
    color: #7a6553;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.metric-tile .value {
    color: #3d2314;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.2rem;
}

.stTabs [data-baseweb="tab-list"] { gap: 0.35rem; }

.stTabs [data-baseweb="tab"] {
    background: #f7f1ea;
    color: #6b4a2c !important;
    border: 1px solid #e2d4c3;
    border-bottom: none;
    border-radius: 10px 10px 0 0;
    padding: 0.55rem 1rem;
    font-weight: 600;
}

.stTabs [data-baseweb="tab"] * {
    color: #6b4a2c !important;
}

.stTabs [aria-selected="true"] {
    background: #fff !important;
    color: #4a2f18 !important;
    border-color: #d7c3ad !important;
}

.stTabs [aria-selected="true"] * {
    color: #4a2f18 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fffdfa;
    border-color: #e7dcca !important;
}

.stButton>button {
    background: linear-gradient(135deg, #6b3e1e 0%, #8b5a2b 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.7rem 1rem;
    box-shadow: 0 6px 16px rgba(107, 62, 30, 0.22);
}

.stButton>button:hover {
    background: linear-gradient(135deg, #7a4824 0%, #9a6833 100%);
    color: white;
}

h2, h3, h4 { color: #4a2f18 !important; }

.warning-chip {
    background: #fff4e5;
    border: 1px solid #f0d39b;
    color: #7a4d00;
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    font-size: 0.86rem;
    margin-top: 0.5rem;
}
"""

DARK_CSS = """
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #141210;
    color: #f2ebe3;
}

:root {
    --background-color: #141210;
    --secondary-background-color: #1c1814;
    --text-color: #f2ebe3;
}

[data-testid="stSidebar"] {
    background-color: #1c1814;
    border-right: 1px solid #3a322a;
}

[data-testid="stSidebar"] * {
    color: #f2ebe3 !important;
}

/* Dark widget surfaces */
[data-baseweb="input"],
[data-baseweb="select"] > div,
[data-baseweb="base-input"] {
    background: #231d17 !important;
    border-color: #4a3d2f !important;
}

[data-baseweb="input"] input,
[data-baseweb="select"] input,
[data-baseweb="select"] span,
[data-testid="stNumberInput"] button,
[data-testid="stSelectbox"] button {
    color: #f2ebe3 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background: #4a3d2f !important;
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #1f1a15 !important;
    color: #f2ebe3 !important;
}

[data-testid="stDataFrame"] * ,
[data-testid="stTable"] * {
    color: #f2ebe3 !important;
}

.disclaimer {
    background: #2a2219;
    border-color: #4a3d2f;
    color: #e8d8c4;
}

.kpi-card {
    background: linear-gradient(180deg, #221c16 0%, #2a2219 100%);
    border-color: #4a3d2f;
}

.kpi-label, .kpi-sub { color: #c4b5a3; }
.kpi-value, .metric-tile .value { color: #f7efe6; }

.metric-tile {
    background: #1f1a15;
    border-color: #3a322a;
}

.metric-tile .label { color: #b8a894; }

.result-title { color: #f2ebe3; }
.result-message { color: #d9cbb9; }
.confidence-label { color: #b8a894; }
.confidence-track { background: #3a322a; }

.result-card.severe { background: #3a1f22; border-color: #7a3a42; }
.result-card.moderate { background: #3a2f14; border-color: #7a5e22; }
.result-card.normal { background: #1a2e22; border-color: #2f6b4a; }

.agreement.match { background: #1a2e22; border-color: #2f6b4a; color: #b9e3c3; }
.agreement.mismatch { background: #1a2438; border-color: #3a5f8a; color: #b8cff5; }

.warning-chip {
    background: #3a2f14;
    border-color: #7a5e22;
    color: #f0d39b;
}

h2, h3, h4 { color: #f2ebe3 !important; }

.stTabs [data-baseweb="tab"] {
    background: #221c16;
    color: #d9cbb9 !important;
    border: 1px solid #3a322a;
    border-bottom: none;
}

.stTabs [data-baseweb="tab"] * {
    color: #d9cbb9 !important;
}

.stTabs [aria-selected="true"] {
    background: #2a2219 !important;
    color: #f7efe6 !important;
    border-color: #4a3d2f !important;
}

.stTabs [aria-selected="true"] * {
    color: #f7efe6 !important;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #1f1a15;
    border-color: #3a322a !important;
}
"""


def inject_theme(dark_mode: bool = False) -> None:
    css = f"<style>{BASE_CSS}"
    if dark_mode:
        css += DARK_CSS
    css += "</style>"
    st.markdown(css, unsafe_allow_html=True)

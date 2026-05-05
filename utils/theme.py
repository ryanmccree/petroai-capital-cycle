"""
utils/theme.py
Injects the dark slate finance theme CSS into the Streamlit app.
"""

import streamlit as st

# Unsplash image URLs per stage (mirrored from state.py for CSS generation)
_STAGE_CSS = [
    ("energy",      "#FF6B2B", "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&q=80"),
    ("power",       "#FFD700", "https://images.unsplash.com/photo-1548337138-e87d889cc369?w=800&q=80"),
    ("grid",        "#00D4FF", "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=800&q=80"),
    ("compute",     "#4D9FFF", "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80"),
    ("transfer",    "#00FF94", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80"),
    ("ai",          "#B44DFF", "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&q=80"),
    ("defense",     "#FF3B3B", "https://images.unsplash.com/photo-1521694468822-1e20e3f1b68e?w=800&q=80"),
    ("sovereignty", "#FF9500", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=80"),
]

def _stage_image_css() -> str:
    rules = []
    for key, color, url in _STAGE_CSS:
        rules.append(
            f".si-{key} {{"
            f"background:linear-gradient(rgba(15,17,23,0.78),rgba(15,17,23,0.78)),url('{url}') center/cover no-repeat;"
            f"border-color:{color}40;}}"
            f".si-{key}:hover {{"
            f"background:linear-gradient(rgba(15,17,23,0.52),rgba(15,17,23,0.52)),url('{url}') center/cover no-repeat;"
            f"}}"
            f".si-{key}.active-img-card {{"
            f"border:2px solid {color};"
            f"box-shadow:0 0 24px {color}50;}}"
        )
    return "\n".join(rules)


def inject_css():
    stage_img_css = _stage_image_css()
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;600;700&display=swap');

        /* ── CSS custom properties ── */
        :root {{
            --bg:        #0f1117;
            --card-bg:   #1a1d27;
            --border:    #2a2d3e;
            --text-1:    #ffffff;
            --text-2:    #c8ccd8;
            --text-3:    #9da3b4;
            --ease:      0.2s ease;
        }}

        /* ── Base ── */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: var(--bg) !important;
            color: var(--text-1) !important;
            font-family: 'DM Sans', sans-serif;
            font-size: 1rem;
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background-color: #13151f !important;
            border-right: 1px solid var(--border) !important;
            min-width: 240px !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #c0c8d8 !important;
            font-size: 0.95rem;
        }}
        [data-testid="stSidebar"] h3 {{ color: #FF9500 !important; font-size: 1rem !important; }}

        /* ── Header ── */
        .header-block {{ padding: 0.5rem 0 0.25rem; }}
        .header-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #FF9500;
            letter-spacing: 0.03em;
            margin-bottom: 0.4rem;
            font-family: 'DM Sans', sans-serif;
        }}
        .header-thesis {{
            font-size: 0.88rem;
            line-height: 1.8;
            color: var(--text-2);
            max-width: 900px;
            font-style: italic;
            font-family: 'IBM Plex Mono', monospace;
        }}
        .header-meta {{ text-align: right; padding-top: 0.5rem; }}
        .handle-link {{
            color: #FF9500 !important;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.95rem;
        }}
        .handle-link:hover {{ color: #ffb340 !important; }}
        .last-updated {{ font-size: 0.78rem; color: var(--text-3); margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }}
        .test-badge {{
            display: inline-block;
            background: rgba(255,107,43,0.12);
            color: #FF6B2B;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid #FF6B2B;
            margin-top: 6px;
            letter-spacing: 0.1em;
            font-family: 'IBM Plex Mono', monospace;
        }}
        .header-divider {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 0.5rem 0 1rem;
        }}

        /* ── Tabs ── */
        [data-testid="stTabs"] button {{
            color: #8890a8 !important;
            font-size: 1rem !important;
            font-family: 'DM Sans', sans-serif !important;
            transition: color var(--ease) !important;
        }}
        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: #ffffff !important;
            border-bottom-color: #FF9500 !important;
        }}

        /* ── Section headers ── */
        .section-header {{
            font-size: 0.85rem;
            font-weight: 700;
            color: #a0a8bc;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.9rem;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
            font-family: 'IBM Plex Mono', monospace;
        }}

        /* ── Base stage card (no image) ── */
        .stage-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 10px;
            font-size: 0.95rem;
            min-height: 110px;
            transition: all var(--ease);
            box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }}
        .stage-card:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        }}
        .stage-card.active-constraint {{
            border: 2px solid #FF9500;
            box-shadow: 0 0 24px 4px rgba(255,149,0,0.28);
            background: rgba(255,149,0,0.05);
        }}
        .stage-name {{
            font-weight: 700;
            font-size: 1.2rem;
            color: var(--text-1);
            margin-bottom: 4px;
            font-family: 'DM Sans', sans-serif;
        }}
        .stage-card.active-constraint .stage-name {{ color: #FF9500; }}
        .stage-desc {{
            color: #b0b8cc;
            font-size: 0.9rem;
            margin-top: 4px;
            line-height: 1.5;
            font-family: 'IBM Plex Mono', monospace;
        }}
        .company-pill {{
            display: inline-block;
            background: rgba(255,255,255,0.10);
            color: #ffffff;
            font-size: 0.85rem;
            padding: 3px 8px;
            border-radius: 4px;
            margin: 4px 3px 0 0;
            border: 1px solid var(--border);
            font-weight: 600;
            font-family: 'IBM Plex Mono', monospace;
            transition: all var(--ease);
        }}
        .active-constraint .company-pill {{
            background: rgba(255,149,0,0.15);
            color: #ffffff;
            border-color: rgba(255,149,0,0.4);
        }}

        /* ── Stage image cards ── */
        .stage-img-card {{
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 10px;
            min-height: 160px;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border);
            transition: all var(--ease);
            box-shadow: 0 2px 12px rgba(0,0,0,0.35);
            cursor: default;
        }}
        .stage-img-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 28px rgba(0,0,0,0.55);
        }}

        /* Per-stage image + hover variants */
        {stage_img_css}

        /* ── Responsive stat grid ── */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }}

        /* ── Horizontal flow scroll wrapper ── */
        .flow-scroll-container {{
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}

        /* ── Buttons ── */
        [data-testid="stButton"] button {{
            font-family: 'IBM Plex Mono', monospace !important;
            border-radius: 8px !important;
            font-size: 0.9rem !important;
            transition: all var(--ease) !important;
        }}
        [data-testid="stButton"] button[kind="secondary"] {{
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-2) !important;
        }}
        [data-testid="stButton"] button[kind="secondary"]:hover {{
            background-color: #222535 !important;
            border-color: var(--text-2) !important;
            color: var(--text-1) !important;
        }}
        [data-testid="stButton"] button[kind="primary"] {{
            background-color: rgba(255,149,0,0.12) !important;
            border: 2px solid #FF9500 !important;
            color: #FF9500 !important;
            box-shadow: 0 0 14px rgba(255,149,0,0.35) !important;
        }}

        /* ── Flow arrows ── */
        .flow-arrow {{ text-align:center; color:var(--border); font-size:1.1rem; padding:2px 0; }}
        .flow-arrow.active-arrow {{ color:#FF9500; animation:pulse 1.5s ease-in-out infinite; }}
        @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.4}} }}

        /* ── Footer ── */
        .footer {{
            text-align: center;
            font-size: 0.8rem;
            color: #6a7280;
            padding: 1.5rem 0 0.5rem;
            border-top: 1px solid var(--border);
            margin-top: 2rem;
            font-family: 'IBM Plex Mono', monospace;
        }}

        /* ── Plotly override ── */
        .js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}

        /* ── Alerts ── */
        [data-testid="stAlert"] {{
            background: var(--card-bg) !important;
            border-color: var(--border) !important;
            color: var(--text-2) !important;
            font-size: 0.95rem !important;
        }}

        /* ── Selectbox / radio ── */
        [data-testid="stSelectbox"] > div,
        [data-testid="stRadio"] label {{
            color: var(--text-2) !important;
            font-size: 0.95rem !important;
        }}

        /* ── General markdown text ── */
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-size: 0.95rem;
            color: var(--text-2);
        }}
        .stCaption, [data-testid="stCaptionContainer"] {{
            font-size: 0.85rem !important;
            color: var(--text-3) !important;
        }}

        /* ══════════════════════════════════════════════════════
           MOBILE  (<768px)
        ══════════════════════════════════════════════════════ */
        @media screen and (max-width: 768px) {{
            .header-title  {{ font-size: 1.3rem  !important; }}
            .header-thesis {{ font-size: 0.78rem !important; }}
            .stage-card    {{ min-height: 80px !important; }}
            .stage-img-card {{ min-height: 120px !important; }}
            .company-pill  {{ font-size: 0.72rem !important; padding: 2px 5px !important; }}
            .footer        {{ font-size: 0.72rem !important; }}
            [data-testid="stHorizontalBlock"] {{ flex-wrap: wrap !important; }}
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
                flex: 1 1 100% !important;
                min-width: 100% !important;
                width: 100% !important;
            }}
            .stat-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
            .flow-scroll-container {{ overflow-x: auto !important; -webkit-overflow-scrolling: touch !important; }}
            .flow-scroll-container [data-testid="stPlotlyChart"] .js-plotly-plot {{ min-width: 700px; }}
        }}
        @media screen and (min-width: 480px) and (max-width: 767px) {{
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
                flex: 1 1 48% !important; min-width: 48% !important;
            }}
            .stat-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
        }}
        @media screen and (max-width: 479px) {{
            .stat-grid {{ grid-template-columns: 1fr !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

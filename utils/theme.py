"""
utils/theme.py
Injects the dark-mode finance theme CSS into the Streamlit app.
"""

import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        /* ── Base ── */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0a0e0a !important;
            color: #d4d4c8 !important;
            font-family: 'IBM Plex Mono', 'Courier New', monospace;
        }
        [data-testid="stSidebar"] {
            background-color: #0d120d !important;
            border-right: 1px solid #1a2e1a;
        }
        [data-testid="stSidebar"] * { color: #a8b8a0 !important; }

        /* ── Header ── */
        .header-block {
            padding: 0.5rem 0 0.25rem;
        }
        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f0a500;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }
        .header-thesis {
            font-size: 0.72rem;
            line-height: 1.6;
            color: #7a9e7a;
            max-width: 900px;
            font-style: italic;
        }
        .header-meta {
            text-align: right;
            padding-top: 0.5rem;
        }
        .handle-link {
            color: #f0a500 !important;
            font-weight: 700;
            text-decoration: none;
            font-size: 0.85rem;
        }
        .handle-link:hover { color: #ffc740 !important; }
        .last-updated {
            font-size: 0.65rem;
            color: #4a6e4a;
            margin-top: 4px;
        }
        .test-badge {
            display: inline-block;
            background: #3a1a00;
            color: #f0a500;
            font-size: 0.6rem;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 3px;
            border: 1px solid #f0a500;
            margin-top: 6px;
            letter-spacing: 0.1em;
        }
        .header-divider {
            border: none;
            border-top: 1px solid #1a2e1a;
            margin: 0.5rem 0 1rem;
        }

        /* ── Tabs ── */
        [data-testid="stTabs"] button {
            color: #4a6e4a !important;
            font-size: 0.8rem !important;
            font-family: 'IBM Plex Mono', monospace !important;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #f0a500 !important;
            border-bottom-color: #f0a500 !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            background-color: #0d140d !important;
            border-right: 1px solid #1e3a1e !important;
            min-width: 240px !important;
        }
        [data-testid="stSidebar"] * { color: #a8b8a0 !important; }
        [data-testid="stSidebar"] h3 { color: #f0a500 !important; font-size: 1rem !important; }

        /* ── Section headers ── */
        .section-header {
            font-size: 0.78rem;
            font-weight: 600;
            color: #4a8e4a;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
            padding-bottom: 6px;
            border-bottom: 1px solid #1a2e1a;
        }

        /* ── Stage cards ── */
        .stage-card {
            background: #0f1a0f;
            border: 1px solid #1a2e1a;
            border-radius: 8px;
            padding: 14px 16px;
            margin-bottom: 10px;
            font-size: 0.78rem;
            min-height: 110px;
        }
        .stage-card.active-constraint {
            border: 2px solid #f0a500;
            box-shadow: 0 0 18px 3px rgba(240,165,0,0.35);
            background: #1a1400;
        }
        .stage-name {
            font-weight: 700;
            font-size: 0.92rem;
            color: #c8d8c0;
            margin-bottom: 4px;
        }
        .stage-card.active-constraint .stage-name {
            color: #f0a500;
        }
        .stage-desc {
            color: #4a6e4a;
            font-size: 0.72rem;
            margin-top: 4px;
            line-height: 1.45;
        }
        .company-pill {
            display: inline-block;
            background: #1a2e1a;
            color: #90c890;
            font-size: 0.68rem;
            padding: 3px 8px;
            border-radius: 4px;
            margin: 4px 3px 0 0;
            border: 1px solid #2a4e2a;
            font-weight: 600;
        }
        .active-constraint .company-pill {
            background: #2a1a00;
            color: #f0a500;
            border-color: #5a3a00;
        }

        /* ── Quick-set buttons ── */
        [data-testid="stButton"] button {
            font-family: 'IBM Plex Mono', monospace !important;
            border-radius: 6px !important;
            transition: all 0.15s ease !important;
        }
        [data-testid="stButton"] button[kind="secondary"] {
            background-color: #0f1a0f !important;
            border: 1px solid #2a5e2a !important;
            color: #90c890 !important;
        }
        [data-testid="stButton"] button[kind="secondary"]:hover {
            background-color: #1a2e1a !important;
            border-color: #4a8e4a !important;
        }
        [data-testid="stButton"] button[kind="primary"] {
            background-color: #2a1a00 !important;
            border: 2px solid #f0a500 !important;
            color: #f0a500 !important;
            box-shadow: 0 0 10px rgba(240,165,0,0.4) !important;
        }

        /* ── Flow arrows ── */
        .flow-arrow {
            text-align: center;
            color: #2a5e2a;
            font-size: 1.1rem;
            padding: 2px 0;
        }
        .flow-arrow.active-arrow {
            color: #f0a500;
            animation: pulse 1.5s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        /* ── Footer ── */
        .footer {
            text-align: center;
            font-size: 0.65rem;
            color: #2a4e2a;
            padding: 1.5rem 0 0.5rem;
            border-top: 1px solid #1a2e1a;
            margin-top: 2rem;
        }

        /* ── Plotly override for dark bg ── */
        .js-plotly-plot .plotly .main-svg {
            background: transparent !important;
        }

        /* ── Info / warning boxes ── */
        [data-testid="stAlert"] {
            background: #0f1a0f !important;
            border-color: #2a4e2a !important;
            color: #7a9e7a !important;
        }

        /* ── Selectbox / radio ── */
        [data-testid="stSelectbox"] > div,
        [data-testid="stRadio"] label {
            color: #a8b8a0 !important;
        }

        /* ── Responsive stat grid (portfolio summary) ── */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin-bottom: 16px;
        }

        /* ── Stage breakdown cards (cycle viz) ── */
        /* col_count=4 in Python; CSS overrides to 2 on mobile */

        /* ── Horizontal flow scroll wrapper ── */
        .flow-scroll-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        /* ══════════════════════════════════════════════════════
           MOBILE  (<768px)
           Streamlit shows its native hamburger menu for the
           sidebar — we do not hide it ourselves so the toggle
           keeps working.
        ══════════════════════════════════════════════════════ */
        @media screen and (max-width: 768px) {

            /* — Font size reductions — */
            .header-title  { font-size: 1.1rem  !important; }
            .header-thesis { font-size: 0.62rem !important; }
            .stage-card    { font-size: 0.7rem  !important; min-height: 80px !important; }
            .stage-name    { font-size: 0.78rem !important; }
            .company-pill  { font-size: 0.58rem !important; padding: 2px 5px !important; }
            .footer        { font-size: 0.58rem !important; }

            /* — Stack most column blocks — */
            [data-testid="stHorizontalBlock"] {
                flex-wrap: wrap !important;
            }
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {
                flex: 1 1 100% !important;
                min-width: 100% !important;
                width: 100% !important;
            }

            /* — Stat grid: 2 columns on mobile — */
            .stat-grid { grid-template-columns: repeat(2, 1fr) !important; }

            /* — Horizontal flow: allow horizontal scroll — */
            .flow-scroll-container {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
            .flow-scroll-container [data-testid="stPlotlyChart"] .js-plotly-plot {
                min-width: 700px;
            }
        }

        /* ══════════════════════════════════════════════════════
           TABLET  (480px – 767px): 2-column for wider grids
        ══════════════════════════════════════════════════════ */
        @media screen and (min-width: 480px) and (max-width: 767px) {
            [data-testid="stHorizontalBlock"] > [data-testid="column"] {
                flex: 1 1 48% !important;
                min-width: 48% !important;
            }
            .stat-grid { grid-template-columns: repeat(2, 1fr) !important; }
        }

        /* ══════════════════════════════════════════════════════
           SMALL MOBILE  (<480px): true single column
        ══════════════════════════════════════════════════════ */
        @media screen and (max-width: 479px) {
            .stat-grid { grid-template-columns: 1fr !important; }
        }
        </style>
        <!-- Google Font -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

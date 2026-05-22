"""
utils/theme.py
Injects the institutional terminal theme CSS into the Streamlit app.
Design reference: PetroAI Terminal — Inter Tight + JetBrains Mono, dark slate palette.
"""

import streamlit as st

_STAGE_CSS = [
    ("energy",      "#e76f1c", "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&q=80"),
    ("power",       "#f4d220", "https://images.unsplash.com/photo-1548337138-e87d889cc369?w=800&q=80"),
    ("grid",        "#22d3ee", "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=800&q=80"),
    ("compute",     "#3b82f6", "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80"),
    ("transfer",    "#4ade80", "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80"),
    ("ai",          "#a855f7", "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&q=80"),
    ("defense",     "#ef4444", "https://images.unsplash.com/photo-1521694468822-1e20e3f1b68e?w=800&q=80"),
    ("sovereignty", "#f59e0b", "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=80"),
]


def _stage_image_css() -> str:
    rules = []
    for key, color, url in _STAGE_CSS:
        rules.append(
            f".si-{key} {{"
            f"background:linear-gradient(rgba(7,9,13,0.78),rgba(7,9,13,0.78)),url('{url}') center/cover no-repeat;"
            f"border-color:{color}40;}}"
            f".si-{key}:hover {{"
            f"background:linear-gradient(rgba(7,9,13,0.52),rgba(7,9,13,0.52)),url('{url}') center/cover no-repeat;"
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
        @import url('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* ── Design tokens ── */
        :root {{
            --bg:       #07090d;
            --panel:    #0d1117;
            --panel-2:  #11161f;
            --panel-3:  #161c27;
            --line:     #1c2330;
            --line-2:   #262e3d;
            --text:     #e6e9ef;
            --text-2:   #9aa3b2;
            --text-3:   #5b6473;
            --text-4:   #3d4453;
            --pos:      #34d399;
            --neg:      #f87171;
            --energy:      #e76f1c;
            --power:       #f4d220;
            --grid:        #22d3ee;
            --compute:     #3b82f6;
            --transfer:    #4ade80;
            --ai:          #a855f7;
            --defense:     #ef4444;
            --sovereignty: #f59e0b;
            --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
            --sans: 'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        /* ── Base ── */
        * {{ box-sizing: border-box; }}
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: var(--bg) !important;
            color: var(--text) !important;
            font-family: var(--sans) !important;
            font-size: 13px !important;
            -webkit-font-smoothing: antialiased;
            letter-spacing: -0.005em;
        }}

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {{
            background-color: var(--panel) !important;
            border-right: 1px solid var(--line) !important;
        }}
        [data-testid="stSidebar"] * {{
            color: var(--text-2) !important;
            font-size: 11px !important;
            font-family: var(--mono) !important;
        }}
        [data-testid="stSidebar"] h3 {{
            color: var(--energy) !important;
            font-size: 10px !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
        }}

        /* ── Terminal topbar ── */
        .topbar {{
            display: grid;
            grid-template-columns: auto 1fr auto;
            align-items: center;
            gap: 0;
            padding: 0 0 0 0;
            height: 52px;
            border-bottom: 1px solid var(--line);
            margin-bottom: 0;
        }}
        .brand {{
            display: flex; align-items: center; gap: 10px;
            padding: 0 16px 0 0;
            height: 100%;
            border-right: 1px solid var(--line);
        }}
        .brand-mark {{
            width: 28px; height: 28px;
            border-radius: 6px;
            background: linear-gradient(135deg, var(--energy), var(--ai));
            position: relative;
            flex-shrink: 0;
            box-shadow: 0 0 0 1px rgba(255,255,255,0.06), 0 6px 18px rgba(231,111,28,0.18);
        }}
        .brand-mark::after {{
            content: "";
            position: absolute; inset: 6px;
            border-radius: 3px;
            background: var(--panel);
        }}
        .brand-mark::before {{
            content: "";
            position: absolute; inset: 10px;
            border-radius: 50%;
            background: conic-gradient(var(--energy), var(--power), var(--grid), var(--compute), var(--transfer), var(--ai), var(--defense), var(--sovereignty), var(--energy));
        }}
        .brand-name {{
            font-family: var(--sans);
            font-weight: 600;
            font-size: 14px;
            letter-spacing: -0.02em;
            color: var(--text);
            white-space: nowrap;
        }}
        .brand-sub {{
            font-family: var(--mono);
            font-size: 10px;
            color: var(--text-3);
            letter-spacing: 0.12em;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .vdiv {{
            width: 1px; height: 28px;
            background: var(--line);
            flex-shrink: 0;
        }}
        .status-pill {{
            display: inline-flex; align-items: center; gap: 6px;
            font-family: var(--mono);
            font-size: 10px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-2);
            padding: 4px 8px;
            border-radius: 3px;
            background: rgba(52,211,153,0.06);
            border: 1px solid rgba(52,211,153,0.15);
            flex-shrink: 0;
            white-space: nowrap;
        }}
        .status-dot {{
            width: 6px; height: 6px;
            border-radius: 50%;
            background: var(--pos);
            box-shadow: 0 0 8px var(--pos);
            animation: sdpulse 2s ease-in-out infinite;
            flex-shrink: 0;
        }}
        @keyframes sdpulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} }}

        /* ── Ticker tape ── */
        .ticker {{
            overflow: hidden;
            position: relative;
            height: 100%;
            display: flex;
            align-items: center;
            padding: 0 16px;
        }}
        .ticker::before, .ticker::after {{
            content: ""; position: absolute; top: 0; bottom: 0;
            width: 40px; pointer-events: none; z-index: 2;
        }}
        .ticker::before {{ left: 0; background: linear-gradient(to right, var(--bg), transparent); }}
        .ticker::after  {{ right: 0; background: linear-gradient(to left, var(--bg), transparent); }}
        .ticker-track {{
            display: flex; gap: 28px; white-space: nowrap;
            animation: tickertape 90s linear infinite;
        }}
        @keyframes tickertape {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-50%); }} }}
        .ticker-item {{
            display: inline-flex; align-items: center; gap: 8px;
            font-family: var(--mono); font-size: 11px;
        }}
        .ticker-item .sym {{ color: var(--text); font-weight: 500; }}
        .ticker-item .px  {{ color: var(--text-2); }}
        .ticker-item .up   {{ color: var(--pos); }}
        .ticker-item .dn   {{ color: var(--neg); }}

        /* ── User cluster ── */
        .user-cluster {{
            display: flex; align-items: center; gap: 10px;
            padding: 0 0 0 16px;
            height: 100%;
            border-left: 1px solid var(--line);
        }}
        .utc-clock {{
            font-family: var(--mono);
            font-size: 11px;
            color: var(--text-2);
            padding: 4px 8px;
            border: 1px solid var(--line);
            border-radius: 3px;
            white-space: nowrap;
        }}
        .nav-meta {{
            display: flex; gap: 12px; align-items: center;
            font-family: var(--mono); font-size: 10px;
            color: var(--text-3); letter-spacing: 0.08em; text-transform: uppercase;
        }}
        .nav-meta .sep {{ width: 1px; height: 12px; background: var(--line); }}
        .nav-meta .nv  {{ color: var(--text); }}
        .nav-meta .np  {{ color: var(--pos); }}

        /* ── Streamlit tabs override ── */
        [data-testid="stTabs"] > div:first-child {{
            background: var(--panel) !important;
            border-bottom: 1px solid var(--line) !important;
            padding: 0 !important;
            gap: 0 !important;
        }}
        [data-testid="stTabs"] button {{
            color: var(--text-3) !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            font-family: var(--sans) !important;
            letter-spacing: -0.01em !important;
            padding: 0 16px !important;
            height: 44px !important;
            border-radius: 0 !important;
            border-bottom: 2px solid transparent !important;
            margin-bottom: -1px !important;
            transition: color 120ms ease !important;
        }}
        [data-testid="stTabs"] button:hover {{
            color: var(--text-2) !important;
            background: transparent !important;
        }}
        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--text) !important;
            border-bottom-color: var(--energy) !important;
            background: transparent !important;
        }}
        [data-testid="stTabs"] button p {{
            font-size: 12px !important;
            font-weight: 500 !important;
        }}

        /* ── Panel primitives ── */
        .panel {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            overflow: hidden;
        }}
        .panel-head {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 10px 14px;
            border-bottom: 1px solid var(--line);
        }}
        .panel-title {{
            font-size: 10px;
            font-family: var(--mono);
            letter-spacing: 0.14em;
            text-transform: uppercase;
            color: var(--text-2);
        }}
        .panel-actions {{
            display: flex; align-items: center; gap: 6px;
            font-family: var(--mono); font-size: 10px; color: var(--text-3);
        }}
        .panel-body {{ padding: 14px; }}
        .chip {{
            font-family: var(--mono); font-size: 10px;
            letter-spacing: 0.08em; text-transform: uppercase;
            color: var(--text-3); padding: 2px 6px;
            border: 1px solid var(--line); border-radius: 2px;
        }}
        .chip.live {{
            color: var(--pos);
            border-color: rgba(52,211,153,0.25);
            background: rgba(52,211,153,0.05);
        }}

        /* ── Index strip ── */
        .index-strip {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 1px;
            background: var(--line);
            border: 1px solid var(--line);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        .idx {{
            background: var(--panel);
            padding: 12px 14px;
        }}
        .idx .nm {{
            font-family: var(--mono); font-size: 10px;
            letter-spacing: 0.14em; text-transform: uppercase;
            color: var(--text-3);
        }}
        .idx .px {{
            font-family: var(--mono); font-size: 18px;
            margin-top: 4px; letter-spacing: -0.01em;
            color: var(--text);
        }}
        .idx .ch {{
            font-family: var(--mono); font-size: 11px;
            margin-top: 2px; display: flex; gap: 8px;
        }}
        .idx .sparkbox {{ height: 24px; margin-top: 6px; }}

        /* ── Heatmap ── */
        .heatmap {{
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: 2px;
            padding: 12px;
        }}
        .heat-cell {{
            aspect-ratio: 1.6 / 1;
            padding: 7px;
            position: relative;
            font-family: var(--mono);
            border-radius: 2px;
            overflow: hidden;
        }}
        .heat-cell .t {{ font-size: 11px; font-weight: 600; color: var(--text); }}
        .heat-cell .c {{
            font-size: 10px; color: rgba(255,255,255,0.7);
            position: absolute; bottom: 7px; left: 7px;
        }}

        /* ── Flow visualization ── */
        .flow-vis {{ padding: 12px 14px; }}
        .flow-row {{
            display: grid;
            grid-template-columns: 80px 1fr 48px;
            align-items: center;
            gap: 10px;
            padding: 5px 0;
        }}
        .flow-row .lab {{
            font-family: var(--mono); font-size: 10px;
            color: var(--text-3); letter-spacing: 0.1em; text-transform: uppercase;
        }}
        .flow-row .bar-track {{
            height: 6px; background: var(--panel-3);
            border-radius: 2px; overflow: hidden;
        }}
        .flow-row .bar {{ height: 100%; border-radius: 2px; }}
        .flow-row .num {{
            font-family: var(--mono); font-size: 11px;
            text-align: right; color: var(--text-2);
        }}

        /* ── Movers ── */
        .mover-row {{
            display: grid;
            grid-template-columns: auto 1fr auto auto;
            gap: 10px; align-items: center;
            padding: 9px 14px;
            border-bottom: 1px solid var(--line);
        }}
        .mover-row:last-child {{ border-bottom: none; }}
        .mover-bar {{ width: 3px; height: 22px; border-radius: 2px; flex-shrink: 0; }}
        .mover-sym {{ font-family: var(--mono); font-size: 12px; font-weight: 600; color: var(--text); }}
        .mover-nm  {{ font-size: 11px; color: var(--text-3); margin-top: 1px; }}
        .mover-px  {{ font-family: var(--mono); font-size: 12px; color: var(--text-2); }}
        .mover-ch  {{ font-family: var(--mono); font-size: 12px; text-align: right; min-width: 60px; }}

        /* ── Signals ── */
        .signal-row {{
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px; align-items: center;
            padding: 9px 14px;
            border-bottom: 1px solid var(--line);
        }}
        .signal-row:last-child {{ border-bottom: none; }}
        .signal-lhs {{ display: flex; align-items: center; gap: 10px; }}
        .signal-dot {{
            width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
        }}
        .signal-lbl {{ font-size: 12px; color: var(--text); }}
        .signal-sub {{
            display: block; color: var(--text-3); font-size: 10px;
            margin-top: 1px; font-family: var(--mono); letter-spacing: 0.05em;
        }}
        .signal-val {{ font-family: var(--mono); font-size: 12px; color: var(--text-2); }}

        /* ── Newsflow ── */
        .news-row {{
            padding: 9px 14px;
            border-bottom: 1px solid var(--line);
            display: grid;
            grid-template-columns: 44px 1fr;
            gap: 10px;
        }}
        .news-row:last-child {{ border-bottom: none; }}
        .news-time {{ font-family: var(--mono); font-size: 10px; color: var(--text-3); padding-top: 2px; }}
        .news-src {{
            font-family: var(--mono); font-size: 9px;
            letter-spacing: 0.14em; text-transform: uppercase;
        }}
        .news-hl {{ font-size: 12px; color: var(--text); margin-top: 3px; line-height: 1.35; }}

        /* ── Stage ranking rows ── */
        .rank-row {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 9px 14px;
            border-bottom: 1px solid var(--line);
        }}
        .rank-row:last-child {{ border-bottom: none; }}
        .rank-lhs {{ display: flex; align-items: center; gap: 8px; }}
        .rank-num {{ font-family: var(--mono); font-size: 9px; color: var(--text-3); }}
        .rank-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
        .rank-name {{ font-size: 12px; font-weight: 500; }}
        .rank-val {{ font-family: var(--mono); font-size: 13px; font-weight: 700; }}

        /* ── Thesis alignment card ── */
        .alignment-card {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 14px 18px;
        }}

        /* ── KPI row ── */
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 12px;
        }}
        .kpi {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 14px 16px;
            position: relative; overflow: hidden;
        }}
        .kpi .k {{
            font-family: var(--mono); font-size: 10px;
            letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-3);
        }}
        .kpi .v {{ font-family: var(--mono); font-size: 24px; margin-top: 6px; letter-spacing: -0.015em; color: var(--text); }}
        .kpi .sub {{ font-family: var(--mono); font-size: 11px; margin-top: 2px; color: var(--text-2); }}

        /* ── Stat grid (portfolio summary) ── */
        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 16px;
        }}

        /* ── Legacy stage cards (cycle tab) ── */
        .stage-card {{
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 14px;
            margin-bottom: 8px;
            transition: all 0.12s ease;
        }}
        .stage-card:hover {{ background: var(--panel-2); }}
        .stage-card.active-constraint {{
            border-color: var(--energy);
            background: rgba(231,111,28,0.04);
        }}
        .stage-name {{ font-weight: 600; font-size: 13px; color: var(--text); font-family: var(--sans); }}
        .stage-card.active-constraint .stage-name {{ color: var(--energy); }}
        .stage-desc {{
            color: var(--text-3); font-size: 11px;
            margin-top: 4px; line-height: 1.5;
            font-family: var(--mono);
        }}
        .company-pill {{
            display: inline-block;
            background: var(--panel-2);
            color: var(--text-2);
            font-size: 11px;
            padding: 2px 6px;
            border-radius: 2px;
            margin: 3px 2px 0 0;
            border: 1px solid var(--line-2);
            font-weight: 600;
            font-family: var(--mono);
        }}
        .active-constraint .company-pill {{
            background: rgba(231,111,28,0.1);
            border-color: rgba(231,111,28,0.3);
            color: var(--text);
        }}

        /* ── Stage image cards ── */
        .stage-img-card {{
            border-radius: 4px;
            padding: 14px;
            margin-bottom: 8px;
            min-height: 140px;
            position: relative;
            overflow: hidden;
            border: 1px solid var(--line);
            transition: all 0.12s ease;
            cursor: default;
        }}
        .stage-img-card:hover {{ transform: translateY(-1px); }}
        {stage_img_css}

        /* ── Section header ── */
        .section-header {{
            font-size: 10px;
            font-weight: 400;
            color: var(--text-2);
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--line);
            font-family: var(--mono);
        }}

        /* ── Header block ── */
        .header-block {{ padding: 4px 0 6px; }}
        .header-title {{
            font-size: 16px; font-weight: 700;
            color: var(--energy);
            letter-spacing: -0.01em;
            font-family: var(--sans);
        }}
        .header-thesis {{
            font-size: 11px; line-height: 1.6;
            color: var(--text-3);
            font-family: var(--mono);
            margin-top: 4px;
        }}
        .header-meta {{ text-align: right; padding-top: 4px; }}
        .handle-link {{
            color: var(--energy) !important;
            font-weight: 600; text-decoration: none;
            font-size: 12px; font-family: var(--mono);
        }}
        .last-updated {{ font-size: 10px; color: var(--text-3); margin-top: 4px; font-family: var(--mono); }}
        .test-badge {{
            display: inline-block;
            background: rgba(239,68,68,0.12); color: var(--neg);
            font-size: 9px; font-weight: 600;
            padding: 2px 8px; border-radius: 2px;
            border: 1px solid var(--neg); margin-top: 4px;
            letter-spacing: 0.1em; font-family: var(--mono);
        }}
        .header-divider {{ border: none; border-top: 1px solid var(--line); margin: 6px 0 10px; }}

        /* ── Footer bar ── */
        .footer-bar {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 8px 0;
            border-top: 1px solid var(--line);
            font-family: var(--mono); font-size: 10px;
            color: var(--text-3); letter-spacing: 0.08em;
            text-transform: uppercase; margin-top: 24px;
        }}
        .footer-bar .grp {{ display: flex; gap: 16px; align-items: center; }}
        .footer-dot {{
            width: 6px; height: 6px; border-radius: 50%;
            background: var(--pos); box-shadow: 0 0 6px var(--pos);
            display: inline-block; margin-right: 6px;
            animation: sdpulse 2s ease-in-out infinite;
        }}
        .footer {{ display: none; }}

        /* ── Flow arrows (cycle viz) ── */
        .flow-arrow {{ text-align:center; color:var(--line-2); font-size:1rem; padding:2px 0; }}
        .flow-arrow.active-arrow {{ color:var(--energy); animation:sdpulse 1.5s ease-in-out infinite; }}

        /* ── Plotly transparent bg ── */
        .js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}

        /* ── Streamlit widget overrides ── */
        [data-testid="stAlert"] {{
            background: var(--panel) !important;
            border-color: var(--line) !important;
            color: var(--text-2) !important;
            font-size: 12px !important;
            font-family: var(--mono) !important;
        }}
        [data-testid="stSelectbox"] > div,
        [data-testid="stRadio"] label {{
            color: var(--text-2) !important;
            font-size: 12px !important;
            font-family: var(--mono) !important;
        }}
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-size: 12px;
            color: var(--text-2);
            font-family: var(--sans);
        }}
        [data-testid="stButton"] button {{
            font-family: var(--mono) !important;
            border-radius: 2px !important;
            font-size: 11px !important;
        }}
        [data-testid="stButton"] button[kind="secondary"] {{
            background-color: var(--panel) !important;
            border: 1px solid var(--line-2) !important;
            color: var(--text-2) !important;
        }}
        [data-testid="stButton"] button[kind="primary"] {{
            background-color: rgba(231,111,28,0.08) !important;
            border: 1px solid var(--energy) !important;
            color: var(--energy) !important;
        }}

        /* ── Mobile ── */
        @media screen and (max-width: 768px) {{
            .topbar {{ grid-template-columns: 1fr auto; }}
            .ticker {{ display: none; }}
            .index-strip {{ grid-template-columns: repeat(3, 1fr) !important; }}
            .heatmap {{ grid-template-columns: repeat(4, 1fr) !important; }}
            .kpi-row {{ grid-template-columns: repeat(2, 1fr) !important; }}
            .stat-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
        }}
        @media screen and (max-width: 479px) {{
            .stat-grid {{ grid-template-columns: 1fr !important; }}
            .kpi-row {{ grid-template-columns: 1fr !important; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

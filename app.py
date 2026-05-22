"""
PetroAI Capital Cycle Dashboard
================================
Institutional terminal layout — Inter Tight + JetBrains Mono dark slate theme.
"""

import streamlit as st
from datetime import datetime, timezone

from utils.state import init_session_state
from utils.theme import inject_css
from tabs.cycle_viz import render_cycle_viz
from tabs.portfolio import render_portfolio
from tabs.constraints import render_constraints
from tabs.deep_dive import render_deep_dive
from tabs.market_overview import render_market_overview

# ─── TEST MODE ────────────────────────────────────────────────────────────────
TEST_MODE = False
# ──────────────────────────────────────────────────────────────────────────────

# Static ticker tape items (symbol, price, direction, pct)
_TICKER_ITEMS = [
    ("PETROAI", "4827.42", "up",   "+1.31%"),
    ("NVDA",    "1284.30", "up",   "+4.21%"),
    ("XOM",     "118.42",  "up",   "+1.82%"),
    ("VST",     "167.21",  "up",   "+3.10%"),
    ("CCJ",     "58.93",   "up",   "+2.41%"),
    ("MSFT",    "478.20",  "up",   "+1.12%"),
    ("PLTR",    "142.80",  "up",   "+3.41%"),
    ("MP",      "28.40",   "up",   "+6.21%"),
    ("LMT",     "612.40",  "up",   "+0.81%"),
    ("CEG",     "281.50",  "up",   "+1.62%"),
    ("GEV",     "392.18",  "up",   "+2.91%"),
    ("ANET",    "412.80",  "up",   "+1.42%"),
    ("KTOS",    "38.20",   "up",   "+4.21%"),
    ("WTI",     "78.42",   "up",   "+2.40%"),
    ("URA",     "38.92",   "dn",   "-1.07%"),
    ("DXY",     "104.28",  "dn",   "-0.17%"),
    ("OKLO",    "42.18",   "up",   "+5.30%"),
    ("CRWV",    "78.40",   "up",   "+5.81%"),
    ("ETN",     "348.92",  "up",   "+1.20%"),
    ("MU",      "118.50",  "up",   "+2.80%"),
]

st.set_page_config(
    page_title="PetroAI Capital Cycle",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session_state()

# ─── DYNAMIC STAGE BACKGROUND ─────────────────────────────────────────────────
_stage_bg = {
    "⚡ Energy":      "#0d0a07",
    "🔋 Power":       "#0d0d04",
    "🔌 Grid":        "#04100d",
    "💻 Compute":     "#050a12",
    "🔁 Transfer":    "#050d08",
    "🤖 AI":          "#09050d",
    "🛡️ Defense":     "#0d0505",
    "🌐 Sovereignty": "#0d0b04",
}
_current_bg = _stage_bg.get(st.session_state.current_stage, "#07090d")
st.markdown(f"""
<style>
.stApp {{
    background-color: {_current_bg} !important;
    transition: background-color 0.5s ease;
}}
[data-testid="stAppViewContainer"] {{
    background-color: {_current_bg} !important;
}}
[data-testid="stHeader"] {{
    background-color: {_current_bg} !important;
}}
.ticker::before {{ background: linear-gradient(to right, {_current_bg}, transparent) !important; }}
.ticker::after  {{ background: linear-gradient(to left,  {_current_bg}, transparent) !important; }}
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────────────────────

# ─── TERMINAL TOPBAR ──────────────────────────────────────────────────────────
_utc_now = datetime.now(timezone.utc).strftime("%H:%M:%S")

_ticker_html = " ".join(
    f'<span class="ticker-item">'
    f'<span class="sym">{sym}</span>'
    f'<span class="px">{px}</span>'
    f'<span class="{d}">{pct}</span>'
    f'</span>'
    for sym, px, d, pct in _TICKER_ITEMS
)

st.markdown(f"""
<div class="topbar">
    <div class="brand">
        <div class="brand-mark"></div>
        <div>
            <div class="brand-name">PetroAI <span style="color:var(--text-3);font-weight:400">// Capital Cycle</span></div>
            <div class="brand-sub">Institutional · v4.2.1 · Energy → Sovereignty</div>
        </div>
        <div class="vdiv"></div>
        <span class="status-pill"><span class="status-dot"></span>Markets Open</span>
    </div>
    <div class="ticker">
        <div class="ticker-track">
            {_ticker_html}{_ticker_html}
        </div>
    </div>
    <div class="user-cluster">
        <span class="utc-clock">{_utc_now} UTC</span>
        <div class="nav-meta">
            <span>NAV <span class="nv">$2.284B</span></span>
            <span class="sep"></span>
            <span>Δ Today <span class="np">+1.31%</span></span>
            <span class="sep"></span>
            <span>YTD <span class="np">+18.42%</span></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────────────────────

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Controls")

    st.markdown("**Active Constraint**")
    _stages = [
        "⚡ Energy", "🔋 Power", "🔌 Grid",
        "💻 Compute", "🔁 Transfer", "🤖 AI",
        "🛡️ Defense", "🌐 Sovereignty"
    ]
    _current = st.selectbox(
        "Set current bottleneck",
        _stages,
        index=_stages.index(st.session_state.current_stage),
        key="stage_selector",
        label_visibility="collapsed",
    )
    if _current != st.session_state.current_stage:
        st.session_state.current_stage = _current

    st.markdown("---")
    st.markdown("**View Mode**")
    st.session_state.viz_mode = st.radio(
        "Cycle diagram style",
        ["Horizontal Flow", "Circular", "Heatmap"],
        index=0,
        key="viz_mode_radio",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Add / remove positions in the Portfolio tab.")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01  Cycle Visualization",
    "02  Portfolio",
    "03  Market Overview",
    "04  Constraints",
    "05  Deep Dive",
])

with tab1:
    render_cycle_viz(TEST_MODE)

with tab2:
    render_portfolio(TEST_MODE)

with tab3:
    render_market_overview(TEST_MODE)

with tab4:
    render_constraints(TEST_MODE)

with tab5:
    render_deep_dive(TEST_MODE)

# ─── FOOTER BAR ───────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer-bar'>"
    "<div class='grp'>"
    "<span><span class='footer-dot'></span>Stream · NYSE/NASDAQ · IEX</span>"
    "<span>Latency 42ms</span>"
    "<span>Quote feed · L2</span>"
    "</div>"
    "<div class='grp'>"
    "<span>Engine v4.2.1</span>"
    "<span>© PetroAI Research · @mikalche thesis · Not financial advice</span>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

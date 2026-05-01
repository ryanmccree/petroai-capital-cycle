"""
PetroAI Capital Cycle Dashboard
================================
Step 1: Core layout, session state, and Cycle Visualization tab.
"""

import streamlit as st
from utils.state import init_session_state
from utils.theme import inject_css
from tabs.cycle_viz import render_cycle_viz
from tabs.portfolio import render_portfolio
from tabs.constraints import render_constraints
from tabs.deep_dive import render_deep_dive
from tabs.market_overview import render_market_overview

# ─── TEST MODE ────────────────────────────────────────────────────────────────
# Set True to bypass yfinance entirely and use hardcoded dummy data.
TEST_MODE = True
# ──────────────────────────────────────────────────────────────────────────────

THESIS_SUMMARY = (
    "PetroAI Capital Cycle — Where energy, compute & capital converge. "
    "It is a flywheel: Solve one constraint → expose the next → capital rotates. "
    "The system moves through these interconnected stages: "
    "Energy → Power → Grid → Compute → Transfer → AI → Defense → Sovereignty. "
    "Companies are not separate plays — they are layers in one integrated stack. "
    "The market constantly shifts capital to the current bottleneck forcing trillions in capex."
)

st.set_page_config(
    page_title="PetroAI Capital Cycle",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session_state()

# ─── HEADER ───────────────────────────────────────────────────────────────────
from datetime import datetime

col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown(
        f"""
        <div class="header-block">
            <div class="header-title">⚡ PetroAI Capital Cycle</div>
            <div class="header-thesis">{THESIS_SUMMARY}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_meta:
    st.markdown(
        f"""
        <div class="header-meta">
            <a href="https://twitter.com/mikalche" target="_blank" class="handle-link">@mikalche</a>
            <div class="last-updated">Updated {datetime.now().strftime('%b %d, %Y %H:%M')}</div>
            {"<div class='test-badge'>TEST MODE</div>" if TEST_MODE else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<hr class='header-divider'>", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Dashboard Controls")

    st.markdown("**Active Constraint Stage**")
    stages = [
        "⚡ Energy", "🔋 Power", "🔌 Grid",
        "💻 Compute", "🔁 Transfer", "🤖 AI",
        "🛡️ Defense", "🌐 Sovereignty"
    ]
    current = st.selectbox(
        "Set current bottleneck",
        stages,
        index=stages.index(st.session_state.current_stage),
        key="stage_selector",
    )
    if current != st.session_state.current_stage:
        st.session_state.current_stage = current

    st.markdown("---")
    st.markdown("**View Mode**")
    st.session_state.viz_mode = st.radio(
        "Cycle diagram style",
        ["Horizontal Flow", "Circular", "Heatmap"],
        index=0,
        key="viz_mode_radio",
    )

    st.markdown("---")
    st.caption("Use the Portfolio tab to add or remove positions.")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔄 Cycle Visualization",
    "📊 Portfolio",
    "🎯 Constraints",
    "🔍 Deep Dive",
    "📈 Market Overview",
])

with tab1:
    render_cycle_viz(TEST_MODE)

with tab2:
    render_portfolio(TEST_MODE)

with tab3:
    render_constraints(TEST_MODE)

with tab4:
    render_deep_dive(TEST_MODE)

with tab5:
    render_market_overview(TEST_MODE)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='footer'>Built by R.McCree to monitor @mikalche's PetroAI Capital Cycle Thesis • Not financial advice</div>",
    unsafe_allow_html=True,
)

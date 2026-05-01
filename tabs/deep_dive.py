"""
tabs/deep_dive.py
──────────────────
Tab 4: Company Deep Dive
- Select any company from the portfolio
- 30-day price chart with volume
- Key metrics: price, changes, market cap
- Stage context and thesis note
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

from utils.state import STAGES, STAGE_DESCRIPTIONS
from utils.data import get_quote, get_sparkline, DUMMY_QUOTES


# ── Chart builder ──────────────────────────────────────────────────────────────

def _price_chart(ticker: str, series, test_mode: bool) -> go.Figure:
    prices = series.tolist()
    n = len(prices)
    xs = list(range(n))

    color_line = "#4ade80" if prices[-1] >= prices[0] else "#f87171"
    fill_color = "rgba(122,184,122,0.08)" if prices[-1] >= prices[0] else "rgba(200,64,64,0.08)"

    # Fake volume for test mode
    rng = np.random.default_rng(seed=abs(hash(ticker)) % (2**31))
    volumes = (rng.integers(500_000, 5_000_000, n)).tolist()

    fig = go.Figure()

    # Volume bars (secondary y)
    fig.add_trace(go.Bar(
        x=xs,
        y=volumes,
        marker_color="#1a2e1a",
        opacity=0.5,
        name="Volume",
        yaxis="y2",
        hovertemplate="%{y:,.0f}<extra>Volume</extra>",
    ))

    # Price area
    fig.add_trace(go.Scatter(
        x=xs,
        y=prices,
        mode="lines",
        line=dict(color=color_line, width=2),
        fill="tozeroy",
        fillcolor=fill_color,
        name="Price",
        hovertemplate="$%{y:.2f}<extra>Price</extra>",
    ))

    # Entry / exit reference (start price)
    fig.add_hline(
        y=prices[0],
        line_dash="dot",
        line_color="#2a5e2a",
        line_width=1,
    )

    fig.update_layout(
        paper_bgcolor="#0a0e0a",
        plot_bgcolor="#0a0e0a",
        margin=dict(l=10, r=10, t=30, b=10),
        height=280,
        xaxis=dict(
            tickfont=dict(size=8, color="#2a5e2a", family="IBM Plex Mono"),
            gridcolor="#0f1a0f",
            showticklabels=False,
        ),
        yaxis=dict(
            tickfont=dict(size=9, color="#4a6e4a", family="IBM Plex Mono"),
            gridcolor="#0f1a0f",
            tickprefix="$",
        ),
        yaxis2=dict(
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(size=7, color="#1a3e1a", family="IBM Plex Mono"),
        ),
        title=dict(
            text=f"{ticker} — 30-Day Price" + (" (TEST DATA)" if test_mode else ""),
            font=dict(size=10, color="#4a8e4a", family="IBM Plex Mono"),
            x=0.01,
        ),
        showlegend=False,
        hovermode="x unified",
    )
    return fig


# ── Main render ────────────────────────────────────────────────────────────────

def render_deep_dive(test_mode: bool):
    companies = st.session_state.companies

    if not companies:
        st.warning("No companies in the portfolio yet. Add some in the Portfolio tab.")
        return

    st.markdown(
        "<div style='font-size:0.75rem; color:#4a8e4a; margin-bottom:0.75rem;'>"
        "Select a position for a detailed look — price history, key metrics, and cycle context."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Ticker selector ──────────────────────────────────────────────────────
    all_tickers = [c["ticker"] for c in companies]
    sel_col, _, _ = st.columns([2, 2, 2])
    with sel_col:
        selected_ticker = st.selectbox(
            "Select ticker",
            all_tickers,
            key="deep_dive_ticker",
            label_visibility="collapsed",
        )

    co = next((c for c in companies if c["ticker"] == selected_ticker), None)
    if co is None:
        st.error("Company not found.")
        return

    ticker = co["ticker"]
    stage  = co["stage"]
    note   = co.get("note", "")
    active = st.session_state.current_stage
    is_active_stage = (stage == active)

    q     = get_quote(ticker, test_mode)
    spark = get_sparkline(ticker, test_mode, 30)

    price  = q.get("price", 0)
    chg_1d = q.get("chg_1d", 0)
    chg_5d = q.get("chg_5d", 0)
    chg_1m = q.get("chg_1m", 0)
    mcap   = q.get("mcap", "N/A")

    def chg_color(v):
        return "#4ade80" if v > 0 else ("#f87171" if v < 0 else "#6b7280")

    def fmt_chg(v):
        return f"{'+'if v>0 else''}{v:.1f}%"

    # ── Header strip ─────────────────────────────────────────────────────────
    border = "#5a3a00" if is_active_stage else "#1a2e1a"
    bg     = "#1a1400" if is_active_stage else "#0f1a0f"
    st.markdown(
        f"<div style='background:{bg}; border:1px solid {border}; border-radius:8px;"
        f" padding:16px 20px; margin-bottom:16px;'>"
        f"<div style='display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;'>"
        f"<span style='font-size:1.6rem; font-weight:700; color:{'#f0a500' if is_active_stage else '#90c890'};'>{ticker}</span>"
        f"<span style='font-size:0.8rem; color:#7a9e7a;'>{stage}</span>"
        f"{'<span style=\"font-size:0.65rem; background:#3a1a00; color:#f0a500; padding:2px 8px; border-radius:3px; border:1px solid #f0a500; font-weight:700;\">ACTIVE CONSTRAINT STAGE</span>' if is_active_stage else ''}"
        f"</div>"
        f"<div style='font-size:0.75rem; color:#4a6e4a; margin-top:6px; font-style:italic;'>{note}</div>"
        f"<div style='font-size:0.72rem; color:#3a6e3a; margin-top:4px;'>{STAGE_DESCRIPTIONS.get(stage,'')}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Metrics row ──────────────────────────────────────────────────────────
    m1, m2, m3, m4, m5 = st.columns(5)
    metrics = [
        (m1, "Price", f"${price:.2f}", "#c8d8c0"),
        (m2, "1D Change", fmt_chg(chg_1d), chg_color(chg_1d)),
        (m3, "5D Change", fmt_chg(chg_5d), chg_color(chg_5d)),
        (m4, "1M Change", fmt_chg(chg_1m), chg_color(chg_1m)),
        (m5, "Market Cap", mcap, "#7a9e7a"),
    ]
    for col, label, val, color in metrics:
        with col:
            st.markdown(
                f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:6px;"
                f" padding:10px 12px; text-align:center;'>"
                f"<div style='font-size:0.62rem; color:#3a6e3a; text-transform:uppercase;"
                f" letter-spacing:0.08em;'>{label}</div>"
                f"<div style='font-size:1.1rem; font-weight:700; color:{color}; margin-top:4px;'>{val}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Price chart ──────────────────────────────────────────────────────────
    fig = _price_chart(ticker, spark, test_mode)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Stage peers ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
        " text-transform:uppercase; margin-bottom:0.5rem;'>Stage peers</div>",
        unsafe_allow_html=True,
    )

    peers = [c for c in companies if c["stage"] == stage and c["ticker"] != ticker]
    if peers:
        peer_cols = st.columns(min(len(peers), 6))
        for i, peer in enumerate(peers[:6]):
            pq = get_quote(peer["ticker"], test_mode)
            pc = pq.get("chg_1m", 0)
            with peer_cols[i]:
                st.markdown(
                    f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:4px;"
                    f" padding:8px; text-align:center;'>"
                    f"<div style='font-size:0.8rem; font-weight:700; color:#90c890;'>{peer['ticker']}</div>"
                    f"<div style='font-size:0.65rem; color:#4a6e4a;'>{peer.get('note','')}</div>"
                    f"<div style='font-size:0.75rem; color:{'#4ade80' if pc>=0 else '#f87171'}; margin-top:4px;'>"
                    f"{'+'if pc>=0 else''}{pc:.1f}% 1M</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        st.markdown(
            "<span style='font-size:0.72rem; color:#2a5e2a;'>No other positions in this stage.</span>",
            unsafe_allow_html=True,
        )

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem; font-size:0.65rem; color:#3a4e3a;"
            " border:1px solid #1a2e1a; border-radius:4px; padding:6px 10px;'>"
            "🧪 TEST MODE — chart data is synthetically generated from dummy prices."
            "</div>",
            unsafe_allow_html=True,
        )

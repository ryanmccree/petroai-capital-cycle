"""
tabs/portfolio.py
─────────────────
Tab 2: Portfolio Manager
- Company table with price data (TEST_MODE or live)
- Sparkline mini-charts per company
- Add / remove companies from the cycle
"""

import streamlit as st
import plotly.graph_objects as go

from utils.state import STAGES, STAGE_DESCRIPTIONS
from utils.data import get_quote, get_sparkline


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chg_color(val: float) -> str:
    if val > 0:
        return "#4ade80"
    if val < 0:
        return "#f87171"
    return "#6b7280"


def _fmt_chg(val: float) -> str:
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.1f}%"


def _sparkline_fig(series) -> go.Figure:
    color = "#4ade80" if series.iloc[-1] >= series.iloc[0] else "#f87171"
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fill_color = f"rgba({r},{g},{b},0.10)"
    fig = go.Figure(go.Scatter(
        y=series.tolist(),
        mode="lines",
        line=dict(color=color, width=1.5),
        fill="tozeroy",
        fillcolor=fill_color,
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=40,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


# ── Main render ────────────────────────────────────────────────────────────────

def render_portfolio(test_mode: bool):
    active = st.session_state.current_stage

    st.markdown(
        "<div style='font-size:0.75rem; color:#4a8e4a; margin-bottom:0.75rem;'>"
        "Track every position in the capital cycle — price performance, stage allocation, and momentum."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Summary stats ────────────────────────────────────────────────────────
    companies = st.session_state.companies
    total = len(companies)
    stage_counts = {}
    for c in companies:
        stage_counts[c["stage"]] = stage_counts.get(c["stage"], 0) + 1

    top_stage = max(stage_counts, key=stage_counts.get) if stage_counts else "—"

    sm1, sm2, sm3, sm4 = st.columns(4)
    for col, label, val in [
        (sm1, "Total Positions", str(total)),
        (sm2, "Active Stages", str(len(stage_counts))),
        (sm3, "Heaviest Stage", top_stage.split(" ", 1)[-1] if " " in top_stage else top_stage),
        (sm4, "Active Constraint", active.split(" ", 1)[-1] if " " in active else active),
    ]:
        with col:
            st.markdown(
                f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:6px;"
                f" padding:10px 14px; text-align:center;'>"
                f"<div style='font-size:0.65rem; color:#4a6e4a; text-transform:uppercase;"
                f" letter-spacing:0.08em;'>{label}</div>"
                f"<div style='font-size:1.3rem; font-weight:700; color:#f0a500; margin-top:4px;'>{val}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Filter by stage ──────────────────────────────────────────────────────
    filter_options = ["All Stages"] + STAGES
    selected_filter = st.selectbox(
        "Filter by stage",
        filter_options,
        key="portfolio_stage_filter",
        label_visibility="collapsed",
    )

    filtered = companies if selected_filter == "All Stages" else [
        c for c in companies if c["stage"] == selected_filter
    ]

    if not filtered:
        st.warning("No companies in this stage yet.")
        _render_add_form()
        return

    # ── Company rows ─────────────────────────────────────────────────────────
    st.markdown(
        "<div style='display:grid; grid-template-columns: 70px 130px 1fr 80px 80px 80px 80px 80px 60px;"
        " gap:4px; padding:4px 8px; font-size:0.65rem; color:#3a6e3a;"
        " text-transform:uppercase; letter-spacing:0.08em;'>"
        "<div>Ticker</div><div>Stage</div><div>Note</div>"
        "<div style='text-align:right;'>Price</div>"
        "<div style='text-align:right;'>1D</div>"
        "<div style='text-align:right;'>5D</div>"
        "<div style='text-align:right;'>1M</div>"
        "<div style='text-align:right;'>MCap</div>"
        "<div style='text-align:right;'>30D</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    for idx, co in enumerate(filtered):
        ticker = co["ticker"]
        stage  = co["stage"]
        note   = co.get("note", "")
        is_active_stage = (stage == active)

        q = get_quote(ticker, test_mode)
        spark = get_sparkline(ticker, test_mode, 30)

        price  = q.get("price", 0)
        chg_1d = q.get("chg_1d", 0)
        chg_5d = q.get("chg_5d", 0)
        chg_1m = q.get("chg_1m", 0)
        mcap   = q.get("mcap", "N/A")

        border = "#5a3a00" if is_active_stage else "#1a2e1a"
        bg     = "#1a1400" if is_active_stage else "#0f1a0f"

        col_ticker, col_stage, col_note, col_price, col_1d, col_5d, col_1m, col_mcap, col_spark, col_del = st.columns(
            [0.9, 1.6, 2.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.2, 0.5]
        )

        with col_ticker:
            st.markdown(
                f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                f" padding:6px 8px; font-weight:700; font-size:0.82rem;"
                f" color:{'#f0a500' if is_active_stage else '#90c890'};'>{ticker}</div>",
                unsafe_allow_html=True,
            )
        with col_stage:
            st.markdown(
                f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                f" padding:6px 8px; font-size:0.7rem; color:#7a9e7a;'>{stage}</div>",
                unsafe_allow_html=True,
            )
        with col_note:
            st.markdown(
                f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                f" padding:6px 8px; font-size:0.7rem; color:#4a6e4a;'>{note}</div>",
                unsafe_allow_html=True,
            )
        with col_price:
            st.markdown(
                f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                f" padding:6px 8px; font-size:0.82rem; color:#c8d8c0; text-align:right;'>${price:.2f}</div>",
                unsafe_allow_html=True,
            )
        for col_chg, chg in [(col_1d, chg_1d), (col_5d, chg_5d), (col_1m, chg_1m)]:
            with col_chg:
                st.markdown(
                    f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                    f" padding:6px 8px; font-size:0.78rem; color:{_chg_color(chg)}; text-align:right;'>{_fmt_chg(chg)}</div>",
                    unsafe_allow_html=True,
                )
        with col_mcap:
            st.markdown(
                f"<div style='background:{bg}; border:1px solid {border}; border-radius:4px;"
                f" padding:6px 8px; font-size:0.72rem; color:#7a9e7a; text-align:right;'>{mcap}</div>",
                unsafe_allow_html=True,
            )
        with col_spark:
            st.plotly_chart(
                _sparkline_fig(spark),
                use_container_width=True,
                config={"displayModeBar": False},
                key=f"spark_{ticker}_{idx}",
            )
        with col_del:
            if st.button("✕", key=f"del_{ticker}_{idx}", help=f"Remove {ticker}"):
                st.session_state.companies = [
                    c for c in st.session_state.companies if c["ticker"] != ticker
                ]
                st.rerun()

    # ── Add company ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    _render_add_form()


def _render_add_form():
    st.markdown(
        "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
        " text-transform:uppercase; margin-bottom:0.5rem;'>Add position</div>",
        unsafe_allow_html=True,
    )
    with st.form("add_company_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([1, 2, 3, 1])
        with c1:
            new_ticker = st.text_input("Ticker", placeholder="e.g. AAPL", label_visibility="collapsed")
        with c2:
            new_stage = st.selectbox("Stage", STAGES, label_visibility="collapsed")
        with c3:
            new_note = st.text_input("Note", placeholder="Short thesis note", label_visibility="collapsed")
        with c4:
            submitted = st.form_submit_button("Add", use_container_width=True)

        if submitted:
            ticker = new_ticker.strip().upper()
            if not ticker:
                st.error("Ticker is required.")
            elif any(c["ticker"] == ticker for c in st.session_state.companies):
                st.warning(f"{ticker} is already in the portfolio.")
            else:
                st.session_state.companies.append({
                    "ticker": ticker,
                    "stage": new_stage,
                    "note": new_note.strip(),
                })
                st.success(f"Added {ticker} → {new_stage}")
                st.rerun()

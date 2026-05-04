"""
tabs/market_overview.py
────────────────────────
Tab 5: Market Overview
- Stage-level performance heatmap (1D / 5D / 1M)
- Top movers table
- Stage momentum ranking
- Thesis alignment score
"""

import streamlit as st
import plotly.graph_objects as go

from utils.state import STAGES, STAGE_DESCRIPTIONS, STAGE_COLORS
from utils.data import get_quote


# ── Helpers ────────────────────────────────────────────────────────────────────

def _chg_color(val: float) -> str:
    if val > 0:
        return "#4ade80"
    if val < 0:
        return "#f87171"
    return "#6b7280"


def _cell_bg(val: float) -> str:
    """Heatmap cell background based on % change."""
    if val >= 20:
        return "#1a3a00"
    if val >= 10:
        return "#153000"
    if val >= 5:
        return "#0f2500"
    if val >= 0:
        return "#0f1a0f"
    if val >= -5:
        return "#1a0f0f"
    if val >= -10:
        return "#2a0f0f"
    return "#3a0f0f"


def _compute_stage_stats(test_mode: bool) -> dict:
    """Aggregate price stats per stage."""
    companies = st.session_state.companies
    stats = {}
    for stage in STAGES:
        tickers = [c["ticker"] for c in companies if c["stage"] == stage]
        if not tickers:
            stats[stage] = {"count": 0, "avg_1d": 0, "avg_5d": 0, "avg_1m": 0, "tickers": []}
            continue
        chg_1d_list, chg_5d_list, chg_1m_list = [], [], []
        for t in tickers:
            q = get_quote(t, test_mode)
            chg_1d_list.append(q.get("chg_1d", 0))
            chg_5d_list.append(q.get("chg_5d", 0))
            chg_1m_list.append(q.get("chg_1m", 0))
        stats[stage] = {
            "count":   len(tickers),
            "avg_1d":  sum(chg_1d_list) / len(chg_1d_list),
            "avg_5d":  sum(chg_5d_list) / len(chg_5d_list),
            "avg_1m":  sum(chg_1m_list) / len(chg_1m_list),
            "tickers": tickers,
        }
    return stats


# ── Heatmap figure ─────────────────────────────────────────────────────────────

def _heatmap_fig(stats: dict, period: str) -> go.Figure:
    key = {"1D": "avg_1d", "5D": "avg_5d", "1M": "avg_1m"}[period]
    labels = [s.split(" ", 1)[-1] for s in STAGES]
    values = [stats[s][key] for s in STAGES]
    bar_colors = [STAGE_COLORS.get(s, "#4D9FFF") for s in STAGES]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker=dict(
            color=bar_colors,
            opacity=0.85,
            line=dict(color="#0f1117", width=1),
        ),
        text=[f"{'+'if v>=0 else''}{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(size=9, color="#8b8fa8", family="IBM Plex Mono"),
    ))

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        margin=dict(l=10, r=10, t=36, b=10),
        height=220,
        xaxis=dict(
            tickfont=dict(size=9, color="#8b8fa8", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
        ),
        yaxis=dict(
            tickfont=dict(size=8, color="#4a4e6a", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
            ticksuffix="%",
            zeroline=True,
            zerolinecolor="#2a2d3e",
            zerolinewidth=1,
        ),
        title=dict(
            text=f"Stage Avg Performance — {period}",
            font=dict(size=10, color="#8b8fa8", family="IBM Plex Mono"),
            x=0.01,
        ),
        showlegend=False,
    )
    return fig


# ── Main render ────────────────────────────────────────────────────────────────

def render_market_overview(test_mode: bool):
    active = st.session_state.current_stage
    companies = st.session_state.companies

    st.markdown(
        "<div style='font-size:0.75rem; color:#4a8e4a; margin-bottom:0.75rem;'>"
        "Stage-level performance snapshot — see where capital is flowing and which layers are outperforming."
        "</div>",
        unsafe_allow_html=True,
    )

    if not companies:
        st.warning("No companies in the portfolio. Add positions in the Portfolio tab.")
        return

    stats = _compute_stage_stats(test_mode)

    # ── Period selector ──────────────────────────────────────────────────────
    period_col, _, _ = st.columns([1, 2, 2])
    with period_col:
        period = st.radio(
            "Period",
            ["1D", "5D", "1M"],
            horizontal=True,
            key="market_period",
            label_visibility="collapsed",
        )

    st.plotly_chart(
        _heatmap_fig(stats, period),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Stage ranking table ──────────────────────────────────────────────────
    # CSS grid collapses to single column on mobile via theme.py media queries
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(
            "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
            " text-transform:uppercase; margin-bottom:0.5rem;'>Stage momentum ranking</div>",
            unsafe_allow_html=True,
        )
        key_map = {"1D": "avg_1d", "5D": "avg_5d", "1M": "avg_1m"}
        sorted_stages = sorted(STAGES, key=lambda s: stats[s][key_map[period]], reverse=True)

        for rank, stage in enumerate(sorted_stages, 1):
            s = stats[stage]
            val = s[key_map[period]]
            is_active = (stage == active)
            chg_color = _chg_color(val)
            sc = STAGE_COLORS.get(stage, "#8b8fa8")

            st.markdown(
                f"<div style='background:#1a1d27;border:1px solid {'#2a2d3e' if not is_active else sc};"
                f"border-left:3px solid {sc};"
                f"border-radius:0 8px 8px 0;padding:8px 12px;margin-bottom:6px;"
                f"display:flex;justify-content:space-between;align-items:center;"
                f"box-shadow:{'0 0 12px ' + sc + '30' if is_active else 'none'};'>"
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<span style='font-size:0.62rem;color:#4a4e6a;font-family:IBM Plex Mono,monospace;'>#{rank}</span>"
                f"<span style='width:8px;height:8px;border-radius:50%;background:{sc};"
                f"display:inline-block;flex-shrink:0;'></span>"
                f"<span style='font-size:0.78rem;color:{'#ffffff' if is_active else '#8b8fa8'};"
                f"font-weight:{'700' if is_active else '400'};'>{stage}</span>"
                f"</div>"
                f"<div style='font-size:0.84rem;font-weight:700;color:{chg_color};"
                f"font-family:IBM Plex Mono,monospace;'>{'+'if val>=0 else''}{val:.1f}%</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Top movers ───────────────────────────────────────────────────────────
    with right_col:
        st.markdown(
            "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
            " text-transform:uppercase; margin-bottom:0.5rem;'>Top movers</div>",
            unsafe_allow_html=True,
        )

        all_quotes = []
        for co in companies:
            q = get_quote(co["ticker"], test_mode)
            val = q.get({"1D": "chg_1d", "5D": "chg_5d", "1M": "chg_1m"}[period], 0)
            all_quotes.append({
                "ticker": co["ticker"],
                "stage":  co["stage"],
                "val":    val,
            })

        all_quotes.sort(key=lambda x: x["val"], reverse=True)
        gainers = all_quotes[:5]
        losers  = all_quotes[-3:][::-1]

        st.markdown(
            "<div style='font-size:0.65rem; color:#2a5e2a; margin-bottom:4px;'>▲ Top gainers</div>",
            unsafe_allow_html=True,
        )
        for item in gainers:
            color = _chg_color(item["val"])
            st.markdown(
                f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:4px;"
                f" padding:5px 10px; margin-bottom:4px; display:flex; justify-content:space-between;'>"
                f"<span style='font-size:0.75rem; font-weight:700; color:#90c890;'>{item['ticker']}</span>"
                f"<span style='font-size:0.65rem; color:#3a6e3a;'>{item['stage'].split(' ',1)[-1]}</span>"
                f"<span style='font-size:0.75rem; color:{color}; font-weight:700;'>"
                f"{'+'if item['val']>=0 else''}{item['val']:.1f}%</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div style='font-size:0.65rem; color:#3a1a1a; margin-bottom:4px; margin-top:8px;'>▼ Laggards</div>",
            unsafe_allow_html=True,
        )
        for item in losers:
            color = _chg_color(item["val"])
            st.markdown(
                f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:4px;"
                f" padding:5px 10px; margin-bottom:4px; display:flex; justify-content:space-between;'>"
                f"<span style='font-size:0.75rem; font-weight:700; color:#90c890;'>{item['ticker']}</span>"
                f"<span style='font-size:0.65rem; color:#3a6e3a;'>{item['stage'].split(' ',1)[-1]}</span>"
                f"<span style='font-size:0.75rem; color:{color}; font-weight:700;'>"
                f"{'+'if item['val']>=0 else''}{item['val']:.1f}%</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Thesis alignment score ────────────────────────────────────────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    active_val = stats.get(active, {}).get(key_map[period], 0)
    other_avg  = sum(
        stats[s][key_map[period]] for s in STAGES if s != active
    ) / max(len(STAGES) - 1, 1)

    outperform = active_val - other_avg
    score = min(100, max(0, 50 + outperform * 2))

    score_color = "#f0a500" if score >= 65 else ("#4ade80" if score >= 45 else "#f87171")
    st.markdown(
        f"<div style='background:#0f1a0f; border:1px solid #1a2e1a; border-radius:6px;"
        f" padding:14px 18px;'>"
        f"<div style='font-size:0.65rem; color:#3a6e3a; text-transform:uppercase;"
        f" letter-spacing:0.08em;'>Thesis alignment score — {period}</div>"
        f"<div style='display:flex; align-items:center; gap:16px; margin-top:8px;'>"
        f"<div style='font-size:2rem; font-weight:700; color:{score_color};'>{score:.0f}</div>"
        f"<div style='font-size:0.72rem; color:#4a6e4a; max-width:500px;'>"
        f"Active constraint stage (<b style='color:#f0a500;'>{active}</b>) is "
        f"{'outperforming' if outperform >= 0 else 'underperforming'} the rest of the cycle by "
        f"<b style='color:{score_color};'>{'+'if outperform>=0 else''}{outperform:.1f}pp</b>. "
        f"{'Capital is rotating to the constraint. ✓' if outperform >= 0 else 'Watch for rotation shift.'}"
        f"</div>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem; font-size:0.65rem; color:#3a4e3a;"
            " border:1px solid #1a2e1a; border-radius:4px; padding:6px 10px;'>"
            "🧪 TEST MODE — all performance data is dummy. Set TEST_MODE=False in app.py for live data."
            "</div>",
            unsafe_allow_html=True,
        )

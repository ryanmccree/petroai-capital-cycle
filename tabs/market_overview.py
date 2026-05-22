"""
tabs/market_overview.py
────────────────────────
Tab 3: Market Overview  (institutional terminal design)
- Index strip with SVG sparklines
- Cycle heatmap (per-company, HTML)
- Capital-flow rotation bars
- Top movers
- Cycle signals
- Cycle newsflow
- Stage momentum ranking
- Thesis alignment score
"""

import streamlit as st
import plotly.graph_objects as go

from utils.state import STAGES, STAGE_COLORS
from utils.data import get_quote


# ── Static reference data (mirrors design/data.jsx) ──────────────────────────

_INDICES = [
    {"nm": "PETROAI-100", "px": "4,827.42", "ch": "+62.18",  "pct": "+1.31%", "dir": "up",   "seed": 3},
    {"nm": "S&P 500",     "px": "6,148.20", "ch": "+24.80",  "pct": "+0.40%", "dir": "up",   "seed": 14},
    {"nm": "NDX",         "px": "22,481.6", "ch": "+128.4",  "pct": "+0.57%", "dir": "up",   "seed": 25},
    {"nm": "WTI",         "px": "$78.42",   "ch": "+1.84",   "pct": "+2.40%", "dir": "up",   "seed": 36},
    {"nm": "URA",         "px": "$38.92",   "ch": "-0.42",   "pct": "-1.07%", "dir": "dn",   "seed": 47},
    {"nm": "DXY",         "px": "104.28",   "ch": "-0.18",   "pct": "-0.17%", "dir": "dn",   "seed": 58},
]

_SIGNALS = [
    {"stage": "⚡ Energy",      "lbl": "Crude term structure",  "sub": "Backwardation steepening at front",   "val": "+218bps"},
    {"stage": "💻 Compute",     "lbl": "HBM utilization",       "sub": "Samsung + SK Hynix fab loading",      "val": "94.2%"},
    {"stage": "🔋 Power",       "lbl": "PJM forward strip",     "sub": "2027 capacity auction clear",         "val": "$329/MW-d"},
    {"stage": "🔌 Grid",        "lbl": "Transformer lead time", "sub": "GSU 500MVA+",                         "val": "142 wks"},
    {"stage": "🤖 AI",          "lbl": "Tokens / wafer-out",    "sub": "Frontier inference cost",             "val": "$0.038"},
    {"stage": "🛡️ Defense",     "lbl": "FY26 budget velocity",  "sub": "Procurement obligations YoY",         "val": "+11.4%"},
    {"stage": "🌐 Sovereignty", "lbl": "NdPr oxide premium",    "sub": "Ex-China vs CN spot",                 "val": "+34.8%"},
]

_NEWS = [
    {"time": "14:42", "stage": "⚡ Energy",      "hl": "Saudi Aramco signals output discipline through Q3; spot WTI gaps higher pre-open"},
    {"time": "14:31", "stage": "💻 Compute",     "hl": "NVIDIA confirms Blackwell Ultra shipping ahead of schedule; supply-chain checks confirm 1.4M units H2"},
    {"time": "14:18", "stage": "🔋 Power",       "hl": "Vistra–Microsoft 1.6GW PPA expanded with co-located SMR option, structure favors VST capex"},
    {"time": "13:55", "stage": "🌐 Sovereignty", "hl": "Treasury floats expanded outbound investment review on rare earths; MP Materials breaks 30-day base"},
    {"time": "13:41", "stage": "🛡️ Defense",     "hl": "House mark adds $4.2B for autonomous undersea program; KTOS, AVAV named recipients"},
    {"time": "13:22", "stage": "🤖 AI",          "hl": "Frontier model spend now tracking $312B for FY26 across hyperscalers — Morgan Stanley desk note"},
]


# ── Sparkline helpers ─────────────────────────────────────────────────────────

def _gen_series(seed: int, n: int = 30, vol: float = 0.025) -> list:
    v, s, out = 100.0, seed, []
    for _ in range(n):
        s = (s * 9301 + 49297) % 233280
        v *= 1 + ((s / 233280) - 0.5) * vol
        out.append(v)
    return out


def _sparkline_svg(data: list, color: str, w: int = 120, h: int = 24) -> str:
    mn, mx = min(data), max(data)
    rng = mx - mn or 1
    pts = [((i / (len(data) - 1)) * w, h - ((d - mn) / rng) * (h - 4) - 2)
           for i, d in enumerate(data)]
    path = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts))
    area = path + f" L{w},{h} L0,{h} Z"
    gid  = f"sg{abs(hash(color)) % 99991}"
    return (
        f'<svg width="100%" height="{h}" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{color}" stop-opacity="0.35"/>'
        f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<path d="{area}" fill="url(#{gid})"/>'
        f'<path d="{path}" stroke="{color}" stroke-width="1.4" fill="none"/>'
        f'</svg>'
    )


# ── Color helpers ─────────────────────────────────────────────────────────────

def _chg_color(val: float) -> str:
    if val > 0:  return "#34d399"
    if val < 0:  return "#f87171"
    return "#5b6473"


def _sign(val: float) -> str:
    return "+" if val >= 0 else ""


# ── Index strip ───────────────────────────────────────────────────────────────

def _index_strip_html() -> str:
    cells = []
    for ix in _INDICES:
        color = "#34d399" if ix["dir"] == "up" else "#f87171"
        spark = _sparkline_svg(_gen_series(ix["seed"]), color)
        cells.append(
            f"<div class='idx'>"
            f"<div class='nm'>{ix['nm']}</div>"
            f"<div class='px'>{ix['px']}</div>"
            f"<div class='ch'>"
            f"<span style='color:{color}'>{ix['ch']}</span>"
            f"<span style='color:{color}'>{ix['pct']}</span>"
            f"</div>"
            f"<div class='sparkbox'>{spark}</div>"
            f"</div>"
        )
    return "<div class='index-strip'>" + "".join(cells) + "</div>"


# ── Heatmap (per-company, HTML) ───────────────────────────────────────────────

def _heatmap_html(test_mode: bool) -> str:
    companies = st.session_state.companies
    # Collect up to 4 companies per stage, get their 1D change
    stage_buckets: dict[str, list] = {s: [] for s in STAGES}
    for co in companies:
        s = co["stage"]
        if s in stage_buckets and len(stage_buckets[s]) < 4:
            q = get_quote(co["ticker"], test_mode)
            stage_buckets[s].append({
                "sym": co["ticker"],
                "ch":  q.get("chg_1d", 0.0),
            })

    # Build 8-col grid: each group of 4 is one stage in sequence
    cells_html = []
    for stage in STAGES:
        items = stage_buckets[stage]
        sc = STAGE_COLORS.get(stage, "#5b6473")
        for item in items:
            ch  = item["ch"]
            c   = sc if ch >= 0 else "#ef4444"
            intensity = min(abs(ch) / 5.0, 1.0)
            h60 = format(round(intensity * 0x60), "02x")
            h20 = format(round(intensity * 0x20), "02x")
            bg  = f"linear-gradient(135deg,{c}{h60} 0%,{c}{h20} 100%)"
            sign = "+" if ch >= 0 else ""
            cells_html.append(
                f"<div class='heat-cell' style='background:{bg};border-left:2px solid {c}'>"
                f"<div class='t'>{item['sym']}</div>"
                f"<div class='c'>{sign}{ch:.1f}%</div>"
                f"</div>"
            )
        # Pad empty cells for stages with < 4 companies
        for _ in range(4 - len(items)):
            cells_html.append("<div class='heat-cell' style='background:var(--panel-3)'></div>")

    legend = "".join(
        f"<span style='display:inline-flex;align-items:center;gap:4px;'>"
        f"<span style='width:8px;height:8px;background:{STAGE_COLORS.get(s)};border-radius:1px'></span>"
        f"<span>{s.split(' ',1)[-1]}</span>"
        f"</span>"
        for s in STAGES
    )

    return (
        "<div class='panel' style='margin-bottom:12px'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Cycle Heatmap · Intraday</span>"
        "<span class='panel-actions'><span class='chip'>1D</span><span class='chip live'>LIVE</span></span>"
        "</div>"
        "<div class='heatmap'>" + "".join(cells_html) + "</div>"
        "<div style='display:flex;justify-content:space-between;padding:8px 12px;"
        "border-top:1px solid var(--line);font-family:var(--mono);font-size:10px;"
        "color:var(--text-3);letter-spacing:0.1em;text-transform:uppercase;gap:8px;flex-wrap:wrap'>"
        "<span>Color = stage · Intensity = move</span>"
        f"<span style='display:flex;gap:10px;flex-wrap:wrap'>{legend}</span>"
        "</div>"
        "</div>"
    )


# ── Capital-flow rotation bars ────────────────────────────────────────────────

def _flow_html() -> str:
    intensities = st.session_state.constraint_intensities
    rows = []
    for stage in STAGES:
        sc   = STAGE_COLORS.get(stage, "#5b6473")
        val  = intensities.get(stage, 50)
        name = stage.split(" ", 1)[-1]
        glow = f"box-shadow:0 0 8px {sc}"
        rows.append(
            f"<div class='flow-row'>"
            f"<div class='lab'>{name}</div>"
            f"<div class='bar-track'>"
            f"<div class='bar' style='width:{val}%;background:{sc};{glow}'></div>"
            f"</div>"
            f"<div class='num'>{val}</div>"
            f"</div>"
        )
    return (
        "<div class='panel'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Capital Flow · Cross-Stage Rotation</span>"
        "<span class='panel-actions'><span class='chip'>5D</span></span>"
        "</div>"
        "<div class='flow-vis'>" + "".join(rows) + "</div>"
        "</div>"
    )


# ── Top movers ────────────────────────────────────────────────────────────────

def _movers_html(test_mode: bool, period: str) -> str:
    companies = st.session_state.companies
    key = {"1D": "chg_1d", "5D": "chg_5d", "1M": "chg_1m"}[period]
    all_q = []
    for co in companies:
        q   = get_quote(co["ticker"], test_mode)
        val = q.get(key, 0.0)
        all_q.append({
            "ticker": co["ticker"],
            "stage":  co["stage"],
            "price":  q.get("price", 0.0),
            "val":    val,
        })
    all_q.sort(key=lambda x: x["val"], reverse=True)

    rows = []
    for item in all_q[:7]:
        sc    = STAGE_COLORS.get(item["stage"], "#5b6473")
        color = _chg_color(item["val"])
        sign  = _sign(item["val"])
        rows.append(
            f"<div class='mover-row'>"
            f"<div class='mover-bar' style='background:{sc}'></div>"
            f"<div>"
            f"<div class='mover-sym'>{item['ticker']}</div>"
            f"<div class='mover-nm'>{item['stage'].split(' ',1)[-1]}</div>"
            f"</div>"
            f"<span class='mover-px'>${item['price']:.2f}</span>"
            f"<span class='mover-ch' style='color:{color}'>{sign}{item['val']:.1f}%</span>"
            f"</div>"
        )

    return (
        "<div class='panel' style='margin-bottom:12px'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Top Movers</span>"
        "<span class='panel-actions'>"
        f"<span class='chip'>{period}</span>"
        "</span>"
        "</div>"
        + "".join(rows) +
        "</div>"
    )


# ── Cycle signals ─────────────────────────────────────────────────────────────

def _signals_html() -> str:
    rows = []
    for sig in _SIGNALS:
        sc = STAGE_COLORS.get(sig["stage"], "#5b6473")
        rows.append(
            f"<div class='signal-row'>"
            f"<div class='signal-lhs'>"
            f"<span class='signal-dot' style='background:{sc};box-shadow:0 0 10px {sc}'></span>"
            f"<div class='signal-lbl'>{sig['lbl']}"
            f"<small class='signal-sub'>{sig['sub']}</small></div>"
            f"</div>"
            f"<span class='signal-val'>{sig['val']}</span>"
            f"</div>"
        )
    return (
        "<div class='panel' style='margin-bottom:12px'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Cycle Signals</span>"
        "<span class='panel-actions'><span class='chip live'>Real-Time</span></span>"
        "</div>"
        + "".join(rows) +
        "</div>"
    )


# ── Cycle newsflow ────────────────────────────────────────────────────────────

def _news_html() -> str:
    rows = []
    for n in _NEWS:
        sc = STAGE_COLORS.get(n["stage"], "#5b6473")
        stage_name = n["stage"].split(" ", 1)[-1]
        rows.append(
            f"<div class='news-row'>"
            f"<span class='news-time'>{n['time']}</span>"
            f"<div>"
            f"<span class='news-src' style='color:{sc}'>{stage_name}</span>"
            f"<div class='news-hl'>{n['hl']}</div>"
            f"</div>"
            f"</div>"
        )
    return (
        "<div class='panel'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Cycle Newsflow</span>"
        "<span class='panel-actions'><span class='chip'>All Stages</span></span>"
        "</div>"
        + "".join(rows) +
        "</div>"
    )


# ── Stage ranking ─────────────────────────────────────────────────────────────

def _compute_stage_stats(test_mode: bool) -> dict:
    companies = st.session_state.companies
    stats = {}
    for stage in STAGES:
        tickers = [c["ticker"] for c in companies if c["stage"] == stage]
        if not tickers:
            stats[stage] = {"count": 0, "avg_1d": 0, "avg_5d": 0, "avg_1m": 0}
            continue
        chg_1d, chg_5d, chg_1m = [], [], []
        for t in tickers:
            q = get_quote(t, test_mode)
            chg_1d.append(q.get("chg_1d", 0))
            chg_5d.append(q.get("chg_5d", 0))
            chg_1m.append(q.get("chg_1m", 0))
        n = len(tickers)
        stats[stage] = {
            "count":  n,
            "avg_1d": sum(chg_1d) / n,
            "avg_5d": sum(chg_5d) / n,
            "avg_1m": sum(chg_1m) / n,
        }
    return stats


def _stage_ranking_html(stats: dict, active: str, period: str) -> str:
    key_map = {"1D": "avg_1d", "5D": "avg_5d", "1M": "avg_1m"}
    key = key_map[period]
    sorted_stages = sorted(STAGES, key=lambda s: stats[s][key], reverse=True)

    rows = []
    for rank, stage in enumerate(sorted_stages, 1):
        val       = stats[stage][key]
        sc        = STAGE_COLORS.get(stage, "#5b6473")
        color     = _chg_color(val)
        is_active = stage == active
        name      = stage.split(" ", 1)[-1]
        fw        = "700" if is_active else "400"
        tc        = "var(--text)" if is_active else "var(--text-2)"
        rows.append(
            f"<div class='rank-row' style='background:{'var(--panel-2)' if is_active else 'transparent'}'>"
            f"<div class='rank-lhs'>"
            f"<span class='rank-num'>#{rank}</span>"
            f"<span class='rank-dot' style='background:{sc};box-shadow:0 0 8px {sc}40'></span>"
            f"<span class='rank-name' style='color:{tc};font-weight:{fw}'>{name}</span>"
            f"</div>"
            f"<span class='rank-val' style='color:{color}'>{_sign(val)}{val:.1f}%</span>"
            f"</div>"
        )

    return (
        "<div class='panel'>"
        "<div class='panel-head'>"
        "<span class='panel-title'>Stage Momentum Ranking</span>"
        f"<span class='panel-actions'><span class='chip'>{period}</span></span>"
        "</div>"
        + "".join(rows) +
        "</div>"
    )


# ── Thesis alignment score ────────────────────────────────────────────────────

def _alignment_html(stats: dict, active: str, period: str) -> str:
    key_map = {"1D": "avg_1d", "5D": "avg_5d", "1M": "avg_1m"}
    key = key_map[period]
    active_val = stats.get(active, {}).get(key, 0)
    other_avg  = sum(stats[s][key] for s in STAGES if s != active) / max(len(STAGES) - 1, 1)
    outperform = active_val - other_avg
    score      = min(100, max(0, 50 + outperform * 2))
    color      = "#f4d220" if score >= 65 else ("#34d399" if score >= 45 else "#f87171")
    active_name = active.split(" ", 1)[-1]

    return (
        f"<div class='alignment-card'>"
        f"<div style='font-size:10px;color:var(--text-3);text-transform:uppercase;letter-spacing:0.12em;"
        f"font-family:var(--mono)'>Thesis Alignment Score — {period}</div>"
        f"<div style='display:flex;align-items:center;gap:16px;margin-top:8px'>"
        f"<div style='font-size:28px;font-weight:600;color:{color};font-family:var(--mono)'>{score:.0f}</div>"
        f"<div style='font-size:11px;color:var(--text-3);max-width:480px;font-family:var(--mono)'>"
        f"Active constraint (<span style='color:#f59e0b'>{active_name}</span>) is "
        f"{'outperforming' if outperform >= 0 else 'underperforming'} rest of cycle by "
        f"<span style='color:{color}'>{_sign(outperform)}{outperform:.1f}pp</span>. "
        f"{'Capital rotating to constraint. ✓' if outperform >= 0 else 'Watch for rotation shift.'}"
        f"</div></div></div>"
    )


# ── Main render ───────────────────────────────────────────────────────────────

def render_market_overview(test_mode: bool):
    active    = st.session_state.current_stage
    companies = st.session_state.companies

    if not companies:
        st.warning("No companies in the portfolio. Add positions in the Portfolio tab.")
        return

    # Period selector
    _, period_col, _ = st.columns([3, 1, 3])
    with period_col:
        period = st.radio(
            "Period",
            ["1D", "5D", "1M"],
            horizontal=True,
            key="market_period",
            label_visibility="collapsed",
        )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Index strip ──────────────────────────────────────────────────────────
    st.markdown(_index_strip_html(), unsafe_allow_html=True)

    # ── Two-column layout ────────────────────────────────────────────────────
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # Cycle heatmap
        st.markdown(_heatmap_html(test_mode), unsafe_allow_html=True)

        # Capital flow rotation
        st.markdown(_flow_html(), unsafe_allow_html=True)

    with right_col:
        # Top movers
        st.markdown(_movers_html(test_mode, period), unsafe_allow_html=True)

        # Cycle signals
        st.markdown(_signals_html(), unsafe_allow_html=True)

        # Cycle newsflow
        st.markdown(_news_html(), unsafe_allow_html=True)

    # ── Stage ranking + alignment ────────────────────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    stats = _compute_stage_stats(test_mode)

    rank_col, align_col = st.columns([1, 1])

    with rank_col:
        st.markdown(_stage_ranking_html(stats, active, period), unsafe_allow_html=True)

    with align_col:
        st.markdown(_alignment_html(stats, active, period), unsafe_allow_html=True)

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem;font-size:10px;color:var(--text-3);"
            "border:1px solid var(--line);border-radius:4px;padding:6px 10px;"
            "font-family:var(--mono)'>TEST MODE — all performance data is dummy.</div>",
            unsafe_allow_html=True,
        )

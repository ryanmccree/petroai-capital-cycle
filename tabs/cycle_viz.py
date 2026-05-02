"""
tabs/cycle_viz.py
─────────────────
Cycle Visualization Tab
- Horizontal flow diagram (Plotly) or Circular mode
- Nodes = 8 stages, amber highlight on active constraint
- Clickable nodes → show assigned companies
- Animated flow arrows between stages
"""

import streamlit as st
import plotly.graph_objects as go
import math

from utils.state import STAGES, STAGE_DESCRIPTIONS


# ── Color scheme ──────────────────────────────────────────────────────────────
BG         = "#0a0e0a"
NODE_BASE  = "#0f1a0f"
NODE_BORDER= "#2a5e2a"
NODE_TEXT  = "#c8d8c0"
ACTIVE_BG  = "#1a1400"
ACTIVE_BRD = "#f0a500"
ACTIVE_TXT = "#f0a500"
ARROW_CLR  = "#2a5e2a"
ARROW_ACTV = "#f0a500"
PILL_BG    = "#1a2e1a"
PILL_TXT   = "#90c890"
ACTIVE_PILL_BG  = "#2a1a00"
ACTIVE_PILL_TXT = "#f0a500"
GLOW_COLOR = "rgba(240,165,0,0.4)"


def _companies_for_stage(stage: str) -> list[str]:
    """Return list of tickers assigned to a given stage."""
    return [c["ticker"] for c in st.session_state.companies if c["stage"] == stage]


def _render_horizontal_flow():
    """Render the 8-stage horizontal flow using Plotly shapes + annotations."""
    active = st.session_state.current_stage
    n = len(STAGES)
    fig = go.Figure()

    # Layout constants — larger boxes with better spacing
    BOX_W, BOX_H = 2.0, 1.2
    GAP = 0.65
    STEP = BOX_W + GAP
    Y_CENTER = 0
    ARROW_Y = Y_CENTER
    LABEL_Y = Y_CENTER + 0.02

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        margin=dict(l=10, r=10, t=36, b=48),
        height=320,
        xaxis=dict(visible=False, range=[-0.4, STEP * n]),
        yaxis=dict(visible=False, range=[-1.3, 1.6]),
        showlegend=False,
    )

    for i, stage in enumerate(STAGES):
        x0 = i * STEP
        x1 = x0 + BOX_W
        xc = (x0 + x1) / 2
        is_active = (stage == active)

        companies = _companies_for_stage(stage)
        pill_text = "  ".join(companies[:4]) + ("  +" + str(len(companies)-4) if len(companies) > 4 else "")

        # Box fill
        fig.add_shape(
            type="rect",
            x0=x0, y0=Y_CENTER - BOX_H/2,
            x1=x1, y1=Y_CENTER + BOX_H/2,
            fillcolor=ACTIVE_BG if is_active else NODE_BASE,
            line=dict(
                color=ACTIVE_BRD if is_active else NODE_BORDER,
                width=2.5 if is_active else 1.2,
            ),
        )

        # Glow effect for active node
        if is_active:
            fig.add_shape(
                type="rect",
                x0=x0-0.08, y0=Y_CENTER - BOX_H/2 - 0.08,
                x1=x1+0.08, y1=Y_CENTER + BOX_H/2 + 0.08,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color=GLOW_COLOR, width=8),
            )

        # Stage emoji + name
        fig.add_annotation(
            x=xc, y=LABEL_Y + 0.22,
            text=f"<b>{stage}</b>",
            showarrow=False,
            font=dict(size=12, color=ACTIVE_TXT if is_active else NODE_TEXT, family="IBM Plex Mono"),
            xanchor="center",
        )

        # Companies pills text
        if pill_text:
            fig.add_annotation(
                x=xc, y=LABEL_Y - 0.28,
                text=pill_text,
                showarrow=False,
                font=dict(size=9, color=ACTIVE_PILL_TXT if is_active else PILL_TXT, family="IBM Plex Mono"),
                xanchor="center",
            )

        # Description below box
        desc = STAGE_DESCRIPTIONS.get(stage, "")
        short_desc = desc[:42] + "…" if len(desc) > 42 else desc
        fig.add_annotation(
            x=xc, y=Y_CENTER - BOX_H/2 - 0.28,
            text=short_desc,
            showarrow=False,
            font=dict(size=8, color="#3a6e3a", family="IBM Plex Mono"),
            xanchor="center",
        )

        # Arrow to next stage
        if i < n - 1:
            ax = x1 + GAP/2
            fig.add_annotation(
                x=ax, y=ARROW_Y,
                text="→",
                showarrow=False,
                font=dict(size=20, color=ARROW_ACTV if is_active else ARROW_CLR),
                xanchor="center",
            )

        # Active constraint badge above box
        if is_active:
            fig.add_annotation(
                x=xc, y=Y_CENTER + BOX_H/2 + 0.28,
                text="▲ ACTIVE CONSTRAINT",
                showarrow=False,
                font=dict(size=8.5, color=ACTIVE_BRD, family="IBM Plex Mono"),
                xanchor="center",
            )

    return fig


def _render_circular_flow():
    """Render the 8-stage cycle as a circular Plotly diagram."""
    active = st.session_state.current_stage
    n = len(STAGES)
    fig = go.Figure()

    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        margin=dict(l=30, r=30, t=30, b=30),
        height=600,
        xaxis=dict(visible=False, range=[-2.3, 2.3]),
        yaxis=dict(visible=False, range=[-2.3, 2.3], scaleanchor="x"),
        showlegend=False,
    )

    R = 1.58      # node center radius
    BOX_W = 0.85
    BOX_H = 0.50

    # Draw outer ring circle
    theta_ring = [i * 2 * math.pi / 360 for i in range(361)]
    fig.add_trace(go.Scatter(
        x=[R * math.cos(t) for t in theta_ring],
        y=[R * math.sin(t) for t in theta_ring],
        mode="lines",
        line=dict(color="#1a2e1a", width=1, dash="dot"),
        hoverinfo="skip",
    ))

    for i, stage in enumerate(STAGES):
        angle = math.pi / 2 - i * 2 * math.pi / n
        cx = R * math.cos(angle)
        cy = R * math.sin(angle)
        is_active = (stage == active)

        companies = _companies_for_stage(stage)
        pill_txt = " ".join(companies[:3]) + ("…" if len(companies) > 3 else "")

        # Box
        fig.add_shape(
            type="rect",
            x0=cx - BOX_W/2, y0=cy - BOX_H/2,
            x1=cx + BOX_W/2, y1=cy + BOX_H/2,
            fillcolor=ACTIVE_BG if is_active else NODE_BASE,
            line=dict(color=ACTIVE_BRD if is_active else NODE_BORDER, width=2 if is_active else 1),
        )
        if is_active:
            fig.add_shape(
                type="rect",
                x0=cx - BOX_W/2 - 0.04, y0=cy - BOX_H/2 - 0.04,
                x1=cx + BOX_W/2 + 0.04, y1=cy + BOX_H/2 + 0.04,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color=GLOW_COLOR, width=5),
            )

        fig.add_annotation(
            x=cx, y=cy + 0.08,
            text=f"<b>{stage}</b>",
            showarrow=False,
            font=dict(size=10, color=ACTIVE_TXT if is_active else NODE_TEXT, family="IBM Plex Mono"),
            xanchor="center",
        )
        if pill_txt:
            fig.add_annotation(
                x=cx, y=cy - 0.13,
                text=pill_txt,
                showarrow=False,
                font=dict(size=8.5, color=ACTIVE_PILL_TXT if is_active else PILL_TXT, family="IBM Plex Mono"),
                xanchor="center",
            )

        # Arrow to next node
        next_angle = math.pi / 2 - ((i + 1) % n) * 2 * math.pi / n
        nx = R * math.cos(next_angle)
        ny = R * math.sin(next_angle)

        # Midpoint slightly inside the ring for the arrowhead
        mx = (cx + nx) / 2 * 0.82
        my = (cy + ny) / 2 * 0.82

        fig.add_annotation(
            ax=cx * 0.91, ay=cy * 0.91,
            x=nx * 0.91,  y=ny * 0.91,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.0,
            arrowwidth=1.5,
            arrowcolor=ARROW_ACTV if is_active else ARROW_CLR,
        )

    # Center label
    fig.add_annotation(
        x=0, y=0,
        text="<b>PetroAI<br>Flywheel</b>",
        showarrow=False,
        font=dict(size=14, color="#4a8e4a", family="IBM Plex Mono"),
        xanchor="center",
        yanchor="middle",
    )

    return fig


def _render_heatmap():
    """Render the 8 stages as a 4×2 colored heatmap grid."""
    active = st.session_state.current_stage
    intensities = st.session_state.get("constraint_intensities", {})

    cols = st.columns(4)
    for i, stage in enumerate(STAGES):
        intensity = intensities.get(stage, 50)
        t = intensity / 100.0

        # Interpolate dark green (#0f1a0f) → bright amber (#f0a500)
        r = int(15 + 225 * t)
        g = int(26 + 139 * t)
        b = int(15 * (1 - t))
        tile_bg = f"rgb({r},{g},{b})"

        is_active = (stage == active)
        border_css = (
            "border:2px solid #f0a500;box-shadow:0 0 14px 4px rgba(240,165,0,0.55);"
            if is_active else "border:1px solid #2a5e2a;"
        )

        companies = _companies_for_stage(stage)
        pill_html = "".join(
            f"<span style='background:#0a0e0a;color:#90c890;border-radius:3px;"
            f"padding:1px 5px;font-size:0.58rem;margin:1px 2px;display:inline-block;'>{tk}</span>"
            for tk in companies[:6]
        ) or "<span style='font-size:0.6rem;opacity:0.35;color:#c8d8c0;'>—</span>"

        text_color = "#0a0e0a" if intensity > 65 else "#c8d8c0"
        pct_color = "#f0a500" if is_active else ("#0a0e0a" if intensity > 65 else "#4ade80")
        active_badge = (
            "<div style='position:absolute;top:9px;right:11px;font-size:0.62rem;"
            "color:#f0a500;font-weight:700;letter-spacing:0.07em;'>▲ ACTIVE</div>"
            if is_active else ""
        )

        html = (
            f"<div style='background:{tile_bg};{border_css}border-radius:10px;"
            f"padding:20px 16px;margin:0 0 10px 0;min-height:160px;position:relative;'>"
            f"{active_badge}"
            f"<div style='font-size:0.82rem;font-weight:700;color:{text_color};"
            f"font-family:IBM Plex Mono,monospace;margin-bottom:8px;'>{stage}</div>"
            f"<div style='font-size:2rem;font-weight:700;color:{pct_color};"
            f"font-family:IBM Plex Mono,monospace;line-height:1;'>{intensity}%</div>"
            f"<div style='font-size:0.62rem;color:{text_color};opacity:0.65;"
            f"margin-bottom:10px;'>constraint intensity</div>"
            f"<div>{pill_html}</div>"
            f"</div>"
        )
        with cols[i % 4]:
            st.markdown(html.strip(), unsafe_allow_html=True)


def render_cycle_viz(test_mode: bool):
    """Main entry point for the Cycle Visualization tab."""

    active = st.session_state.current_stage

    st.markdown(
        f"<div style='font-size:0.82rem;color:#4a8e4a;margin-bottom:1.1rem;"
        f"padding:10px 14px;background:#0d140d;border:1px solid #1a2e1a;"
        f"border-left:3px solid #f0a500;border-radius:4px;'>"
        f"Active constraint: "
        f"<span style='color:#f0a500;font-weight:700;'>{active}</span>"
        f"<span style='color:#3a6e3a;'> — {STAGE_DESCRIPTIONS.get(active,'')}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # ── Diagram ──────────────────────────────────────────────────────────────
    viz_mode = st.session_state.get("viz_mode", "Horizontal Flow")

    if viz_mode == "Horizontal Flow":
        st.markdown("<div class='flow-scroll-container'>", unsafe_allow_html=True)
        fig = _render_horizontal_flow()
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    elif viz_mode == "Circular":
        fig = _render_circular_flow()
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        _render_heatmap()

    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    # ── Stage breakdown cards ─────────────────────────────────────────────────
    st.markdown(
        "<div class='section-header'>Stage breakdown</div>",
        unsafe_allow_html=True,
    )

    col_count = 4
    cols = st.columns(col_count)
    for i, stage in enumerate(STAGES):
        is_active = (stage == active)
        companies = _companies_for_stage(stage)
        pills = "".join(
            f"<span class='company-pill'>{t}</span>" for t in companies
        ) if companies else "<span style='color:#2a4e2a;font-size:0.65rem;'>—</span>"

        card_class = "stage-card active-constraint" if is_active else "stage-card"
        html = (
            f"<div class='{card_class}'>"
            f"<div class='stage-name'>{stage}</div>"
            f"<div class='stage-desc'>{STAGE_DESCRIPTIONS.get(stage,'')}</div>"
            f"<div style='margin-top:8px;'>{pills}</div>"
            f"</div>"
        )
        with cols[i % col_count]:
            st.markdown(html, unsafe_allow_html=True)

    # ── Quick-set constraint shortcut ────────────────────────────────────────
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-header'>Quick-set active constraint</div>",
        unsafe_allow_html=True,
    )
    btn_cols = st.columns(len(STAGES))
    for i, stage in enumerate(STAGES):
        is_active = (stage == active)
        emoji = stage.split(" ")[0]
        short = stage.split(" ", 1)[1] if " " in stage else stage
        with btn_cols[i]:
            if st.button(
                f"{emoji}\n{short}",
                key=f"qset_{i}",
                help=stage,
                type="primary" if is_active else "secondary",
                use_container_width=True,
            ):
                st.session_state.current_stage = stage
                st.rerun()

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem; font-size:0.65rem; color:#3a4e3a;"
            " border:1px solid #1a2e1a; border-radius:4px; padding:6px 10px;'>"
            "🧪 TEST MODE active — all price data is hardcoded. "
            "Set <code>TEST_MODE = False</code> in <code>app.py</code> to use live yfinance data."
            "</div>",
            unsafe_allow_html=True,
        )

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

from utils.state import STAGES, STAGE_DESCRIPTIONS, STAGE_COLORS, STAGE_CSS_KEYS, STAGE_IMAGES


# ── Color scheme (slate dark) ─────────────────────────────────────────────────
BG         = "#0f1117"
NODE_BASE  = "#1a1d27"
NODE_BORDER= "#2a2d3e"
NODE_TEXT  = "#ffffff"
ARROW_CLR  = "#2a2d3e"
PILL_TXT   = "#8b8fa8"


def _hex_rgba(h: str, a: float) -> str:
    r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return f"rgba({r},{g},{b},{a})"


def _companies_for_stage(stage: str) -> list[str]:
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
        sc = STAGE_COLORS.get(stage, "#ffffff")

        companies = _companies_for_stage(stage)
        pill_text = "  ".join(companies[:4]) + ("  +" + str(len(companies)-4) if len(companies) > 4 else "")

        # Box fill — stage color fill at low opacity
        fig.add_shape(
            type="rect",
            x0=x0, y0=Y_CENTER - BOX_H/2,
            x1=x1, y1=Y_CENTER + BOX_H/2,
            fillcolor=_hex_rgba(sc, 0.12) if is_active else NODE_BASE,
            line=dict(color=sc if is_active else _hex_rgba(sc, 0.4), width=2.5 if is_active else 1.2),
        )

        # Glow for active node
        if is_active:
            fig.add_shape(
                type="rect",
                x0=x0-0.08, y0=Y_CENTER - BOX_H/2 - 0.08,
                x1=x1+0.08, y1=Y_CENTER + BOX_H/2 + 0.08,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color=_hex_rgba(sc, 0.45), width=8),
            )

        # Stage name
        fig.add_annotation(
            x=xc, y=LABEL_Y + 0.22,
            text=f"<b>{stage}</b>",
            showarrow=False,
            font=dict(size=13, color=sc if is_active else NODE_TEXT, family="IBM Plex Mono"),
            xanchor="center",
        )

        # Ticker pills
        if pill_text:
            fig.add_annotation(
                x=xc, y=LABEL_Y - 0.28,
                text=pill_text,
                showarrow=False,
                font=dict(size=10, color=_hex_rgba(sc, 0.9) if is_active else "#c8ccd8", family="IBM Plex Mono"),
                xanchor="center",
            )

        # Description below box
        desc = STAGE_DESCRIPTIONS.get(stage, "")
        short_desc = desc[:42] + "…" if len(desc) > 42 else desc
        fig.add_annotation(
            x=xc, y=Y_CENTER - BOX_H/2 - 0.28,
            text=short_desc,
            showarrow=False,
            font=dict(size=9, color=_hex_rgba(sc, 0.6), family="IBM Plex Mono"),
            xanchor="center",
        )

        # Arrow to next stage
        if i < n - 1:
            ax = x1 + GAP/2
            next_sc = STAGE_COLORS.get(STAGES[i + 1], "#ffffff")
            fig.add_annotation(
                x=ax, y=ARROW_Y,
                text="→",
                showarrow=False,
                font=dict(size=20, color=sc if is_active else ARROW_CLR),
                xanchor="center",
            )

        # Active badge
        if is_active:
            fig.add_annotation(
                x=xc, y=Y_CENTER + BOX_H/2 + 0.28,
                text="▲ ACTIVE CONSTRAINT",
                showarrow=False,
                font=dict(size=8.5, color=sc, family="IBM Plex Mono"),
                xanchor="center",
            )

    return fig


def _render_circular_flow():
    """Professional flywheel — 8 stage nodes on a ring with arc arrows and center hub."""
    active = st.session_state.current_stage
    n      = len(STAGES)
    fig    = go.Figure()

    R          = 1.55   # ring radius (node centers)
    R_HUB      = 0.44   # hub circle radius
    R_ARC      = 1.70   # arc arrow radius (outside ring)
    HW         = 0.43   # node half-width
    HH         = 0.29   # node half-height
    ARC_MARGIN = 0.10   # radians to trim near each node end

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=24, b=24),
        height=650,
        xaxis=dict(visible=False, range=[-2.4, 2.4]),
        yaxis=dict(visible=False, range=[-2.4, 2.4], scaleanchor="x"),
        showlegend=False,
        clickmode="event+select",
    )

    # ── Outer dashed ring ────────────────────────────────────────────────────
    ring_t = [2 * math.pi * k / 120 for k in range(121)]
    fig.add_trace(go.Scatter(
        x=[R * math.cos(t) for t in ring_t],
        y=[R * math.sin(t) for t in ring_t],
        mode="lines",
        line=dict(color="#2a2d3e", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False,
    ))

    # ── Center hub ───────────────────────────────────────────────────────────
    fig.add_shape(type="circle",
        x0=-R_HUB, y0=-R_HUB, x1=R_HUB, y1=R_HUB,
        fillcolor="#13151f", line=dict(color="#2a2d3e", width=2))
    fig.add_shape(type="circle",
        x0=-R_HUB*0.82, y0=-R_HUB*0.82, x1=R_HUB*0.82, y1=R_HUB*0.82,
        fillcolor="rgba(0,0,0,0)", line=dict(color="#1e2130", width=1, dash="dot"))

    for text, y_pos, sz, color in [
        ("<b>PetroAI</b>",   0.19, 12,  "#FF9500"),
        ("Flywheel",         0.04, 9.5, "#8b8fa8"),
        ("Solve one →",     -0.12, 7,   "#4a4e6a"),
        ("expose the next", -0.22, 7,   "#4a4e6a"),
    ]:
        fig.add_annotation(x=0, y=y_pos, text=text, showarrow=False,
            font=dict(size=sz, color=color, family="IBM Plex Mono"),
            xanchor="center", yanchor="middle")

    # Clockwise rotation indicators inside hub
    for hub_deg in [30, 120, 210, 300]:
        ha = math.radians(hub_deg)
        pr = R_HUB * 0.54
        px, py = pr * math.cos(ha), pr * math.sin(ha)
        tx, ty = math.sin(ha) * 0.055, -math.cos(ha) * 0.055
        fig.add_annotation(ax=px - tx, ay=py - ty, x=px + tx, y=py + ty,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=0.7, arrowwidth=1,
            arrowcolor="#2a2d3e")

    # ── Nodes + arc arrows + click targets ───────────────────────────────────
    scatter_x, scatter_y, hover_texts, stage_labels = [], [], [], []

    for i, stage in enumerate(STAGES):
        angle = math.pi / 2 - i * math.pi / 4      # clock positions, clockwise
        cx    = R * math.cos(angle)
        cy    = R * math.sin(angle)
        is_active = (stage == active)
        sc = STAGE_COLORS.get(stage, "#ffffff")
        companies = _companies_for_stage(stage)
        tickers_txt = " · ".join(companies[:3])

        # Glow rings (active only)
        if is_active:
            for pad, alpha, lw in [(0.08, 0.25, 8), (0.14, 0.10, 6)]:
                fig.add_shape(type="rect",
                    x0=cx-HW-pad, y0=cy-HH-pad, x1=cx+HW+pad, y1=cy+HH+pad,
                    fillcolor="rgba(0,0,0,0)",
                    line=dict(color=_hex_rgba(sc, alpha), width=lw))

        # Node box
        fig.add_shape(type="rect",
            x0=cx-HW, y0=cy-HH, x1=cx+HW, y1=cy+HH,
            fillcolor=_hex_rgba(sc, 0.40 if is_active else 0.14),
            line=dict(color=sc, width=3 if is_active else 1.8))

        # "▲ ACTIVE" badge above the node
        if is_active:
            fig.add_annotation(x=cx, y=cy+HH+0.13, text="▲ ACTIVE", showarrow=False,
                font=dict(size=7.5, color=sc, family="IBM Plex Mono"),
                xanchor="center", yanchor="bottom",
                bgcolor=_hex_rgba(sc, 0.18), bordercolor=sc,
                borderwidth=1, borderpad=3)

        # Emoji (large, top of node)
        emoji = stage.split(" ")[0]
        fig.add_annotation(x=cx, y=cy+0.15, text=emoji, showarrow=False,
            font=dict(size=17), xanchor="center", yanchor="middle")

        # Stage name (middle)
        name = stage.split(" ", 1)[1] if " " in stage else stage
        fig.add_annotation(x=cx, y=cy-0.02, text=f"<b>{name}</b>", showarrow=False,
            font=dict(size=11, color=sc if is_active else "#ffffff",
                      family="IBM Plex Mono"),
            xanchor="center", yanchor="middle")

        # Tickers (bottom)
        if tickers_txt:
            fig.add_annotation(x=cx, y=cy-0.19, text=tickers_txt, showarrow=False,
                font=dict(size=9,
                          color=_hex_rgba(sc, 0.95) if is_active else "#c8ccd8",
                          family="IBM Plex Mono"),
                xanchor="center", yanchor="middle")

        # Arc arrow to next stage (clockwise = decreasing angle)
        # arc_delta always decreases by exactly (π/4 − 2·margin), no wrap needed
        arc_start = angle - ARC_MARGIN
        arc_delta = -(math.pi / 4 - 2 * ARC_MARGIN)
        n_arc = 25
        arc_t = [arc_start + arc_delta * k / (n_arc - 1) for k in range(n_arc)]
        arc_x = [R_ARC * math.cos(t) for t in arc_t]
        arc_y = [R_ARC * math.sin(t) for t in arc_t]

        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y, mode="lines",
            line=dict(
                color=sc if is_active else _hex_rgba(sc, 0.50),
                width=2.8 if is_active else 1.5,
                dash="dash" if is_active else "solid",
            ),
            hoverinfo="skip", showlegend=False,
        ))
        # Arrowhead at end of arc (from [-3] → [-1] gives correct tangent direction)
        fig.add_annotation(
            ax=arc_x[-3], ay=arc_y[-3], x=arc_x[-1], y=arc_y[-1],
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2,
            arrowsize=1.2 if is_active else 0.9,
            arrowwidth=2.5 if is_active else 1.5,
            arrowcolor=sc if is_active else _hex_rgba(sc, 0.50))

        # Invisible click-target data
        scatter_x.append(cx)
        scatter_y.append(cy)
        stage_labels.append(stage)
        desc = STAGE_DESCRIPTIONS.get(stage, "")
        tickers_hover = ", ".join(companies) if companies else "—"
        hover_texts.append(
            f"<b>{stage}</b><br><i>{desc}</i><br><br>"
            f"<b>Positions:</b> {tickers_hover}<br>"
            f"<span style='color:#666;font-size:0.8em;'>Click to set as active constraint</span>"
        )

    # Invisible large markers — intercept clicks on node areas
    fig.add_trace(go.Scatter(
        x=scatter_x, y=scatter_y,
        mode="markers",
        marker=dict(size=80, opacity=0, color="rgba(0,0,0,0)"),
        customdata=stage_labels,
        hovertemplate="%{hovertext}<extra></extra>",
        hovertext=hover_texts,
        showlegend=False,
    ))

    return fig


def _render_heatmap():
    """Render the 8 stages as a 4×2 heatmap grid with background images."""
    active = st.session_state.current_stage
    intensities = st.session_state.get("constraint_intensities", {})

    cols = st.columns(4)
    for i, stage in enumerate(STAGES):
        intensity = intensities.get(stage, 50)
        sc = STAGE_COLORS.get(stage, "#ffffff")
        css_key = STAGE_CSS_KEYS.get(stage, "energy")
        is_active = (stage == active)

        companies = _companies_for_stage(stage)
        pill_html = "".join(
            f"<span style='background:rgba(0,0,0,0.5);color:{sc};border-radius:3px;"
            f"padding:2px 6px;font-size:0.6rem;margin:2px 2px 0 0;display:inline-block;"
            f"border:1px solid {_hex_rgba(sc, 0.3)};font-family:IBM Plex Mono,monospace;"
            f"font-weight:600;'>{tk}</span>"
            for tk in companies[:6]
        ) or f"<span style='font-size:0.6rem;opacity:0.35;color:#8b8fa8;'>—</span>"

        active_badge = (
            f"<div style='position:absolute;top:9px;right:11px;font-size:0.6rem;"
            f"color:{sc};font-weight:700;letter-spacing:0.07em;font-family:IBM Plex Mono,monospace;"
            f"background:rgba(0,0,0,0.5);padding:2px 6px;border-radius:3px;'>▲ ACTIVE</div>"
            if is_active else ""
        )
        active_extra = f"border:2px solid {sc};box-shadow:0 0 20px {_hex_rgba(sc, 0.45)};" if is_active else ""

        html = (
            f"<div class='stage-img-card si-{css_key}{' active-img-card' if is_active else ''}' "
            f"style='min-height:160px;padding:20px 16px;{active_extra}'>"
            f"{active_badge}"
            f"<div style='font-size:0.82rem;font-weight:700;color:{sc};"
            f"font-family:DM Sans,sans-serif;margin-bottom:6px;'>{stage}</div>"
            f"<div style='font-size:2.1rem;font-weight:700;color:#ffffff;"
            f"font-family:IBM Plex Mono,monospace;line-height:1;'>{intensity}%</div>"
            f"<div style='font-size:0.6rem;color:rgba(255,255,255,0.45);"
            f"font-family:IBM Plex Mono,monospace;margin-bottom:10px;'>constraint intensity</div>"
            f"<div>{pill_html}</div>"
            f"</div>"
        )
        with cols[i % 4]:
            st.markdown(html, unsafe_allow_html=True)


def render_cycle_viz(test_mode: bool):
    """Main entry point for the Cycle Visualization tab."""

    active = st.session_state.current_stage

    active_sc = STAGE_COLORS.get(active, "#FF9500")
    st.markdown(
        f"<div style='font-size:0.82rem;color:#8b8fa8;margin-bottom:1.1rem;"
        f"padding:12px 16px;background:#1a1d27;border:1px solid #2a2d3e;"
        f"border-left:4px solid {active_sc};border-radius:0 8px 8px 0;"
        f"box-shadow:0 0 20px {_hex_rgba(active_sc,0.15)};'>"
        f"Active constraint: "
        f"<span style='color:{active_sc};font-weight:700;'>{active}</span>"
        f"<span style='color:#4a4e6a;'> — {STAGE_DESCRIPTIONS.get(active,'')}</span>"
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
        try:
            event = st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
                on_select="rerun",
                selection_mode=["points"],
                key="flywheel_chart",
            )
            sel = getattr(event, "selection", None) or {}
            pts = sel.get("points", []) if isinstance(sel, dict) else getattr(sel, "points", [])
            if pts:
                first = pts[0]
                clicked = (first.get("customdata") if isinstance(first, dict)
                           else getattr(first, "customdata", None))
                if clicked and clicked in STAGES and clicked != st.session_state.current_stage:
                    st.session_state.current_stage = clicked
                    st.rerun()
        except TypeError:
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
        sc = STAGE_COLORS.get(stage, "#ffffff")
        css_key = STAGE_CSS_KEYS.get(stage, "energy")
        companies = _companies_for_stage(stage)
        pills = "".join(
            f"<span style='background:rgba(0,0,0,0.5);color:{sc};border-radius:3px;"
            f"padding:2px 6px;font-size:0.62rem;margin:3px 2px 0 0;display:inline-block;"
            f"border:1px solid {_hex_rgba(sc,0.3)};font-family:IBM Plex Mono,monospace;"
            f"font-weight:600;'>{t}</span>"
            for t in companies
        ) if companies else "<span style='font-size:0.65rem;opacity:0.35;color:#8b8fa8;'>—</span>"

        active_extra = f"border:2px solid {sc};box-shadow:0 0 20px {_hex_rgba(sc,0.35)};" if is_active else ""
        html = (
            f"<div class='stage-img-card si-{css_key}' style='min-height:110px;{active_extra}'>"
            f"<div style='font-size:0.88rem;font-weight:700;color:{sc};"
            f"font-family:DM Sans,sans-serif;margin-bottom:4px;'>{stage}</div>"
            f"<div style='font-size:0.67rem;color:rgba(255,255,255,0.55);"
            f"font-family:IBM Plex Mono,monospace;line-height:1.4;margin-bottom:8px;'>"
            f"{STAGE_DESCRIPTIONS.get(stage,'')}</div>"
            f"<div>{pills}</div>"
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

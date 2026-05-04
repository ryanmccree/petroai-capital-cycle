"""
tabs/constraints.py
────────────────────
Tab 3: Constraint Tracker
- Visual intensity bars per stage
- Constraint rotation log with timeline
- Adjust intensity sliders interactively
- Add new constraint log entries
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

from utils.state import STAGES, STAGE_DESCRIPTIONS, STAGE_COLORS


def _intensity_color(val: int) -> str:
    if val >= 80: return "#FF6B2B"
    if val >= 60: return "#FFD700"
    if val >= 40: return "#4D9FFF"
    return "#2a2d3e"


def _intensity_label(val: int) -> str:
    if val >= 80:
        return "CRITICAL"
    if val >= 60:
        return "HIGH"
    if val >= 40:
        return "MODERATE"
    return "LOW"


# ── Intensity bar chart ───────────────────────────────────────────────────────

def _render_intensity_chart():
    intensities = st.session_state.constraint_intensities
    active = st.session_state.current_stage

    labels = [s.split(" ", 1)[-1] for s in STAGES]
    values = [intensities.get(s, 50) for s in STAGES]
    colors = [STAGE_COLORS.get(s, "#4D9FFF") for s in STAGES]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker_color=colors,
        marker_line_color="#0f1117",
        marker_line_width=1,
        text=[f"{v}" for v in values],
        textposition="outside",
        textfont=dict(size=9, color="#8b8fa8", family="IBM Plex Mono"),
    ))

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        margin=dict(l=10, r=10, t=36, b=10),
        height=240,
        xaxis=dict(
            tickfont=dict(size=9, color="#8b8fa8", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
            linecolor="#2a2d3e",
        ),
        yaxis=dict(
            range=[0, 115],
            tickfont=dict(size=8, color="#4a4e6a", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
            tickvals=[0, 25, 50, 75, 100],
        ),
        title=dict(
            text="Constraint Intensity by Stage",
            font=dict(size=10, color="#8b8fa8", family="IBM Plex Mono"),
            x=0.01,
        ),
        showlegend=False,
    )

    fig.add_hline(y=80, line_dash="dot", line_color="#FF6B2B", line_width=1, opacity=0.4)
    fig.add_annotation(
        x=len(STAGES) - 0.5, y=83,
        text="Critical threshold",
        showarrow=False,
        font=dict(size=7, color="#FF6B2B", family="IBM Plex Mono"),
        xanchor="right",
    )

    return fig


# ── Main render ────────────────────────────────────────────────────────────────

def render_constraints(test_mode: bool):
    active = st.session_state.current_stage

    st.markdown(
        "<div style='font-size:0.75rem; color:#4a8e4a; margin-bottom:0.75rem;'>"
        "Track which stage is the current bottleneck — capital rotates to wherever the constraint is highest."
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Intensity chart ──────────────────────────────────────────────────────
    fig = _render_intensity_chart()
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ── Intensity sliders ────────────────────────────────────────────────────
    left_col, right_col = st.columns([1.8, 1])

    with left_col:
        st.markdown(
            "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
            " text-transform:uppercase; margin-bottom:0.75rem;'>Adjust constraint intensity</div>",
            unsafe_allow_html=True,
        )
        changed = False
        for stage in STAGES:
            is_active = (stage == active)
            current_val = st.session_state.constraint_intensities.get(stage, 50)
            label_color = "#f0a500" if is_active else "#7a9e7a"
            intensity_label = _intensity_label(current_val)
            color = _intensity_color(current_val)

            col_lbl, col_slide, col_badge = st.columns([2, 4, 1.2])
            with col_lbl:
                st.markdown(
                    f"<div style='font-size:0.72rem; color:{label_color}; padding-top:6px;"
                    f" font-weight:{'700' if is_active else '400'};'>{stage}</div>",
                    unsafe_allow_html=True,
                )
            with col_slide:
                new_val = st.slider(
                    stage,
                    0, 100,
                    current_val,
                    key=f"intensity_{stage}",
                    label_visibility="collapsed",
                )
                if new_val != current_val:
                    st.session_state.constraint_intensities[stage] = new_val
                    changed = True
            with col_badge:
                st.markdown(
                    f"<div style='background:#0f1a0f; border:1px solid {color}33; border-radius:3px;"
                    f" padding:3px 6px; font-size:0.6rem; color:{color}; text-align:center;"
                    f" margin-top:4px; font-weight:700; letter-spacing:0.06em;'>{intensity_label}</div>",
                    unsafe_allow_html=True,
                )

        if changed:
            st.rerun()

    # ── Constraint log ───────────────────────────────────────────────────────
    with right_col:
        st.markdown(
            "<div style='font-size:0.7rem; color:#3a6e3a; letter-spacing:0.08em;"
            " text-transform:uppercase; margin-bottom:0.75rem;'>Rotation log</div>",
            unsafe_allow_html=True,
        )

        log = st.session_state.constraint_log
        for entry in reversed(log):
            date  = entry.get("date", "")
            stage = entry.get("stage", "")
            note  = entry.get("note", "")
            sc = STAGE_COLORS.get(stage, "#8b8fa8")

            st.markdown(
                f"<div style='background:#1a1d27;border-left:3px solid {sc};"
                f"padding:10px 12px;margin-bottom:8px;border-radius:0 8px 8px 0;"
                f"box-shadow:0 2px 8px rgba(0,0,0,0.2);'>"
                f"<div style='font-size:0.62rem;color:#4a4e6a;font-family:IBM Plex Mono,monospace;'>{date}</div>"
                f"<div style='font-size:0.78rem;color:{sc};font-weight:700;margin:3px 0;"
                f"font-family:DM Sans,sans-serif;'>{stage}</div>"
                f"<div style='font-size:0.68rem;color:#8b8fa8;line-height:1.45;"
                f"font-family:IBM Plex Mono,monospace;'>{note}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # Add log entry form
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        with st.expander("+ Add log entry"):
            with st.form("add_log_form", clear_on_submit=True):
                log_stage = st.selectbox("Stage", STAGES, key="log_stage_sel")
                log_date  = st.text_input("Date (e.g. 2025-Q2)", placeholder="2025-Q2")
                log_note  = st.text_area("Note", placeholder="What changed at this stage?", height=80)
                if st.form_submit_button("Add entry"):
                    if log_note.strip():
                        st.session_state.constraint_log.append({
                            "date":  log_date.strip() or datetime.now().strftime("%Y-%m-%d"),
                            "stage": log_stage,
                            "note":  log_note.strip(),
                        })
                        st.success("Entry added.")
                        st.rerun()
                    else:
                        st.error("Note is required.")

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem; font-size:0.65rem; color:#3a4e3a;"
            " border:1px solid #1a2e1a; border-radius:4px; padding:6px 10px;'>"
            "🧪 TEST MODE — intensity values are editable but not persisted across sessions."
            "</div>",
            unsafe_allow_html=True,
        )

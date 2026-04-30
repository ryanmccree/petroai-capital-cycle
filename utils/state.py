"""
utils/state.py
Centralized session state initialization.
All keys are defined here so every tab can import them safely.
"""

import streamlit as st

# Default companies pre-loaded into the cycle
DEFAULT_COMPANIES = [
    {"ticker": "OKLO",  "stage": "⚡ Energy",       "note": "Micro-nuclear power"},
    {"ticker": "CEG",   "stage": "⚡ Energy",       "note": "Nuclear + power gen"},
    {"ticker": "ETN",   "stage": "🔋 Power",        "note": "Power mgmt & data center"},
    {"ticker": "VST",   "stage": "🔋 Power",        "note": "Power generation"},
    {"ticker": "NRG",   "stage": "🔌 Grid",         "note": "Grid & demand response"},
    {"ticker": "ANET",  "stage": "🔌 Grid",         "note": "Network infrastructure"},
    {"ticker": "NVDA",  "stage": "💻 Compute",      "note": "GPU compute leader"},
    {"ticker": "NVTS",  "stage": "💻 Compute",      "note": "AI chip efficiency"},
    {"ticker": "MU",    "stage": "🔁 Transfer",     "note": "Memory / HBM"},
    {"ticker": "COHR",  "stage": "🔁 Transfer",     "note": "Optical interconnects"},
    {"ticker": "RGTI",  "stage": "🤖 AI",           "note": "Quantum AI"},
    {"ticker": "IONQ",  "stage": "🤖 AI",           "note": "Quantum computing"},
    {"ticker": "QBTS",  "stage": "🤖 AI",           "note": "Quantum systems"},
    {"ticker": "PLTR",  "stage": "🛡️ Defense",      "note": "AI defense analytics"},
    {"ticker": "MP",    "stage": "🛡️ Defense",      "note": "Rare earth / defense supply"},
    {"ticker": "CRML",  "stage": "🌐 Sovereignty",  "note": "Critical minerals"},
    {"ticker": "INTC",  "stage": "💻 Compute",      "note": "Semiconductor fab"},
    {"ticker": "CIFR",  "stage": "⚡ Energy",       "note": "Bitcoin / energy arb"},
    {"ticker": "CRWV",  "stage": "💻 Compute",      "note": "AI cloud infra"},
]

STAGES = [
    "⚡ Energy",
    "🔋 Power",
    "🔌 Grid",
    "💻 Compute",
    "🔁 Transfer",
    "🤖 AI",
    "🛡️ Defense",
    "🌐 Sovereignty",
]

STAGE_DESCRIPTIONS = {
    "⚡ Energy":       "Solve the energy source constraint — nuclear, gas, renewables",
    "🔋 Power":        "Convert & manage power — transformers, UPS, power electronics",
    "🔌 Grid":         "Distribute power & data — transmission, networking, fiber",
    "💻 Compute":      "Process at scale — GPUs, ASICs, semiconductor fab",
    "🔁 Transfer":     "Move data fast — memory, optical, high-bandwidth interconnects",
    "🤖 AI":           "Intelligence layer — models, inference, quantum acceleration",
    "🛡️ Defense":      "Protect & deploy — autonomous systems, cyber, DoD AI",
    "🌐 Sovereignty":  "Control critical inputs — minerals, chips, data, energy independence",
}


def init_session_state():
    """Initialize all session state keys with defaults. Safe to call on every run."""

    if "companies" not in st.session_state:
        st.session_state.companies = DEFAULT_COMPANIES.copy()

    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "💻 Compute"

    if "viz_mode" not in st.session_state:
        st.session_state.viz_mode = "Horizontal Flow"

    if "constraint_log" not in st.session_state:
        st.session_state.constraint_log = [
            {"date": "2024-Q1", "stage": "⚡ Energy",   "note": "Power availability became the primary AI build-out constraint."},
            {"date": "2024-Q3", "stage": "🔌 Grid",     "note": "Grid interconnection queues exceeded 2,000 GW backlog in the US."},
            {"date": "2025-Q1", "stage": "💻 Compute",  "note": "NVDA H100 allocation constraints drove hyperscaler capex surge."},
        ]

    if "constraint_intensities" not in st.session_state:
        st.session_state.constraint_intensities = {
            "⚡ Energy": 65,
            "🔋 Power": 70,
            "🔌 Grid": 80,
            "💻 Compute": 95,
            "🔁 Transfer": 60,
            "🤖 AI": 50,
            "🛡️ Defense": 45,
            "🌐 Sovereignty": 55,
        }

    if "price_cache" not in st.session_state:
        st.session_state.price_cache = {}

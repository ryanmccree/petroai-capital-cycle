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
    {"ticker": "GFS",   "stage": "💻 Compute",      "note": "Domestic semiconductor fab — US chip sovereignty play"},
    {"ticker": "GLW",   "stage": "🔁 Transfer",     "note": "Fiber optic infrastructure — backbone of AI data transfer"},
    {"ticker": "AA",    "stage": "🌐 Sovereignty",  "note": "Domestic aluminum supply — critical material for AI infrastructure buildout"},
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

STAGE_COLORS = {
    "⚡ Energy":      "#FF6B2B",
    "🔋 Power":       "#FFD700",
    "🔌 Grid":        "#00D4FF",
    "💻 Compute":     "#4D9FFF",
    "🔁 Transfer":    "#00FF94",
    "🤖 AI":          "#B44DFF",
    "🛡️ Defense":     "#FF3B3B",
    "🌐 Sovereignty": "#FF9500",
}

STAGE_CSS_KEYS = {
    "⚡ Energy":      "energy",
    "🔋 Power":       "power",
    "🔌 Grid":        "grid",
    "💻 Compute":     "compute",
    "🔁 Transfer":    "transfer",
    "🤖 AI":          "ai",
    "🛡️ Defense":     "defense",
    "🌐 Sovereignty": "sovereignty",
}

STAGE_IMAGES = {
    "⚡ Energy":      "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&q=80",
    "🔋 Power":       "https://images.unsplash.com/photo-1548337138-e87d889cc369?w=800&q=80",
    "🔌 Grid":        "https://images.unsplash.com/photo-1544724569-5f546fd6f2b5?w=800&q=80",
    "💻 Compute":     "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80",
    "🔁 Transfer":    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80",
    "🤖 AI":          "https://images.unsplash.com/photo-1677442135703-1787eea5ce01?w=800&q=80",
    "🛡️ Defense":     "https://images.unsplash.com/photo-1521694468822-1e20e3f1b68e?w=800&q=80",
    "🌐 Sovereignty": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=80",
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

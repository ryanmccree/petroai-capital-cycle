"""
tabs/deep_dive.py
──────────────────
Tab 4: Company Deep Dive
- Select any company from the portfolio
- 30-day price chart with volume
- Key metrics: price, changes, market cap
- Stage context and thesis note
- Company summary, income statement, balance sheet (live or TEST_MODE dummy)
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

from utils.state import STAGES, STAGE_DESCRIPTIONS, STAGE_COLORS, STAGE_CSS_KEYS, STAGE_IMAGES
from utils.data import get_quote, get_sparkline, DUMMY_QUOTES


# ── Dummy fundamental data ─────────────────────────────────────────────────────

_DUMMY_INFO = {
    "NVDA": {
        "summary": (
            "NVIDIA Corporation designs and manufactures graphics processing units, chipsets, "
            "and system-on-chip units used in gaming, data centers, and AI workloads. "
            "The company is the dominant supplier of AI training and inference accelerators, "
            "making it the central infrastructure layer in the compute stage of the capital cycle."
        ),
        "sector": "Technology", "industry": "Semiconductors",
        "employees": 29600, "city": "Santa Clara", "state": "CA", "country": "United States",
        "website": "https://www.nvidia.com", "ceo": "Jensen Huang",
    },
    "PLTR": {
        "summary": (
            "Palantir Technologies Inc. builds software platforms — Gotham, Foundry, and AIP — "
            "that enable government agencies and large enterprises to integrate and analyze "
            "complex, large-scale data. "
            "Its AI Platform (AIP) is accelerating commercial adoption across defense and enterprise verticals."
        ),
        "sector": "Technology", "industry": "Software — Infrastructure",
        "employees": 3584, "city": "Denver", "state": "CO", "country": "United States",
        "website": "https://www.palantir.com", "ceo": "Alex Karp",
    },
    "OKLO": {
        "summary": (
            "Oklo Inc. is developing advanced fission power plants to deliver clean, reliable, "
            "and affordable baseload energy at scale. "
            "Its Aurora compact fast reactor is designed to operate for years without refueling, "
            "targeting data center operators, industrial sites, and government facilities."
        ),
        "sector": "Utilities", "industry": "Nuclear Power",
        "employees": 120, "city": "Santa Clara", "state": "CA", "country": "United States",
        "website": "https://www.oklo.com", "ceo": "Jacob DeWitte",
    },
    "MU": {
        "summary": (
            "Micron Technology Inc. produces DRAM, NAND flash, and NOR flash memory and storage "
            "products for compute, networking, mobile, embedded, and storage markets. "
            "Micron is a critical supplier of high-bandwidth memory used in AI accelerators, "
            "positioning it at the intersection of memory and compute in the capital cycle."
        ),
        "sector": "Technology", "industry": "Semiconductors",
        "employees": 48000, "city": "Boise", "state": "ID", "country": "United States",
        "website": "https://www.micron.com", "ceo": "Sanjay Mehrotra",
    },
    "ANET": {
        "summary": (
            "Arista Networks Inc. develops and sells cloud networking solutions including Ethernet "
            "switches and routers optimized for hyperscale data center environments. "
            "Its EOS software platform and CloudVision management suite are widely deployed across "
            "AI training clusters requiring high-throughput, low-latency network fabric."
        ),
        "sector": "Technology", "industry": "Computer Networking",
        "employees": 4400, "city": "Santa Clara", "state": "CA", "country": "United States",
        "website": "https://www.arista.com", "ceo": "Jayshree Ullal",
    },
    "ETN": {
        "summary": (
            "Eaton Corporation plc is a power management company providing electrical switchgear, "
            "transformers, UPS systems, and busway products critical for grid modernization and "
            "data center power infrastructure. "
            "Eaton is a primary beneficiary of the grid upgrade supercycle driven by AI electrification demand."
        ),
        "sector": "Industrials", "industry": "Electrical Equipment & Parts",
        "employees": 92000, "city": "Dublin", "state": "", "country": "Ireland",
        "website": "https://www.eaton.com", "ceo": "Craig Arnold",
    },
    "VST": {
        "summary": (
            "Vistra Corp is an integrated retail electricity and power generation company with "
            "over 41 GW of capacity from natural gas, nuclear, solar, and battery storage assets. "
            "Its nuclear fleet and flexible generation make it a key supplier of 24/7 clean firm "
            "power to hyperscalers and AI data centers."
        ),
        "sector": "Utilities", "industry": "Utilities — Independent Power Producers",
        "employees": 6000, "city": "Irving", "state": "TX", "country": "United States",
        "website": "https://www.vistracorp.com", "ceo": "Jim Burke",
    },
}

_GENERIC_INFO = {
    "summary": (
        "This company operates in a sector relevant to the PetroAI Capital Cycle thesis. "
        "Live company data is available when TEST_MODE is disabled. "
        "The business contributes to the broader energy, compute, and AI infrastructure stack."
    ),
    "sector": "N/A", "industry": "N/A",
    "employees": None, "city": "N/A", "state": "", "country": "N/A",
    "website": None, "ceo": "N/A",
}

_Q_LABELS = ["Q1 2025", "Q4 2024", "Q3 2024", "Q2 2024"]

_DUMMY_INCOME = {
    "NVDA": {
        "Total Revenue":    [26_044_000_000, 22_103_000_000, 18_120_000_000, 13_507_000_000],
        "Gross Profit":     [19_434_000_000, 16_791_000_000, 14_004_000_000,  9_462_000_000],
        "Operating Income": [16_909_000_000, 14_742_000_000, 11_993_000_000,  7_658_000_000],
        "Net Income":       [14_881_000_000, 12_843_000_000, 10_019_000_000,  6_188_000_000],
        "EBITDA":           [17_540_000_000, 15_310_000_000, 12_490_000_000,  7_980_000_000],
    },
    "PLTR": {
        "Total Revenue":    [  884_000_000,   828_000_000,   726_000_000,   678_000_000],
        "Gross Profit":     [  718_000_000,   671_000_000,   581_000_000,   546_000_000],
        "Operating Income": [   69_000_000,    42_000_000,    25_000_000,    10_000_000],
        "Net Income":       [  214_000_000,   149_000_000,   144_000_000,    84_000_000],
        "EBITDA":           [  106_000_000,    79_000_000,    62_000_000,    48_000_000],
    },
    "OKLO": {
        "Total Revenue":    [            0,             0,             0,             0],
        "Gross Profit":     [   -5_200_000,    -4_100_000,    -3_400_000,    -3_100_000],
        "Operating Income": [  -22_100_000,   -18_400_000,   -14_800_000,   -12_200_000],
        "Net Income":       [  -20_300_000,   -16_100_000,   -13_200_000,   -11_000_000],
        "EBITDA":           [  -19_200_000,   -15_000_000,   -12_100_000,   -10_400_000],
    },
    "MU": {
        "Total Revenue":    [8_705_000_000,  8_707_000_000,  7_750_000_000,  6_811_000_000],
        "Gross Profit":     [3_718_000_000,  3_718_000_000,  3_016_000_000,  2_086_000_000],
        "Operating Income": [1_565_000_000,  1_557_000_000,    941_000_000,    414_000_000],
        "Net Income":       [1_584_000_000,  1_568_000_000,    887_000_000,    476_000_000],
        "EBITDA":           [3_450_000_000,  3_440_000_000,  2_820_000_000,  2_180_000_000],
    },
    "ANET": {
        "Total Revenue":    [1_932_000_000,  1_931_000_000,  1_811_000_000,  1_690_000_000],
        "Gross Profit":     [1_220_000_000,  1_219_000_000,  1_143_000_000,  1_063_000_000],
        "Operating Income": [  624_000_000,    621_000_000,    574_000_000,    520_000_000],
        "Net Income":       [  730_000_000,    728_000_000,    578_000_000,    540_000_000],
        "EBITDA":           [  681_000_000,    678_000_000,    627_000_000,    574_000_000],
    },
    "ETN": {
        "Total Revenue":    [6_236_000_000,  6_207_000_000,  6_100_000_000,  5_940_000_000],
        "Gross Profit":     [2_720_000_000,  2_706_000_000,  2_634_000_000,  2_520_000_000],
        "Operating Income": [1_305_000_000,  1_295_000_000,  1_250_000_000,  1_152_000_000],
        "Net Income":       [1_054_000_000,  1_048_000_000,    977_000_000,    868_000_000],
        "EBITDA":           [1_498_000_000,  1_485_000_000,  1_450_000_000,  1_350_000_000],
    },
    "VST": {
        "Total Revenue":    [4_520_000_000,  3_820_000_000,  6_130_000_000,  3_920_000_000],
        "Gross Profit":     [  904_000_000,    610_000_000,  1_840_000_000,    706_000_000],
        "Operating Income": [  402_000_000,    204_000_000,  1_420_000_000,    302_000_000],
        "Net Income":       [  254_000_000,    104_000_000,    952_000_000,    152_000_000],
        "EBITDA":           [  851_000_000,    552_000_000,  1_950_000_000,    651_000_000],
    },
}

_GENERIC_INCOME = {
    "Total Revenue":    [1_200_000_000,  1_100_000_000,  1_050_000_000,   980_000_000],
    "Gross Profit":     [  480_000_000,    440_000_000,    420_000_000,   392_000_000],
    "Operating Income": [  144_000_000,    132_000_000,    126_000_000,   118_000_000],
    "Net Income":       [  108_000_000,     99_000_000,     94_000_000,    88_000_000],
    "EBITDA":           [  192_000_000,    176_000_000,    168_000_000,   157_000_000],
}

_DUMMY_BALANCE = {
    "NVDA": {
        "Total Assets":       [111_601_000_000, 65_728_000_000, 60_114_000_000, 56_563_000_000],
        "Total Liabilities":  [ 30_282_000_000, 23_416_000_000, 22_148_000_000, 22_266_000_000],
        "Total Equity":       [ 80_491_000_000, 42_978_000_000, 38_905_000_000, 34_264_000_000],
        "Cash & Equivalents": [  8_241_000_000,  7_954_000_000,  7_281_000_000,  6_400_000_000],
        "Total Debt":         [  8_992_000_000,  8_980_000_000,  8_984_000_000,  9_703_000_000],
    },
    "PLTR": {
        "Total Assets":       [4_635_000_000,  4_503_000_000,  4_302_000_000,  4_104_000_000],
        "Total Liabilities":  [  498_000_000,    487_000_000,    471_000_000,    456_000_000],
        "Total Equity":       [4_137_000_000,  4_016_000_000,  3_831_000_000,  3_648_000_000],
        "Cash & Equivalents": [2_024_000_000,  1_941_000_000,  1_832_000_000,  1_646_000_000],
        "Total Debt":         [            0,              0,              0,              0],
    },
    "OKLO": {
        "Total Assets":       [471_000_000,  452_000_000,  432_000_000,  412_000_000],
        "Total Liabilities":  [ 61_000_000,   56_000_000,   49_000_000,   44_000_000],
        "Total Equity":       [410_000_000,  396_000_000,  383_000_000,  368_000_000],
        "Cash & Equivalents": [312_000_000,  298_000_000,  281_000_000,  271_000_000],
        "Total Debt":         [          0,            0,            0,            0],
    },
    "MU": {
        "Total Assets":       [64_141_000_000, 63_919_000_000, 56_048_000_000, 55_163_000_000],
        "Total Liabilities":  [22_048_000_000, 22_140_000_000, 19_819_000_000, 19_614_000_000],
        "Total Equity":       [42_093_000_000, 41_779_000_000, 36_229_000_000, 35_549_000_000],
        "Cash & Equivalents": [ 8_502_000_000,  8_502_000_000,  7_846_000_000,  7_223_000_000],
        "Total Debt":         [12_234_000_000, 12_281_000_000, 10_997_000_000, 11_153_000_000],
    },
    "ANET": {
        "Total Assets":       [11_028_000_000, 10_982_000_000, 10_058_000_000,  9_712_000_000],
        "Total Liabilities":  [ 3_028_000_000,  2_982_000_000,  2_858_000_000,  2_712_000_000],
        "Total Equity":       [ 8_000_000_000,  8_000_000_000,  7_200_000_000,  7_000_000_000],
        "Cash & Equivalents": [ 5_821_000_000,  5_774_000_000,  5_212_000_000,  4_912_000_000],
        "Total Debt":         [             0,              0,              0,              0],
    },
    "ETN": {
        "Total Assets":       [51_940_000_000, 51_812_000_000, 50_104_000_000, 49_218_000_000],
        "Total Liabilities":  [26_014_000_000, 25_940_000_000, 25_104_000_000, 24_818_000_000],
        "Total Equity":       [25_926_000_000, 25_872_000_000, 25_000_000_000, 24_400_000_000],
        "Cash & Equivalents": [   924_000_000,    910_000_000,    840_000_000,    820_000_000],
        "Total Debt":         [ 9_982_000_000,  9_940_000_000,  9_504_000_000,  9_490_000_000],
    },
    "VST": {
        "Total Assets":       [34_142_000_000, 33_182_000_000, 32_248_000_000, 29_410_000_000],
        "Total Liabilities":  [27_040_000_000, 26_482_000_000, 26_048_000_000, 23_410_000_000],
        "Total Equity":       [ 7_102_000_000,  6_700_000_000,  6_200_000_000,  6_000_000_000],
        "Cash & Equivalents": [ 1_520_000_000,  1_218_000_000,  3_842_000_000,  1_102_000_000],
        "Total Debt":         [13_182_000_000, 13_040_000_000, 12_048_000_000, 10_020_000_000],
    },
}

_GENERIC_BALANCE = {
    "Total Assets":       [5_000_000_000,  4_800_000_000,  4_600_000_000,  4_400_000_000],
    "Total Liabilities":  [2_000_000_000,  1_920_000_000,  1_840_000_000,  1_760_000_000],
    "Total Equity":       [3_000_000_000,  2_880_000_000,  2_760_000_000,  2_640_000_000],
    "Cash & Equivalents": [  800_000_000,    760_000_000,    720_000_000,    680_000_000],
    "Total Debt":         [  600_000_000,    580_000_000,    560_000_000,    540_000_000],
}


# ── Number formatting ──────────────────────────────────────────────────────────

def _fmt_num(val) -> str:
    try:
        v = float(val)
    except (TypeError, ValueError):
        return "N/A"
    if v == 0:
        return "$0"
    neg = v < 0
    av = abs(v)
    if av >= 1e12:
        s = f"${av/1e12:.2f}T"
    elif av >= 1e9:
        s = f"${av/1e9:.2f}B"
    elif av >= 1e6:
        s = f"${av/1e6:.1f}M"
    else:
        s = f"${av/1e3:.1f}K"
    return f"-{s}" if neg else s


def _val_color(val) -> str:
    try:
        v = float(val)
    except (TypeError, ValueError):
        return "#8b8fa8"
    if v > 0:
        return "#4ade80"
    if v < 0:
        return "#f87171"
    return "#8b8fa8"


# ── Data fetchers ──────────────────────────────────────────────────────────────

def _get_company_info(ticker: str, test_mode: bool) -> dict:
    if test_mode:
        return _DUMMY_INFO.get(ticker, _GENERIC_INFO)
    try:
        import yfinance as yf
        info = yf.Ticker(ticker).info
        raw = info.get("longBusinessSummary", "")
        sentences = [s.strip() for s in raw.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        summary = ". ".join(sentences[:3]) + ("." if sentences else "")
        officers = info.get("companyOfficers", [])
        ceo = next(
            (o.get("name", "N/A") for o in officers
             if "CEO" in o.get("title", "").upper() or "Chief Executive" in o.get("title", "")),
            officers[0].get("name", "N/A") if officers else "N/A",
        )
        return {
            "summary":   summary or "No description available.",
            "sector":    info.get("sector", "N/A"),
            "industry":  info.get("industry", "N/A"),
            "employees": info.get("fullTimeEmployees"),
            "city":      info.get("city", "N/A"),
            "state":     info.get("state", ""),
            "country":   info.get("country", "N/A"),
            "website":   info.get("website"),
            "ceo":       ceo,
        }
    except Exception as e:
        st.warning(f"⚠️ Could not fetch company info for {ticker}: {e}")
        return _DUMMY_INFO.get(ticker, _GENERIC_INFO)


def _qlabel(col) -> str:
    if hasattr(col, "month"):
        q = (col.month - 1) // 3 + 1
        return f"Q{q} {col.year}"
    return str(col)


def _get_income_stmt(ticker: str, test_mode: bool):
    if test_mode:
        return _DUMMY_INCOME.get(ticker, _GENERIC_INCOME), _Q_LABELS
    try:
        import yfinance as yf
        stmt = yf.Ticker(ticker).quarterly_income_stmt
        if stmt is None or stmt.empty:
            raise ValueError("Empty income statement")
        cols = stmt.columns[:4]
        labels = [_qlabel(c) for c in cols]

        def _row(*names):
            for name in names:
                for idx in stmt.index:
                    if name.lower() in str(idx).lower():
                        return [stmt.loc[idx, c] for c in cols]
            return [None] * 4

        return {
            "Total Revenue":    _row("Total Revenue", "Revenue"),
            "Gross Profit":     _row("Gross Profit"),
            "Operating Income": _row("Operating Income", "Ebit"),
            "Net Income":       _row("Net Income"),
            "EBITDA":           _row("EBITDA", "Ebitda", "Normalized EBITDA"),
        }, labels
    except Exception as e:
        st.warning(f"⚠️ Could not fetch income statement for {ticker}: {e}")
        return _DUMMY_INCOME.get(ticker, _GENERIC_INCOME), _Q_LABELS


def _get_balance_sheet(ticker: str, test_mode: bool):
    if test_mode:
        return _DUMMY_BALANCE.get(ticker, _GENERIC_BALANCE), _Q_LABELS
    try:
        import yfinance as yf
        bs = yf.Ticker(ticker).quarterly_balance_sheet
        if bs is None or bs.empty:
            raise ValueError("Empty balance sheet")
        cols = bs.columns[:4]
        labels = [_qlabel(c) for c in cols]

        def _row(*names):
            for name in names:
                for idx in bs.index:
                    if name.lower() in str(idx).lower():
                        return [bs.loc[idx, c] for c in cols]
            return [None] * 4

        return {
            "Total Assets":       _row("Total Assets"),
            "Total Liabilities":  _row("Total Liabilities Net Minority Interest", "Total Liabilities"),
            "Total Equity":       _row("Stockholders Equity", "Total Equity Gross Minority Interest", "Total Equity"),
            "Cash & Equivalents": _row("Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"),
            "Total Debt":         _row("Total Debt", "Long Term Debt And Capital Lease Obligation"),
        }, labels
    except Exception as e:
        st.warning(f"⚠️ Could not fetch balance sheet for {ticker}: {e}")
        return _DUMMY_BALANCE.get(ticker, _GENERIC_BALANCE), _Q_LABELS


# ── Section renderers ──────────────────────────────────────────────────────────

def _render_company_summary(ticker: str, stage_color: str, test_mode: bool):
    info = _get_company_info(ticker, test_mode)
    hq = ", ".join(p for p in [info.get("city",""), info.get("state",""), info.get("country","")] if p)
    emp = f"{info['employees']:,}" if info.get("employees") else "N/A"
    website = info.get("website") or ""
    web_html = (
        f"<a href='{website}' target='_blank' style='color:{stage_color};text-decoration:none;'>"
        f"{website.replace('https://www.','').replace('https://','')}</a>"
    ) if website else "N/A"

    meta = [
        ("Sector",       info["sector"]),
        ("Industry",     info["industry"]),
        ("Employees",    emp),
        ("Headquarters", hq),
        ("CEO",          info["ceo"]),
        ("Website",      web_html),
    ]
    meta_cells = "".join(
        f"<div>"
        f"<div style='font-size:0.75rem;color:#9da3b4;text-transform:uppercase;"
        f"letter-spacing:0.08em;font-family:IBM Plex Mono,monospace;margin-bottom:2px;'>{k}</div>"
        f"<div style='font-size:0.92rem;color:#c8ccd8;'>{v}</div>"
        f"</div>"
        for k, v in meta
    )

    with st.expander("Company Summary", expanded=True):
        st.markdown(
            f"<div style='background:#1a1d27;border-left:4px solid {stage_color};"
            f"border-radius:0 10px 10px 0;padding:18px 20px;'>"
            f"<div style='font-size:0.95rem;color:#c8ccd8;line-height:1.8;margin-bottom:16px;"
            f"font-family:IBM Plex Mono,monospace;'>{info['summary']}</div>"
            f"<div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'>"
            f"{meta_cells}</div></div>",
            unsafe_allow_html=True,
        )


def _render_fin_table(metrics: dict, labels: list, stage_color: str, title: str):
    th = (
        f"background:{stage_color}22;color:{stage_color};"
        f"font-size:0.82rem;font-family:IBM Plex Mono,monospace;"
        f"padding:8px 10px;text-align:right;font-weight:700;"
        f"border-bottom:2px solid {stage_color}55;"
    )
    th_l = th.replace("text-align:right", "text-align:left")

    header = f"<tr><th style='{th_l}'>Metric</th>"
    for lbl in labels:
        header += f"<th style='{th}'>{lbl}</th>"
    header += "</tr>"

    rows_html = ""
    for i, (metric, values) in enumerate(metrics.items()):
        row_bg = "#1a1d27" if i % 2 == 0 else "#141620"
        td_base = f"font-size:0.92rem;font-family:IBM Plex Mono,monospace;padding:8px 10px;"
        td_lbl  = f"background:{row_bg};color:#c8ccd8;{td_base}border-right:1px solid #2a2d3e;"
        rows_html += f"<tr><td style='{td_lbl}'>{metric}</td>"
        for val in values:
            color = _val_color(val)
            td_val = f"background:{row_bg};color:{color};{td_base}text-align:right;"
            rows_html += f"<td style='{td_val}'>{_fmt_num(val)}</td>"
        rows_html += "</tr>"

    st.markdown(
        f"<div style='font-size:0.7rem;color:{stage_color};text-transform:uppercase;"
        f"letter-spacing:0.1em;font-family:IBM Plex Mono,monospace;"
        f"margin-bottom:8px;font-weight:700;'>{title}</div>"
        f"<div style='overflow-x:auto;'>"
        f"<table style='width:100%;border-collapse:collapse;"
        f"border:1px solid #2a2d3e;border-radius:8px;overflow:hidden;'>"
        f"<thead>{header}</thead><tbody>{rows_html}</tbody></table></div>",
        unsafe_allow_html=True,
    )


def _render_income_stmt(ticker: str, stage_color: str, test_mode: bool):
    data, labels = _get_income_stmt(ticker, test_mode)
    with st.expander("Quarterly Income Statement", expanded=True):
        _render_fin_table(data, labels, stage_color, "Income Statement — Last 4 Quarters")


def _render_balance_sheet(ticker: str, stage_color: str, test_mode: bool):
    data, labels = _get_balance_sheet(ticker, test_mode)
    with st.expander("Quarterly Balance Sheet", expanded=True):
        _render_fin_table(data, labels, stage_color, "Balance Sheet — Last 4 Quarters")

        # Debt/Equity ratio cards
        equity_vals = data.get("Total Equity", [None] * 4)
        debt_vals   = data.get("Total Debt",   [None] * 4)
        de_cards = ""
        for lbl, d, e in zip(labels, debt_vals, equity_vals):
            try:
                de = float(d) / float(e) if float(e) != 0 else 0.0
                color = "#f87171" if de > 2 else ("#FFD700" if de > 1 else "#4ade80")
                de_cards += (
                    f"<div style='background:#1a1d27;border:1px solid #2a2d3e;"
                    f"border-radius:6px;padding:6px 14px;text-align:center;'>"
                    f"<div style='font-size:0.6rem;color:#4a4e6a;"
                    f"font-family:IBM Plex Mono,monospace;'>{lbl}</div>"
                    f"<div style='font-size:0.82rem;font-weight:700;color:{color};"
                    f"font-family:IBM Plex Mono,monospace;margin-top:2px;'>D/E {de:.2f}x</div>"
                    f"</div>"
                )
            except (TypeError, ValueError, ZeroDivisionError):
                pass
        if de_cards:
            st.markdown(
                f"<div style='display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;'>"
                f"{de_cards}</div>",
                unsafe_allow_html=True,
            )


# ── Chart builder ──────────────────────────────────────────────────────────────

def _price_chart(ticker: str, series, stage_color: str, test_mode: bool) -> go.Figure:
    prices = series.tolist()
    n = len(prices)
    xs = list(range(n))

    r, g, b = int(stage_color[1:3], 16), int(stage_color[3:5], 16), int(stage_color[5:7], 16)
    fill_color = f"rgba({r},{g},{b},0.10)"

    rng = np.random.default_rng(seed=abs(hash(ticker)) % (2**31))
    volumes = (rng.integers(500_000, 5_000_000, n)).tolist()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=xs, y=volumes,
        marker_color="#1a2e1a",
        opacity=0.5,
        name="Volume",
        yaxis="y2",
        hovertemplate="%{y:,.0f}<extra>Volume</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=xs, y=prices,
        mode="lines",
        line=dict(color=stage_color, width=2),
        fill="tozeroy",
        fillcolor=fill_color,
        name="Price",
        hovertemplate="$%{y:.2f}<extra>Price</extra>",
    ))

    fig.add_hline(y=prices[0], line_dash="dot", line_color="#2a5e2a", line_width=1)

    fig.update_layout(
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        margin=dict(l=10, r=10, t=36, b=10),
        height=300,
        xaxis=dict(
            tickfont=dict(size=8, color="#4a4e6a", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
            showticklabels=False,
        ),
        yaxis=dict(
            tickfont=dict(size=9, color="#8b8fa8", family="IBM Plex Mono"),
            gridcolor="#1a1d27",
            tickprefix="$",
        ),
        yaxis2=dict(
            overlaying="y", side="right", showgrid=False,
            tickfont=dict(size=7, color="#2a2d3e", family="IBM Plex Mono"),
        ),
        title=dict(
            text=f"{ticker} — 30-Day Price" + (" (TEST DATA)" if test_mode else ""),
            font=dict(size=10, color="#8b8fa8", family="IBM Plex Mono"),
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
    stage_color = STAGE_COLORS.get(stage, "#4D9FFF")
    css_key = STAGE_CSS_KEYS.get(stage, "compute")

    # ── Hero banner ───────────────────────────────────────────────────────────
    st.markdown(
        f"<div class='stage-img-card si-{css_key}' "
        f"style='min-height:100px;padding:20px 24px;margin-bottom:16px;"
        f"border-left:4px solid {stage_color};'>"
        f"<div style='font-size:0.68rem;color:rgba(255,255,255,0.5);"
        f"font-family:IBM Plex Mono,monospace;letter-spacing:0.1em;text-transform:uppercase;"
        f"margin-bottom:4px;'>Deep Dive</div>"
        f"<div style='font-size:1.8rem;font-weight:700;color:#ffffff;"
        f"font-family:DM Sans,sans-serif;'>{ticker}</div>"
        f"<div style='font-size:0.8rem;color:{stage_color};font-weight:600;"
        f"font-family:DM Sans,sans-serif;'>{stage}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

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
        (m1, "Price",     f"${price:.2f}",   "#c8d8c0"),
        (m2, "1D Change", fmt_chg(chg_1d),   chg_color(chg_1d)),
        (m3, "5D Change", fmt_chg(chg_5d),   chg_color(chg_5d)),
        (m4, "1M Change", fmt_chg(chg_1m),   chg_color(chg_1m)),
        (m5, "Market Cap", mcap,              "#7a9e7a"),
    ]
    for col, label, val, color in metrics:
        with col:
            st.markdown(
                f"<div style='background:#1a1d27;border:1px solid #2a2d3e;border-radius:10px;"
                f"padding:12px 14px;text-align:center;"
                f"border-top:3px solid {stage_color};box-shadow:0 2px 8px rgba(0,0,0,0.2);'>"
                f"<div style='font-size:0.78rem;color:#9da3b4;text-transform:uppercase;"
                f"letter-spacing:0.08em;font-family:IBM Plex Mono,monospace;'>{label}</div>"
                f"<div style='font-size:1.4rem;font-weight:700;color:{color};margin-top:5px;"
                f"font-family:IBM Plex Mono,monospace;'>{val}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Price chart ──────────────────────────────────────────────────────────
    fig = _price_chart(ticker, spark, stage_color, test_mode)
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

    # ═══════════════════════════════════════════════════════════════════════════
    # FUNDAMENTALS
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:0.7rem;color:{stage_color};text-transform:uppercase;"
        f"letter-spacing:0.12em;font-family:IBM Plex Mono,monospace;"
        f"font-weight:700;border-bottom:1px solid #2a2d3e;padding-bottom:8px;"
        f"margin-bottom:16px;'>Fundamentals"
        f"{'  ·  TEST DATA' if test_mode else ''}</div>",
        unsafe_allow_html=True,
    )

    # Company summary — full width
    _render_company_summary(ticker, stage_color, test_mode)

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # Income statement + Balance sheet side by side
    col_inc, col_bs = st.columns(2)
    with col_inc:
        _render_income_stmt(ticker, stage_color, test_mode)
    with col_bs:
        _render_balance_sheet(ticker, stage_color, test_mode)

    if test_mode:
        st.markdown(
            "<div style='margin-top:1rem; font-size:0.65rem; color:#3a4e3a;"
            " border:1px solid #1a2e1a; border-radius:4px; padding:6px 10px;'>"
            "🧪 TEST MODE — chart and fundamentals data are synthetically generated."
            "</div>",
            unsafe_allow_html=True,
        )

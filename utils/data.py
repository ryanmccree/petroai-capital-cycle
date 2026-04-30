"""
utils/data.py
Handles all price data fetching.
- When TEST_MODE=True: returns hardcoded dummy data, no network calls.
- When TEST_MODE=False: fetches from yfinance with full error handling + cache.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ── Dummy data for TEST_MODE ───────────────────────────────────────────────────

DUMMY_QUOTES = {
    "OKLO":  {"price": 18.42,  "chg_1d": +8.3,  "chg_5d": +15.2, "chg_1m": +42.1, "mcap": "2.1B"},
    "CEG":   {"price": 243.10, "chg_1d": +2.1,  "chg_5d": +4.8,  "chg_1m": +11.3, "mcap": "76.4B"},
    "ETN":   {"price": 299.85, "chg_1d": +1.4,  "chg_5d": +3.2,  "chg_1m": +8.7,  "mcap": "119.2B"},
    "VST":   {"price": 185.30, "chg_1d": +3.2,  "chg_5d": +6.1,  "chg_1m": +18.4, "mcap": "44.8B"},
    "NRG":   {"price": 112.40, "chg_1d": +1.8,  "chg_5d": +2.9,  "chg_1m": +6.2,  "mcap": "33.1B"},
    "ANET":  {"price": 322.15, "chg_1d": +2.7,  "chg_5d": +5.4,  "chg_1m": +14.9, "mcap": "101.3B"},
    "NVDA":  {"price": 875.40, "chg_1d": +3.1,  "chg_5d": +7.8,  "chg_1m": +22.3, "mcap": "2.16T"},
    "NVTS":  {"price": 4.82,   "chg_1d": +5.4,  "chg_5d": +11.2, "chg_1m": +28.6, "mcap": "1.2B"},
    "MU":    {"price": 132.60, "chg_1d": +1.9,  "chg_5d": +4.1,  "chg_1m": +9.8,  "mcap": "147.8B"},
    "COHR":  {"price": 82.30,  "chg_1d": +4.2,  "chg_5d": +9.8,  "chg_1m": +31.4, "mcap": "11.2B"},
    "RGTI":  {"price": 9.14,   "chg_1d": +12.3, "chg_5d": +24.1, "chg_1m": +67.8, "mcap": "1.4B"},
    "IONQ":  {"price": 28.45,  "chg_1d": +6.8,  "chg_5d": +14.3, "chg_1m": +45.2, "mcap": "5.8B"},
    "QBTS":  {"price": 5.37,   "chg_1d": +9.1,  "chg_5d": +18.7, "chg_1m": +52.3, "mcap": "0.9B"},
    "PLTR":  {"price": 24.85,  "chg_1d": +4.2,  "chg_5d": +8.9,  "chg_1m": +19.7, "mcap": "52.3B"},
    "MP":    {"price": 19.20,  "chg_1d": +5.8,  "chg_5d": +12.4, "chg_1m": +34.1, "mcap": "3.7B"},
    "CRML":  {"price": 7.45,   "chg_1d": +8.1,  "chg_5d": +16.3, "chg_1m": +48.9, "mcap": "0.6B"},
    "INTC":  {"price": 21.30,  "chg_1d": -1.4,  "chg_5d": -2.8,  "chg_1m": -8.3,  "mcap": "90.1B"},
    "CIFR":  {"price": 4.18,   "chg_1d": +3.6,  "chg_5d": +7.2,  "chg_1m": +21.8, "mcap": "0.4B"},
    "CRWV":  {"price": 61.20,  "chg_1d": +2.8,  "chg_5d": +5.9,  "chg_1m": +16.4, "mcap": "14.2B"},
}


def _generate_dummy_sparkline(ticker: str, days: int = 30) -> pd.Series:
    """Generate a reproducible fake price series for sparklines."""
    rng = np.random.default_rng(seed=abs(hash(ticker)) % (2**31))
    base = DUMMY_QUOTES.get(ticker, {}).get("price", 100)
    returns = rng.normal(0.001, 0.025, days)
    prices = base * np.cumprod(1 + returns)
    return pd.Series(prices)


def get_quote(ticker: str, test_mode: bool) -> dict:
    """
    Return quote dict: {price, chg_1d, chg_5d, chg_1m, mcap}.
    Falls back to dummy data on any error.
    """
    ticker = ticker.upper()

    if test_mode:
        return DUMMY_QUOTES.get(ticker, {
            "price": 0.0, "chg_1d": 0.0, "chg_5d": 0.0,
            "chg_1m": 0.0, "mcap": "N/A"
        })

    # Live path
    if ticker in st.session_state.get("price_cache", {}):
        return st.session_state.price_cache[ticker]

    try:
        import yfinance as yf
        info = yf.Ticker(ticker).fast_info
        hist = yf.Ticker(ticker).history(period="1mo")
        if hist.empty:
            raise ValueError("No data returned")

        price = float(hist["Close"].iloc[-1])
        chg_1d = float((hist["Close"].iloc[-1] / hist["Close"].iloc[-2] - 1) * 100) if len(hist) >= 2 else 0.0
        chg_5d = float((hist["Close"].iloc[-1] / hist["Close"].iloc[-6] - 1) * 100) if len(hist) >= 6 else 0.0
        chg_1m = float((hist["Close"].iloc[-1] / hist["Close"].iloc[0]  - 1) * 100)

        mcap_raw = getattr(info, "market_cap", None)
        if mcap_raw and mcap_raw >= 1e12:
            mcap = f"{mcap_raw/1e12:.1f}T"
        elif mcap_raw and mcap_raw >= 1e9:
            mcap = f"{mcap_raw/1e9:.1f}B"
        elif mcap_raw:
            mcap = f"{mcap_raw/1e6:.0f}M"
        else:
            mcap = "N/A"

        result = {"price": price, "chg_1d": chg_1d, "chg_5d": chg_5d, "chg_1m": chg_1m, "mcap": mcap}
        if "price_cache" not in st.session_state:
            st.session_state.price_cache = {}
        st.session_state.price_cache[ticker] = result
        return result

    except Exception as e:
        st.warning(f"⚠️ Could not fetch {ticker}: {e}. Using cached/dummy data.")
        return DUMMY_QUOTES.get(ticker, {
            "price": 0.0, "chg_1d": 0.0, "chg_5d": 0.0,
            "chg_1m": 0.0, "mcap": "N/A"
        })


def get_sparkline(ticker: str, test_mode: bool, days: int = 30) -> pd.Series:
    """Return a Series of closing prices for a mini sparkline chart."""
    if test_mode:
        return _generate_dummy_sparkline(ticker, days)

    try:
        import yfinance as yf
        hist = yf.Ticker(ticker).history(period=f"{days}d")
        if hist.empty:
            raise ValueError("empty")
        return hist["Close"].reset_index(drop=True)
    except Exception:
        return _generate_dummy_sparkline(ticker, days)

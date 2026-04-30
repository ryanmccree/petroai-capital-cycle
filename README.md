# PetroAI Capital Cycle Dashboard

> Monitors @mikalche's PetroAI Capital Cycle Thesis
> Energy → Power → Grid → Compute → Transfer → AI → Defense → Sovereignty

## Project Structure

```
petroai/
├── app.py                  ← Main entry point (routing, session state, layout)
├── requirements.txt
├── utils/
│   ├── state.py            ← Session state init + default data
│   ├── theme.py            ← Dark-mode CSS injection
│   └── data.py             ← Price fetching (TEST_MODE bypass + yfinance)
└── tabs/
    ├── cycle_viz.py        ← Tab 1: Cycle flow diagram (Step 1) ✅
    ├── portfolio.py        ← Tab 2: Portfolio manager (Step 2)
    ├── constraints.py      ← Tab 3: Constraint tracker (Step 3)
    ├── deep_dive.py        ← Tab 4: Company deep dive (Step 4)
    └── market_overview.py  ← Tab 5: Market overview (Step 5)
```

## Quick Start (Local)

pip install -r requirements.txt
streamlit run app.py

## Test Mode

At the top of app.py:
  TEST_MODE = True   <- uses hardcoded dummy data, no yfinance calls
  TEST_MODE = False  <- live yfinance data with error handling

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to share.streamlit.io
3. New app -> select repo -> set app.py as the main file
4. No additional OS-level dependencies required

Not financial advice.

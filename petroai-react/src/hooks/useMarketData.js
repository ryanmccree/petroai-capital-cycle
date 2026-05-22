import { useState, useEffect, useCallback } from 'react';
import { HOLDINGS, TICKER as STATIC_TICKER, HEATMAP } from '../data/staticData';

// Parse a day-change string like "+3.4%" → 3.4
function parseChg(str) {
  return parseFloat(String(str).replace('%', '')) || 0;
}

// Format a numeric change → "+3.42%"
function fmtChg(n) {
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

// Fetch quotes from our Vercel API route (/api/quote).
// Falls back to direct Yahoo Finance if the route isn't available (local dev).
async function fetchQuotes(tickers) {
  // Try the API route first (works in production on Vercel)
  try {
    const res = await fetch(`/api/quote?tickers=${tickers.join(',')}`);
    if (res.ok) return await res.json();
  } catch {
    // API route not available — likely running `vite dev` without the API
  }

  // Fallback: attempt direct Yahoo Finance (may hit CORS in some browsers)
  const results = {};
  await Promise.allSettled(
    tickers.map(async (ticker) => {
      try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=5d`;
        const r = await fetch(url);
        if (!r.ok) return;
        const data = await r.json();
        const meta = data.chart?.result?.[0]?.meta;
        if (!meta) return;
        const price = meta.regularMarketPrice;
        const prev  = meta.regularMarketPreviousClose ?? meta.previousClose;
        const chg1d = prev ? ((price - prev) / prev) * 100 : 0;
        const closes = (data.chart?.result?.[0]?.indicators?.quote?.[0]?.close ?? []).filter(Boolean);
        const chg5d  = closes.length >= 2
          ? ((closes.at(-1) - closes[0]) / closes[0]) * 100
          : chg1d;
        results[ticker] = { ticker, price, chg1d, chg5d };
      } catch {
        // Silently fall back to static data for this ticker
      }
    })
  );
  return Object.keys(results).length ? results : null;
}

export function useMarketData() {
  const [holdings, setHoldings]   = useState(HOLDINGS);
  const [tickerTape, setTicker]   = useState(STATIC_TICKER);
  const [heatmap, setHeatmap]     = useState(HEATMAP);
  const [loading, setLoading]     = useState(true);
  const [lastUpdated, setUpdated] = useState(null);

  const refresh = useCallback(async () => {
    const tickers = [...new Set(HOLDINGS.map(h => h.ticker))];
    const data    = await fetchQuotes(tickers);

    if (!data) {
      setLoading(false);
      return;
    }

    // Merge live prices into holdings
    setHoldings(
      HOLDINGS.map(h => {
        const q = data[h.ticker];
        if (!q || q.error) return h;
        return {
          ...h,
          price: q.price ?? h.price,
          day:   fmtChg(q.chg1d ?? parseChg(h.day)),
        };
      })
    );

    // Merge live changes into heatmap cells
    setHeatmap(
      HEATMAP.map(cell => {
        const q = data[cell.sym];
        if (!q || q.error) return cell;
        return { ...cell, ch: q.chg1d ?? cell.ch };
      })
    );

    // Merge live prices into ticker tape
    setTicker(
      STATIC_TICKER.map(item => {
        const q = data[item[0]];
        if (!q || q.error) return item;
        return [
          item[0],
          q.price.toFixed(2),
          q.chg1d >= 0 ? 'up' : 'down',
          fmtChg(q.chg1d),
        ];
      })
    );

    setLoading(false);
    setUpdated(new Date());
  }, []);

  useEffect(() => {
    refresh();
    // Re-fetch every 5 minutes
    const id = setInterval(refresh, 5 * 60 * 1000);
    return () => clearInterval(id);
  }, [refresh]);

  return { holdings, tickerTape, heatmap, loading, lastUpdated };
}

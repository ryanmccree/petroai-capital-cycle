// Vercel serverless function — proxies Yahoo Finance to avoid browser CORS
export default async function handler(req, res) {
  const { tickers } = req.query;
  if (!tickers) return res.status(400).json({ error: 'tickers param required' });

  const list = tickers.split(',').map(t => t.trim().toUpperCase()).filter(Boolean);

  const results = {};
  await Promise.allSettled(
    list.map(async (ticker) => {
      try {
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?interval=1d&range=5d`;
        const r = await fetch(url, {
          headers: { 'User-Agent': 'Mozilla/5.0' },
        });
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
        results[ticker] = { ticker, error: true };
      }
    })
  );

  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');
  res.status(200).json(results);
}

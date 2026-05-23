import { useState } from 'react';
import Header from './components/Header.jsx';
import CycleTab from './components/CycleTab.jsx';
import PortfolioTab from './components/PortfolioTab.jsx';
import MarketTab from './components/MarketTab.jsx';
import ThesisTab from './components/ThesisTab.jsx';
import FlowsTab from './components/FlowsTab.jsx';
import ScreenerTab from './components/ScreenerTab.jsx';
import AboutTab from './components/AboutTab.jsx';
import { useMarketData } from './hooks/useMarketData.js';

const SCREEN_LABELS = {
  cycle:     '01 Cycle Visualization',
  portfolio: '02 Portfolio',
  market:    '03 Market Overview',
  thesis:    '04 Thesis Tracker',
  flows:     '05 Capital Flows',
  screen:    '06 Screener',
  about:     '07 About',
};

export default function App() {
  const [tab, setTab] = useState('cycle');
  const { holdings, tickerTape, heatmap, loading, lastUpdated } = useMarketData();

  return (
    <div className="app">
      <Header tab={tab} setTab={setTab} tickerTape={tickerTape} />
      <main className="main" data-screen-label={SCREEN_LABELS[tab]}>
        {tab === 'cycle'     && <CycleTab holdings={holdings} />}
        {tab === 'portfolio' && <PortfolioTab holdings={holdings} loading={loading} />}
        {tab === 'market'    && <MarketTab heatmap={heatmap} holdings={holdings} />}
        {tab === 'thesis'    && <ThesisTab />}
        {tab === 'flows'     && <FlowsTab />}
        {tab === 'screen'    && <ScreenerTab holdings={holdings} />}
        {tab === 'about'     && <AboutTab />}
      </main>

      <div className="footer-bar">
        <div className="grp">
          <span><span className="dot-pos" style={{ display: 'inline-block', marginRight: 6 }}></span>Engine v4.2.1 · React + Vite · Vercel</span>
        </div>
        <div className="grp">
          {lastUpdated && <span>Updated {lastUpdated.toLocaleTimeString()}</span>}
          <span>
            Thesis by{' '}
            <a
              href="https://x.com/mikalche"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#f59e0b', textDecoration: 'none' }}
              onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
              onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}
            >@mikalche</a>{' '}
            on X · Built by Ryan M. · Not financial advice
          </span>
        </div>
      </div>
    </div>
  );
}

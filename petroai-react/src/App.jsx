import { useState } from 'react';
import Header from './components/Header.jsx';
import CycleTab from './components/CycleTab.jsx';
import PortfolioTab from './components/PortfolioTab.jsx';
import MarketTab from './components/MarketTab.jsx';
import ThesisTab from './components/ThesisTab.jsx';
import FlowsTab from './components/FlowsTab.jsx';
import ScreenerTab from './components/ScreenerTab.jsx';
import { useMarketData } from './hooks/useMarketData.js';

const SCREEN_LABELS = {
  cycle:     '01 Cycle Visualization',
  portfolio: '02 Portfolio',
  market:    '03 Market Overview',
  thesis:    '04 Thesis Tracker',
  flows:     '05 Capital Flows',
  screen:    '06 Screener',
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
      </main>

      <div className="footer-bar">
        <div className="grp">
          <span><span className="dot-pos" style={{ display: 'inline-block', marginRight: 6 }}></span>Stream · NYSE/NASDAQ · IEX</span>
          <span>Latency 42ms</span>
          <span>Quote feed · L2</span>
        </div>
        <div className="grp">
          <span>Engine v4.2.1</span>
          {lastUpdated && <span>Updated {lastUpdated.toLocaleTimeString()}</span>}
          <span>© PetroAI Research</span>
        </div>
      </div>
    </div>
  );
}

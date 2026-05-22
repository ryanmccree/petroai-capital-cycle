import { useState, useEffect } from 'react';

const TABS = [
  { id: 'cycle',     num: '01', label: 'Cycle Visualization' },
  { id: 'portfolio', num: '02', label: 'Portfolio' },
  { id: 'market',    num: '03', label: 'Market Overview' },
  { id: 'thesis',    num: '04', label: 'Thesis Tracker',  disabled: true },
  { id: 'flows',     num: '05', label: 'Capital Flows',   disabled: true },
  { id: 'screen',    num: '06', label: 'Screener',        disabled: true },
];

export default function Header({ tab, setTab, tickerTape }) {
  const [time, setTime] = useState(() => new Date());

  useEffect(() => {
    const i = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(i);
  }, []);

  const utc = time.toUTCString().slice(17, 25);

  return (
    <>
      <div className="topbar">
        <div className="brand">
          <div className="brand-mark"></div>
          <div>
            <div className="brand-name">
              PetroAI <span style={{ color: 'var(--text-3)', fontWeight: 400 }}>// Capital Cycle</span>
            </div>
            <div className="brand-sub">Institutional · v4.2.1 · Energy → Sovereignty</div>
          </div>
          <div style={{ width: 1, height: 28, background: 'var(--line)', marginLeft: 8 }}></div>
          <span className="status-pill">
            <span className="status-dot"></span>Markets Open
          </span>
        </div>

        <div className="ticker">
          <div className="ticker-track">
            {[...tickerTape, ...tickerTape].map((it, i) => (
              <span className="ticker-item" key={i}>
                <span className="sym">{it[0]}</span>
                <span className="px">{it[1]}</span>
                <span className={it[2]}>{it[3]}</span>
              </span>
            ))}
          </div>
        </div>

        <div className="user-cluster">
          <span className="clock">{utc} UTC</span>
          <button className="iconbtn" title="Search">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="7"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
          </button>
          <button className="iconbtn" title="Alerts">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
              <path d="M10 21a2 2 0 0 0 4 0"/>
            </svg>
          </button>
          <div className="avatar">RV</div>
        </div>
      </div>

      <nav className="tabs">
        {TABS.map(t => (
          <button
            key={t.id}
            className={'tab' + (tab === t.id ? ' active' : '')}
            onClick={() => !t.disabled && setTab(t.id)}
            disabled={t.disabled}
            style={t.disabled ? { opacity: 0.45, cursor: 'not-allowed' } : {}}
          >
            <span className="num">{t.num}</span> {t.label}
          </button>
        ))}
        <div className="tab-spacer"></div>
        <div className="tab-meta">
          <span>NAV <span style={{ color: 'var(--text)' }}>$2.284B</span></span>
          <span className="sep"></span>
          <span>Δ Today <span className="up">+1.31%</span></span>
          <span className="sep"></span>
          <span>YTD <span className="up">+18.42%</span></span>
        </div>
      </nav>
    </>
  );
}

import { useState } from 'react';
import { STAGES } from '../data/staticData.js';

function bgFor(kind, color) {
  const c = color;
  const dim = '#0d1117';
  const patterns = {
    oil: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.55'>
          ${Array.from({ length: 14 }).map((_, i) => `<line x1='${i * 24}' y1='0' x2='${i * 24 - 80}' y2='240' stroke='${c}' stroke-width='0.6' opacity='${0.15 + (i % 3) * 0.08}'/>`).join('')}
        </g>
        <circle cx='220' cy='80' r='90' fill='${c}' opacity='0.12'/>
        <circle cx='80' cy='200' r='60' fill='${c}' opacity='0.08'/>
      </svg>`,
    uranium: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.6'>
          ${Array.from({ length: 10 }).map((_, i) => `<circle cx='${160 + (i % 2 ? 1 : -1) * i * 18}' cy='120' r='${10 + i * 8}' fill='none' stroke='${c}' stroke-width='0.5' opacity='${0.5 - i * 0.04}'/>`).join('')}
        </g>
        <circle cx='160' cy='120' r='6' fill='${c}'/>
      </svg>`,
    reactor: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.5'>
          ${Array.from({ length: 8 }).map((_, i) => `<rect x='${20 + i * 38}' y='${60 + (i % 2) * 40}' width='28' height='${100 - (i % 3) * 20}' fill='none' stroke='${c}' stroke-width='0.6'/>`).join('')}
        </g>
        <line x1='0' y1='190' x2='320' y2='190' stroke='${c}' stroke-width='0.8' opacity='0.5'/>
      </svg>`,
    grid: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.45' stroke='${c}' stroke-width='0.5' fill='none'>
          ${Array.from({ length: 14 }).map((_, i) => `<line x1='${i * 24}' y1='0' x2='${i * 24}' y2='240'/>`).join('')}
          ${Array.from({ length: 10 }).map((_, i) => `<line x1='0' y1='${i * 24}' x2='320' y2='${i * 24}'/>`).join('')}
        </g>
        <g fill='${c}'>
          <circle cx='72' cy='72' r='3'/><circle cx='168' cy='120' r='3'/><circle cx='240' cy='168' r='3'/><circle cx='96' cy='192' r='3'/>
        </g>
        <g stroke='${c}' stroke-width='1' opacity='0.7' fill='none'>
          <path d='M72 72 L168 120 L240 168 M168 120 L96 192'/>
        </g>
      </svg>`,
    chip: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <rect x='80' y='50' width='160' height='140' fill='none' stroke='${c}' stroke-width='0.8' opacity='0.6'/>
        <rect x='100' y='70' width='120' height='100' fill='none' stroke='${c}' stroke-width='0.6' opacity='0.5'/>
        <g opacity='0.5' stroke='${c}' stroke-width='0.5'>
          ${Array.from({ length: 14 }).map((_, i) => `<line x1='${80 + i * 12}' y1='40' x2='${80 + i * 12}' y2='50'/><line x1='${80 + i * 12}' y1='190' x2='${80 + i * 12}' y2='200'/>`).join('')}
          ${Array.from({ length: 12 }).map((_, i) => `<line x1='70' y1='${50 + i * 12}' x2='80' y2='${50 + i * 12}'/><line x1='240' y1='${50 + i * 12}' x2='250' y2='${50 + i * 12}'/>`).join('')}
        </g>
      </svg>`,
    datacenter: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.5'>
          ${Array.from({ length: 6 }).map((_, r) => Array.from({ length: 16 }).map((_, i) => `<rect x='${i * 20 + 2}' y='${40 + r * 30}' width='16' height='4' fill='${c}' opacity='${0.2 + (i % 4) * 0.15}'/>`).join('')).join('')}
        </g>
      </svg>`,
    ai: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <defs>
          <radialGradient id='ai-glow-${c.slice(1)}' cx='50%' cy='50%' r='50%'>
            <stop offset='0%' stop-color='${c}' stop-opacity='0.4'/>
            <stop offset='100%' stop-color='${c}' stop-opacity='0'/>
          </radialGradient>
        </defs>
        <circle cx='160' cy='120' r='100' fill='url(#ai-glow-${c.slice(1)})'/>
        <g stroke='${c}' stroke-width='0.5' opacity='0.5'>
          ${Array.from({ length: 24 }).map((_, i) => { const a = i * Math.PI * 2 / 24; const x1 = 160 + Math.cos(a) * 30; const y1 = 120 + Math.sin(a) * 30; const x2 = 160 + Math.cos(a) * 90; const y2 = 120 + Math.sin(a) * 90; return `<line x1='${x1.toFixed(1)}' y1='${y1.toFixed(1)}' x2='${x2.toFixed(1)}' y2='${y2.toFixed(1)}'/>`;}).join('')}
        </g>
        <circle cx='160' cy='120' r='20' fill='${c}' opacity='0.3'/>
        <circle cx='160' cy='120' r='6' fill='${c}'/>
      </svg>`,
    defense: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g stroke='${c}' stroke-width='0.5' fill='none' opacity='0.5'>
          ${Array.from({ length: 6 }).map((_, i) => `<polygon points='160,${20 + i * 20} ${260 - i * 15},120 160,${220 - i * 20} ${60 + i * 15},120' opacity='${0.6 - i * 0.08}'/>`).join('')}
        </g>
        <circle cx='160' cy='120' r='4' fill='${c}'/>
      </svg>`,
    metals: `
      <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 240' preserveAspectRatio='xMidYMid slice'>
        <rect width='320' height='240' fill='${dim}'/>
        <g opacity='0.55'>
          ${Array.from({ length: 9 }).map((_, i) => { const x = 40 + i * 32; const h = 60 + ((i * 37) % 80); return `<rect x='${x}' y='${240 - h}' width='20' height='${h}' fill='${c}' opacity='${0.18 + (i % 3) * 0.12}'/>`;}).join('')}
        </g>
      </svg>`,
  };
  const svg = patterns[kind] || patterns.grid;
  return `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
}

function PortfolioCard({ h }) {
  const stage = STAGES.find(s => s.id === h.stage);
  const isUp = parseFloat(h.day) >= 0;
  return (
    <div className="pcard" style={{ '--stage-color': stage.color }}>
      <div className="pcard-bg" style={{ backgroundImage: bgFor(h.img, stage.color) }}></div>
      <span className="pcard-stage">{stage.name}</span>
      <span className={'pcard-pct ' + (isUp ? 'up' : 'down')}>{h.day}</span>
      <div className="pcard-body">
        <div className="pcard-ticker">{h.ticker} · {h.mcap}</div>
        <div className="pcard-name">{h.name}</div>
        <div className="pcard-stats">
          <div><div className="k">Last</div><div className="v">${h.price.toFixed(2)}</div></div>
          <div><div className="k">Weight</div><div className="v">{h.wgt}</div></div>
          <div><div className="k">Cost</div><div className="v dim">${h.cost.toFixed(2)}</div></div>
        </div>
      </div>
    </div>
  );
}

export default function PortfolioTab({ holdings, loading }) {
  const [filter, setFilter] = useState('all');
  const filtered = filter === 'all' ? holdings : holdings.filter(h => h.stage === filter);

  return (
    <div>
      <div className="kpi-row">
        <div className="kpi" style={{ '--stage-color': '#22d3ee' }}>
          <div className="k">Net Asset Value</div>
          <div className="v">$2,284.4M</div>
          <div className="sub"><span className="up">+$29.6M</span><span className="dim">vs prior close</span></div>
        </div>
        <div className="kpi" style={{ '--stage-color': '#4ade80' }}>
          <div className="k">Daily Return</div>
          <div className="v up">+1.31%</div>
          <div className="sub"><span className="dim">σ 30d</span><span style={{ color: 'var(--text)' }}>14.2%</span></div>
        </div>
        <div className="kpi" style={{ '--stage-color': '#a855f7' }}>
          <div className="k">YTD Performance</div>
          <div className="v up">+18.42%</div>
          <div className="sub"><span className="dim">vs SPX</span><span className="up">+8.84%</span></div>
        </div>
        <div className="kpi" style={{ '--stage-color': '#e76f1c' }}>
          <div className="k">Cycle Beta</div>
          <div className="v">1.28</div>
          <div className="sub"><span className="dim">Sharpe</span><span style={{ color: 'var(--text)' }}>2.14</span></div>
        </div>
      </div>

      <div className="portfolio-toolbar">
        <div className="pill-group">
          <button className={'pill' + (filter === 'all' ? ' active' : '')} onClick={() => setFilter('all')}>
            All · {holdings.length}
          </button>
          {STAGES.map(s => (
            <button
              key={s.id}
              className={'pill' + (filter === s.id ? ' active' : '')}
              onClick={() => setFilter(s.id)}
              style={filter === s.id ? { boxShadow: `inset 0 -2px 0 ${s.color}` } : {}}
            >
              {s.name}
            </button>
          ))}
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <div className="search-input">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="7"/>
              <path d="m21 21-4.3-4.3"/>
            </svg>
            <span>Search ticker, name, theme…</span>
            <span className="kbd">⌘ K</span>
          </div>
          <div className="pill-group">
            <button className="pill active">Cards</button>
            <button className="pill">Table</button>
          </div>
        </div>
      </div>

      {loading && (
        <div style={{ textAlign: 'center', padding: '20px', fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-3)', letterSpacing: '0.1em' }}>
          LOADING LIVE DATA…
        </div>
      )}

      <div className="portfolio-grid">
        {filtered.map(h => <PortfolioCard key={h.ticker} h={h} />)}
      </div>
    </div>
  );
}

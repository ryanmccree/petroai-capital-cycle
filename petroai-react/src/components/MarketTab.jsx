import { STAGES, INDICES, SIGNALS, NEWS, FLOWS } from '../data/staticData.js';

function genSeries(seed, n = 30, vol = 0.04) {
  let v = 100, s = seed;
  const out = [];
  for (let i = 0; i < n; i++) {
    s = (s * 9301 + 49297) % 233280;
    v *= 1 + ((s / 233280) - 0.5) * vol;
    out.push(v);
  }
  return out;
}

function Sparkline({ color, data, height = 28 }) {
  const w = 120;
  const min = Math.min(...data), max = Math.max(...data);
  const norm = data.map((d, i) => [
    (i / (data.length - 1)) * w,
    height - ((d - min) / (max - min || 1)) * (height - 4) - 2,
  ]);
  const path = norm.map(([x, y], i) => (i === 0 ? `M${x},${y}` : `L${x},${y}`)).join(' ');
  const area = path + ` L${w},${height} L0,${height} Z`;
  const id = `sg-${color.slice(1)}`;
  return (
    <svg width="100%" height={height} viewBox={`0 0 ${w} ${height}`} preserveAspectRatio="none">
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%"   stopColor={color} stopOpacity="0.35"/>
          <stop offset="100%" stopColor={color} stopOpacity="0"/>
        </linearGradient>
      </defs>
      <path d={area} fill={`url(#${id})`} />
      <path d={path} stroke={color} strokeWidth="1.4" fill="none"/>
    </svg>
  );
}

function HeatmapCell({ h }) {
  const stage = STAGES.find(s => s.id === h.stage);
  const intensity = Math.min(Math.abs(h.ch) / 5, 1);
  const c = h.ch >= 0 ? stage.color : '#ef4444';
  const hex = n => Math.round(n).toString(16).padStart(2, '0');
  const bg = `linear-gradient(135deg, ${c}${hex(intensity * 60)} 0%, ${c}${hex(intensity * 20)} 100%)`;
  return (
    <div className="heat-cell" style={{ background: bg, borderLeft: `2px solid ${c}` }}>
      <div className="t">{h.sym}</div>
      <div className="c">{h.ch >= 0 ? '+' : ''}{h.ch.toFixed(1)}%</div>
    </div>
  );
}

export default function MarketTab({ heatmap, holdings }) {
  const sorted = [...holdings].sort((a, b) => parseFloat(b.day) - parseFloat(a.day));

  return (
    <div>
      {/* Index strip */}
      <div className="index-strip">
        {INDICES.map((ix, i) => {
          const c = ix.dir === 'up' ? '#4ade80' : '#f87171';
          const data = genSeries(i * 11 + 3, 30, 0.025);
          return (
            <div className="idx" key={ix.nm}>
              <div className="nm">{ix.nm}</div>
              <div className="px">{ix.px}</div>
              <div className="ch">
                <span className={ix.dir}>{ix.ch}</span>
                <span className={ix.dir}>{ix.pct}</span>
              </div>
              <div className="sparkbox"><Sparkline color={c} data={data} /></div>
            </div>
          );
        })}
      </div>

      <div className="market-grid">
        {/* LEFT column */}
        <div>
          <div className="panel" style={{ marginBottom: 12 }}>
            <div className="panel-head">
              <span className="panel-title">Cycle Heatmap · Intraday</span>
              <span className="panel-actions">
                <span className="chip">1D</span>
                <span className="chip live">LIVE</span>
              </span>
            </div>
            <div className="heatmap">
              {heatmap.map(h => <HeatmapCell key={h.sym} h={h} />)}
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', borderTop: '1px solid var(--line)', fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
              <span>Color = stage · Intensity = move</span>
              <span style={{ display: 'flex', gap: 12 }}>
                {STAGES.map(s => (
                  <span key={s.id} style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                    <span style={{ width: 8, height: 8, background: s.color, borderRadius: 1 }}></span>{s.name}
                  </span>
                ))}
              </span>
            </div>
          </div>

          <div className="panel">
            <div className="panel-head">
              <span className="panel-title">Capital Flow · Cross-Stage Rotation</span>
              <span className="panel-actions"><span className="chip">5D</span></span>
            </div>
            <div className="flow-vis">
              {FLOWS.map(f => {
                const stage = STAGES.find(s => s.id === f.stage);
                return (
                  <div className="flow-row" key={f.stage} style={{ '--stage-color': stage.color }}>
                    <div className="lab">{f.lbl}</div>
                    <div className="bar-track">
                      <div className="bar" style={{ width: f.flow + '%' }}></div>
                    </div>
                    <div className="num">{f.flow}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* RIGHT column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <div className="panel">
            <div className="panel-head">
              <span className="panel-title">Top Movers</span>
              <span className="panel-actions">
                <span className="chip">Gainers</span>
                <span className="chip" style={{ opacity: 0.5 }}>Losers</span>
              </span>
            </div>
            <div className="movers-list">
              {sorted.slice(0, 7).map(h => {
                const stage = STAGES.find(s => s.id === h.stage);
                const isUp = parseFloat(h.day) >= 0;
                return (
                  <div className="mover-row" key={h.ticker} style={{ '--stage-color': stage.color }}>
                    <span className="stage-bar"></span>
                    <div>
                      <div className="sym">{h.ticker}</div>
                      <div className="nm">{h.name}</div>
                    </div>
                    <span className="px">${h.price.toFixed(2)}</span>
                    <span className={'ch ' + (isUp ? 'up' : 'down')}>{h.day}</span>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="panel">
            <div className="panel-head">
              <span className="panel-title">Cycle Signals</span>
              <span className="panel-actions"><span className="chip live">REAL-TIME</span></span>
            </div>
            <div className="signal-list">
              {SIGNALS.map(sig => {
                const stage = STAGES.find(s => s.id === sig.stage);
                return (
                  <div className="signal-row" key={sig.lbl} style={{ '--stage-color': stage.color }}>
                    <div className="lhs">
                      <span className="dot"></span>
                      <div className="lbl">{sig.lbl}<small>{sig.sub}</small></div>
                    </div>
                    <span className="val">{sig.val}</span>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="panel">
            <div className="panel-head">
              <span className="panel-title">Cycle Newsflow</span>
              <span className="panel-actions"><span className="chip">All Stages</span></span>
            </div>
            <div className="news-list">
              {NEWS.map((n, i) => {
                const stage = STAGES.find(s => s.id === n.src);
                return (
                  <div className="news-row" key={i} style={{ '--stage-color': stage.color }}>
                    <span className="time">{n.time}</span>
                    <div>
                      <span className="src">{stage.name}</span>
                      <div className="hl">{n.hl}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

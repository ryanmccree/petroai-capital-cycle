import { useState } from 'react';
import { STAGES } from '../data/staticData.js';

const CATALYSTS = {
  compute:     'Blackwell Ultra production ramp + Q3 hyperscaler capex prints',
  energy:      'OPEC+ JMMC June meeting; US SPR refill cadence accelerates',
  power:       'PJM RPM auction clearing prices for 2027/28 capacity year',
  grid:        'BPS interconnection queue reform; transformer import tariff review',
  transfer:    'CoreWeave secondary; 800G optics inventory channel checks',
  ai:          'Frontier model spend disclosures + inference economics inflection',
  defense:     'FY26 NDAA conference report; Replicator initiative funding',
  sovereignty: 'EU CRMA implementation; rare earth offtake announcements',
};

function Flywheel({ active, setActive }) {
  const cx = 320, cy = 320, R = 220, innerR = 110;
  const n = STAGES.length;
  const angleStep = (Math.PI * 2) / n;
  const angleOf = i => -Math.PI / 2 + i * angleStep;

  return (
    <svg className="flywheel-svg" viewBox="0 0 640 640" preserveAspectRatio="xMidYMid meet">
      <defs>
        {STAGES.map(s => (
          <radialGradient id={`g-${s.id}`} key={s.id} cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor={s.color} stopOpacity="0.35" />
            <stop offset="60%"  stopColor={s.color} stopOpacity="0.08" />
            <stop offset="100%" stopColor={s.color} stopOpacity="0" />
          </radialGradient>
        ))}
        <linearGradient id="ringStroke" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%"   stopColor="#e76f1c" />
          <stop offset="14%"  stopColor="#f4d220" />
          <stop offset="28%"  stopColor="#22d3ee" />
          <stop offset="42%"  stopColor="#3b82f6" />
          <stop offset="56%"  stopColor="#4ade80" />
          <stop offset="70%"  stopColor="#a855f7" />
          <stop offset="84%"  stopColor="#ef4444" />
          <stop offset="100%" stopColor="#f59e0b" />
        </linearGradient>
      </defs>

      {/* concentric rings */}
      <circle cx={cx} cy={cy} r={R + 40}     fill="none" stroke="#1c2330" strokeWidth="1" strokeDasharray="2 4" />
      <circle cx={cx} cy={cy} r={R}           fill="none" stroke="#262e3d" strokeWidth="1" />
      <circle cx={cx} cy={cy} r={innerR + 30} fill="none" stroke="#1c2330" strokeWidth="1" strokeDasharray="1 3" />
      <circle cx={cx} cy={cy} r={innerR}      fill="#0d1117" stroke="#262e3d" strokeWidth="1" />
      <circle cx={cx} cy={cy} r={R}           fill="none" stroke="url(#ringStroke)" strokeWidth="1.5" opacity="0.5" />

      {/* radial spokes */}
      {STAGES.map((s, i) => {
        const a = angleOf(i);
        return (
          <line
            key={s.id}
            x1={cx + Math.cos(a) * (innerR + 4)} y1={cy + Math.sin(a) * (innerR + 4)}
            x2={cx + Math.cos(a) * (R - 4)}       y2={cy + Math.sin(a) * (R - 4)}
            stroke={s.color} strokeWidth="0.5" opacity="0.25"
          />
        );
      })}

      {/* arc arrows */}
      {STAGES.map((s, i) => {
        const a1 = angleOf(i) + angleStep * 0.08;
        const a2 = angleOf(i) + angleStep * 0.92;
        const r  = R + 18;
        const x1 = cx + Math.cos(a1) * r, y1 = cy + Math.sin(a1) * r;
        const x2 = cx + Math.cos(a2) * r, y2 = cy + Math.sin(a2) * r;
        const isActive = active === s.id;
        return (
          <g key={s.id} opacity={isActive ? 1 : 0.5}>
            <defs>
              <marker id={`arr-${s.id}`} viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                <path d="M0,0 L10,5 L0,10 z" fill={s.color} opacity={isActive ? 1 : 0.6} />
              </marker>
            </defs>
            <path
              d={`M ${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2}`}
              fill="none"
              stroke={s.color}
              strokeWidth={isActive ? 2 : 1}
              opacity={isActive ? 0.9 : 0.35}
              markerEnd={`url(#arr-${s.id})`}
            />
          </g>
        );
      })}

      {/* stage nodes */}
      {STAGES.map((s, i) => {
        const a = angleOf(i);
        const x = cx + Math.cos(a) * R;
        const y = cy + Math.sin(a) * R;
        const isActive = active === s.id;
        const labelR = R + 56;
        const lx = cx + Math.cos(a) * labelR;
        const ly = cy + Math.sin(a) * labelR;
        const anchor = Math.cos(a) > 0.3 ? 'start' : Math.cos(a) < -0.3 ? 'end' : 'middle';
        const dy = Math.sin(a) > 0.5 ? 14 : Math.sin(a) < -0.5 ? -6 : 4;

        return (
          <g key={s.id} style={{ cursor: 'pointer' }} onMouseEnter={() => setActive(s.id)} onClick={() => setActive(s.id)}>
            <circle cx={x} cy={y} r={36} fill={`url(#g-${s.id})`} opacity={isActive ? 1 : 0.6} />
            <circle cx={x} cy={y} r={26} fill="#0d1117" stroke={s.color} strokeWidth={isActive ? 2 : 1} />
            <circle cx={x} cy={y} r={isActive ? 8 : 5} fill={s.color} />
            <text x={x} y={y - 38} textAnchor="middle" fill={s.color} fontFamily="JetBrains Mono" fontSize="10" letterSpacing="0.1em">{s.n}</text>
            <text x={lx} y={ly + dy}      textAnchor={anchor} fill="#e6e9ef" fontFamily="Inter Tight" fontSize="14" fontWeight="600" letterSpacing="-0.01em">{s.name}</text>
            <text x={lx} y={ly + dy + 14} textAnchor={anchor} fill="#5b6473" fontFamily="JetBrains Mono" fontSize="10" letterSpacing="0.05em">{s.weight.toFixed(1)}% · {s.ret}</text>
          </g>
        );
      })}

      {/* hub */}
      <text x={cx} y={cy - 24} textAnchor="middle" fill="#5b6473" fontFamily="JetBrains Mono" fontSize="9" letterSpacing="0.18em">CAPITAL CYCLE</text>
      <text x={cx} y={cy + 4}  textAnchor="middle" fill="#e6e9ef" fontFamily="Inter Tight" fontSize="28" fontWeight="600" letterSpacing="-0.02em">$2.284B</text>
      <text x={cx} y={cy + 24} textAnchor="middle" fill="#4ade80" fontFamily="JetBrains Mono" fontSize="11">+18.42% YTD</text>
      <text x={cx} y={cy + 50} textAnchor="middle" fill="#5b6473" fontFamily="JetBrains Mono" fontSize="9" letterSpacing="0.14em">8 STAGES · 47 HOLDINGS</text>
    </svg>
  );
}

export default function CycleTab({ holdings }) {
  const [active, setActive] = useState('compute');
  const activeStage = STAGES.find(s => s.id === active);

  return (
    <div className="cycle-grid">
      {/* LEFT — thesis flow */}
      <div className="panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <div className="panel-head">
          <span className="panel-title">Thesis Flow</span>
          <span className="panel-actions"><span className="chip">8 / 8</span></span>
        </div>
        <div className="thesis-flow">
          {STAGES.map(s => (
            <div
              key={s.id}
              className="thesis-step"
              style={{ '--stage-color': s.color, background: active === s.id ? 'var(--panel-2)' : 'transparent' }}
              onClick={() => setActive(s.id)}
            >
              <div className="dot"></div>
              <div className="nm">{s.name}<small>{s.desc}</small></div>
              <div className="w">{s.weight.toFixed(1)}%</div>
            </div>
          ))}
        </div>
        <div style={{ padding: '12px 14px', borderTop: '1px solid var(--line)', fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
          Last rebalance · 14d ago
        </div>
      </div>

      {/* CENTER — flywheel + stage strip */}
      <div className="cycle-center">
        <div className="flywheel-panel">
          <div className="flywheel-bg"></div>
          <div className="flywheel-stats">
            <div className="flywheel-label-block">
              <div className="k">Cycle Velocity</div>
              <div className="v">0.847</div>
              <div className="d up">+0.024 vs 30d</div>
            </div>
            <div className="flywheel-label-block" style={{ textAlign: 'right' }}>
              <div className="k">Active Stage</div>
              <div className="v" style={{ color: activeStage.color }}>{activeStage.name}</div>
              <div className="d" style={{ color: 'var(--text-3)' }}>{activeStage.desc}</div>
            </div>
          </div>
          <Flywheel active={active} setActive={setActive} />
        </div>

        <div className="stage-strip">
          {STAGES.map(s => (
            <div
              key={s.id}
              className={'stage-cell' + (active === s.id ? ' active' : '')}
              style={{ '--stage-color': s.color }}
              onClick={() => setActive(s.id)}
            >
              <div className="n">{s.n}</div>
              <div className="name"><span>{s.name}</span></div>
              <div className="val">{s.val}</div>
              <div className="chg up">{s.ret}</div>
            </div>
          ))}
        </div>
      </div>

      {/* RIGHT — stage detail */}
      <div className="panel" style={{ display: 'flex', flexDirection: 'column' }}>
        <div className="panel-head">
          <span className="panel-title" style={{ color: activeStage.color }}>{activeStage.n} · {activeStage.name}</span>
          <span className="panel-actions"><span className="chip live">LIVE</span></span>
        </div>

        <div className="side-card">
          <div className="lbl">Stage Allocation</div>
          <div className="big">{activeStage.weight.toFixed(2)}%</div>
          <div className="delta up">{activeStage.ret} contribution YTD</div>
        </div>

        <div className="side-card">
          <div className="lbl">Capital Flow Index</div>
          <div style={{ marginTop: 8 }}>
            <div style={{ height: 6, background: 'var(--panel-3)', borderRadius: 2, overflow: 'hidden' }}>
              <div style={{ width: activeStage.flow + '%', height: '100%', background: activeStage.color, boxShadow: `0 0 12px ${activeStage.color}` }}></div>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 6, fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.08em' }}>
              <span>OUTFLOW</span>
              <span style={{ color: 'var(--text)' }}>{activeStage.flow} / 100</span>
              <span>INFLOW</span>
            </div>
          </div>
        </div>

        <div className="side-card">
          <div className="lbl">Top Holdings</div>
          <div style={{ marginTop: 8, display: 'flex', flexDirection: 'column', gap: 8 }}>
            {holdings.filter(h => h.stage === active).slice(0, 4).map(h => (
              <div key={h.ticker} style={{ display: 'grid', gridTemplateColumns: '48px 1fr auto', gap: 10, alignItems: 'center' }}>
                <span className="mono" style={{ fontSize: 11, color: 'var(--text)', fontWeight: 600 }}>{h.ticker}</span>
                <span style={{ fontSize: 11, color: 'var(--text-3)' }}>{h.name}</span>
                <span className={'mono ' + (parseFloat(h.day) >= 0 ? 'up' : 'down')} style={{ fontSize: 11 }}>{h.day}</span>
              </div>
            ))}
            {holdings.filter(h => h.stage === active).length === 0 && (
              <span style={{ fontSize: 11, color: 'var(--text-3)' }}>No holdings tagged in this stage</span>
            )}
          </div>
        </div>

        <div className="side-card">
          <div className="lbl">Key Catalyst · Next 30d</div>
          <div style={{ fontSize: 12, lineHeight: 1.45, marginTop: 6, color: 'var(--text-2)' }}>
            {CATALYSTS[active] || 'Monitor for emerging macro drivers'}
          </div>
        </div>

        <div className="side-card" style={{ marginTop: 'auto' }}>
          <div className="lbl">Drilldown</div>
          <div style={{ display: 'flex', gap: 6, marginTop: 8, flexWrap: 'wrap' }}>
            {['Holdings', 'Flows', 'Catalysts', 'Risk', 'Notes'].map(b => (
              <button
                key={b}
                style={{ padding: '5px 10px', border: '1px solid var(--line)', borderRadius: 2, fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-2)', letterSpacing: '0.08em', textTransform: 'uppercase', background: 'transparent', cursor: 'pointer' }}
              >{b}</button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

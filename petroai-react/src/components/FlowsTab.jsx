import { STAGES, FLOWS } from '../data/staticData.js';

// Deterministic rotation matrix: how much each stage rotates capital to another
// Positive = source sends to target, negative = source draws from target
function rotationValue(fromIdx, toIdx) {
  if (fromIdx === toIdx) return 0;
  const seed = (fromIdx * 8 + toIdx) * 17 + fromIdx * 3;
  const s = ((seed * 9301 + 49297) % 233280) / 233280;
  // Bias: adjacent stages rotate more
  const adj = Math.abs(fromIdx - toIdx) <= 1 ? 1.4 : 0.7;
  return (s - 0.45) * 100 * adj;
}

const ROTATION_SIGNALS = [
  { from: 'compute', to: 'grid',    dir: 'in',  val: '+$124M', note: 'Power infra upgrade ahead of Blackwell ramps' },
  { from: 'ai',      to: 'compute', dir: 'in',  val: '+$98M',  note: 'Inference cluster buildout drives GPU demand' },
  { from: 'energy',  to: 'power',   dir: 'in',  val: '+$67M',  note: 'Gas-to-power conversion plays gaining traction' },
  { from: 'transfer',to: 'compute', dir: 'out', val: '-$43M',  note: 'Optics digestion cycle; capital reallocating upstream' },
  { from: 'sovereignty', to: 'defense', dir: 'in', val: '+$38M', note: 'Strategic metals → autonomy supply chain plays' },
  { from: 'power',   to: 'grid',    dir: 'in',  val: '+$31M',  note: 'SMR-adjacent grid interconnect investment' },
];

export default function FlowsTab() {
  const maxFlow = Math.max(...FLOWS.map(f => f.flow));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

      {/* Inflow / Outflow bars */}
      <div className="panel">
        <div className="panel-head">
          <span className="panel-title">Capital Flow · Stage Velocity</span>
          <span className="panel-actions">
            <span className="chip">5D Snapshot</span>
            <span className="chip live">LIVE</span>
          </span>
        </div>
        <div style={{ padding: '8px 0 4px' }}>
          {FLOWS.map(f => {
            const stage = STAGES.find(s => s.id === f.stage);
            const pct = (f.flow / maxFlow) * 100;
            const isHigh = f.flow >= 80;
            return (
              <div key={f.stage} style={{ display: 'grid', gridTemplateColumns: '80px 1fr 40px 40px', alignItems: 'center', gap: 12, padding: '7px 18px' }}>
                <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: stage.color, fontWeight: 600 }}>{f.lbl}</span>
                <div style={{ position: 'relative', height: 16, background: 'var(--panel-3)', borderRadius: 2, overflow: 'hidden' }}>
                  <div style={{
                    position: 'absolute', left: 0, top: 0, bottom: 0,
                    width: pct + '%',
                    background: `linear-gradient(90deg, ${stage.color}88, ${stage.color})`,
                    boxShadow: isHigh ? `0 0 14px ${stage.color}66` : 'none',
                    borderRadius: 2,
                    transition: 'width 0.4s ease',
                  }} />
                </div>
                <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text)', textAlign: 'right' }}>{f.flow}</span>
                <span style={{ fontFamily: 'var(--mono)', fontSize: 9, letterSpacing: '0.08em', color: isHigh ? '#4ade80' : 'var(--text-3)', textAlign: 'right' }}>
                  {isHigh ? 'HIGH' : f.flow >= 60 ? 'MED' : 'LOW'}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: 16 }}>

        {/* Rotation matrix */}
        <div className="panel">
          <div className="panel-head">
            <span className="panel-title">Rotation Matrix · Cross-Stage Capital Movement</span>
            <span className="panel-actions"><span className="chip">5D</span></span>
          </div>
          <div style={{ padding: '12px 18px', overflowX: 'auto' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%', fontFamily: 'var(--mono)', fontSize: 9 }}>
              <thead>
                <tr>
                  <th style={{ width: 60, padding: '4px 6px', color: 'var(--text-3)', textAlign: 'left', fontWeight: 400 }}>FROM ↓ TO →</th>
                  {STAGES.map(s => (
                    <th key={s.id} style={{ padding: '4px 6px', color: s.color, fontWeight: 600, textAlign: 'center', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
                      {s.name.slice(0, 4).toUpperCase()}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {STAGES.map((rowStage, ri) => (
                  <tr key={rowStage.id}>
                    <td style={{ padding: '4px 6px', color: rowStage.color, fontWeight: 600, letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>
                      {rowStage.name.slice(0, 4).toUpperCase()}
                    </td>
                    {STAGES.map((colStage, ci) => {
                      if (ri === ci) return (
                        <td key={colStage.id} style={{ padding: '4px 6px', textAlign: 'center', background: 'var(--panel-3)', color: 'var(--text-4)' }}>—</td>
                      );
                      const val = rotationValue(ri, ci);
                      const intensity = Math.min(Math.abs(val) / 80, 1);
                      const isPos = val >= 0;
                      const bg = isPos
                        ? `rgba(74,222,128,${intensity * 0.25})`
                        : `rgba(248,113,113,${intensity * 0.25})`;
                      return (
                        <td key={colStage.id} style={{ padding: '4px 6px', textAlign: 'center', background: bg, color: isPos ? '#4ade80' : '#f87171', borderRadius: 2 }}>
                          {isPos ? '+' : ''}{val.toFixed(0)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ marginTop: 10, fontFamily: 'var(--mono)', fontSize: 9, color: 'var(--text-3)', letterSpacing: '0.08em' }}>
              Values in relative flow units · <span style={{ color: '#4ade80' }}>Green = inflow gaining</span> · <span style={{ color: '#f87171' }}>Red = outflow pressure</span>
            </div>
          </div>
        </div>

        {/* Rotation signals */}
        <div className="panel">
          <div className="panel-head">
            <span className="panel-title">Rotation Signals</span>
            <span className="panel-actions"><span className="chip live">LIVE</span></span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {ROTATION_SIGNALS.map((sig, i) => {
              const fromStage = STAGES.find(s => s.id === sig.from);
              const toStage   = STAGES.find(s => s.id === sig.to);
              const isIn = sig.dir === 'in';
              return (
                <div key={i} style={{ padding: '12px 16px', borderBottom: '1px solid var(--line)', display: 'flex', flexDirection: 'column', gap: 4 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: fromStage.color, fontWeight: 600 }}>{fromStage.name}</span>
                    <span style={{ fontFamily: 'var(--mono)', fontSize: 9, color: 'var(--text-3)' }}>→</span>
                    <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: toStage.color, fontWeight: 600 }}>{toStage.name}</span>
                    <span style={{ marginLeft: 'auto', fontFamily: 'var(--mono)', fontSize: 11, color: isIn ? '#4ade80' : '#f87171', fontWeight: 600 }}>{sig.val}</span>
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-3)', lineHeight: 1.4 }}>{sig.note}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Flow velocity chart — simple SVG bar chart */}
      <div className="panel">
        <div className="panel-head">
          <span className="panel-title">Flow Velocity · Comparative Stage Intensity</span>
          <span className="panel-actions"><span className="chip">Current Snapshot</span></span>
        </div>
        <div style={{ padding: '20px 18px' }}>
          <svg viewBox={`0 0 ${FLOWS.length * 80} 140`} style={{ width: '100%', height: 140, overflow: 'visible' }}>
            {FLOWS.map((f, i) => {
              const stage = STAGES.find(s => s.id === f.stage);
              const barH = (f.flow / 100) * 100;
              const x = i * 80 + 10;
              const y = 110 - barH;
              return (
                <g key={f.stage}>
                  <rect x={x} y={y} width={52} height={barH} fill={stage.color} opacity={0.85} rx={2} />
                  <rect x={x} y={y} width={52} height={3} fill={stage.color} rx={1} />
                  <text x={x + 26} y={125} textAnchor="middle" fill={stage.color} fontFamily="JetBrains Mono" fontSize="8" letterSpacing="0.06em">
                    {f.lbl.slice(0, 5).toUpperCase()}
                  </text>
                  <text x={x + 26} y={y - 5} textAnchor="middle" fill={stage.color} fontFamily="JetBrains Mono" fontSize="9">
                    {f.flow}
                  </text>
                </g>
              );
            })}
            {/* baseline */}
            <line x1={0} y1={111} x2={FLOWS.length * 80} y2={111} stroke="var(--line)" strokeWidth={1} />
          </svg>
        </div>
      </div>
    </div>
  );
}

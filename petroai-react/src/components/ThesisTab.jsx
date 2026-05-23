import { useState } from 'react';
import { STAGES, HOLDINGS } from '../data/staticData.js';

const STATUSES = ['EARLY', 'MID', 'LATE', 'PEAK'];
const STATUS_COLOR = { EARLY: '#4ade80', MID: '#3b82f6', LATE: '#f4d220', PEAK: '#ef4444' };

const DEFAULT_STATE = STAGES.map(s => ({
  id: s.id,
  status: s.id === 'compute' ? 'PEAK' : s.id === 'ai' ? 'LATE' : s.id === 'grid' ? 'MID' : s.id === 'energy' ? 'MID' : 'EARLY',
  conviction: s.id === 'compute' ? 88 : s.id === 'ai' ? 82 : s.id === 'grid' ? 74 : s.id === 'energy' ? 71 : 55,
  bull: '',
  bear: '',
  updated: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
}));

const DEFAULT_BULLS = {
  energy:      'Tight supply discipline + AI power demand creates structurally higher baseload. WTI backwardation signals supply deficit through Q3.',
  power:       'Nuclear renaissance + data center PPAs provide long-duration contracted cash flows. Capacity price reset incoming in PJM 2027/28.',
  grid:        'Once-in-a-generation T&D upgrade cycle. 142-week transformer lead times create durable moat for incumbents.',
  compute:     'GB200 NVL72 rack density unlock drives ASP expansion. Hyperscaler capex guided $312B for FY26 — no signs of pause.',
  transfer:    'Optical transceivers and 800G switching becoming critical path. CoreWeave buildout accelerates demand.',
  ai:          'Inference scaling inflects economics. Enterprise adoption creates durable recurring revenue streams across frontier labs.',
  defense:     'Replicator initiative + autonomous systems shift drives multi-year procurement uplift. Bipartisan support insulates from budget risk.',
  sovereignty: 'Ex-China rare earth supply chain critical path. Government off-take agreements de-risk capital. NdPr premium structurally elevated.',
};
const DEFAULT_BEARS = {
  energy:      'Demand destruction from efficiency gains + EV adoption. OPEC+ cohesion risk if Saudi needs revenue at higher volumes.',
  power:       'Regulatory risk on nuclear permitting timelines. Spot power prices volatile — PPA economics less compelling if grid prices fall.',
  grid:        'Import tariff relief could lower barriers. Permitting reform could accelerate competition. Long lead times create execution risk.',
  compute:     'China export controls could disrupt supply chain. Customer concentration in hyperscalers. Valuation implies continued flawless execution.',
  transfer:    'Inventory digestion cycles in networking. CoreWeave may bring own fiber/optics in-house. Margin compression risk.',
  ai:          'Commoditization of model capabilities. Regulatory headwinds on data/IP. CapEx discipline reversal if ROI disappoints.',
  defense:     'Continuing resolution risk delays large program starts. Budget sequestration scenario. International competitors gaining capability.',
  sovereignty: 'China could flood market with below-cost production. Recycling technology disrupts primary mining economics long-term.',
};

export default function ThesisTab() {
  const [stages, setStages] = useState(
    DEFAULT_STATE.map(s => ({ ...s, bull: DEFAULT_BULLS[s.id] || '', bear: DEFAULT_BEARS[s.id] || '' }))
  );
  const [expanded, setExpanded] = useState(null);

  function update(id, field, value) {
    setStages(prev => prev.map(s =>
      s.id === id ? { ...s, [field]: value, updated: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) } : s
    ));
  }

  const avgConviction = Math.round(stages.reduce((a, s) => a + s.conviction, 0) / stages.length);
  const primaryStage = stages.reduce((a, b) => a.conviction > b.conviction ? a : b);
  const primaryStageDef = STAGES.find(s => s.id === primaryStage.id);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>

      {/* Summary card */}
      <div className="panel">
        <div className="panel-head">
          <span className="panel-title">Thesis Summary</span>
          <span className="panel-actions"><span className="chip live">SESSION</span></span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 1, background: 'var(--line)' }}>
          <div style={{ background: 'var(--panel-2)', padding: '16px 18px' }}>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Primary Focus</div>
            <div style={{ fontSize: 18, fontWeight: 600, color: primaryStageDef.color }}>{primaryStageDef.name}</div>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', marginTop: 4 }}>{primaryStageDef.desc}</div>
          </div>
          <div style={{ background: 'var(--panel-2)', padding: '16px 18px' }}>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Portfolio Conviction</div>
            <div style={{ fontSize: 18, fontWeight: 600, color: avgConviction >= 70 ? '#4ade80' : avgConviction >= 50 ? '#f4d220' : '#f87171' }}>{avgConviction}%</div>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', marginTop: 4 }}>avg across 8 stages</div>
          </div>
          <div style={{ background: 'var(--panel-2)', padding: '16px 18px' }}>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>High Conviction</div>
            <div style={{ fontSize: 18, fontWeight: 600, color: 'var(--text)' }}>{stages.filter(s => s.conviction >= 75).length}</div>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', marginTop: 4 }}>stages ≥ 75%</div>
          </div>
          <div style={{ background: 'var(--panel-2)', padding: '16px 18px' }}>
            <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Cycle Stage</div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 4 }}>
              {['PEAK', 'LATE', 'MID', 'EARLY'].map(st => {
                const count = stages.filter(s => s.status === st).length;
                return count > 0 ? (
                  <span key={st} style={{ fontFamily: 'var(--mono)', fontSize: 10, color: STATUS_COLOR[st], background: STATUS_COLOR[st] + '22', padding: '2px 7px', borderRadius: 2 }}>
                    {st} · {count}
                  </span>
                ) : null;
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Stage rows */}
      {stages.map(stg => {
        const def = STAGES.find(s => s.id === stg.id);
        const tickers = HOLDINGS.filter(h => h.stage === stg.id);
        const isOpen = expanded === stg.id;
        return (
          <div key={stg.id} className="panel" style={{ borderLeft: `3px solid ${def.color}` }}>
            {/* Collapsed header row */}
            <div
              style={{ display: 'grid', gridTemplateColumns: '28px 120px 1fr auto auto 120px', alignItems: 'center', gap: 16, padding: '14px 18px', cursor: 'pointer' }}
              onClick={() => setExpanded(isOpen ? null : stg.id)}
            >
              <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: def.color, letterSpacing: '0.1em' }}>{def.n}</span>
              <span style={{ fontWeight: 600, color: def.color }}>{def.name}</span>

              {/* Status pills */}
              <div style={{ display: 'flex', gap: 4 }}>
                {STATUSES.map(st => (
                  <button
                    key={st}
                    onClick={e => { e.stopPropagation(); update(stg.id, 'status', st); }}
                    style={{
                      padding: '3px 9px', borderRadius: 2, fontFamily: 'var(--mono)', fontSize: 9, letterSpacing: '0.1em',
                      border: `1px solid ${stg.status === st ? STATUS_COLOR[st] : 'var(--line)'}`,
                      background: stg.status === st ? STATUS_COLOR[st] + '22' : 'transparent',
                      color: stg.status === st ? STATUS_COLOR[st] : 'var(--text-3)',
                    }}
                  >{st}</button>
                ))}
              </div>

              {/* Conviction slider */}
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', width: 32, textAlign: 'right' }}>{stg.conviction}%</span>
                <input
                  type="range" min={0} max={100} value={stg.conviction}
                  onClick={e => e.stopPropagation()}
                  onChange={e => { e.stopPropagation(); update(stg.id, 'conviction', Number(e.target.value)); }}
                  style={{ width: 100, accentColor: def.color }}
                />
              </div>

              <div style={{ display: 'flex', gap: 6 }}>
                {tickers.slice(0, 3).map(h => (
                  <span key={h.ticker} style={{ fontFamily: 'var(--mono)', fontSize: 9, color: def.color, background: def.color + '18', padding: '2px 6px', borderRadius: 2 }}>{h.ticker}</span>
                ))}
                {tickers.length > 3 && <span style={{ fontFamily: 'var(--mono)', fontSize: 9, color: 'var(--text-3)' }}>+{tickers.length - 3}</span>}
              </div>

              <span style={{ fontFamily: 'var(--mono)', fontSize: 9, color: 'var(--text-3)', textAlign: 'right' }}>
                {isOpen ? '▲' : '▼'} {stg.updated}
              </span>
            </div>

            {/* Expanded detail */}
            {isOpen && (
              <div style={{ borderTop: '1px solid var(--line)', padding: '16px 18px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
                <div>
                  <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: '#4ade80', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Bull Case</div>
                  <textarea
                    value={stg.bull}
                    onChange={e => update(stg.id, 'bull', e.target.value)}
                    rows={5}
                    style={{ width: '100%', background: 'var(--panel-2)', border: '1px solid var(--line)', borderRadius: 4, color: 'var(--text-2)', fontFamily: 'var(--sans)', fontSize: 12, padding: '10px 12px', resize: 'vertical', lineHeight: 1.5 }}
                  />
                </div>
                <div>
                  <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: '#f87171', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 6 }}>Bear Case</div>
                  <textarea
                    value={stg.bear}
                    onChange={e => update(stg.id, 'bear', e.target.value)}
                    rows={5}
                    style={{ width: '100%', background: 'var(--panel-2)', border: '1px solid var(--line)', borderRadius: 4, color: 'var(--text-2)', fontFamily: 'var(--sans)', fontSize: 12, padding: '10px 12px', resize: 'vertical', lineHeight: 1.5 }}
                  />
                </div>
                <div style={{ gridColumn: '1 / -1' }}>
                  <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 8 }}>Holdings in this Stage</div>
                  <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                    {tickers.map(h => (
                      <div key={h.ticker} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 10px', background: 'var(--panel-2)', border: '1px solid var(--line)', borderRadius: 4 }}>
                        <span style={{ fontFamily: 'var(--mono)', fontSize: 11, fontWeight: 600, color: def.color }}>{h.ticker}</span>
                        <span style={{ fontSize: 11, color: 'var(--text-3)' }}>{h.name}</span>
                        <span style={{ fontFamily: 'var(--mono)', fontSize: 11, color: parseFloat(h.day) >= 0 ? '#4ade80' : '#f87171' }}>{h.day}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

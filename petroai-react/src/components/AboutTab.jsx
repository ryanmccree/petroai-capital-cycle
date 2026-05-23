import { STAGES, HOLDINGS, THESIS_NOTE } from '../data/staticData.js';

const TIER_COLORS = ['#e76f1c', '#3b82f6', '#a855f7'];

const WHY_MATTERS = {
  energy:      'The base of every AI factory is power, and power starts here. Hydrocarbons and uranium define the input cost of compute. Tight upstream supply creates structural scarcity that flows through every layer of the stack.',
  power:       'Electricity is the currency of AI. Every GPU rack requires continuous, reliable power — nuclear and gas generation provide the baseload that intermittent renewables cannot. Data center PPAs are becoming the dominant power contract vehicle.',
  grid:        'The bottleneck between generation and consumption. Transformer lead times of 142+ weeks mean grid infrastructure constrains AI factory buildout more than silicon. Interconnection reform is the critical regulatory catalyst.',
  compute:     'The AI factory floor. NVIDIA\'s $145B supply commitment signals that demand is structural, not cyclical. HBM memory, advanced packaging, and custom silicon (ARM, AMKR) are the adjacent plays as GPU supply loosens.',
  transfer:    'Networking is the fastest-growing bottleneck inside the AI factory. NVDA Spectrum-X networking revenue tripled YoY. Optical transceivers, 800G Ethernet, and accelerated storage are the picks-and-shovels of the inference era.',
  ai:          'The monetization layer. Frontier model spend is tracking $312B for FY26 across hyperscalers. Inference economics are inflecting — cost per token falling rapidly creates demand elasticity that drives volume expansion across the stack.',
  defense:     'AI and autonomy are restructuring how nations project power. Replicator initiative, autonomous undersea vehicles, and ISR platforms represent multi-year procurement uplift with bipartisan budget support.',
  sovereignty: 'The chokepoint in the supply chain. Rare earth elements — neodymium, praseodymium, dysprosium — are critical inputs for motors, magnets, and defense systems. Ex-China supply is structurally undersupplied vs. AI-era demand.',
};

function StagePill({ color, name }) {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '2px 8px', borderRadius: 2, background: color + '20', border: `1px solid ${color}44`, fontFamily: 'var(--mono)', fontSize: 10, color, letterSpacing: '0.06em' }}>
      {name}
    </span>
  );
}

function TickerPill({ ticker, color }) {
  return (
    <span style={{ display: 'inline-block', padding: '3px 10px', borderRadius: 2, background: color + '18', border: `1px solid ${color}55`, fontFamily: 'var(--mono)', fontSize: 11, fontWeight: 600, color, letterSpacing: '0.06em' }}>
      {ticker}
    </span>
  );
}

export default function AboutTab() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 1100, margin: '0 auto' }}>

      {/* ── SECTION 1: Hero ── */}
      <div style={{ padding: '40px 36px', background: 'linear-gradient(135deg, #0d1117 60%, #1a1006 100%)', border: '1px solid #e76f1c44', borderRadius: 6, position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: 0, right: 0, width: 400, height: '100%', background: 'radial-gradient(ellipse at 80% 50%, #e76f1c0a, transparent 70%)', pointerEvents: 'none' }} />
        <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: '#e76f1c', letterSpacing: '0.2em', textTransform: 'uppercase', marginBottom: 12 }}>PetroAI Research · Capital Cycle Dashboard</div>
        <h1 style={{ margin: '0 0 8px', fontSize: 36, fontWeight: 700, letterSpacing: '-0.03em', color: 'var(--text)', lineHeight: 1.1 }}>
          PetroAI Capital Cycle
        </h1>
        <div style={{ fontSize: 18, color: '#e76f1c', fontWeight: 500, marginBottom: 28, letterSpacing: '-0.01em' }}>
          Where energy, compute &amp; capital converge
        </div>

        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 24 }}>
          {STAGES.map(s => (
            <span key={s.id} style={{ padding: '4px 12px', borderRadius: 2, background: s.color + '18', border: `1px solid ${s.color}44`, fontFamily: 'var(--mono)', fontSize: 10, color: s.color, letterSpacing: '0.08em' }}>
              {s.name}
            </span>
          ))}
        </div>

        <div style={{ borderLeft: '3px solid #e76f1c', paddingLeft: 20, display: 'flex', flexDirection: 'column', gap: 10 }}>
          <p style={{ margin: 0, fontSize: 15, lineHeight: 1.7, color: 'var(--text-2)' }}>
            It is a flywheel: <span style={{ color: 'var(--text)', fontWeight: 500 }}>Solve one constraint → expose the next → capital rotates.</span>
          </p>
          <p style={{ margin: 0, fontFamily: 'var(--mono)', fontSize: 12, color: '#e76f1c', letterSpacing: '0.04em' }}>
            Energy → Power → Grid → Compute → Transfer → AI → Defense → Sovereignty
          </p>
          <p style={{ margin: 0, fontSize: 14, lineHeight: 1.65, color: 'var(--text-2)' }}>
            Companies are not separate plays — they are layers in one integrated stack.
            The market constantly shifts capital to the current bottleneck forcing trillions in capex.
          </p>
          <a
            href="https://x.com/mikalche"
            target="_blank"
            rel="noopener noreferrer"
            style={{ fontFamily: 'var(--mono)', fontSize: '0.85rem', color: '#f59e0b', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: 6, marginTop: 4 }}
            onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
            onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}
          >
            𝕏 @mikalche — This thesis was created by @mikalche on X (Twitter)
          </a>
        </div>
      </div>

      {/* ── SECTION 2: AI Factory Framework ── */}
      <div className="panel">
        <div className="panel-head">
          <span className="panel-title">The AI Factory Framework</span>
          <span className="panel-actions">
            <span className="chip">{THESIS_NOTE.source}</span>
            <span className="chip">{THESIS_NOTE.date}</span>
          </span>
        </div>

        <div style={{ padding: '24px 24px 8px' }}>
          <div style={{ fontSize: 20, fontWeight: 600, lineHeight: 1.35, color: 'var(--text)', marginBottom: 20, letterSpacing: '-0.02em' }}>
            {THESIS_NOTE.headline}
          </div>
          <p style={{ fontSize: 14, lineHeight: 1.75, color: 'var(--text-2)', marginBottom: 24 }}>
            {THESIS_NOTE.body}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14, marginBottom: 24 }}>
            {THESIS_NOTE.tiers.map((tier, i) => (
              <div key={i} style={{ padding: '16px 18px', background: 'var(--panel-2)', border: `1px solid ${TIER_COLORS[i]}44`, borderTop: `3px solid ${TIER_COLORS[i]}`, borderRadius: 4 }}>
                <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: TIER_COLORS[i], letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 10 }}>
                  {tier.label}
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }}>
                  {tier.tickers.map(t => <TickerPill key={t} ticker={t} color={TIER_COLORS[i]} />)}
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-3)', lineHeight: 1.5 }}>{tier.desc}</div>
              </div>
            ))}
          </div>

          <div style={{ padding: '16px 20px', background: 'var(--panel-3)', borderRadius: 4, marginBottom: 16 }}>
            <p style={{ margin: 0, fontSize: 14, fontStyle: 'italic', lineHeight: 1.7, color: 'var(--text-2)' }}>
              "{THESIS_NOTE.conclusion}"
            </p>
          </div>

          <div style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--text-3)', marginBottom: 16 }}>
            {THESIS_NOTE.framework}
          </div>

          <div style={{ fontSize: 12, color: 'var(--text-3)', paddingBottom: 8 }}>
            —{' '}
            <a
              href="https://x.com/mikalche"
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: '#e76f1c', textDecoration: 'none' }}
              onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
              onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}
            >{THESIS_NOTE.source}</a>, {THESIS_NOTE.date}
          </div>
        </div>
      </div>

      {/* ── SECTION 3: How to read the dashboard ── */}
      <div>
        <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 12 }}>
          How to read this dashboard
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14 }}>
          {[
            {
              num: '01', label: 'Cycle Visualization', color: '#e76f1c',
              desc: 'The flywheel diagram shows all 8 stages of the capital cycle. Click any node or stage cell to drill into that theme — see allocation, capital flow index, top holdings, and the key catalyst for the next 30 days. The left rail shows the full thesis sequence; hover to switch focus.',
            },
            {
              num: '02', label: 'Portfolio', color: '#3b82f6',
              desc: 'Holdings cards show each position with live price, daily return, weight, and cost basis. Filter by stage using the pill buttons, search by ticker, name, or theme. Toggle to Table view for a sortable spreadsheet layout with P&L% for each position.',
            },
            {
              num: '03', label: 'Market Overview', color: '#a855f7',
              desc: 'Index strip shows PETROAI-100 vs major benchmarks with sparklines. The cycle heatmap shows intraday moves for all tracked names, color-coded by stage. Capital flow bars show rotation intensity. Movers, signals, and newsflow on the right.',
            },
          ].map(card => (
            <div key={card.num} style={{ padding: '20px 20px', background: 'var(--panel)', border: '1px solid var(--line)', borderTop: `3px solid ${card.color}`, borderRadius: 4 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
                <span style={{ fontFamily: 'var(--mono)', fontSize: 10, color: card.color, letterSpacing: '0.1em' }}>{card.num}</span>
                <span style={{ fontWeight: 600, fontSize: 14, color: 'var(--text)' }}>{card.label}</span>
              </div>
              <p style={{ margin: 0, fontSize: 13, lineHeight: 1.65, color: 'var(--text-2)' }}>{card.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ── SECTION 4: The 8 Stages ── */}
      <div>
        <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 12 }}>
          The 8 Stages of the Capital Cycle
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12 }}>
          {STAGES.map(s => {
            const exampleTickers = HOLDINGS.filter(h => h.stage === s.id).slice(0, 3).map(h => h.ticker);
            return (
              <div key={s.id} style={{ padding: '18px 18px', background: 'var(--panel)', border: '1px solid var(--line)', borderLeft: `3px solid ${s.color}`, borderRadius: 4 }}>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 8 }}>
                  <span style={{ fontFamily: 'var(--mono)', fontSize: 9, color: s.color, letterSpacing: '0.1em' }}>{s.n}</span>
                  <span style={{ fontWeight: 700, fontSize: 14, color: s.color }}>{s.name}</span>
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-3)', marginBottom: 10, fontFamily: 'var(--mono)', letterSpacing: '0.04em' }}>{s.desc}</div>
                <p style={{ margin: '0 0 12px', fontSize: 12, lineHeight: 1.6, color: 'var(--text-2)' }}>
                  {WHY_MATTERS[s.id]}
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 5 }}>
                  {exampleTickers.map(t => (
                    <span key={t} style={{ fontFamily: 'var(--mono)', fontSize: 9, color: s.color, background: s.color + '15', padding: '2px 7px', borderRadius: 2, letterSpacing: '0.06em' }}>{t}</span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── SECTION 5: Credits ── */}
      <div style={{ padding: '28px 20px', textAlign: 'center', borderTop: '1px solid var(--line)', marginTop: 8 }}>
        <div style={{ fontSize: 13, color: 'var(--text-2)', marginBottom: 8 }}>
          Built by <span style={{ color: 'var(--text)', fontWeight: 500 }}>Ryan M.</span> to monitor{' '}
          <span style={{ color: '#e76f1c', fontWeight: 500 }}>@mikalche</span>'s PetroAI Capital Cycle Thesis
        </div>
        <div style={{ fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.08em', display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
          <span>Not financial advice</span>
          <span style={{ color: 'var(--line-2)' }}>·</span>
          <span>Data via Yahoo Finance</span>
          <span style={{ color: 'var(--line-2)' }}>·</span>
          <span>Powered by React + Vite + Vercel</span>
          <span style={{ color: 'var(--line-2)' }}>·</span>
          <span>Engine v4.2.1</span>
        </div>
      </div>

    </div>
  );
}

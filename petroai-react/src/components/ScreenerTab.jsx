import { useState, useMemo } from 'react';
import { STAGES } from '../data/staticData.js';

const SORT_OPTIONS = ['Ticker', 'Name', 'Day %', 'Weight', 'Market Cap', 'P&L %'];

function parsePct(str) { return parseFloat(String(str).replace('%', '')) || 0; }
function parseMcap(str) {
  const s = String(str).replace(/[$,]/g, '');
  if (s.endsWith('T')) return parseFloat(s) * 1e12;
  if (s.endsWith('B')) return parseFloat(s) * 1e9;
  if (s.endsWith('M')) return parseFloat(s) * 1e6;
  return parseFloat(s) || 0;
}

export default function ScreenerTab({ holdings }) {
  const [stageFilter, setStageFilter] = useState(new Set());
  const [perfFilter, setPerfFilter] = useState('all');
  const [sortBy, setSortBy] = useState('Weight');
  const [sortDir, setSortDir] = useState('desc');
  const [selected, setSelected] = useState(null);

  function toggleStage(id) {
    setStageFilter(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }

  function handleSort(col) {
    if (sortBy === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc');
    else { setSortBy(col); setSortDir('desc'); }
  }

  const results = useMemo(() => {
    let list = [...holdings];

    if (stageFilter.size > 0) list = list.filter(h => stageFilter.has(h.stage));
    if (perfFilter === 'gainers') list = list.filter(h => parsePct(h.day) > 0);
    if (perfFilter === 'losers')  list = list.filter(h => parsePct(h.day) < 0);

    list.sort((a, b) => {
      let va, vb;
      if (sortBy === 'Ticker')      { va = a.ticker; vb = b.ticker; }
      else if (sortBy === 'Name')   { va = a.name; vb = b.name; }
      else if (sortBy === 'Day %')  { va = parsePct(a.day); vb = parsePct(b.day); }
      else if (sortBy === 'Weight') { va = a.pct; vb = b.pct; }
      else if (sortBy === 'Market Cap') { va = parseMcap(a.mcap); vb = parseMcap(b.mcap); }
      else if (sortBy === 'P&L %')  { va = ((a.price - a.cost) / a.cost); vb = ((b.price - b.cost) / b.cost); }
      else { va = 0; vb = 0; }
      if (typeof va === 'string') return sortDir === 'asc' ? va.localeCompare(vb) : vb.localeCompare(va);
      return sortDir === 'asc' ? va - vb : vb - va;
    });

    return list;
  }, [holdings, stageFilter, perfFilter, sortBy, sortDir]);

  const totalWeight = results.reduce((a, h) => a + h.pct, 0);

  function exportCsv() {
    const header = 'Ticker,Name,Stage,Price,Day%,Weight%,Cost,MarketCap,P&L%';
    const rows = results.map(h => {
      const pnl = (((h.price - h.cost) / h.cost) * 100).toFixed(1);
      return [h.ticker, h.name, h.stage, h.price, h.day, h.wgt, h.cost, h.mcap, pnl + '%'].join(',');
    });
    const csv = [header, ...rows].join('\n');
    navigator.clipboard.writeText(csv).then(() => alert('CSV copied to clipboard'));
  }

  const SortIcon = ({ col }) => {
    if (sortBy !== col) return <span style={{ color: 'var(--text-4)', marginLeft: 3 }}>⇅</span>;
    return <span style={{ color: 'var(--text-2)', marginLeft: 3 }}>{sortDir === 'asc' ? '↑' : '↓'}</span>;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>

      {/* Filter toolbar */}
      <div className="panel" style={{ padding: '14px 18px' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, alignItems: 'center' }}>

          {/* Stage filters */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
            <button
              onClick={() => setStageFilter(new Set())}
              className={'pill' + (stageFilter.size === 0 ? ' active' : '')}
            >All</button>
            {STAGES.map(s => (
              <button
                key={s.id}
                onClick={() => toggleStage(s.id)}
                style={{
                  padding: '4px 10px', borderRadius: 2, fontFamily: 'var(--mono)', fontSize: 10,
                  border: stageFilter.has(s.id) ? `1px solid ${s.color}` : '1px solid var(--line)',
                  background: stageFilter.has(s.id) ? s.color + '22' : 'transparent',
                  color: stageFilter.has(s.id) ? s.color : 'var(--text-2)',
                  cursor: 'pointer',
                }}
              >{s.name}</button>
            ))}
          </div>

          <div style={{ width: 1, height: 24, background: 'var(--line)' }}></div>

          {/* Performance filter */}
          <div className="pill-group">
            {['all', 'gainers', 'losers'].map(p => (
              <button key={p} className={'pill' + (perfFilter === p ? ' active' : '')} onClick={() => setPerfFilter(p)}>
                {p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>

          <div style={{ marginLeft: 'auto' }}>
            <button
              onClick={exportCsv}
              style={{ padding: '6px 14px', border: '1px solid var(--line)', borderRadius: 2, fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-2)', letterSpacing: '0.08em', cursor: 'pointer', background: 'transparent' }}
            >
              EXPORT CSV
            </button>
          </div>
        </div>
      </div>

      {/* Results table */}
      <div className="panel" style={{ overflow: 'hidden' }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontFamily: 'var(--mono)', fontSize: 11 }}>
            <thead>
              <tr style={{ background: '#1c2330' }}>
                {['Ticker', 'Name', 'Stage', 'Price', 'Day %', 'Weight', 'Cost Basis', 'Mkt Cap', 'P&L %'].map(col => {
                  const sortCol = col === 'Cost Basis' ? 'Cost' : col === 'Mkt Cap' ? 'Market Cap' : col;
                  const isSortable = SORT_OPTIONS.includes(sortCol) || SORT_OPTIONS.includes(col);
                  return (
                    <th
                      key={col}
                      onClick={() => isSortable && handleSort(col === 'Cost Basis' ? 'Weight' : col === 'Mkt Cap' ? 'Market Cap' : col)}
                      style={{
                        padding: '9px 12px', textAlign: col === 'Name' || col === 'Stage' ? 'left' : 'right',
                        color: 'var(--text-3)', fontWeight: 500, letterSpacing: '0.08em', textTransform: 'uppercase',
                        fontSize: 10, whiteSpace: 'nowrap', userSelect: 'none',
                        cursor: isSortable ? 'pointer' : 'default',
                        borderBottom: '1px solid var(--line-2)',
                      }}
                    >
                      {col}{isSortable && <SortIcon col={col === 'Cost Basis' ? 'Weight' : col === 'Mkt Cap' ? 'Market Cap' : col} />}
                    </th>
                  );
                })}
              </tr>
            </thead>
            <tbody>
              {results.map((h, i) => {
                const stage = STAGES.find(s => s.id === h.stage);
                const dayPct = parsePct(h.day);
                const pnl = ((h.price - h.cost) / h.cost) * 100;
                const isSelected = selected === h.ticker;
                return (
                  <tr
                    key={h.ticker}
                    onClick={() => setSelected(isSelected ? null : h.ticker)}
                    style={{
                      background: isSelected ? stage.color + '14' : i % 2 === 0 ? '#161b27' : '#1c2330',
                      borderBottom: '1px solid var(--line)',
                      cursor: 'pointer',
                      outline: isSelected ? `1px solid ${stage.color}44` : 'none',
                    }}
                  >
                    <td style={{ padding: '9px 12px', color: 'var(--text)', fontWeight: 600, letterSpacing: '0.04em', textAlign: 'left' }}>{h.ticker}</td>
                    <td style={{ padding: '9px 12px', color: 'var(--text-2)', fontFamily: 'var(--sans)', textAlign: 'left', whiteSpace: 'nowrap' }}>{h.name}</td>
                    <td style={{ padding: '9px 12px', textAlign: 'left' }}>
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
                        <span style={{ width: 6, height: 6, borderRadius: '50%', background: stage.color, flexShrink: 0 }}></span>
                        <span style={{ color: stage.color, fontSize: 10, letterSpacing: '0.06em' }}>{stage.name}</span>
                      </span>
                    </td>
                    <td style={{ padding: '9px 12px', color: 'var(--text)', textAlign: 'right' }}>${h.price.toFixed(2)}</td>
                    <td style={{ padding: '9px 12px', color: dayPct >= 0 ? '#4ade80' : '#f87171', textAlign: 'right', fontWeight: 600 }}>{h.day}</td>
                    <td style={{ padding: '9px 12px', color: 'var(--text-2)', textAlign: 'right' }}>{h.wgt}</td>
                    <td style={{ padding: '9px 12px', color: 'var(--text-3)', textAlign: 'right' }}>${h.cost.toFixed(2)}</td>
                    <td style={{ padding: '9px 12px', color: 'var(--text-2)', textAlign: 'right' }}>{h.mcap}</td>
                    <td style={{ padding: '9px 12px', color: pnl >= 0 ? '#4ade80' : '#f87171', textAlign: 'right', fontWeight: 600 }}>
                      {pnl >= 0 ? '+' : ''}{pnl.toFixed(1)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Summary row */}
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', borderTop: '1px solid var(--line)', fontFamily: 'var(--mono)', fontSize: 10, color: 'var(--text-3)', letterSpacing: '0.08em' }}>
          <span>{results.length} holdings · {stageFilter.size > 0 ? [...stageFilter].join(', ') : 'all stages'}</span>
          <span>Total weight: <span style={{ color: 'var(--text)' }}>{totalWeight.toFixed(1)}%</span></span>
        </div>
      </div>
    </div>
  );
}

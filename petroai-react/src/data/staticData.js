// Static seed data — matches design-reference/data.jsx
// Live data from Yahoo Finance overlays these values at runtime.

export const STAGES = [
  { id: 'energy',      n: '01', name: 'Energy',      color: '#e76f1c', desc: 'Hydrocarbons & uranium upstream', weight: 18.4, ret: '+12.4%', val: '$0.42B', flow: 82 },
  { id: 'power',       n: '02', name: 'Power',        color: '#f4d220', desc: 'Generation, reactors, baseload',  weight: 14.2, ret: '+8.7%',  val: '$0.32B', flow: 71 },
  { id: 'grid',        n: '03', name: 'Grid',         color: '#22d3ee', desc: 'T&D, transformers, interconnect', weight: 11.8, ret: '+18.1%', val: '$0.27B', flow: 65 },
  { id: 'compute',     n: '04', name: 'Compute',      color: '#3b82f6', desc: 'Datacenters, GPUs, HBM',          weight: 16.6, ret: '+24.3%', val: '$0.38B', flow: 92 },
  { id: 'transfer',    n: '05', name: 'Transfer',     color: '#4ade80', desc: 'Optical, networking, cooling',    weight:  8.9, ret: '+6.2%',  val: '$0.20B', flow: 58 },
  { id: 'ai',          n: '06', name: 'AI',           color: '#a855f7', desc: 'Frontier labs, model platforms',  weight: 13.1, ret: '+31.8%', val: '$0.30B', flow: 88 },
  { id: 'defense',     n: '07', name: 'Defense',      color: '#ef4444', desc: 'Autonomy, ISR, primes',           weight:  9.4, ret: '+14.6%', val: '$0.21B', flow: 67 },
  { id: 'sovereignty', n: '08', name: 'Sovereignty',  color: '#f59e0b', desc: 'Strategic metals, capital ctrls', weight:  7.6, ret: '+9.8%',  val: '$0.17B', flow: 54 },
];

export const HOLDINGS = [
  { ticker: 'XOM',   name: 'Exxon Mobil',         stage: 'energy',      pct: 4.2, price: 118.42,  day: '+1.8%',  wgt: '4.20%', cost:  96.10, mcap: '$472B',  img: 'oil'        },
  { ticker: 'CCJ',   name: 'Cameco Corp',          stage: 'energy',      pct: 3.1, price:  58.93,  day: '+2.4%',  wgt: '3.10%', cost:  41.20, mcap: '$25.4B', img: 'uranium'    },
  { ticker: 'VST',   name: 'Vistra Corp',          stage: 'power',       pct: 3.8, price: 167.21,  day: '+3.1%',  wgt: '3.80%', cost:  88.40, mcap: '$56.8B', img: 'reactor'    },
  { ticker: 'CEG',   name: 'Constellation Energy', stage: 'power',       pct: 3.4, price: 281.50,  day: '+1.6%',  wgt: '3.40%', cost: 198.20, mcap: '$88.2B', img: 'reactor'    },
  { ticker: 'GEV',   name: 'GE Vernova',           stage: 'grid',        pct: 3.2, price: 392.18,  day: '+2.9%',  wgt: '3.20%', cost: 215.40, mcap: '$108B',  img: 'grid'       },
  { ticker: 'ETN',   name: 'Eaton Corporation',    stage: 'grid',        pct: 2.8, price: 348.92,  day: '+1.2%',  wgt: '2.80%', cost: 268.10, mcap: '$138B',  img: 'grid'       },
  { ticker: 'NVDA',  name: 'NVIDIA',               stage: 'compute',     pct: 6.4, price: 1284.30, day: '+4.2%',  wgt: '6.40%', cost: 412.80, mcap: '$3.16T', img: 'chip'       },
  { ticker: 'AVGO',  name: 'Broadcom',             stage: 'compute',     pct: 3.9, price: 1748.20, day: '+2.7%',  wgt: '3.90%', cost: 982.40, mcap: '$816B',  img: 'chip'       },
  { ticker: 'CRWV',  name: 'CoreWeave',            stage: 'transfer',    pct: 2.1, price:   78.40, day: '+5.8%',  wgt: '2.10%', cost:  42.10, mcap: '$38.2B', img: 'datacenter' },
  { ticker: 'ANET',  name: 'Arista Networks',      stage: 'transfer',    pct: 2.4, price:  412.80, day: '+1.4%',  wgt: '2.40%', cost: 268.40, mcap: '$130B',  img: 'datacenter' },
  { ticker: 'MSFT',  name: 'Microsoft',            stage: 'ai',          pct: 4.8, price:  478.20, day: '+1.1%',  wgt: '4.80%', cost: 312.40, mcap: '$3.55T', img: 'ai'         },
  { ticker: 'PLTR',  name: 'Palantir',             stage: 'ai',          pct: 2.9, price:  142.80, day: '+3.4%',  wgt: '2.90%', cost:  28.40, mcap: '$320B',  img: 'ai'         },
  { ticker: 'LMT',   name: 'Lockheed Martin',      stage: 'defense',     pct: 3.2, price:  612.40, day: '+0.8%',  wgt: '3.20%', cost: 478.10, mcap: '$144B',  img: 'defense'    },
  { ticker: 'KTOS',  name: 'Kratos Defense',       stage: 'defense',     pct: 1.8, price:   38.20, day: '+4.2%',  wgt: '1.80%', cost:  18.40, mcap: '$5.8B',  img: 'defense'    },
  { ticker: 'MP',    name: 'MP Materials',         stage: 'sovereignty', pct: 2.4, price:   28.40, day: '+6.2%',  wgt: '2.40%', cost:  14.80, mcap: '$4.6B',  img: 'metals'     },
  { ticker: 'AEM',   name: 'Agnico Eagle Mines',   stage: 'sovereignty', pct: 2.1, price:   94.80, day: '+1.9%',  wgt: '2.10%', cost:  62.40, mcap: '$47.2B', img: 'metals'     },
];

export const INDICES = [
  { nm: 'PETROAI-100', px: '4,827.42', ch: '+62.18', pct: '+1.31%', dir: 'up'   },
  { nm: 'S&P 500',     px: '6,148.20', ch: '+24.80', pct: '+0.40%', dir: 'up'   },
  { nm: 'NDX',         px: '22,481.6', ch: '+128.4', pct: '+0.57%', dir: 'up'   },
  { nm: 'WTI',         px: '$78.42',   ch: '+1.84',  pct: '+2.40%', dir: 'up'   },
  { nm: 'URA',         px: '$38.92',   ch: '-0.42',  pct: '-1.07%', dir: 'down' },
  { nm: 'DXY',         px: '104.28',   ch: '-0.18',  pct: '-0.17%', dir: 'down' },
];

export const HEATMAP = [
  { sym: 'NVDA', stage: 'compute',     ch:  4.2 },
  { sym: 'AVGO', stage: 'compute',     ch:  2.7 },
  { sym: 'AMD',  stage: 'compute',     ch:  3.1 },
  { sym: 'TSM',  stage: 'compute',     ch:  1.8 },
  { sym: 'MSFT', stage: 'ai',          ch:  1.1 },
  { sym: 'GOOG', stage: 'ai',          ch:  0.8 },
  { sym: 'META', stage: 'ai',          ch: -0.4 },
  { sym: 'PLTR', stage: 'ai',          ch:  3.4 },
  { sym: 'XOM',  stage: 'energy',      ch:  1.8 },
  { sym: 'CVX',  stage: 'energy',      ch:  1.2 },
  { sym: 'CCJ',  stage: 'energy',      ch:  2.4 },
  { sym: 'OXY',  stage: 'energy',      ch: -0.6 },
  { sym: 'VST',  stage: 'power',       ch:  3.1 },
  { sym: 'CEG',  stage: 'power',       ch:  1.6 },
  { sym: 'NRG',  stage: 'power',       ch:  0.4 },
  { sym: 'TLN',  stage: 'power',       ch:  2.8 },
  { sym: 'GEV',  stage: 'grid',        ch:  2.9 },
  { sym: 'ETN',  stage: 'grid',        ch:  1.2 },
  { sym: 'PWR',  stage: 'grid',        ch:  0.6 },
  { sym: 'MMM',  stage: 'grid',        ch: -0.2 },
  { sym: 'ANET', stage: 'transfer',    ch:  1.4 },
  { sym: 'CRWV', stage: 'transfer',    ch:  5.8 },
  { sym: 'CSCO', stage: 'transfer',    ch:  0.3 },
  { sym: 'CIEN', stage: 'transfer',    ch:  2.1 },
  { sym: 'LMT',  stage: 'defense',     ch:  0.8 },
  { sym: 'KTOS', stage: 'defense',     ch:  4.2 },
  { sym: 'RTX',  stage: 'defense',     ch:  0.4 },
  { sym: 'AVAV', stage: 'defense',     ch:  2.6 },
  { sym: 'MP',   stage: 'sovereignty', ch:  6.2 },
  { sym: 'AEM',  stage: 'sovereignty', ch:  1.9 },
  { sym: 'TMC',  stage: 'sovereignty', ch:  3.8 },
  { sym: 'LAC',  stage: 'sovereignty', ch: -1.2 },
];

export const NEWS = [
  { time: '14:42', src: 'energy',      hl: 'Saudi Aramco signals output discipline through Q3; spot WTI gaps higher pre-open' },
  { time: '14:31', src: 'compute',     hl: 'NVIDIA confirms Blackwell Ultra shipping ahead of schedule; supply-chain checks confirm 1.4M units H2' },
  { time: '14:18', src: 'power',       hl: 'Vistra–Microsoft 1.6GW PPA expanded with co-located SMR option, structure favors VST capex' },
  { time: '13:55', src: 'sovereignty', hl: 'Treasury floats expanded outbound investment review on rare earths; MP Materials breaks 30-day base' },
  { time: '13:41', src: 'defense',     hl: 'House mark adds $4.2B for autonomous undersea program; KTOS, AVAV named recipients' },
  { time: '13:22', src: 'ai',          hl: 'Frontier model spend now tracking $312B for FY26 across hyperscalers — Morgan Stanley desk note' },
];

export const SIGNALS = [
  { stage: 'energy',      lbl: 'Crude term structure',  sub: 'Backwardation steepening at front',  val: '+218bps'   },
  { stage: 'compute',     lbl: 'HBM utilization',       sub: 'Samsung + SK Hynix fab loading',     val: '94.2%'     },
  { stage: 'power',       lbl: 'PJM forward strip',     sub: '2027 capacity auction clear',        val: '$329/MW-d' },
  { stage: 'grid',        lbl: 'Transformer lead time', sub: 'GSU 500MVA+',                        val: '142 wks'   },
  { stage: 'ai',          lbl: 'Tokens / wafer-out',    sub: 'Frontier inference cost',            val: '$0.038'    },
  { stage: 'defense',     lbl: 'FY26 budget velocity',  sub: 'Procurement obligations YoY',        val: '+11.4%'    },
  { stage: 'sovereignty', lbl: 'NdPr oxide premium',    sub: 'Ex-China vs CN spot',                val: '+34.8%'    },
];

export const FLOWS = [
  { stage: 'energy',      lbl: 'Energy',   flow: 82 },
  { stage: 'power',       lbl: 'Power',    flow: 71 },
  { stage: 'grid',        lbl: 'Grid',     flow: 65 },
  { stage: 'compute',     lbl: 'Compute',  flow: 92 },
  { stage: 'transfer',    lbl: 'Transfer', flow: 58 },
  { stage: 'ai',          lbl: 'AI',       flow: 88 },
  { stage: 'defense',     lbl: 'Defense',  flow: 67 },
  { stage: 'sovereignty', lbl: 'Sovrgn',   flow: 54 },
];

export const TICKER = [
  ['PETROAI', '4827.42', 'up',   '+1.31%'],
  ['NVDA',    '1284.30', 'up',   '+4.21%'],
  ['XOM',     '118.42',  'up',   '+1.82%'],
  ['VST',     '167.21',  'up',   '+3.10%'],
  ['CCJ',     '58.93',   'up',   '+2.41%'],
  ['MSFT',    '478.20',  'up',   '+1.12%'],
  ['PLTR',    '142.80',  'up',   '+3.41%'],
  ['MP',      '28.40',   'up',   '+6.21%'],
  ['LMT',     '612.40',  'up',   '+0.81%'],
  ['CEG',     '281.50',  'up',   '+1.62%'],
  ['GEV',     '392.18',  'up',   '+2.91%'],
  ['ANET',    '412.80',  'up',   '+1.42%'],
  ['KTOS',    '38.20',   'up',   '+4.21%'],
  ['AEM',     '94.80',   'up',   '+1.91%'],
  ['CRWV',    '78.40',   'up',   '+5.81%'],
  ['WTI',     '78.42',   'up',   '+2.40%'],
  ['URA',     '38.92',   'down', '-1.07%'],
  ['DXY',     '104.28',  'down', '-0.17%'],
];

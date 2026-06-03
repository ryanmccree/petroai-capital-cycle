// Static seed data — live Yahoo Finance overlays these values at runtime.

export const STAGES = [
  { id: 'energy',      n: '01', name: 'Energy',      color: '#e76f1c', desc: 'Hydrocarbons, uranium, nuclear upstream',            weight: 18.4, ret: '+12.4%', val: '$0.42B', flow: 82 },
  { id: 'power',       n: '02', name: 'Power',        color: '#f4d220', desc: 'Generation, reactors, baseload, cooling',            weight: 14.2, ret: '+8.7%',  val: '$0.32B', flow: 71 },
  { id: 'grid',        n: '03', name: 'Grid',         color: '#22d3ee', desc: 'T&D, transformers, fiber, physical buildout',        weight: 11.8, ret: '+18.1%', val: '$0.27B', flow: 65 },
  { id: 'compute',     n: '04', name: 'Compute',      color: '#3b82f6', desc: 'Datacenters, GPUs, HBM, servers, packaging',         weight: 16.6, ret: '+24.3%', val: '$0.38B', flow: 92 },
  { id: 'transfer',    n: '05', name: 'Transfer',     color: '#4ade80', desc: 'Optical, networking, optics, storage, interconnects', weight:  8.9, ret: '+6.2%',  val: '$0.20B', flow: 58 },
  { id: 'ai',          n: '06', name: 'AI',           color: '#a855f7', desc: 'Frontier labs, inference, model platforms',          weight: 13.1, ret: '+31.8%', val: '$0.30B', flow: 88 },
  { id: 'defense',     n: '07', name: 'Defense',      color: '#ef4444', desc: 'Autonomy, ISR, primes, cyber',                       weight:  9.4, ret: '+14.6%', val: '$0.21B', flow: 67 },
  { id: 'sovereignty', n: '08', name: 'Sovereignty',  color: '#f59e0b', desc: 'Strategic metals, rare earth, capital controls',     weight:  7.6, ret: '+9.8%',  val: '$0.17B', flow: 54 },
];

export const HOLDINGS = [
  // ── Energy ──
  { ticker: 'XOM',   name: 'Exxon Mobil',               stage: 'energy',      pct: 4.2, price: 118.42,  day: '+1.8%',  wgt: '4.20%', cost:  96.10, mcap: '$472B',  img: 'oil'        },
  { ticker: 'CCJ',   name: 'Cameco Corp',                stage: 'energy',      pct: 3.1, price:  58.93,  day: '+2.4%',  wgt: '3.10%', cost:  41.20, mcap: '$25.4B', img: 'uranium'    },
  // ── Power + Cooling ──
  { ticker: 'VST',   name: 'Vistra Corp',                stage: 'power',       pct: 3.8, price: 167.21,  day: '+3.1%',  wgt: '3.80%', cost:  88.40, mcap: '$56.8B', img: 'reactor'    },
  { ticker: 'CEG',   name: 'Constellation Energy',       stage: 'power',       pct: 3.4, price: 281.50,  day: '+1.6%',  wgt: '3.40%', cost: 198.20, mcap: '$88.2B', img: 'reactor'    },
  { ticker: 'VRT',   name: 'Vertiv Holdings',            stage: 'power',       pct: 2.4, price:  92.40,  day: '+2.2%',  wgt: '2.40%', cost:  62.00, mcap: '$32.8B', img: 'reactor'    },
  // ── Grid + Physical Buildout ──
  { ticker: 'GEV',   name: 'GE Vernova',                 stage: 'grid',        pct: 3.2, price: 392.18,  day: '+2.9%',  wgt: '3.20%', cost: 215.40, mcap: '$108B',  img: 'grid'       },
  { ticker: 'ETN',   name: 'Eaton Corporation',          stage: 'grid',        pct: 2.8, price: 348.92,  day: '+1.2%',  wgt: '2.80%', cost: 268.10, mcap: '$138B',  img: 'grid'       },
  { ticker: 'DY',    name: 'Dycom Industries',           stage: 'grid',        pct: 1.4, price: 188.40,  day: '+1.4%',  wgt: '1.40%', cost: 142.80, mcap: '$6.8B',  img: 'grid'       },
  // ── Compute (AI Server Layer) ──
  { ticker: 'NVDA',  name: 'NVIDIA',                     stage: 'compute',     pct: 6.4, price: 1284.30, day: '+4.2%',  wgt: '6.40%', cost: 412.80, mcap: '$3.16T', img: 'chip'       },
  { ticker: 'ARM',   name: 'Arm Holdings',               stage: 'compute',     pct: 2.2, price: 182.40,  day: '+1.4%',  wgt: '2.20%', cost: 124.00, mcap: '$148B',  img: 'chip'       },
  { ticker: 'AMKR',  name: 'Amkor Technology',           stage: 'compute',     pct: 1.4, price:  24.80,  day: '+0.8%',  wgt: '1.40%', cost:  18.20, mcap: '$6.2B',  img: 'chip'       },
  { ticker: 'HPE',   name: 'Hewlett Packard Enterprise', stage: 'compute',     pct: 1.8, price:  22.40,  day: '+2.1%',  wgt: '1.80%', cost:  16.80, mcap: '$32.4B', img: 'datacenter' },
  { ticker: 'DELL',  name: 'Dell Technologies',          stage: 'compute',     pct: 1.6, price: 128.40,  day: '+1.8%',  wgt: '1.60%', cost:  92.40, mcap: '$48.2B', img: 'datacenter' },
  { ticker: 'SMCI',  name: 'Super Micro Computer',       stage: 'compute',     pct: 1.4, price:  48.20,  day: '+3.4%',  wgt: '1.40%', cost:  28.40, mcap: '$22.8B', img: 'chip'       },
  { ticker: 'CAMT',  name: 'Camtek',                     stage: 'compute',     pct: 0.9, price:  68.40,  day: '+1.2%',  wgt: '0.90%', cost:  48.20, mcap: '$2.8B',  img: 'chip'       },
  { ticker: 'GFS',   name: 'GlobalFoundries',            stage: 'compute',     pct: 1.6, price:  28.40,  day: '+0.8%',  wgt: '1.60%', cost:  22.40, mcap: '$12.4B', img: 'chip'       },
  // ── Transfer (Networking + Optics + Storage) ──
  { ticker: 'AVGO',  name: 'Broadcom',                   stage: 'transfer',    pct: 3.9, price: 1748.20, day: '+2.7%',  wgt: '3.90%', cost: 982.40, mcap: '$816B',  img: 'chip'       },
  { ticker: 'MRVL',  name: 'Marvell Technology',         stage: 'transfer',    pct: 2.1, price:  94.20,  day: '+21.8%', wgt: '2.10%', cost:  58.40, mcap: '$58.4B', img: 'networking' },
  { ticker: 'CRDO',  name: 'Credo Technology',           stage: 'transfer',    pct: 1.8, price:  42.80,  day: '+8.4%',  wgt: '1.80%', cost:  22.10, mcap: '$8.2B',  img: 'networking' },
  { ticker: 'ANET',  name: 'Arista Networks',            stage: 'transfer',    pct: 2.4, price: 412.80,  day: '+1.4%',  wgt: '2.40%', cost: 268.40, mcap: '$130B',  img: 'datacenter' },
  { ticker: 'CRWV',  name: 'CoreWeave',                  stage: 'transfer',    pct: 2.1, price:  78.40,  day: '+5.8%',  wgt: '2.10%', cost:  42.10, mcap: '$38.2B', img: 'datacenter' },
  { ticker: 'GLW',   name: 'Corning',                    stage: 'transfer',    pct: 1.8, price:  52.40,  day: '+2.2%',  wgt: '1.80%', cost:  38.20, mcap: '$38.2B', img: 'optics'     },
  { ticker: 'LITE',  name: 'Lumentum Holdings',          stage: 'transfer',    pct: 1.6, price:  68.20,  day: '+3.8%',  wgt: '1.60%', cost:  42.80, mcap: '$4.1B',  img: 'optics'     },
  { ticker: 'PSTG',  name: 'Pure Storage',               stage: 'transfer',    pct: 1.5, price:  62.40,  day: '+1.2%',  wgt: '1.50%', cost:  38.80, mcap: '$18.4B', img: 'datacenter' },
  { ticker: 'NTAP',  name: 'NetApp',                     stage: 'transfer',    pct: 1.2, price: 118.60,  day: '+0.9%',  wgt: '1.20%', cost:  82.40, mcap: '$22.1B', img: 'datacenter' },
  { ticker: 'STX',   name: 'Seagate Technology',         stage: 'transfer',    pct: 1.2, price:  98.40,  day: '+1.6%',  wgt: '1.20%', cost:  72.40, mcap: '$18.4B', img: 'datacenter' },
  { ticker: 'POET',  name: 'POET Technologies',          stage: 'transfer',    pct: 0.8, price:   8.20,  day: '+2.8%',  wgt: '0.80%', cost:   4.80, mcap: '$0.4B',  img: 'optics'     },
  // ── AI Platform ──
  { ticker: 'MSFT',  name: 'Microsoft',                  stage: 'ai',          pct: 4.8, price: 478.20,  day: '+1.1%',  wgt: '4.80%', cost: 312.40, mcap: '$3.55T', img: 'ai'         },
  { ticker: 'PLTR',  name: 'Palantir',                   stage: 'ai',          pct: 2.9, price: 142.80,  day: '+3.4%',  wgt: '2.90%', cost:  28.40, mcap: '$320B',  img: 'ai'         },
  { ticker: 'ORCL',  name: 'Oracle Corporation',         stage: 'ai',          pct: 2.1, price: 182.40,  day: '-0.8%',  wgt: '2.10%', cost: 142.40, mcap: '$412B',  img: 'ai'         },
  // ── Defense ──
  { ticker: 'LMT',   name: 'Lockheed Martin',            stage: 'defense',     pct: 3.2, price: 612.40,  day: '+0.8%',  wgt: '3.20%', cost: 478.10, mcap: '$144B',  img: 'defense'    },
  { ticker: 'KTOS',  name: 'Kratos Defense',             stage: 'defense',     pct: 1.8, price:  38.20,  day: '+4.2%',  wgt: '1.80%', cost:  18.40, mcap: '$5.8B',  img: 'defense'    },
  // ── Sovereignty ──
  { ticker: 'MP',    name: 'MP Materials',               stage: 'sovereignty', pct: 2.4, price:  28.40,  day: '+6.2%',  wgt: '2.40%', cost:  14.80, mcap: '$4.6B',  img: 'metals'     },
  { ticker: 'AEM',   name: 'Agnico Eagle Mines',         stage: 'sovereignty', pct: 2.1, price:  94.80,  day: '+1.9%',  wgt: '2.10%', cost:  62.40, mcap: '$47.2B', img: 'metals'     },
  { ticker: 'AA',    name: 'Alcoa Corporation',          stage: 'sovereignty', pct: 1.2, price:  34.80,  day: '+0.9%',  wgt: '1.20%', cost:  24.40, mcap: '$8.4B',  img: 'metals'     },
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
  // Compute
  { sym: 'NVDA',  stage: 'compute',     ch:  4.2 },
  { sym: 'ARM',   stage: 'compute',     ch:  1.4 },
  { sym: 'HPE',   stage: 'compute',     ch:  2.1 },
  { sym: 'DELL',  stage: 'compute',     ch:  1.8 },
  { sym: 'SMCI',  stage: 'compute',     ch:  3.4 },
  { sym: 'AMD',   stage: 'compute',     ch:  3.1 },
  // AI
  { sym: 'MSFT',  stage: 'ai',          ch:  1.1 },
  { sym: 'ORCL',  stage: 'ai',          ch: -0.8 },
  { sym: 'META',  stage: 'ai',          ch: -0.4 },
  { sym: 'PLTR',  stage: 'ai',          ch:  3.4 },
  // Energy
  { sym: 'XOM',   stage: 'energy',      ch:  1.8 },
  { sym: 'CVX',   stage: 'energy',      ch:  1.2 },
  { sym: 'CCJ',   stage: 'energy',      ch:  2.4 },
  { sym: 'OXY',   stage: 'energy',      ch: -0.6 },
  // Power
  { sym: 'VST',   stage: 'power',       ch:  3.1 },
  { sym: 'CEG',   stage: 'power',       ch:  1.6 },
  { sym: 'VRT',   stage: 'power',       ch:  2.2 },
  { sym: 'TLN',   stage: 'power',       ch:  2.8 },
  // Grid
  { sym: 'GEV',   stage: 'grid',        ch:  2.9 },
  { sym: 'ETN',   stage: 'grid',        ch:  1.2 },
  { sym: 'DY',    stage: 'grid',        ch:  1.4 },
  { sym: 'PWR',   stage: 'grid',        ch:  0.6 },
  // Transfer
  { sym: 'MRVL',  stage: 'transfer',    ch: 21.8 },
  { sym: 'CRDO',  stage: 'transfer',    ch:  8.4 },
  { sym: 'AVGO',  stage: 'transfer',    ch:  2.7 },
  { sym: 'GLW',   stage: 'transfer',    ch:  2.2 },
  { sym: 'ANET',  stage: 'transfer',    ch:  1.4 },
  { sym: 'CRWV',  stage: 'transfer',    ch:  5.8 },
  // Defense
  { sym: 'LMT',   stage: 'defense',     ch:  0.8 },
  { sym: 'KTOS',  stage: 'defense',     ch:  4.2 },
  { sym: 'RTX',   stage: 'defense',     ch:  0.4 },
  { sym: 'AVAV',  stage: 'defense',     ch:  2.6 },
  // Sovereignty
  { sym: 'MP',    stage: 'sovereignty', ch:  6.2 },
  { sym: 'AEM',   stage: 'sovereignty', ch:  1.9 },
  { sym: 'AA',    stage: 'sovereignty', ch:  0.9 },
  { sym: 'TMC',   stage: 'sovereignty', ch:  3.8 },
];

export const NEWS = [
  { time: '14:42', src: 'transfer',    hl: 'Jensen Huang calls $MRVL next trillion-dollar company on CNBC; AI factory networking chain reprices across the board' },
  { time: '14:31', src: 'compute',     hl: 'NVIDIA confirms Blackwell Ultra shipping ahead of schedule; $145B supply commitment locks AI factory chain through 2027' },
  { time: '14:18', src: 'power',       hl: 'Vistra–Microsoft 1.6GW PPA expanded with co-located SMR option; VRT confirms AI data center cooling demand +38% YoY' },
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
  { stage: 'transfer',    lbl: 'Transfer', flow: 88 },
  { stage: 'ai',          lbl: 'AI',       flow: 88 },
  { stage: 'defense',     lbl: 'Defense',  flow: 67 },
  { stage: 'sovereignty', lbl: 'Sovrgn',   flow: 54 },
];

export const TICKER = [
  ['PETROAI', '4827.42', 'up',   '+1.31%'],
  ['NVDA',    '1284.30', 'up',   '+4.21%'],
  ['MRVL',    '94.20',   'up',   '+21.8%'],
  ['CRDO',    '42.80',   'up',   '+8.41%'],
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
  ['AVGO',    '1748.20', 'up',   '+2.71%'],
  ['KTOS',    '38.20',   'up',   '+4.21%'],
  ['AEM',     '94.80',   'up',   '+1.91%'],
  ['CRWV',    '78.40',   'up',   '+5.81%'],
  ['VRT',     '92.40',   'up',   '+2.21%'],
  ['ARM',     '182.40',  'up',   '+1.41%'],
  ['GLW',     '52.40',   'up',   '+2.21%'],
  ['LITE',    '68.20',   'up',   '+3.81%'],
  ['HPE',     '22.40',   'up',   '+2.11%'],
  ['DELL',    '128.40',  'up',   '+1.81%'],
  ['SMCI',    '48.20',   'up',   '+3.41%'],
  ['AMKR',    '24.80',   'up',   '+0.81%'],
  ['PSTG',    '62.40',   'up',   '+1.21%'],
  ['NTAP',    '118.60',  'up',   '+0.91%'],
  ['STX',     '98.40',   'up',   '+1.61%'],
  ['DY',      '188.40',  'up',   '+1.41%'],
  ['POET',    '8.20',    'up',   '+2.81%'],
  ['GFS',     '28.40',   'up',   '+0.81%'],
  ['CAMT',    '68.40',   'up',   '+1.21%'],
  ['ORCL',    '182.40',  'down', '-0.81%'],
  ['AA',      '34.80',   'up',   '+0.91%'],
  ['WTI',     '78.42',   'up',   '+2.40%'],
  ['URA',     '38.92',   'down', '-1.07%'],
  ['DXY',     '104.28',  'down', '-0.17%'],
];

export const THESIS_NOTE = {
  title: 'The AI Factory Framework',
  source: '@mikalche',
  date: 'May 2026',
  headline: 'Customers do not buy GPUs. They build AI factories.',
  body: 'Everyone is focused on the headline beat. But the real signal from $NVDA was much bigger. That one line changes the whole framework. This is no longer just about $NVDA, $AMD, semis, or GPUs. The next leg of the AI trade is the full physical stack required to build intelligence at scale: Networking, Optics, Fiber, Power, Cooling, Storage, Packaging, Physical infrastructure. $NVDA Data Center networking revenue was roughly $15B and nearly tripled year over year. Spectrum-X is now larger than all Ethernet network peers combined. That confirms networking is one of the fastest-growing bottlenecks in the AI factory stack. The biggest capstone was the $145B supply commitment — $NVDA is not just talking about demand. They are locking up supply across the chain.',
  tiers: [
    { label: 'Tier 1 — Named / direct $NVDA read-through',   tickers: ['CRDO', 'LITE', 'COHR', 'GLW', 'MRVL'], desc: 'AI connectivity, strategic optics partners, optical fiber' },
    { label: 'Tier 2 — Structural AI factory read-through',  tickers: ['VRT', 'AMKR', 'ARM'],                  desc: 'Power + cooling, advanced packaging, custom CPU' },
    { label: 'Tier 3 — Next-leg AI factory stack',           tickers: ['PSTG', 'NTAP'],                        desc: 'Accelerated storage infrastructure for agentic AI factories' },
  ],
  conclusion: 'The market already understands GPUs. Now it has to understand the factory. AI is not just software anymore. AI is infrastructure. And infrastructure needs builders, power, cooling, fiber, optics, networking, storage & packaging.',
  framework: 'Tier 1 → direct NVDA named partners. Tier 2 → structural AI factory plays. Tier 3 → next-leg agentic AI stack.',
};

export const THESIS_NOTE_2 = {
  title: 'Jensen Lights the Fuse on the AI Factory Chain',
  source: '@mikalche',
  date: 'June 2026',
  headline: '🚨 JENSEN JUST DROPPED A BOMB — $MRVL +21.8% AND THE ENTIRE AI FACTORY CHAIN IS REPRICING',
  body: 'This is not a normal sympathy move. This is Jensen Huang publicly validating the next layer of the AI trade. He just called $MRVL the next trillion-dollar company on CNBC. $MRVL sits directly inside the AI factory networking / custom silicon / silicon photonics layer. The next AI trade is not just GPUs. It is the factory. And today, Jensen just lit the fuse on the entire AI factory chain.',
  chain: [
    { ticker: 'MRVL', note: 'Custom silicon / networking — Jensen endorsed as next trillion-dollar company' },
    { ticker: 'CRDO', note: 'AI connectivity — thesis confirmed, Jensen validated the entire lane' },
    { ticker: 'AVGO', note: 'Custom silicon / networking peer — June 12 earnings catalyst' },
    { ticker: 'COHR', note: 'Optical interconnects — through $360 target, now ~$380' },
    { ticker: 'LITE', note: 'Optics / photonics — AI factory bandwidth bottleneck beneficiary' },
    { ticker: 'GLW',  note: 'Fiber / optical infrastructure — AI factory chain confirmed' },
    { ticker: 'POET', note: 'Optical / photonics sympathy — silicon photonics exposure' },
    { ticker: 'HPE',  note: 'AI server demand confirmed +25.9%' },
    { ticker: 'DELL', note: 'AI infrastructure demand confirmed' },
    { ticker: 'SMCI', note: 'AI server assembly — physical AI factory layer' },
    { ticker: 'VRT',  note: 'Power and cooling — physical backbone of AI factory' },
    { ticker: 'STX',  note: 'Storage sympathy — memory and storage layer' },
    { ticker: 'NTAP', note: 'Next-leg AI factory storage' },
    { ticker: 'PSTG', note: 'Accelerated storage for agentic AI factories' },
    { ticker: 'DY',   note: 'Physical buildout — fiber and grid infrastructure contractor' },
    { ticker: 'ARM',  note: 'Architecture layer — green on MRVL catalyst' },
    { ticker: 'MU',   note: 'Memory sympathy — storage layer moving' },
  ],
  losers: [
    { ticker: 'ORCL', note: 'Down ~4% on rotation — money moving from cloud/software INTO physical AI infrastructure. June 10 earnings setup may be asymmetric: $57M+ in $220C July calls, very little put activity. Lower price + same AI thesis = better risk/reward.' },
    { ticker: 'AMD',  note: 'Red — Jensen endorsing MRVL custom silicon lane is not great for general-purpose GPU competition narrative.' },
    { ticker: 'INTC', note: 'Red — inverse sympathy. Market rewarding modern AI factory stack, not legacy turnaround names.' },
  ],
  stackOrder: ['Servers', 'Networking', 'Optics', 'Power', 'Cooling', 'Storage', 'Infrastructure'],
  conclusion: 'The PetroAI Capital Cycle thesis is being validated in real time. First $DELL confirmed AI server demand. Then $HPE confirmed AI infrastructure demand. Now Jensen confirmed $MRVL as a possible trillion-dollar custom silicon / networking winner. The chain is clear. The next AI trade is not just chips. It is the factory.',
};

export const NVDA_TIERS = {
  tier1:     { label: 'Tier 1 — Named / Direct NVDA Read-Through',     color: '#e76f1c', desc: 'Directly named by Jensen Huang as strategic partners',      tickers: ['CRDO', 'LITE', 'COHR', 'GLW', 'MRVL'] },
  tier2:     { label: 'Tier 2 — Structural AI Factory Read-Through',   color: '#3b82f6', desc: 'Structural beneficiaries of AI factory buildout',           tickers: ['VRT', 'AMKR', 'ARM', 'GFS'] },
  tier3:     { label: 'Tier 3 — Next-Leg AI Factory Stack',            color: '#a855f7', desc: 'Next leg storage and infrastructure plays',                 tickers: ['PSTG', 'NTAP'] },
  confirmed: { label: 'Jensen Catalyst — AI Factory Chain Confirmed',  color: '#4ade80', desc: 'Moving on Jensen MRVL endorsement',                         tickers: ['HPE', 'DELL', 'SMCI', 'AVGO', 'POET', 'CAMT', 'STX', 'DY'] },
};

path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Zeitraumfilter-UI oben auf der Stats-Seite einfuegen
old_stats_page = '''    <div class="page" id="page-stats">
      <div class="panel">
        <div class="panel-title">Monatliche Entwicklung</div>'''

new_stats_page = '''    <div class="page" id="page-stats">
      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;align-items:center;gap:0.75rem;flex-wrap:wrap">
          <span style="font-size:0.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:0.1rem">Zeitraum</span>
          <input class="form-input" type="date" id="stats-from" style="max-width:160px" onchange="loadStats()">
          <span style="color:var(--muted);font-size:0.85rem">bis</span>
          <input class="form-input" type="date" id="stats-to" style="max-width:160px" onchange="loadStats()">
          <button class="btn btn-ghost btn-sm" onclick="resetStatsFilter()">Alle</button>
        </div>
      </div>
      <div class="panel">
        <div class="panel-title">Monatliche Entwicklung</div>'''

c = c.replace(old_stats_page, new_stats_page, 1)

# 2. resetStatsFilter Funktion + loadStats anpassen
old_loadstats = '''async function loadStats() {
  const [sum,monthly,ts]=await Promise.all([api('/stats/summary'),api('/stats/monthly'),api('/stats/tournaments')]);'''

new_loadstats = '''function resetStatsFilter() {
  document.getElementById('stats-from').value = '';
  document.getElementById('stats-to').value = '';
  loadStats();
}

async function loadStats() {
  const from = document.getElementById('stats-from')?.value || '';
  const to = document.getElementById('stats-to')?.value || '';

  // Filtere allSessions clientseitig
  let filtered = allSessions;
  if (from) filtered = filtered.filter(s => s.date >= from);
  if (to)   filtered = filtered.filter(s => s.date <= to);

  // Stats lokal berechnen statt API
  const sum = calcSummary(filtered);
  const monthly = calcMonthly(filtered);
  const [ts] = await Promise.all([api('/stats/tournaments')]);'''

c = c.replace(old_loadstats, new_loadstats, 1)

# 3. calcSummary und calcMonthly Hilfsfunktionen vor loadStats einfuegen
helper = '''
function calcSummary(sessions) {
  if (!sessions.length) return {total_sessions:0,total_profit:0,total_buy_in:0,win_rate:0,roi:0,avg_profit_per_session:0,total_hours:0,profit_per_hour:0,biggest_win:0,biggest_loss:0,current_streak:0};
  const profits = sessions.map(s => s.profit);
  const total_profit = profits.reduce((a,b)=>a+b,0);
  const total_buy_in = sessions.reduce((a,s)=>a+s.buy_in,0);
  const wins = profits.filter(p=>p>0);
  const total_minutes = sessions.reduce((a,s)=>a+(s.duration_minutes||0),0);
  const total_hours = total_minutes/60;
  const sorted = [...sessions].sort((a,b)=>b.date.localeCompare(a.date)).map(s=>s.profit);
  let streak=0;
  if(sorted.length){const sign=sorted[0]>=0?1:-1;for(const p of sorted){if((p>=0&&sign===1)||(p<0&&sign===-1))streak+=sign;else break;}}
  return {
    total_sessions: sessions.length,
    total_profit: Math.round(total_profit*100)/100,
    total_buy_in: Math.round(total_buy_in*100)/100,
    win_rate: Math.round(wins.length/sessions.length*1000)/10,
    roi: total_buy_in>0?Math.round(total_profit/total_buy_in*1000)/10:0,
    avg_profit_per_session: Math.round(total_profit/sessions.length*100)/100,
    total_hours: Math.round(total_hours*10)/10,
    profit_per_hour: total_hours>0?Math.round(total_profit/total_hours*100)/100:0,
    biggest_win: Math.round(Math.max(...profits)*100)/100,
    biggest_loss: Math.round(Math.min(...profits)*100)/100,
    current_streak: streak,
  };
}

function calcMonthly(sessions) {
  const m = {};
  for (const s of sessions) {
    const key = s.date.slice(0,7);
    if (!m[key]) m[key] = {profit:0,sessions:0,buy_in:0};
    m[key].profit += s.profit;
    m[key].sessions++;
    m[key].buy_in += s.buy_in;
  }
  return Object.entries(m).sort().map(([month,v])=>({month,...v}));
}

'''

c = c.replace('function resetStatsFilter()', helper + 'function resetStatsFilter()', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

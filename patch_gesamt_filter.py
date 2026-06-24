path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old_fn = '''// ── GESAMT ──
function resetGesamtFilter(){document.getElementById('gesamt-from').value='';document.getElementById('gesamt-to').value='';loadGesamt();}

async function loadGesamt(){
  const from=document.getElementById('gesamt-from')?.value||'';
  const to=document.getElementById('gesamt-to')?.value||'';

  // Cash clientseitig filtern
  let filteredSessions=allSessions;
  if(from)filteredSessions=filteredSessions.filter(s=>s.date>=from);
  if(to)filteredSessions=filteredSessions.filter(s=>s.date<=to);

  const cashProfit=filteredSessions.reduce((a,s)=>a+s.profit,0);
  const cashInvested=filteredSessions.reduce((a,s)=>a+s.buy_in,0);
  const cashHours=filteredSessions.reduce((a,s)=>a+(s.duration_minutes||0),0)/60;

  // Turnierdaten vom Server
  const combined=await api('/stats/combined');

  // Turnierdaten ebenfalls filtern
  let tMonthly=combined.monthly;
  if(from||to) tMonthly=tMonthly.filter(m=>(!from||m.month>=from.slice(0,7))&&(!to||m.month<=to.slice(0,7)));

  const tProfit=tMonthly.reduce((a,m)=>a+m.tournament_profit,0);
  const tInvested=combined.tournament_invested;

  const totalProfit=cashProfit+tProfit;
  const totalInvested=cashInvested+tInvested;
  const roi=totalInvested>0?Math.round(totalProfit/totalInvested*1000)/10:0;

  const cls=v=>v>0?'pos':v<0?'neg':'neutral';
  setVal('g-total','$'+(totalProfit>=0?'+':'')+totalProfit.toFixed(0),cls(totalProfit));
  setVal('g-cash','$'+(cashProfit>=0?'+':'')+cashProfit.toFixed(0),cls(cashProfit));
  setVal('g-tourney','$'+(tProfit>=0?'+':'')+tProfit.toFixed(0),cls(tProfit));
  setVal('g-invested','$'+totalInvested.toFixed(0),'neutral');
  setVal('g-roi',roi+'%',cls(roi));
  setVal('g-hours',cashHours.toFixed(1)+'h','neutral');
  setVal('g-sessions',filteredSessions.length,'neutral');
  setVal('g-tournaments',combined.total_tournaments,'neutral');

  // Kombiniertes Monatsdiagramm
  const cashMonthly=calcMonthly(filteredSessions);
  const allMonths=[...new Set([...cashMonthly.map(m=>m.month),...tMonthly.map(m=>m.month)])].sort();
  const combined_monthly=allMonths.map(month=>({
    month,
    cash_profit:cashMonthly.find(m=>m.month===month)?.profit||0,
    tournament_profit:tMonthly.find(m=>m.month===month)?.tournament_profit||0,
  }));
  drawCombinedChart('gesamt-chart',combined_monthly);
}'''

new_fn = '''// ── GESAMT ──
function resetGesamtFilter(){document.getElementById('gesamt-from').value='';document.getElementById('gesamt-to').value='';loadGesamt();}

async function loadGesamt(){
  const from=document.getElementById('gesamt-from')?.value||'';
  const to=document.getElementById('gesamt-to')?.value||'';
  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';

  // Alle Daten vom Server holen
  const combined=await api('/stats/combined');

  // Monatsdaten filtern
  let monthly=combined.monthly;
  if(fromMonth) monthly=monthly.filter(m=>m.month>=fromMonth);
  if(toMonth) monthly=monthly.filter(m=>m.month<=toMonth);

  // Alles aus den monatlichen Daten berechnen
  const cashProfit=monthly.reduce((a,m)=>a+m.cash_profit,0);
  const cashInvested=monthly.reduce((a,m)=>a+m.cash_invested,0);
  const cashSessions=monthly.reduce((a,m)=>a+m.cash_sessions,0);
  const tProfit=monthly.reduce((a,m)=>a+m.tournament_profit,0);
  const tInvested=monthly.reduce((a,m)=>a+m.tournament_invested,0);
  const tCount=monthly.reduce((a,m)=>a+m.tournament_count,0);
  const totalProfit=cashProfit+tProfit;
  const totalInvested=cashInvested+tInvested;
  const roi=totalInvested>0?Math.round(totalProfit/totalInvested*1000)/10:0;

  // Stunden aus allSessions (clientseitig filtern)
  let filteredSessions=allSessions;
  if(from) filteredSessions=filteredSessions.filter(s=>s.date>=from);
  if(to) filteredSessions=filteredSessions.filter(s=>s.date<=to);
  const cashHours=filteredSessions.reduce((a,s)=>a+(s.duration_minutes||0),0)/60;

  const cls=v=>v>0?'pos':v<0?'neg':'neutral';
  setVal('g-total','$'+(totalProfit>=0?'+':'')+totalProfit.toFixed(0),cls(totalProfit));
  setVal('g-cash','$'+(cashProfit>=0?'+':'')+cashProfit.toFixed(0),cls(cashProfit));
  setVal('g-tourney','$'+(tProfit>=0?'+':'')+tProfit.toFixed(0),cls(tProfit));
  setVal('g-invested','$'+totalInvested.toFixed(0),'neutral');
  setVal('g-roi',roi+'%',cls(roi));
  setVal('g-hours',cashHours.toFixed(1)+'h','neutral');
  setVal('g-sessions',cashSessions,'neutral');
  setVal('g-tournaments',tCount,'neutral');

  // Kombiniertes Monatsdiagramm
  drawCombinedChart('gesamt-chart',monthly);
}'''

if old_fn in c:
    c = c.replace(old_fn, new_fn, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('patched')
else:
    print('NOT FOUND')

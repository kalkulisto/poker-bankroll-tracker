path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Nav: Statistiken -> Turnier-Stats, + Gesamt
old_nav = '''    <nav>
      <button class="nav-btn active" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Statistiken</button>
    </nav>'''

new_nav = '''    <nav>
      <button class="nav-btn active" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Turnier-Stats</button>
      <button class="nav-btn" onclick="showPage('gesamt')">Gesamt</button>
    </nav>'''

c = c.replace(old_nav, new_nav, 1)

# 2. Mobile CSS: 6 Items in 2 Reihen (3+3)
old_mobile_nav = '''  nav{width:100%;display:grid;grid-template-columns:repeat(5,1fr);gap:.2rem;}
  .nav-btn{padding:.4rem .1rem;font-size:.7rem;text-align:center;border-radius:6px;}'''

new_mobile_nav = '''  nav{width:100%;display:grid;grid-template-columns:repeat(3,1fr);gap:.2rem;}
  .nav-btn{padding:.35rem .1rem;font-size:.68rem;text-align:center;border-radius:6px;}'''

c = c.replace(old_mobile_nav, new_mobile_nav, 1)

# 3. Gesamt-Page HTML vor dem schliessenden </main>
gesamt_page = '''
    <!-- GESAMT -->
    <div class="page" id="page-gesamt">
      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem">Zeitraum</span>
          <input class="form-input" type="date" id="gesamt-from" style="max-width:160px" onchange="loadGesamt()">
          <span style="color:var(--muted);font-size:.85rem">bis</span>
          <input class="form-input" type="date" id="gesamt-to" style="max-width:160px" onchange="loadGesamt()">
          <button class="btn btn-ghost btn-sm" onclick="resetGesamtFilter()">Alle</button>
        </div>
      </div>

      <div class="stat-grid">
        <div class="stat-card"><div class="stat-label">Gesamtprofit</div><div class="stat-value neutral" id="g-total">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Cash Profit</div><div class="stat-value neutral" id="g-cash">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Turnier Profit</div><div class="stat-value neutral" id="g-tourney">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Gesamt Invested</div><div class="stat-value neutral" id="g-invested">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">ROI Gesamt</div><div class="stat-value neutral" id="g-roi">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Cash Stunden</div><div class="stat-value neutral" id="g-hours">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Cash Sessions</div><div class="stat-value neutral" id="g-sessions">&#8212;</div></div>
        <div class="stat-card"><div class="stat-label">Turniere</div><div class="stat-value neutral" id="g-tournaments">&#8212;</div></div>
      </div>

      <div class="panel">
        <div class="panel-title">Monatliche Entwicklung (Cash + Turniere)</div>
        <canvas id="gesamt-chart" height="160"></canvas>
        <div style="display:flex;gap:1rem;margin-top:.75rem;font-size:.75rem">
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:12px;background:#2d8f4e;border-radius:2px;display:inline-block"></span>Cash</span>
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:12px;background:#c9a84c;border-radius:2px;display:inline-block"></span>Turniere</span>
        </div>
      </div>
    </div>

'''

c = c.replace('\n  </main>\n</div>', gesamt_page + '\n  </main>\n</div>', 1)

# 4. showPage: gesamt -> loadGesamt()
old_show = "  if(name==='stats')loadStats();\n  if(name==='rangliste')loadRangliste();"
new_show = "  if(name==='stats')loadStats();\n  if(name==='rangliste')loadRangliste();\n  if(name==='gesamt')loadGesamt();"
c = c.replace(old_show, new_show, 1)

# 5. loadGesamt + resetGesamtFilter Funktionen vor // ── INIT ──
gesamt_js = '''
// ── GESAMT ──
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
}

function drawCombinedChart(id,data){
  const canvas=document.getElementById(id);if(!canvas||!data.length)return;
  const W=canvas.offsetWidth||700,H=160;canvas.width=W;canvas.height=H;
  const ctx=canvas.getContext('2d');ctx.clearRect(0,0,W,H);
  const allVals=data.flatMap(d=>[d.cash_profit,d.tournament_profit,0]);
  const mx=Math.max(...allVals),mn=Math.min(...allVals),range=mx-mn||1;
  const pad={top:10,bottom:30,left:10,right:10};
  const slotW=(W-pad.left-pad.right)/data.length;
  const bw=Math.max(6,slotW/2-3);
  const toY=v=>pad.top+((mx-v)/range)*(H-pad.top-pad.bottom),zy=toY(0);
  ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad.left,zy);ctx.lineTo(W-pad.right,zy);ctx.stroke();ctx.setLineDash([]);
  data.forEach((d,i)=>{
    const x=pad.left+i*slotW;
    // Cash (gruen/rot)
    const cp=d.cash_profit,cbh=Math.abs(toY(cp)-zy),cy=cp>=0?zy-cbh:zy;
    ctx.fillStyle=cp>=0?'#2d8f4e':'#c0392b';ctx.fillRect(x+2,cy,bw,Math.max(2,cbh));
    // Turnier (gold/dunkelrot)
    const tp=d.tournament_profit,tbh=Math.abs(toY(tp)-zy),ty=tp>=0?zy-tbh:zy;
    ctx.fillStyle=tp>=0?'#c9a84c':'#8b3a2a';ctx.fillRect(x+bw+4,ty,bw,Math.max(2,tbh));
    ctx.fillStyle='#7a8a7a';ctx.font='10px sans-serif';ctx.fillText(d.month.slice(5),x+slotW/2-10,H-6);
  });
}

'''

c = c.replace('// ── INIT ──', gesamt_js + '// ── INIT ──', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

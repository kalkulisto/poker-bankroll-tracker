path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Filter-UI: Location-Dropdown zur Turnier-Stats Seite hinzufuegen
old_filter = '''      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem">Zeitraum</span>
          <input class="form-input" type="date" id="stats-from" style="max-width:160px" onchange="loadStats()">
          <span style="color:var(--muted);font-size:.85rem">bis</span>
          <input class="form-input" type="date" id="stats-to" style="max-width:160px" onchange="loadStats()">
          <button class="btn btn-ghost btn-sm" onclick="resetStatsFilter()">Alle</button>
        </div>
      </div>'''

new_filter = '''      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem">Zeitraum</span>
          <input class="form-input" type="date" id="stats-from" style="max-width:160px" onchange="loadStats()">
          <span style="color:var(--muted);font-size:.85rem">bis</span>
          <input class="form-input" type="date" id="stats-to" style="max-width:160px" onchange="loadStats()">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;margin-left:.5rem">Location</span>
          <select class="form-select" id="stats-location" style="max-width:180px" onchange="loadStats()">
            <option value="">Alle</option>
          </select>
          <button class="btn btn-ghost btn-sm" onclick="resetStatsFilter()">Alle</button>
        </div>
      </div>'''

c = c.replace(old_filter, new_filter, 1)

# 2. resetStatsFilter: Location zuruecksetzen
old_reset = "function resetStatsFilter(){document.getElementById('stats-from').value='';document.getElementById('stats-to').value='';loadStats();}"
new_reset = "function resetStatsFilter(){document.getElementById('stats-from').value='';document.getElementById('stats-to').value='';document.getElementById('stats-location').value='';loadStats();}"

c = c.replace(old_reset, new_reset, 1)

# 3. loadStats: Location-Filter anwenden
old_loadstats = '''async function loadStats(){
  const from=document.getElementById('stats-from')?.value||'';
  const to=document.getElementById('stats-to')?.value||'';
  let filtered=allSessions;
  if(from)filtered=filtered.filter(s=>s.date>=from);
  if(to)filtered=filtered.filter(s=>s.date<=to);'''

new_loadstats = '''async function loadStats(){
  const from=document.getElementById('stats-from')?.value||'';
  const to=document.getElementById('stats-to')?.value||'';
  const loc=document.getElementById('stats-location')?.value||'';
  let filtered=allSessions;
  if(from)filtered=filtered.filter(s=>s.date>=from);
  if(to)filtered=filtered.filter(s=>s.date<=to);
  // Location-Filter fuer Turnier-Stats wird weiter unten angewandt'''

c = c.replace(old_loadstats, new_loadstats, 1)

# 4. Turnier-Stats: Location-Filter auf monatliche Daten anwenden
# Dazu muessen wir nach dem ts-Abruf die Location aus den Turnierdaten filtern
# Da ts/monthly keine Location enthaelt, holen wir allTournaments fuer Filterung
old_tsfilter = '''  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';
  const useFilter=!!(from||to);
  let tsMonthly=ts.monthly||[];
  if(fromMonth) tsMonthly=tsMonthly.filter(m=>m.month>=fromMonth);
  if(toMonth) tsMonthly=tsMonthly.filter(m=>m.month<=toMonth);'''

new_tsfilter = '''  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';
  const useFilter=!!(from||to||loc);

  // Location-Filter: Turniere nach Location einschraenken, dann Stats neu berechnen
  let tsMonthly=ts.monthly||[];
  if(loc){
    // Turnier-IDs mit dieser Location ermitteln
    const matchIds=new Set(allTournaments.filter(t=>(t.location||'').toLowerCase().includes(loc.toLowerCase())).map(t=>t.id));
    // Leider hat monthly keine tournament_id - wir rechnen direkt aus allTournaments+entries
    // Vereinfachung: monthly nach Monat filtern basierend auf Turnier-Daten
    const matchMonths=new Set(allTournaments.filter(t=>matchIds.has(t.id)&&t.start_date).map(t=>t.start_date.slice(0,7)));
    tsMonthly=tsMonthly.filter(m=>matchMonths.has(m.month));
  }
  if(fromMonth) tsMonthly=tsMonthly.filter(m=>m.month>=fromMonth);
  if(toMonth) tsMonthly=tsMonthly.filter(m=>m.month<=toMonth);'''

if old_tsfilter in c:
    c = c.replace(old_tsfilter, new_tsfilter, 1)
    print('tsfilter patched')
else:
    print('tsfilter NOT FOUND')

# 5. Location-Dropdown befuellen wenn Turnier-Stats geladen wird
old_drawmonth = '  drawMonthlyChart(\'monthly-chart\',monthly);'
new_drawmonth = '''  drawMonthlyChart('monthly-chart',monthly);
  // Location-Dropdown aus allTournaments befuellen
  const locSelect=document.getElementById('stats-location');
  const currentLoc=locSelect.value;
  const locs=[...new Set(allTournaments.map(t=>t.location).filter(Boolean))].sort();
  locSelect.innerHTML='<option value="">Alle</option>'+locs.map(l=>`<option value="${l}" ${l===currentLoc?'selected':''}>${l}</option>`).join('');'''

if old_drawmonth in c:
    c = c.replace(old_drawmonth, new_drawmonth, 1)
    print('dropdown patched')
else:
    print('dropdown NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

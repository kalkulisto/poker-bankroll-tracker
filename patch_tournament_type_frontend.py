path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Tournament Modal: tournament_type Dropdown hinzufuegen
old_modal_game = '      <div class="form-group"><label class="form-label">Spieltyp</label><select class="form-select" id="t-game"><option>NL Hold\'em</option><option>PLO</option></select></div>'
new_modal_game = '''      <div class="form-group"><label class="form-label">Spieltyp</label><select class="form-select" id="t-game"><option>NL Hold'em</option><option>PLO</option></select></div>
      <div class="form-group"><label class="form-label">Typ</label><select class="form-select" id="t-type"><option value="Live">Live</option><option value="Online">Online</option></select></div>'''

c = c.replace(old_modal_game, new_modal_game, 1)

# 2. openTournamentModal: t-type befuellen
old_open = "document.getElementById('t-global').checked=t.is_global;}"
new_open = "document.getElementById('t-global').checked=t.is_global;document.getElementById('t-type').value=t.tournament_type||'Live';}"
c = c.replace(old_open, new_open, 1)

old_else = "['t-name','t-series','t-location','t-start','t-end','t-buyin','t-fieldsize'].forEach(i=>document.getElementById(i).value='');document.getElementById('t-global').checked=false;"
new_else = "['t-name','t-series','t-location','t-start','t-end','t-buyin','t-fieldsize'].forEach(i=>document.getElementById(i).value='');document.getElementById('t-global').checked=false;document.getElementById('t-type').value='Live';"
c = c.replace(old_else, new_else, 1)

# 3. saveTournament: tournament_type mitsenden
old_save = "game_type:document.getElementById('t-game').value,is_global:document.getElementById('t-global').checked};"
new_save = "game_type:document.getElementById('t-game').value,tournament_type:document.getElementById('t-type').value,is_global:document.getElementById('t-global').checked};"
c = c.replace(old_save, new_save, 1)

# 4. Turnier-Liste: Typ-Badge anzeigen
old_badge = "const badge=t.is_global?'<span class=\"t-badge global-badge\">Global</span>':'<span class=\"t-badge own-badge\">Eigenes</span>';"
new_badge = "const badge=t.is_global?'<span class=\"t-badge global-badge\">Global</span>':'<span class=\"t-badge own-badge\">Eigenes</span>';\n    const typeBadge=t.tournament_type==='Online'?'<span class=\"t-badge\" style=\"background:#0d1a2a;color:#5b9bd5\">Online</span>':'';"
c = c.replace(old_badge, new_badge, 1)

# type badge in der Zeile einbauen
old_nameline = '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><span class="t-name">${t.name}</span>${badge}</div>'
new_nameline = '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><span class="t-name">${t.name}</span>${badge}${typeBadge}</div>'
c = c.replace(old_nameline, new_nameline, 1)

# 5. Location-Filter durch Typ-Filter ersetzen in Turnier-Stats
old_loc_filter = '''          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;margin-left:.5rem">Location</span>
          <select class="form-select" id="stats-location" style="max-width:180px" onchange="loadStats()">
            <option value="">Alle</option>
          </select>'''
new_loc_filter = '''          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;margin-left:.5rem">Typ</span>
          <select class="form-select" id="stats-location" style="max-width:130px" onchange="loadStats()">
            <option value="">Alle</option>
            <option value="Live">Live</option>
            <option value="Online">Online</option>
          </select>'''
c = c.replace(old_loc_filter, new_loc_filter, 1)

# 6. Typ-Filter Logik in loadStats anpassen
old_loc_logic = '''  if(loc){
    // Turnier-IDs mit dieser Location ermitteln
    const matchIds=new Set(allTournaments.filter(t=>(t.location||'').toLowerCase().includes(loc.toLowerCase())).map(t=>t.id));
    // Leider hat monthly keine tournament_id - wir rechnen direkt aus allTournaments+entries
    // Vereinfachung: monthly nach Monat filtern basierend auf Turnier-Daten
    const matchMonths=new Set(allTournaments.filter(t=>matchIds.has(t.id)&&t.start_date).map(t=>t.start_date.slice(0,7)));
    tsMonthly=tsMonthly.filter(m=>matchMonths.has(m.month));
  }'''
new_loc_logic = '''  if(loc){
    // Typ-Filter (Live/Online): Turniere dieses Typs bestimmen, Monate ermitteln
    const matchMonths=new Set(allTournaments.filter(t=>(t.tournament_type||'Live')===loc&&t.start_date).map(t=>t.start_date.slice(0,7)));
    tsMonthly=tsMonthly.filter(m=>matchMonths.has(m.month));
  }'''
if old_loc_logic in c:
    c = c.replace(old_loc_logic, new_loc_logic, 1)
    print('loc logic patched')
else:
    print('loc logic NOT FOUND')

# 7. Dropdown-Befuellung entfernen (nicht mehr dynamisch noetig)
old_dropdown = '''  // Location-Dropdown aus allTournaments befuellen
  const locSelect=document.getElementById('stats-location');
  const currentLoc=locSelect.value;
  const locs=[...new Set(allTournaments.map(t=>t.location).filter(Boolean))].sort();
  locSelect.innerHTML='<option value="">Alle</option>'+locs.map(l=>`<option value="${l}" ${l===currentLoc?'selected':''}>${l}</option>`).join('');'''
new_dropdown = ''  # statisches Dropdown braucht keine dynamische Befuellung
if old_dropdown in c:
    c = c.replace(old_dropdown, new_dropdown, 1)
    print('dropdown fill removed')
else:
    print('dropdown fill NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

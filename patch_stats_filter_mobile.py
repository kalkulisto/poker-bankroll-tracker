path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem">Zeitraum</span>
          <input class="form-input" type="date" id="stats-from" style="max-width:160px" onchange="loadStats()">
          <span style="color:var(--muted);font-size:.85rem">bis</span>
          <input class="form-input" type="date" id="stats-to" style="max-width:160px" onchange="loadStats()">
          <span style="font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;margin-left:.5rem">Typ</span>
          <select class="form-select" id="stats-location" style="max-width:130px" onchange="loadStats()">
            <option value="" selected>Alle</option>
            <option value="Live">Live</option>
            <option value="Online">Online</option>
          </select>
          <button class="btn btn-ghost btn-sm" onclick="resetStatsFilter()">Alle</button>
        </div>
      </div>'''

new = '''      <div class="panel" style="padding:1rem 1.25rem">
        <div style="display:flex;flex-direction:column;gap:.6rem">
          <div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap">
            <span style="font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;min-width:4rem">Zeitraum</span>
            <input class="form-input" type="date" id="stats-from" style="flex:1;min-width:130px;max-width:160px" onchange="loadStats()">
            <span style="color:var(--muted);font-size:.85rem">bis</span>
            <input class="form-input" type="date" id="stats-to" style="flex:1;min-width:130px;max-width:160px" onchange="loadStats()">
          </div>
          <div style="display:flex;align-items:center;gap:.5rem">
            <span style="font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1rem;min-width:4rem">Typ</span>
            <select class="form-select" id="stats-location" style="flex:1;max-width:160px" onchange="loadStats()">
              <option value="" selected>Alle</option>
              <option value="Live">Live</option>
              <option value="Online">Online</option>
            </select>
            <button class="btn btn-ghost btn-sm" onclick="resetStatsFilter()">Alle</button>
          </div>
        </div>
      </div>'''

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

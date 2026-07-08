path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Typ-Dropdown standardmaessig auf "Alle" setzen
old = '''          <select class="form-select" id="stats-location" style="max-width:130px" onchange="loadStats()">
            <option value="">Alle</option>
            <option value="Live">Live</option>
            <option value="Online">Online</option>
          </select>'''
new = '''          <select class="form-select" id="stats-location" style="max-width:130px" onchange="loadStats()">
            <option value="" selected>Alle</option>
            <option value="Live">Live</option>
            <option value="Online">Online</option>
          </select>'''

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

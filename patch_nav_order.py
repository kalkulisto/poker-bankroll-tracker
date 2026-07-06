path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old_nav = '''    <nav>
      <button class="nav-btn" onclick="showPage('dashboard')">Cash-Stats</button>
      <button class="nav-btn" onclick="showPage('sessions')">Cash Games</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn active" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Turnier-Stats</button>
      <button class="nav-btn" onclick="showPage('gesamt')">Gesamt</button>
    </nav>'''

new_nav = '''    <nav>
      <button class="nav-btn" onclick="showPage('sessions')">Cash Games</button>
      <button class="nav-btn" onclick="showPage('dashboard')">Cash-Stats</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('stats')">Turnier-Stats</button>
      <button class="nav-btn active" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('gesamt')">Gesamt</button>
    </nav>'''

if old_nav in c:
    c = c.replace(old_nav, new_nav, 1)
    print('OK')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

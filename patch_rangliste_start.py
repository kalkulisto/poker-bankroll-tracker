path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Nav: Rangliste statt Dashboard als active markieren
old_nav = '''    <nav>
      <button class="nav-btn active" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Turnier-Stats</button>
      <button class="nav-btn" onclick="showPage('gesamt')">Gesamt</button>
    </nav>'''

new_nav = '''    <nav>
      <button class="nav-btn" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn active" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Turnier-Stats</button>
      <button class="nav-btn" onclick="showPage('gesamt')">Gesamt</button>
    </nav>'''
c = c.replace(old_nav, new_nav, 1)

# 2. page-dashboard: "active" entfernen, page-rangliste: "active" hinzufuegen
c = c.replace('<div class="page active" id="page-dashboard">', '<div class="page" id="page-dashboard">', 1)
c = c.replace('<div class="page" id="page-rangliste">', '<div class="page active" id="page-rangliste">', 1)

# 3. enterApp: nach loadAll() auch loadRangliste() aufrufen, damit Rangliste sofort befuellt ist
old_enter = '''function enterApp(){
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  document.getElementById('header-username').textContent=currentUser.name;
  if(currentUser.is_admin)document.getElementById('admin-section').style.display='block';
  loadAll();
  if(currentUser.pin_changed===false){
    setTimeout(()=>openModal('pin-change-modal'),500);
  }
}'''

new_enter = '''function enterApp(){
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  document.getElementById('header-username').textContent=currentUser.name;
  if(currentUser.is_admin)document.getElementById('admin-section').style.display='block';
  loadAll();
  loadRangliste();
  if(currentUser.pin_changed===false){
    setTimeout(()=>openModal('pin-change-modal'),500);
  }
}'''
c = c.replace(old_enter, new_enter, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

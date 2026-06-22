path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Altes mobile CSS ersetzen
old_css = '''@media(max-width:640px){
  header{padding:0 1rem;gap:.5rem;}
  .nav-btn{padding:.4rem .5rem;font-size:.75rem;}
  .tournament-item{grid-template-columns:1fr;}
  .lb-header,.lb-row{grid-template-columns:2rem 1fr repeat(3,5rem);}
  .lb-header>*:nth-child(5),.lb-row>*:nth-child(5),
  .lb-header>*:nth-child(6),.lb-row>*:nth-child(6){display:none;}
}'''

new_css = '''@media(max-width:640px){
  header{padding:.5rem 1rem;flex-direction:column;height:auto;gap:.4rem;}
  .header-top{display:flex;justify-content:space-between;align-items:center;width:100%;}
  nav{width:100%;display:grid;grid-template-columns:repeat(5,1fr);gap:.2rem;}
  .nav-btn{padding:.4rem .1rem;font-size:.7rem;text-align:center;border-radius:6px;}
  main{padding:1rem .75rem;}
  .tournament-item{grid-template-columns:1fr;}
  .lb-header,.lb-row{grid-template-columns:2rem 1fr repeat(3,5rem);}
  .lb-header>*:nth-child(5),.lb-row>*:nth-child(5),
  .lb-header>*:nth-child(6),.lb-row>*:nth-child(6){display:none;}
}
@media(min-width:641px){
  .header-top{display:contents;}
}'''

c = c.replace(old_css, new_css, 1)

# 2. Header HTML umstrukturieren
old_header = '''  <header>
    <span class="header-logo">&#9824; Chico &amp; Zwieback</span>
    <nav>
      <button class="nav-btn active" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Statistiken</button>
    </nav>
    <div class="header-user">
      <strong id="header-username"></strong>
      <button class="logout-btn" onclick="logout()">Logout</button>
    </div>
  </header>'''

new_header = '''  <header>
    <div class="header-top">
      <span class="header-logo">&#9824; Chico &amp; Zwieback</span>
      <div class="header-user">
        <strong id="header-username"></strong>
        <button class="logout-btn" onclick="logout()">Logout</button>
      </div>
    </div>
    <nav>
      <button class="nav-btn active" onclick="showPage('dashboard')">Dashboard</button>
      <button class="nav-btn" onclick="showPage('sessions')">Sessions</button>
      <button class="nav-btn" onclick="showPage('tournaments')">Turniere</button>
      <button class="nav-btn" onclick="showPage('rangliste')">Rangliste</button>
      <button class="nav-btn" onclick="showPage('stats')">Statistiken</button>
    </nav>
  </header>'''

c = c.replace(old_header, new_header, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

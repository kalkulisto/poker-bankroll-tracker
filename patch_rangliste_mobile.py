path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. lb-header: Turniere und Best Platz entfernen
old_header = '''          <div class="lb-header">
            <div>#</div><div>Spieler</div>
            <div style="text-align:right">Turniere</div>
            <div style="text-align:right">Profit</div>
            <div style="text-align:right">ROI</div>
            <div style="text-align:right">ITM</div>
            <div style="text-align:right">Best Platz</div>
          </div>'''

new_header = '''          <div class="lb-header">
            <div>#</div><div>Spieler</div>
            <div style="text-align:right">Profit</div>
            <div style="text-align:right">ROI</div>
            <div style="text-align:right">ITM</div>
          </div>'''

c = c.replace(old_header, new_header, 1)

# 2. lb-row: Turniere und Best Platz entfernen, grid anpassen
old_row = '''      <div style="display:grid;grid-template-columns:2rem 1fr repeat(5,6rem);gap:.5rem;align-items:center">
        <div class="lb-rank ${i===0?'r1':i===1?'r2':i===2?'r3':''}">${i<3?rankIcons[i]:i+1}</div>
        <div class="lb-name">${u.name}</div>
        <div class="lb-val">${u.tournaments}</div>
        <div class="lb-val ${pCls}">${fmtMoney(u.total_profit)}</div>
        <div class="lb-val ${rCls}">${u.roi}%</div>
        <div class="lb-val">${u.itm_rate}%</div>
        <div class="lb-val">${u.best_position?'#'+u.best_position:'\\u2014'}</div>
      </div>'''

new_row = '''      <div style="display:grid;grid-template-columns:2rem 1fr repeat(3,5rem);gap:.5rem;align-items:center">
        <div class="lb-rank ${i===0?'r1':i===1?'r2':i===2?'r3':''}">${i<3?rankIcons[i]:i+1}</div>
        <div class="lb-name">${u.name}</div>
        <div class="lb-val ${pCls}">${fmtMoney(u.total_profit)}</div>
        <div class="lb-val ${rCls}">${u.roi}%</div>
        <div class="lb-val">${u.itm_rate}%</div>
      </div>'''

if old_row in c:
    c = c.replace(old_row, new_row, 1)
    print('lb-row patched')
else:
    print('lb-row NOT FOUND')

# 3. Shared tournament: Platzierung mit Spieleranzahl anzeigen
old_pos = '''          <div class="shared-player-pos">${p.position?'#'+p.position:'\\u2014'}</div>'''
new_pos = '''          <div class="shared-player-pos">${p.position?(t.field_size?'#'+p.position+' / '+t.field_size:'#'+p.position):'\\u2014'}</div>'''

if old_pos in c:
    c = c.replace(old_pos, new_pos, 1)
    print('shared-pos patched')
else:
    print('shared-pos NOT FOUND')

# 4. lb-header CSS: ebenfalls anpassen
old_css = '.lb-header{display:grid;grid-template-columns:2rem 1fr repeat(5,6rem);gap:.5rem;padding:.5rem .75rem;font-size:.7rem;text-transform:uppercase;letter-spacing:.1rem;color:var(--muted);border-bottom:1px solid var(--border);}'
new_css = '.lb-header{display:grid;grid-template-columns:2rem 1fr repeat(3,5rem);gap:.5rem;padding:.5rem .75rem;font-size:.7rem;text-transform:uppercase;letter-spacing:.1rem;color:var(--muted);border-bottom:1px solid var(--border);}'

if old_css in c:
    c = c.replace(old_css, new_css, 1)
    print('lb-header css patched')
else:
    print('lb-header css NOT FOUND')

# Altes mobile CSS fuer lb entfernen (war fuer 5-spaltig)
old_mob = '''  .lb-header,.lb-row{grid-template-columns:2rem 1fr repeat(3,5rem);}
  .lb-header>*:nth-child(5),.lb-row>*:nth-child(5),
  .lb-header>*:nth-child(6),.lb-row>*:nth-child(6){display:none;}'''
new_mob = ''  # nicht mehr noetig da grid jetzt schon klein

if old_mob in c:
    c = c.replace(old_mob, new_mob, 1)
    print('mobile lb css removed')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

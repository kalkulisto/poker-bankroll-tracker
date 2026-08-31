path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Checkbox im Tournament Modal nach dem Typ-Feld
old = '      <div class="form-group full" id="global-toggle" style="display:none">\n        <div class="checkbox-row"><input type="checkbox" id="t-global"><label for="t-global">F&#252;r alle sichtbar (global)</label></div>\n      </div>'
new = '''      <div class="form-group full" id="global-toggle" style="display:none">
        <div class="checkbox-row"><input type="checkbox" id="t-global"><label for="t-global">F&#252;r alle sichtbar (global)</label></div>
      </div>
      <div class="form-group full">
        <div class="checkbox-row"><input type="checkbox" id="t-challenge" checked><label for="t-challenge">&#127919; Z&#228;hlt f&#252;r die Challenge</label></div>
      </div>'''

if old in c:
    c = c.replace(old, new, 1)
    print('modal patched')
else:
    print('modal NOT FOUND')

# 2. openTournamentModal: challenge_eligible befuellen
old_open = "document.getElementById('t-type').value=t.tournament_type||'Live';}"
new_open = "document.getElementById('t-type').value=t.tournament_type||'Live';document.getElementById('t-challenge').checked=t.challenge_eligible!==false;}"
c = c.replace(old_open, new_open, 1)

old_else = "document.getElementById('t-global').checked=false;document.getElementById('t-type').value='Live';"
new_else = "document.getElementById('t-global').checked=false;document.getElementById('t-type').value='Live';document.getElementById('t-challenge').checked=true;"
c = c.replace(old_else, new_else, 1)

# 3. saveTournament: challenge_eligible mitsenden
old_save = "tournament_type:document.getElementById('t-type').value,is_global:document.getElementById('t-global').checked};"
new_save = "tournament_type:document.getElementById('t-type').value,challenge_eligible:document.getElementById('t-challenge').checked,is_global:document.getElementById('t-global').checked};"
c = c.replace(old_save, new_save, 1)

# 4. Turnierliste: nicht-eligible Turniere mit Badge kennzeichnen
old_badge = "const typeBadge=t.tournament_type==='Online'?'<span class=\"t-badge\" style=\"background:#0d1a2a;color:#5b9bd5\">Online</span>':'';"
new_badge = "const typeBadge=t.tournament_type==='Online'?'<span class=\"t-badge\" style=\"background:#0d1a2a;color:#5b9bd5\">Online</span>':'';\n    const notEligible=t.challenge_eligible===false?'<span class=\"t-badge\" style=\"background:#1a1010;color:#7a5a5a\">&#10006; Challenge</span>':'';"
c = c.replace(old_badge, new_badge, 1)

old_nameline = '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><span class="t-name">${t.name}</span>${badge}${typeBadge}</div>'
new_nameline = '<div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><span class="t-name">${t.name}</span>${badge}${typeBadge}${notEligible}</div>'
c = c.replace(old_nameline, new_nameline, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

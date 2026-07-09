path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Platzierungs-Input auf type="text" aendern fuer eigene Validierung
old = '<input class="form-input" type="number" id="e-position" min="1" placeholder="z.B. 47">'
new = '<input class="form-input" type="text" inputmode="numeric" id="e-position" placeholder="z.B. 47">'

if old in c:
    c = c.replace(old, new, 1)
    print('input patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

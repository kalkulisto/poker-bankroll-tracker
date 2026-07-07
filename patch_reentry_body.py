path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = "const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,notes:document.getElementById('e-notes').value||null};"
new = "const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,reentries:parseInt(document.getElementById('e-reentries').value)||0,notes:document.getElementById('e-notes').value||null};"

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

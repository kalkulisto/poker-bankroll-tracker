path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Alle Mehrfach-async bereinigen
for wrong in ['async async async function', 'async async function']:
    while wrong in c:
        c = c.replace(wrong, 'async function')
        print(f'fixed: {wrong}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

# Verifizieren
idx = c.find('function fetchUsers')
print('result:', repr(c[max(0,idx-20):idx+25]))

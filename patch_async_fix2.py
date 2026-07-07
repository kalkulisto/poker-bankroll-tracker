path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Mit fuehrendem Leerzeichen
old = ' function fetchUsers(){'
new = ' async function fetchUsers(){'

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND - searching...')
    idx = c.find('fetchUsers')
    print(repr(c[idx-15:idx+30]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

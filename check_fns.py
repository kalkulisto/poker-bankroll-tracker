import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html', encoding='utf-8') as f:
    c = f.read()

# Suche nach selectUser und fetchUsers
for keyword in ['function selectUser', 'function fetchUsers', 'function openEntryModal', 'function updateTotalCost']:
    idx = c.find(keyword)
    if idx >= 0:
        line = c[:idx].count('\n') + 1
        print(f'{keyword}: Zeile {line}')
        print(repr(c[idx:idx+120]))
        print()
    else:
        print(f'NOT FOUND: {keyword}')

path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

replacements = [
    ("onclick=\"showPage('dashboard')\">Dashboard</button>", "onclick=\"showPage('dashboard')\">Cash-Stats</button>"),
    ('<title>Chico und Zwieback</title>', '<title>Chico und Zwieback</title>'),
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new, 1)
        print(f'OK: {old[:60]}')
    else:
        print(f'NOT FOUND: {old[:60]}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

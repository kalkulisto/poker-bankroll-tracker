path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

replacements = [
    ('onclick="showPage(\'sessions\')">Sessions</button>', 'onclick="showPage(\'sessions\')">Cash Games</button>'),
    ('<div class="section-title">Cash Game Sessions</div>', '<div class="section-title">Cash Games</div>'),
    ('<div class="section-title">Letzte Sessions</div>', '<div class="section-title">Letzte Cash Games</div>'),
    ("id='session-modal-title'>Session erfassen", "id='session-modal-title'>Cash Game erfassen"),
    ('id="session-modal-title">Session erfassen', 'id="session-modal-title">Cash Game erfassen'),
    ("document.getElementById('session-modal-title').textContent=id?'Session bearbeiten':'Session erfassen'",
     "document.getElementById('session-modal-title').textContent=id?'Cash Game bearbeiten':'Cash Game erfassen'"),
    ('<p>Noch keine Sessions.</p>', '<p>Noch keine Cash Games.</p>'),
    ("confirm('Session l\\u00f6schen?')", "confirm('Cash Game l\\u00f6schen?')"),
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new, 1)
        print(f'OK: {old[:50]}')
    else:
        print(f'NOT FOUND: {old[:50]}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

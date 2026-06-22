import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

replacements = [
    ('<title>Poker Bankroll Tracker</title>', '<title>Chico und Zwieback</title>'),
    ('logo-title\">Bankroll Tracker</div>', 'logo-title\">Chico und Zwieback</div>'),
    ('<option>7-Card Stud</option>', ''),
    ('<option>Mixed</option>', ''),
    ('<option>Other</option>', ''),
]

for old, new in replacements:
    if old in c:
        c = c.replace(old, new)
        print('OK')
    else:
        print('NOT FOUND')

# Header logo ohne Sonderzeichen
import re
c = re.sub(r'class="header-logo">[^<]+</span>', 'class="header-logo">C&amp;Z</span>', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('Saved.')

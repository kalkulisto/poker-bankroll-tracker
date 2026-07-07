import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/page.html', encoding='utf-8').read()
idx = 0
print("=== fetchUsers Vorkommen in LIVE-Version ===")
while True:
    idx = c.find('fetchUsers', idx)
    if idx < 0: break
    print(repr(c[idx-15:idx+40]))
    idx += 1

# Syntax-Check des kompletten JS mit node falls vorhanden, sonst grobe Pruefung
import re
# Alle <script> Bloecke extrahieren
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
print(f"\n{len(scripts)} Script-Bloecke gefunden")
for i, s in enumerate(scripts):
    open(f'J:/Meine Ablage/ClaudeProjekte/poker-tracker/live_script_{i}.js', 'w', encoding='utf-8').write(s)
    print(f"Script {i}: {len(s)} Zeichen")

import urllib.request, json

# Login als ElChicoDe und Zwieback-Token simulieren - wir pruefen den Entry fuer Turnier 5
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg2MjE0NTkwfQ.LmoWQkgZfUk1wPO2dC4kqBO_raSS_pUN1eNxxY6o6ew'

# Leaderboard pruefen - sehen wir Zwieback's Entry?
req = urllib.request.Request(
    'https://poker-bankroll-tracker-7mk8.onrender.com/stats/leaderboard',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as r:
    d = json.loads(r.read())

out = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/debug_zwieback.txt', 'w', encoding='utf-8')
out.write('=== Leaderboard ===\n')
for lb in d['leaderboard']:
    out.write(f"{lb['name']}: profit={lb['total_profit']}, tournaments={lb['tournaments']}\n")

out.write('\n=== Tournaments ===\n')
for t in d['tournaments']:
    out.write(f"Turnier: {t['name']}\n")
    for p in t['players']:
        out.write(f"  {p['name']}: pos={p['position']} prize={p['prize_money']} reentries={p.get('reentries')}\n")
out.close()
print('done')

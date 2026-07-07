import json, urllib.request

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg2MDQyNTgzfQ.AKUs2PUlFh3m34eB8h9od4gnahtOQZ-SIUrxzpEr1Ss'
req = urllib.request.Request(
    'https://poker-bankroll-tracker-7mk8.onrender.com/stats/leaderboard',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req) as r:
    d = json.loads(r.read())

out = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/lb_result.txt', 'w', encoding='utf-8')
for t in d['tournaments']:
    out.write(f"Turnier: {t['name']} buy_in={t['buy_in']}\n")
    for p in t['players']:
        out.write(f"  {p['name']}: pos={p['position']} prize={p['prize_money']} profit={p['profit']} reentries={p.get('reentries')}\n")

# Auch die rohen Entries pruefen
req2 = urllib.request.Request(
    'https://poker-bankroll-tracker-7mk8.onrender.com/tournaments/',
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req2) as r:
    tours = json.loads(r.read())
for t in tours:
    if t.get('entry'):
        out.write(f"\nTurnier {t['name']}: entry reentries={t['entry'].get('reentries')}\n")

out.close()

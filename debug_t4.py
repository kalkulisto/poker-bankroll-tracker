import urllib.request, json

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg2MjE0NTkwfQ.LmoWQkgZfUk1wPO2dC4kqBO_raSS_pUN1eNxxY6o6ew'

# Neue Anmeldung: ElChicoDe Token (ID=1) - erneuern
data = json.dumps({"name": "ElChicoDe", "pin": "0323"}).encode()
req = urllib.request.Request('https://poker-bankroll-tracker-7mk8.onrender.com/auth/login',
    data=data, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req) as r:
    resp = json.loads(r.read())
    token = resp['token']

# Turniere holen
req2 = urllib.request.Request('https://poker-bankroll-tracker-7mk8.onrender.com/tournaments/',
    headers={'Authorization': f'Bearer {token}'})
with urllib.request.urlopen(req2) as r:
    tours = json.loads(r.read())

out = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/debug_t4.txt', 'w', encoding='utf-8')
for t in tours:
    out.write(f"ID={t['id']} Name={t['name']} buy_in={t['buy_in']} type={t.get('tournament_type')} entry={t.get('entry')}\n")

# Neuestes Turnier finden (Spieltag 4)
newest = max(tours, key=lambda t: t['id'])
out.write(f"\nNeuestes Turnier: ID={newest['id']}\n")

# PUT als ElChicoDe simulieren (Anmelden ohne Ergebnis)
body = json.dumps({"result_position": None, "prize_money": 0, "reentries": 0, "notes": None}).encode()
req3 = urllib.request.Request(
    f"https://poker-bankroll-tracker-7mk8.onrender.com/tournaments/{newest['id']}/entry",
    data=body, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'},
    method='PUT')
try:
    with urllib.request.urlopen(req3) as r:
        result = json.loads(r.read())
        out.write(f"PUT result: {result}\n")
except Exception as e:
    out.write(f"PUT ERROR: {e}\n")

out.close()
print('done')

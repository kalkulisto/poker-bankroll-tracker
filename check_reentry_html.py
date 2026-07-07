import urllib.request, re

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzg2MDQyNTgzfQ.AKUs2PUlFh3m34eB8h9od4gnahtOQZ-SIUrxzpEr1Ss'
req = urllib.request.Request('https://poker-bankroll-tracker-7mk8.onrender.com/')
with urllib.request.urlopen(req) as r:
    c = r.read().decode('utf-8')

out = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/live_check.txt', 'w', encoding='utf-8')

# Reentries Feld im Modal?
idx = c.find('e-reentries')
if idx >= 0:
    out.write('e-reentries field found:\n')
    out.write(c[max(0,idx-50):idx+100] + '\n\n')
else:
    out.write('e-reentries NICHT GEFUNDEN im HTML!\n\n')

# saveEntry Funktion
idx2 = c.find('async function saveEntry')
if idx2 >= 0:
    out.write('saveEntry:\n')
    out.write(c[idx2:idx2+400] + '\n')

out.close()

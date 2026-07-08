import urllib.request, re

req = urllib.request.Request('https://poker-bankroll-tracker-7mk8.onrender.com/')
with urllib.request.urlopen(req) as r:
    c = r.read().decode('utf-8')

idx = c.find('reentries:parseInt')
result = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/live_reentry_check.txt', 'w', encoding='utf-8')
if idx >= 0:
    result.write('FIX IS LIVE:\n')
    result.write(c[idx-20:idx+80])
else:
    result.write('FIX NOT YET DEPLOYED')
result.close()

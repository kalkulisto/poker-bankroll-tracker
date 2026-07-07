import urllib.request, re, sys
url = 'https://poker-bankroll-tracker-7mk8.onrender.com/'
with urllib.request.urlopen(url) as r:
    c = r.read().decode('utf-8')
base = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/'
open(base+'page2.html','w',encoding='utf-8').write(c)
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
open(base+'live2.js','w',encoding='utf-8').write(scripts[0])
result = open(base+'fetch_result.txt','w',encoding='utf-8')
result.write(f'size: {len(c)}\n')
result.write(f'async async count: {c.count("async async")}\n')
result.write(f'async function fetchUsers: {"async function fetchUsers" in c}\n')
result.write(f'scripts found: {len(scripts)}\n')
result.close()

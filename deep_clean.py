import re, sys

path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
c = open(path, encoding='utf-8').read()

# Alle async-Varianten bereinigen
before = c.count('async')
while 'async async' in c:
    c = c.replace('async async', 'async')
after = c.count('async')

open(path, 'w', encoding='utf-8').write(c)

# Script extrahieren und mit Node pruefen
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/test_script.js', 'w', encoding='utf-8').write(scripts[0])

result = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/cleanup_result.txt', 'w', encoding='utf-8')
result.write(f'async count before: {before}\n')
result.write(f'async count after: {after}\n')
result.write(f'async async remaining: {c.count("async async")}\n')
result.write(f'async function fetchUsers present: {"async function fetchUsers" in c}\n')
result.close()

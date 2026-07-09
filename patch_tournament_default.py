path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. showPage: beim Turniere-Tab neu laden
old_showpage = "  if(name==='stats')loadStats();\n  if(name==='rangliste')loadRangliste();\n  if(name==='gesamt')loadGesamt();"
new_showpage = "  if(name==='stats')loadStats();\n  if(name==='rangliste')loadRangliste();\n  if(name==='gesamt')loadGesamt();\n  if(name==='tournaments')loadTournaments();"
c = c.replace(old_showpage, new_showpage, 1)

# 2. Standard-Filter auf 'all' statt 'upcoming'
old_default = "setTFilter('upcoming');"
new_default = "setTFilter('all');"
c = c.replace(old_default, new_default, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

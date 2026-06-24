path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Overflow-x hidden auf html und body, Tabellen scrollbar innerhalb Container
old = 'body{font-family:\'Segoe UI\',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}'
new = ('html,body{overflow-x:hidden;}'
       'body{font-family:\'Segoe UI\',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;}')

c = c.replace(old, new, 1)

# Tabellen in scrollbaren Container (mobil)
old2 = '.data-table{width:100%;border-collapse:collapse;font-size:.875rem;}'
new2 = ('.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;}'
        '.data-table{width:100%;border-collapse:collapse;font-size:.875rem;min-width:480px;}')

c = c.replace(old2, new2, 1)

# Alle data-table in table-wrap einwickeln
c = c.replace('<table class="data-table">', '<div class="table-wrap"><table class="data-table">')
c = c.replace('</table>', '</table></div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

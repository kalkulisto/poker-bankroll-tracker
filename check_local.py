import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html', encoding='utf-8').read()
idx = c.find('fetchUsers')
print('local fetchUsers:', repr(c[idx-10:idx+30]))

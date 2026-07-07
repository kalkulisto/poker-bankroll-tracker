import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html', encoding='utf-8').read()
idx = 0
while True:
    idx = c.find('fetchUsers', idx)
    if idx < 0: break
    print(repr(c[idx-15:idx+40]))
    idx += 1

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
c = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/page.html', encoding='utf-8').read()
idx = c.find('fetchUsers')
print('fetchUsers at index:', idx)
if idx >= 0:
    print(repr(c[idx-5:idx+80]))
    line = c[:idx].count('\n') + 1
    print('line:', line)

# check for syntax errors - find async functions
import re
fns = re.findall(r'(async\s+)?function\s+\w+', c)
non_async = [f for f in fns if 'await' not in f and not f.startswith('async')]
print('\nAll function declarations (first 20):')
for f in fns[:20]:
    print(' ', repr(f))

import re
c = open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html', encoding='utf-8').read()
scripts = re.findall(r'<script>(.*?)</script>', c, re.DOTALL)
open('J:/Meine Ablage/ClaudeProjekte/poker-tracker/local_script_0.js', 'w', encoding='utf-8').write(scripts[0])
print('extracted, count of "async async":', c.count('async async'))

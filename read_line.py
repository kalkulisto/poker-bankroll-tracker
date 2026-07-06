f=open('frontend/index.html',encoding='utf-8')
lines=f.readlines()
f.close()
out=open('line605.txt','w',encoding='utf-8')
for i,l in enumerate(lines[598:615],start=599):
    out.write(f"{i+1}: {l}")
out.close()
print('written', len(lines), 'total lines')

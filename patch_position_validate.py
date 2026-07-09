path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''async function saveEntry(){
  const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,reentries:parseInt(document.getElementById('e-reentries').value)||0,notes:document.getElementById('e-notes').value||null};'''

new = '''async function saveEntry(){
  const posVal=document.getElementById('e-position').value.trim();
  if(posVal!==''&&(isNaN(parseInt(posVal))||parseInt(posVal)<1)){
    alert('Platzierung muss eine positive Zahl sein (oder leer lassen).');return;
  }
  const body={result_position:posVal?parseInt(posVal):null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,reentries:parseInt(document.getElementById('e-reentries').value)||0,notes:document.getElementById('e-notes').value||null};'''

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

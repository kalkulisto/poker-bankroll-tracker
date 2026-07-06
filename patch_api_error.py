path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''// ── API ──
async function api(path,method='GET',body=null){
  const opts={method,headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}};
  if(body)opts.body=JSON.stringify(body);
  const res=await fetch(API+path,opts);
  if(!res.ok)throw await res.json();
  return res.json();
}'''

new = '''// ── API ──
async function api(path,method='GET',body=null){
  const opts={method,headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}};
  if(body)opts.body=JSON.stringify(body);
  let res;
  try{res=await fetch(API+path,opts);}
  catch(e){throw{detail:'Keine Verbindung zum Server. Bitte kurz warten und nochmal versuchen.'};}
  if(!res.ok){
    let err;
    try{err=await res.json();}
    catch(e){err={detail:`Server-Fehler (${res.status}). Render startet evtl. gerade neu \u2014 bitte 30 Sekunden warten.`};}
    throw err;
  }
  try{return await res.json();}
  catch(e){throw{detail:'Ung\u00fcltige Server-Antwort. Bitte nochmal versuchen.'};}
}'''

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

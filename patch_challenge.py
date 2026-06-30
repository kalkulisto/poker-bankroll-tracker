path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. CSS fuer Challenge-Widget ergaenzen
old_css_anchor = '.winner-badge{font-size:.65rem;background:#2a1f00;color:var(--gold);padding:.15rem .5rem;border-radius:4px;font-weight:700;margin-left:.4rem;}'
new_css = old_css_anchor + '''
.challenge-box{background:linear-gradient(135deg,#162016,#1a2010);border:1px solid var(--gold-dim);border-radius:12px;padding:1.25rem 1.5rem;margin-bottom:1.25rem;}
.challenge-title{font-size:.7rem;text-transform:uppercase;letter-spacing:.15rem;color:var(--gold);margin-bottom:.6rem;font-weight:700;}
.challenge-progress-row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.5rem;}
.challenge-count{font-size:1.6rem;font-weight:700;color:var(--text);}
.challenge-count span{font-size:1rem;color:var(--muted);font-weight:400;}
.challenge-pct{font-size:.85rem;color:var(--gold);font-weight:600;}
.challenge-bar-track{width:100%;height:10px;background:var(--surface);border-radius:6px;overflow:hidden;border:1px solid var(--border);}
.challenge-bar-fill{height:100%;background:linear-gradient(90deg,#2d8f4e,#c9a84c);border-radius:6px;transition:width .4s ease;}
.challenge-lead{margin-top:.85rem;padding-top:.85rem;border-top:1px solid var(--border);display:flex;align-items:center;gap:.5rem;font-size:.9rem;}
.challenge-lead-name{font-weight:700;color:var(--gold);}
.challenge-lead-gap{font-weight:700;}
'''
c = c.replace(old_css_anchor, new_css, 1)

# 2. HTML: Challenge-Box vor dem lb-header Panel einfuegen
old_html = '''      <div id="rangliste-content" style="display:none">
        <div class="panel" style="padding:.75rem">'''

new_html = '''      <div id="rangliste-content" style="display:none">
        <div class="challenge-box" id="challenge-box" style="display:none">
          <div class="challenge-title">&#127919; 100-Turniere-Challenge</div>
          <div class="challenge-progress-row">
            <div class="challenge-count"><span id="challenge-played">0</span><span> / 100 Turniere</span></div>
            <div class="challenge-pct" id="challenge-pct">0%</div>
          </div>
          <div class="challenge-bar-track"><div class="challenge-bar-fill" id="challenge-bar" style="width:0%"></div></div>
          <div class="challenge-lead" id="challenge-lead"></div>
        </div>
        <div class="panel" style="padding:.75rem">'''

c = c.replace(old_html, new_html, 1)

# 3. JS: loadRangliste um Challenge-Befuellung erweitern
old_js = '''async function loadRangliste(){
  const data=await api('/stats/leaderboard');
  const empty=document.getElementById('rangliste-empty');
  const content=document.getElementById('rangliste-content');
  if(!data.leaderboard.length){empty.style.display='block';content.style.display='none';return;}
  empty.style.display='none';content.style.display='block';'''

new_js = '''async function loadRangliste(){
  const data=await api('/stats/leaderboard');
  const empty=document.getElementById('rangliste-empty');
  const content=document.getElementById('rangliste-content');
  if(!data.leaderboard.length){empty.style.display='block';content.style.display='none';return;}
  empty.style.display='none';content.style.display='block';

  // Challenge-Widget befuellen
  if(data.challenge){
    const ch=data.challenge;
    document.getElementById('challenge-box').style.display='block';
    document.getElementById('challenge-played').textContent=ch.played;
    document.getElementById('challenge-pct').textContent=ch.progress_pct+'%';
    document.getElementById('challenge-bar').style.width=ch.progress_pct+'%';
    const leadEl=document.getElementById('challenge-lead');
    if(ch.leader_name && ch.gap>0){
      leadEl.innerHTML=`&#128081; <span class="challenge-lead-name">${ch.leader_name}</span> f\\u00fchrt mit <span class="challenge-lead-gap profit-pos">${fmtMoney(ch.gap)}</span> Vorsprung`;
    }else if(ch.leader_name && ch.gap===0){
      leadEl.innerHTML='&#129309; Beide gleichauf \\u2014 noch ist alles offen!';
    }else{
      leadEl.innerHTML='Noch keine Ergebnisse eingetragen.';
    }
  }
'''

c = c.replace(old_js, new_js, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

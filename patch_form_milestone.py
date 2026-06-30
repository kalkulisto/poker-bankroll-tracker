path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. CSS fuer Form-Dots und Milestone-Popup
old_css_anchor = '''.h2h-itm-score .vs{color:var(--muted);font-weight:400;margin:0 .5rem;font-size:.85rem;}'''
new_css = old_css_anchor + '''
.form-row{display:flex;align-items:center;gap:.35rem;margin-top:.4rem;}
.form-label-mini{font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06rem;margin-right:.2rem;}
.form-dot{width:10px;height:10px;border-radius:50%;cursor:default;flex-shrink:0;}
.form-dot.itm{background:var(--green-hi);}
.form-dot.bust{background:var(--red);opacity:.65;}

.milestone-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.8);z-index:300;align-items:center;justify-content:center;}
.milestone-overlay.open{display:flex;}
.milestone-card{background:linear-gradient(135deg,#162016,#1a2010);border:2px solid var(--gold);border-radius:18px;padding:2.5rem 2rem;text-align:center;max-width:340px;position:relative;overflow:hidden;animation:milestonePop .4s ease;}
@keyframes milestonePop{from{transform:scale(.7);opacity:0;}to{transform:scale(1);opacity:1;}}
.milestone-icon{font-size:3rem;margin-bottom:.75rem;}
.milestone-title{font-size:1.3rem;font-weight:700;color:var(--gold);margin-bottom:.4rem;}
.milestone-sub{font-size:.9rem;color:var(--text);margin-bottom:1.5rem;}
.milestone-close{background:var(--gold);color:#0a0f0a;border:none;padding:.6rem 1.5rem;border-radius:8px;font-weight:700;cursor:pointer;font-size:.9rem;}
.confetti{position:absolute;width:8px;height:8px;top:-10px;opacity:.9;animation:confettiFall linear forwards;}
@keyframes confettiFall{to{transform:translateY(420px) rotate(540deg);opacity:0;}}
'''
c = c.replace(old_css_anchor, new_css, 1)

# 2. Milestone-Overlay HTML vor dem schliessenden </body> (vor den Scripts)
milestone_html = '''
<div class="milestone-overlay" id="milestone-overlay">
  <div class="milestone-card" id="milestone-card">
    <div class="milestone-icon">&#127881;</div>
    <div class="milestone-title" id="milestone-title">25 Turniere!</div>
    <div class="milestone-sub" id="milestone-sub">Ein Viertel der Challenge geschafft.</div>
    <button class="milestone-close" onclick="closeMilestone()">Weiter geht's &#9824;</button>
  </div>
</div>
'''
c = c.replace('<script>\nconst API=', milestone_html + '\n<script>\nconst API=', 1)

# 3. Form-Dots in der Leaderboard-Row anzeigen
old_render = '''      ${badgesHtml?`<div class="player-badges">${badgesHtml}</div>`:''}
    </div>`;
  }).join('');'''

new_render = '''      ${badgesHtml?`<div class="player-badges">${badgesHtml}</div>`:''}
      ${(u.form&&u.form.length)?`<div class="form-row"><span class="form-label-mini">Form</span>${u.form.map(f=>`<span class="form-dot ${f.itm?'itm':'bust'}" title="${fmtDate(f.date)}: ${fmtMoney(f.profit)}"></span>`).join('')}</div>`:''}
    </div>`;
  }).join('');

  checkMilestone(data.challenge);'''

c = c.replace(old_render, new_render, 1)

# 4. Milestone-Logik + Konfetti JS vor // ── INIT ──
milestone_js = '''
// ── MILESTONE ──
const MILESTONES=[25,50,75,100];
function checkMilestone(challenge){
  if(!challenge)return;
  const played=challenge.played;
  const seen=parseInt(localStorage.getItem('cz_milestone_seen')||'0');
  const hit=MILESTONES.filter(m=>played>=m&&m>seen).sort((a,b)=>b-a)[0];
  if(hit){
    showMilestone(hit,challenge);
    localStorage.setItem('cz_milestone_seen',String(hit));
  }
}

function showMilestone(n,challenge){
  const titles={25:'25 Turniere!',50:'Halbzeit!',75:'75 Turniere!',100:'CHALLENGE GESCHAFFT!'};
  const subs={
    25:'Ein Viertel der 100er-Challenge geschafft.',
    50:'Die H\\u00e4lfte ist geschafft \\u2014 weiter so!',
    75:'Nur noch 25 Turniere bis zum Ziel.',
    100:`${challenge.leader_name||''} liegt aktuell vorne. Zeit f\\u00fcr die Abrechnung! &#127942;`
  };
  document.getElementById('milestone-title').textContent=titles[n];
  document.getElementById('milestone-sub').innerHTML=subs[n];
  document.querySelector('.milestone-icon').textContent=n===100?'\\u{1F3C6}':'\\u{1F389}';
  spawnConfetti();
  openModalRaw('milestone-overlay');
}

function closeMilestone(){document.getElementById('milestone-overlay').classList.remove('open');}

function openModalRaw(id){document.getElementById(id).classList.add('open');}

function spawnConfetti(){
  const card=document.getElementById('milestone-card');
  const colors=['#c9a84c','#2d8f4e','#3db866','#e8e8e4','#8a6f30'];
  for(let i=0;i<28;i++){
    const el=document.createElement('div');
    el.className='confetti';
    el.style.left=Math.random()*100+'%';
    el.style.background=colors[Math.floor(Math.random()*colors.length)];
    el.style.animationDuration=(1.2+Math.random()*1)+'s';
    el.style.animationDelay=(Math.random()*.3)+'s';
    el.style.borderRadius=Math.random()>.5?'50%':'2px';
    card.appendChild(el);
    setTimeout(()=>el.remove(),2500);
  }
}

'''

c = c.replace('// ── INIT ──', milestone_js + '// ── INIT ──', 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

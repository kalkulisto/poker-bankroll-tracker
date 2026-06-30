path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Tournament Modal: field_size Eingabefeld ergaenzen
old_modal = '''      <div class="form-group"><label class="form-label">Buy-in ($)</label><input class="form-input" type="number" id="t-buyin" min="0" step="10"></div>
      <div class="form-group"><label class="form-label">Spieltyp</label><select class="form-select" id="t-game"><option>NL Hold'em</option><option>PLO</option></select></div>'''

new_modal = '''      <div class="form-group"><label class="form-label">Buy-in ($)</label><input class="form-input" type="number" id="t-buyin" min="0" step="10"></div>
      <div class="form-group"><label class="form-label">Teilnehmer (optional)</label><input class="form-input" type="number" id="t-fieldsize" min="0" placeholder="z.B. 84"></div>
      <div class="form-group"><label class="form-label">Spieltyp</label><select class="form-select" id="t-game"><option>NL Hold'em</option><option>PLO</option></select></div>'''

c = c.replace(old_modal, new_modal, 1)

# 2. openTournamentModal + saveTournament: field_size mit aufnehmen
old_open = '''  if(id){const t=allTournaments.find(x=>x.id===id);document.getElementById('t-name').value=t.name;document.getElementById('t-series').value=t.series||'';document.getElementById('t-location').value=t.location||'';document.getElementById('t-start').value=t.start_date||'';document.getElementById('t-end').value=t.end_date||'';document.getElementById('t-buyin').value=t.buy_in||'';document.getElementById('t-game').value=t.game_type;document.getElementById('t-global').checked=t.is_global;}
  else{['t-name','t-series','t-location','t-start','t-end','t-buyin'].forEach(i=>document.getElementById(i).value='');document.getElementById('t-global').checked=false;}'''

new_open = '''  if(id){const t=allTournaments.find(x=>x.id===id);document.getElementById('t-name').value=t.name;document.getElementById('t-series').value=t.series||'';document.getElementById('t-location').value=t.location||'';document.getElementById('t-start').value=t.start_date||'';document.getElementById('t-end').value=t.end_date||'';document.getElementById('t-buyin').value=t.buy_in||'';document.getElementById('t-fieldsize').value=t.field_size||'';document.getElementById('t-game').value=t.game_type;document.getElementById('t-global').checked=t.is_global;}
  else{['t-name','t-series','t-location','t-start','t-end','t-buyin','t-fieldsize'].forEach(i=>document.getElementById(i).value='');document.getElementById('t-global').checked=false;}'''

c = c.replace(old_open, new_open, 1)

old_save = '''  const body={name:document.getElementById('t-name').value,series:document.getElementById('t-series').value||null,location:document.getElementById('t-location').value||null,start_date:document.getElementById('t-start').value||null,end_date:document.getElementById('t-end').value||null,buy_in:parseFloat(document.getElementById('t-buyin').value)||null,game_type:document.getElementById('t-game').value,is_global:document.getElementById('t-global').checked};'''

new_save = '''  const body={name:document.getElementById('t-name').value,series:document.getElementById('t-series').value||null,location:document.getElementById('t-location').value||null,start_date:document.getElementById('t-start').value||null,end_date:document.getElementById('t-end').value||null,buy_in:parseFloat(document.getElementById('t-buyin').value)||null,field_size:parseInt(document.getElementById('t-fieldsize').value)||null,game_type:document.getElementById('t-game').value,is_global:document.getElementById('t-global').checked};'''

c = c.replace(old_save, new_save, 1)

# 3. CSS fuer Badges
old_css_anchor = '.challenge-lead-gap{font-weight:700;}'
new_css = old_css_anchor + '''
.player-badges{display:flex;gap:.3rem;flex-wrap:wrap;margin-top:.4rem;}
.badge-chip{display:inline-flex;align-items:center;gap:.25rem;background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:.15rem .55rem;font-size:.7rem;color:var(--muted);cursor:default;}
.badge-chip .badge-count{color:var(--gold);font-weight:700;}
.h2h-itm-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:.85rem 1.25rem;margin-bottom:1.25rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.5rem;}
.h2h-itm-title{font-size:.7rem;text-transform:uppercase;letter-spacing:.1rem;color:var(--muted);}
.h2h-itm-score{font-size:1.1rem;font-weight:700;}
.h2h-itm-score .vs{color:var(--muted);font-weight:400;margin:0 .5rem;font-size:.85rem;}
'''
c = c.replace(old_css_anchor, new_css, 1)

# 4. HTML: H2H-ITM Box vor Challenge-Box einfuegen
old_html = '''        <div class="challenge-box" id="challenge-box" style="display:none">'''
new_html = '''        <div class="h2h-itm-box" id="h2h-itm-box" style="display:none">
          <span class="h2h-itm-title">&#128176; Head-to-Head ITM</span>
          <span class="h2h-itm-score" id="h2h-itm-score"></span>
        </div>
        <div class="challenge-box" id="challenge-box" style="display:none">'''
c = c.replace(old_html, new_html, 1)

# 5. Leaderboard-Row HTML: Badges unter jeder Zeile anzeigen
old_lb_render = '''  document.getElementById('lb-rows').innerHTML=data.leaderboard.map((u,i)=>{
    const pCls=u.total_profit>0?'profit-pos':u.total_profit<0?'profit-neg':'';
    const rCls=u.roi>0?'profit-pos':u.roi<0?'profit-neg':'';
    return`<div class="lb-row">
      <div class="lb-rank ${i===0?'r1':i===1?'r2':i===2?'r3':''}">${i<3?rankIcons[i]:i+1}</div>
      <div class="lb-name">${u.name}</div>
      <div class="lb-val">${u.tournaments}</div>
      <div class="lb-val ${pCls}">${fmtMoney(u.total_profit)}</div>
      <div class="lb-val ${rCls}">${u.roi}%</div>
      <div class="lb-val">${u.itm_rate}%</div>
      <div class="lb-val">${u.best_position?'#'+u.best_position:'\\u2014'}</div>
    </div>`;
  }).join('');'''

new_lb_render = '''  document.getElementById('lb-rows').innerHTML=data.leaderboard.map((u,i)=>{
    const pCls=u.total_profit>0?'profit-pos':u.total_profit<0?'profit-neg':'';
    const rCls=u.roi>0?'profit-pos':u.roi<0?'profit-neg':'';
    const badgesHtml=(u.badges||[]).map(b=>
      `<span class="badge-chip" title="${b.detail||b.label}">${b.icon} ${b.label} <span class="badge-count">${b.count}</span></span>`
    ).join('');
    return`<div class="lb-row" style="flex-direction:column;align-items:stretch;display:flex;gap:.4rem">
      <div style="display:grid;grid-template-columns:2rem 1fr repeat(5,6rem);gap:.5rem;align-items:center">
        <div class="lb-rank ${i===0?'r1':i===1?'r2':i===2?'r3':''}">${i<3?rankIcons[i]:i+1}</div>
        <div class="lb-name">${u.name}</div>
        <div class="lb-val">${u.tournaments}</div>
        <div class="lb-val ${pCls}">${fmtMoney(u.total_profit)}</div>
        <div class="lb-val ${rCls}">${u.roi}%</div>
        <div class="lb-val">${u.itm_rate}%</div>
        <div class="lb-val">${u.best_position?'#'+u.best_position:'\\u2014'}</div>
      </div>
      ${badgesHtml?`<div class="player-badges">${badgesHtml}</div>`:''}
    </div>`;
  }).join('');

  // Head-to-Head ITM Score
  const h2hBox=document.getElementById('h2h-itm-box');
  if(data.h2h_itm){
    h2hBox.style.display='flex';
    document.getElementById('h2h-itm-score').innerHTML=
      `${data.h2h_itm.a_name} <span style="color:var(--gold)">${data.h2h_itm.a_itm}</span><span class="vs">:</span><span style="color:var(--gold)">${data.h2h_itm.b_itm}</span> ${data.h2h_itm.b_name}`;
  }else{
    h2hBox.style.display='none';
  }'''

if old_lb_render in c:
    c = c.replace(old_lb_render, new_lb_render, 1)
    print('leaderboard patched')
else:
    print('LB NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

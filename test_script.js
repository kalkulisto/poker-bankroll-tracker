
const API='';
let token=localStorage.getItem('poker_token');
let currentUser=JSON.parse(localStorage.getItem('poker_user')||'null');
let allSessions=[],allTournaments=[];
let editingSessionId=null,editingTournamentId=null,entryTournamentId=null;
let tournamentFilter='upcoming';

// ── AUTH ──
async function fetchUsers(){
  const res=await fetch('/auth/users');
  const users=await res.json();
  const avatars=['\u2660','\u2665','\u2666','\u2663','\u2605','\u25c6'];
  document.getElementById('user-list').innerHTML=users.map((u,i)=>
    `<div class="user-card" onclick="selectUser(${u.id},'${u.name}',${u.is_admin})" data-uid="${u.id}">
      <div class="user-card-avatar">${avatars[i%avatars.length]}</div>
      <div class="user-card-name">${u.name}</div>
      ${u.is_admin?'<div class="user-card-admin">Admin</div>':''}
    </div>`).join('');
}

let selectedUserName='',selectedUserId=null;
function selectUser(id,name,isAdmin){
  selectedUserId=id;selectedUserName=name;
  document.querySelectorAll('.user-card').forEach(c=>c.classList.remove('selected'));
  document.querySelector(`[data-uid="${id}"]`).classList.add('selected');
  document.getElementById('pin-section').style.display='flex';
  document.getElementById('pin-error').textContent='';
  pinValue='';updateDots();buildPinGrid();
}

let pinValue='';
function buildPinGrid(){
  const keys=['1','2','3','4','5','6','7','8','9','','0','\u232b'];
  document.getElementById('pin-grid').innerHTML=keys.map(k=>{
    if(k==='')return'<div></div>';
    if(k==='\u232b')return`<button class="pin-btn del" onclick="pinDel()">\u232b</button>`;
    return`<button class="pin-btn" onclick="pinPress('${k}')">${k}</button>`;
  }).join('');
}
function updateDots(){for(let i=0;i<4;i++)document.getElementById(`d${i}`).classList.toggle('filled',i<pinValue.length);}
function pinPress(k){if(pinValue.length>=4)return;pinValue+=k;updateDots();if(pinValue.length===4)doLogin();}
function pinDel(){pinValue=pinValue.slice(0,-1);updateDots();}

async function doLogin(){
  const res=await fetch('/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:selectedUserName,pin:pinValue})});
  if(!res.ok){document.getElementById('pin-error').textContent='Falscher PIN';pinValue='';updateDots();return;}
  const data=await res.json();
  token=data.token;currentUser=data.user;
  localStorage.setItem('poker_token',token);
  localStorage.setItem('poker_user',JSON.stringify(currentUser));
  enterApp();
}

function enterApp(){
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  document.getElementById('header-username').textContent=currentUser.name;
  if(currentUser.is_admin)document.getElementById('admin-section').style.display='block';
  loadAll();
  loadRangliste();
  if(currentUser.pin_changed===false){
    setTimeout(()=>openModal('pin-change-modal'),500);
  }
}

function logout(){
  token=null;currentUser=null;
  localStorage.removeItem('poker_token');localStorage.removeItem('poker_user');
  document.getElementById('app').style.display='none';
  document.getElementById('login-screen').style.display='flex';
  pinValue='';selectedUserId=null;
  document.querySelectorAll('.user-card').forEach(c=>c.classList.remove('selected'));
  document.getElementById('pin-section').style.display='none';
  fetchUsers();
}

async function saveNewPin(){
  const p1=document.getElementById('new-pin-1').value;
  const p2=document.getElementById('new-pin-2').value;
  const err=document.getElementById('pin-change-error');
  if(p1.length<4){err.textContent='PIN muss 4 Ziffern haben';return;}
  if(p1!==p2){err.textContent='PINs stimmen nicht \u00fcberein';return;}
  try{
    await api(`/auth/users/${currentUser.id}/pin`,'PUT',{new_pin:p1});
    currentUser.pin_changed=true;
    localStorage.setItem('poker_user',JSON.stringify(currentUser));
    closeModal('pin-change-modal');
  }catch(e){err.textContent='Fehler beim Speichern';}
}

// ── NAV ──
function showPage(name){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(`page-${name}`).classList.add('active');
  event.target.classList.add('active');
  if(name==='stats')loadStats();
  if(name==='rangliste')loadRangliste();
  if(name==='gesamt')loadGesamt();
  if(name==='tournaments')loadTournaments();
}

// ── API ──
async function api(path,method='GET',body=null){
  const opts={method,headers:{'Content-Type':'application/json','Authorization':`Bearer ${token}`}};
  if(body)opts.body=JSON.stringify(body);
  let res;
  try{res=await fetch(API+path,opts);}
  catch(e){throw{detail:'Keine Verbindung zum Server. Bitte kurz warten und nochmal versuchen.'};}
  if(!res.ok){
    let err;
    try{err=await res.json();}
    catch(e){err={detail:`Server-Fehler (${res.status}). Render startet evtl. gerade neu — bitte 30 Sekunden warten.`};}
    throw err;
  }
  try{return await res.json();}
  catch(e){throw{detail:'Ungültige Server-Antwort. Bitte nochmal versuchen.'};}
}

// ── DATA ──
async function loadAll(){await Promise.all([loadSessions(),loadTournaments()]);renderDashboard();}
async function loadSessions(){allSessions=await api('/sessions/');renderSessions();renderRecentSessions();}
async function loadTournaments(){allTournaments=await api('/tournaments/');renderTournaments();}

// ── FORMAT ──
function fmtMoney(v){const n=parseFloat(v);if(isNaN(n))return'\u2014';return(n>=0?'+':'')+'$'+Math.abs(n).toFixed(0);}
function fmtDate(s){return new Date(s).toLocaleDateString('de-DE',{day:'2-digit',month:'2-digit',year:'2-digit'});}
function fmtDur(m){if(!m)return'\u2014';const h=Math.floor(m/60),mn=m%60;return h?`${h}h ${mn}m`:`${mn}m`;}
function setVal(id,val,cls){const el=document.getElementById(id);if(el){el.textContent=val;el.className='stat-value '+(cls||'neutral');}}

// ── SESSIONS ──
function renderSessions(){
  const fl=(document.getElementById('session-filter-loc')?.value||'').toLowerCase();
  const fg=document.getElementById('session-filter-game')?.value||'';
  const data=allSessions.filter(s=>(!fl||(s.location||'').toLowerCase().includes(fl))&&(!fg||s.game_type===fg));
  const tbody=document.getElementById('session-table');
  const empty=document.getElementById('sessions-empty');
  if(!data.length){tbody.innerHTML='';empty.style.display='block';return;}
  empty.style.display='none';
  tbody.innerHTML=data.map(s=>{
    const p=s.profit,cls=p>0?'profit-pos':p<0?'profit-neg':'';
    return`<tr><td>${fmtDate(s.date)}</td><td>${s.location||'\u2014'}</td><td>${s.game_type}</td><td>${s.stakes||'\u2014'}</td><td>$${s.buy_in}</td><td>$${s.cash_out}</td><td class="${cls}">${fmtMoney(p)}</td><td>${fmtDur(s.duration_minutes)}</td><td style="white-space:nowrap"><button class="btn btn-ghost btn-sm" onclick="openSessionModal(${s.id})">&#9998;</button><button class="btn btn-danger btn-sm" onclick="deleteSession(${s.id})">&#10005;</button></td></tr>`;
  }).join('');
}

function renderRecentSessions(){
  const tbody=document.getElementById('recent-sessions');
  const data=allSessions.slice(0,5);
  if(!data.length){tbody.innerHTML='<tr><td colspan="6" style="color:var(--muted);text-align:center;padding:1rem">Noch keine Sessions</td></tr>';return;}
  tbody.innerHTML=data.map(s=>{
    const p=s.profit,cls=p>0?'profit-pos':p<0?'profit-neg':'';
    return`<tr><td>${fmtDate(s.date)}</td><td>${s.location||'\u2014'}</td><td>${s.game_type}</td><td>$${s.buy_in}</td><td>$${s.cash_out}</td><td class="${cls}">${fmtMoney(p)}</td></tr>`;
  }).join('');
}

function openSessionModal(id=null){
  editingSessionId=id;
  document.getElementById('session-modal-title').textContent=id?'Cash Game bearbeiten':'Cash Game erfassen';
  if(id){const s=allSessions.find(x=>x.id===id);document.getElementById('s-date').value=s.date;document.getElementById('s-location').value=s.location||'';document.getElementById('s-game').value=s.game_type;document.getElementById('s-stakes').value=s.stakes||'';document.getElementById('s-buyin').value=s.buy_in;document.getElementById('s-cashout').value=s.cash_out;document.getElementById('s-duration').value=s.duration_minutes||'';document.getElementById('s-notes').value=s.notes||'';}
  else{document.getElementById('s-date').value=new Date().toISOString().split('T')[0];['s-location','s-buyin','s-cashout','s-duration','s-notes'].forEach(i=>document.getElementById(i).value='');}
  openModal('session-modal');
}

async function saveSession(){
  const body={date:document.getElementById('s-date').value,location:document.getElementById('s-location').value||null,game_type:document.getElementById('s-game').value,stakes:document.getElementById('s-stakes').value||null,buy_in:parseFloat(document.getElementById('s-buyin').value),cash_out:parseFloat(document.getElementById('s-cashout').value),duration_minutes:parseInt(document.getElementById('s-duration').value)||null,notes:document.getElementById('s-notes').value||null};
  try{if(editingSessionId)await api(`/sessions/${editingSessionId}`,'PUT',body);else await api('/sessions/','POST',body);closeModal('session-modal');await loadSessions();renderDashboard();}
  catch(e){alert('Fehler: '+(e.detail||JSON.stringify(e)));}
}

async function deleteSession(id){if(!confirm('Cash Game l\u00f6schen?'))return;await api(`/sessions/${id}`,'DELETE');await loadSessions();renderDashboard();}

// ── DASHBOARD CHART ──
function renderDashboard(){
  const sorted=[...allSessions].sort((a,b)=>a.date.localeCompare(b.date));
  let cum=0;const points=sorted.map(s=>{cum+=s.profit;return cum;});
  drawLineChart('bankroll-chart',points);
  if(allSessions.length){
    const profits=allSessions.map(s=>s.profit);
    const tp=profits.reduce((a,b)=>a+b,0);
    const tbi=allSessions.reduce((a,s)=>a+s.buy_in,0);
    const wins=profits.filter(p=>p>0);
    setVal('s-total-profit','$'+(tp>=0?'+':'')+tp.toFixed(0),tp>0?'pos':tp<0?'neg':'neutral');
    setVal('s-sessions',allSessions.length,'neutral');
    setVal('s-winrate',(wins.length/profits.length*100).toFixed(1)+'%',wins.length/profits.length>=0.5?'pos':'neg');
    setVal('s-roi',tbi>0?(tp/tbi*100).toFixed(1)+'%':'\u2014',tp>0?'pos':tp<0?'neg':'neutral');
    setVal('s-avg',fmtMoney(tp/profits.length),tp>=0?'pos':'neg');
    const hrs=allSessions.reduce((a,s)=>a+(s.duration_minutes||0),0)/60;
    setVal('s-hr',hrs>0?fmtMoney(tp/hrs)+'/h':'\u2014',tp>=0?'pos':'neg');
    setVal('s-bigwin','+$'+Math.max(...profits).toFixed(0),'pos');
    setVal('s-bigloss','$'+Math.min(...profits).toFixed(0),'neg');
  }
}

function drawLineChart(id,data){
  const canvas=document.getElementById(id);if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const W=canvas.offsetWidth||600,H=canvas.offsetHeight||120;
  canvas.width=W;canvas.height=H;ctx.clearRect(0,0,W,H);
  if(!data.length){ctx.fillStyle='#7a8a7a';ctx.font='14px sans-serif';ctx.fillText('Noch keine Daten',W/2-70,H/2);return;}
  const pad=20,mn=Math.min(0,...data),mx=Math.max(0,...data),range=mx-mn||1;
  const toY=v=>H-pad-((v-mn)/range)*(H-2*pad);
  const toX=i=>pad+(i/(data.length-1||1))*(W-2*pad);
  const zy=toY(0);
  ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad,zy);ctx.lineTo(W-pad,zy);ctx.stroke();ctx.setLineDash([]);
  const last=data[data.length-1];
  const grad=ctx.createLinearGradient(0,0,0,H);
  if(last>=0){grad.addColorStop(0,'rgba(45,143,78,.3)');grad.addColorStop(1,'rgba(45,143,78,0)');}
  else{grad.addColorStop(0,'rgba(192,57,43,0)');grad.addColorStop(1,'rgba(192,57,43,.25)');}
  ctx.beginPath();ctx.moveTo(toX(0),toY(data[0]));
  data.forEach((v,i)=>ctx.lineTo(toX(i),toY(v)));
  ctx.lineTo(toX(data.length-1),H);ctx.lineTo(toX(0),H);ctx.closePath();
  ctx.fillStyle=grad;ctx.fill();
  ctx.beginPath();ctx.lineWidth=2;ctx.strokeStyle=last>=0?'#2d8f4e':'#c0392b';
  ctx.moveTo(toX(0),toY(data[0]));data.forEach((v,i)=>ctx.lineTo(toX(i),toY(v)));ctx.stroke();
  const lx=toX(data.length-1),ly=toY(data[data.length-1]);
  ctx.beginPath();ctx.arc(lx,ly,4,0,Math.PI*2);ctx.fillStyle=last>=0?'#2d8f4e':'#c0392b';ctx.fill();
}

// ── TOURNAMENTS ──
const MONTHS=['Jan','Feb','M\u00e4r','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'];

function setTFilter(f){
  tournamentFilter=f;
  document.querySelectorAll('[id^="tf-"]').forEach(b=>b.classList.remove('btn-primary'));
  document.getElementById(`tf-${f}`)?.classList.add('btn-primary');
  renderTournaments();
}

function renderTournaments(){
  const today=new Date().toISOString().split('T')[0];
  let data=allTournaments;
  if(tournamentFilter==='upcoming')data=data.filter(t=>!t.start_date||t.start_date>=today);
  else if(tournamentFilter==='entered')data=data.filter(t=>t.entry);
  const list=document.getElementById('tournament-list');
  const empty=document.getElementById('tournaments-empty');
  if(!data.length){list.innerHTML='';empty.style.display='block';return;}
  empty.style.display='none';
  list.innerHTML=data.map(t=>{
    const d=t.start_date?new Date(t.start_date):null;
    const day=d?d.getUTCDate():'?',month=d?MONTHS[d.getUTCMonth()]:'';
    const badge=t.is_global?'<span class="t-badge global-badge">Global</span>':'<span class="t-badge own-badge">Eigenes</span>';
    const typeBadge=t.tournament_type==='Online'?'<span class="t-badge" style="background:#0d1a2a;color:#5b9bd5">Online</span>':'';
    const entry=t.entry?`<div class="entry-result ${t.entry.prize_money>0?'won':''}">&#10003; Angemeldet${t.entry.result_position?` \u00b7 Platz ${t.entry.result_position}`:''}${t.entry.prize_money>0?` \u00b7 $${t.entry.prize_money}`:''}${t.entry.reentries>0?` \u00b7 ${t.entry.reentries}x Reentry`:''}</div>`:'';
    const canEdit=t.created_by_name===currentUser.name||currentUser.is_admin;
    const editBtns=canEdit?`<button class="btn btn-ghost btn-sm" onclick="openTournamentModal(${t.id})">&#9998;</button><button class="btn btn-danger btn-sm" onclick="deleteTournament(${t.id})">&#10005;</button>`:'';
    return`<div class="tournament-item ${t.is_global?'global':'personal'}">
      <div class="t-date"><div class="t-date-day">${day}</div><div class="t-date-month">${month}</div></div>
      <div class="t-info">
        <div style="display:flex;align-items:center;gap:.5rem;flex-wrap:wrap"><span class="t-name">${t.name}</span>${badge}${typeBadge}</div>
        <div class="t-meta">${t.series?`<span class="t-series">${t.series}</span> \u00b7 `:''}${t.location||''}${t.buy_in?` \u00b7 <span class="t-buyin">$${t.buy_in}</span>`:''} \u00b7 ${t.game_type}${t.end_date&&t.end_date!==t.start_date?` \u00b7 bis ${fmtDate(t.end_date)}`:''}</div>
        ${entry}
      </div>
      <div class="t-actions">
        <button class="btn ${t.entry?'btn-ghost':'btn-gold'} btn-sm" onclick="openEntryModal(${t.id})">${t.entry?'Ergebnis':'+ Anmelden'}</button>
        <div style="display:flex;gap:.3rem">${editBtns}</div>
      </div>
    </div>`;
  }).join('');
}

function openTournamentModal(id=null){
  editingTournamentId=id;
  document.getElementById('tournament-modal-title').textContent=id?'Turnier bearbeiten':'Turnier hinzuf\u00fcgen';
  document.getElementById('global-toggle').style.display=currentUser.is_admin?'block':'none';
  if(id){const t=allTournaments.find(x=>x.id===id);document.getElementById('t-name').value=t.name;document.getElementById('t-series').value=t.series||'';document.getElementById('t-location').value=t.location||'';document.getElementById('t-start').value=t.start_date||'';document.getElementById('t-end').value=t.end_date||'';document.getElementById('t-buyin').value=t.buy_in||'';document.getElementById('t-fieldsize').value=t.field_size||'';document.getElementById('t-game').value=t.game_type;document.getElementById('t-global').checked=t.is_global;document.getElementById('t-type').value=t.tournament_type||'Live';}
  else{['t-name','t-series','t-location','t-start','t-end','t-buyin','t-fieldsize'].forEach(i=>document.getElementById(i).value='');document.getElementById('t-global').checked=false;document.getElementById('t-type').value='Live';}
  openModal('tournament-modal');
}

async function saveTournament(){
  const body={name:document.getElementById('t-name').value,series:document.getElementById('t-series').value||null,location:document.getElementById('t-location').value||null,start_date:document.getElementById('t-start').value||null,end_date:document.getElementById('t-end').value||null,buy_in:parseFloat(document.getElementById('t-buyin').value)||null,field_size:parseInt(document.getElementById('t-fieldsize').value)||null,game_type:document.getElementById('t-game').value,tournament_type:document.getElementById('t-type').value,is_global:document.getElementById('t-global').checked};
  try{if(editingTournamentId)await api(`/tournaments/${editingTournamentId}`,'PUT',body);else await api('/tournaments/','POST',body);closeModal('tournament-modal');await loadTournaments();}
  catch(e){alert('Fehler: '+(e.detail||JSON.stringify(e)));}
}

async function deleteTournament(id){if(!confirm('Turnier l\u00f6schen?'))return;await api(`/tournaments/${id}`,'DELETE');await loadTournaments();}

function updateTotalCost(){
  const t=allTournaments.find(x=>x.id===entryTournamentId);
  if(!t||!t.buy_in)return;
  const re=parseInt(document.getElementById('e-reentries').value)||0;
  const total=t.buy_in*(re+1);
  document.getElementById('e-total-cost').textContent=`Gesamt Buy-in: $${total}`;
}

function openEntryModal(tid){
  entryTournamentId=tid;
  const t=allTournaments.find(x=>x.id===tid);
  document.getElementById('entry-modal-title').textContent=t.name;
  const rb=document.getElementById('entry-remove-btn');
  if(t.entry){
    document.getElementById('e-position').value=t.entry.result_position||'';
    document.getElementById('e-prize').value=t.entry.prize_money||0;
    document.getElementById('e-reentries').value=t.entry.reentries||0;
    document.getElementById('e-notes').value=t.entry.notes||'';
    rb.style.display='block';
  }else{
    document.getElementById('e-position').value='';
    document.getElementById('e-prize').value='0';
    document.getElementById('e-reentries').value='0';
    document.getElementById('e-notes').value='';
    rb.style.display='none';
  }
  setTimeout(updateTotalCost,50);
  openModal('entry-modal');
}

async function saveEntry(){
  const posVal=document.getElementById('e-position').value.trim();
  if(posVal!==''&&(isNaN(parseInt(posVal))||parseInt(posVal)<1)){
    alert('Platzierung muss eine positive Zahl sein (oder leer lassen).');return;
  }
  const body={result_position:posVal?parseInt(posVal):null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,reentries:parseInt(document.getElementById('e-reentries').value)||0,notes:document.getElementById('e-notes').value||null};
  try{
    await api(`/tournaments/${entryTournamentId}/entry`,'PUT',body);
  }catch(e){
    alert('Fehler beim Speichern: '+(e.detail||JSON.stringify(e)));
    return;
  }
  closeModal('entry-modal');
  try{ await loadTournaments(); }catch(e){ console.error('Render error:',e); location.reload(); }
}
async function removeEntry(){if(!confirm('Anmeldung entfernen?'))return;await api(`/tournaments/${entryTournamentId}/entry`,'DELETE');closeModal('entry-modal');await loadTournaments();}

// ── RANGLISTE ──
async function loadRangliste(){
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
      leadEl.innerHTML=`&#128081; <span class="challenge-lead-name">${ch.leader_name}</span> f\u00fchrt mit <span class="challenge-lead-gap profit-pos">${fmtMoney(ch.gap)}</span> Vorsprung`;
    }else if(ch.leader_name && ch.gap===0){
      leadEl.innerHTML='&#129309; Beide gleichauf \u2014 noch ist alles offen!';
    }else{
      leadEl.innerHTML='Noch keine Ergebnisse eingetragen.';
    }
  }

  const rankIcons=['&#127947;','&#129352;','&#129353;'];
  document.getElementById('lb-rows').innerHTML=data.leaderboard.map((u,i)=>{
    const pCls=u.total_profit>0?'profit-pos':u.total_profit<0?'profit-neg':'';
    const rCls=u.roi>0?'profit-pos':u.roi<0?'profit-neg':'';
    const badgesHtml=(u.badges||[]).map(b=>
      `<span class="badge-chip" title="${b.detail||b.label}">${b.icon} ${b.label} <span class="badge-count">${b.count}</span></span>`
    ).join('');
    return`<div class="lb-row" style="flex-direction:column;align-items:stretch;display:flex;gap:.4rem">
      <div style="display:grid;grid-template-columns:2rem 1fr repeat(3,5rem);gap:.5rem;align-items:center">
        <div class="lb-rank ${i===0?'r1':i===1?'r2':i===2?'r3':''}">${i<3?rankIcons[i]:i+1}</div>
        <div class="lb-name">${u.name}</div>
        <div class="lb-val ${pCls}">${fmtMoney(u.total_profit)}</div>
        <div class="lb-val ${rCls}">${u.roi}%</div>
        <div class="lb-val">${u.itm_rate}%</div>
      </div>
      ${badgesHtml?`<div class="player-badges">${badgesHtml}</div>`:''}
      ${(u.form&&u.form.length)?`<div class="form-row"><span class="form-label-mini">Form</span>${u.form.map(f=>`<span class="form-dot ${f.itm?'itm':'bust'}" title="${fmtDate(f.date)}: ${fmtMoney(f.profit)}"></span>`).join('')}</div>`:''}
    </div>`;
  }).join('');

  checkMilestone(data.challenge);

  // Head-to-Head ITM Score
  const h2hBox=document.getElementById('h2h-itm-box');
  if(data.h2h_itm){
    h2hBox.style.display='flex';
    document.getElementById('h2h-itm-score').innerHTML=
      `${data.h2h_itm.a_name} <span style="color:var(--gold)">${data.h2h_itm.a_itm}</span><span class="vs">:</span><span style="color:var(--gold)">${data.h2h_itm.b_itm}</span> ${data.h2h_itm.b_name}`;
  }else{
    h2hBox.style.display='none';
  }
  document.getElementById('shared-tournaments').innerHTML=data.tournaments.map(t=>{
    const winner=t.players.reduce((a,b)=>{if(!a.position)return b;if(!b.position)return a;return a.position<b.position?a:b;},t.players[0]);
    return`<div class="shared-tournament">
      <div class="shared-t-header">
        <div><span class="shared-t-name">${t.name}</span>${winner&&winner.position?`<span class="winner-badge">&#127942; ${winner.name}</span>`:''}</div>
        <div class="shared-t-meta">${t.start_date?fmtDate(t.start_date):''} &middot; Buy-in $${t.buy_in}</div>
      </div>
      <div class="shared-players">
        ${t.players.map(p=>`<div class="shared-player">
          <div class="shared-player-name">${p.name}</div>
          <div class="shared-player-pos">${p.position?(t.field_size?'#'+p.position+' / '+t.field_size:'#'+p.position):'\u2014'}</div>
          ${p.prize_money>0?`<div class="shared-player-prize">$${p.prize_money} Preisgeld</div>`:''}
          <div class="shared-player-profit ${p.profit>0?'profit-pos':p.profit<0?'profit-neg':''}">${fmtMoney(p.profit)}</div>
        </div>`).join('')}
      </div>
    </div>`;
  }).join('');
}

// ── STATS ──
function calcSummary(sessions){
  if(!sessions.length)return{total_sessions:0,total_profit:0,total_buy_in:0,win_rate:0,roi:0,avg_profit_per_session:0,total_hours:0,profit_per_hour:0,biggest_win:0,biggest_loss:0,current_streak:0};
  const profits=sessions.map(s=>s.profit);
  const tp=profits.reduce((a,b)=>a+b,0);
  const tbi=sessions.reduce((a,s)=>a+s.buy_in,0);
  const wins=profits.filter(p=>p>0);
  const hrs=sessions.reduce((a,s)=>a+(s.duration_minutes||0),0)/60;
  const sorted=[...sessions].sort((a,b)=>b.date.localeCompare(a.date)).map(s=>s.profit);
  let streak=0;
  if(sorted.length){const sign=sorted[0]>=0?1:-1;for(const p of sorted){if((p>=0&&sign===1)||(p<0&&sign===-1))streak+=sign;else break;}}
  return{total_sessions:sessions.length,total_profit:Math.round(tp*100)/100,total_buy_in:Math.round(tbi*100)/100,win_rate:Math.round(wins.length/sessions.length*1000)/10,roi:tbi>0?Math.round(tp/tbi*1000)/10:0,avg_profit_per_session:Math.round(tp/sessions.length*100)/100,total_hours:Math.round(hrs*10)/10,profit_per_hour:hrs>0?Math.round(tp/hrs*100)/100:0,biggest_win:Math.round(Math.max(...profits)*100)/100,biggest_loss:Math.round(Math.min(...profits)*100)/100,current_streak:streak};
}

function calcMonthly(sessions){
  const m={};
  for(const s of sessions){const k=s.date.slice(0,7);if(!m[k])m[k]={profit:0,sessions:0,buy_in:0};m[k].profit+=s.profit;m[k].sessions++;m[k].buy_in+=s.buy_in;}
  return Object.entries(m).sort().map(([month,v])=>({month,...v}));
}

function resetStatsFilter(){document.getElementById('stats-from').value='';document.getElementById('stats-to').value='';document.getElementById('stats-location').value='';loadStats();}

async function loadStats(){
  const from=document.getElementById('stats-from')?.value||'';
  const to=document.getElementById('stats-to')?.value||'';
  const loc=document.getElementById('stats-location')?.value||'';
  let filtered=allSessions;
  if(from)filtered=filtered.filter(s=>s.date>=from);
  if(to)filtered=filtered.filter(s=>s.date<=to);
  // Location-Filter fuer Turnier-Stats wird weiter unten angewandt
  const sum=calcSummary(filtered);
  const monthly=calcMonthly(filtered);
  // Filter-Parameter an Backend uebergeben fuer exakte Berechnung inkl. ITM
  const tsParams=new URLSearchParams();
  if(loc) tsParams.set('tournament_type',loc);
  if(from) tsParams.set('from_date',from);
  if(to) tsParams.set('to_date',to);
  const tsUrl='/stats/tournaments'+(tsParams.toString()?'?'+tsParams.toString():'');
  const ts=await api(tsUrl);
  const p=sum.total_profit;
  setVal('s-total-profit','$'+(p>=0?'+':'')+p.toFixed(0),p>0?'pos':p<0?'neg':'neutral');
  setVal('s-sessions',sum.total_sessions,'neutral');
  setVal('s-winrate',sum.win_rate+'%',sum.win_rate>=50?'pos':'neg');
  setVal('s-roi',sum.roi+'%',sum.roi>0?'pos':sum.roi<0?'neg':'neutral');
  setVal('s-avg',fmtMoney(sum.avg_profit_per_session),sum.avg_profit_per_session>=0?'pos':'neg');
  setVal('s-hr',fmtMoney(sum.profit_per_hour)+'/h',sum.profit_per_hour>=0?'pos':'neg');
  setVal('s-bigwin','+$'+sum.biggest_win,'pos');
  setVal('s-bigloss','$'+sum.biggest_loss,'neg');
  // Backend liefert bereits gefilterte Werte - direkt anzeigen
  document.getElementById('ts-entered').textContent=ts.total_entered;
  document.getElementById('ts-invested').textContent='$'+parseFloat(ts.total_invested).toFixed(0);
  document.getElementById('ts-winnings').textContent='$'+parseFloat(ts.total_winnings).toFixed(2);
  const tp=parseFloat(ts.tournament_profit);
  setVal('ts-profit',(tp>=0?'+':'')+'$'+Math.abs(tp).toFixed(2),tp>0?'pos':tp<0?'neg':'neutral');
  document.getElementById('ts-itm').textContent=ts.total_entered>0?ts.itm_rate+'%':'0%';
  drawMonthlyChart('monthly-chart',monthly);

}

function drawMonthlyChart(id,data){
  const canvas=document.getElementById(id);if(!canvas||!data.length)return;
  const W=canvas.offsetWidth||700,H=160;canvas.width=W;canvas.height=H;
  const ctx=canvas.getContext('2d');ctx.clearRect(0,0,W,H);
  const profits=data.map(d=>d.profit),mx=Math.max(0,...profits),mn=Math.min(0,...profits),range=mx-mn||1;
  const pad={top:10,bottom:30,left:10,right:10};
  const bw=Math.max(10,(W-pad.left-pad.right)/data.length-4);
  const toY=v=>pad.top+((mx-v)/range)*(H-pad.top-pad.bottom),zy=toY(0);
  ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad.left,zy);ctx.lineTo(W-pad.right,zy);ctx.stroke();ctx.setLineDash([]);
  data.forEach((d,i)=>{
    const x=pad.left+i*((W-pad.left-pad.right)/data.length)+2;
    const p=d.profit,barH=Math.abs(toY(p)-zy),y=p>=0?zy-barH:zy;
    ctx.fillStyle=p>=0?'#2d8f4e':'#c0392b';ctx.fillRect(x,y,bw,Math.max(2,barH));
    ctx.fillStyle='#7a8a7a';ctx.font='10px sans-serif';ctx.fillText(d.month.slice(5),x+bw/2-10,H-6);
  });
}

// ── ADMIN ──
async function createUser(){
  const name=document.getElementById('new-user-name').value.trim();
  const pin=document.getElementById('new-user-pin').value.trim();
  const is_admin=document.getElementById('new-user-admin').checked;
  const msg=document.getElementById('create-user-msg');
  if(!name||pin.length<4){msg.style.color='var(--red)';msg.textContent='Name und 4-stellige PIN erforderlich';return;}
  try{await api('/auth/users','POST',{name,pin,is_admin});msg.style.color='var(--green-hi)';msg.textContent=`\u2713 Nutzer "${name}" angelegt`;document.getElementById('new-user-name').value='';document.getElementById('new-user-pin').value='';}
  catch(e){msg.style.color='var(--red)';msg.textContent=e.detail||'Fehler';}
}

// ── MODALS ──
function openModal(id){document.getElementById(id).classList.add('open');}
function closeModal(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.modal-overlay').forEach(m=>m.addEventListener('click',e=>{if(e.target===m)m.classList.remove('open');}));


// ── GESAMT ──
function resetGesamtFilter(){document.getElementById('gesamt-from').value='';document.getElementById('gesamt-to').value='';loadGesamt();}

async function loadGesamt(){
  const from=document.getElementById('gesamt-from')?.value||'';
  const to=document.getElementById('gesamt-to')?.value||'';
  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';

  // Alle Daten vom Server holen
  const combined=await api('/stats/combined');

  // Monatsdaten filtern
  let monthly=combined.monthly;
  if(fromMonth) monthly=monthly.filter(m=>m.month>=fromMonth);
  if(toMonth) monthly=monthly.filter(m=>m.month<=toMonth);

  // Alles aus den monatlichen Daten berechnen
  const cashProfit=monthly.reduce((a,m)=>a+m.cash_profit,0);
  const cashInvested=monthly.reduce((a,m)=>a+m.cash_invested,0);
  const cashSessions=monthly.reduce((a,m)=>a+m.cash_sessions,0);
  const tProfit=monthly.reduce((a,m)=>a+m.tournament_profit,0);
  const tInvested=monthly.reduce((a,m)=>a+m.tournament_invested,0);
  const tCount=monthly.reduce((a,m)=>a+m.tournament_count,0);
  const totalProfit=cashProfit+tProfit;
  const totalInvested=cashInvested+tInvested;
  const roi=totalInvested>0?Math.round(totalProfit/totalInvested*1000)/10:0;

  // Stunden aus allSessions (clientseitig filtern)
  let filteredSessions=allSessions;
  if(from) filteredSessions=filteredSessions.filter(s=>s.date>=from);
  if(to) filteredSessions=filteredSessions.filter(s=>s.date<=to);
  const cashHours=filteredSessions.reduce((a,s)=>a+(s.duration_minutes||0),0)/60;

  const cls=v=>v>0?'pos':v<0?'neg':'neutral';
  setVal('g-total','$'+(totalProfit>=0?'+':'')+totalProfit.toFixed(0),cls(totalProfit));
  setVal('g-cash','$'+(cashProfit>=0?'+':'')+cashProfit.toFixed(0),cls(cashProfit));
  setVal('g-tourney','$'+(tProfit>=0?'+':'')+tProfit.toFixed(0),cls(tProfit));
  setVal('g-invested','$'+totalInvested.toFixed(0),'neutral');
  setVal('g-roi',roi+'%',cls(roi));
  setVal('g-hours',cashHours.toFixed(1)+'h','neutral');
  setVal('g-sessions',cashSessions,'neutral');
  setVal('g-tournaments',tCount,'neutral');

  // Zeitlicher Verlauf-Chart
  const timeline=await api('/stats/timeline');
  let filtTimeline=timeline;
  if(from) filtTimeline=filtTimeline.filter(e=>e.date>=from);
  if(to) filtTimeline=filtTimeline.filter(e=>e.date<=to);
  drawTimelineChart('gesamt-chart',filtTimeline);
}

function drawTimelineChart(id,events){
  const canvas=document.getElementById(id);if(!canvas)return;
  const W=canvas.offsetWidth||700,H=220;canvas.width=W;canvas.height=H;
  const ctx=canvas.getContext('2d');ctx.clearRect(0,0,W,H);
  if(!events.length){
    ctx.fillStyle='#7a8a7a';ctx.font='14px sans-serif';
    ctx.fillText('Noch keine Daten',W/2-70,H/2);return;
  }

  // Kumulative Punkte berechnen
  let cumCash=0,cumT=0,cumTotal=0;
  const pts=[{date:'',cash:0,tournament:0,total:0}];
  events.forEach(e=>{
    if(e.type==='cash') cumCash+=e.profit;
    else cumT+=e.profit;
    cumTotal+=e.profit;
    pts.push({date:e.date,cash:cumCash,tournament:cumT,total:cumTotal,label:e.label,type:e.type});
  });

  const allVals=pts.flatMap(p=>[p.cash,p.tournament,p.total,0]);
  const mx=Math.max(...allVals),mn=Math.min(...allVals),range=mx-mn||1;

  // Y-Achse Beschriftung: sinnvolle Schrittweite berechnen
  const yAxisW=52;
  const pad={top:15,bottom:30,left:yAxisW,right:12};
  const toY=v=>pad.top+((mx-v)/range)*(H-pad.top-pad.bottom);
  const toX=i=>pad.left+(i/(pts.length-1||1))*(W-pad.left-pad.right);
  const zy=toY(0);

  // Y-Achsen-Gridlines und Labels
  const nTicks=5;
  const step=(mx-mn)/nTicks;
  ctx.font='10px sans-serif';
  for(let i=0;i<=nTicks;i++){
    const val=mn+step*i;
    const y=toY(val);
    // Gridline
    ctx.strokeStyle='#1e2e1e';ctx.lineWidth=1;ctx.setLineDash([2,4]);
    ctx.beginPath();ctx.moveTo(pad.left,y);ctx.lineTo(W-pad.right,y);ctx.stroke();
    ctx.setLineDash([]);
    // Label
    const label=(val>=0?'+':'')+Math.round(val)+'$';
    ctx.fillStyle=val>0?'#3db866':val<0?'#c0392b':'#7a8a7a';
    ctx.textAlign='right';
    ctx.fillText(label,yAxisW-4,y+3.5);
  }
  ctx.textAlign='left';

  // Nulllinie
  ctx.strokeStyle='#3a4a3a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad.left,zy);ctx.lineTo(W-pad.right,zy);ctx.stroke();
  ctx.setLineDash([]);

  function drawLine(key,color,width=2){
    ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=width;
    pts.forEach((p,i)=>{
      i===0?ctx.moveTo(toX(i),toY(p[key])):ctx.lineTo(toX(i),toY(p[key]));
    });
    ctx.stroke();
    const last=pts[pts.length-1];
    ctx.beginPath();ctx.arc(toX(pts.length-1),toY(last[key]),4,0,Math.PI*2);
    ctx.fillStyle=color;ctx.fill();
    // Endwert-Label
    const labelVal=(last[key]>=0?'+':'')+Math.round(last[key])+'$';
    ctx.fillStyle=color;ctx.font='bold 10px sans-serif';ctx.textAlign='left';
    ctx.fillText(labelVal,toX(pts.length-1)+6,toY(last[key])+4);
    ctx.font='10px sans-serif';
  }

  drawLine('cash','#2d8f4e');
  drawLine('tournament','#c9a84c');
  drawLine('total','#e8e8e4',2.5);

  // Event-Markierungen
  pts.slice(1).forEach((p,i)=>{
    const x=toX(i+1);
    const color=p.type==='cash'?'#2d8f4e':'#c9a84c';
    ctx.beginPath();ctx.fillStyle=color;
    ctx.moveTo(x,H-pad.bottom+2);ctx.lineTo(x-3,H-pad.bottom+9);ctx.lineTo(x+3,H-pad.bottom+9);
    ctx.closePath();ctx.fill();
  });

  // Datum-Labels
  ctx.fillStyle='#7a8a7a';ctx.font='10px sans-serif';ctx.textAlign='left';
  if(pts.length>1){
    ctx.fillText(pts[1].date.slice(5),toX(1)-10,H-4);
    if(pts.length>2) ctx.fillText(pts[pts.length-1].date.slice(5),toX(pts.length-1)-10,H-4);
  }
}


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
    50:'Die H\u00e4lfte ist geschafft \u2014 weiter so!',
    75:'Nur noch 25 Turniere bis zum Ziel.',
    100:`${challenge.leader_name||''} liegt aktuell vorne. Zeit f\u00fcr die Abrechnung! &#127942;`
  };
  document.getElementById('milestone-title').textContent=titles[n];
  document.getElementById('milestone-sub').innerHTML=subs[n];
  document.querySelector('.milestone-icon').textContent=n===100?'\u{1F3C6}':'\u{1F389}';
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

// ── INIT ──
fetchUsers();
if(token&&currentUser){enterApp();}else{document.getElementById('login-screen').style.display='flex';}
window.addEventListener('resize',()=>{if(allSessions.length)renderDashboard();});
setTFilter('all');

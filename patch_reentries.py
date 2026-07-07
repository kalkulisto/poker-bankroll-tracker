path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Entry-Modal: Reentries-Feld ergaenzen
old_modal = '''    <div class="form-grid">
      <div class="form-group"><label class="form-label">Platzierung</label><input class="form-input" type="number" id="e-position" min="1" placeholder="z.B. 47"></div>
      <div class="form-group"><label class="form-label">Preisgeld ($)</label><input class="form-input" type="number" id="e-prize" min="0" step="1" value="0"></div>
      <div class="form-group full"><label class="form-label">Notizen</label><textarea class="form-textarea" id="e-notes" placeholder="z.B. Day 2 erreicht, busted KK vs AA..."></textarea></div>
    </div>'''

new_modal = '''    <div class="form-grid">
      <div class="form-group"><label class="form-label">Platzierung</label><input class="form-input" type="number" id="e-position" min="1" placeholder="z.B. 47"></div>
      <div class="form-group"><label class="form-label">Preisgeld ($)</label><input class="form-input" type="number" id="e-prize" min="0" step="1" value="0"></div>
      <div class="form-group"><label class="form-label">Reentries</label><input class="form-input" type="number" id="e-reentries" min="0" step="1" value="0" placeholder="0 = kein Reentry"></div>
      <div class="form-group" style="display:flex;align-items:flex-end;padding-bottom:.2rem">
        <span id="e-total-cost" style="font-size:.8rem;color:var(--muted)"></span>
      </div>
      <div class="form-group full"><label class="form-label">Notizen</label><textarea class="form-textarea" id="e-notes" placeholder="z.B. Day 2 erreicht, busted KK vs AA..."></textarea></div>
    </div>'''

c = c.replace(old_modal, new_modal, 1)

# 2. openEntryModal: reentries befuellen + total cost anzeigen
old_open = '''function openEntryModal(tid){
  entryTournamentId=tid;
  const t=allTournaments.find(x=>x.id===tid);
  document.getElementById('entry-modal-title').textContent=t.name;
  const rb=document.getElementById('entry-remove-btn');
  if(t.entry){document.getElementById('e-position').value=t.entry.result_position||'';document.getElementById('e-prize').value=t.entry.prize_money||0;document.getElementById('e-notes').value=t.entry.notes||'';rb.style.display='block';}
  else{document.getElementById('e-position').value='';document.getElementById('e-prize').value='0';document.getElementById('e-notes').value='';rb.style.display='none';}
  openModal('entry-modal');
}'''

new_open = '''function updateTotalCost(){
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
}'''

c = c.replace(old_open, new_open, 1)

# 3. saveEntry: reentries mitsenden
old_save = "async function saveEntry(){const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,notes:document.getElementById('e-notes').value||null};"
new_save = "async function saveEntry(){const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,reentries:parseInt(document.getElementById('e-reentries').value)||0,notes:document.getElementById('e-notes').value||null};"

c = c.replace(old_save, new_save, 1)

# 4. Reentries-Anzeige in der Turnier-Liste (entry-result)
old_entry_display = "entry=t.entry?`<div class=\"entry-result ${t.entry.prize_money>0?'won':''}\">&#10003; Angemeldet${t.entry.result_position?` \\u00b7 Platz ${t.entry.result_position}`:''}${t.entry.prize_money>0?` \\u00b7 $${t.entry.prize_money}`:''}</div>`:''"
new_entry_display = "entry=t.entry?`<div class=\"entry-result ${t.entry.prize_money>0?'won':''}\">&#10003; Angemeldet${t.entry.result_position?` \\u00b7 Platz ${t.entry.result_position}`:''}${t.entry.prize_money>0?` \\u00b7 $${t.entry.prize_money}`:''}${t.entry.reentries>0?` \\u00b7 ${t.entry.reentries}x Reentry`:''}</div>`:'')"

if old_entry_display in c:
    c = c.replace(old_entry_display, new_entry_display, 1)
    print('entry display patched')
else:
    print('entry display NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

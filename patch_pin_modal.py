path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Modal HTML vor </body> einfuegen
modal = '''
<!-- MODAL: PIN ändern (Erstlogin) -->
<div class="modal-overlay" id="pin-change-modal">
  <div class="modal" style="max-width:360px">
    <div class="modal-title"><span>PIN festlegen</span></div>
    <p style="font-size:0.875rem;color:var(--muted);margin-bottom:1.25rem">Bitte leg einen eigenen PIN fest bevor du loslegst.</p>
    <div class="form-grid">
      <div class="form-group full"><label class="form-label">Neuer PIN (4 Ziffern)</label><input class="form-input" type="password" id="new-pin-1" maxlength="4" placeholder="&#8226;&#8226;&#8226;&#8226;" inputmode="numeric"></div>
      <div class="form-group full"><label class="form-label">PIN wiederholen</label><input class="form-input" type="password" id="new-pin-2" maxlength="4" placeholder="&#8226;&#8226;&#8226;&#8226;" inputmode="numeric"></div>
    </div>
    <div id="pin-change-error" style="font-size:0.85rem;color:var(--red);min-height:1.2rem;margin-top:0.5rem"></div>
    <div class="modal-footer">
      <button class="btn btn-primary" onclick="saveNewPin()">PIN speichern</button>
    </div>
  </div>
</div>'''

sw_tag = '<script>if("serviceWorker"in navigator)'
c = c.replace(sw_tag, modal + '\n' + sw_tag, 1)

# 2. saveNewPin Funktion und enterApp-Patch vor dem letzten </script>
js = '''
async function saveNewPin() {
  const p1 = document.getElementById('new-pin-1').value;
  const p2 = document.getElementById('new-pin-2').value;
  const err = document.getElementById('pin-change-error');
  if(p1.length < 4){ err.textContent='PIN muss 4 Ziffern haben'; return; }
  if(p1 !== p2){ err.textContent='PINs stimmen nicht \u00fcberein'; return; }
  try {
    await api(`/auth/users/${currentUser.id}/pin`, 'PUT', {new_pin: p1});
    currentUser.pin_changed = true;
    localStorage.setItem('poker_user', JSON.stringify(currentUser));
    closeModal('pin-change-modal');
  } catch(e) { err.textContent = 'Fehler beim Speichern'; }
}
'''

c = c.replace('fetchUsers();\n', js + 'fetchUsers();\n', 1)

# 3. enterApp: nach dem Login pruefen ob PIN schon geaendert wurde
old_enter = '''function enterApp() {
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  document.getElementById('header-username').textContent=currentUser.name;
  if(currentUser.is_admin) document.getElementById('admin-section').style.display='block';
  loadAll();
}'''

new_enter = '''function enterApp() {
  document.getElementById('login-screen').style.display='none';
  document.getElementById('app').style.display='block';
  document.getElementById('header-username').textContent=currentUser.name;
  if(currentUser.is_admin) document.getElementById('admin-section').style.display='block';
  loadAll();
  if(currentUser.pin_changed === false) {
    setTimeout(() => openModal('pin-change-modal'), 500);
  }
}'''

c = c.replace(old_enter, new_enter, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

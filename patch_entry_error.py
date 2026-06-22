path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = "async function saveEntry(){const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,notes:document.getElementById('e-notes').value||null};await api(`/tournaments/${entryTournamentId}/entry`,'PUT',body);closeModal('entry-modal');await loadTournaments();}"

new = "async function saveEntry(){const body={result_position:parseInt(document.getElementById('e-position').value)||null,prize_money:parseFloat(document.getElementById('e-prize').value)||0,notes:document.getElementById('e-notes').value||null};try{await api(`/tournaments/${entryTournamentId}/entry`,'PUT',body);closeModal('entry-modal');await loadTournaments();}catch(e){alert('Fehler beim Speichern: '+(e.detail||JSON.stringify(e)));console.error(e);}}"

if old in c:
    c = c.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('patched')
else:
    print('NOT FOUND')

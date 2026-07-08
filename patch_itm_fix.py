path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''  const ts=await api('/stats/tournaments');
  const p=sum.total_profit;'''

new = '''  // Filter-Parameter an Backend uebergeben fuer exakte Berechnung inkl. ITM
  const tsParams=new URLSearchParams();
  if(loc) tsParams.set('tournament_type',loc);
  if(from) tsParams.set('from_date',from);
  if(to) tsParams.set('to_date',to);
  const tsUrl='/stats/tournaments'+(tsParams.toString()?'?'+tsParams.toString():'');
  const ts=await api(tsUrl);
  const p=sum.total_profit;'''

if old in c:
    c = c.replace(old, new, 1)
    print('api call patched')
else:
    print('NOT FOUND')

# Clientseitige Filterlogik vereinfachen - Backend liefert jetzt korrekte Werte
old_filter = '''  // Turnier-Stats nach Zeitraum filtern (exakt auf Tag genau via monthly)
  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';
  const useFilter=!!(from||to||loc);

  // Location-Filter: Turniere nach Location einschraenken, dann Stats neu berechnen
  let tsMonthly=ts.monthly||[];
  if(loc){
    // Typ-Filter (Live/Online): Turniere dieses Typs bestimmen, Monate ermitteln
    const matchMonths=new Set(allTournaments.filter(t=>(t.tournament_type||'Live')===loc&&t.start_date).map(t=>t.start_date.slice(0,7)));
    tsMonthly=tsMonthly.filter(m=>matchMonths.has(m.month));
  }
  if(fromMonth) tsMonthly=tsMonthly.filter(m=>m.month>=fromMonth);
  if(toMonth) tsMonthly=tsMonthly.filter(m=>m.month<=toMonth);
  // Exakte Tagesgrenze: erstes/letztes Monat koennte teilweise ausserhalb liegen
  // Da monthly nur Monat-Granularitaet hat, nutzen wir sie nur wenn kein Tagesfilter im gleichen Monat
  const tsEntered=useFilter?tsMonthly.reduce((a,m)=>a+m.tournaments,0):ts.total_entered;
  const tsInvested=useFilter?tsMonthly.reduce((a,m)=>a+m.invested,0):ts.total_invested;
  const tsProfit=useFilter?tsMonthly.reduce((a,m)=>a+m.profit,0):ts.tournament_profit;
  const tsWinnings=useFilter?(tsInvested+tsProfit):ts.total_winnings;
  const tsItmRate=useFilter?(tsEntered>0?'\u2014':'0%'):ts.itm_rate+'%';
  document.getElementById('ts-entered').textContent=tsEntered;
  document.getElementById('ts-invested').textContent='$'+parseFloat(tsInvested).toFixed(0);
  document.getElementById('ts-winnings').textContent='$'+parseFloat(tsWinnings).toFixed(2);
  const tp=parseFloat(tsProfit);
  setVal('ts-profit',(tp>=0?'+':'')+'$'+Math.abs(tp).toFixed(2),tp>0?'pos':tp<0?'neg':'neutral');
  document.getElementById('ts-itm').textContent=tsItmRate;'''

new_filter = '''  // Backend liefert bereits gefilterte Werte - direkt anzeigen
  document.getElementById('ts-entered').textContent=ts.total_entered;
  document.getElementById('ts-invested').textContent='$'+parseFloat(ts.total_invested).toFixed(0);
  document.getElementById('ts-winnings').textContent='$'+parseFloat(ts.total_winnings).toFixed(2);
  const tp=parseFloat(ts.tournament_profit);
  setVal('ts-profit',(tp>=0?'+':'')+'$'+Math.abs(tp).toFixed(2),tp>0?'pos':tp<0?'neg':'neutral');
  document.getElementById('ts-itm').textContent=ts.total_entered>0?ts.itm_rate+'%':'0%';'''

if old_filter in c:
    c = c.replace(old_filter, new_filter, 1)
    print('filter logic patched')
else:
    print('filter logic NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

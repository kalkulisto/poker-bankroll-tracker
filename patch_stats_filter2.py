path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''  // Turnier-Stats ebenfalls nach Zeitraum filtern (clientseitig via monthly)
  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';
  let tsMonthly=ts.monthly||[];
  if(fromMonth) tsMonthly=tsMonthly.filter(m=>m.month>=fromMonth);
  if(toMonth) tsMonthly=tsMonthly.filter(m=>m.month<=toMonth);
  const tsEntered=tsMonthly.reduce((a,m)=>a+m.tournaments,0);
  const tsInvested=tsMonthly.reduce((a,m)=>a+m.invested,0);
  const tsProfit=tsMonthly.reduce((a,m)=>a+m.profit,0);
  const tsWinnings=tsInvested+tsProfit;
  const tsItm=from||to?'-':ts.itm_rate+'%';
  document.getElementById('ts-entered').textContent=from||to?tsEntered:ts.total_entered;
  document.getElementById('ts-invested').textContent='$'+(from||to?tsInvested.toFixed(0):ts.total_invested);
  document.getElementById('ts-winnings').textContent='$'+(from||to?tsWinnings.toFixed(0):ts.total_winnings);
  const tp=from||to?tsProfit:ts.tournament_profit;
  setVal('ts-profit',(tp>=0?'+':'')+'$'+tp.toFixed(0),tp>0?'pos':tp<0?'neg':'neutral');
  document.getElementById('ts-itm').textContent=from||to?(tsEntered>0?(tsMonthly.reduce((a,m)=>a+m.profit,0)>0?'>0%':'0%'):'0%'):ts.itm_rate+'%';'''

new = '''  // Turnier-Stats nach Zeitraum filtern (exakt auf Tag genau via monthly)
  const fromMonth=from?from.slice(0,7):'';
  const toMonth=to?to.slice(0,7):'';
  const useFilter=!!(from||to);
  let tsMonthly=ts.monthly||[];
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

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

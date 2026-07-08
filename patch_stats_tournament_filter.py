path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old = '''  const ts=await api('/stats/tournaments');
  const p=sum.total_profit;
  setVal('s-total-profit','$'+(p>=0?'+':'')+p.toFixed(0),p>0?'pos':p<0?'neg':'neutral');
  setVal('s-sessions',sum.total_sessions,'neutral');
  setVal('s-winrate',sum.win_rate+'%',sum.win_rate>=50?'pos':'neg');
  setVal('s-roi',sum.roi+'%',sum.roi>0?'pos':sum.roi<0?'neg':'neutral');
  setVal('s-avg',fmtMoney(sum.avg_profit_per_session),sum.avg_profit_per_session>=0?'pos':'neg');
  setVal('s-hr',fmtMoney(sum.profit_per_hour)+'/h',sum.profit_per_hour>=0?'pos':'neg');
  setVal('s-bigwin','+$'+sum.biggest_win,'pos');
  setVal('s-bigloss','$'+sum.biggest_loss,'neg');
  document.getElementById('ts-entered').textContent=ts.total_entered;
  document.getElementById('ts-invested').textContent='$'+ts.total_invested;
  document.getElementById('ts-winnings').textContent='$'+ts.total_winnings;
  const tp=ts.tournament_profit;
  setVal('ts-profit',(tp>=0?'+':'')+'$'+tp,tp>0?'pos':tp<0?'neg':'neutral');
  document.getElementById('ts-itm').textContent=ts.itm_rate+'%';
  drawMonthlyChart('monthly-chart',monthly);'''

new = '''  const ts=await api('/stats/tournaments');
  const p=sum.total_profit;
  setVal('s-total-profit','$'+(p>=0?'+':'')+p.toFixed(0),p>0?'pos':p<0?'neg':'neutral');
  setVal('s-sessions',sum.total_sessions,'neutral');
  setVal('s-winrate',sum.win_rate+'%',sum.win_rate>=50?'pos':'neg');
  setVal('s-roi',sum.roi+'%',sum.roi>0?'pos':sum.roi<0?'neg':'neutral');
  setVal('s-avg',fmtMoney(sum.avg_profit_per_session),sum.avg_profit_per_session>=0?'pos':'neg');
  setVal('s-hr',fmtMoney(sum.profit_per_hour)+'/h',sum.profit_per_hour>=0?'pos':'neg');
  setVal('s-bigwin','+$'+sum.biggest_win,'pos');
  setVal('s-bigloss','$'+sum.biggest_loss,'neg');
  // Turnier-Stats ebenfalls nach Zeitraum filtern (clientseitig via monthly)
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
  document.getElementById('ts-itm').textContent=from||to?(tsEntered>0?(tsMonthly.reduce((a,m)=>a+m.profit,0)>0?'>0%':'0%'):'0%'):ts.itm_rate+'%';
  drawMonthlyChart('monthly-chart',monthly);'''

if old in c:
    c = c.replace(old, new, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

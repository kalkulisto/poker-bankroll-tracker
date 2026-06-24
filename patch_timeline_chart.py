path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# 1. Chart-HTML: Hoehe anpassen + Legende aktualisieren
old_chart_html = '''        <canvas id="gesamt-chart" height="160"></canvas>
        <div style="display:flex;gap:1rem;margin-top:.75rem;font-size:.75rem">
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:12px;background:#2d8f4e;border-radius:2px;display:inline-block"></span>Cash</span>
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:12px;background:#c9a84c;border-radius:2px;display:inline-block"></span>Turniere</span>
        </div>'''

new_chart_html = '''        <canvas id="gesamt-chart" height="200"></canvas>
        <div style="display:flex;gap:1rem;margin-top:.75rem;font-size:.75rem">
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:3px;background:#2d8f4e;display:inline-block;border-radius:2px"></span>Cash</span>
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:3px;background:#c9a84c;display:inline-block;border-radius:2px"></span>Turniere</span>
          <span style="display:flex;align-items:center;gap:.35rem"><span style="width:12px;height:3px;background:#e8e8e4;display:inline-block;border-radius:2px"></span>Gesamt</span>
        </div>'''

c = c.replace(old_chart_html, new_chart_html, 1)

# 2. loadGesamt: timeline statt combined fuer den Chart
old_load = '''  // Kombiniertes Monatsdiagramm
  drawCombinedChart('gesamt-chart',monthly);
}'''

new_load = '''  // Zeitlicher Verlauf-Chart
  const timeline=await api('/stats/timeline');
  let filtTimeline=timeline;
  if(from) filtTimeline=filtTimeline.filter(e=>e.date>=from);
  if(to) filtTimeline=filtTimeline.filter(e=>e.date<=to);
  drawTimelineChart('gesamt-chart',filtTimeline);
}'''

c = c.replace(old_load, new_load, 1)

# 3. drawTimelineChart Funktion - ersetzt drawCombinedChart
old_draw = '''function drawCombinedChart(id,data){
  const canvas=document.getElementById(id);if(!canvas||!data.length)return;
  const W=canvas.offsetWidth||700,H=160;canvas.width=W;canvas.height=H;
  const ctx=canvas.getContext('2d');ctx.clearRect(0,0,W,H);
  const allVals=data.flatMap(d=>[d.cash_profit,d.tournament_profit,0]);
  const mx=Math.max(...allVals),mn=Math.min(...allVals),range=mx-mn||1;
  const pad={top:10,bottom:30,left:10,right:10};
  const slotW=(W-pad.left-pad.right)/data.length;
  const bw=Math.max(6,slotW/2-3);
  const toY=v=>pad.top+((mx-v)/range)*(H-pad.top-pad.bottom),zy=toY(0);
  ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad.left,zy);ctx.lineTo(W-pad.right,zy);ctx.stroke();ctx.setLineDash([]);
  data.forEach((d,i)=>{
    const x=pad.left+i*slotW;
    // Cash (gruen/rot)
    const cp=d.cash_profit,cbh=Math.abs(toY(cp)-zy),cy=cp>=0?zy-cbh:zy;
    ctx.fillStyle=cp>=0?'#2d8f4e':'#c0392b';ctx.fillRect(x+2,cy,bw,Math.max(2,cbh));
    // Turnier (gold/dunkelrot)
    const tp=d.tournament_profit,tbh=Math.abs(toY(tp)-zy),ty=tp>=0?zy-tbh:zy;
    ctx.fillStyle=tp>=0?'#c9a84c':'#8b3a2a';ctx.fillRect(x+bw+4,ty,bw,Math.max(2,tbh));
    ctx.fillStyle='#7a8a7a';ctx.font='10px sans-serif';ctx.fillText(d.month.slice(5),x+slotW/2-10,H-6);
  });
}'''

new_draw = '''function drawTimelineChart(id,events){
  const canvas=document.getElementById(id);if(!canvas)return;
  const W=canvas.offsetWidth||700,H=200;canvas.width=W;canvas.height=H;
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
  const pad={top:15,bottom:35,left:10,right:10};
  const toY=v=>pad.top+((mx-v)/range)*(H-pad.top-pad.bottom);
  const toX=i=>pad.left+(i/(pts.length-1||1))*(W-pad.left-pad.right);
  const zy=toY(0);

  // Nulllinie
  ctx.strokeStyle='#2a3a2a';ctx.lineWidth=1;ctx.setLineDash([4,4]);
  ctx.beginPath();ctx.moveTo(pad.left,zy);ctx.lineTo(W-pad.right,zy);ctx.stroke();
  ctx.setLineDash([]);

  function drawLine(key,color,width=2){
    ctx.beginPath();ctx.strokeStyle=color;ctx.lineWidth=width;
    pts.forEach((p,i)=>{
      i===0?ctx.moveTo(toX(i),toY(p[key])):ctx.lineTo(toX(i),toY(p[key]));
    });
    ctx.stroke();
    // Endpunkt
    const last=pts[pts.length-1];
    ctx.beginPath();ctx.arc(toX(pts.length-1),toY(last[key]),4,0,Math.PI*2);
    ctx.fillStyle=color;ctx.fill();
  }

  drawLine('cash','#2d8f4e');
  drawLine('tournament','#c9a84c');
  drawLine('total','#e8e8e4',2.5);

  // Event-Markierungen (Dreiecke oben auf X-Achse)
  pts.slice(1).forEach((p,i)=>{
    const x=toX(i+1);
    const color=p.type==='cash'?'#2d8f4e':'#c9a84c';
    ctx.beginPath();ctx.fillStyle=color;
    ctx.moveTo(x,H-pad.bottom+4);ctx.lineTo(x-4,H-pad.bottom+12);ctx.lineTo(x+4,H-pad.bottom+12);
    ctx.closePath();ctx.fill();
  });

  // Datum-Labels (nur erste und letzte)
  ctx.fillStyle='#7a8a7a';ctx.font='10px sans-serif';
  if(pts.length>1){
    const first=pts[1],last=pts[pts.length-1];
    ctx.fillText(first.date.slice(5),toX(1)-10,H-4);
    if(pts.length>2) ctx.fillText(last.date.slice(5),toX(pts.length-1)-10,H-4);
  }
}'''

c = c.replace(old_draw, new_draw, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')

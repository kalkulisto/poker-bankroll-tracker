path = 'J:/Meine Ablage/ClaudeProjekte/poker-tracker/frontend/index.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

old_fn = '''function drawTimelineChart(id,events){
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

new_fn = '''function drawTimelineChart(id,events){
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
}'''

if old_fn in c:
    c = c.replace(old_fn, new_fn, 1)
    print('patched')
else:
    print('NOT FOUND')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

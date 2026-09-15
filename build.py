#!/usr/bin/env python3
"""
GordoGains page generator.

    python3 build.py

Reads program.json, writes index.html. Deterministic: same input, same output.
Do NOT hand-edit index.html. It gets overwritten every build.
"""
import json, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "program.json")
STATS = os.path.join(HERE, "stats.json")
OUT  = os.path.join(HERE, "index.html")

SECRET_PAT = re.compile(r"(?:[A-Za-z0-9_\-]{8,}-[A-Za-z0-9_\-]{8,}-[A-Za-z0-9_\-]{8,})|(?:api[_-]?key['\"]?\s*[:=]\s*['\"][^'\"]{12,})", re.I)

CSS = """
:root{--bg:#0c0e14;--s1:#161922;--s2:#1e2230;--s3:#252a3a;--green:#4ade80;--green-d:#162a1e;
--blue:#60a5fa;--blue-d:#111d2e;--amber:#fbbf24;--amber-d:#251b08;--red:#f87171;--purple:#a78bfa;
--purple-d:#1e1535;--teal:#2dd4bf;--teal-d:#0d2521;--text:#e2e6f0;--muted:#64748b;--bd:#1e2535}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 'DM Sans',-apple-system,system-ui,sans-serif;
padding:0 0 60px;max-width:760px;margin:0 auto}
.mono{font-family:'DM Mono',ui-monospace,Menlo,monospace}
header{padding:18px 16px 12px;border-bottom:1px solid var(--bd);position:sticky;top:0;background:var(--bg);z-index:10}
h1{font-size:19px;margin:0;letter-spacing:-.01em}
h1 span{color:var(--muted);font-weight:400}
.built{font-size:11px;color:var(--muted);margin-top:3px}
.pills{display:flex;gap:6px;overflow-x:auto;padding:12px 16px;scrollbar-width:none}
.pills::-webkit-scrollbar{display:none}
.pill{flex:0 0 auto;min-width:46px;padding:8px 10px;border-radius:9px;border:1px solid var(--bd);
background:var(--s1);color:var(--muted);font-size:13px;cursor:pointer;text-align:center}
.pill.on{background:var(--purple-d);border-color:var(--purple);color:var(--purple);font-weight:600}
.pill.dl{border-color:var(--amber);color:var(--amber)}
.pill.dl.on{background:var(--amber-d)}
.days{display:flex;gap:5px;overflow-x:auto;padding:0 16px 12px;scrollbar-width:none}
.days::-webkit-scrollbar{display:none}
.day{flex:0 0 auto;padding:8px 13px;border-radius:9px;border:1px solid var(--bd);background:var(--s1);
color:var(--muted);font-size:13px;cursor:pointer}
.day.on{background:var(--s3);border-color:var(--blue);color:var(--blue);font-weight:600}
.day.today::after{content:"•";color:var(--green);margin-left:5px}
main{padding:0 16px}
.banner{background:var(--purple-d);border:1px solid var(--purple);border-radius:11px;padding:13px 15px;margin:4px 0 16px}
.banner.dl{background:var(--amber-d);border-color:var(--amber)}
.banner b{display:block;font-size:12px;letter-spacing:.09em;text-transform:uppercase;margin-bottom:5px;color:var(--purple)}
.banner.dl b{color:var(--amber)}
.banner p{margin:0;font-size:14px;color:var(--text);opacity:.93}
.sect{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:var(--muted);margin:22px 0 9px}
.card{background:var(--s1);border:1px solid var(--bd);border-radius:11px;padding:13px 15px;margin-bottom:9px}
.card.new{border-color:var(--red)}
.card h3{margin:0 0 7px;font-size:15px;font-weight:600;display:flex;justify-content:space-between;gap:10px;align-items:baseline}
.tag{font-size:10px;letter-spacing:.07em;text-transform:uppercase;padding:2px 7px;border-radius:5px;
background:var(--red);color:#2a1212;font-weight:700;flex:0 0 auto}
.tag.drop{background:var(--amber);color:#251b08}
.prescribe{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;margin-bottom:6px}
.prescribe div{color:var(--muted)}
.prescribe b{color:var(--teal);font-weight:600}
.note{font-size:13px;color:var(--muted);margin:0;line-height:1.5}
.big{font-size:30px;font-weight:700;letter-spacing:-.02em}
.big small{font-size:14px;font-weight:400;color:var(--muted);letter-spacing:0}
.rounds{display:flex;gap:7px;flex-wrap:wrap;margin:12px 0 4px}
.rnd{width:46px;height:46px;border-radius:10px;border:1px solid var(--blue);background:var(--blue-d);
color:var(--blue);font-size:15px;font-weight:600;cursor:pointer;display:flex;align-items:center;justify-content:center}
.rnd.on{background:var(--green);border-color:var(--green);color:#0c1a10}
.donebtn{width:100%;padding:13px;margin-top:11px;border-radius:10px;border:1px solid var(--blue);
background:var(--blue-d);color:var(--blue);font:600 15px 'DM Sans',sans-serif;cursor:pointer}
.donebtn.on{background:var(--green-d);border-color:var(--green);color:var(--green)}
.rest{background:var(--s1);border:1px dashed var(--bd);border-radius:11px;padding:26px 15px;text-align:center;color:var(--muted)}
table{width:100%;border-collapse:collapse;font-size:13.5px}
td{padding:6px 0;border-bottom:1px solid var(--bd);vertical-align:top}
td:last-child{text-align:right;color:var(--teal);white-space:nowrap;padding-left:12px}
tr:last-child td{border-bottom:none}
details{margin-top:9px}
summary{cursor:pointer;color:var(--muted);font-size:13px;padding:4px 0}
.zone{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--bd);font-size:13.5px}
.zone:last-child{border-bottom:none}
.zone b{color:var(--teal);font-weight:600}

/* progress tab */
.tabs{display:flex;gap:6px;padding:12px 16px 0}
.tab{flex:1;padding:9px;border-radius:9px;border:1px solid var(--bd);background:var(--s1);
color:var(--muted);font:600 14px 'DM Sans',sans-serif;cursor:pointer}
.tab.on{background:var(--s3);border-color:var(--teal);color:var(--teal)}
.tiles{display:grid;grid-template-columns:repeat(2,1fr);gap:9px;margin-bottom:6px}
.tile{background:var(--s1);border:1px solid var(--bd);border-radius:11px;padding:12px 14px}
.tile .lbl{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.tile .val{font-size:25px;font-weight:700;letter-spacing:-.02em;margin-top:3px}
.tile .sub{font-size:12px;color:var(--muted);margin-top:1px}
.chart{background:var(--s1);border:1px solid var(--bd);border-radius:11px;padding:13px 15px;margin-bottom:9px;position:relative}
.chart h3{margin:0 0 2px;font-size:15px;font-weight:600}
.chart .cap{font-size:12px;color:var(--muted);margin:0 0 10px}
.chart svg{display:block;width:100%;overflow:visible}
.empty{padding:22px 4px;text-align:center;color:var(--muted);font-size:13px}
.lgnd{display:flex;gap:13px;flex-wrap:wrap;font-size:12px;color:var(--muted);margin-top:9px}
.lgnd span{display:flex;align-items:center;gap:5px}
.sw{width:11px;height:11px;border-radius:3px;flex:0 0 auto}
.tip{position:absolute;pointer-events:none;background:var(--s3);border:1px solid var(--bd);
border-radius:7px;padding:6px 9px;font-size:12px;color:var(--text);white-space:nowrap;
opacity:0;transition:opacity .1s;z-index:5;box-shadow:0 4px 14px rgba(0,0,0,.5)}
.grid16{display:grid;grid-template-columns:22px repeat(16,1fr);gap:3px;font-size:9px}
.grid16 .hd{color:var(--muted);text-align:center;font-size:9px;line-height:14px}
.cell{aspect-ratio:1;border-radius:3px;background:var(--s2);border:1px solid var(--bd);cursor:default}
.cell.done{background:#0ca30c;border-color:#0ca30c}
.cell.miss{background:#d03b3b;border-color:#d03b3b}
.cell.fut{background:var(--s2);border-color:var(--bd);opacity:.45}
"""

JS = r"""
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const START=new Date(P.meta.start_date+'T00:00:00');
const DAYS=[['tue','Tue'],['wed','Wed'],['thu','Thu'],['fri','Fri'],['sat','Sat'],['sun','Sun'],['mon','Mon']];
const NW=P.meta.weeks;

function weekStart(w){const d=new Date(START);d.setDate(d.getDate()+(w-1)*7);return d}
function weekEnd(w){const d=weekStart(w);d.setDate(d.getDate()+6);return d}
function fmt(d){return d.toLocaleDateString('en-US',{month:'short',day:'numeric'})}
function curWeek(){const n=new Date();n.setHours(0,0,0,0);
  const w=Math.floor((n-START)/6048e5)+1;return Math.min(NW,Math.max(1,w))}
function curDay(){const k=['sun','mon','tue','wed','thu','fri','sat'][new Date().getDay()];return k}
function phaseOf(w){return P.phases.find(p=>p.weeks.includes(w))}
function isDeload(w){return phaseOf(w).name.toLowerCase().includes('deload')}
function setsFor(base,w,idx){const m=phaseOf(w).sets_mod;
  let s = m===-2?2 : m===-1?Math.max(2,base-1) : base;
  if(idx===0 && [5,6,10,11].includes(w)) s+=1;
  return s}
function dayDate(w,dk){const i=DAYS.findIndex(d=>d[0]===dk);const d=weekStart(w);d.setDate(d.getDate()+i);return d}

let W=curWeek(), D=curDay()==='mon'?'mon':curDay();
if(!DAYS.some(d=>d[0]===D)) D='tue';

function save(k,v){try{localStorage.setItem('gg_'+k,JSON.stringify(v))}catch(e){}}
function load(k,d){try{const v=localStorage.getItem('gg_'+k);return v?JSON.parse(v):d}catch(e){return d}}

function renderPills(){
  $('#pills').innerHTML=DAYS?Array.from({length:NW},(_,i)=>{const w=i+1;
    return `<button class="pill${w===W?' on':''}${isDeload(w)?' dl':''}" data-w="${w}">${w}</button>`}).join(''):'';
  $$('#pills .pill').forEach(b=>b.onclick=()=>{W=+b.dataset.w;render()});
  const on=$('#pills .pill.on'); if(on) on.scrollIntoView({inline:'center',block:'nearest'});
}
function renderDays(){
  const td=curDay(), tw=curWeek();
  $('#days').innerHTML=DAYS.map(([k,l])=>
    `<button class="day${k===D?' on':''}${(k===td&&W===tw)?' today':''}" data-d="${k}">${l}</button>`).join('');
  $$('#days .day').forEach(b=>b.onclick=()=>{D=b.dataset.d;render()});
}
function exCard(e,w,idx,total){
  const ph=phaseOf(w);
  const isNew = w>=8 && /^NEW/.test(e.note||'');
  const drop = [13,14].includes(w) && idx===total-2;
  return `<div class="card${isNew?' new':''}">
    <h3><span>${e.n}</span>${isNew?'<span class="tag">New</span>':''}${drop?'<span class="tag drop">Drop set</span>':''}</h3>
    <div class="prescribe">
      <div>Sets <b>${setsFor(e.s,w,idx)}</b></div>
      <div>Reps <b>${e.r}</b></div>
      <div>Load <b>${ph.sets_mod===-2?'60% of working':e.w}</b></div>
      <div>Rest <b>${e.rest}s</b></div>
    </div>
    <p class="note">${e.note||''}${drop?' <b style="color:var(--amber)">Last set: to failure, strip 30%, go again to failure.</b>':''}</p>
  </div>`;
}
function strengthDay(dk,w){
  const s=P.strength[dk], ph=phaseOf(w);
  const all = (w>=8 && s.p2!=='same') ? s.p2 : s.p1;
  const list = all.filter(e=>!(e.n.startsWith('Hip Thrust') && w<3));
  let h=`<div class="sect">${s.title} &middot; ${list.length} exercises</div>`;
  if(s.warmup) h+=`<div class="card"><h3>Warm-up</h3><p class="note">${s.warmup}</p></div>`;
  h+=list.map((e,i)=>exCard(e,w,i,list.length)).join('');
  return h;
}
function z2Day(w){
  const [mins,hr]=P.cardio.zone2[w];
  const k=`z2_${w}`, done=load(k,false);
  return `<div class="sect">Zone 2 Cardio</div>
  <div class="card"><div class="big">${mins}<small> min</small></div>
  <div class="prescribe" style="margin-top:8px"><div>Heart rate <b>${hr} bpm</b></div></div>
  <p class="note">Conversational the whole way. If you cannot talk, slow down. Peloton, or treadmill at 3.5-4 mph and 3-5% incline, or a rower. Pick what you will actually do.</p>
  <button class="donebtn${done?' on':''}" id="z2">${done?'Done':'Mark done'}</button></div>`;
}
function intDay(w){
  const [rounds,mins,hr,rest,note]=P.cardio.intervals[w];
  const k=`iv_${w}`, st=load(k,[]);
  const total=10+rounds*mins+(rounds-1)*rest+5;
  return `<div class="sect">VO2max Intervals &middot; about ${Math.round(total)} min</div>
  <div class="card"><div class="big">${rounds} &times; ${mins}<small> min</small></div>
  <div class="prescribe" style="margin-top:8px">
    <div>Target <b>${hr} bpm</b></div><div>Recovery <b>${rest} min</b></div></div>
  <p class="note">10 min easy warm-up. ${rounds} rounds of ${mins} min at ${hr} bpm, ${rest} min easy between. 5 min cooldown. Bike or rower, not running.</p>
  <p class="note" style="color:var(--amber);margin-top:8px">${note}</p>
  <div class="rounds">${Array.from({length:rounds},(_,i)=>
    `<button class="rnd${st.includes(i)?' on':''}" data-r="${i}">${i+1}</button>`).join('')}</div>
  <p class="note" style="font-size:12px">Tap a round as you finish it.</p></div>`;
}
function sunDay(w){
  const [lo,hi]=P.cardio.sunday[w];
  const k=`su_${w}`, done=load(k,false);
  return `<div class="sect">Easy Cardio &middot; optional</div>
  <div class="card"><div class="big">${lo}${hi!==lo?'-'+hi:''}<small> min</small></div>
  <div class="prescribe" style="margin-top:8px"><div>Heart rate <b>under ${P.hr.easy_max} bpm</b></div></div>
  <p class="note">Optional. This is the day you drop in a bad week and it costs you nothing. Outdoors if the weather allows. If you are pushing, you have missed the point.</p>
  <button class="donebtn${done?' on':''}" id="su">${done?'Done':'Mark done'}</button></div>`;
}
function refCard(){
  const n=P.nutrition;
  return `<div class="sect">Daily reference</div>
  <div class="card"><h3><span>Macros</span></h3><table>
    <tr><td>Calories</td><td>${n.calories}</td></tr>
    <tr><td>Protein</td><td>${n.protein_g} g</td></tr>
    <tr><td>Carbs</td><td>${n.carbs_g} g</td></tr>
    <tr><td>Fat</td><td>${n.fat_g} g</td></tr>
    <tr><td>Creatine</td><td>${n.creatine_g} g daily</td></tr></table>
    <details><summary>Protein anchors</summary><table>
    ${n.anchors.map(a=>`<tr><td><b>${a.when}</b><br><span class="note">${a.what}</span></td><td>${a.g} g</td></tr>`).join('')}
    </table></details></div>
  <div class="card"><h3><span>Heart rate zones</span></h3>
    <div class="zone"><span>Easy</span><b>under ${P.hr.easy_max}</b></div>
    <div class="zone"><span>Zone 2</span><b>${P.hr.z2[0]}-${P.hr.z2[1]}</b></div>
    <div class="zone"><span>VO2max</span><b>${P.hr.vo2[0]}-${P.hr.vo2[1]}</b></div>
    <div class="zone"><span>Max</span><b>${P.meta.athlete.hr_max}</b></div></div>`;
}
function renderPlan(){
  const ph=phaseOf(W);
  $('#hdr').innerHTML=`Week ${W} <span>of ${NW} &middot; ${ph.name}</span>`;
  $('#sub').textContent=`${fmt(weekStart(W))} to ${fmt(weekEnd(W))}`;
  renderPills(); renderDays();
  let h=`<div class="banner${isDeload(W)?' dl':''}"><b>${ph.name}</b><p>${ph.note}</p></div>`;
  if(D==='mon') h+=`<div class="rest"><div style="font-size:19px;margin-bottom:6px">Rest day</div>
    Full rest. Walk if you want, nothing structured.</div>`;
  else if(D==='wed') h+=z2Day(W);
  else if(D==='thu') h+=intDay(W);
  else if(D==='sun') h+=sunDay(W);
  else h+=strengthDay(D,W);
  h+=refCard();
  $('#main').innerHTML=h;
  const z=$('#z2'); if(z) z.onclick=()=>{const k=`z2_${W}`,v=!load(k,false);save(k,v);render()};
  const s=$('#su'); if(s) s.onclick=()=>{const k=`su_${W}`,v=!load(k,false);save(k,v);render()};
  $$('.rnd').forEach(b=>b.onclick=()=>{const k=`iv_${W}`;let st=load(k,[]);const r=+b.dataset.r;
    st=st.includes(r)?st.filter(x=>x!==r):[...st,r];save(k,st);render()});
}

/* ---------- progress tab ---------- */
const SERIES=['#3987e5','#d95926','#199e70','#c98500','#d55181'];
const INK='#898781', GRID='#2c2c2a';
let TAB='plan';

function elapsedWeeks(){return Math.min(NW,Math.max(1,curWeek()))}

function svgLine(pts,{w=340,h=110,fmt=v=>v,color='#3987e5',ylab=''}={}){
  if(pts.length===0) return '<div class="empty">No data yet.</div>';
  const pad={l:34,r:46,t:8,b:18};
  const xs=pts.map(p=>p.x), ys=pts.map(p=>p.y);
  let y0=Math.min(...ys), y1=Math.max(...ys);
  if(y0===y1){y0-=1;y1+=1}
  const padY=(y1-y0)*0.15; y0-=padY; y1+=padY;
  const x0=Math.min(...xs), x1=Math.max(...xs)===x0?x0+1:Math.max(...xs);
  const X=v=>pad.l+(v-x0)/(x1-x0)*(w-pad.l-pad.r);
  const Y=v=>pad.t+(1-(v-y0)/(y1-y0))*(h-pad.t-pad.b);
  const ticks=[y0+(y1-y0)*0.1, (y0+y1)/2, y1-(y1-y0)*0.1];
  let g=ticks.map(t=>`<line x1="${pad.l}" x2="${w-pad.r}" y1="${Y(t).toFixed(1)}" y2="${Y(t).toFixed(1)}" stroke="${GRID}" stroke-width="1"/>`+
    `<text x="${pad.l-6}" y="${(Y(t)+3.5).toFixed(1)}" fill="${INK}" font-size="9.5" text-anchor="end">${fmt(t)}</text>`).join('');
  const d=pts.map((p,i)=>(i?'L':'M')+X(p.x).toFixed(1)+' '+Y(p.y).toFixed(1)).join(' ');
  const marks=pts.map(p=>`<circle cx="${X(p.x).toFixed(1)}" cy="${Y(p.y).toFixed(1)}" r="4.5" fill="${color}" stroke="var(--s1)" stroke-width="2" data-t="Wk ${p.x} &middot; ${fmt(p.y)}${ylab}"/>`).join('');
  const last=pts[pts.length-1];
  return `<svg viewBox="0 0 ${w} ${h}" role="img">${g}
    <path d="${d}" fill="none" stroke="${color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    ${marks}
    <text x="${(X(last.x)+8).toFixed(1)}" y="${(Y(last.y)+3.5).toFixed(1)}" fill="${color}" font-size="11" font-weight="600">${fmt(last.y)}${ylab}</text>
  </svg>`;
}

function svgBars(vals,targets,{w=340,h=120}={}){
  const any=vals.some(v=>v>0);
  if(!any) return '<div class="empty">No cardio logged yet.</div>';
  const pad={l:30,r:8,t:8,b:16};
  const max=Math.max(...vals,...targets)*1.1;
  const n=vals.length, bw=(w-pad.l-pad.r)/n;
  const Y=v=>pad.t+(1-v/max)*(h-pad.t-pad.b);
  let out=`<line x1="${pad.l}" x2="${w-pad.r}" y1="${Y(0)}" y2="${Y(0)}" stroke="#383835" stroke-width="1"/>`;
  [max*0.5, max*0.92].forEach(t=>{out+=`<line x1="${pad.l}" x2="${w-pad.r}" y1="${Y(t).toFixed(1)}" y2="${Y(t).toFixed(1)}" stroke="${GRID}" stroke-width="1"/>
    <text x="${pad.l-5}" y="${(Y(t)+3.5).toFixed(1)}" fill="${INK}" font-size="9.5" text-anchor="end">${Math.round(t)}</text>`});
  vals.forEach((v,i)=>{
    const x=pad.l+i*bw+1, bwid=Math.max(3,bw-3);
    if(v>0) out+=`<rect x="${x.toFixed(1)}" y="${Y(v).toFixed(1)}" width="${bwid.toFixed(1)}" height="${(Y(0)-Y(v)).toFixed(1)}" rx="3" fill="${SERIES[0]}" data-t="Wk ${i+1} &middot; ${v} min (target ${targets[i]})"/>`;
    const ty=Y(targets[i]);
    out+=`<line x1="${x.toFixed(1)}" x2="${(x+bwid).toFixed(1)}" y1="${ty.toFixed(1)}" y2="${ty.toFixed(1)}" stroke="${INK}" stroke-width="1.5" stroke-dasharray="2 2"/>`;
  });
  return `<svg viewBox="0 0 ${w} ${h}" role="img">${out}</svg>`;
}

function strengthChart(strength){
  const names=Object.keys(strength).filter(n=>Object.keys(strength[n]).length>=2).slice(0,5);
  if(!names.length) return {html:'<div class="empty">Two weeks of logged lifting needed before progression shows.</div>',legend:''};
  const w=340,h=140,pad={l:34,r:40,t:8,b:18};
  // Index every lift to its own first logged week. Absolute loads differ by 5x
  // (leg press vs lateral raise), so a shared pound axis makes the light lifts
  // unreadable. Percent change puts them on one honest scale.
  const idx={};
  names.forEach(n=>{
    const e=Object.entries(strength[n]).map(([k,v])=>[+k,v]).sort((a,b)=>a[0]-b[0]);
    const b0=e[0][1];
    idx[n]=e.map(([k,v])=>({x:k,y:(v/b0-1)*100,raw:v}));
  });
  let y0=1e9,y1=-1e9,x1=1;
  names.forEach(n=>idx[n].forEach(p=>{y0=Math.min(y0,p.y);y1=Math.max(y1,p.y);x1=Math.max(x1,p.x)}));
  y0=Math.min(y0,0); y1=Math.max(y1,5);
  const padY=(y1-y0)*0.15||2; y0-=padY; y1+=padY;
  const X=v=>pad.l+(v-1)/Math.max(1,x1-1)*(w-pad.l-pad.r);
  const Y=v=>pad.t+(1-(v-y0)/(y1-y0))*(h-pad.t-pad.b);
  let out='';
  [y0+(y1-y0)*0.1,(y0+y1)/2,y1-(y1-y0)*0.1].forEach(t=>{
    out+=`<line x1="${pad.l}" x2="${w-pad.r}" y1="${Y(t).toFixed(1)}" y2="${Y(t).toFixed(1)}" stroke="${GRID}" stroke-width="1"/>
    <text x="${pad.l-6}" y="${(Y(t)+3.5).toFixed(1)}" fill="${INK}" font-size="9.5" text-anchor="end">${t>0?'+':''}${Math.round(t)}%</text>`});
  out+=`<line x1="${pad.l}" x2="${w-pad.r}" y1="${Y(0).toFixed(1)}" y2="${Y(0).toFixed(1)}" stroke="#383835" stroke-width="1"/>`;
  const labs=[];
  names.forEach((n,i)=>{
    const c=SERIES[i], pts=idx[n];
    out+=`<path d="${pts.map((p,j)=>(j?'L':'M')+X(p.x).toFixed(1)+' '+Y(p.y).toFixed(1)).join(' ')}" fill="none" stroke="${c}" stroke-width="2" stroke-linejoin="round"/>`;
    out+=pts.map(p=>`<circle cx="${X(p.x).toFixed(1)}" cy="${Y(p.y).toFixed(1)}" r="4" fill="${c}" stroke="var(--s1)" stroke-width="2" data-t="${n} &middot; Wk ${p.x} &middot; ${p.raw} lbs (${p.y>=0?'+':''}${p.y.toFixed(1)}%)"/>`).join('');
    const l=pts[pts.length-1];
    labs.push({y:Y(l.y),x:X(l.x),c,t:(l.y>=0?'+':'')+Math.round(l.y)+'%'});
  });
  labs.sort((a,b)=>a.y-b.y);
  for(let i=1;i<labs.length;i++) if(labs[i].y-labs[i-1].y<11) labs[i].y=labs[i-1].y+11;
  labs.forEach(l=>{out+=`<text x="${(l.x+7).toFixed(1)}" y="${(l.y+3.5).toFixed(1)}" fill="${l.c}" font-size="10" font-weight="600">${l.t}</text>`});
  const legend=`<div class="lgnd">${names.map((n,i)=>`<span><i class="sw" style="background:${SERIES[i]}"></i>${n.replace(/\s*\([^)]*\)/,'')}</span>`).join('')}</div>`;
  return {html:`<svg viewBox="0 0 ${w} ${h}" role="img">${out}</svg>`, legend};
}

function adherence(sessions,cardio){
  const done={};
  sessions.forEach(s=>{const d=new Date(s.date+'T00:00:00');done[`${s.week}_${['sun','mon','tue','wed','thu','fri','sat'][d.getDay()]}`]=1});
  cardio.forEach(c=>{const d=new Date(c.date+'T00:00:00');done[`${c.week}_${['sun','mon','tue','wed','thu','fri','sat'][d.getDay()]}`]=1});
  const today=new Date(); today.setHours(23,59,59,999);
  const rows=DAYS.filter(d=>d[0]!=='mon');
  let h='<div class="grid16"><div></div>';
  for(let w=1;w<=NW;w++) h+=`<div class="hd">${w%4===1||w===NW?w:''}</div>`;
  rows.forEach(([k,l])=>{
    h+=`<div class="hd" style="text-align:left">${l}</div>`;
    for(let w=1;w<=NW;w++){
      const fut=dayDate(w,k)>today, hit=done[`${w}_${k}`];
      const cls=hit?'done':(fut?'fut':'miss');
      h+=`<div class="cell ${cls}" data-t="Wk ${w} ${l} &middot; ${hit?'done':(fut?'upcoming':'not logged')}"></div>`;
    }
  });
  h+='</div><div class="lgnd"><span><i class="sw" style="background:#0ca30c"></i>Logged</span>'+
     '<span><i class="sw" style="background:#d03b3b"></i>Not logged</span>'+
     '<span><i class="sw" style="background:var(--s2);border:1px solid var(--bd)"></i>Upcoming</span></div>';
  return h;
}

function renderProgress(){
  const S=STATS, cw=elapsedWeeks(), wk=S.weekly||[], p=S.pulled||{};
  const last=wk.length?wk[wk.length-1]:null;
  const bw=S.baseline.weight_lbs, bwa=S.baseline.waist_in;
  const curW=last&&last.weight_lbs!=null?last.weight_lbs:bw;
  const curWa=last&&last.waist_in!=null?last.waist_in:bwa;
  const dW=(curW-bw), sessions=(p.sessions||[]).length;
  const totalSessions=cw*5;

  let h=`<div class="tiles">
    <div class="tile"><div class="lbl">Week</div><div class="val">${cw}<span style="font-size:14px;color:var(--muted)"> / ${NW}</span></div><div class="sub">${phaseOf(cw).name}</div></div>
    <div class="tile"><div class="lbl">Sessions</div><div class="val">${sessions}</div><div class="sub">of ~${totalSessions} scheduled</div></div>
    <div class="tile"><div class="lbl">Weight</div><div class="val">${curW??'--'}</div><div class="sub">${dW?(dW>0?'+':'')+dW.toFixed(1)+' lbs':'baseline'}</div></div>
    <div class="tile"><div class="lbl">Waist</div><div class="val">${curWa??'--'}</div><div class="sub">${curWa?'inches':'not measured yet'}</div></div>
  </div>`;

  const wPts=wk.filter(e=>e.weight_lbs!=null).map(e=>({x:e.week,y:e.weight_lbs}));
  const aPts=wk.filter(e=>e.waist_in!=null).map(e=>({x:e.week,y:e.waist_in}));
  const rPts=wk.filter(e=>e.resting_hr!=null).map(e=>({x:e.week,y:e.resting_hr}));

  h+=`<div class="chart"><h3>Bodyweight</h3><p class="cap">Target around ${S.targets.weight_lbs} lbs, but the waist decides</p>
    ${svgLine(wPts,{color:SERIES[0],fmt:v=>v.toFixed(1),ylab:' lbs'})}</div>`;
  h+=`<div class="chart"><h3>Waist</h3><p class="cap">Navel, morning, before food. Target ${S.targets.waist_change_in} inches over the block</p>
    ${svgLine(aPts,{color:SERIES[2],fmt:v=>v.toFixed(1),ylab:'"'})}</div>`;
  h+=`<div class="chart"><h3>Resting heart rate</h3><p class="cap">From ${S.baseline.resting_hr} at baseline. Target ${S.targets.resting_hr}</p>
    ${svgLine(rPts,{color:SERIES[4],fmt:v=>Math.round(v),ylab:' bpm'})}</div>`;

  const cardio=p.cardio||[];
  const mins=Array.from({length:NW},(_,i)=>cardio.filter(c=>c.week===i+1).reduce((a,c)=>a+c.min,0));
  const tgt=Array.from({length:NW},(_,i)=>S.targets.cardio_min_per_week[String(i+1)]||0);
  h+=`<div class="chart"><h3>Cardio minutes per week</h3><p class="cap">Dashes are the target. Climbing from about 90 to 180 is the point.</p>
    ${svgBars(mins,tgt)}</div>`;

  const st=strengthChart(p.strength||{});
  h+=`<div class="chart"><h3>Top set by lift</h3><p class="cap">Change from each lift's first logged week. Tap a point for the actual weight.</p>${st.html}${st.legend}</div>`;

  h+=`<div class="chart"><h3>Adherence</h3><p class="cap">Every training day of the block</p>${adherence(p.sessions||[],cardio)}</div>`;

  h+=`<div class="chart"><h3>Data sources</h3>
    <div class="zone"><span>Strength</span><b>Hevy</b></div>
    <div class="zone"><span>Cardio</span><b>Garmin to Strava</b></div>
    <div class="zone"><span>Recovery</span><b>Ultrahuman</b></div>
    <div class="zone"><span>Weight, waist, protein</span><b>entered weekly</b></div>
    <p class="note" style="margin-top:9px">Last pulled: ${p.fetched_at?p.fetched_at.replace('T',' '):'never'}</p></div>`;

  $('#main').innerHTML=h;
  attachTips();
}

function attachTips(){
  let tip=document.querySelector('.tip');
  if(!tip){tip=document.createElement('div');tip.className='tip';document.body.appendChild(tip)}
  $$('[data-t]').forEach(el=>{
    const show=e=>{tip.innerHTML=el.dataset.t;tip.style.opacity='1';
      const r=el.getBoundingClientRect();
      tip.style.left=Math.min(window.innerWidth-tip.offsetWidth-8,Math.max(8,r.left+r.width/2-tip.offsetWidth/2))+'px';
      tip.style.top=(r.top+window.scrollY-tip.offsetHeight-8)+'px'};
    el.addEventListener('mouseenter',show);
    el.addEventListener('touchstart',show,{passive:true});
    el.addEventListener('mouseleave',()=>tip.style.opacity='0');
  });
  document.addEventListener('scroll',()=>{tip.style.opacity='0'},{passive:true});
}

function render(){
  $('#pills').style.display = TAB==='plan'?'':'none';
  $('#days').style.display  = TAB==='plan'?'':'none';
  $$('.tab').forEach(b=>b.classList.toggle('on', b.dataset.tab===TAB));
  if(TAB==='plan') renderPlan(); else renderProgress();
}
$$('.tab').forEach(b=>b.onclick=()=>{TAB=b.dataset.tab;window.scrollTo(0,0);render()});
render();

"""

def build():
    with open(DATA) as f:
        program = json.load(f)
    with open(STATS) as f:
        stats = json.load(f)
    blob = json.dumps(program, separators=(",", ":"))
    sblob = json.dumps(stats, separators=(",", ":"))
    if SECRET_PAT.search(blob) or SECRET_PAT.search(sblob):
        raise SystemExit("ABORT: program.json contains something that looks like a credential. Nothing written.")
    built = datetime.date.today().isoformat()
    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="#0c0e14">
<title>GordoGains</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<header>
  <h1 id="hdr"></h1>
  <div class="built"><span id="sub"></span> &middot; built {built}</div>
</header>
<div class="tabs">
  <button class="tab on" data-tab="plan">Plan</button>
  <button class="tab" data-tab="progress">Progress</button>
</div>
<div class="pills" id="pills"></div>
<div class="days" id="days"></div>
<main id="main"></main>
<script>const P={blob};const STATS={sblob};</script>
<script>{JS}</script>
</body></html>"""
    if SECRET_PAT.search(html):
        raise SystemExit("ABORT: generated page contains something key-shaped. Nothing written.")
    with open(OUT, "w") as f:
        f.write(html)
    print(f"built index.html  ({len(html):,} bytes)  start {program['meta']['start_date']}  {program['meta']['weeks']} weeks")

if __name__ == "__main__":
    build()

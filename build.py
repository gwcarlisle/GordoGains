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
function render(){
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
render();
"""

def build():
    with open(DATA) as f:
        program = json.load(f)
    blob = json.dumps(program, separators=(",", ":"))
    if SECRET_PAT.search(blob):
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
<div class="pills" id="pills"></div>
<div class="days" id="days"></div>
<main id="main"></main>
<script>const P={blob};</script>
<script>{JS}</script>
</body></html>"""
    if SECRET_PAT.search(html):
        raise SystemExit("ABORT: generated page contains something key-shaped. Nothing written.")
    with open(OUT, "w") as f:
        f.write(html)
    print(f"built index.html  ({len(html):,} bytes)  start {program['meta']['start_date']}  {program['meta']['weeks']} weeks")

if __name__ == "__main__":
    build()

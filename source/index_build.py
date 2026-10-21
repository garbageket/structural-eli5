import json, sys
from lib_css import CSS
T = [
(1,'load-path','🏗️','Foundations of structural behaviour','How loads flow through a building','Slab to beam to column to footing, with tributary areas.'),
(2,'beam-bending','📏','Foundations of structural behaviour','Bending, shear and deflection in beams','Load a beam and read the shear and moment diagrams.'),
(3,'columns-buckling','🏛️','Foundations of structural behaviour','Columns and buckling','Push a column until it bows. Slenderness decides the failure.'),
(4,'stiffness','⚖️','Foundations of structural behaviour','Stiffness: the stiff member takes the load','Why a small size change moves most of the force.'),
(5,'materials','🧱','Foundations of structural behaviour','Concrete and steel as materials','Stress-strain curves, creep and shrinkage, IS 456 design values.'),
(6,'limit-state-design','🎯','RCC design','Limit state design','Factored combinations, which one governs, and why factors exist.'),
(7,'rc-beam','🔩','RCC design','How a reinforced concrete beam works','Neutral axis, steel strain and the brittle failure to avoid.'),
(8,'slabs','🔲','RCC design','Slabs: one-way, two-way, flat','Load sharing, thickness, and punching shear at a column.'),
(9,'shear-walls-cores','🧬','RCC design','Shear walls and cores in tall buildings','Core shape against sway, and coupled walls.'),
(10,'ductile-detailing','🪢','RCC design','Ductile detailing (IS 13920)','Hoop spacing, hysteresis loops and strong column, weak beam.'),
(11,'earthquake-loads','🌍','Loads','Earthquake loads','IS 1893 spectrum, zone, R factor and the base shear.'),
(12,'wind-loads','💨','Loads','Wind loads on tall buildings','Pressure with height, and across-wind vortex shedding.'),
(13,'dead-live-loads','📦','Loads','Dead, live and imposed loads','Build a floor, weigh it, and see live load reduction.'),
(14,'lateral-systems','🗼','Tall buildings','How a high-rise stands up','Frames, walls, cores, tubes, and the outrigger sweet spot.'),
(15,'drift-torsion-irregularity','🌀','Tall buildings','Drift, torsion and irregularities','Twist from offset mass, and the soft storey.'),
(16,'modal-analysis','🎼','Tall buildings','Modal analysis','Animated mode shapes, periods and mass participation.'),
(17,'p-delta','📐','Tall buildings','P-Delta effects','When weight makes the lean worse. The stability index.'),
(18,'transfer-structures','🔀','Tall buildings','Transfer structures and floating columns','Transfer beam sizing and the soft transfer floor.'),
(19,'soil-bearing-capacity','🌱','Geotechnical and foundations','Soil basics and bearing capacity','Three-phase soil and what the ground can carry.'),
(20,'retaining-walls','🧗','Geotechnical and foundations','Retaining walls and earth pressure','Active, passive, K values, water, and a wall design lab.'),
(21,'foundation-types','🦶','Geotechnical and foundations','Shallow versus deep foundations','Pick footings, raft or piles. Pressure bulb under a raft.'),
(22,'piles','📍','Geotechnical and foundations','Piles: how they carry load','Skin friction, tip bearing, groups and load tests.'),
(23,'basements-excavation','⛏️','Geotechnical and foundations','Basements, excavation, dewatering','Flotation check and the cone of depression.'),
(24,'etabs-modelling','🖥️','Analysis and checking','How ETABS models a building','Meshing, rigid diaphragms and modelling assumptions.'),
(25,'etabs-reviewer-red-flags','🚩','Analysis and checking','Reading an ETABS model like a reviewer','Five gauges, and a spot-the-red-flag quiz.'),
(26,'cracked-section-modifiers','🪨','Analysis and checking','Cracked section modifiers','Moment-curvature, effective stiffness and building-level effect.'),
(27,'value-engineering-framing','💡','Economy and practice','Value engineering in RCC framing','Floor systems by span and concrete grade stepping.'),
(28,'quantity-benchmarks','📊','Economy and practice','Quantity benchmarks for towers','Concrete and steel intensity against typical bands.'),
(29,'formwork-construction-sequence','🏗','Economy and practice','Formwork and construction sequence','Form pressure, tie loads and safe striking times.'),
(30,'durability','🛡️','Economy and practice','Durability: cover, exposure, corrosion','Exposure classes and chloride initiation time.'),
]
groups=[]
for t in T:
    if t[3] not in groups: groups.append(t[3])
cards=''
for n,slug,ic,g,title,blurb in T:
    cards+='<article class="card" data-g="%s" data-t="%s"><a class="cl" href="eli5-%02d-%s.html"><span class="ic" aria-hidden="true">%s</span><span class="no">%02d</span><h3>%s</h3><p>%s</p></a><label class="done"><input type="checkbox" data-n="%d"> Done</label></article>\n'%(g,(title+' '+blurb).lower().replace('"',''),n,slug,ic,n,title,blurb,n)
chips=''.join('<button type="button" data-g="%s" aria-pressed="false">%s</button>'%(g,g) for g in groups)
html='''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Structural engineering in pictures: 30 topics</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>%s
.cards{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));margin-top:1.5rem}
.card{border:1.5px solid var(--line);border-radius:14px;background:var(--bg);display:flex;flex-direction:column;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--ink)}
.card .cl{display:block;padding:1rem 1.1rem .4rem;text-decoration:none;color:inherit;position:relative;flex:1}
.card .ic{font-size:2.6rem;line-height:1;display:block}
.card .no{position:absolute;top:1rem;right:1.1rem;font-family:'Barlow Condensed',sans-serif;font-size:1.5rem;font-weight:700;color:var(--muted)}
.card h3{font-size:1.45rem;margin-top:.7rem}
.card p{font-size:.96rem;color:var(--muted);margin:.4rem 0 0}
.card .done{padding:.4rem 1.1rem .8rem;font-size:.9rem;color:var(--muted);display:flex;gap:.5rem;align-items:center;cursor:pointer}
.card .done input{accent-color:var(--ok);width:1.1rem;height:1.1rem}
.card.is-done{background:var(--panel)}
.card.is-done h3::after{content:" ✓";color:var(--ok)}
.tools{display:grid;gap:.9rem;margin-top:2rem}
.tools input[type=search]{font:inherit;padding:.65rem 1rem;border:1.5px solid var(--line);border-radius:999px;background:var(--bg);color:var(--ink);width:100%%;max-width:420px}
.gh{font-family:'Barlow Condensed',sans-serif;font-size:1.7rem;font-weight:700;margin:2.2rem 0 0}
.prog{font-weight:600;color:var(--muted)}
</style></head><body>
<main>
<div class="top"><span class="prog" id="prog"></span>
<div class="seg" role="group" aria-label="Colour theme"><button type="button" data-th="auto" aria-pressed="true">Auto</button><button type="button" data-th="light" aria-pressed="false">Light</button><button type="button" data-th="dark" aria-pressed="false">Dark</button></div></div>
<div class="kick">Explain like I know nothing</div>
<h1>Structural engineering in pictures</h1>
<p class="lede">Thirty topics, one page each. Big drawings, few words, sliders to play with, a short quiz at the end. Indian codes throughout. Works in light and dark mode.</p>
<div class="tools"><input type="search" id="q" placeholder="Search topics" aria-label="Search topics"><div class="chips" id="chips"><button type="button" data-g="" aria-pressed="true">All</button>%s</div></div>
<div id="list">%s</div>
</main>
<footer>Learning aids and quick sense-checks. Final design comes from the project design basis, the geotechnical report and the governing codes.</footer>
<script>
const root=document.documentElement;
function setTheme(t){if(t==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',t);document.querySelectorAll('.seg button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.th===t?'true':'false'));try{localStorage.setItem('es-theme',t)}catch(e){}}
let th='auto';try{th=localStorage.getItem('es-theme')||localStorage.getItem('rw-theme')||'auto'}catch(e){}
setTheme(th);document.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.th)));
let done={};try{done=JSON.parse(localStorage.getItem('es-done')||'{}')}catch(e){}
const cards=[...document.querySelectorAll('.card')];let g='';
function render(){const q=document.getElementById('q').value.trim().toLowerCase();let shown=0,dn=0;const list=document.getElementById('list');
 list.querySelectorAll('.gh,.cards').forEach(e=>e.remove());
 const groups=[...new Set(cards.map(c=>c.dataset.g))];
 groups.forEach(gr=>{const cs=cards.filter(c=>c.dataset.g===gr&&(!g||c.dataset.g===g)&&(!q||c.dataset.t.indexOf(q)>=0));if(!cs.length)return;
  const h=document.createElement('h2');h.className='gh';h.textContent=gr;list.appendChild(h);const w=document.createElement('div');w.className='cards';cs.forEach(c=>{w.appendChild(c);shown++});list.appendChild(w)});
 cards.forEach(c=>{const n=c.querySelector('input').dataset.n;const on=!!done[n];c.classList.toggle('is-done',on);c.querySelector('input').checked=on;if(on)dn++});
 document.getElementById('prog').textContent=dn+' of '+cards.length+' done'}
cards.forEach(c=>c.querySelector('input').addEventListener('change',e=>{const n=e.target.dataset.n;if(e.target.checked)done[n]=1;else delete done[n];try{localStorage.setItem('es-done',JSON.stringify(done))}catch(x){}render()}));
document.getElementById('q').addEventListener('input',render);
document.querySelectorAll('#chips button').forEach(b=>b.addEventListener('click',()=>{g=b.dataset.g;document.querySelectorAll('#chips button').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));render()}));
render();
</script></body></html>'''%(CSS,chips,cards)
open(sys.argv[1]+'/eli5-index.html','w').write(html)
print('index ok',len(T))

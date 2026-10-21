JS = r"""
const NS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id);
const rad=d=>d*Math.PI/180, deg=r=>r*180/Math.PI;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const STY={stroke:1,'stroke-width':1,'stroke-dasharray':1,fill:1,'fill-opacity':1};
function S(tag,a,p){const e=document.createElementNS(NS,tag);let st=a&&a.style?a.style+';':'';for(const k in a){if(k==='style')continue;if(STY[k])st+=k+':'+a[k]+';';else e.setAttribute(k,a[k])}if(st)e.setAttribute('style',st);if(p)p.appendChild(e);return e}
function T(p,x,y,txt,a){const e=S('text',Object.assign({x:x,y:y,'font-size':22},a||{}),p);e.textContent=txt;return e}
function clear(e){while(e.firstChild)e.removeChild(e.firstChild)}
function pts(a){return a.map(q=>q[0].toFixed(1)+','+q[1].toFixed(1)).join(' ')}
function poly(p,a,at){return S('polygon',Object.assign({points:pts(a)},at||{}),p)}
function pline(p,a,cls,at){return S('polyline',Object.assign({points:pts(a),class:cls||'s-ink'},at||{}),p)}
function line(p,x1,y1,x2,y2,cls,at){return S('line',Object.assign({x1:x1,y1:y1,x2:x2,y2:y2,class:cls||'s-ink'},at||{}),p)}
function rect(p,x,y,w,h,cls,at){return S('rect',Object.assign({x:x,y:y,width:Math.max(0,w),height:Math.max(0,h),class:cls},at||{}),p)}
function circ(p,cx,cy,r,cls,at){return S('circle',Object.assign({cx:cx,cy:cy,r:r,class:cls},at||{}),p)}
function path(p,d,cls,at){return S('path',Object.assign({d:d,class:cls||'s-ink'},at||{}),p)}
function arrow(p,x1,y1,x2,y2,cls,m,at){return S('line',Object.assign({x1:x1,y1:y1,x2:x2,y2:y2,class:cls||'s-push','marker-end':'url(#'+(m||'ah')+')'},at||{}),p)}
function dimH(p,x1,x2,y,label,o){o=o||{};line(p,x1,y,x2,y,'s-ink');line(p,x1,y-7,x1,y+7,'s-ink');line(p,x2,y-7,x2,y+7,'s-ink');if(label)T(p,(x1+x2)/2,y+(o.dy===undefined?-10:o.dy),label,{'text-anchor':'middle','font-size':o.fs||21})}
function dimV(p,x,y1,y2,label,o){o=o||{};line(p,x,y1,x,y2,'s-ink');line(p,x-7,y1,x+7,y1,'s-ink');line(p,x-7,y2,x+7,y2,'s-ink');if(label)T(p,x+(o.dx===undefined?-10:o.dx),(y1+y2)/2+7,label,{'text-anchor':o.anchor||'end','font-size':o.fs||21})}
function pin(p,x,y,s){s=s||16;poly(p,[[x,y],[x-s,y+s*1.4],[x+s,y+s*1.4]],{class:'f-slab',stroke:'var(--ink)','stroke-width':2});line(p,x-s*1.4,y+s*1.4,x+s*1.4,y+s*1.4,'s-ink')}
function roller(p,x,y,s){s=s||16;poly(p,[[x,y],[x-s,y+s*1.2],[x+s,y+s*1.2]],{class:'f-slab',stroke:'var(--ink)','stroke-width':2});circ(p,x-s*.5,y+s*1.2+5,5,'f-slab',{stroke:'var(--ink)'});circ(p,x+s*.5,y+s*1.2+5,5,'f-slab',{stroke:'var(--ink)'});line(p,x-s*1.4,y+s*1.2+10,x+s*1.4,y+s*1.2+10,'s-ink')}
function fixedWall(p,x,y1,y2,side){const w=16;rect(p,side<0?x-w:x,y1,w,y2-y1,'f-conc');}
function fixedBase(p,x1,x2,y){rect(p,x1,y,x2-x1,14,'f-conc')}
const nice=x=>{const e=Math.pow(10,Math.floor(Math.log10(x))),f=x/e;return (f<1.5?1:f<3?2:f<7?5:10)*e};
function ticks(a,b,n){const st=nice((b-a)/n),r=[];for(let v=Math.ceil(a/st-1e-9)*st;v<=b+1e-9;v+=st)r.push(+v.toFixed(10));return r}
const fmtT=v=>Math.abs(v)>=10000?(v/1000)+'k':(+v.toFixed(3))+'';
function plot(g,o){const x=o.x===undefined?72:o.x,y=o.y===undefined?24:o.y,w=o.w||530,h=o.h||300;
  const X=v=>x+(v-o.x0)/(o.x1-o.x0)*w,Y=v=>y+h-(v-o.y0)/(o.y1-o.y0)*h;
  const xs=Array.isArray(o.xt)?o.xt:ticks(o.x0,o.x1,o.xt||5),ys=Array.isArray(o.yt)?o.yt:ticks(o.y0,o.y1,o.yt||5);
  xs.forEach(v=>{line(g,X(v),y,X(v),y+h,'s-grid');T(g,X(v),y+h+24,fmtT(v),{'font-size':18,'text-anchor':'middle'})});
  ys.forEach(v=>{line(g,x,Y(v),x+w,Y(v),'s-grid');T(g,x-8,Y(v)+6,fmtT(v),{'font-size':18,'text-anchor':'end'})});
  line(g,x,y+h,x+w,y+h,'s-ink');line(g,x,y,x,y+h,'s-ink');
  if(o.xl)T(g,x+w,y+h+50,o.xl,{'font-size':19,'text-anchor':'end'});
  if(o.yl)T(g,x,y-8,o.yl,{'font-size':19});
  return {X:X,Y:Y,x:x,y:y,w:w,h:h,o:o}}
function curve(g,P,fn,a,b,cls,n,at){n=n||120;const q=[];for(let i=0;i<=n;i++){const v=a+(b-a)*i/n;let yv=fn(v);if(!isFinite(yv))continue;{const lo=Math.min(P.o.y0,P.o.y1),hi=Math.max(P.o.y0,P.o.y1),pd=(hi-lo)*.05;yv=clamp(yv,lo-pd,hi+pd)};q.push([P.X(v),P.Y(yv)])}return pline(g,q,cls||'s-push',at)}
let _id=0;
function slider(host,o){const id='sl'+(++_id);let w=host.querySelector(':scope > .sls');if(!w){w=document.createElement('div');w.className='sls';host.appendChild(w)}
  const d=document.createElement('div');d.className='sl';
  d.innerHTML='<div class="slh"><label for="'+id+'">'+o.label+'</label><output for="'+id+'"></output></div><input type="range" id="'+id+'" min="'+o.min+'" max="'+o.max+'" step="'+o.step+'" value="'+o.value+'">';
  w.appendChild(d);const i=d.querySelector('input'),out=d.querySelector('output');
  const u=()=>{out.innerHTML=o.fmt?o.fmt(+i.value):i.value};
  i.addEventListener('input',()=>{u();if(o.on)o.on(+i.value)});u();
  i.v=()=>+i.value;i.set=v=>{i.value=v;i.dispatchEvent(new Event('input'))};return i}
function chips(host,items,on,init,label){const w=document.createElement('div');if(label){const l=document.createElement('div');l.className='cl';l.innerHTML=label;w.appendChild(l)}
  const c=document.createElement('div');c.className='chips';w.appendChild(c);host.appendChild(w);let cur=init===undefined?items[0][1]:init;
  const bs=items.map(it=>{const b=document.createElement('button');b.type='button';b.innerHTML=it[0];b.onclick=()=>set(it[1],true);c.appendChild(b);return [b,it[1]]});
  function set(v,f){cur=v;bs.forEach(x=>x[0].setAttribute('aria-pressed',x[1]===v?'true':'false'));if(f&&on)on(v)}
  set(cur,false);return {get:()=>cur,set:v=>set(v,true)}}
function checkbox(host,label,on,init){const l=document.createElement('label');l.className='chk';l.innerHTML='<input type="checkbox"> '+label;const i=l.querySelector('input');i.checked=!!init;i.addEventListener('change',()=>{if(on)on(i.checked)});host.appendChild(l);i.v=()=>i.checked;return i}
function button(host,label,on,solid){const b=document.createElement('button');b.type='button';b.className='btn'+(solid?' solid':'');b.innerHTML=label;b.onclick=on;host.appendChild(b);return b}
function tiles(host,arr){host.innerHTML='<div class="metrics">'+arr.map(t=>'<div class="m '+(t.c||'')+'"><div class="lbl">'+t.l+'</div><div class="val">'+t.v+(t.u?'<small>'+t.u+'</small>':'')+'</div>'+(t.st?'<div class="st">'+t.st+'</div>':'')+(t.s?'<div class="sb">'+t.s+'</div>':'')+'</div>').join('')+'</div>'}
function bars(host,rows){host.innerHTML='<div class="bars">'+rows.map(r=>'<div class="bar '+(r.c||'')+(r.on?' on':'')+'"><span>'+r.l+'</span><i><b style="width:'+clamp(r.v/(r.max||1)*100,1.5,100).toFixed(1)+'%"></b></i><span>'+(r.t===undefined?Math.round(r.v):r.t)+'</span></div>').join('')+'</div>'}
function Lab(host,o){o=o||{};const d=document.createElement('div');d.className='lab';
  d.innerHTML='<figure><svg viewBox="0 0 '+(o.w||640)+' '+(o.h||440)+'" role="img" aria-label="'+(o.label||'Interactive diagram')+'"></svg>'+(o.note?'<p class="note">'+o.note+'</p>':'')+'</figure><div class="ctl"><div class="cin"></div><div class="out"></div></div>';
  host.appendChild(d);const ctl=d.querySelector('.cin');return {svg:d.querySelector('svg'),sl:ctl,out:d.querySelector('.out'),el:d}}
function animate(from,to,ms,fn,done){if(reduce){fn(to);if(done)done();return}const t0=performance.now();function st(t){const k=Math.min(1,(t-t0)/ms),e=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;fn(from+(to-from)*e);if(k<1)requestAnimationFrame(st);else if(done)done()}requestAnimationFrame(st)}
function loop(el,fn){let vis=true,t0=performance.now(),on=true;if('IntersectionObserver' in window){new IntersectionObserver(es=>{vis=es[0].isIntersecting;if(vis&&on)requestAnimationFrame(f)}).observe(el)}
  function f(t){if(!on||!vis)return;fn((t-t0)/1000);requestAnimationFrame(f)}
  if(reduce)fn(0.4);else requestAnimationFrame(f);return {stop:()=>{on=false}}}
function quiz(host,items){const w=document.createElement('div');const score=document.createElement('p');score.className='score';let sc=0,dn=0;
  items.forEach(it=>{const q=document.createElement('div');q.className='q';q.innerHTML='<h3>'+it.q+'</h3><div class="opts"></div><p class="why" hidden></p>';const ob=q.querySelector('.opts'),why=q.querySelector('.why');
    it.o.forEach((t,j)=>{const b=document.createElement('button');b.type='button';b.className='btn';b.innerHTML=t;b.onclick=()=>{if(q.dataset.d)return;q.dataset.d=1;dn++;const ok=j===it.a;if(ok)sc++;b.classList.add(ok?'right':'wrong');if(!ok)ob.children[it.a].classList.add('right');why.hidden=false;why.innerHTML=(ok?'Right. ':'Not quite. ')+it.w;score.textContent=sc+' of '+items.length+' right'+(dn<items.length?' so far':'')};ob.appendChild(b)});
    w.appendChild(q)});w.appendChild(score);host.appendChild(w)}
const f0=v=>Math.round(v).toLocaleString('en-IN');
const f1=v=>(Math.round(v*10)/10).toFixed(1);
const f2=v=>(Math.round(v*100)/100).toFixed(2);
const f3=v=>(Math.round(v*1000)/1000).toFixed(3);
const ok=(c,a,b,x)=>c?a:(x||b);
/* theme */
const root=document.documentElement;
function setTheme(t){if(t==='auto')root.removeAttribute('data-theme');else root.setAttribute('data-theme',t);document.querySelectorAll('.seg button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.th===t?'true':'false'));try{localStorage.setItem('es-theme',t)}catch(e){}}
let _th='auto';try{_th=localStorage.getItem('es-theme')||(localStorage.getItem('rw-theme')||'auto')}catch(e){}
setTheme(_th);document.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.th)));
"""

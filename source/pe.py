PAGES = []

# ---------------------------------------------------------------- 13
PAGES.append(dict(n=13, slug='dead-live-loads', group='Loads',
 title='Dead, live and imposed loads',
 lede='Before any analysis, you have to know what the floor weighs and what people will put on it. Most design errors start with a wrong number here.',
 sections=[
 dict(h='Build a floor, weigh it', p='Add the layers. The dead load is what the floor itself weighs. The live load comes from the use. Slide and see what dominates.', js=r"""
const L=Lab(H,{h:440,label:'Floor layers and a stacked load bar',note:'Unit weights from IS 875 (Part 1): RCC 25, cement mortar 20.4, flooring 22 kN/m³ (typical). Imposed loads from IS 875 (Part 2) Table 1, typical values: check the table for your use.'});
const st=slider(L.sl,{label:'Slab thickness',min:125,max:300,step:5,value:175,fmt:v=>v+' mm',on:d});
const ss=slider(L.sl,{label:'Cement screed',min:0,max:100,step:5,value:40,fmt:v=>v+' mm',on:d});
const sf=slider(L.sl,{label:'Floor tile / stone',min:0,max:40,step:5,value:20,fmt:v=>v+' mm',on:d});
const sp=slider(L.sl,{label:'Partition allowance',min:0,max:2,step:.25,value:1,fmt:v=>f2(v)+' kN/m²',on:d});
const oc=chips(L.sl,[['Home 2.0',2],['Balcony / stairs 3.0',3],['Office 2.5',2.5],['Shops 4.0',4],['Assembly 5.0',5],['Plant 7.5',7.5]],d,2,'Use');
function vals(){const a=25*st.v()/1000,b=20.4*ss.v()/1000,c=22*sf.v()/1000,e=.5,p=sp.v(),ll=oc.get();return {a:a,b:b,c:c,e:e,p:p,ll:ll,dl:a+b+c+e+p}}
function d(){const v=vals(),g=L.svg;clear(g);
 const x0=40,y0=70,sc=.55;
 const lay=[['Floor tile',22*0+sf.v(),'f-warn'],['Screed',ss.v(),'f-sand'],['RCC slab',st.v(),'f-conc']];
 let y=y0;lay.forEach(l=>{if(l[1]>0){rect(g,x0,y,220,Math.max(4,l[1]*sc),l[2]);T(g,x0+230,y+Math.max(4,l[1]*sc)/2+7,l[0]+' '+l[1]+' mm',{'font-size':19});y+=Math.max(4,l[1]*sc)}});
 rect(g,x0,y,220,10,'f-ink',{opacity:.6});T(g,x0+230,y+9,'ceiling and services',{'font-size':19});
 arrow(g,x0+110,y0-56,x0+110,y0-6,'s-push','ah',{'stroke-width':4});T(g,x0+130,y0-24,'live load '+f1(v.ll)+' kN/m²',{'font-size':20,'font-weight':600});
 const bx=450,bot=400,scl=300/Math.max(v.dl+v.ll,8),parts=[['Slab',v.a,'f-conc'],['Screed + tile',v.b+v.c,'f-sand'],['Services',v.e,'f-ink'],['Partitions',v.p,'f-warn'],['Live',v.ll,'f-push']];
 let yy=bot;parts.forEach(p=>{const h=p[1]*scl;if(h>0.5){rect(g,bx,yy-h,110,h,p[2],{opacity:p[0]==='Services'?.6:1});if(h>16)T(g,bx+118,yy-h/2+7,p[0]+' '+f1(p[1]),{'font-size':19});yy-=h}});
 T(g,bx+55,bot+30,'kN/m²',{'text-anchor':'middle','font-size':19});
 tiles(L.out,[{l:'Dead load',v:f1(v.dl),u:'kN/m²'},{l:'Live load',v:f1(v.ll),u:'kN/m²'},{l:'Service total',v:f1(v.dl+v.ll),u:'kN/m²'},{l:'Factored 1.5 (DL+LL)',v:f1(1.5*(v.dl+v.ll)),u:'kN/m²'},{l:'Live ÷ dead',v:f2(v.ll/v.dl),c:v.ll/v.dl>1?'warn':'ok',st:v.ll/v.dl>1?'live governs':'dead governs'}])}
d();
// reduction
const L2=Lab(H,{h:420,label:'Live load reduction on a column down a tower',note:'IS 875 (Part 2) cl 3.2: the live load on a column or foundation may be cut when many floors are carried: 0, 10, 20, 30, 40% for 1–5 floors, 40% up to 10 floors, 50% beyond.'});
const sn=slider(L2.sl,{label:'Floors carried by the column',min:1,max:60,step:1,value:20,fmt:v=>v+' floors',on:d2});
const sa=slider(L2.sl,{label:'Floor area per column',min:20,max:80,step:2,value:50,fmt:v=>v+' m²',on:d2});
function red(n){return n<=1?0:n===2?10:n===3?20:n===4?30:n<=10?40:50}
function d2(){const g=L2.svg,n=sn.v(),A=sa.v(),v=vals(),r=red(n),full=n*A*v.ll,cut=full*(1-r/100);clear(g);
 const W=420,x0=70,bh=34;
 T(g,x0,70,'Live load without reduction',{'font-size':21});rect(g,x0,84,W,bh,'f-water');T(g,x0+W+8,84+bh*.72,f0(full)+' kN',{'font-size':20});
 T(g,x0,170,'With IS 875 reduction ('+r+'%)',{'font-size':21});rect(g,x0,184,W*(1-r/100),bh,'f-ok');rect(g,x0+W*(1-r/100),184,W*r/100,bh,'f-none',{stroke:'var(--muted)','stroke-dasharray':'6 4'});T(g,x0+W*(1-r/100)+W*r/200,184+bh*.72,r?'saved':'',{'font-size':19,'text-anchor':'middle'});
 T(g,x0+W+8,184+bh*.72,f0(cut)+' kN',{'font-size':20});
 const dl=n*A*v.dl;T(g,x0,280,'Dead load on the same column',{'font-size':21});rect(g,x0,294,Math.min(W*2,W*dl/Math.max(full,dl)),bh,'f-conc');T(g,x0+Math.min(W*2,W*dl/Math.max(full,dl))+8,294+bh*.72,f0(dl)+' kN',{'font-size':20});
 tiles(L2.out,[{l:'Reduction',v:r,u:'%'},{l:'Live load saved',v:f0(full-cut),u:'kN'},{l:'Live ÷ total',v:Math.round(cut/(cut+dl)*100),u:'%',s:'after reduction'}])}
[st,ss,sf,sp].forEach(e=>e.addEventListener('input',d2));d2();
""")],
 quiz=[dict(q='A 150 mm RCC slab weighs about…', o=['1.5 kN/m²','3.75 kN/m²','7.5 kN/m²'], a=1, w='25 kN/m³ × 0.15 m = 3.75 kN/m². A good number to carry in your head.'),
  dict(q='Why is live load reduced for columns in tall buildings?', o=['It is lighter in tall buildings','All floors are very unlikely to be fully loaded at once','Columns are stronger'], a=1, w='The chance of every floor carrying full live load together is tiny. IS 875 (Part 2) allows up to 50% reduction.'),
  dict(q='A brick partition wall is 3 m high, 115 mm thick, 6 m long. Roughly its weight is…', o=['5 kN','20 kN','60 kN'], a=1, w='19 kN/m³ × 0.115 × 3 × 6 ≈ 39 kN plus plaster ≈ 45 kN. Small but real, and it needs a beam or slab strip under it.')],
 rules=['Dead load: weigh every layer. Finishes, screed and partitions can add 2–3 kN/m².','Take partition walls as real loads, not “allowances”, when they are heavy or fixed.','Live load reduction applies to columns and foundations, not to slabs and beams.','Add the seismic share of live load to the weight for earthquake (25% below 3 kN/m², 50% above).'],
 codes=['IS 875 (Part 1):1987 dead loads','IS 875 (Part 2):1987 imposed loads','IS 875 (Part 5):1987 combinations','IS 1893 Table 10 (seismic weight)']))

# ---------------------------------------------------------------- 14
PAGES.append(dict(n=14, slug='lateral-systems', group='Tall buildings',
 title='How a high-rise stands up: lateral systems',
 lede='A tower is a cantilever fixed in the ground. The system you pick decides how it leans, and how tall it can get before the cost explodes.',
 sections=[
 dict(h='Five ways to resist the wind', p='Pick a system. Each bends differently: frames lean like a rack, walls like a diving board. Slide the height to see if the system is in its comfort zone.', js=r"""
const L=Lab(H,{h:480,label:'Deflected shapes and economical height ranges of lateral systems',note:'Shapes under uniform lateral load, normalised. Height ranges are rough textbook values of storeys where each system is usually economical. They shift with loads and seismic zone.'});
const sy=chips(L.sl,[['Frame',0],['Shear wall',1],['Wall + frame',2],['Core + outrigger',3],['Tube',4]],d,2,'System');
const sn=slider(L.sl,{label:'Number of storeys',min:5,max:110,step:1,value:45,fmt:v=>v+' storeys',on:d});
const R=[[5,25],[10,35],[15,50],[40,100],[40,100]],NM=['Rigid frame','Shear wall','Wall + frame (dual)','Core + outrigger','Framed tube'];
const TX=['Beams and columns bend. Leans like a rack: most drift low down. Good to about 25 floors.','Cantilever bending. Stiff but heavy. Works till about 35 floors, then walls get too thick.','Wall controls the bottom, frame the top. They hold each other. Good to about 50 floors.','Outriggers tie the core to far columns. They cut sway and the base moment a lot.','Closely spaced perimeter columns act as a hollow tube. Stiff against wind and torsion.'];
function sh(t,z){const b=(6-4*z+z*z)*z*z/3,s=2*z-z*z;return t===0?s:t===1?b:t===2?.45*b+.55*s:t===3?.5*b:.3*b+.1*s}
function d(){const g=L.svg,t=sy.get(),n=sn.v();clear(g);
 const bx=130,by=400,ht=320;rect(g,bx-50,by,100,12,'f-conc');
 const pts0=[],pts1=[];for(let i=0;i<=40;i++){const z=i/40;pts0.push([bx,by-z*ht]);pts1.push([bx+sh(t,z)*70,by-z*ht])}
 pline(g,pts0,'s-muted');pline(g,pts1,'s-thick',{'stroke-width':16,stroke:'var(--conc2)'});pline(g,pts1,'s-push',{'stroke-width':3});
 T(g,bx,by+40,NM[t],{'text-anchor':'middle','font-size':22,'font-weight':600});
 // range chart
 const rx=300,rw=300,max=120;T(g,rx,50,'economical storeys',{'font-size':20,'font-weight':600});
 NM.forEach((nm,i)=>{const y=72+i*58;T(g,rx,y,nm,{'font-size':18});rect(g,rx,y+8,rw,16,'f-slab');rect(g,rx+R[i][0]/max*rw,y+8,(R[i][1]-R[i][0])/max*rw,16,i===t?'f-push':'f-water');
  if(i===t){}});
 const mx=rx+Math.min(n,max)/max*rw;line(g,mx,58,mx,350,'s-ink',{'stroke-width':3});T(g,mx,372,n+' storeys',{'text-anchor':'middle','font-size':20,'font-weight':600});
 const inR=n>=R[t][0]&&n<=R[t][1],over=n>R[t][1];
 tiles(L.out,[{l:'Fit for height',v:inR?'In range':over?'Too tall':'Overkill',c:inR?'ok':over?'bad':'warn',st:inR?'Comfortable':over?'Cost climbs fast, consider outriggers or a tube':'A simpler system would do'},{l:'Typical range',v:R[t][0]+'–'+R[t][1],u:'storeys'}]);
 L.out.insertAdjacentHTML('beforeend','<p>'+TX[t]+'</p>')}
d();
"""),
 dict(h='Outriggers: tie the core to the edge', p='An outrigger pulls the far columns into the work. Move it up or down the building and change how stiff it is. There is a best floor.', js=r"""
const L=Lab(H,{h:460,label:'Core with one outrigger: sway with and without',note:'Cantilever core under uniform load, one outrigger. Compatibility: core rotation at the outrigger level equals outrigger rotation. Normalised so the core alone has top drift = 1/8. r = outrigger rotational stiffness × H / EI.'});
const sa=slider(L.sl,{label:'Outrigger level, share of height',min:.1,max:.95,step:.01,value:.55,fmt:v=>Math.round(v*100)+'% of H',on:d});
const sr=slider(L.sl,{label:'Outrigger stiffness r',min:.5,max:40,step:.5,value:8,fmt:v=>f1(v),on:d});
function calc(a,r){const th=(1-Math.pow(1-a,3))/6,Mo=th/(a+1/r),dl=.125-Mo*a*(1-a/2);return {Mo:Mo,dl:dl,dred:(.125-dl)/.125,mred:Mo/.5}}
function d(){const g=L.svg,a=sa.v(),r=sr.v(),c=calc(a,r);clear(g);
 const bx=160,by=410,ht=330,sc=150/.125;rect(g,bx-50,by,100,12,'f-conc');
 const d0=z=>(6-4*z+z*z)*z*z/24,d1=z=>d0(z)-c.Mo*(z<=a?z*z/2:a*z-a*a/2);
 const p0=[],p1=[];for(let i=0;i<=50;i++){const z=i/50;p0.push([bx+d0(z)*sc,by-z*ht]);p1.push([bx+d1(z)*sc,by-z*ht])}
 pline(g,[[bx,by],[bx,by-ht]],'s-muted');pline(g,p0,'s-muted',{'stroke-width':3});
 pline(g,p1,'s-thick',{'stroke-width':12,stroke:'var(--conc2)'});pline(g,p1,'s-push',{'stroke-width':3});
 const ya=by-a*ht,xa=bx+d1(a)*sc;line(g,xa-90,ya,xa+90,ya,'s-ink',{'stroke-width':6});line(g,xa-90,ya,xa-90,ya+44,'s-ink',{'stroke-width':6});line(g,xa+90,ya,xa+90,ya+44,'s-ink',{'stroke-width':6});
 T(g,xa+100,ya-8,'outrigger',{'font-size':20,'font-weight':600});T(g,bx+d0(1)*sc-12,by-ht+30,'no outrigger',{'font-size':19,'text-anchor':'end'});
 const P=plot(g,{x:395,y:70,w:215,h:250,x0:0,x1:1,y0:0,y1:100,xt:[0,.25,.5,.75,1],yt:[0,25,50,75,100],xl:'level, share of H',yl:'sway reduction %'});
 curve(g,P,x=>calc(Math.max(x,.02),r).dred*100,.02,1,'s-push',80,{'stroke-width':3});circ(g,P.X(a),P.Y(c.dred*100),8,'f-ink',{stroke:'var(--halo)','stroke-width':3});
 tiles(L.out,[{l:'Sway reduced by',v:Math.round(c.dred*100),u:'%'},{l:'Core base moment reduced by',v:Math.round(c.mred*100),u:'%',s:'the outrigger takes the rest'},{l:'Best level for this r',v:Math.round(best(r)*100),u:'% of H'}])}
function best(r){let b=.1,bv=-1;for(let a=.1;a<=.95;a+=.01){const v=calc(a,r).dred;if(v>bv){bv=v;b=a}}return b}
d();
""")],
 quiz=[dict(q='A frame leans most where?', o=['Near the top','Near the bottom, where storey shear is biggest','Evenly'], a=1, w='A frame sways in shear mode. Drift per storey follows the storey shear, which peaks at the base.'),
  dict(q='Where does one outrigger work best, in a typical tower?', o=['At the roof','About mid-height','At the base'], a=1, w='Near 0.45–0.6 of the height for one outrigger, depending on stiffness. Two outriggers share the work better.'),
  dict(q='Which system is best against torsion?', o=['Frame','Closed core or tube','Isolated walls'], a=1, w='A closed section resists twisting as a loop of shear flow.')],
 rules=['Use the simplest system that meets drift: frames below ~25 floors, walls to ~35–40, then add dual action, outriggers or a tube.','Outrigger levels are heavy: they often double as refuge or MEP floors.','Differential column shortening between core and perimeter loads the outrigger. Plan the construction sequence.','A hard-working core needs shear, not just bending: check the base shear stress and coupling beams.'],
 codes=['IS 16700:2023','IS 456:2000 cl 32','IS 13920:2016 cl 9','IS 875 (Part 3) / IS 1893 for loads']))

# ---------------------------------------------------------------- 15
PAGES.append(dict(n=15, slug='drift-torsion-irregularity', group='Tall buildings',
 title='Drift, torsion and irregularities',
 lede='If the centre of mass and the centre of stiffness do not line up, the building twists. One corner moves much more than the other. That is torsion, and codes watch for it.',
 sections=[
 dict(h='Move the mass, watch the twist', p='A rigid floor sits on two end frames. Make one frame stiffer, or shift the mass, and the floor rotates. Compare the two edge drifts.', js=r"""
const L=Lab(H,{h:420,label:'Floor plan twisting about its centre of stiffness',note:'Two end frames resisting a force along Y at the centre of mass. Rotation exaggerated. IS 1893 asks designers to add accidental eccentricity of 5% of the plan dimension, and calls the plan torsionally irregular if Δmax / Δmin > 1.5.'});
const sk=slider(L.sl,{label:'Right frame stiffness ÷ left',min:.3,max:4,step:.1,value:1.6,fmt:v=>f1(v)+' ×',on:d});
const sm=slider(L.sl,{label:'Centre of mass position',min:0,max:1,step:.01,value:.5,fmt:v=>Math.round(v*100)+'% across',on:d});
const ac=chips(L.sl,[['Accidental ecc. on',1],['off',0]],d,1,'Add 5% accidental eccentricity');
function d(){const g=L.svg,kR=sk.v(),kL=1,B=1,xm=sm.v();clear(g);
 const xr=kR*B/(kL+kR),K=kL+kR,Kt=kL*xr*xr+kR*(B-xr)**2;
 let e=xm-xr;if(ac.get())e=e+(e>=0?.05:-.05);
 const u0=1/K,th=e/Kt,dL=u0-th*xr,dR=u0+th*(B-xr),mx=Math.max(dL,dR),mn=Math.min(dL,dR),avg=(dL+dR)/2;
 const px=90,py=70,pw=420,ph=200,sc=60*1/Math.max(mx,.01);
 rect(g,px,py,pw,ph,'f-slab');
 line(g,px,py,px,py+ph,'s-thick',{'stroke-width':8});line(g,px+pw,py,px+pw,py+ph,'s-thick',{'stroke-width':8+Math.min(10,kR*2)});
 const dl=dL*sc*.55,dr=dR*sc*.55;
 poly(g,[[px,py+dl],[px+pw,py+dr],[px+pw,py+ph+dr],[px,py+ph+dl]],{class:'f-none',stroke:'var(--push)','stroke-width':3,'stroke-dasharray':'8 5'});
 circ(g,px+xm*pw,py+ph/2,10,'f-pushs',{stroke:'var(--halo)','stroke-width':2});T(g,px+xm*pw,py+ph/2-18,'mass',{'text-anchor':'middle','font-size':19});
 circ(g,px+xr*pw,py+ph/2,10,'f-waters',{stroke:'var(--halo)','stroke-width':2});T(g,px+xr*pw,py+ph/2+36,'stiffness',{'text-anchor':'middle','font-size':19});
 arrow(g,px+xm*pw,py+ph+60,px+xm*pw,py+ph+14,'s-push','ah',{'stroke-width':3});
 T(g,px,py-12,'left Δ '+f2(dL/dL*(dL/avg)),{'font-size':20,'font-weight':600});T(g,px+pw,py-12,'right Δ '+f2(dR/avg),{'font-size':20,'font-weight':600,'text-anchor':'end'});
 tiles(L.out,[{l:'Eccentricity e',v:f2(Math.abs(e)*100),u:'% of B'},{l:'Δmax ÷ Δavg',v:f2(mx/avg),c:mx/avg>1.4?'bad':mx/avg>1.2?'warn':'ok',st:mx/avg>1.4?'Too much twist (IS 16700 style limit 1.4)':mx/avg>1.2?'Getting twisty':'Fine'},{l:'Δmax ÷ Δmin',v:f2(mx/mn),c:mx/mn>1.5?'bad':'ok',st:mx/mn>1.5?'IS 1893: torsionally irregular':'Within 1.5'}])}
d();
"""),
 dict(h='The soft storey', p='One weak floor takes all the drift. Reduce the stiffness of one storey and see where the drift piles up. Compare it with the 0.4% limit.', js=r"""
const L=Lab(H,{h:490,label:'Storey drift down a building with one soft storey',note:'Shear building, lateral force ∝ height. Drift ratio scaled so a uniform building has 0.30% at the base. Soft storey per IS 1893 Table 6: stiffness below 70% of the storey above, or below 80% of the average of the three above.'});
const sn=slider(L.sl,{label:'Number of storeys',min:6,max:40,step:1,value:20,fmt:v=>v+'',on:d});
const sp=slider(L.sl,{label:'Soft storey at level',min:1,max:40,step:1,value:3,fmt:v=>'storey '+v,on:d});
const sr=slider(L.sl,{label:'Its stiffness, share of normal',min:20,max:100,step:5,value:50,fmt:v=>v+'%',on:d});
function d(){const g=L.svg,N=sn.v(),p=Math.min(sp.v(),N),r=sr.v()/100;clear(g);
 const k=i=>i===p?r:1;let sum=N*(N+1)/2;const Vi=[];for(let i=1;i<=N;i++){let s=0;for(let j=i;j<=N;j++)s+=j;Vi[i]=s/sum}
 const dr=i=>.3*(Vi[i]/k(i))/Vi[1];
 const top=36,bot=420,dy=(bot-top)/N;const P=plot(g,{x:70,y:top,w:520,h:bot-top,x0:0,x1:Math.max(.6,Math.ceil(Math.max(...Array.from({length:N},(_,i)=>dr(i+1)))*10+1)/10),y0:0,y1:N,xt:5,yt:[],xl:'storey drift ratio, %',yl:''});
 for(let i=1;i<=N;i++){const y=P.Y(i),w=P.X(dr(i))-P.x;rect(g,P.x,y,Math.max(1,w),dy*.8,dr(i)>.4?'f-pushs':'f-waters',{opacity:i===p?1:.75})}
 line(g,P.X(.4),P.y,P.X(.4),P.y+P.h,'s-push',{'stroke-dasharray':'8 5','stroke-width':3});T(g,P.X(.4)+8,P.y+22,'IS 1893 limit 0.4%',{'font-size':19});
 T(g,P.x+6,P.Y(p)-6,'soft storey '+p,{'font-size':19,'font-weight':600});
 const kav=N-p>=3?(k(p+1)+k(p+2)+k(p+3))/3:null,soft=(p<N&&k(p)<.7*k(p+1))||(kav!==null&&k(p)<.8*kav),mxd=Math.max(...Array.from({length:N},(_,i)=>dr(i+1)));
 tiles(L.out,[{l:'Worst storey drift',v:f2(mxd),u:'%',c:mxd>.4?'bad':'ok',st:mxd>.4?'Over 0.4%':'Within limit'},{l:'Soft storey?',v:soft?'Yes':'No',c:soft?'bad':'ok',st:soft?'IS 1893: soft storey irregularity':'Regular stiffness'},{l:'Drift ratio, soft ÷ normal',v:f1(dr(p)/Math.max(dr(p===N?p-1:p+1),.001)),u:'×'}])}
d();
""")],
 quiz=[dict(q='Centre of mass and centre of stiffness do not coincide. What does the floor do?', o=['Nothing','Rotates under a sideways force','Slides only'], a=1, w='The force acts through the mass but the structure resists through its stiffness. The offset creates a twisting moment.'),
  dict(q='IS 1893 flags a floor as torsionally irregular when Δmax / Δmin is more than…', o=['1.2','1.5','2.0'], a=1, w='1.5 (Table 5). IS 16700 style checks on tall buildings often use tighter limits on Δmax / Δavg.'),
  dict(q='A storey with a stiffness of 65% of the one above is…', o=['Fine','A soft storey','Extreme soft storey'], a=1, w='Below 70% of the storey above makes it soft. Below 60% is extreme soft (Table 6).')],
 rules=['Put the core near the centre of plan and keep walls spread out around the edges.','Soft and weak storeys cost lives: transfer floors, open ground storeys, and tall podiums are the usual causes.','Drift limits: 0.4% of storey height for earthquake (IS 1893), and tighter wind drift limits for tall buildings under IS 16700.','Accidental eccentricity of 5% of plan dimension must be added to the design eccentricity.'],
 codes=['IS 1893 (Part 1):2016 cl 7.1, Tables 5 and 6','IS 1893 cl 7.11.1.1 (drift)','IS 16700:2023 cl 5','IS 13920:2016']))

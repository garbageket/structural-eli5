PAGES = []

# ---------------------------------------------------------------- 07
PAGES.append(dict(n=7, slug='rc-beam', group='RCC design',
 title='How a reinforced concrete beam works',
 lede='Concrete squeezes at the top. Steel pulls at the bottom. The neutral axis sits between them and tells you how the beam will fail.',
 sections=[
 dict(h='Add steel and watch the neutral axis move', p='Slide the steel area. More steel pulls the neutral axis down. Too much, and concrete crushes before steel yields. That is the <b>brittle</b> failure you must avoid.', js=r"""
const L=Lab(H,{h:440,label:'Beam section, strain diagram and stress block',note:'IS 456 Annex G, singly reinforced rectangular section. d = D − 50 mm. Stress block: 0.36 f<sub>ck</sub> over 0.42 x<sub>u</sub>. Steel elastic-plastic for the picture.'});
const sb=slider(L.sl,{label:'Width b',min:200,max:600,step:25,value:300,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Depth D',min:300,max:1000,step:25,value:600,fmt:v=>v+' mm',on:d});
const sA=slider(L.sl,{label:'Tension steel Ast',min:200,max:6000,step:50,value:1500,fmt:v=>f0(v)+' mm²',on:d});
const fc=chips(L.sl,[['M25',25],['M30',30],['M40',40],['M50',50]],d,30,'Concrete');
const fyc=chips(L.sl,[['Fe415',415],['Fe500',500],['Fe550',550]],d,500,'Steel');
function solve(b,dd,A,fck,fy){const Es=2e5,fyd=.87*fy;let lo=1,hi=dd;for(let i=0;i<60;i++){const x=(lo+hi)/2,es=.0035*(dd-x)/x,fs=Math.min(Es*es,fyd);if(.36*fck*b*x>fs*A)hi=x;else lo=x}
 const x=(lo+hi)/2,es=.0035*(dd-x)/x,fs=Math.min(Es*es,fyd);return {x:x,es:es,fs:fs}}
function Mu(b,dd,A,fck,fy){const kx=.0035/(.0035+.87*fy/2e5+.002),xm=kx*dd,fyd=.87*fy;const xu=fyd*A/(.36*fck*b);
 if(xu<=xm)return {M:fyd*A*(dd-.42*xu)/1e6,xu:xu,xm:xm,lim:false};return {M:.36*fck*b*xm*(dd-.42*xm)/1e6,xu:xu,xm:xm,lim:true}}
function d(){const b=sb.v(),D=sD.v(),dd=D-50,A=sA.v(),fck=fc.get(),fy=fyc.get(),g=L.svg;clear(g);
 const r=solve(b,dd,A,fck,fy),m=Mu(b,dd,A,fck,fy),sc=.36,x0=40,top=40;
 const kx=m.xm/dd,xr=r.x/dd,over=r.x>m.xm*1.001,bal=Math.abs(r.x-m.xm)<m.xm*.03;
 rect(g,x0,top,b*sc,D*sc,'f-conc');
 const yna=top+r.x*sc;rect(g,x0,top,b*sc,r.x*sc,'f-push',{opacity:.55});
 line(g,x0-12,yna,x0+b*sc+12,yna,'s-ink',{'stroke-dasharray':'7 5'});T(g,x0+b*sc+14,yna+7,'neutral axis',{'font-size':19});
 const nb=Math.max(2,Math.min(8,Math.round(A/314)));for(let i=0;i<nb;i++)circ(g,x0+22+(b*sc-44)*i/(nb-1),top+(D-50)*sc,6,'f-steel');
 dimV(g,x0-24,top,top+D*sc,D+'',{dx:-10});
 // strain
 const xs=300;line(g,xs,top,xs,top+D*sc,'s-ink');T(g,xs+4,top-10,'strain',{'font-size':20,'text-anchor':'middle'});
 const cl=80,es=Math.min(r.es/.0035*cl,150),ys=top+dd*sc;
 line(g,xs-cl,top,xs,yna,'s-push',{'stroke-width':3});line(g,xs,yna,xs+es,ys,'s-push',{'stroke-width':3});
 T(g,xs-cl-4,top+22,'0.0035',{'text-anchor':'end','font-size':19});T(g,xs+es+8,ys+22,f3(r.es),{'font-size':19});
 // stress
 const xt=450;T(g,xt+50,top-10,'forces',{'font-size':20,'text-anchor':'middle'});
 rect(g,xt,top,70,.807*r.x*sc,'f-push');
 const Cf=.36*fck*b*r.x/1000,Tf=r.fs*A/1000;
 T(g,xt+78,top+.42*r.x*sc+6,'C '+f0(Cf)+' kN',{'font-size':20,'font-weight':600});
 arrow(g,xt+70,ys,xt-4,ys,'s-ok','aho',{'stroke-width':4});T(g,xt+78,ys+6,'T '+f0(Tf)+' kN',{'font-size':20,'font-weight':600});
 line(g,xt+36,top+.42*r.x*sc,xt+36,ys,'s-muted');T(g,xt+44,(top+.42*r.x*sc+ys)/2+6,'lever arm',{'font-size':18});
 const pt=100*A/(b*dd),pmin=85/fy,pmax=4;
 const mode=over?'Over-reinforced':bal?'Balanced':'Under-reinforced';
 tiles(L.out,[{l:'xu / d',v:f2(r.x/dd),c:over?'bad':'ok',st:'limit '+f2(kx),s:mode},{l:'Moment capacity Mu',v:f0(m.M),u:'kNm',s:m.lim?'capped at limiting value':'IS 456 G-1.1'},{l:'Steel strain',v:f3(r.es),c:r.fs<.87*fy-1?'bad':'ok',st:r.fs<.87*fy-1?'steel not yielding':'steel yields'},{l:'Steel ratio pt',v:f2(pt),u:'%',c:pt<pmin?'bad':pt>pmax?'bad':'ok',st:'min '+f2(pmin)+'%, max 4%'},{l:'Failure',v:over?'Brittle':'Ductile',c:over?'bad':'ok',st:over?'concrete crushes first':'steel yields first'}])}
d();
// Mu vs Ast
const L2=Lab(H,{h:400,label:'Moment capacity against steel area',note:'The curve flattens at the limiting section: extra steel beyond it does nothing for capacity, and makes the beam brittle.'});
function d2(){const g=L2.svg;clear(g);const b=sb.v(),D=sD.v(),dd=D-50,fck=fc.get(),fy=fyc.get(),A=sA.v();
 const Amax=Math.min(6000,.04*b*D);const Mm=Mu(b,dd,Amax*1.5,fck,fy).M;
 const P=plot(g,{x0:0,x1:6000,y0:0,y1:Math.ceil(Mm*1.15/100)*100,xt:6,yt:5,xl:'steel area, mm²',yl:'Mu, kNm'});
 curve(g,P,a=>Mu(b,dd,a,fck,fy).M,10,6000,'s-push',150,{'stroke-width':3.5});
 const kx=.0035/(.0035+.87*fy/2e5+.002),Al=.36*fck*b*kx*dd/(.87*fy);
 line(g,P.X(Al),P.y,P.X(Al),P.y+P.h,'s-muted');T(g,P.X(Al)+8,P.y+26,'balanced: '+f0(Al),{'font-size':19});
 circ(g,P.X(A),P.Y(Mu(b,dd,A,fck,fy).M),9,'f-ink',{stroke:'var(--halo)','stroke-width':3});
 L2.out.innerHTML='<p>Left of the dashed line: steel yields, beam gives warning. Right: do not add steel. Deepen the section instead.</p>'}
[sb,sD,sA].forEach(e=>e.addEventListener('input',d2));[fc,fyc];
const _d=d;d2();
"""),
 ],
 quiz=[dict(q='A beam has too much steel. What happens at failure?', o=['Steel yields slowly and the beam sags a lot','Concrete crushes suddenly with little warning','Nothing, more steel is always safer'], a=1, w='Over-reinforced beams fail by crushing, which is brittle. IS 456 limits x_u to x_u,max.'),
  dict(q='The most efficient way to raise a beam’s moment capacity is to…', o=['Add more bars','Increase the depth','Raise the concrete grade'], a=1, w='Capacity ~ Ast × lever arm. Depth raises the lever arm and gives a lot more than extra bars or grade.'),
  dict(q='Why is there a minimum steel limit (0.85/fy × 100 %)?', o=['To save cost','So the beam does not fail suddenly when it cracks','To control shear'], a=1, w='With too little steel, the first crack releases more force than steel can take, and the beam snaps.')],
 rules=['Under-reinforced is the goal: steel yields first and warns you.','Mu ≈ 0.87 fy Ast × (d − 0.42 xu). Depth is the big lever.','Keep pt between 0.85/fy and 4% (practically under 2.5%).','Check shear, deflection and cracking after flexure. Flexure rarely governs alone.'],
 codes=['IS 456:2000 cl 26.5.1 (steel limits)','IS 456 Annex G (flexure)','IS 456 cl 38.1','SP 16 design aids']))

# ---------------------------------------------------------------- 08
PAGES.append(dict(n=8, slug='slabs', group='RCC design',
 title='Slabs: one-way, two-way and flat slabs',
 lede='A slab spans in one direction or two, depending on its shape. A flat slab has no beams, and its danger is a column punching through it.',
 sections=[
 dict(h='Which way does a slab span?', p='Stretch the slab. A square panel splits its load both ways. A long thin one passes almost everything to its short side.', js=r"""
const L=Lab(H,{h:440,label:'Slab plan with load sharing arrows',note:'Load share by equal-deflection strips: w<sub>short</sub> = w × l<sub>y</sub>⁴ / (l<sub>x</sub>⁴ + l<sub>y</sub>⁴). IS 456 cl 24.4: treat as two-way when l<sub>y</sub> / l<sub>x</sub> ≤ 2.'});
const sx=slider(L.sl,{label:'Short span lx',min:3,max:8,step:.5,value:4,fmt:v=>f1(v)+' m',on:d});
const sy=slider(L.sl,{label:'Long span ly',min:3,max:14,step:.5,value:6,fmt:v=>f1(v)+' m',on:d});
const sp=chips(L.sl,[['Continuous (26)',26],['Simply supported (20)',20]],d,26,'Edges (IS 456 span/depth)');
function d(){const lx=sx.v(),ly=Math.max(sy.v(),lx),g=L.svg;clear(g);
 const s=Math.min(480/ly,330/lx),W=ly*s,Hh=lx*s,x0=(640-W)/2,y0=30;
 rect(g,x0,y0,W,Hh,'f-slab');
 const wx=ly**4/(lx**4+ly**4),wy=1-wx;
 for(let i=1;i<=6;i++){const x=x0+W*i/7;arrow(g,x,y0+Hh*.5-Hh*.38*wx-6,x,y0+8,'s-push','ah',{'stroke-width':1+wx*6,opacity:.9});arrow(g,x,y0+Hh*.5+Hh*.38*wx+6,x,y0+Hh-8,'s-push','ah',{'stroke-width':1+wx*6,opacity:.9})}
 if(wy>.03)for(let j=1;j<=3;j++){const y=y0+Hh*j/4;arrow(g,x0+W*.5-W*.38*wy-6,y,x0+8,y,'s-water','ahw',{'stroke-width':1+wy*6});arrow(g,x0+W*.5+W*.38*wy+6,y,x0+W-8,y,'s-water','ahw',{'stroke-width':1+wy*6})}
 dimH(g,x0,x0+W,y0+Hh+34,'ly = '+f1(ly)+' m');dimV(g,x0-14,y0,y0+Hh,'lx = '+f1(lx)+' m');
 const two=ly/lx<=2,dd=lx*1000/sp.get(),D=Math.ceil((dd+25)/5)*5;
 tiles(L.out,[{l:'ly / lx',v:f2(ly/lx),c:two?'ok':'warn',st:two?'Two-way slab':'One-way slab'},{l:'Carried in short direction',v:Math.round(wx*100),u:'%'},{l:'Main steel',v:two?'Both ways':'Short way',s:two?'short-direction bars at the bottom layer':'distribution steel the other way'},{l:'Thickness guide',v:f0(D),u:'mm',s:'lx / '+sp.get()+', basic'}])}
d();
"""),
 dict(h='Flat slabs: the column punches through', p='With no beams, the column pushes up through the slab like a punch through paper. The check is shear around the column, at half the slab depth.', js=r"""
const L=Lab(H,{h:430,label:'Punching shear around a column in a flat slab',note:'Interior square column. Critical section at d/2 from the column face: b<sub>0</sub> = 4(c + d). Allowable τ<sub>c</sub> = k<sub>s</sub> × 0.25√f<sub>ck</sub>, k<sub>s</sub> = 1 here. d = D − 35 mm (IS 456 cl 31.6).'});
const sc=slider(L.sl,{label:'Column size c',min:300,max:1000,step:50,value:500,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Slab thickness D',min:150,max:400,step:10,value:250,fmt:v=>v+' mm',on:d});
const sV=slider(L.sl,{label:'Factored column load Vu',min:200,max:5000,step:50,value:1500,fmt:v=>f0(v)+' kN',on:d});
const fc=chips(L.sl,[['M30',30],['M40',40],['M50',50]],d,40,'Concrete');
const dp=checkbox(L.sl,'Add a drop panel (+100 mm at the column)',d,false);
function d(){const c=sc.v(),D0=sD.v(),Vu=sV.v(),fck=fc.get(),D=D0+(dp.checked?100:0),dd=D-35,g=L.svg;clear(g);
 const b0=4*(c+dd),tv=Vu*1000/(b0*dd),tc=.25*Math.sqrt(fck),u=tv/tc,need=(-c+Math.sqrt(c*c+Vu*1000/tc))/2;
 const k=.15,px=140,py=210;
 rect(g,px-120,py-120,240,240,'f-slab');
 rect(g,px-(c+dd)*k/2,py-(c+dd)*k/2,(c+dd)*k,(c+dd)*k,'f-push',{'stroke-dasharray':'6 4'});
 rect(g,px-c*k/2,py-c*k/2,c*k,c*k,'f-ink');
 T(g,px,py+112+34,'plan: critical perimeter',{'text-anchor':'middle','font-size':19});
 // section
 const sx=400,yb=290,ks=.42;
 rect(g,sx-40,yb-D0*ks,260,D0*ks,'f-conc');
 if(dp.checked)rect(g,sx+30,yb,110,100*ks,'f-conc');
 rect(g,sx+30+(dp.checked?0:0),yb+(dp.checked?100*ks:0),110,90,'f-conc');
 rect(g,sx+50,yb+(dp.checked?100*ks:0),70,100,'f-conc');
 const cw=c*.12;
 line(g,sx+85-cw/2,yb+(dp.checked?100*ks:0),sx+85-cw/2-dd*ks,yb-D0*ks,'s-push',{'stroke-width':3,'stroke-dasharray':'7 5'});
 line(g,sx+85+cw/2,yb+(dp.checked?100*ks:0),sx+85+cw/2+dd*ks,yb-D0*ks,'s-push',{'stroke-width':3,'stroke-dasharray':'7 5'});
 arrow(g,sx+85,yb+170,sx+85,yb+110,'s-push','ah',{'stroke-width':5});T(g,sx+85,yb+196,f0(Vu)+' kN',{'text-anchor':'middle','font-size':21,'font-weight':600});
 T(g,sx+85,60,'the 45° cone that punches out',{'text-anchor':'middle','font-size':19});
 tiles(L.out,[{l:'Shear stress τv',v:f2(tv),u:'MPa'},{l:'Allowable τc',v:f2(tc),u:'MPa'},{l:'Utilisation',v:Math.round(u*100),u:'%',c:u<=1?(u>.85?'warn':'ok'):u<=1.5?'warn':'bad',st:u<=1?'OK':u<=1.5?'Needs shear reinforcement':'Fails: thicken'},{l:'d needed',v:f0(need),u:'mm',s:'you have '+f0(dd)}])}
d();
""")],
 quiz=[dict(q='A slab is 3 m × 7 m. Which way does most of the load travel?', o=['Short direction','Long direction','Equally'], a=0, w='ly/lx = 2.3, so it behaves as one-way. The stiffer short strip takes almost everything.'),
  dict(q='You want to stop a flat slab punching. The best single fix is…', o=['More bottom steel','More thickness or a drop panel','Higher steel grade'], a=1, w='Punching resists with concrete shear over b0 × d, and d counts twice: once in the perimeter, once in the depth.'),
  dict(q='The IS 456 span/depth limit is higher for a continuous slab than a simply supported one because…', o=['Continuity reduces mid-span moment and sag','Continuous slabs use more steel','It is cheaper'], a=0, w='Continuity cuts the sagging moment, so the slab can be thinner for the same sag.')],
 rules=['If ly / lx > 2, design as one-way. Do not skimp on distribution steel.','Slab thickness is set by deflection, not strength. Thicker is usually cheaper than more steel.','Flat slabs: always check punching at the column and at drop panel edges.','Edge and corner columns punch with unbalanced moment. Their stresses are higher than this simple check.'],
 codes=['IS 456:2000 cl 24 (slabs)','IS 456 cl 31.6 (punching shear)','IS 456 Annex D (coefficients)','IS 456 cl 23.2 (span/depth)']))

# ---------------------------------------------------------------- 09
PAGES.append(dict(n=9, slug='shear-walls-cores', group='RCC design',
 title='Shear walls and cores in tall buildings',
 lede='Tall buildings lean into the wind. The stiff concrete core is the spine that holds them upright. Shape it right and it does the work of a whole frame.',
 sections=[
 dict(h='Shape the core, change the sway', p='A box core is far stiffer than the same walls left open. Choose a shape and slide the sizes. The picture on the right shows the sway under wind.', js=r"""
const L=Lab(H,{h:480,label:'Core plan and building sway',note:'Wind pushes in Y. E = 5000√fck for M50 × 0.7 cracked. Drift = wH⁴ / 8EI. Limit H/500 (typical for tall buildings). This is the core alone: real towers add perimeter walls or frames. Openings not included.'});
const sh=chips(L.sl,[['Closed box',0],['Open U',1],['Two walls',2]],d,0,'Core shape');
const sx=slider(L.sl,{label:'Core width Lx',min:6,max:20,step:.5,value:12,fmt:v=>f1(v)+' m',on:d});
const sy=slider(L.sl,{label:'Core depth Ly',min:6,max:20,step:.5,value:12,fmt:v=>f1(v)+' m',on:d});
const st=slider(L.sl,{label:'Wall thickness',min:200,max:800,step:25,value:500,fmt:v=>v+' mm',on:d});
const sH=slider(L.sl,{label:'Building height H',min:60,max:300,step:10,value:150,fmt:v=>v+' m',on:d});
const sw=slider(L.sl,{label:'Wind load, line load',min:20,max:150,step:5,value:50,fmt:v=>v+' kN/m',on:d});
function Ixx(shape,Lx,Ly,t){const P=[];const web=[t*Ly,Ly/2,t*Ly**3/12],fl=[t*Lx,0,Lx*t**3/12],fl2=[t*Lx,Ly,Lx*t**3/12];
 if(shape===0){P.push(web,web,fl,fl2)}else if(shape===1){P.push(web,web,fl)}else{P.push(web,web)}
 const A=P.reduce((a,p)=>a+p[0],0),yb=P.reduce((a,p)=>a+p[0]*p[1],0)/A;return P.reduce((a,p)=>a+p[2]+p[0]*(p[1]-yb)**2,0)}
function d(){const shape=sh.get(),Lx=sx.v(),Ly=sy.v(),t=st.v()/1000,Hh=sH.v(),w=sw.v(),g=L.svg;clear(g);
 const I=Ixx(shape,Lx,Ly,t),E=5000*Math.sqrt(50)*1e3*.7,dr=w*Hh**4/(8*E*I)*1000,ratio=Hh*1000/dr;
 const s=14,px=40,py=100;
 rect(g,px-4,py-4,Lx*s+8,Ly*s+8,'f-none',{stroke:'var(--line)'});
 const tw=Math.max(5,t*s*2.2);
 rect(g,px,py,tw,Ly*s,'f-conc');rect(g,px+Lx*s-tw,py,tw,Ly*s,'f-conc');
 if(shape<=1)rect(g,px,py,Lx*s,tw,'f-conc');if(shape===0)rect(g,px,py+Ly*s-tw,Lx*s,tw,'f-conc');
 T(g,px+Lx*s/2,py+Ly*s+34,'plan',{'text-anchor':'middle','font-size':20});
 arrow(g,px+Lx*s/2,py-40,px+Lx*s/2,py-8,'s-push','ah',{'stroke-width':4});T(g,px+Lx*s/2+10,py-18,'wind',{'font-size':19});
 const bx=420,by=420,ht=340,sc=ht/Hh,maxOff=Math.min(150,dr/1000*sc*60);
 rect(g,bx-24,by,48,10,'f-conc');
 const q=[];for(let i=0;i<=40;i++){const z=i/40,def=(6-4*z+z*z)*z*z/3;q.push([bx+def*maxOff,by-z*ht])}
 pline(g,[[bx,by],[bx,by-ht]],'s-muted');
 pline(g,q,'s-thick',{'stroke-width':14,stroke:'var(--conc2)'});pline(g,q,'s-push',{'stroke-width':3});
 T(g,bx-30,by-ht/2,f0(Hh)+' m',{'text-anchor':'end','font-size':21});
 T(g,q[40][0]+10,q[40][1]+4,f0(dr)+' mm',{'font-size':21,'font-weight':700});
 tiles(L.out,[{l:'Stiffness I',v:f0(I),u:'m⁴'},{l:'Top sway',v:f0(dr),u:'mm',c:ratio>=500?'ok':'bad',st:ratio>=500?'OK':'Too flexible'},{l:'H / drift',v:f0(ratio),s:'needs ≥ 500'},{l:'Base moment',v:f0(w*Hh*Hh/2/1000),u:'MNm'}])}
d();
"""),
 dict(h='Link the walls and they act as one', p='Two walls joined by stiff coupling beams resist as one deep section. Walls alone just add. Slide the coupling and see the stiffness grow.', js=r"""
const L=Lab(H,{h:440,label:'Two walls joined by coupling beams',note:'I<sub>eff</sub> = 2I<sub>wall</sub> + γ × 2A(d/2)². γ = 0: no link (walls act alone). γ = 1: fully composite (rigid links). Real coupling is partial.'});
const sg=slider(L.sl,{label:'Coupling beam stiffness γ',min:0,max:1,step:.05,value:.5,fmt:v=>f2(v),on:d});
const sd=slider(L.sl,{label:'Distance between walls',min:3,max:20,step:.5,value:10,fmt:v=>f1(v)+' m',on:d});
function d(){const g=L.svg;clear(g);const gm=sg.v(),dist=sd.v(),Lw=5,t=.4,Iw=t*Lw**3/12,A=t*Lw;
 const I0=2*Iw,I=I0+gm*2*A*(dist/2)**2;const top=40,bot=380;
 const wx1=190-dist*6,wx2=190+dist*6;
 rect(g,wx1-10,top,20,bot-top,'f-conc');rect(g,wx2-10,top,20,bot-top,'f-conc');
 for(let i=1;i<=10;i++){const y=top+i*(bot-top)/11;line(g,wx1+10,y,wx2-10,y,'s-beam',{'stroke-width':2+gm*8,opacity:gm<.02?.2:1})}
 const bx=470;T(g,bx,top-6,'stiffness',{'text-anchor':'middle','font-size':20});
 const k=Math.min(1,I/(I0+2*A*(20/2)**2));rect(g,bx-30,bot-(bot-top)*k,60,(bot-top)*k,'f-push');
 T(g,bx,bot+30,f1(I/I0)+'× walls alone',{'text-anchor':'middle','font-size':21,'font-weight':600});
 tiles(L.out,[{l:'Stiffness gain',v:f1(I/I0),u:'×',s:'sway falls to '+Math.round(I0/I*100)+'% of the walls-alone value'},{l:'Moment resisted by',v:Math.round(gm*2*A*(dist/2)**2/I*100),u:'%',s:'axial push-pull in the walls, not bending'}])}
d();
""")],
 quiz=[dict(q='Which core shape is stiffest against twisting and sway: closed box or open U?', o=['Open U','Closed box','Same'], a=1, w='A closed section carries torsion as a loop and acts as a stiffer composite. Open sections twist badly and shear lag.'),
  dict(q='You double wall thickness. Core stiffness…', o=['Doubles','Roughly doubles','Quadruples'], a=1, w='I is linear in t for thin walls. Length matters far more: it goes with length³.'),
  dict(q='Coupling beams between walls resist wind by creating…', o=['Axial push-pull in the walls','More bending in the walls','Tension in slabs'], a=0, w='The pair acts like one big section: one wall pulls, the other pushes, over a long lever arm.')],
 rules=['Stiffness is geometry: length³ × thickness. Spread walls wide, not thick.','Place the core near the centre of plan to limit torsion.','Openings and door cuts weaken a core a lot. Check them at the base.','Cracked stiffness: use modifiers when you check drift (see topic 26).'],
 codes=['IS 16700:2023','IS 13920:2016 cl 9 (shear walls)','IS 456:2000 cl 32 (walls)','IS 1893 (Part 1):2016 cl 7']))

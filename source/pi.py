PAGES = []

# ---------------------------------------------------------------- 25
PAGES.append(dict(n=25, slug='etabs-reviewer-red-flags', group='Analysis and checking',
 title='Reading an ETABS model like a reviewer',
 lede='You do not need to re-run the model to catch most errors. A handful of numbers tell you whether it can be trusted. Check them first.',
 sections=[
 dict(h='Five gauges every model must pass', p='Enter the numbers from the model. Each gauge turns red when a check fails. These are the first five questions a reviewer asks.', js=r"""
const L=Lab(H,{h:420,label:'Five review gauges with green zones',note:'Hand weight = area × storeys × load. Period compared with the IS 1893 empirical value. Mass participation ≥ 90% (IS 1893 cl 7.7.5.2). Response spectrum base shear scaled up to the static base shear (cl 7.7.3). Drift ≤ 0.4% (cl 7.11.1.1).'});
const sA=slider(L.sl,{label:'Floor area per storey (hand)',min:500,max:3500,step:50,value:1200,fmt:v=>f0(v)+' m²',on:d});
const sN=slider(L.sl,{label:'Storeys above base',min:10,max:80,step:1,value:40,fmt:v=>v+'',on:d});
const sW=slider(L.sl,{label:'Seismic weight in the model',min:100,max:1500,step:10,value:660,fmt:v=>v+' MN',on:d});
const sT=slider(L.sl,{label:'Model T1 ÷ empirical Ta',min:.3,max:3,step:.05,value:1.3,fmt:v=>f2(v),on:d});
const sM=slider(L.sl,{label:'Mass participation, weakest direction',min:60,max:100,step:1,value:92,fmt:v=>v+'%',on:d});
const sV=slider(L.sl,{label:'Response-spectrum shear ÷ static shear',min:40,max:130,step:1,value:100,fmt:v=>v+'%',on:d});
const sD=slider(L.sl,{label:'Max storey drift ratio',min:.05,max:.7,step:.01,value:.28,fmt:v=>f2(v)+'%',on:d});
function d(){const g=L.svg;clear(g);const hand=sA.v()*sN.v()*13/1000,diff=(sW.v()-hand)/hand*100;
 const rows=[['Weight vs hand check',diff,-30,30,-10,10,v=>(v>=0?'+':'')+f0(v)+'%',Math.abs(diff)<=10?0:Math.abs(diff)<=20?1:2],
  ['Period ÷ empirical Ta',sT.v(),.3,3,.8,2,v=>f2(v)+'×',sT.v()>=.8&&sT.v()<=2?0:sT.v()>=.6&&sT.v()<=2.5?1:2],
  ['Mass participation',sM.v(),60,100,90,100,v=>f0(v)+'%',sM.v()>=90?0:sM.v()>=85?1:2],
  ['Dynamic ÷ static shear',sV.v(),40,130,100,130,v=>f0(v)+'%',sV.v()>=100?0:sV.v()>=90?1:2],
  ['Storey drift ratio',sD.v(),0,.7,0,.4,v=>f2(v)+'%',sD.v()<=.4?0:sD.v()<=.45?1:2]];
 const x0=60,w=400;let bad=0,warn=0;
 rows.forEach((r,i)=>{const y=50+i*72,X=v=>x0+(v-r[2])/(r[3]-r[2])*w;T(g,x0,y-12,r[0],{'font-size':21,'font-weight':600});
  rect(g,x0,y,w,18,'f-slab');rect(g,X(r[4]),y,X(r[5])-X(r[4]),18,'f-ok');
  const st=r[7];if(st===2)bad++;if(st===1)warn++;
  circ(g,X(clamp(r[1],r[2],r[3])),y+9,12,st===0?'f-oks':st===1?'f-warns':'f-pushs',{stroke:'var(--halo)','stroke-width':3});
  T(g,x0+w+16,y+16,r[6](r[1]),{'font-size':22,'font-weight':700,style:st===2?'fill:var(--push)':st===1?'fill:var(--warn)':''})});
 tiles(L.out,[{l:'Hand weight',v:f0(hand),u:'MN',s:'13 kN/m² per floor'},{l:'Gauges failing',v:bad,c:bad?'bad':warn?'warn':'ok',st:bad?'Do not accept the model':warn?'Ask for an explanation':'Passes first review'},{l:'Gauges borderline',v:warn}])}
d();
"""),
 dict(h='Spot the red flag', p='Eight things you might see in a model summary or a table. Fine, or a red flag?', js=r"""
quiz(H,[
{q:'Self-weight multiplier = 1 in the dead load case, AND slab area loads that already include the slab’s own weight.',o:['Fine','Red flag'],a:1,w:'The slab weight is counted twice. Slab area loads should be only finishes and partitions when self-weight is switched on.'},
{q:'Mass source: 100% dead load + 25% live load on floors with live load up to 3 kN/m².',o:['Fine','Red flag'],a:0,w:'This matches IS 1893 Table 10: 25% below 3 kN/m², 50% above.'},
{q:'Mass source includes 100% of the live load.',o:['Fine','Red flag'],a:1,w:'It over-estimates seismic weight and shifts the period. Check against Table 10.'},
{q:'Static earthquake pattern is applied from ground to terrace, but the lift machine room and overhead tank are outside the pattern range.',o:['Fine','Red flag'],a:1,w:'Weight outside the pattern gets no earthquake force. The pattern range must include every mass above the base.'},
{q:'Hundreds of joints sit on top of each other at the same location on every floor.',o:['Fine','Red flag'],a:1,w:'Duplicate joints mean disconnected members and double-counted load transfer. Merge them.'},
{q:'Modal participation: 12 modes give 78% of the mass in Y.',o:['Fine','Red flag'],a:1,w:'IS 1893 asks for at least 90% in each direction. Add modes until you reach it.'},
{q:'Response spectrum results are scaled so the dynamic base shear equals the static base shear, in each direction.',o:['Fine','Red flag'],a:0,w:'This is the code requirement. Scale up if dynamic is lower than static.'},
{q:'Wall piers have no labels and spandrels are not defined, yet the model reports a wall design.',o:['Fine','Red flag'],a:1,w:'Wall design needs pier and spandrel labels. Without them, the design output may be blank or meaningless.'}]);
""")],
 quiz=[dict(q='A model’s weight is 25% above the hand check. First thing to look at?', o=['The wind load','Load patterns, self-weight multipliers and mass source','The foundation'], a=1, w='Weight mismatches nearly always trace to duplicated loads or wrong mass source.'),
  dict(q='T1 from the model is 0.5 × the empirical period. This suggests…', o=['A great structure','A model that is too stiff or missing mass','Nothing'], a=1, w='A model much stiffer than the empirical formula often has rigid zones, wrong modifiers or missing mass.'),
  dict(q='Dynamic base shear is 80% of static. You should…', o=['Accept it','Scale it up to 100% of static','Scale it down further'], a=1, w='IS 1893 asks for scaling to at least the static base shear.')],
 rules=['Review order: units and grid, materials and sections, modifiers, loads and mass source, supports and diaphragms, analysis cases, then results.','Always do a hand weight check and compare T1 with the empirical Ta.','Ask for the model-check report and load summary, not just the design output.','Anything you cannot explain is a question for the consultant, not an approval.'],
 codes=['IS 1893 (Part 1):2016 cl 7.7, 7.11','IS 1893 Table 10 (seismic weight)','IS 16700:2023','IS 875 (Parts 1, 2)']))

# ---------------------------------------------------------------- 26
PAGES.append(dict(n=26, slug='cracked-section-modifiers', group='Analysis and checking',
 title='Cracked section modifiers: stiffness changes with load',
 lede='Concrete cracks, and a cracked beam is much softer than the gross section on paper. The modifiers we type into the model say how soft.',
 sections=[
 dict(h='How soft is a cracked beam?', p='Slide the service moment. Below the cracking moment the beam is stiff. After cracking it falls to a fraction of that. See where your beam sits.', js=r"""
const L=Lab(H,{h:440,label:'Moment against curvature for a cracking beam',note:'Cracked inertia from the transformed section: b x²/2 = m A<sub>st</sub> (d − x), I<sub>cr</sub> = b x³/3 + m A<sub>st</sub> (d − x)². Modular ratio m = 280 / (3σ<sub>cbc</sub>), IS 456 Annex B. Effective inertia by Branson’s expression.'});
const sb=slider(L.sl,{label:'Width b',min:200,max:600,step:25,value:300,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Depth D',min:300,max:1000,step:25,value:600,fmt:v=>v+' mm',on:d});
const sA=slider(L.sl,{label:'Tension steel',min:400,max:6000,step:100,value:1800,fmt:v=>f0(v)+' mm²',on:d});
const fc=chips(L.sl,[['M25',25],['M30',30],['M40',40]],d,30,'Concrete');
const sm=slider(L.sl,{label:'Service moment, share of ultimate',min:5,max:100,step:1,value:45,fmt:v=>v+'%',on:d});
const SG={25:8.5,30:10,40:13};
function d(){const g=L.svg;clear(g);const b=sb.v(),D=sD.v(),dd=D-50,A=sA.v(),fck=fc.get(),m=280/(3*SG[fck]),E=5000*Math.sqrt(fck);
 const mA=m*A,x=(-mA+Math.sqrt(mA*mA+2*b*mA*dd))/b,Icr=b*x**3/3+mA*(dd-x)**2,Ig=b*D**3/12,r=Icr/Ig;
 const Mcr=.7*Math.sqrt(fck)*Ig/(D/2)/1e6,xu=.87*500*A/(.36*fck*b),Mu=.87*500*A*(dd-.42*Math.min(xu,.456*dd))/1e6;
 const Ma=Math.max(sm.v()/100*Mu,1e-6),Ie=Ma<=Mcr?Ig:Math.min(Ig,Icr+(Ig-Icr)*Math.pow(Mcr/Ma,3));
 const EIg=E*Ig/1e12,EIcr=E*Icr/1e12,phiCr=Mcr/EIg,phiU=phiCr+(Mu-Mcr)/EIcr;
 const P=plot(g,{x0:0,x1:phiU*1.05,y0:0,y1:Mu*1.15,xt:4,yt:5,xl:'curvature',yl:'moment, kNm'});
 const p=[[P.X(0),P.Y(0)],[P.X(phiCr),P.Y(Mcr)],[P.X(phiU),P.Y(Mu)]];pline(g,p,'s-thick');
 line(g,P.X(0),P.Y(0),P.X(phiCr*2.2),P.Y(Mcr*2.2),'s-muted');T(g,P.X(phiCr*2.2)-6,P.Y(Mcr*2.2)+24,'gross EI',{'font-size':19,'text-anchor':'end'});
 T(g,P.X(phiCr)+10,P.Y(Mcr)+30,'cracks at '+f0(Mcr),{'font-size':20});
 const phA=Ma<=Mcr?Ma/EIg:phiCr+(Ma-Mcr)/EIcr;circ(g,P.X(phA),P.Y(Ma),10,'f-pushs',{stroke:'var(--halo)','stroke-width':3});
 tiles(L.out,[{l:'Cracking moment',v:f0(Mcr),u:'kNm'},{l:'Ultimate moment',v:f0(Mu),u:'kNm'},{l:'Fully cracked I ÷ gross I',v:f2(r),s:'typical modifier 0.35',c:r<.25?'warn':'ok'},{l:'Effective I ÷ gross I',v:f2(Ie/Ig),s:Ma<=Mcr?'uncracked':'cracked at this load',c:Ma<=Mcr?'ok':'warn'}])}
d();
"""),
 dict(h='What modifiers do to the whole building', p='Cracked stiffness lengthens the period and increases the drift. Set modifiers by member type and see how the whole building responds.', js=r"""
const L=Lab(H,{h:380,label:'Period and drift under different stiffness modifiers',note:'Weighted stiffness of the lateral system: factor = Σ share × modifier. Period ∝ 1/√factor, drift ∝ 1/factor. Typical practice shown as presets. Project design basis fixes the values (IS 1893 / IS 16700).'});
const ty=chips(L.sl,[['Wall-only tower',[.9,.05,.05,0]],['Dual wall + frame',[.6,.15,.25,0]],['Frame',[0,.4,.6,0]]],d,[.6,.15,.25,0],'Lateral system');
const sw=slider(L.sl,{label:'Walls modifier',min:.2,max:1,step:.05,value:.7,fmt:v=>f2(v),on:d});
const sb=slider(L.sl,{label:'Beams modifier',min:.2,max:1,step:.05,value:.35,fmt:v=>f2(v),on:d});
const sc=slider(L.sl,{label:'Columns modifier',min:.4,max:1,step:.05,value:.7,fmt:v=>f2(v),on:d});
const s0=slider(L.sl,{label:'Period with gross sections',min:2,max:10,step:.1,value:5,fmt:v=>f1(v)+' s',on:d});
chips(L.sl,[['Gross (1.0)',[1,1,1]],['Strength level',[.7,.35,.7]],['Serviceability / wind',[.9,.7,.9]]],v=>{sw.set(v[0]);sb.set(v[1]);sc.set(v[2])},undefined,'Presets (check project basis)');
function d(){const g=L.svg;clear(g);const sh=ty.get(),f=sh[0]*sw.v()+sh[1]*sb.v()+sh[2]*sc.v(),T0=s0.v(),T1=T0/Math.sqrt(f),dr=1/f;
 const W=440,x0=80;T(g,x0,50,'period, s',{'font-size':21,'font-weight':600});rect(g,x0,64,T0/10*W,28,'f-water');rect(g,x0,100,T1/10*W,28,'f-push');
 T(g,x0+T0/10*W+10,84,'gross '+f1(T0),{'font-size':20});T(g,x0+T1/10*W+10,120,'cracked '+f1(T1),{'font-size':20,'font-weight':700});
 T(g,x0,200,'drift, relative',{'font-size':21,'font-weight':600});rect(g,x0,214,Math.min(W,W/4),28,'f-water');rect(g,x0,250,Math.min(W,W/4*dr),28,'f-push');
 T(g,x0+Math.min(W,W/4*dr)+10,270,f2(dr)+'×',{'font-size':20,'font-weight':700});
 tiles(L.out,[{l:'Stiffness factor',v:f2(f)},{l:'Period grows by',v:'+'+Math.round((T1/T0-1)*100),u:'%',c:'warn'},{l:'Drift grows by',v:'+'+Math.round((dr-1)*100),u:'%',c:dr>1.5?'bad':'warn'}])}
d();
""")],
 quiz=[dict(q='A typical flexural stiffness modifier for beams at strength level is…', o=['1.0','0.35','0.05'], a=1, w='About 0.35 Ig. Walls are 0.35–0.7 depending on cracking, columns 0.7. The project design basis states them.'),
  dict(q='Using gross stiffness for a drift check leads to…', o=['Safe results','Unconservative (too small) drift','No change'], a=1, w='Gross sections are stiffer than the cracked reality, so drift is under-predicted.'),
  dict(q='Cracked stiffness gives a period that is…', o=['Shorter','Longer','The same'], a=1, w='Less stiffness means longer period. For tall buildings this usually lowers the earthquake force but raises drift.')],
 rules=['Say in the design basis which modifiers apply to which check: wind drift, earthquake drift, strength, deflection.','Do not mix cracked stiffness for strength design with gross stiffness for drift.','A very low modifier on walls is the biggest lever on period and drift. Check it first.','Slabs: 0.25 for flat slabs carrying lateral load in flexure; 1.0 where only gravity matters.'],
 codes=['IS 456:2000 Annex C (effective moment of inertia)','IS 1893 (Part 1):2016 cl 6.4.3','IS 16700:2023','ACI 318 Table 6.6.3.1.1 (reference)']))

# ---------------------------------------------------------------- 27
PAGES.append(dict(n=27, slug='value-engineering-framing', group='Economy and practice',
 title='Value engineering in RCC framing',
 lede='The cheapest structure is not the one with the least concrete. It is the one with the least concrete, steel, formwork and time that still performs. Here are the levers.',
 sections=[
 dict(h='Which floor system for which span?', p='Slide the span. Each system has a sweet spot. The comparison uses simple rules for thickness and steel. Replace the rates with yours.', js=r"""
const L=Lab(H,{h:440,label:'Cost of floor systems per square metre of floor',note:'Indicative rules: beam-slab (secondary beams above 5 m), flat slab t = L/28, flat slab with drops t = L/34, PT flat slab t = L/38. Steel: slab 85, beam 140, flat slab 100 kg/m³; PT 35 kg/m³ + 3.5 kg/m² strand at ₹ 180/kg. Ratios, not quotes: replace with project rates.'});
const sL=slider(L.sl,{label:'Square bay span',min:5,max:12,step:.5,value:8,fmt:v=>f1(v)+' m',on:d});
const sc=slider(L.sl,{label:'Concrete rate',min:6000,max:14000,step:250,value:9000,fmt:v=>'₹'+f0(v)+' / m³',on:d});
const ss=slider(L.sl,{label:'Steel rate',min:55,max:100,step:1,value:75,fmt:v=>'₹'+v+' / kg',on:d});
const sf=slider(L.sl,{label:'Formwork rate',min:350,max:900,step:25,value:550,fmt:v=>'₹'+v+' / m²',on:d});
function sys(Lm){const out=[];
 // beam-slab
 {const a=Lm>5?Lm/2:Lm,t=Math.max(.125,a/32),Dm=Lm/11,b=.3,bl=(Lm>5?3:2)/Lm,cb=bl*b*(Dm-t);out.push({n:'Beam + slab',c:t+cb,s:t*85+cb*140,f:1+bl*(b+2*(Dm-t))*.9})}
 {const t=Math.max(.175,Lm/28);out.push({n:'Flat slab',c:t,s:t*100,f:1.0})}
 {const t=Math.max(.175,Lm/34),dp=.1/9;out.push({n:'Flat slab + drops',c:t+dp,s:(t+dp)*100,f:1.08})}
 {const t=Math.max(.2,Lm/38);out.push({n:'PT flat slab',c:t,s:t*35+3.5,f:1.0,pt:3.5})}
 return out}
function d(){const g=L.svg,Lm=sL.v(),cr=sc.v(),sr=ss.v(),fr=sf.v();clear(g);
 const S=sys(Lm).map(x=>{const steel=x.s*sr+(x.pt?x.pt*(180-sr):0);return Object.assign({cost:x.c*cr+steel+x.f*fr*.18},x)}),mn=Math.min(...S.map(x=>x.cost)),mx=Math.max(...S.map(x=>x.cost));
 const x0=190,w=380;S.forEach((s,i)=>{const y=60+i*80,best=s.cost===mn;T(g,20,y+24,s.n,{'font-size':22,'font-weight':best?700:500});
  rect(g,x0,y,s.cost/mx*w,38,best?'f-ok':'f-water');T(g,x0+s.cost/mx*w+10,y+26,'₹'+f0(s.cost),{'font-size':21,'font-weight':600});
  T(g,x0,y+62,'concrete '+f2(s.c)+' m³/m² · steel '+f1(s.s)+' kg/m²',{'font-size':17})});
 const bst=S.find(x=>x.cost===mn);
 tiles(L.out,[{l:'Cheapest at this span',v:bst.n,c:'ok'},{l:'Concrete',v:f2(bst.c),u:'m³/m²'},{l:'Steel',v:f1(bst.s),u:'kg/m²'},{l:'Saving vs the dearest',v:f0((mx-mn)/mx*100),u:'%'}]);
 L.out.insertAdjacentHTML('beforeend','<p>Flat slabs save floor-to-floor height and formwork, so on tall towers they often win despite more concrete. Beams win on long spans and where loads are heavy.</p>')}
d();
"""),
 dict(h='Match the concrete grade to the load', p='Load falls going up. The grade can fall too. Step the grade down the tower and see the saving against one grade throughout.', js=r"""
const L=Lab(H,{h:440,label:'A tower with concrete grade stepping down with height',note:'Core and column concrete only. Rates are illustrative ₹/m³. More grades means more testing and more risk of site mix-ups: three or four zones is the usual limit.'});
const sn=slider(L.sl,{label:'Storeys',min:20,max:80,step:1,value:50,fmt:v=>v+'',on:d});
const sv=slider(L.sl,{label:'Vertical concrete per floor',min:60,max:300,step:10,value:140,fmt:v=>v+' m³',on:d});
const sg=chips(L.sl,[['One grade M60',0],['Step every 20 floors',20],['Step every 10 floors',10]],d,20,'Grade strategy');
const RATE={30:6500,40:7500,50:8700,60:10000};
function grade(i,N,step){if(!step)return 60;const k=Math.floor((i)/step);return Math.max(30,60-5*k*2)}
function d(){const g=L.svg,N=sn.v(),V=sv.v(),st=sg.get();clear(g);
 let cost=0,base=0;const top=40,bot=400,dy=(bot-top)/N,col={30:'f-water',40:'f-ok',50:'f-warn',60:'f-push'};
 for(let i=0;i<N;i++){const gr=grade(i,N,st),gr2=60;let gg=gr;gg=gg>=60?60:gg>=50?50:gg>=40?40:30;cost+=V*RATE[gg];base+=V*RATE[60];rect(g,200,bot-(i+1)*dy,160,dy+.5,col[gg])}
 [[60,'M60'],[50,'M50'],[40,'M40'],[30,'M30']].forEach((r,i)=>{rect(g,420,70+i*40,24,24,col[r[0]]);T(g,452,90+i*40,r[1]+'  ₹'+f0(RATE[r[0]])+'/m³',{'font-size':20})});
 T(g,200,top-8,'top',{'font-size':19});T(g,200,bot+26,'base',{'font-size':19});
 tiles(L.out,[{l:'Vertical concrete cost',v:f1(cost/1e7),u:'₹ crore'},{l:'Saved vs one grade',v:f1((base-cost)/1e7),u:'₹ crore',c:'ok'},{l:'Saving',v:f0((base-cost)/base*100),u:'%'}]);
 L.out.insertAdjacentHTML('beforeend','<p>Higher grades also cut member size, which saves floor area. A saving is real only if grade changes line up with the actual load and formwork changes.</p>')}
d();
""")],
 quiz=[dict(q='A flat slab system on a tower often wins over beam-slab because…', o=['It uses less concrete per floor','It saves formwork, time and storey height','It needs no steel'], a=1, w='Simpler formwork and lower floor-to-floor height. Over 50 floors, the storey height saving is large.'),
  dict(q='Reducing the concrete grade up the tower mainly saves…', o=['Steel','Concrete cost, and wall or column size where design allows','Formwork'], a=1, w='Lower grades are cheaper per cubic metre, but sizes must still carry the load and meet durability grades.'),
  dict(q='The first place to look for savings in a tower’s structure?', o=['Foundations only','Repetition: same sizes, same spans and same formwork','Smaller bars'], a=1, w='Repetition cuts formwork cost and time and gives the contractor a faster cycle.')],
 rules=['Fix the grid early. A uniform grid with repeated spans beats the clever irregular one.','Slab thickness and column positions drive more cost than bar diameter.','Optimise the tower’s concrete grade, wall thickness and section size by zone, not floor by floor.','Check buildability and cycle time: a design that saves 3% in steel but adds a day per floor is a loss.'],
 codes=['IS 456:2000 Table 5 (min grades)','IS 16700:2023','IS 13920:2016','IS 456 cl 23.2 (deflection)']))

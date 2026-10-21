PAGES = []

# ---------------------------------------------------------------- 22
PAGES.append(dict(n=22, slug='piles', group='Geotechnical and foundations',
 title='Piles: how they carry load',
 lede='A pile holds up a building in two ways: friction along its sides and bearing at its tip. Which one does the work depends on the ground it passes through.',
 sections=[
 dict(h='Skin friction and tip bearing', p='Choose the soil along the pile, then change its length and width. Watch how much comes from the shaft and how much from the tip.', js=r"""
const L=Lab(H,{h:470,label:'Pile in soil with shaft friction and tip bearing',note:'Static formula, bored pile. Clay: shaft = 0.5 c<sub>u</sub>, tip = 9 c<sub>u</sub>. Sand: shaft = 0.35 × vertical effective stress (max 100 kPa), tip = 30 σ′ (max 4 MPa). Rock: shaft 100 kPa, tip 3 MPa. Safe load = Q<sub>u</sub> / 2.5 (IS 2911). Indicative only.'});
const sd=slider(L.sl,{label:'Pile diameter',min:.4,max:1.5,step:.05,value:.9,fmt:v=>f2(v)+' m',on:d});
const sl=slider(L.sl,{label:'Pile length',min:5,max:50,step:1,value:30,fmt:v=>v+' m',on:d});
const so=chips(L.sl,[['Soft clay',0],['Stiff clay',1],['Dense sand',2],['Weathered rock',3]],d,1,'Soil along the pile');
function cap(dm,Lm,t){const per=Math.PI*dm,Ab=Math.PI*dm*dm/4;let Qs=0,qb=0;
 if(t<=1){const cu=t===0?30:100;Qs=per*Lm*.5*cu;qb=9*cu}
 else if(t===2){const n=200;for(let i=0;i<n;i++){const z=(i+.5)/n*Lm;Qs+=per*Math.min(3.5*z,100)*Lm/n}qb=Math.min(300*Lm,4000)}
 else{Qs=per*Lm*100;qb=3000}return {Qs:Qs,Qb:qb*Ab}}
let safe1=1000;
function d(){const g=L.svg,dm=sd.v(),Lm=sl.v(),t=so.get();clear(g);
 const c=cap(dm,Lm,t),Qu=c.Qs+c.Qb;safe1=Qu/2.5;
 const gx=200,top=60,ht=330,sc=ht/50,py=top+Lm*sc;
 rect(g,40,top,320,ht+30,t<=1?'f-clay':t===2?'f-sand':'f-conc');
 rect(g,40,top-40,320,40,'f-slab');
 const pw=Math.max(14,dm*46);rect(g,gx-pw/2,top-34,pw,py-top+34,'f-conc',{stroke:'var(--ink)','stroke-width':2});
 arrow(g,gx,top-70,gx,top-38,'s-push','ah',{'stroke-width':5});
 const n=Math.max(2,Math.round(Lm/5)),fr=c.Qs/Qu;
 for(let i=0;i<n;i++){const y=top+8+(py-top-16)*i/(n-1||1);arrow(g,gx-pw/2-8,y+14,gx-pw/2-8,y-10,'s-water','ahw',{'stroke-width':2+fr*3});arrow(g,gx+pw/2+8,y+14,gx+pw/2+8,y-10,'s-water','ahw',{'stroke-width':2+fr*3})}
 arrow(g,gx,py+50,gx,py+4,'s-ok','aho',{'stroke-width':3+(1-fr)*8});
 T(g,gx+pw/2+30,(top+py)/2,'friction '+Math.round(fr*100)+'%',{'font-size':21,'font-weight':600});T(g,gx+pw/2+30,py+44,'tip '+Math.round((1-fr)*100)+'%',{'font-size':21,'font-weight':600});
 dimV(g,70,top,py,Lm+' m',{dx:-10});
 tiles(L.out,[{l:'Shaft friction',v:f0(c.Qs),u:'kN'},{l:'Tip bearing',v:f0(c.Qb),u:'kN'},{l:'Ultimate Qu',v:f0(Qu),u:'kN'},{l:'Safe load, FS 2.5',v:f0(Qu/2.5),u:'kN',c:'ok'},{l:'Load per m of pile',v:f0(Qu/2.5/Lm),u:'kN/m'}]);
 if(window.__g)window.__g()}
d();
// group
const L2=Lab(H,{h:400,label:'Pile group plan with spacing',note:'Converse–Labarre efficiency: E = 1 − θ [(n−1)m + (m−1)n] / (90 m n), θ = atan(d / s) in degrees. Applies to friction piles in clay. In sand, group efficiency is often near 1 for bored piles. IS 2911 minimum spacing: 2.5d for friction piles, 2d for end bearing.'});
const ss=slider(L2.sl,{label:'Spacing ÷ diameter  s / d',min:2,max:6,step:.25,value:3,fmt:v=>f2(v)+' d',on:d2});
const gm=chips(L2.sl,[['2 × 2',2],['3 × 3',3],['4 × 4',4],['5 × 5',5]],d2,3,'Pile arrangement');
function d2(){const g=L2.svg,m=gm.get(),sdv=ss.v(),dm=sd.v();clear(g);
 const sp=Math.min(110,300/((m-1)*sdv+1)),r=sp/sdv/2,ox=320,oy=185;
 const w=(m-1)*sp+2*r*2.2;rect(g,ox-w/2+((m-1)*sp)/2-((m-1)*sp)/2,oy-w/2,w,w,'f-conc',{opacity:.6});
 for(let i=0;i<m;i++)for(let j=0;j<m;j++)circ(g,ox-(m-1)*sp/2+i*sp,oy-(m-1)*sp/2+j*sp,r,'f-steel');
 const th=deg(Math.atan(1/sdv)),E=1-th*((m-1)*m+(m-1)*m)/(90*m*m),N=m*m;
 line(g,ox-(m-1)*sp/2,oy+w/2+14,ox-(m-1)*sp/2+sp,oy+w/2+14,'s-ink');T(g,ox-(m-1)*sp/2+sp/2,oy+w/2+36,'s = '+f2(sdv*dm)+' m',{'text-anchor':'middle','font-size':19});
 tiles(L2.out,[{l:'Group efficiency',v:f2(E),c:E>=.8?'ok':'warn'},{l:'Piles',v:N},{l:'Group capacity',v:f0(E*N*safe1),u:'kN',s:'if friction piles in clay'},{l:'Spacing check',v:sdv>=2.5?'OK':sdv>=2?'End bearing only':'Too close',c:sdv>=2.5?'ok':sdv>=2?'warn':'bad',st:'IS 2911 min 2.5d, 2d'}])}
window.__g=d2;d2();
// load test
const L3=Lab(H,{h:430,label:'Pile load test curve with safe load criteria',note:'Illustrative load-settlement curve. IS 2911 (Part 4): safe load is the lesser of two-thirds of the load at 12 mm settlement, and half of the load at settlement equal to 10% of the pile diameter.'});
const sq=slider(L3.sl,{label:'Pile ultimate capacity',min:1000,max:12000,step:500,value:5000,fmt:v=>f0(v)+' kN',on:d3});
const sd3=slider(L3.sl,{label:'Pile diameter',min:.4,max:1.5,step:.05,value:.9,fmt:v=>f2(v)+' m',on:d3});
function d3(){const g=L3.svg,Qu=sq.v(),dm=sd3.v();clear(g);const s=Q=>(4*(Q/Qu)+30*Math.pow(Q/Qu,5))*(dm/.9);
 const inv=y=>{let a=0,b=3*Qu;for(let i=0;i<60;i++){const m=(a+b)/2;if(s(m)<y)a=m;else b=m}return (a+b)/2};
 const P=plot(g,{x0:0,x1:Qu*1.5,y0:40,y1:0,xt:5,yt:[0,10,20,30,40],xl:'load, kN',yl:'settlement, mm'});
 curve(g,P,Q=>s(Q),0,Qu*1.5,'s-push',120,{'stroke-width':3.5});
 const Q12=inv(12),Q10=inv(dm*100),safe=Math.min(2/3*Q12,.5*Q10);
 line(g,P.x,P.Y(12),P.X(Q12),P.Y(12),'s-muted');line(g,P.X(Q12),P.Y(12),P.X(Q12),P.y,'s-muted');circ(g,P.X(Q12),P.Y(12),7,'f-ink');
 line(g,P.X(safe),P.y,P.X(safe),P.y+P.h,'s-ok',{'stroke-width':3});T(g,P.X(safe)+8,P.y+P.h-14,'safe '+f0(safe),{'font-size':21,'font-weight':600});
 tiles(L3.out,[{l:'Load at 12 mm',v:f0(Q12),u:'kN',s:'⅔ of it: '+f0(2/3*Q12)},{l:'Load at 10% of d',v:f0(Q10),u:'kN',s:'half of it: '+f0(.5*Q10)},{l:'Safe load',v:f0(safe),u:'kN',c:'ok',st:'÷ Qu = '+f2(safe/Qu)}])}
d3();
""")],
 quiz=[dict(q='A pile in soft clay on weak ground below is mainly a…', o=['End-bearing pile','Friction pile','Tension pile'], a=1, w='With nothing firm to rest on, most load is carried by friction along the shaft.'),
  dict(q='Close pile spacing in a group in clay…', o=['Raises capacity per pile','Lowers capacity per pile (group effect)','Has no effect'], a=1, w='Stress zones overlap, so each pile contributes less than alone. Keep at least 2.5d for friction piles.'),
  dict(q='The safe load from a load test is based on…', o=['The settlement at the test load','Both a 12 mm settlement and a 10%-of-diameter settlement criterion','The cost of the pile'], a=1, w='IS 2911 (Part 4) takes the lesser of two-thirds the load at 12 mm and half the load at 10% of diameter.')],
 rules=['Rock sockets and end-bearing in hard strata give stiff piles. Friction piles in clay can settle a lot.','Do load tests on trial piles before final design. They calibrate the soil numbers.','Piles take lateral load poorly. Add raking piles or rely on basement walls and the raft.','Negative skin friction from settling fill can add to pile load: check it for fill sites.'],
 codes=['IS 2911 (Part 1/Sec 2):2010 bored piles','IS 2911 (Part 4):2013 load tests','IS 14593 (bored cast-in-situ rock socket)','IS 456:2000 cl 34 (pile caps)']))

# ---------------------------------------------------------------- 23
PAGES.append(dict(n=23, slug='basements-excavation', group='Geotechnical and foundations',
 title='Basements, deep excavation and dewatering',
 lede='Dig below the water table and the ground tries to float your building. Keeping the site dry and the neighbours safe takes as much design as the structure itself.',
 sections=[
 dict(h='Will the basement float?', p='Water pushes up on the base slab with the height of water above it. The building’s weight pushes down. See how much margin you have.', js=r"""
const L=Lab(H,{h:440,label:'Basement with water pressure under the raft',note:'Uplift = γw × (raft level − water table depth). Weight includes raft and all floors, dead load only. Typical minimum factor of safety 1.1 against flotation (check your project criteria). Use the highest ground-water level.'});
const sb=slider(L.sl,{label:'Basement depth',min:2,max:18,step:.5,value:9,fmt:v=>f1(v)+' m',on:d});
const sw=slider(L.sl,{label:'Water table depth below ground',min:0,max:12,step:.5,value:2,fmt:v=>f1(v)+' m',on:d});
const sW=slider(L.sl,{label:'Weight of building per m² of raft',min:40,max:600,step:10,value:120,fmt:v=>v+' kN/m²',on:d});
const sA=slider(L.sl,{label:'Raft area',min:500,max:6000,step:100,value:2500,fmt:v=>f0(v)+' m²',on:d});
function d(){const g=L.svg,B=sb.v(),w=sw.v(),W=sW.v(),A=sA.v();clear(g);
 const U=Math.max(0,9.81*(B-w)),fs=U>0?W/U:99;
 const top=60,sc=18,gb=top+B*sc;
 rect(g,0,top,640,380,'f-sand');rect(g,0,top-30,640,30,'f-slab');
 if(w<B+4)rect(g,0,top+Math.min(w,B+2)*sc,640,440-top-Math.min(w,B+2)*sc,'f-none',{fill:'var(--water)','fill-opacity':'var(--wf)'});
 line(g,0,top+w*sc,640,top+w*sc,'s-water',{'stroke-width':3});
 rect(g,150,top-30,340,B*sc+30,'f-slab',{stroke:'var(--ink)','stroke-width':3,fill:'var(--bg)'});
 rect(g,140,gb,360,22,'f-conc');
 const ua=Math.min(70,U*.5);
 for(let i=0;i<7;i++)arrow(g,160+i*52,gb+90,160+i*52,gb+26,'s-water','ahw',{'stroke-width':2+Math.min(3,U/60)});
 arrow(g,320,top-70,320,top-34,'s-push','ah',{'stroke-width':3+Math.min(8,W/60)});T(g,336,top-48,'weight '+f0(W)+' kN/m²',{'font-size':21,'font-weight':600});
 T(g,320,gb+112,'uplift '+f0(U)+' kN/m²',{'text-anchor':'middle','font-size':21,'font-weight':600,style:'fill:var(--water)'});
 T(g,620,top+w*sc-8,'water table',{'text-anchor':'end','font-size':19,style:'fill:var(--water)'});
 const deficit=Math.max(0,(1.1*U-W)*A);
 tiles(L.out,[{l:'Uplift',v:f0(U),u:'kN/m²'},{l:'Weight',v:f0(W),u:'kN/m²'},{l:'Factor of safety',v:fs>50?'∞':f2(fs),c:fs>=1.1?'ok':'bad',st:fs>=1.1?'Safe against flotation':'Floats'},{l:'Extra tie-down needed',v:f0(deficit/1000),u:'MN',s:deficit>0?'= '+Math.ceil(deficit/1500)+' tension piles of 1500 kN':'none'}])}
d();
"""),
 dict(h='Pumping lowers the water, and the neighbours’ ground', p='To dig dry, wells draw the water table down. The cone of depression can stretch far in clean sand. See how much water you must pump, and how far the effect reaches.', js=r"""
const L=Lab(H,{h:440,label:'Cone of depression around a dewatering well',note:'Thiem equation, unconfined aquifer: Q = π k (H² − h²) / ln(R/r), radius of influence R = 3000 s √k (Sichardt). One well, uniform soil. Real design uses well fields, pumping tests and monitoring.'});
const sk=slider(L.sl,{label:'Permeability k',min:-6,max:-3,step:.25,value:-4.5,fmt:v=>'1e'+v+' m/s',on:d});
const ss=slider(L.sl,{label:'Drawdown at the well s',min:2,max:15,step:.5,value:8,fmt:v=>f1(v)+' m',on:d});
const sH=slider(L.sl,{label:'Aquifer thickness H',min:10,max:40,step:1,value:25,fmt:v=>v+' m',on:d});
function d(){const g=L.svg,k=Math.pow(10,sk.v()),s=Math.min(ss.v(),sH.v()-1),Hh=sH.v(),h=Hh-s,r=.15,R=Math.min(3000*s*Math.sqrt(k),1500);clear(g);
 const Rr=Math.max(R,2*r+1),Q=Math.PI*k*(Hh*Hh-h*h)/Math.log(Rr/r);
 const top=40,sc=240/Hh,gy=top+40,base=gy+Hh*sc,cx=60,W=520,xs=Math.max(Rr,20);
 rect(g,0,gy-40,640,40,'f-slab');rect(g,0,gy,640,Hh*sc+30,'f-sand');rect(g,0,base,640,30,'f-conc');
 const wl=[],wl2=[];
 for(let i=0;i<=80;i++){const x=Rr*i/80,xx=Math.max(x,r),hh=Math.sqrt(Math.max(0,Hh*Hh-(Hh*Hh-h*h)*Math.log(Rr/xx)/Math.log(Rr/r)));wl.push([cx+(x/xs)*W,base-hh*sc]);wl2.push([cx+(x/xs)*W,base-Hh*sc])}
 poly(g,wl.concat(wl2.slice().reverse()),{class:'f-push',opacity:.8});
 pline(g,wl,'s-water',{'stroke-width':3.5});line(g,cx,base-Hh*sc,640,base-Hh*sc,'s-muted');
 T(g,630,base-Hh*sc-10,'original water table',{'text-anchor':'end','font-size':19});
 rect(g,cx-6,gy-20,12,base-gy+20,'f-ink',{opacity:.6});
 T(g,cx+14,top+14,'well',{'font-size':20,'font-weight':600});
 dimH(g,cx,cx+(Rr/xs)*W,base+54,'R = '+f0(Rr)+' m',{});
 tiles(L.out,[{l:'Pumping rate',v:f1(Q*1000),u:'L/s',s:f0(Q*86400)+' m³ per day'},{l:'Radius of influence',v:f0(Rr),u:'m',c:Rr>150?'warn':'ok',st:Rr>150?'Neighbours may settle':'Local effect'},{l:'Water drawn down by',v:f1(s),u:'m'}]);
 L.out.insertAdjacentHTML('beforeend','<p>Clean sand (k near 1e-4) pulls water from far away. Clays barely move: dewatering them is slow and gives little.</p>')}
d();
""")],
 quiz=[dict(q='The base slab of a basement is 10 m below the water table. The uplift pressure is about…', o=['10 kN/m²','100 kN/m²','1000 kN/m²'], a=1, w='γw × 10 m = 98 kN/m². A big number against building weight.'),
  dict(q='Dewatering next to a neighbouring building can cause…', o=['Nothing','Settlement of the neighbour’s foundations','Stronger soil'], a=1, w='Removing water increases effective stress, which compresses soft soil and settles buildings, sometimes far away.'),
  dict(q='If a basement would float, a common fix is…', o=['Make it lighter','Tension piles or anchors, or thicker raft weight','Ignore it'], a=1, w='Add weight (thicker raft), tie it down (tension piles, rock anchors), or relieve pressure with drains.')],
 rules=['Design basements for the highest likely water table, and check flotation during construction too.','Waterproofing and structure work together: crack control, water stops and construction joints matter as much as thickness.','Retaining walls of a basement are propped by floors: design for K₀ plus water, not active pressure.','Monitor neighbouring buildings and the water level during dewatering.'],
 codes=['IS 456:2000 cl 20 (stability)','IS 3370 (Part 2) (crack width)','IS 9556 (diaphragm walls)','IS 14458 (retaining walls)']))

# ---------------------------------------------------------------- 24
PAGES.append(dict(n=24, slug='etabs-modelling', group='Analysis and checking',
 title='How ETABS models a building',
 lede='A model is a simplified picture of the building made of lines, plates and rules. Know what each piece assumes, and you know where it can lie to you.',
 sections=[
 dict(h='Mesh: how finely to cut a wall', p='Walls and slabs are cut into small elements. Coarse cuts are stiff and wrong. Fine cuts are right and slow. Move the cell size and see how the error and element count change.', js=r"""
const L=Lab(H,{h:440,label:'A wall panel meshed into elements',note:'Illustrative convergence: stress error falls fast with a finer mesh. As a rule of thumb, mesh walls and slabs to about 0.5–1.0 m and always make elements match at the junctions.'});
const sm=slider(L.sl,{label:'Element size',min:.25,max:1.5,step:.05,value:.75,fmt:v=>f2(v)+' m',on:d});
const sw=slider(L.sl,{label:'Wall length',min:2,max:10,step:.5,value:6,fmt:v=>f1(v)+' m',on:d});
function d(){const g=L.svg,h=sm.v(),Lw=sw.v(),Hh=3.2;clear(g);
 const nx=Math.max(1,Math.ceil(Lw/h)),ny=Math.max(1,Math.ceil(Hh/h)),sc=Math.min(520/Lw,260/Hh),w=Lw*sc,hh=Hh*sc,x0=(640-w)/2,y0=70;
 rect(g,x0,y0,w,hh,'f-slab',{stroke:'var(--ink)','stroke-width':2.5});
 for(let i=1;i<nx;i++)line(g,x0+w*i/nx,y0,x0+w*i/nx,y0+hh,'s-grid');for(let j=1;j<ny;j++)line(g,x0,y0+hh*j/ny,x0+w,y0+hh*j/ny,'s-grid');
 rect(g,x0-10,y0+hh,w+20,12,'f-conc');
 const err=Math.min(70,4*Math.pow(h/.25,1.5)*(1+.1*(nx<3?3:0))),nel=nx*ny;
 arrow(g,x0-60,y0+8,x0-4,y0+8,'s-push','ah',{'stroke-width':4});
 T(g,x0+w/2,y0-14,nx+' × '+ny+' elements',{'text-anchor':'middle','font-size':22,'font-weight':600});
 tiles(L.out,[{l:'Elements per storey wall',v:nel},{l:'Peak stress error',v:'~'+f0(err),u:'%',c:err<=12?'ok':err<=25?'warn':'bad',st:err<=12?'Good':err<=25?'Coarse':'Too coarse'},{l:'Across the wall',v:nx,u:'elements',c:nx>=3?'ok':'bad',st:nx>=3?'':'min 3 across'}])}
d();
"""),
 dict(h='Rigid, semi-rigid or flexible floor?', p='ETABS lets you pick how a floor spreads force to the frames. A rigid diaphragm shares by stiffness. A flexible one shares by area. The wrong choice changes the force on every frame.', js=r"""
const L=Lab(H,{h:400,label:'Two frames sharing a lateral load through a floor',note:'Uniform lateral load over a floor between a stiff frame on the right and a soft frame on the left. Rigid diaphragm: shares in proportion to stiffness. Flexible: by tributary area. Semi-rigid sits between the two.'});
const sk=slider(L.sl,{label:'Right frame stiffness ÷ left',min:1,max:8,step:.5,value:4,fmt:v=>f1(v)+' ×',on:d});
const dg=chips(L.sl,[['Rigid',0],['Semi-rigid',.5],['Flexible',1]],d,0,'Diaphragm');
function d(){const g=L.svg,k=sk.v(),f=dg.get();clear(g);
 const rigidR=k/(1+k),flexR=.5,R=rigidR*(1-f)+flexR*f,Lf=1-R;
 const px=100,py=90,pw=440,ph=130;rect(g,px,py,pw,ph,'f-slab');
 line(g,px,py,px,py+ph,'s-thick',{'stroke-width':6});line(g,px+pw,py,px+pw,py+ph,'s-thick',{'stroke-width':14});
 for(let i=1;i<9;i++)arrow(g,px+i*pw/9,py-48,px+i*pw/9,py-8,'s-push','ah',{'stroke-width':2});
 arrow(g,px-10,py+ph/2,px-10-Lf*100,py+ph/2,'s-ink','ahk',{'stroke-width':3+Lf*8});arrow(g,px+pw+10,py+ph/2,px+pw+10+R*100,py+ph/2,'s-ink','ahk',{'stroke-width':3+R*8});
 T(g,px-6,py+ph+40,'left frame '+Math.round(Lf*100)+'%',{'font-size':21,'font-weight':600});T(g,px+pw+6,py+ph+40,'right frame '+Math.round(R*100)+'%',{'text-anchor':'end','font-size':21,'font-weight':600});
 const dif=Math.abs(rigidR-flexR)/flexR*100;
 tiles(L.out,[{l:'Right frame share',v:Math.round(R*100),u:'%'},{l:'Left frame share',v:Math.round(Lf*100),u:'%'},{l:'Rigid vs flexible, right frame',v:'+'+f0(dif),u:'%',s:'the cost of assuming wrongly',c:'warn'}]);
 L.out.insertAdjacentHTML('beforeend','<p>Slabs with big openings, long thin plans (length over ~3× width) or very stiff walls sometimes need a semi-rigid diaphragm.</p>')}
d();
""")],
 quiz=[dict(q='A wall element mesh is too coarse. The model usually…', o=['Is too flexible','Is too stiff and under-predicts peak stresses','Is exact'], a=1, w='Coarse elements cannot bend into the right shape, so they are stiffer than reality and smear stress peaks.'),
  dict(q='A rigid diaphragm in ETABS assumes…', o=['The slab cannot deform in plane, floors move as one plate','The slab is infinitely thin','No slab at all'], a=0, w='All joints on the floor stay in a fixed shape in plan. Force shares by stiffness.'),
  dict(q='Beams drawn as lines connecting at column centres are modelled as…', o=['Plates','Frame elements with end offsets and rigid zones if set','Springs'], a=1, w='Frame objects have section properties, and rigid end zones can be set where they meet columns or walls.')],
 rules=['A model is a set of assumptions. List them: diaphragms, offsets, end releases, modifiers, support conditions.','Mesh auto-edge constraints and matching at wall-slab joints. A mismatch hides stress.','Check units, storeys and grid first. Wrong storey heights make everything after wrong.','Run a simple hand check on weight, base shear and period before trusting the results.'],
 codes=['IS 1893 (Part 1):2016 cl 7.2 (modelling)','IS 16700:2023','CSI ETABS manuals','IS 456:2000 (member design)']))

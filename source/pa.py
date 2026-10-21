PAGES = []

# ---------------------------------------------------------------- 01
PAGES.append(dict(n=1, slug='load-path', group='Foundations of structural behaviour',
 title='How loads flow through a building',
 lede='Every kilonewton you put on a floor has to reach the ground. Follow it down: slab, beam, column, footing, soil.',
 sections=[
 dict(h='Each column owns a patch of floor', p='A column carries the floor area closest to it, called its <b>tributary area</b>. Change the bays, pick a column, and watch the load add up floor after floor.', js=r"""
const L=Lab(H,{h:420,label:'Plan with beams and columns; tributary area of one column shaded',note:'Plan of a slab on beams, drawn to scale. Shaded patch = floor area feeding the chosen column. Column sized by IS 456 cl 39.3 with 2% steel, Fe500, load factor 1.5. Footing includes 10% self-weight.'});
const sx=slider(L.sl,{label:'Bay size X',min:3,max:12,step:.5,value:8,fmt:v=>f1(v)+' m',on:d});
const sy=slider(L.sl,{label:'Bay size Y',min:3,max:12,step:.5,value:8,fmt:v=>f1(v)+' m',on:d});
const sf=slider(L.sl,{label:'Floors above',min:1,max:60,step:1,value:20,fmt:v=>v+' floors',on:d});
const sw=slider(L.sl,{label:'Floor load, DL + LL',min:8,max:20,step:.5,value:12,fmt:v=>f1(v)+' kN/m²',on:d});
const ss=slider(L.sl,{label:'Safe bearing capacity',min:100,max:600,step:25,value:300,fmt:v=>v+' kN/m²',on:d});
const cc=chips(L.sl,[['Interior','i'],['Edge','e'],['Corner','c']],d,'i','Which column');
const gg=chips(L.sl,[['M30',30],['M40',40],['M50',50],['M60',60]],d,40,'Column concrete');
function vals(){const bx=sx.v(),by=sy.v(),c=cc.get(),fl=sf.v(),w=sw.v();
 const A=(c==='c'?.25:c==='e'?.5:1)*bx*by,P=A*w*fl,Pu=1.5*P,fck=gg.get();
 const Ag=Pu*1000/(0.4*fck*.98+0.67*500*.02),side=Math.sqrt(Ag);
 const Af=P*1.1/ss.v();return {bx:bx,by:by,c:c,fl:fl,w:w,A:A,Pf:A*w,P:P,side:side,Af:Af}}
let after=null;
function d(){const v=vals(),g=L.svg;clear(g);
 const W=3*v.bx,Hh=3*v.by,s=Math.min(560/W,320/Hh),x0=(640-W*s)/2,y0=30;
 rect(g,x0,y0,W*s,Hh*s,'f-slab');
 const ix=v.c==='i'?1:0,iy=v.c==='c'?0:1;
 const cx=x0+ix*v.bx*s,cy=y0+iy*v.by*s;
 const tx0=Math.max(x0,cx-v.bx*s/2),tx1=Math.min(x0+W*s,cx+v.bx*s/2),ty0=Math.max(y0,cy-v.by*s/2),ty1=Math.min(y0+Hh*s,cy+v.by*s/2);
 rect(g,tx0,ty0,tx1-tx0,ty1-ty0,'f-push');
 for(let i=0;i<=3;i++){line(g,x0+i*v.bx*s,y0,x0+i*v.bx*s,y0+Hh*s,'s-beam');line(g,x0,y0+i*v.by*s,x0+W*s,y0+i*v.by*s,'s-beam')}
 for(let i=0;i<=3;i++)for(let j=0;j<=3;j++){const on=(i===ix&&j===iy);rect(g,x0+i*v.bx*s-8,y0+j*v.by*s-8,16,16,on?'f-ink':'f-steel')}
 T(g,(tx0+tx1)/2,(ty0+ty1)/2+(v.c==='c'?34:36),f0(v.A)+' m²',{'text-anchor':'middle','font-weight':600,'font-size':24});
 dimH(g,x0,x0+v.bx*s,y0+Hh*s+30,f1(v.bx)+' m');dimV(g,x0-14,y0,y0+v.by*s,f1(v.by)+' m');
 tiles(L.out,[{l:'Tributary area',v:f0(v.A),u:'m²'},{l:'Per floor',v:f0(v.Pf),u:'kN'},{l:'At the base',v:f0(v.P),u:'kN',s:'service load'},{l:'Column size',v:f0(Math.ceil(v.side/25)*25),u:'mm',s:'square, approx.'},{l:'Footing',v:f1(Math.sqrt(v.Af)),u:'m',s:'square, isolated'}]);if(after)after()}
// follow the load
const L2=Lab(H,{h:430,label:'Steps the load takes from slab to soil',note:'Press the button to follow one patch of load down to the ground.'});
button(L2.sl,'Follow the load',run,true);
const boxes=[];
function steps(){const v=vals(),udl=v.w*v.bx,end=udl*v.by/2;
 return [['1  Slab','w = '+f1(v.w)+' kN/m² on the floor'],['2  Beam','UDL = w × bay = '+f0(udl)+' kN/m'],['3  Beam ends','each end gives '+f0(end)+' kN'],['4  Column, one floor','two ends meet: '+f0(v.Pf)+' kN'],['5  Column, all floors','× '+v.fl+' floors = '+f0(v.P)+' kN'],['6  Footing to soil','pressure ≈ '+f0(v.P*1.1/v.Af)+' kN/m²']]}
function draw(on){const g=L2.svg;clear(g);const st=steps();
 st.forEach((s,i)=>{const y=14+i*68;rect(g,40,y,560,56,on===i?'f-push':'f-slab',{rx:10});
  circ(g,72,y+28,16,on===i?'f-pushs':'f-steel');T(g,72,y+35,String(i+1),{'text-anchor':'middle','font-size':20,style:'fill:var(--bg);stroke:none'});
  T(g,104,y+25,s[0].slice(3),{'font-size':22,'font-weight':600});T(g,104,y+46,s[1],{'font-size':19});
  if(i<5)arrow(g,320,y+56,320,y+68,'s-ink','ahk')})}
function run(){let i=-1;(function nx(){i++;draw(i);if(i<5)setTimeout(nx,reduce?200:750)})()}
after=()=>draw(-1);d();
"""),
 dict(h='Why ground-floor columns are huge', p='The same column at three heights. Load piles up, so the column grows. Slide the floors and watch the size.', js=r"""
const L=Lab(H,{h:400,label:'Column size growing down a tower',note:'Interior column, bay 8 m × 8 m, floor load 12 kN/m², M40, Fe500, 2% steel. Real towers also taper concrete grade upward.'});
const sf=slider(L.sl,{label:'Floors in the tower',min:5,max:70,step:1,value:40,fmt:v=>v+' floors',on:d});
function side(n){const P=64*12*n*1.5;return Math.sqrt(P*1000/(0.4*40*.98+0.67*500*.02))}
function d(){const n=sf.v(),g=L.svg;clear(g);const base=side(n),sc=170/Math.max(base,1);
 const top=30,bot=360,x=250;
 for(let i=0;i<n;i++){const y0=top+(bot-top)*i/n,y1=top+(bot-top)*(i+1)/n;const sd=side(i+1);const w=Math.max(6,sd*sc*.6);
  rect(g,x-w/2,y0,w,y1-y0+.5,'f-conc')}
 rect(g,x-130,bot,260,16,'f-conc');
 dimH(g,x-base*sc*.3,x+base*sc*.3,bot-14,'',{});
 T(g,x+base*sc*.3+14,bot-6,f0(Math.ceil(base/25)*25)+' mm at the base',{'font-size':22,'font-weight':600});
 T(g,x+Math.max(6,side(1)*sc*.6)/2+14,top+22,f0(Math.ceil(side(1)/25)*25)+' mm at the top',{'font-size':22});
 tiles(L.out,[{l:'Base load',v:f0(64*12*n),u:'kN'},{l:'Base column',v:f0(Math.ceil(base/25)*25),u:'mm'},{l:'Top column',v:f0(Math.ceil(side(1)/25)*25),u:'mm'}])}
d();
""")],
 quiz=[dict(q='A corner column and an interior column sit on the same grid. Which carries more floor load?', o=['The corner column','The interior column, about 4× more','They are equal'], a=1, w='An interior column feeds a full bay. A corner column feeds only a quarter of one.'),
  dict(q='You double the bay size in both directions. The column load per floor becomes…', o=['2×','4×','8×'], a=1, w='Load follows area, and area goes with the square of the span.'),
  dict(q='Why are ground-floor columns in towers so large?', o=['Soil is weak','They carry every floor above','Fire rules'], a=1, w='Axial load is the sum of all floors above. Designers also raise concrete grade to hold the size down.')],
 rules=['Quick check on any column: tributary area × floor load × number of floors. Compare it to your model.','Load goes where the stiffness leads, not where you draw the arrows.','Check the load at three places: the slab, the column, the footing.','Edge and corner columns see less gravity but more moment.'],
 codes=['IS 875 (Part 1) dead loads','IS 875 (Part 2) imposed loads','IS 456:2000 cl 39 (columns)','IS 16700:2023']))

# ---------------------------------------------------------------- 02
PAGES.append(dict(n=2, slug='beam-bending', group='Foundations of structural behaviour',
 title='Bending, shear and deflection in beams',
 lede='A beam does three jobs at once: it bends, it shears, it sags. See how span and depth change all three.',
 sections=[
 dict(h='Load a beam and read the diagrams', p='Pick the support type and load. The shear and bending diagrams redraw. Then change the <b>depth</b> and see what it does to sag.', js=r"""
const L=Lab(H,{h:560,label:'Beam with shear force and bending moment diagrams',note:'RC beam, M25, gross section (uncracked). Deflection is exaggerated in the picture. Real cracked deflection is larger.'});
const st=chips(L.sl,[['Simply supported','ss'],['Cantilever','ct'],['Fixed both ends','fx']],d,'ss','Supports');
const lt=chips(L.sl,[['Even load (UDL)','u'],['Point load','p']],d,'u','Load');
const sL=slider(L.sl,{label:'Span L',min:2,max:10,step:.5,value:6,fmt:v=>f1(v)+' m',on:d});
const sq=slider(L.sl,{label:'Load (kN/m or kN)',min:5,max:100,step:5,value:30,fmt:v=>v+'',on:d});
const sb=slider(L.sl,{label:'Width b',min:200,max:600,step:25,value:300,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Depth D',min:250,max:1000,step:25,value:500,fmt:v=>v+' mm',on:d});
function d(){const t=st.get(),k=lt.get(),Lm=sL.v(),q=sq.v(),b=sb.v(),D=sD.v();
 const EI=25000e3*(b/1000)*Math.pow(D/1000,3)/12;
 let V,M,Y,Mm,Vm,dm;
 if(t==='ss'&&k==='u'){V=x=>q*(Lm/2-x);M=x=>q*x*(Lm-x)/2;Y=x=>q*x*(Lm**3-2*Lm*x*x+x**3)/(24*EI);Mm=q*Lm*Lm/8;Vm=q*Lm/2;dm=5*q*Lm**4/(384*EI)}
 if(t==='ss'&&k==='p'){V=x=>x<Lm/2?q/2:-q/2;M=x=>x<Lm/2?q*x/2:q*(Lm-x)/2;Y=x=>{const u=x<Lm/2?x:Lm-x;return q*u*(3*Lm*Lm-4*u*u)/(48*EI)};Mm=q*Lm/4;Vm=q/2;dm=q*Lm**3/(48*EI)}
 if(t==='ct'&&k==='u'){V=x=>q*(Lm-x);M=x=>-q*(Lm-x)**2/2;Y=x=>q*x*x*(6*Lm*Lm-4*Lm*x+x*x)/(24*EI);Mm=q*Lm*Lm/2;Vm=q*Lm;dm=q*Lm**4/(8*EI)}
 if(t==='ct'&&k==='p'){V=x=>q;M=x=>-q*(Lm-x);Y=x=>q*x*x*(3*Lm-x)/(6*EI);Mm=q*Lm;Vm=q;dm=q*Lm**3/(3*EI)}
 if(t==='fx'&&k==='u'){V=x=>q*(Lm/2-x);M=x=>q*(6*Lm*x-6*x*x-Lm*Lm)/12;Y=x=>q*x*x*(Lm-x)**2/(24*EI);Mm=q*Lm*Lm/12;Vm=q*Lm/2;dm=q*Lm**4/(384*EI)}
 if(t==='fx'&&k==='p'){V=x=>x<Lm/2?q/2:-q/2;M=x=>{const u=x<Lm/2?x:Lm-x;return q*(4*u-Lm)/8};Y=x=>{const u=x<Lm/2?x:Lm-x;return q*u*u*(3*Lm-4*u)/(48*EI)};Mm=q*Lm/8;Vm=q/2;dm=q*Lm**3/(192*EI)}
 const g=L.svg;clear(g);const x0=70,w=500,N=80,sx=x=>x0+x/Lm*w;
 const sc=Math.min(50/Math.max(dm,1e-6),1e4);
 // loads
 if(k==='u'){for(let i=0;i<=12;i++){const x=x0+w*i/12;arrow(g,x,34,x,84,'s-push','ah')}line(g,x0,34,x0+w,34,'s-push')}
 else{const xp=t==='ct'?x0+w:x0+w/2;arrow(g,xp,20,xp,92,'s-push','ah',{'stroke-width':5})}
 // beam shape
 const pts0=[],pts1=[];for(let i=0;i<=N;i++){const x=Lm*i/N;pts0.push([sx(x),104]);pts1.push([sx(x),104+Y(x)*sc])}
 rect(g,x0,96,w,16,'f-conc');
 pline(g,pts1,'s-push',{'stroke-width':3.5});
 if(t==='ss'){pin(g,x0,112,14);roller(g,x0+w,112,14)}
 if(t==='ct'){rect(g,x0-16,70,16,80,'f-conc')}
 if(t==='fx'){rect(g,x0-16,70,16,80,'f-conc');rect(g,x0+w,70,16,80,'f-conc')}
 T(g,x0+w/2,176,'Shear force',{'font-size':20,'text-anchor':'middle','font-weight':600});
 const vm=Math.max(Vm,1e-6),sv=55/vm,y1=240;line(g,x0,y1,x0+w,y1,'s-ink');
 const qv=[[x0,y1]];for(let i=0;i<=N;i++){const x=Lm*i/N;qv.push([sx(x),y1-V(x)*sv])}qv.push([x0+w,y1]);poly(g,qv,{class:'f-push'});
 T(g,x0-6,y1-V(0.001)*sv+6,f0(Math.abs(V(0.001))),{'text-anchor':'end','font-size':19});
 T(g,x0+w/2,328,'Bending moment (tension side)',{'font-size':20,'text-anchor':'middle','font-weight':600});
 const y2=400,sm=65/Math.max(Mm,1e-6);line(g,x0,y2,x0+w,y2,'s-ink');
 // sagging plotted below axis, hogging above axis
 const qm2=[[x0,y2]];for(let i=0;i<=N;i++){const x=Lm*i/N;qm2.push([sx(x),y2+M(x)*sm])}qm2.push([x0+w,y2]);poly(g,qm2,{class:'f-water'});
 const mid=M(Lm/2);
 // labels
 const lab=(x,m)=>T(g,x,y2+(m>=0?M_off(m,sm):-8-Math.abs(m)*sm)-0,f0(Math.abs(m))+' kNm',{'font-size':19,'text-anchor':'middle'});
 function M_off(m,s){return m*s+22}
 lab(sx(Lm/2),mid);if(t!=='ss'){lab(sx(0.3),M(0.001))}
 const Dd=D/1000,Ld=Lm*1000/(D-50),lim=t==='ss'?20:t==='ct'?7:26;
 const z=b*D*D/6,sig=Mm*1e6/z;
 tiles(L.out,[{l:'Max moment',v:f0(Mm),u:'kNm'},{l:'Max shear',v:f0(Vm),u:'kN'},{l:'Sag (uncracked)',v:f1(dm*1000),u:'mm',c:dm*1000<=Lm*1000/250?'ok':'bad',st:'limit L/250 = '+f1(Lm*1000/250)+' mm'},{l:'Tension stress',v:f1(sig),u:'MPa',c:sig>3.5?'warn':'ok',st:sig>3.5?'concrete cracks':'uncracked',s:'cracks above 0.7√fck = 3.5 MPa'},{l:'Span / depth',v:f1(Ld),c:Ld<=lim?'ok':'warn',st:'IS 456 basic limit '+lim}])}
d();
"""),
 dict(h='Depth is the cheap way to stop sagging', p='Deflection falls with the <b>cube</b> of depth. Doubling the width only halves it. Move both and compare.', js=r"""
const L=Lab(H,{h:360,label:'Beam sections with equal concrete but different shapes',note:'Same span and load. Concrete volume is shown to compare cost. Deflection ∝ 1 / (b × D³).'});
const sb=slider(L.sl,{label:'Width b',min:200,max:600,step:25,value:300,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Depth D',min:300,max:900,step:25,value:500,fmt:v=>v+' mm',on:d});
function d(){const b=sb.v(),D=sD.v(),g=L.svg;clear(g);const I=b*D**3/12,I0=300*500**3/12;
 const sc=.42;
 rect(g,70,200-250*sc*.5,300*sc,500*sc,'f-ink',{opacity:.12});
 rect(g,70,200-250*sc*.5,300*sc,500*sc,'f-none',{stroke:'var(--muted)','stroke-dasharray':'5 4'});
 T(g,70,40,'reference 300 × 500',{'font-size':20});
 rect(g,350,200-D*sc*.5,b*sc,D*sc,'f-conc');
 T(g,350,40,'yours '+b+' × '+D,{'font-size':20,'font-weight':600});
 const rel=I0/I;
 tiles(L.out,[{l:'Stiffness EI',v:f2(I/I0),u:'×',s:'vs 300 × 500'},{l:'Sag',v:f2(rel),u:'×',c:rel<=1?'ok':'bad',st:rel<=1?'less than reference':'more than reference'},{l:'Concrete',v:f2(b*D/(300*500)),u:'×',s:'per metre of beam'},{l:'Steel lever arm',v:f0(D-50),u:'mm'}])}
d();
""")],
 quiz=[dict(q='A beam is too flexible. You can add 50% to its width or 50% to its depth. Which helps more?', o=['Width','Depth','Same'], a=1, w='Stiffness goes with b × D³. 1.5× width gives 1.5× stiffness. 1.5× depth gives 3.4×.'),
  dict(q='Where does a cantilever beam crack first?', o=['Top, at the support','Bottom, at mid span','At the free tip'], a=0, w='A cantilever hogs. Tension is on the top, so main steel goes on top at the support.'),
  dict(q='Doubling the span of a simply supported beam under UDL multiplies its moment by…', o=['2','4','8'], a=1, w='M = wL²/8, so it goes with L². Deflection goes with L⁴, which is 16×.')],
 rules=['Moment goes with L², shear with L, deflection with L⁴.','Depth buys stiffness cheaply. Width is the expensive way.','A fixed-end beam has half the sag of a simply supported one, but needs top steel at the supports.','Check deflection even when strength is fine: IS 456 cl 23.2 uses span/250, and span/350 after partitions.'],
 codes=['IS 456:2000 cl 22–23','IS 456 cl 23.2 (deflection)','IS 456 Annex C']))

# ---------------------------------------------------------------- 03
PAGES.append(dict(n=3, slug='columns-buckling', group='Foundations of structural behaviour',
 title='Columns and buckling',
 lede='A short column crushes. A slender one bows sideways and gives up long before it crushes. Slenderness decides which.',
 sections=[
 dict(h='Push a column and watch it bow', p='Load a column up to its <b>Euler load</b>. As you get close, a tiny wobble becomes a big sideways bow.', js=r"""
const L=Lab(H,{h:470,label:'Column bowing under axial load',note:'Square M30 column, 2% Fe500 steel. Euler load uses gross EI; cracking lowers it. Sideways bow is exaggerated and includes a small initial crookedness of L/500.'});
const sL=slider(L.sl,{label:'Column height L',min:2,max:14,step:.5,value:6,fmt:v=>f1(v)+' m',on:d});
const sD=slider(L.sl,{label:'Size D (square)',min:250,max:1000,step:25,value:400,fmt:v=>v+' mm',on:d});
const sp=slider(L.sl,{label:'Load as % of Euler load',min:0,max:99,step:1,value:50,fmt:v=>v+'%',on:d});
const en=chips(L.sl,[['Fixed–fixed 0.65',.65],['Fixed–pinned 0.8',.8],['Pinned–pinned 1.0',1],['Cantilever 2.0',2]],d,1,'Ends (IS 456 Table 28)');
function calc(){const Lm=sL.v(),D=sD.v()/1000,k=en.get(),Le=k*Lm,Ec=5000*Math.sqrt(30)*1e3,I=D**4/12;
 const Pcr=Math.PI**2*Ec*I/(Le*Le),Ag=D*D,Pcrush=(0.4*30*.98+0.67*500*.02)*1000*Ag;return {Lm:Lm,D:D,k:k,Le:Le,Pcr:Pcr,Pcrush:Pcrush}}
function d(){const c=calc(),pr=sp.v()/100,P=pr*c.Pcr,g=L.svg;clear(g);
 const x=320,top=50,bot=400,hpx=bot-top,e0=hpx/500*1;
 const amp=e0/(1-pr)*12;const N=60,q=[];
 for(let i=0;i<=N;i++){const t=i/N;let off;
  if(c.k===.65)off=Math.sin(Math.PI*t)**2;else if(c.k===.8)off=Math.sin(Math.PI*t)*(1-.5*t)*1.0;else if(c.k===1)off=Math.sin(Math.PI*t);else off=1-Math.cos(Math.PI*t/2);
  q.push([x+clamp(off*amp,-170,170),bot-t*hpx])}
 rect(g,x-130,bot,260,16,'f-conc');rect(g,x-130,top-16,260,16,'f-conc',{opacity:c.k===2?0:1});
 const w=Math.max(10,c.D*60);for(let i=0;i<N;i++){}
 pline(g,q,'s-thick',{'stroke-width':10,stroke:'var(--conc2)'});
 pline(g,q,'s-push',{'stroke-width':3});
 arrow(g,x+(q[N][0]-x),top-60,x+(q[N][0]-x),top-6,'s-push','ah',{'stroke-width':4+pr*8});
 T(g,x+(q[N][0]-x)+34,top-26,f0(P)+' kN',{'font-size':22,'font-weight':600});
 const sl=c.Le/c.D,Pu=Math.min(c.Pcrush,c.Pcr);
 const emin=Math.max(c.Lm*1000/500+c.D*1000/30,20),Ma=sl>12?1.5*P*c.D*1000/2000*sl*sl/1000:0;
 tiles(L.out,[{l:'Effective length',v:f1(c.Le),u:'m',s:'k × L'},{l:'Le / D',v:f1(sl),c:sl<=12?'ok':'warn',st:sl<=12?'short column':'slender column',s:'IS 456 limit 12'},{l:'Euler load',v:f0(c.Pcr),u:'kN'},{l:'Crush load',v:f0(c.Pcrush),u:'kN'},{l:'Governs',v:c.Pcr<c.Pcrush?'Buckling':'Crush',c:c.Pcr<c.Pcrush?'bad':'ok'},{l:'Extra moment',v:f0(Ma),u:'kNm',s:'cl 39.7, at 1.5 × load'}])}
d();
// capacity vs slenderness
const L2=Lab(H,{h:420,label:'Column capacity versus slenderness',note:'Capacity is the smaller of crushing and Euler buckling. The dot is your column.'});
function h_off(P){return P.h-12}
function d2(){const g=L2.svg;clear(g);const c=calc();
 const P=plot(g,{x0:0,x1:60,y0:0,y1:1.1,xt:6,yt:[0,.25,.5,.75,1],xl:'Le / D',yl:'capacity ÷ crush load'});
 const pc=lam=>{const Le=lam*c.D,Pcr=Math.PI**2*5000*Math.sqrt(30)*1e3*c.D**4/12/(Le*Le);return Math.min(1,Pcr/c.Pcrush)};
 curve(g,P,pc,2,60,'s-push',120,{'stroke-width':3.5});
 line(g,P.X(12),P.y,P.X(12),P.y+P.h,'s-muted');T(g,P.X(12)+8,P.y+h_off(P),'Le/D = 12 limit',{'font-size':18});
 const sl=c.Le/c.D;circ(g,P.X(Math.min(sl,60)),P.Y(pc(Math.max(sl,2))),9,'f-ink',{stroke:'var(--halo)','stroke-width':3});
 T(g,P.X(Math.min(sl,60))+14,P.Y(pc(Math.max(sl,2)))+30,'you: '+f1(sl),{'font-size':21,'font-weight':600});
 L2.out.innerHTML='<p>Short columns sit on the flat top and crush. Past a slenderness near 20–30, buckling takes over and capacity drops fast.</p>'}
[sL,sD,en].forEach(e=>{if(e.addEventListener)e.addEventListener('input',d2)});d2();
""")],
 quiz=[dict(q='Both ends of a column are pinned, then you fix one end. Its effective length…', o=['Rises','Falls','Is unchanged'], a=1, w='Fixing an end holds the column straighter. k drops from 1.0 to 0.8, so buckling load rises by about 1.6×.'),
  dict(q='By how much does a column’s Euler load fall if its height doubles?', o=['Half','A quarter','An eighth'], a=1, w='Euler load goes with 1/L².'),
  dict(q='IS 456 treats a column as slender when Le/D is more than…', o=['6','12','20'], a=1, w='Above 12 in either direction you must add moment for slenderness (cl 39.7).')],
 rules=['Effective length is set by how the ends are held. Check the beams really restrain the column.','Buckling load goes with EI / L². Size and height matter most.','A slender column still needs minimum eccentricity: L/500 + D/30, at least 20 mm.','Cantilever columns (free tops) are four times weaker than pinned ones.'],
 codes=['IS 456:2000 cl 25.1 (slenderness)','IS 456 cl 25.4 (min eccentricity)','IS 456 cl 39.7 (slender columns)','IS 456 Table 28']))

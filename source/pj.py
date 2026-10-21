PAGES = []

# ---------------------------------------------------------------- 28
PAGES.append(dict(n=28, slug='quantity-benchmarks', group='Economy and practice',
 title='Quantity benchmarks for towers',
 lede='How much concrete and steel should a tower use per square metre? Benchmarks let you see in seconds whether a design is lean, fat, or hiding a mistake.',
 sections=[
 dict(h='Where does your tower sit?', p='Enter the project totals. The bars show where the quantities fall against typical ranges for towers of that height. Outside the band is a question, not a verdict.', js=r"""
const L=Lab(H,{h:360,label:'Concrete and steel intensity against a typical band',note:'Indicative ranges for above-ground RCC residential towers, built-up area basis. They shift with seismic zone, wall layout and the grade used. Calibrate against your own completed projects before using as a reference.'});
const sB=slider(L.sl,{label:'Built-up area (superstructure)',min:20000,max:200000,step:5000,value:80000,fmt:v=>f0(v)+' m²',on:d});
const sN=slider(L.sl,{label:'Storeys',min:10,max:80,step:1,value:40,fmt:v=>v+'',on:d});
const sC=slider(L.sl,{label:'Concrete quantity',min:5000,max:100000,step:500,value:34000,fmt:v=>f0(v)+' m³',on:d});
const sS=slider(L.sl,{label:'Steel quantity',min:500,max:20000,step:50,value:5200,fmt:v=>f0(v)+' t',on:d});
function band(N){return N<=20?{c:[.33,.42],s:[40,55]}:N<=40?{c:[.36,.46],s:[50,70]}:N<=60?{c:[.40,.52],s:[60,85]}:{c:[.45,.60],s:[75,110]}}
function gauge(g,y,lab,v,lo,hi,max,fm){const x0=70,w=460,X=a=>x0+a/max*w;T(g,x0,y-14,lab,{'font-size':21,'font-weight':600});rect(g,x0,y,w,22,'f-slab');rect(g,X(lo),y,X(hi)-X(lo),22,'f-ok');
 const st=v<lo?1:v>hi?2:0;circ(g,X(Math.min(v,max)),y+11,13,st===0?'f-oks':st===1?'f-warns':'f-pushs',{stroke:'var(--halo)','stroke-width':3});
 T(g,x0,y+52,fm(v)+'   typical '+fm(lo)+' to '+fm(hi),{'font-size':20});return st}
function d(){const g=L.svg;clear(g);const B=sB.v(),N=sN.v(),bd=band(N),c=sC.v()/B,s=sS.v()*1000/B,sd=sS.v()*1000/sC.v();
 const a=gauge(g,60,'Concrete intensity',c,bd.c[0],bd.c[1],.8,v=>f2(v)+' m³/m²'),b=gauge(g,170,'Steel intensity',s,bd.s[0],bd.s[1],130,v=>f0(v)+' kg/m²'),sdn=Math.round(sd);
 T(g,70,290,'Steel per m³ of concrete: '+sdn+' kg/m³  (towers: roughly 110 to 170)',{'font-size':20});
 tiles(L.out,[{l:'Concrete',v:f2(c),u:'m³/m²',c:a===0?'ok':'warn',st:a===0?'In band':a===1?'Lean: check sizes':'Heavy: check thickness'},{l:'Steel',v:f0(s),u:'kg/m²',c:b===0?'ok':'warn',st:b===0?'In band':b===1?'Lean: check design':'Heavy: look for waste'},{l:'Steel per m³',v:sdn,u:'kg/m³',c:sd>=110&&sd<=170?'ok':'warn'}])}
d();
"""),
 dict(h='Break it down by element', p='Slabs carry most of the concrete, but columns and walls carry most of the steel per cubic metre. Move the shares and see the totals and cost.', js=r"""
const L=Lab(H,{h:400,label:'Concrete and steel by structural element',note:'Typical shares per m² of built-up area. Rates illustrative: change them to your own. Steel kg/m³: slabs 85, walls 110, columns 230, beams 160, stairs and misc 100.'});
const sl=slider(L.sl,{label:'Slab thickness equivalent',min:.12,max:.3,step:.01,value:.17,fmt:v=>f2(v)+' m³/m²',on:d});
const sw=slider(L.sl,{label:'Wall concrete',min:.02,max:.2,step:.01,value:.09,fmt:v=>f2(v)+' m³/m²',on:d});
const sc=slider(L.sl,{label:'Column concrete',min:.01,max:.1,step:.01,value:.04,fmt:v=>f2(v)+' m³/m²',on:d});
const sb=slider(L.sl,{label:'Beam concrete',min:0,max:.12,step:.01,value:.05,fmt:v=>f2(v)+' m³/m²',on:d});
const cr=slider(L.sl,{label:'Concrete rate',min:6000,max:14000,step:250,value:9000,fmt:v=>'₹'+f0(v),on:d});
const sr=slider(L.sl,{label:'Steel rate',min:55,max:100,step:1,value:75,fmt:v=>'₹'+v,on:d});
function d(){const g=L.svg;clear(g);const E=[['Slabs',sl.v(),85,'f-conc'],['Walls',sw.v(),110,'f-water'],['Columns',sc.v(),230,'f-warn'],['Beams',sb.v(),160,'f-ok'],['Stairs, misc',.02,100,'f-sand']];
 const tc=E.reduce((a,e)=>a+e[1],0),ts=E.reduce((a,e)=>a+e[1]*e[2],0),cc=tc*cr.v(),cs=ts*sr.v();
 const x0=140,w=400;E.forEach((e,i)=>{const y=40+i*56;T(g,12,y+24,e[0],{'font-size':21});rect(g,x0,y,e[1]/.3*w*.9,22,e[3]);T(g,x0+e[1]/.3*w*.9+8,y+18,f2(e[1])+' m³/m² · '+f1(e[1]*e[2])+' kg',{'font-size':18});
  rect(g,x0,y+26,e[1]*e[2]/40*w*.9*.3,10,'f-steel')});
 T(g,12,356,'thin bar = steel kg/m² for the element',{'font-size':18});
 tiles(L.out,[{l:'Concrete',v:f2(tc),u:'m³/m²'},{l:'Steel',v:f0(ts),u:'kg/m²'},{l:'Cost, concrete + steel',v:f0(cc+cs),u:'₹/m²'},{l:'Steel share of cost',v:f0(cs/(cc+cs)*100),u:'%'}])}
d();
""")],
 quiz=[dict(q='Your tower’s steel intensity is far above the benchmark band. What do you do?', o=['Accept it','Ask why: a high wall count, a transfer, or double-counted bars','Cut the steel'], a=1, w='A benchmark outlier is a prompt to look for the reason. It may be justified, or may be waste.'),
  dict(q='Which element usually has the highest steel per cubic metre?', o=['Slabs','Columns','Walls'], a=1, w='Columns are heavily reinforced in a small volume. Typical 200–300 kg/m³.'),
  dict(q='Benchmarks are most reliable when…', o=['Taken from a book','Built from your own completed projects of the same type','Copied from a competitor'], a=1, w='Layout, grade and seismic zone vary. Local and project-type data beat generic ranges.')],
 rules=['Quote quantities per m² of built-up area and per m³ of concrete. Both tell a story.','Compare like with like: height class, seismic zone, grade and system.','Record every completed project’s quantities. Your own database beats any published range.','Check totals by element: a lean slab and a fat wall can hide behind a normal total.'],
 codes=['IS 456:2000 (member design basis)','IS 1786:2008 (reinforcing bars)','IS 1200 (Part 2) (measurement of concrete)','IS 13920:2016']))

# ---------------------------------------------------------------- 29
PAGES.append(dict(n=29, slug='formwork-construction-sequence', group='Economy and practice',
 title='Formwork and construction sequence',
 lede='The structure you design is only as good as the way it gets built. Formwork pushes against fresh concrete, and early stripping can overload a young slab.',
 sections=[
 dict(h='Fresh concrete is a liquid, for a while', p='Pour fast and it acts like water: the form must resist full liquid pressure. Pour slowly, and the lower concrete stiffens and stops pushing. Move the sliders.', js=r"""
const L=Lab(H,{h:440,label:'Pressure of fresh concrete on a wall form',note:'Simplified: pressure = γ × min(H, R × t), γ = 25 kN/m³, R = pour rate, t = time the concrete stays liquid. Real design uses CIRIA R108 or IS 14687 with temperature, slump and admixtures.'});
const sH=slider(L.sl,{label:'Wall height',min:2,max:8,step:.5,value:4,fmt:v=>f1(v)+' m',on:d});
const sR=slider(L.sl,{label:'Rate of rise',min:.3,max:5,step:.1,value:2,fmt:v=>f1(v)+' m/h',on:d});
const ct=chips(L.sl,[['Hot weather, 2 h',2],['Normal, 3.5 h',3.5],['Cold, 6 h',6]],d,3.5,'Concrete stays workable');
const sT=slider(L.sl,{label:'Tie spacing, each way',min:.5,max:1.5,step:.05,value:.9,fmt:v=>f2(v)+' m',on:d});
const sC=slider(L.sl,{label:'Safe load per tie',min:20,max:100,step:5,value:45,fmt:v=>v+' kN',on:d});
function d(){const g=L.svg;clear(g);const Hh=sH.v(),R=sR.v(),t=ct.get(),sp=sT.v(),cap=sC.v(),h=Math.min(Hh,R*t),p=25*h,full=25*Hh;
 const top=50,bot=400,sc=(bot-top)/8,y0=bot-Hh*sc,fx=200;
 rect(g,fx,y0,60,Hh*sc,'f-conc');rect(g,fx-18,y0,18,Hh*sc,'f-slab');rect(g,fx+60,y0,18,Hh*sc,'f-slab');rect(g,fx-60,bot,200,12,'f-sand');
 const pk=250/Math.max(full,1);
 poly(g,[[fx+78,y0],[fx+78+p*pk,y0+h*sc],[fx+78+p*pk,bot],[fx+78,bot]],{class:'f-push'});
 line(g,fx+78,y0,fx+78+full*pk,bot,'s-muted');T(g,fx+78+full*pk,bot+24,'full liquid '+f0(full),{'text-anchor':'end','font-size':19});
 T(g,fx+78+p*pk+8,bot-16,f0(p)+' kN/m²',{'font-size':22,'font-weight':700});
 for(let i=0;i<Math.floor(Hh/sp);i++){const y=bot-(i+.5)*sp*sc;line(g,fx-18,y,fx+78,y,'s-ink',{'stroke-width':3})}
 const tie=p*sp*sp;
 tiles(L.out,[{l:'Liquid head',v:f1(h),u:'m',s:'of '+f1(Hh)+' m wall'},{l:'Max pressure',v:f0(p),u:'kN/m²',c:p>=full*.95?'bad':p>.6*full?'warn':'ok',st:p>=full*.95?'Full liquid pressure':'Reduced'},{l:'Load on lowest tie',v:f0(tie),u:'kN',c:tie>cap?'bad':tie>.85*cap?'warn':'ok',st:tie>cap?'Over the tie capacity':'Within it',s:'limit '+cap+' kN'}])}
d();
"""),
 dict(h='When can the formwork come off?', p='Concrete gains strength with age and warmth. Choose the member and the weather. See the earliest safe day against the IS 456 minimum times.', js=r"""
const L=Lab(H,{h:420,label:'Strength gain with age and the earliest strip day',note:'f(t)/f28 = t / (4 + 0.85t), age adjusted by maturity (T + 10)/30. Stripping thresholds are assumptions: vertical forms need 5 MPa; soffits 70% (short spans) or 85% of f<sub>ck</sub>. IS 456 cl 11.3 minimum times (at 15 °C or more) shown for reference.'});
const el=chips(L.sl,[['Walls, columns',0],['Slab soffit ≤ 4.5 m',1],['Slab soffit > 4.5 m',2],['Beam soffit ≤ 6 m',3],['Beam soffit > 6 m',4]],d,1,'Member');
const sf=slider(L.sl,{label:'Concrete grade',min:25,max:60,step:5,value:40,fmt:v=>'M'+v,on:d});
const sT=slider(L.sl,{label:'Average temperature',min:10,max:40,step:1,value:28,fmt:v=>v+' °C',on:d});
const IS=[['16–24 h','about 1 day'],['7 d','props left under 3 d'],['14 d',''],['14 d',''],['21 d','']];const ISd=[1,7,14,14,21];
function d(){const g=L.svg;clear(g);const m=el.get(),fck=sf.v(),T0=sT.v(),k=(T0+10)/30;
 const th=[5/fck,.7,.85,.7,.85][m],f=t=>{const te=t*k;return te/(4+.85*te)};
 const tneed=4*th/(1-.85*th)/k;
 const P=plot(g,{x0:0,x1:28,y0:0,y1:1.05,xt:[0,7,14,21,28],yt:[0,.25,.5,.75,1],xl:'age, days',yl:'strength ÷ 28-day'});
 curve(g,P,t=>f(t),0,28,'s-push',100,{'stroke-width':3.5});
 line(g,P.x,P.Y(th),P.x+P.w,P.Y(th),'s-muted');T(g,P.x+P.w-6,P.Y(th)-8,'needed '+Math.round(th*100)+'%',{'text-anchor':'end','font-size':20});
 line(g,P.X(Math.min(tneed,28)),P.y,P.X(Math.min(tneed,28)),P.y+P.h,'s-ok',{'stroke-width':3});circ(g,P.X(Math.min(tneed,28)),P.Y(th),8,'f-ink');
 line(g,P.X(ISd[m]),P.y,P.X(ISd[m]),P.y+P.h,'s-water',{'stroke-dasharray':'7 5','stroke-width':2.5});T(g,P.X(ISd[m])+8,P.y+22,'IS 456 '+IS[m][0],{'font-size':19,style:'fill:var(--water)'});
 const fm=th*fck;
 tiles(L.out,[{l:'Earliest strip',v:tneed<1?f1(tneed*24)+' h':f1(tneed)+' d',s:'for '+f1(fm)+' MPa'},{l:'IS 456 minimum',v:IS[m][0],s:IS[m][1]||''},{l:'Strength at IS day',v:Math.round(f(ISd[m])*100),u:'%',c:f(ISd[m])>=th?'ok':'bad',st:f(ISd[m])>=th?'Enough':'Not enough, wait'}]);
 L.out.insertAdjacentHTML('beforeend','<p>Leave back-props under slabs for several floors during construction: a young slab carries the weight of the floors above through them.</p>')}
d();
""")],
 quiz=[dict(q='Pour a tall wall quickly in cool weather. The form pressure is…', o=['Low, concrete sets fast','Close to full liquid pressure','Zero'], a=1, w='Slow stiffening plus fast rise means the lower concrete stays liquid, so pressure follows the full head.'),
  dict(q='Early striking of slab soffits is dangerous mainly because…', o=['The surface marks','The slab may crack or sag under construction loads','Plastering is difficult'], a=1, w='Early-age concrete has low stiffness and strength. Props must stay as the floors above load it.'),
  dict(q='Hot weather generally makes concrete…', o=['Gain strength faster, so earlier stripping is possible','Gain strength slower','Weaker for ever'], a=0, w='Faster hydration in warmth. But hot weather also risks cracking, so cure carefully.')],
 rules=['Design the formwork for the actual pour rate and temperature, not the textbook one.','Never strip soffit forms or remove props on a calendar day alone: use cube results or maturity.','Construction loads and sequence can be the governing case for slabs and transfer beams.','Keep back-props through at least two or three floors below the one being cast.'],
 codes=['IS 456:2000 cl 11 (formwork)','IS 14687:1999 (formwork guidelines)','IS 14687 / CIRIA R108 (pressure)','IS 456 cl 13 (concreting)']))

# ---------------------------------------------------------------- 30
PAGES.append(dict(n=30, slug='durability', group='Economy and practice',
 title='Durability: cover, exposure and corrosion',
 lede='Steel rusts, and rust swells and splits the concrete. The cover, the mix and the exposure decide how long that takes: decades, if you design it right.',
 sections=[
 dict(h='Pick the exposure, get the requirements', p='IS 456 sets five exposure conditions. Each one demands more cover, a richer and stronger mix, and a tighter water-cement ratio.', js=r"""
const L=Lab(H,{h:420,label:'Beam section showing the cover for the chosen exposure',note:'IS 456:2000 Tables 3, 5 and 16 for reinforced concrete. Cover is nominal cover to the outermost bar (including stirrups). Fire needs may add to it.'});
const T5=[['Mild',20,'M20',.55,300,'Protected indoors'],['Moderate',30,'M25',.5,300,'Exposed to rain, buried in non-aggressive soil'],['Severe',45,'M30',.45,320,'Coastal spray, alternate wet-dry'],['Very severe',50,'M35',.45,340,'Direct sea spray, aggressive soil or sulphate'],['Extreme',75,'M40',.4,360,'Tidal zone, aggressive chemicals']];
const ex=chips(L.sl,T5.map((t,i)=>[t[0],i]),d,1,'Exposure condition');
function d(){const g=L.svg;clear(g);const t=T5[ex.get()],c=t[1],sc=3.2,x0=60,y0=40,w=240,h=300;
 rect(g,x0,y0,w,h,'f-conc');rect(g,x0+c*sc,y0+c*sc,w-2*c*sc,h-2*c*sc,'f-none',{stroke:'var(--ink)','stroke-width':3.5});
 [0,1,2].forEach(i=>circ(g,x0+c*sc+14+(w-2*c*sc-28)*i/2,y0+h-c*sc-14,12,'f-steel'));
 dimV(g,x0+w+30,y0+h-c*sc,y0+h,c+' mm',{anchor:'start',dx:12,fs:24});
 T(g,x0+w+18,y0+40,t[0],{'font-size':26,'font-weight':700});T(g,x0+w+18,y0+70,t[5],{'font-size':18});
 tiles(L.out,[{l:'Nominal cover',v:c,u:'mm'},{l:'Minimum grade',v:t[2]},{l:'Max water-cement ratio',v:f2(t[3])},{l:'Min cement',v:t[4],u:'kg/m³'}])}
d();
"""),
 dict(h='How long until the steel starts to rust?', p='Chloride works its way in by diffusion, slowly. Thicker cover and a tight mix slow it a lot. Test your cover and mix against a 50-year life.', js=r"""
const L=Lab(H,{h:420,label:'Chloride front moving towards the steel',note:'Fick’s second law: initiation time t when chloride at cover depth reaches the corrosion threshold. D falls with age (m = 0.3). D28 from water-cement ratio, scaled by binder. Illustrative, not a design method: use a service-life model for design.'});
const sc=slider(L.sl,{label:'Cover',min:20,max:90,step:5,value:50,fmt:v=>v+' mm',on:d});
const sw=slider(L.sl,{label:'Water-cement ratio',min:.3,max:.65,step:.01,value:.45,fmt:v=>f2(v),on:d});
const bd=chips(L.sl,[['OPC only',1],['30% fly ash',.4],['50% slag',.3]],d,1,'Binder');
const ex=chips(L.sl,[['Coastal air',.35],['Marine spray',.2],['Splash zone',.1]],d,.2,'Exposure (threshold ÷ surface chloride)');
function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+.3275911*x),y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-x*x);return s*y}
function erfinv(y){let a=0,b=4;for(let i=0;i<50;i++){const m=(a+b)/2;if(erf(m)<y)a=m;else b=m}return(a+b)/2}
function tinit(c,wc,bm,r){const D=Math.pow(10,-12.7+2.9*wc)*bm,z=erfinv(1-r),x=c/1000,m=.3,t28=28*86400;const t=Math.pow(x*x/(4*z*z*D*Math.pow(t28,m)),1/(1-m));return t/(365*86400)}
function d(){const g=L.svg;clear(g);const c=sc.v(),wc=sw.v(),bm=bd.get(),r=ex.get(),yrs=tinit(c,wc,bm,r);
 const P=plot(g,{x0:20,x1:90,y0:0,y1:150,xt:7,yt:[0,50,100,150],xl:'cover, mm',yl:'years to corrosion start'});
 curve(g,P,x=>tinit(x,wc,bm,r),20,90,'s-push',70,{'stroke-width':3.5});
 line(g,P.x,P.Y(50),P.x+P.w,P.Y(50),'s-ok',{'stroke-dasharray':'8 5','stroke-width':3});T(g,P.x+8,P.Y(50)-8,'50-year life',{'font-size':20});
 circ(g,P.X(c),P.Y(Math.min(yrs,150)),9,'f-ink',{stroke:'var(--halo)','stroke-width':3});
 tiles(L.out,[{l:'Corrosion starts after',v:yrs>200?'> 200':f0(yrs),u:'years',c:yrs>=50?'ok':yrs>=30?'warn':'bad',st:yrs>=50?'Meets 50 years':yrs>=30?'Short of 50':'Far too short'},{l:'Diffusivity D28',v:(Math.pow(10,-12.7+2.9*wc)*bm*1e12).toFixed(1),u:'×10⁻¹² m²/s'},{l:'Cover needed for 50 yr',v:(()=>{for(let x=20;x<=150;x+=5)if(tinit(x,wc,bm,r)>=50)return x;return '> 150'})(),u:'mm'}])}
d();
""")],
 quiz=[dict(q='Doubling the cover from 25 to 50 mm lengthens the time to corrosion by about…', o=['2×','4×','8×'], a=1, w='Diffusion time goes with the square of the distance. Doubling cover gives about four times the life.'),
  dict(q='The simplest way to slow chloride ingress?', o=['A lower water-cement ratio and SCMs like fly ash or slag','A thicker plaster','Painting the steel'], a=0, w='A denser paste slows diffusion. Fly ash and slag blends cut diffusivity a lot.'),
  dict(q='A basement slab in aggressive groundwater is usually at what exposure?', o=['Mild','Severe or very severe','None'], a=1, w='Classify by the worse of the soil and water conditions. Sulphates need sulphate-resisting cement or SCMs too.')],
 rules=['Pick the exposure from the site, not the drawing. Basements, balconies, and coastal sites are not “mild”.','Cover blocks and checking at site matter as much as the nominal cover on the drawing.','Crack widths: keep to 0.3 mm (0.2 mm for severe, very severe and extreme exposure) for steel protection.','Durability is part of the design life. State the cover, grade, w/c ratio and cement in the drawing notes.'],
 codes=['IS 456:2000 cl 8, Table 3 (exposure)','IS 456 Table 5 (mix limits)','IS 456 cl 26.4 (cover), Table 16','IS 456 cl 35.3.2 (crack width)']))

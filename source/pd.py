PAGES = []

# ---------------------------------------------------------------- 10
PAGES.append(dict(n=10, slug='ductile-detailing', group='RCC design',
 title='Ductile detailing: why seismic detailing matters',
 lede='In an earthquake we cannot afford strength for the full shaking. We buy ductility instead: the ability to bend a long way without breaking.',
 sections=[
 dict(h='Tight hoops let a column keep its strength', p='Close hoops confine the concrete core. Widen the spacing and watch the hysteresis loop collapse after a big drift.', js=r"""
const L=Lab(H,{h:440,label:'Force against drift loops for a column',note:'Illustrative model, not a code formula. Yield at 1% drift. Drift capacity grows with confinement: hoop spacing against the IS 13920:2016 limit, and hook type.'});
const ss=slider(L.sl,{label:'Hoop spacing',min:50,max:300,step:10,value:100,fmt:v=>v+' mm',on:d});
const sD=slider(L.sl,{label:'Smallest column size D',min:300,max:1000,step:50,value:500,fmt:v=>v+' mm',on:d});
const sb=slider(L.sl,{label:'Main bar diameter',min:16,max:32,step:2,value:25,fmt:v=>v+' mm',on:d});
const sdm=slider(L.sl,{label:'Drift demand',min:1,max:6,step:.25,value:3,fmt:v=>f2(v)+'%',on:d});
const hk=chips(L.sl,[['135° hooks',1],['90° hooks',.6]],d,1,'Hook type');
function d(){const g=L.svg;clear(g);const s=ss.v(),D=sD.v(),db=sb.v(),dem=sdm.v(),h=hk.get();
 const lim=Math.max(75,Math.min(100,Math.min(D/4,6*db)));
 const conf=Math.max(.12,Math.min(1,1-(s-lim)/(2.5*lim)))*h,du=1.5+4.5*conf;
 const E=a=>{a=Math.abs(a);return a<=1?a:a<=du?1+.04*(a-1):Math.max(.2,1+.04*(du-1)-(a-du)*.55)};
 const P=plot(g,{x0:-7,x1:7,y0:-1.6,y1:1.6,xt:[-6,-4,-2,0,2,4,6],yt:[-1,0,1],xl:'drift, %',yl:'force ÷ yield'});
 line(g,P.X(0),P.y,P.X(0),P.y+P.h,'s-muted');line(g,P.x,P.Y(0),P.x+P.w,P.Y(0),'s-muted');
 let En=0;const amps=[];for(let a=1;a<=dem+1e-9;a+=1)amps.push(a);if(amps[amps.length-1]<dem-.01)amps.push(dem);
 amps.forEach((a,i)=>{const F=E(a),A=[a,F],B=[a-2*F,-F],C=[-a,-F],Dd=[-a+2*F,F];
  poly(g,[A,B,C,Dd].map(q=>[P.X(q[0]),P.Y(q[1])]),{class:'f-push',opacity:.25+.5*(i+1)/amps.length});
  En+=Math.abs((A[0]*B[1]-B[0]*A[1])+(B[0]*C[1]-C[0]*B[1])+(C[0]*Dd[1]-Dd[0]*C[1])+(Dd[0]*A[1]-A[0]*Dd[1]))/2});
 const env=[];for(let x=-7;x<=7.001;x+=.1)env.push([P.X(x),P.Y(Math.sign(x)*E(x))]);pline(g,env,'s-thick');
 if(dem>du){line(g,P.X(du),P.y,P.X(du),P.y+P.h,'s-push',{'stroke-dasharray':'6 5'});T(g,P.X(du)+8,P.y+26,'strength falls',{'font-size':19})}
 tiles(L.out,[{l:'Code spacing limit',v:f0(lim),u:'mm',c:s<=lim?'ok':'bad',st:s<=lim?'You meet it':'Too wide',s:'min(D/4, 6 db, 100), not under 75'},{l:'Drift capacity',v:f1(du),u:'%'},{l:'Ductility',v:f1(du),u:'×',s:'drift capacity ÷ yield drift'},{l:'Survives demand?',v:dem<=du?'Yes':'No',c:dem<=du?'ok':'bad',st:dem<=du?'Keeps its strength':'Collapses at this drift'}])}
d();
"""),
 dict(h='Strong column, weak beam', p='We want hinges in the beams, which can spread damage across every floor, not in the columns of one floor, which makes the building fold. IS 13920 asks the columns to be stronger by a margin.', js=r"""
const L=Lab(H,{h:440,label:'Frame with hinges forming in beams or in columns',note:'IS 13920:2016 cl 7.2.1 asks ΣM<sub>c</sub> ≥ 1.4 ΣM<sub>b</sub> at every joint (design moment capacities). Below that, one storey can become a soft-storey mechanism.'});
const sc=slider(L.sl,{label:'Column capacity ΣMc',min:500,max:5000,step:100,value:2600,fmt:v=>f0(v)+' kNm',on:d});
const sb=slider(L.sl,{label:'Beam capacity ΣMb',min:500,max:4000,step:100,value:1800,fmt:v=>f0(v)+' kNm',on:d});
function d(){const g=L.svg;clear(g);const r=sc.v()/sb.v(),good=r>=1.4;
 const ys=[380,290,200,110],xs=[110,290,470],off=good?[0,8,16,24]:[0,8,70,78];
 rect(g,70,380,460,14,'f-conc');
 for(let i=0;i<3;i++)xs.forEach(x=>line(g,x+off[i],ys[i],x+off[i+1],ys[i+1],'s-beam',{'stroke-width':10}));
 for(let i=1;i<4;i++){line(g,xs[0]+off[i],ys[i],xs[2]+off[i],ys[i],'s-beam',{'stroke-width':8})}
 if(good){for(let i=1;i<4;i++)xs.forEach((x,j)=>{if(j<2){circ(g,x+off[i]+16,ys[i],8,'f-oks',{stroke:'var(--halo)','stroke-width':2});circ(g,xs[j+1]+off[i]-16,ys[i],8,'f-oks',{stroke:'var(--halo)','stroke-width':2})}})}
 else{xs.forEach(x=>{circ(g,x+off[1]+3,ys[1]-4,9,'f-pushs',{stroke:'var(--halo)','stroke-width':2});circ(g,x+off[2]-3,ys[2]+4,9,'f-pushs',{stroke:'var(--halo)','stroke-width':2})})}
 T(g,590,56,good?'hinges in beams':'hinges in one storey',{'font-size':21,'font-weight':600,'text-anchor':'end'});
 tiles(L.out,[{l:'ΣMc / ΣMb',v:f2(r),c:good?'ok':r>=1?'warn':'bad',st:good?'Meets 1.4: beams yield first':r>=1?'Weak margin':'Weak column','s':'IS 13920:2016 asks for at least 1.4'},{l:'Mechanism',v:good?'Beam sway':'Storey',c:good?'ok':'bad',st:good?'Damage spread over many floors':'One floor folds, building collapses'}])}
d();
""")],
 quiz=[dict(q='Closer hoops near column ends mainly…', o=['Raise axial strength','Confine the core and raise ductility','Reduce shrinkage'], a=1, w='They hold the core together and stop main bars buckling, so the column keeps carrying load after the cover spalls.'),
  dict(q='Why 135° hook ends on stirrups?', o=['They look neat','90° hooks open when cover spalls','Easier to fix'], a=1, w='A 90° hook opens in the core once cover falls away. A 135° hook stays anchored in the core.'),
  dict(q='If columns are weaker than beams at a joint, damage concentrates in…', o=['All beams equally','One storey of columns','The slab'], a=1, w='A storey mechanism forms, and that storey bears all the drift.')],
 rules=['Ductility is what lets us design for less than the elastic earthquake force. Detail it or do not rely on it.','Hoops: close spacing over the end regions (typically the larger of D, H/6, 450 mm), 135° hooks.','Beams yield first. Keep the column capacity above 1.4 × the beam capacity at every joint.','Keep lap splices out of the yielding zones.'],
 codes=['IS 13920:2016','IS 13920 cl 7 (columns), cl 6 (beams)','IS 1893 (Part 1):2016 R factors','IS 456:2000 cl 26.2 (anchorage)']))

# ---------------------------------------------------------------- 11
PAGES.append(dict(n=11, slug='earthquake-loads', group='Loads',
 title='Earthquake loads: spectrum, zones and R factor',
 lede='An earthquake does not push a building. It shakes the ground, and the building’s own mass resists. Heavier and stiffer attracts more force.',
 sections=[
 dict(h='From the ground to a base shear', p='Pick the zone, soil and system. The response spectrum gives how hard a building of period T is shaken. The result is the base shear: <b>V<sub>B</sub> = A<sub>h</sub> × W</b>.', js=r"""
const L=Lab(H,{h:470,label:'IS 1893 response spectrum with building period marker',note:'IS 1893 (Part 1):2016, 5% damping. A<sub>h</sub> = (Z/2)(I/R)(S<sub>a</sub>/g). Empirical period T<sub>a</sub> = 0.075h<sup>0.75</sup> (bare RC frame) or 0.09h/√d (walls, infill).'});
const zc=chips(L.sl,[['II 0.10',.10],['III 0.16',.16],['IV 0.24',.24],['V 0.36',.36]],d,.16,'Zone factor Z (Mumbai: Zone III)');
const sc=chips(L.sl,[['Type I rock',1],['II medium',2],['III soft',3]],d,2,'Soil');
const rc=chips(L.sl,[['R 3 ordinary',3],['R 4 ductile wall',4],['R 5 SMRF',5]],d,4,'System');
const ic=chips(L.sl,[['I 1.0',1],['I 1.2',1.2],['I 1.5',1.5]],d,1.2,'Importance');
const sys=chips(L.sl,[['Bare RC frame',0],['Walls / infill',1]],d,1,'For empirical period');
const sH=slider(L.sl,{label:'Building height h',min:10,max:300,step:5,value:150,fmt:v=>v+' m',on:d});
const sdd=slider(L.sl,{label:'Base dimension d',min:15,max:60,step:1,value:35,fmt:v=>v+' m',on:d});
const sT=slider(L.sl,{label:'Period T (from your model)',min:.1,max:8,step:.05,value:4,fmt:v=>f2(v)+' s',on:d});
const sW=slider(L.sl,{label:'Seismic weight W',min:20,max:1000,step:10,value:400,fmt:v=>v+' MN',on:d});
button(L.sl,'Use empirical Ta',()=>{sT.set(clamp(ta(),.1,8))});
function ta(){const h=sH.v(),dd=sdd.v();return sys.get()?0.09*h/Math.sqrt(dd):0.075*Math.pow(h,.75)}
function sag(T,s){if(T<.1)return 1+15*T;const k=s===1?[.4,1,4]:s===2?[.55,1.36,5.44]:[.67,1.67,6.68];return T<=k[0]?2.5:T<=4?k[1]/T:k[2]/(T*T)}
function d(){const g=L.svg;clear(g);const Z=zc.get(),s=sc.get(),R=rc.get(),I=ic.get(),Tm=sT.v(),W=sW.v();
 const P=plot(g,{x0:0,x1:6,y0:0,y1:3,xt:6,yt:[0,.5,1,1.5,2,2.5,3],xl:'period T, s',yl:'Sa / g'});
 curve(g,P,t=>sag(Math.max(t,.001),s),0,6,'s-push',200,{'stroke-width':3.5});
 const sa=sag(Tm,s),Ah=Z/2*I/R*sa,tt=ta();
 line(g,P.X(Tm),P.Y(0),P.X(Tm),P.Y(sa),'s-ink',{'stroke-dasharray':'6 4'});circ(g,P.X(Tm),P.Y(sa),9,'f-ink',{stroke:'var(--halo)','stroke-width':3});
 line(g,P.X(clamp(tt,0,6)),P.y+P.h,P.X(clamp(tt,0,6)),P.y+P.h-16,'s-ok',{'stroke-width':4});T(g,P.X(clamp(tt,0,6)),P.y+P.h-22,'Ta '+f2(tt),{'font-size':18,'text-anchor':'middle'});
 tiles(L.out,[{l:'Empirical Ta',v:f2(tt),u:'s'},{l:'Sa / g at your T',v:f2(sa)},{l:'Design Ah',v:f3(Ah),s:'Z/2 × I/R × Sa/g'},{l:'Base shear VB',v:f1(Ah*W),u:'MN',s:'= Ah × W'},{l:'VB / W',v:f2(Ah*100),u:'%'}]);
 window.__VB=Ah*W;if(window.__after)window.__after()}
d();
// floor forces
const L2=Lab(H,{h:430,label:'Base shear shared among floors',note:'Equal floor weights. Q<sub>i</sub> = V<sub>B</sub> × W<sub>i</sub>h<sub>i</sub>² / ΣW<sub>j</sub>h<sub>j</sub>² (IS 1893 cl 7.6.3). Heavier, higher floors take the most.'});
const sN=slider(L2.sl,{label:'Number of storeys',min:4,max:60,step:1,value:30,fmt:v=>v+' floors',on:()=>d2()});
function d2(){const g=L2.svg,N=sN.v(),VB=(window.__VB||100)*1000,h=3.2;clear(g);
 let sum=0;for(let i=1;i<=N;i++)sum+=(i*h)**2;const Q=[];for(let i=1;i<=N;i++)Q.push(VB*(i*h)**2/sum);
 const top=40,bot=390,dy=(bot-top)/N;rect(g,150,top,150,bot-top,'f-slab');
 for(let i=1;i<=N;i++){const y=bot-i*dy;line(g,150,y,300,y,'s-grid')}
 for(let i=1;i<=N;i++){const y=bot-i*dy,len=10+Q[i-1]/Q[N-1]*110;arrow(g,150-len,y+dy/2,148,y+dy/2,'s-push','ah',{'stroke-width':Math.max(1.2,Math.min(4,dy*.5))})}
 let cum=0;const V=[];for(let i=N;i>=1;i--){cum+=Q[i-1];V.push([i,cum])}
 const q=[[350,bot]];V.reverse().forEach(v=>{const y=bot-(v[0]-1)*dy,y2=bot-v[0]*dy;q.push([350+v[1]/VB*230,y]);q.push([350+v[1]/VB*230,y2])});q.push([350,top]);
 poly(g,q,{class:'f-water'});T(g,350,top-8,'storey shear',{'font-size':20});T(g,350+230,bot+30,'VB',{'font-size':20,'text-anchor':'end'});
 let M=0;for(let i=1;i<=N;i++)M+=Q[i-1]*i*h;
 tiles(L2.out,[{l:'Top floor force',v:f0(Q[N-1]),u:'kN'},{l:'Ground floor force',v:f0(Q[0]),u:'kN'},{l:'Overturning moment',v:f0(M/1000),u:'MNm'}])}
window.__after=d2;d2();
""")],
 quiz=[dict(q='Mumbai sits in which IS 1893:2016 seismic zone, and what is Z?', o=['Zone II, 0.10','Zone III, 0.16','Zone IV, 0.24'], a=1, w='Greater Mumbai is Zone III, Z = 0.16. Zone factors: II 0.10, III 0.16, IV 0.24, V 0.36.'),
  dict(q='A higher R factor means…', o=['Higher design force, less ductility needed','Lower design force, more ductility needed','No change in force'], a=1, w='R divides the elastic force. A high R only works if the detailing delivers the ductility.'),
  dict(q='Which floor takes the largest share of the base shear in a uniform building?', o=['Ground','Middle','Top'], a=2, w='Force goes with weight × height². The top floor is highest, so it takes the most.')],
 rules=['VB = Ah × W. Seismic weight W includes dead load plus a share of live load (25% under 3 kN/m², 50% above; IS 1893 Table 10).','Periods from the model must make sense against the empirical Ta. If they are very different, find out why.','Dynamic analysis base shear must be scaled up to at least the static base shear (cl 7.7.3).','Mass participation of at least 90% in each direction.'],
 codes=['IS 1893 (Part 1):2016','IS 1893 Table 2 (Z), Table 9 (R), Table 8 (I)','IS 1893 cl 7.6.2 (Ta)','IS 16700:2023']))

# ---------------------------------------------------------------- 12
PAGES.append(dict(n=12, slug='wind-loads', group='Loads',
 title='Wind loads on tall buildings',
 lede='Wind speeds up with height, and pressure goes with speed squared. Tall buildings catch far more than short ones, and they also sway across the wind.',
 sections=[
 dict(h='Height makes the wind stronger', p='Pick a wind zone and terrain. Pressure climbs with height. Open terrain gives more wind than a city.', js=r"""
const L=Lab(H,{h:460,label:'Wind pressure growing with building height',note:'IS 875 (Part 3):2015: V<sub>z</sub> = V<sub>b</sub>k<sub>1</sub>k<sub>2</sub>k<sub>3</sub>k<sub>4</sub>, p<sub>z</sub> = 0.6 V<sub>z</sub>². Simplified power-law profile for k<sub>2</sub> (IS 875 Table 2 lists exact values). k<sub>1</sub> = k<sub>3</sub> = k<sub>4</sub> = 1.'});
const vb=chips(L.sl,[['39',39],['44 Mumbai',44],['47',47],['50',50],['55',55]],d,44,'Basic wind speed Vb, m/s');
const tc=chips(L.sl,[['TC1 open sea',0],['TC2 open',1],['TC3 suburban',2],['TC4 city',3]],d,2,'Terrain category');
const sH=slider(L.sl,{label:'Building height',min:30,max:300,step:10,value:150,fmt:v=>v+' m',on:d});
const sB=slider(L.sl,{label:'Width facing the wind',min:20,max:80,step:2,value:40,fmt:v=>v+' m',on:d});
const sC=slider(L.sl,{label:'Force coefficient Cf',min:1,max:1.6,step:.05,value:1.3,fmt:v=>f2(v),on:d});
const K10=[1.05,1,.91,.8],AL=[.10,.15,.22,.30],ZG=[250,300,400,500];
function Vz(z,t,Vb){const zz=Math.min(Math.max(z,10),ZG[t]);return Vb*K10[t]*Math.pow(zz/10,AL[t])}
function d(){const g=L.svg;clear(g);const Vb=vb.get(),t=tc.get(),Hh=sH.v(),B=sB.v(),Cf=sC.v();
 const bot=410,top=40,sc=(bot-top)/300,bx=420,bw=B*2.2;
 rect(g,bx,bot-Hh*sc,bw,Hh*sc,'f-conc');rect(g,40,bot,560,12,'f-sand');
 const pz=z=>.6*Vz(z,t,Vb)**2/1000,pmax=Math.max(pz(Hh),.1),q=[];
 for(let i=0;i<=30;i++){const z=Hh*i/30,y=bot-z*sc;q.push([bx-20-pz(z)/pmax*240,y])}
 poly(g,[[bx-20,bot]].concat(q).concat([[bx-20,bot-Hh*sc]]),{class:'f-push'});
 for(let i=0;i<=8;i++){const z=Hh*i/8,y=bot-z*sc,len=pz(z)/pmax*240;if(len>14)arrow(g,bx-20-len,y,bx-4,y,'s-push','ah',{'stroke-width':2})}
 T(g,bx-20-pz(Hh)/pmax*240-6,bot-Hh*sc+6,f2(pz(Hh))+' kN/m²',{'text-anchor':'end','font-size':20,'font-weight':600});
 T(g,bx-24,bot-8,f2(pz(10))+' kN/m²',{'text-anchor':'end','font-size':20});
 let F=0,M=0;const n=60;for(let i=0;i<n;i++){const z=Hh*(i+.5)/n,f=Cf*pz(z)*B*Hh/n;F+=f;M+=f*z}
 window.__VZ=Vz(Hh,t,Vb);window.__B=B;window.__H=Hh;if(window.__after)window.__after();
 tiles(L.out,[{l:'Speed at top',v:f1(Vz(Hh,t,Vb)),u:'m/s'},{l:'Pressure at top',v:f2(pz(Hh)),u:'kN/m²',s:'pz = 0.6 Vz²'},{l:'Top ÷ ground pressure',v:f1(pz(Hh)/pz(10)),u:'×'},{l:'Base shear',v:f1(F/1000),u:'MN'},{l:'Base moment',v:f0(M/1000),u:'MNm'}])}
d();
// vortex shedding
const L2=Lab(H,{h:360,label:'Wind shedding vortices past a tall building',note:'Across-wind resonance: when vortices shed at the building’s own frequency, it sways sideways. V<sub>cr</sub> = f B / St. IS 875 (Part 3) asks for dynamic checks if h/B > 5 or the first frequency is below 1 Hz.'});
const sT=slider(L2.sl,{label:'Building period T (first mode)',min:2,max:12,step:.25,value:6,fmt:v=>f2(v)+' s',on:()=>d2()});
const st=chips(L2.sl,[['Square 0.12',.12],['Rectangle 0.1',.1],['Round 0.2',.2]],()=>d2(),.12,'Shape (Strouhal number)');
let tm=0;const lp=loop(L2.svg,t=>{tm=t;d2(true)});
function d2(an){const g=L2.svg;clear(g);const T0=sT.v(),St=st.get(),B=window.__B||40,Hh=window.__H||150,Vz=window.__VZ||50,f=1/T0,Vcr=f*B/St;
 const bx=250,by=320,hh=230,bw=Math.max(30,B*1.6),sway=Math.sin(tm*2*Math.PI*Math.min(f,.5)*1.2)*14*(Vcr<Vz?1.4:.4);
 rect(g,40,by,540,12,'f-sand');
 for(let i=0;i<5;i++)arrow(g,40,70+i*55,bx-10,70+i*55,'s-water','ahw',{'stroke-width':2.5,opacity:.6});
 pline(g,[[bx-bw/2,by],[bx-bw/2+sway,by-hh],[bx+bw/2+sway,by-hh],[bx+bw/2,by]],'s-ink',{'stroke-width':3,fill:'var(--panel)'});
 poly(g,[[bx-bw/2,by],[bx-bw/2+sway,by-hh],[bx+bw/2+sway,by-hh],[bx+bw/2,by]],{class:'f-conc'});
 for(let i=0;i<8;i++){const ph=(tm*f*6+i*.5)%4,x=bx+bw/2+30+ph*120,up=i%2?1:-1,y=by-hh*.6+up*38*(1-Math.abs(x-bx-200)/400);if(x>bx+bw/2+20&&x<590)circ(g,x,y,13,'f-water',{opacity:Math.max(.2,1-ph/4)})}
 if(!an)tiles(L2.out,[{l:'Shedding resonance speed',v:f1(Vcr),u:'m/s',s:'= f × B / St'},{l:'Design speed at top',v:f1(Vz),u:'m/s'},{l:'Slenderness h / B',v:f1(Hh/B),c:Hh/B>5?'bad':'ok',st:Hh/B>5?'Wind-sensitive':'OK'},{l:'Resonance risk',v:Vcr<Vz?'Yes':'Low',c:Vcr<Vz?'bad':'ok',st:Vcr<Vz?'Sways across the wind. Consider a wind tunnel.':'Resonance above design speed'}])}
window.__after=()=>d2();d2();
""")],
 quiz=[dict(q='Wind speed doubles. Pressure goes up by…', o=['2×','4×','8×'], a=1, w='p = 0.6 V². Double the speed, four times the pressure.'),
  dict(q='Which terrain gives the strongest wind at a given height?', o=['City centre','Open flat country or sea','Suburbs'], a=1, w='Rough terrain slows the wind near the ground. Open terrain lets it run free.'),
  dict(q='When is a wind tunnel test usually asked for?', o=['Any building above 10 m','Tall, slender or unusual-shape buildings','Only coastal buildings'], a=1, w='Tall (above about 120 m), slender (h/B > 5) or irregular towers need real flow data, including across-wind and torsion.')],
 rules=['Pressure goes with V². A 10% wind speed change is a 21% pressure change.','Across-wind response and torsion often govern tall towers, not along-wind.','Comfort (acceleration) can govern even when strength is fine.','Wind tunnel forces replace code forces. Check the load combination and scaling carefully.'],
 codes=['IS 875 (Part 3):2015','IS 875 Table 2 (k₂), Fig. 1 (wind map)','IS 16700:2023 (tall buildings)','IS 456 cl 18.2']))

PAGES = []

# ---------------------------------------------------------------- 16
PAGES.append(dict(n=16, slug='modal-analysis', group='Tall buildings',
 title='Modal analysis: periods, mode shapes, participation',
 lede='A building does not sway one way. It has a family of natural shapes, each with its own period. The analysis finds them, and tells you which ones matter.',
 sections=[
 dict(h='Meet the modes', p='Pick a mode and watch the building move in that shape. Tall buildings need many modes before most of their mass is moving. Change the floors and stiffness pattern.', js=r"""
const L=Lab(H,{h:470,label:'Mode shapes of a multi-storey shear building, animated',note:'Shear building: lumped storey masses and storey stiffnesses, solved numerically (Jacobi eigenvalue method). Shapes normalised to the roof. IS 1893 asks for modes covering at least 90% of the mass in each direction.'});
const sN=slider(L.sl,{label:'Number of storeys',min:3,max:20,step:1,value:12,fmt:v=>v+'',on:d});
const sT=slider(L.sl,{label:'First-mode period T1',min:.5,max:9,step:.1,value:5,fmt:v=>f1(v)+' s',on:d});
const tp=chips(L.sl,[['Uniform stiffness',0],['Stiffer below',1],['Soft ground storey',2]],d,0,'Stiffness pattern');
const md=chips(L.sl,[['Mode 1',0],['Mode 2',1],['Mode 3',2]],d,0,'Show');
function jacobi(A){const n=A.length,V=[];for(let i=0;i<n;i++){V.push(new Array(n).fill(0));V[i][i]=1}
 for(let sw=0;sw<80;sw++){let off=0;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)off+=A[i][j]*A[i][j];if(off<1e-20)break;
  for(let p=0;p<n-1;p++)for(let q=p+1;q<n;q++){if(Math.abs(A[p][q])<1e-14)continue;const th=(A[q][q]-A[p][p])/(2*A[p][q]),t=(th>=0?1:-1)/(Math.abs(th)+Math.sqrt(th*th+1)),c=1/Math.sqrt(t*t+1),s=t*c;
   for(let k=0;k<n;k++){const a=A[k][p],b=A[k][q];A[k][p]=c*a-s*b;A[k][q]=s*a+c*b}
   for(let k=0;k<n;k++){const a=A[p][k],b=A[q][k];A[p][k]=c*a-s*b;A[q][k]=s*a+c*b}
   for(let k=0;k<n;k++){const a=V[k][p],b=V[k][q];V[k][p]=c*a-s*b;V[k][q]=s*a+c*b}}}
 return {vals:A.map((r,i)=>r[i]),vecs:V}}
let R=null;
function solve(){const N=sN.v(),t=tp.get(),k=[];for(let i=1;i<=N;i++)k.push(t===0?1:t===1?1+2*(N-i)/N:(i===1?.35:1));
 const A=[];for(let i=0;i<N;i++){A.push(new Array(N).fill(0));A[i][i]=k[i]+(i<N-1?k[i+1]:0);if(i<N-1){A[i][i+1]=-k[i+1]}}
 for(let i=0;i<N-1;i++)A[i+1][i]=A[i][i+1];
 const e=jacobi(A),idx=e.vals.map((v,i)=>i).sort((a,b)=>e.vals[a]-e.vals[b]);
 const T1u=2*Math.PI/Math.sqrt(e.vals[idx[0]]),sc=sT.v()/T1u,modes=[];let cum=0;
 idx.forEach((ix,m)=>{const ph=e.vecs.map(r=>r[ix]);const sg=ph[N-1]<0?-1:1;const p2=ph.map(x=>x*sg),sm=p2.reduce((a,b)=>a+b,0),ss=p2.reduce((a,b)=>a+b*b,0);
  const eff=sm*sm/ss/N;cum+=eff;modes.push({T:sc*2*Math.PI/Math.sqrt(e.vals[ix]),phi:p2.map(x=>x/p2[N-1]),eff:eff,cum:cum})});return {N:N,modes:modes}}
let tm=0;
function d(){R=solve();draw();info()}
function info(){const m=R.modes,n90=m.findIndex(x=>x.cum>=.9)+1;
 bars(L.out,m.slice(0,6).map((x,i)=>({l:'Mode '+(i+1)+' · '+f2(x.T)+' s',v:x.cum*100,max:100,t:Math.round(x.cum*100)+'%',c:x.cum>=.9?'ok':'water',on:i===md.get()})));
 L.out.insertAdjacentHTML('beforeend','<div class="metrics" style="margin-top:1rem"><div class="m '+(n90<=6?'ok':'warn')+'"><div class="lbl">Modes for 90% mass</div><div class="val">'+(n90||'> '+m.length)+'</div></div><div class="m"><div class="lbl">T2 ÷ T1</div><div class="val">'+f2(m[1].T/m[0].T)+'</div></div><div class="m"><div class="lbl">T3 ÷ T1</div><div class="val">'+f2(m[2].T/m[0].T)+'</div></div></div>')}
function draw(){const g=L.svg;clear(g);if(!R)return;const N=R.N,mo=R.modes[md.get()],bx=230,by=420,ht=350,w=70,dy=ht/N;
 const om=2*Math.PI*.35*(R.modes[md.get()].T>0?R.modes[0].T/mo.T:1),s=Math.sin(tm*om)*80;
 rect(g,bx-80,by,160,12,'f-conc');
 line(g,bx,by,bx,by-ht,'s-muted');
 const pts=[[bx,by]];for(let i=0;i<N;i++)pts.push([bx+mo.phi[i]*s,by-(i+1)*dy]);pline(g,pts,'s-thick',{'stroke-width':14,stroke:'var(--conc2)'});pline(g,pts,'s-push',{'stroke-width':3});
 for(let i=0;i<N;i++){const p=pts[i+1];line(g,p[0]-w/2,p[1],p[0]+w/2,p[1],'s-ink',{'stroke-width':5})}
 T(g,bx+160,60,'Mode '+(md.get()+1),{'font-size':26,'font-weight':700});T(g,bx+160,92,'T = '+f2(mo.T)+' s',{'font-size':22});T(g,bx+160,122,Math.round(mo.eff*100)+'% of mass',{'font-size':22})}
loop(L.svg,t=>{tm=t;draw()});
d();
""")],
 quiz=[dict(q='Mode 1 of a tall building typically moves…', o=['Every floor the same way, most at the top','Top and bottom in opposite directions','Only the bottom half'], a=0, w='Mode 1 is the fundamental sway. All floors move the same way, increasing with height.'),
  dict(q='IS 1893 asks you to include enough modes to capture at least…', o=['75% of the mass','90% of the mass','100% of the mass'], a=1, w='At least 90% in each direction. Tall buildings often need 15–30 modes.'),
  dict(q='Your model’s T1 is half of the empirical Ta. What does that tell you?', o=['The building is great','The model may be too stiff or missing mass','Nothing'], a=1, w='A model much stiffer than reality, from wrong modifiers, rigid zones or missing mass, will under-predict period and forces.')],
 rules=['Compare T1 from the model with the empirical Ta. A big gap needs an explanation.','The first three modes should be two translations and one torsion. A torsional first mode is a warning.','Mass participation of at least 90% in both directions; add modes until reached.','Modal combination (CQC) is used when modes are close together; SRSS only if well separated.'],
 codes=['IS 1893 (Part 1):2016 cl 7.7 (response spectrum)','IS 1893 cl 7.7.5.2 (90% mass)','IS 16700:2023','IS 1893 cl 7.6 (period)']))

# ---------------------------------------------------------------- 17
PAGES.append(dict(n=17, slug='p-delta', group='Tall buildings',
 title='P-Delta: when weight makes the lean worse',
 lede='A leaning building has weight above that pulls it further over. The more it leans, the bigger the pull. This second-order effect grows quickly in tall, flexible buildings.',
 sections=[
 dict(h='Lean it and watch the weight help', p='A cantilever column under a sideways force and a weight at the top. Raise the weight towards its buckling load and the lean runs away.', js=r"""
const L=Lab(H,{h:470,label:'Cantilever column with P-Delta',note:'Second-order tip drift δ = δ₁ / (1 − P / Pcr), with δ₁ = HL³/3EI and Pcr = π²EI / 4L². Extra moment = P × δ. Drawing exaggerated.'});
const sL=slider(L.sl,{label:'Height L',min:3,max:30,step:.5,value:12,fmt:v=>f1(v)+' m',on:d});
const sE=slider(L.sl,{label:'Stiffness EI',min:50,max:5000,step:50,value:600,fmt:v=>f0(v)+' MNm²',on:d});
const sH=slider(L.sl,{label:'Sideways force H',min:10,max:500,step:10,value:100,fmt:v=>v+' kN',on:d});
const sP=slider(L.sl,{label:'Weight as % of Pcr',min:0,max:95,step:1,value:50,fmt:v=>v+'%',on:d});
function d(){const g=L.svg,Lm=sL.v(),EI=sE.v()*1000,Hh=sH.v(),pr=sP.v()/100;clear(g);
 const Pcr=Math.PI**2*EI/(4*Lm*Lm),P=pr*Pcr,d1=Hh*Lm**3/(3*EI),d2=d1/(1-pr),Mo=Hh*Lm,M2=Mo+P*d2;
 const bx=250,by=410,ht=330,sc=Math.min(150/d2,300);rect(g,bx-70,by,140,12,'f-conc');
 const f=(z,dl)=>dl*(3*z*z-z*z*z)/2;
 const a=[],b=[];for(let i=0;i<=40;i++){const z=i/40;a.push([bx+f(z,d1)*sc,by-z*ht]);b.push([bx+f(z,d2)*sc,by-z*ht])}
 pline(g,[[bx,by],[bx,by-ht]],'s-muted');pline(g,a,'s-muted',{'stroke-width':3});pline(g,b,'s-thick',{'stroke-width':12,stroke:'var(--conc2)'});pline(g,b,'s-push',{'stroke-width':3});
 const tx=b[40][0];arrow(g,tx-90,by-ht-14,tx-6,by-ht-14,'s-ink','ahk',{'stroke-width':4});arrow(g,tx+16,by-ht-80,tx+16,by-ht-20,'s-push','ah',{'stroke-width':4+pr*6});
 T(g,tx+30,by-ht-44,f0(P)+' kN',{'font-size':21,'font-weight':600});
 T(g,tx+14,by-ht+34,'δ '+f0(d2*1000)+' mm',{'font-size':21,'font-weight':600});
 const th=P*d2/(Hh*Lm);
 tiles(L.out,[{l:'Buckling load Pcr',v:f0(Pcr),u:'kN'},{l:'First-order drift',v:f0(d1*1000),u:'mm'},{l:'With P-Delta',v:f0(d2*1000),u:'mm',c:d2/d1>1.2?'bad':d2/d1>1.1?'warn':'ok',st:'× '+f2(d2/d1)},{l:'Base moment',v:f0(M2),u:'kNm',s:'+'+Math.round((M2/Mo-1)*100)+'% over first-order'},{l:'Stability index θ',v:f2(th),c:th>.1?'bad':'ok',st:th>.1?'P-Delta must be included':'Small'}])}
d();
"""),
 dict(h='In a tower, the base storey feels it most', p='The stability index of a storey is the weight above times the drift, over the storey shear. At the base the weight is greatest.', js=r"""
const L=Lab(H,{h:470,label:'Stability index by storey',note:'θ = P × Δ / (V × h) for each storey. With uniform stiffness drift ∝ storey shear, so θ at the base = base storey drift ratio ÷ base shear coefficient, and falls with height. Typical code threshold 0.1.'});
const sn=slider(L.sl,{label:'Number of storeys',min:10,max:70,step:1,value:40,fmt:v=>v+'',on:d});
const sc=slider(L.sl,{label:'Base shear coefficient VB / W',min:.5,max:6,step:.1,value:1.5,fmt:v=>f1(v)+'%',on:d});
const sd=slider(L.sl,{label:'Base storey drift ratio',min:.05,max:.5,step:.01,value:.12,fmt:v=>f2(v)+'%',on:d});
function d(){const g=L.svg,N=sn.v(),c=sc.v()/100,dd=sd.v()/100,th0=dd/c;clear(g);
 const P=plot(g,{x:70,y:30,w:520,h:360,x0:0,x1:Math.max(.2,Math.ceil(th0*10+.5)/10),y0:0,y1:N,xt:5,yt:[],xl:'stability index θ',yl:''});
 const dy=P.h/N;for(let i=1;i<=N;i++){const th=th0*(N-i+1)/N;rect(g,P.x,P.Y(i),Math.max(1,P.X(th)-P.x),dy*.8,th>.1?'f-pushs':'f-waters',{opacity:.8})}
 line(g,P.X(.1),P.y,P.X(.1),P.y+P.h,'s-push',{'stroke-dasharray':'8 5','stroke-width':3});T(g,P.X(.1)+8,P.y+22,'0.1',{'font-size':20});
 const nOver=Array.from({length:N},(_,i)=>th0*(N-i)/N).filter(t=>t>.1).length;
 tiles(L.out,[{l:'θ at the base',v:f2(th0),c:th0>.25?'bad':th0>.1?'warn':'ok',st:th0>.25?'Unstable, redesign':th0>.1?'Include P-Delta':'Negligible'},{l:'Storeys over 0.1',v:nOver},{l:'Amplification at base',v:f2(1/(1-Math.min(th0,.95))),u:'×',s:'1 / (1 − θ), roughly'}])}
d();
""")],
 quiz=[dict(q='P-Delta makes drift…', o=['Smaller','Larger','No change'], a=1, w='The weight acts through a leaning member and adds overturning moment, so drift rises.'),
  dict(q='Where is the stability index highest in a tall building?', o=['Top storey','Base storey','Middle'], a=1, w='The base carries the weight of every floor above it.'),
  dict(q='In ETABS you should switch on P-Delta…', o=['Only for buildings above 100 m','For every load combination the building will be designed with, including gravity','Never'], a=1, w='Set the P-Delta case to include the gravity load pattern you intend to combine, and run it in each combination.')],
 rules=['Include P-Delta in every tall building analysis. It is cheap and avoids unconservative drift.','If θ goes above 0.25, the structure is flirting with instability: stiffen it.','P-Delta and column slenderness are different things: P-Delta is global lean, slenderness is local bow.','Use the nominal gravity load pattern consistent with the combination, not an arbitrary one.'],
 codes=['IS 456:2000 cl 39.7 (slender columns)','IS 1893 (Part 1):2016 cl 7.11.1','IS 16700:2023 cl 5','ACI 318 stability index (for reference)']))

# ---------------------------------------------------------------- 18
PAGES.append(dict(n=18, slug='transfer-structures', group='Tall buildings',
 title='Transfer structures and floating columns',
 lede='When a column or wall above has no column below, the load must be carried sideways first. That detour is what a transfer structure does, and it comes at a cost.',
 sections=[
 dict(h='A column sitting on a beam', p='Move the load along the beam. The closer to the middle, the more the beam bends. See how deep it has to be.', js=r"""
const L=Lab(H,{h:470,label:'Transfer beam carrying a column load',note:'Point load on a simply supported transfer beam, M50, no self-weight. Depth from limiting moment: M<sub>u,lim</sub> = 0.133 f<sub>ck</sub> b d². Real transfer beams are deep: check shear, bearing and torsion too.'});
const sL=slider(L.sl,{label:'Span L',min:4,max:16,step:.5,value:9,fmt:v=>f1(v)+' m',on:d});
const sa=slider(L.sl,{label:'Load position along the span',min:.1,max:.9,step:.05,value:.5,fmt:v=>Math.round(v*100)+'%',on:d});
const sP=slider(L.sl,{label:'Factored column load Pu',min:1000,max:30000,step:500,value:8000,fmt:v=>f0(v)+' kN',on:d});
const sb=slider(L.sl,{label:'Beam width b',min:400,max:2000,step:100,value:1000,fmt:v=>v+' mm',on:d});
function d(){const g=L.svg,Lm=sL.v(),a=sa.v(),P=sP.v(),b=sb.v();clear(g);
 const R1=P*(1-a),R2=P*a,M=P*a*(1-a)*Lm,V=Math.max(R1,R2),dreq=Math.sqrt(M*1e6/(.133*50*b)),D=dreq+60;
 const x0=70,w=500,xp=x0+a*w;
 arrow(g,xp,40,xp,106,'s-push','ah',{'stroke-width':6});T(g,xp,30,f0(P)+' kN',{'text-anchor':'middle','font-size':21,'font-weight':600});
 const hh=Math.min(70,Math.max(20,D/16));rect(g,x0,110,w,hh,'f-conc');pin(g,x0,110+hh,14);roller(g,x0+w,110+hh,14);
 T(g,x0,110+hh+64,f0(R1)+' kN',{'text-anchor':'middle','font-size':20});T(g,x0+w,110+hh+64,f0(R2)+' kN',{'text-anchor':'middle','font-size':20});
 const y=370,sc=90/Math.max(M,1);line(g,x0,y,x0+w,y,'s-ink');poly(g,[[x0,y],[xp,y+M*sc],[x0+w,y]],{class:'f-water'});
 T(g,xp,y+M*sc+26,f0(M)+' kNm',{'text-anchor':'middle','font-size':21,'font-weight':600});T(g,x0,y-60,'bending moment',{'font-size':19});
 const Ld=Lm*1000/D;
 tiles(L.out,[{l:'Max moment',v:f0(M),u:'kNm'},{l:'Max shear',v:f0(V),u:'kN'},{l:'Depth needed',v:f0(D),u:'mm',c:Ld<4?'warn':'ok',st:'span/depth '+f1(Ld),s:Ld<4?'deep beam: use strut-and-tie':'normal flexure'},{l:'Moment ratio',v:f2(M/(P*Lm/4)),s:'to load at mid span',c:'warn'}])}
d();
"""),
 dict(h='A wall that stops at the podium', p='Above the podium, walls make the building stiff. Below, a few columns. That stiffness cliff makes the transfer floor a soft storey. Make the podium stiffer and watch the ratio.', js=r"""
const L=Lab(H,{h:460,label:'Stiffness of the transfer storey compared with the storey above',note:'Storey stiffness: walls 1 / (h³/12EI + 1.2h/GA), columns 12EI/h³, same concrete. Soft storey if podium stiffness is under 70% of the storey above (IS 1893 Table 6).'});
const sw=slider(L.sl,{label:'Number of walls above',min:2,max:10,step:1,value:6,fmt:v=>v+'',on:d});
const sl=slider(L.sl,{label:'Wall length',min:2,max:10,step:.5,value:5,fmt:v=>f1(v)+' m',on:d});
const st=slider(L.sl,{label:'Wall thickness',min:200,max:600,step:25,value:300,fmt:v=>v+' mm',on:d});
const sn=slider(L.sl,{label:'Columns in the podium',min:4,max:30,step:1,value:12,fmt:v=>v+'',on:d});
const sc=slider(L.sl,{label:'Podium column size',min:600,max:2000,step:100,value:1000,fmt:v=>v+' mm',on:d});
const sh=slider(L.sl,{label:'Podium storey height',min:3.5,max:8,step:.5,value:5,fmt:v=>f1(v)+' m',on:d});
function d(){const g=L.svg;clear(g);const nw=sw.v(),Lw=sl.v(),t=st.v()/1000,n=sn.v(),c=sc.v()/1000,hp=sh.v(),ha=3.2,E=1,G=.4;
 const kw=Lw0=>{const I=t*Lw**3/12,A=t*Lw;return 1/(ha**3/(12*E*I)+1.2*ha/(G*E*A))},kc=(c,h)=>12*E*(c**4/12)/h**3;
 const kA=nw*kw(),kP=n*kc(c,hp)+0,ratio=kP/kA;
 const top=40,bot=360;rect(g,40,bot,520,14,'f-conc');
 const wallsx=[];for(let i=0;i<nw;i++)wallsx.push(70+i*(480/Math.max(nw-1,1)));
 for(let f=0;f<3;f++){const y1=top+f*60,y2=y1+60;line(g,60,y2,560,y2,'s-beam',{'stroke-width':4});wallsx.forEach(x=>rect(g,x-Math.max(4,t*14),y1,Math.max(8,t*28),60,'f-conc'))}
 const py=top+180;line(g,60,py,560,py,'s-beam',{'stroke-width':8});
 for(let i=0;i<n&&i<12;i++){const x=70+i*(480/Math.max(Math.min(n,12)-1,1));rect(g,x-c*9,py,c*18,bot-py,'f-conc')}
 T(g,300,py+28,'transfer floor',{'text-anchor':'middle','font-size':20,'font-weight':600});
 const rr=Math.min(ratio,1.2);T(g,550,top+90,'walls above',{'text-anchor':'end','font-size':20});
 tiles(L.out,[{l:'Podium ÷ storey above',v:f2(ratio),c:ratio>=.8?'ok':ratio>=.7?'warn':'bad',st:ratio>=.7?(ratio>=.8?'Regular':'Close to soft'):ratio>=.6?'Soft storey':'Extreme soft storey',s:'needs ≥ 0.7'},{l:'Storey above',v:f0(kA*1000),s:'relative units'},{l:'Podium storey',v:f0(kP*1000),s:'relative units'}])}
d();
""")],
 quiz=[dict(q='A transfer beam’s depth is mainly set by…', o=['Wind','Large bending and shear from the load it collects','Fire'], a=1, w='All the column load above must bend through the beam to reach its supports. The moment is large, so the beam is deep.'),
  dict(q='Floating columns (stopping on a beam) are discouraged in seismic zones because…', o=['They are ugly','The load path is indirect and the beam can fail suddenly','They need more concrete'], a=1, w='IS 1893 treats them as a vertical irregularity. Failure of the beam drops the column load abruptly.'),
  dict(q='Walls above, open columns below: the transfer floor is typically…', o=['Stiff','A soft storey','Unaffected'], a=1, w='The sharp stiffness drop collects the drift in that storey.')],
 rules=['Avoid transfers if you can. Try to line up walls and columns.','If you must, make the transfer structure a deep beam or thick slab designed for strut-and-tie action.','Check the soft storey at the transfer level and use shear walls to carry through.','Put extra strength in the supporting columns: they carry the whole redirected load plus overturning.'],
 codes=['IS 456:2000 cl 29 (deep beams)','IS 1893 (Part 1):2016 Table 6','IS 13920:2016','IS 16700:2023']))

PAGES = []

# ---------------------------------------------------------------- 04
PAGES.append(dict(n=4, slug='stiffness', group='Foundations of structural behaviour',
 title='Stiffness: the stiff member takes the load',
 lede='Load does not share equally. It goes to whatever resists movement most. A small change in size can move most of the force.',
 sections=[
 dict(h='Three columns, one slab, one push', p='A sideways force hits a stiff floor slab. It is shared between the columns in proportion to their <b>stiffness</b>, which goes with size to the <b>fourth power</b>.', js=r"""
const L=Lab(H,{h:440,label:'Three columns resisting a sideways force',note:'Columns fixed at both ends, same material and height. Stiffness k = 12EI/h³ and I = D⁴/12, so share ∝ D⁴.'});
const sa=slider(L.sl,{label:'Column A size',min:300,max:900,step:25,value:400,fmt:v=>v+' mm',on:d});
const sb=slider(L.sl,{label:'Column B size',min:300,max:900,step:25,value:400,fmt:v=>v+' mm',on:d});
const sc=slider(L.sl,{label:'Column C size',min:300,max:900,step:25,value:600,fmt:v=>v+' mm',on:d});
const sv=slider(L.sl,{label:'Sideways force',min:100,max:2000,step:50,value:600,fmt:v=>v+' kN',on:d});
const sh=slider(L.sl,{label:'Storey height',min:3,max:6,step:.25,value:3.5,fmt:v=>f2(v)+' m',on:d});
function d(){const D=[sa.v(),sb.v(),sc.v()],V=sv.v(),h=sh.v(),g=L.svg;clear(g);
 const k=D.map(x=>Math.pow(x,4)),K=k[0]+k[1]+k[2],F=k.map(x=>V*x/K);
 const xs=[140,320,500],bot=380,top=140;
 rect(g,50,top-26,540,26,'f-conc');rect(g,40,bot,560,16,'f-conc');
 D.forEach((x,i)=>{const w=x*.11;rect(g,xs[i]-w/2,top,w,bot-top,'f-conc');
  const L2=20+F[i]/V*150;arrow(g,xs[i]+w/2+L2,(top+bot)/2,xs[i]+w/2+6,(top+bot)/2,'s-push','ah',{'stroke-width':3+F[i]/V*7});
  T(g,xs[i],bot+44,String.fromCharCode(65+i)+': '+D[i]+' mm',{'text-anchor':'middle','font-size':21,'font-weight':600});
  T(g,xs[i]+w/2+L2+8,(top+bot)/2-12,f0(F[i])+' kN',{'font-size':21,'font-weight':600})});
 arrow(g,18,top-13,48,top-13,'s-ink','ahk',{'stroke-width':4});T(g,18,top-34,f0(V)+' kN',{'font-size':21});
 tiles(L.out,D.map((x,i)=>({l:'Column '+String.fromCharCode(65+i),v:f0(F[i]),u:'kN',s:Math.round(F[i]/V*100)+'% of force · M = '+f0(F[i]*h/2)+' kNm',c:F[i]/V>.5?'warn':''})).concat([{l:'C vs A',v:f1(Math.pow(D[2]/D[0],4)),u:'×',s:'stiffness ratio'}]))}
d();
"""),
 dict(h='The short-column trap', p='Brick infill that stops partway up a column makes it <b>short</b>. A short column is far stiffer, so it grabs far more force. Then it breaks in shear.', js=r"""
const L=Lab(H,{h:420,label:'Two identical columns, one partly walled in',note:'Same section and material. Stiffness goes with 1 / free height³. Shear failure of short columns is a classic earthquake damage pattern.'});
const si=slider(L.sl,{label:'Infill height, as share of storey',min:0,max:85,step:5,value:50,fmt:v=>v+'%',on:d});
function d(){const r=si.v()/100,g=L.svg;clear(g);const top=90,bot=360,hh=bot-top,free=1-r;
 const kA=1,kB=1/Math.pow(free,3),sB=kB/(kA+kB),V=1;
 rect(g,100,top-26,440,26,'f-conc');rect(g,90,bot,460,16,'f-conc');
 rect(g,180,top,36,hh,'f-conc');rect(g,424,top,36,hh,'f-conc');
 rect(g,216,bot-r*hh,208,r*hh,'f-sand');
 T(g,320,bot-r*hh/2+8,r>0?'brick infill':'',{'text-anchor':'middle','font-size':20});
 line(g,460,top,460,top,'s-ink');
 dimV(g,490,top,bot-r*hh,f2(free)+' h free',{anchor:'start',dx:12});
 arrow(g,50,top-13,98,top-13,'s-ink','ahk',{'stroke-width':4});
 arrow(g,170,(top+bot)/2,150-(1-sB)*80,(top+bot)/2,'s-push','ah',{'stroke-width':3+(1-sB)*8});
 arrow(g,470,(top+bot)/2+0,520,(top+bot)/2,'s-push','ah',{'stroke-width':3+sB*8,display:'none'});
 T(g,198,bot+44,'A: full height',{'text-anchor':'middle','font-size':21});T(g,442,bot+44,'B: short',{'text-anchor':'middle','font-size':21,'font-weight':600});
 if(sB>.55){const y=bot-r*hh-10;line(g,424,y-18,460,y+18,'s-push',{'stroke-width':4});line(g,460,y-18,424,y+18,'s-push',{'stroke-width':4})}
 tiles(L.out,[{l:'Short column B stiffness',v:f1(kB),u:'× A'},{l:'Force on A',v:Math.round((1-sB)*100),u:'%'},{l:'Force on B',v:Math.round(sB*100),u:'%',c:sB>.6?'bad':sB>.5?'warn':'ok',st:sB>.6?'shear failure risk':sB>.5?'attracts more':'shares equally'}])}
d();
""")],
 quiz=[dict(q='You make one column 20% bigger in each direction. Its stiffness rises by about…', o=['20%','44%','107%'], a=2, w='Stiffness goes with D⁴. 1.2⁴ = 2.07, so it more than doubles and attracts that much more force.'),
  dict(q='A shear wall and a frame share a lateral load. Who takes most of it at low levels?', o=['The frame','The shear wall','Equal'], a=1, w='The wall is far stiffer, so it attracts the load. Models must carry the wall stiffness correctly.'),
  dict(q='Brick infill goes only half way up a column. The column…', o=['Gets stronger','Becomes short and stiffer, and attracts more force','Is unchanged'], a=1, w='The free height halves, so stiffness goes up 8×. Shear failure follows.')],
 rules=['Force follows stiffness. Never assume equal sharing.','Stiffness: columns D⁴, beams b × D³, walls ~ length³ × thickness.','Cracking changes stiffness. Modifiers matter in ETABS (see topic 26).','Check every place where a column or wall is partly restrained.'],
 codes=['IS 1893 (Part 1):2016 cl 7.1 (irregularities)','IS 13920:2016','IS 16700:2023']))

# ---------------------------------------------------------------- 05
PAGES.append(dict(n=5, slug='materials', group='Foundations of structural behaviour',
 title='Concrete and steel: the two materials',
 lede='Concrete is strong in squeezing and weak in pulling. Steel is strong in pulling. Together they work, if you know how each behaves.',
 sections=[
 dict(h='How each material answers a push', p='Pick a material and grade. The curve shows the stress each can give at any strain, using the <b>design curves of IS 456</b>.', js=r"""
const L=Lab(H,{h:440,label:'Stress-strain curve of concrete or steel',note:'IS 456 design curves (Fig. 21 and Fig. 23). Concrete: parabola to 0.002 then flat to 0.0035. Steel: straight to 0.8 f<sub>yd</sub>, then curved to f<sub>yd</sub>.'});
const mt=chips(L.sl,[['Concrete','c'],['Steel','s']],d,'c','Material');
const sf=slider(L.sl,{label:'Concrete grade fck',min:20,max:60,step:5,value:30,fmt:v=>'M'+v,on:d});
const fy=chips(L.sl,[['Fe415',415],['Fe500',500],['Fe550',550]],d,500,'Steel grade');
function d(){const g=L.svg;clear(g);const fck=sf.v(),Fy=fy.get(),fyd=.87*Fy,Es=2e5;
 if(mt.get()==='c'){const P=plot(g,{x0:0,x1:4,y0:0,y1:60,xt:4,yt:[0,10,20,30,40,50,60],xl:'strain × 10⁻³',yl:'stress, MPa'});
  const fd=.446*fck;curve(g,P,e=>{const x=e*1e-3;return x<=.002?fd*(2*x/.002-(x/.002)**2):fd},0,4,'s-push',100,{'stroke-width':3.5});
  line(g,P.X(0),P.Y(fck),P.X(4),P.Y(fck),'s-muted');T(g,P.X(4)-6,P.Y(fck)-8,'fck '+fck,{'font-size':19,'text-anchor':'end'});
  circ(g,P.X(2),P.Y(fd),7,'f-ink');T(g,P.X(2)+12,P.Y(fd)-12,'peak 0.446 fck = '+f1(fd),{'font-size':20});
  line(g,P.X(3.5),P.Y(0),P.X(3.5),P.Y(fd),'s-ink');T(g,P.X(3.5)-4,P.Y(0)-10,'crushes 0.0035',{'font-size':19,'text-anchor':'end'});
  tiles(L.out,[{l:'Elastic modulus Ec',v:f0(5000*Math.sqrt(fck)),u:'MPa',s:'5000√fck'},{l:'Cracks in tension',v:f1(.7*Math.sqrt(fck)),u:'MPa',s:'0.7√fck'},{l:'Design strength',v:f1(fd),u:'MPa'},{l:'Crushing strain',v:'0.0035'}])}
 else{const P=plot(g,{x0:0,x1:6,y0:0,y1:500,xt:6,yt:[0,100,200,300,400,500],xl:'strain × 10⁻³',yl:'stress, MPa'});
  const fr=[.8,.85,.9,.95,.975,1],ex=[0,.0001,.000295,.000695,.001,.002];
  const pp=[[0,0]].concat(fr.map((f,i)=>[(f*fyd/Es+ex[i])*1e3,f*fyd]));pp.push([6,fyd]);
  pline(g,pp.map(q=>[P.X(q[0]),P.Y(q[1])]),'s-push',{'stroke-width':3.5});
  line(g,P.X(0),P.Y(Fy),P.X(6),P.Y(Fy),'s-muted');T(g,P.X(6)-6,P.Y(Fy)-8,'fy '+Fy,{'font-size':19,'text-anchor':'end'});
  circ(g,P.X(pp[6][0]),P.Y(fyd),7,'f-ink');T(g,P.X(pp[6][0])+12,P.Y(fyd)+30,'design 0.87 fy = '+f0(fyd),{'font-size':20});
  tiles(L.out,[{l:'Modulus Es',v:'2,00,000',u:'MPa'},{l:'Design strength',v:f0(fyd),u:'MPa'},{l:'Yield strain',v:f3(fyd/Es+.002),s:'fyd/Es + 0.002'},{l:'Ratio Es / Ec',v:f1(Es/(5000*Math.sqrt(fck))),s:'modular-ratio feel'}])}}
d();
"""),
 dict(h='Concrete keeps moving after you load it', p='Under a steady load, concrete slowly creeps. It also shrinks as it dries. Both make a slab sag far more than the day-one calculation.', js=r"""
const L=Lab(H,{h:440,label:'Strain growing with time under steady stress',note:'Creep coefficients from IS 456 cl 6.2.5.1: 2.2 (loaded at 7 days), 1.6 (28 days), 1.1 (1 year). Shrinkage 0.0003 if no data.'});
const sf=slider(L.sl,{label:'Concrete grade',min:20,max:60,step:5,value:30,fmt:v=>'M'+v,on:d});
const ss=slider(L.sl,{label:'Sustained stress',min:2,max:15,step:.5,value:8,fmt:v=>f1(v)+' MPa',on:d});
const ag=chips(L.sl,[['Loaded at 7 days',2.2],['at 28 days',1.6],['at 1 year',1.1]],d,1.6,'When you load it');
const sh=slider(L.sl,{label:'Shrinkage strain',min:200,max:600,step:50,value:300,fmt:v=>(v)+' × 10⁻⁶',on:d});
function d(){const g=L.svg;clear(g);const fck=sf.v(),Ec=5000*Math.sqrt(fck),el=ss.v()/Ec*1e6,th=ag.get(),sk=sh.v();
 const P=plot(g,{x0:0,x1:5,y0:0,y1:Math.ceil((el*(1+2.2)+600)/200)*200,xt:5,yt:5,xl:'years after loading',yl:'strain × 10⁻⁶'});
 const cr=t=>el*(1+th*(1-Math.exp(-t/.6))),tot=t=>cr(t)+sk*(1-Math.exp(-t));
 curve(g,P,t=>el,0,5,'s-muted',2);T(g,P.X(.1),P.Y(el)+24,'elastic, day one',{'font-size':19});
 curve(g,P,cr,0,5,'s-water',100,{'stroke-width':3});T(g,P.X(5)-4,P.Y(cr(5))+26,'+ creep',{'font-size':19,'text-anchor':'end'});
 curve(g,P,tot,0,5,'s-push',100,{'stroke-width':3.5});T(g,P.X(5)-4,P.Y(tot(5))-10,'+ shrinkage',{'font-size':19,'text-anchor':'end'});
 tiles(L.out,[{l:'Elastic strain',v:f0(el),u:'×10⁻⁶'},{l:'Creep at 5 yr',v:f0(cr(5)-el),u:'×10⁻⁶'},{l:'Shrinkage',v:f0(sk),u:'×10⁻⁶'},{l:'Total at 5 yr',v:f0(tot(5)),u:'×10⁻⁶'},{l:'Long-term stiffness',v:f0(Ec/(1+th)),u:'MPa',s:'Ec / (1 + θ)',c:'warn'},{l:'Sag multiplier',v:f2(1+th),u:'×',s:'creep only'}])}
d();
""")],
 quiz=[dict(q='Concrete cracks in tension at a stress of roughly…', o=['0.7√fck, about 3.8 MPa for M30','0.5 fck','fck'], a=0, w='Tensile strength is only about a tenth of compressive strength, so steel carries tension.'),
  dict(q='A slab is loaded at 7 days instead of 28. Creep…', o=['Is lower','Is higher','Is unchanged'], a=1, w='Younger concrete creeps more. θ = 2.2 against 1.6. Early propping removal costs you stiffness later.'),
  dict(q='Steel Fe500 has design strength of…', o=['500 MPa','435 MPa','415 MPa'], a=1, w='fyd = 0.87 fy = 0.87 × 500 = 435 MPa.')],
 rules=['Ec = 5000√fck (IS 456). Higher grade means stiffer, but not in proportion.','Design strengths are 0.446 fck and 0.87 fy. Always design with these, not the characteristic values.','Long-term deflection can be 2–3× the short-term value.','Steel and concrete expand together, which is why they work as one.'],
 codes=['IS 456:2000 cl 6.2 (elastic properties)','IS 456 Fig. 21, 23','IS 456 cl 6.2.5 (creep)','IS 1786 (reinforcing bars)']))

# ---------------------------------------------------------------- 06
PAGES.append(dict(n=6, slug='limit-state-design', group='RCC design',
 title='Limit state design: factors and combinations',
 lede='We do not design for the loads we expect. We design for loads pushed up by factors, against strengths pushed down. The gap is the safety.',
 sections=[
 dict(h='Load combinations: which one governs?', p='A member sees many load combinations. Pick lateral load type, set the loads, and see which combination is the worst.', js=r"""
const L=Lab(H,{h:440,label:'Factored load combinations as bars',note:'Axial force in a column, kN. Bars run from the case with the lateral load acting one way to the other. Combinations from IS 456 Table 18 (wind) and IS 1893 / IS 16700 (earthquake).'});
const kd=chips(L.sl,[['Wind','w'],['Earthquake','e']],d,'e','Lateral load');
const sD=slider(L.sl,{label:'Dead load DL',min:200,max:3000,step:50,value:1200,fmt:v=>v+' kN',on:d});
const sL=slider(L.sl,{label:'Live load LL',min:0,max:1500,step:50,value:300,fmt:v=>v+' kN',on:d});
const sE=slider(L.sl,{label:'Lateral effect (±)',min:0,max:1500,step:25,value:500,fmt:v=>v+' kN',on:d});
const sC=slider(L.sl,{label:'Column capacity',min:500,max:6000,step:100,value:2500,fmt:v=>v+' kN',on:d});
function d(){const DL=sD.v(),LL=sL.v(),E=sE.v(),Cp=sC.v(),eq=kd.get()==='e',g=L.svg;clear(g);
 const nm=eq?'EL':'WL';
 const cb=[['1.5 (DL + LL)',1.5*(DL+LL),1.5*(DL+LL)],['1.2 (DL + LL ± '+nm+')',1.2*(DL+LL)+1.2*E,1.2*(DL+LL)-1.2*E],['1.5 (DL ± '+nm+')',1.5*DL+1.5*E,1.5*DL-1.5*E],['0.9 DL ± 1.5 '+nm,.9*DL+1.5*E,.9*DL-1.5*E]];
 const mx=Math.max(Cp*1.1,...cb.map(c=>c[1])),mn=Math.min(0,...cb.map(c=>c[2])),x0=60,w=560,X=v=>x0+(v-mn)/(mx-mn)*w;
 const gov=cb.reduce((a,c,i)=>c[1]>cb[a][1]?i:a,0);
 line(g,X(0),40,X(0),360,'s-ink');
 cb.forEach((c,i)=>{const y=60+i*78;T(g,x0,y-10,c[0],{'font-size':21,'font-weight':i===gov?700:500});
  rect(g,X(Math.min(c[1],c[2])),y,Math.abs(X(c[1])-X(c[2]))+4,34,i===gov?'f-push':'f-water');
  T(g,X(c[1])+8,y+25,f0(c[1]),{'font-size':20});if(c[2]<0)T(g,X(c[2])-8,y+25,f0(c[2]),{'font-size':20,'text-anchor':'end'})});
 line(g,X(Cp),36,X(Cp),372,'s-push',{'stroke-dasharray':'8 5','stroke-width':3});T(g,X(Cp)-6,392,'capacity '+f0(Cp),{'font-size':21,'text-anchor':'end','font-weight':600});
 const u=cb[gov][1]/Cp,tens=Math.min(...cb.map(c=>c[2]));
 tiles(L.out,[{l:'Governing, compression',v:f0(cb[gov][1]),u:'kN',s:cb[gov][0]},{l:'Utilisation',v:Math.round(u*100),u:'%',c:u<=1?(u>.9?'warn':'ok'):'bad',st:u<=1?'OK':'Overloaded'},{l:'Least force',v:f0(tens),u:'kN',c:tens<0?'bad':'ok',st:tens<0?'Net tension: check uplift and splices':'Always in compression'}])}
d();
"""),
 dict(h='Why the factors exist: scatter', p='Real loads and real strengths both vary. The factors keep the overlap of the two bell curves very small. Change the scatter and see the chance of failure.', js=r"""
const L=Lab(H,{h:400,label:'Load and resistance distributions overlapping',note:'Normal distributions. Reliability index β = (mean R − mean S) / √(σR² + σS²). Illustrative: code factors are calibrated on many more cases.'});
const sr=slider(L.sl,{label:'Mean resistance ÷ mean load',min:1.2,max:3,step:.05,value:1.8,fmt:v=>f2(v)+' ×',on:d});
const cs=slider(L.sl,{label:'Scatter in load',min:5,max:40,step:1,value:15,fmt:v=>v+'%',on:d});
const cr=slider(L.sl,{label:'Scatter in resistance',min:5,max:30,step:1,value:12,fmt:v=>v+'%',on:d});
function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+.3275911*x),y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-x*x);return s*y}
const Phi=z=>.5*(1+erf(z/Math.SQRT2));
function d(){const g=L.svg;clear(g);const mS=100,mR=100*sr.v(),sS=mS*cs.v()/100,sR=mR*cr.v()/100;
 const P=plot(g,{x0:0,x1:400,y0:0,y1:1,xt:4,yt:[0],xl:'load or resistance (relative)',yl:''});
 const nrm=(m,s)=>x=>Math.exp(-.5*((x-m)/s)**2)/(Math.sqrt(2*Math.PI)*s);
 const fS=nrm(mS,sS),fR=nrm(mR,sR),pk=Math.max(fS(mS),fR(mR));
 P.o.y1=pk*1.1;const Y=v=>P.y+P.h-v/(pk*1.1)*P.h;
 const a=[],b=[],o=[];for(let x=0;x<=400;x+=2){a.push([P.X(x),Y(fS(x))]);b.push([P.X(x),Y(fR(x))]);o.push([P.X(x),Y(Math.min(fS(x),fR(x)))])}
 poly(g,[[P.X(0),Y(0)]].concat(o).concat([[P.X(400),Y(0)]]),{class:'f-push'});
 pline(g,a,'s-water',{'stroke-width':3.5});pline(g,b,'s-ok',{'stroke-width':3.5});
 T(g,P.X(mS),Y(fS(mS))-10,'load',{'text-anchor':'middle','font-size':22,'font-weight':600});T(g,P.X(mR),Y(fR(mR))-10,'resistance',{'text-anchor':'middle','font-size':22,'font-weight':600});
 const beta=(mR-mS)/Math.sqrt(sR*sR+sS*sS),pf=Phi(-beta);
 tiles(L.out,[{l:'Reliability index β',v:f2(beta),c:beta>=3.5?'ok':beta>=2.5?'warn':'bad',st:beta>=3.5?'Comfortable':beta>=2.5?'Marginal':'Too risky',s:'buildings aim near 3.5–4'},{l:'Chance of failure',v:pf<1e-7?'< 1 in 10 million':'1 in '+f0(1/pf)},{l:'Overlap',v:'red area'}])}
d();
"""),
 dict(h='Design strengths: what the code takes away', p='The code cuts material strength before you use it. This is the other half of safety.', js=r"""
const L=Lab(H,{h:300,label:'Characteristic versus design strength',note:'γm = 1.5 for concrete, 1.15 for steel. The 0.67 factor covers the gap between a test cube and the real member.'});
const g1=chips(L.sl,[['M25',25],['M30',30],['M40',40],['M50',50]],d,30,'Concrete');
const g2=chips(L.sl,[['Fe415',415],['Fe500',500],['Fe550',550]],d,500,'Steel');
function d(){const g=L.svg;clear(g);const fc=g1.get(),fy=g2.get(),rows=[['Concrete fck',fc,.67*fc/1.5,'0.67 / 1.5 = 0.446'],['Steel fy',fy,fy/1.15,'1 / 1.15 = 0.87']];
 rows.forEach((r,i)=>{const y=40+i*130,sc=470/Math.max(fy,fc*10);const mx=i?fy:fc*10;const k=470/ (i?560:60);
  T(g,40,y,r[0]+' = '+r[1]+' MPa',{'font-size':22,'font-weight':600});rect(g,40,y+14,r[1]*k,28,'f-water');
  rect(g,40,y+50,r[2]*k,28,'f-ok');T(g,40+r[2]*k+10,y+72,'design '+f0(r[2])+' MPa  ('+r[3]+')',{'font-size':20})});
 L.out.innerHTML=''}
d();
""")],
 quiz=[dict(q='Which combination usually governs a column in tension (uplift)?', o=['1.5 (DL + LL)','1.2 (DL + LL ± EL)','0.9 DL ± 1.5 EL'], a=2, w='Less dead load to hold it down, more lateral load pulling it up. This combination reveals net tension.'),
  dict(q='A design load factor is higher on live load than on dead load because…', o=['Live load is more uncertain','Live load is heavier','It is a habit'], a=0, w='Live and lateral loads scatter more. Factors follow the scatter.'),
  dict(q='The partial safety factor on steel (1.15) is lower than concrete (1.5) because…', o=['Steel is stronger','Steel is made in a factory so its strength varies less','Steel is cheaper'], a=1, w='Steel strength is far more consistent than site concrete.')],
 rules=['Check every combination. Do not trust one to cover all.','The 0.9 DL combination matters for uplift and overturning.','Serviceability checks (deflection, cracks, drift) use unfactored loads.','A higher factor does not fix a wrong model. It only adds margin to a good one.'],
 codes=['IS 456:2000 cl 18, Table 18','IS 1893 (Part 1):2016 cl 6.3','IS 16700:2023 cl 5','IS 875 (Part 5) load combinations']))

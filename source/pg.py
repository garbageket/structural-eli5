PAGES = []

# ---------------------------------------------------------------- 19
PAGES.append(dict(n=19, slug='soil-bearing-capacity', group='Geotechnical and foundations',
 title='Soil basics and bearing capacity',
 lede='Soil is solids, water and air. How much of each it holds decides its weight, and how much load it can carry before it fails under a footing.',
 sections=[
 dict(h='Three phases in one block', p='Imagine a unit block of soil. Change the voids and the water in them and see weight, water content and density change.', js=r"""
const L=Lab(H,{h:440,label:'Soil block split into solids, water and air',note:'γ = (Gs + S e) γw / (1 + e). Dry density γd = Gs γw / (1 + e). γw = 9.81 kN/m³.'});
const se=slider(L.sl,{label:'Void ratio e',min:.3,max:1.6,step:.05,value:.7,fmt:v=>f2(v),on:d});
const sr=slider(L.sl,{label:'Saturation S',min:0,max:100,step:5,value:60,fmt:v=>v+'%',on:d});
const sg=slider(L.sl,{label:'Specific gravity of solids Gs',min:2.55,max:2.8,step:.01,value:2.65,fmt:v=>f2(v),on:d});
chips(L.sl,[['Dense dry sand',[.5,0]],['Wet sand',[.7,70]],['Soft clay, saturated',[1.3,100]],['Murum',[.6,50]]],v=>{se.set(v[0]);sr.set(v[1])},undefined,'Typical soils');
function d(){const e=se.v(),S=sr.v()/100,Gs=sg.v(),g=L.svg;clear(g);
 const Vs=1/(1+e),Vv=e/(1+e),Vw=S*Vv,Va=Vv-Vw,gw=9.81,gam=(Gs+S*e)*gw/(1+e),gd=Gs*gw/(1+e),gs=(Gs+e)*gw/(1+e),w=S*e/Gs;
 const x0=80,w0=190,top=40,hh=340;let y=top+hh;
 const parts=[['Air',Va,'f-slab'],['Water',Vw,'f-water'],['Solids',Vs,'f-sand']].reverse();
 [['Solids',Vs,'f-sand'],['Water',Vw,'f-water'],['Air',Va,'f-slab']].forEach(p=>{const h=p[1]*hh;if(h>.3){rect(g,x0,y-h,w0,h,p[2]);if(h>22)T(g,x0+w0+14,y-h/2+7,p[0]+' '+f2(p[1]),{'font-size':21,'font-weight':600});y-=h}});
 rect(g,x0,top,w0,hh,'f-none',{stroke:'var(--ink)','stroke-width':2.5});
 T(g,x0+w0/2,top-10,'1 m³ of soil',{'text-anchor':'middle','font-size':20});
 tiles(L.out,[{l:'Bulk unit weight γ',v:f1(gam),u:'kN/m³'},{l:'Dry unit weight γd',v:f1(gd),u:'kN/m³'},{l:'Saturated γsat',v:f1(gs),u:'kN/m³'},{l:'Water content w',v:f1(w*100),u:'%'},{l:'Porosity n',v:Math.round(e/(1+e)*100),u:'%'}])}
d();
"""),
 dict(h='What can the ground carry under a footing?', p='Terzaghi-type bearing capacity: cohesion, overburden and the soil’s own weight each add something. Change the soil, the footing and the water table.', js=r"""
const L=Lab(H,{h:470,label:'Footing in soil with failure wedge and water table',note:'q<sub>u</sub> = cN<sub>c</sub> + qN<sub>q</sub> + ½γBN<sub>γ</sub> (strip); square: 1.3cN<sub>c</sub> + qN<sub>q</sub> + 0.4γBN<sub>γ</sub>. Meyerhof N factors, FS = 3. Indicative: design from the geotechnical report and IS 6403.'});
const sc=slider(L.sl,{label:'Cohesion c',min:0,max:120,step:5,value:0,fmt:v=>v+' kPa',on:d});
const sp=slider(L.sl,{label:'Friction angle φ',min:0,max:42,step:1,value:32,fmt:v=>v+'°',on:d});
const sB=slider(L.sl,{label:'Footing width B',min:1,max:6,step:.25,value:2.5,fmt:v=>f2(v)+' m',on:d});
const sD=slider(L.sl,{label:'Depth Df',min:.5,max:5,step:.25,value:1.5,fmt:v=>f2(v)+' m',on:d});
const sy=slider(L.sl,{label:'Soil unit weight γ',min:15,max:22,step:.5,value:18,fmt:v=>f1(v)+' kN/m³',on:d});
const sw=slider(L.sl,{label:'Water table depth',min:0,max:10,step:.5,value:10,fmt:v=>v>=10?'none':f1(v)+' m',on:d});
const sh=chips(L.sl,[['Strip',0],['Square',1]],d,1,'Shape');
function Nf(p){const t=Math.tan(rad(p)),Nq=Math.exp(Math.PI*t)*Math.pow(Math.tan(rad(45+p/2)),2),Nc=p>0?(Nq-1)/t:5.14,Ng=(Nq-1)*Math.tan(rad(1.4*p));return {Nq:Nq,Nc:Nc,Ng:Ng}}
function d(){const g=L.svg;clear(g);const c=sc.v(),p=sp.v(),B=sB.v(),Df=sD.v(),gm=sy.v(),wt=sw.v(),sq=sh.get(),N=Nf(p),gp=Math.max(gm-9.81,6);
 const q=wt>=Df?gm*Df:gm*wt+gp*(Df-wt);
 let ge=gm;if(wt<=Df)ge=gp;else if(wt<Df+B)ge=gp+(wt-Df)/B*(gm-gp);
 const t1=(sq?1.3:1)*c*N.Nc,t2=q*N.Nq,t3=(sq?.4:.5)*ge*B*N.Ng,qu=t1+t2+t3,qns=(qu-q)/3,gross=q+qns;
 // drawing
 const sc2=44,ground=100,fx=320;
 rect(g,0,ground,640,360,'f-sand');
 if(wt<10)line(g,0,ground+wt*sc2*.6,640,ground+wt*sc2*.6,'s-water',{'stroke-width':3}),T(g,630,ground+wt*sc2*.6-8,'water table',{'text-anchor':'end','font-size':19,style:'fill:var(--water)'});
 const fy=ground+Df*sc2*.6,bw=B*sc2;
 rect(g,fx-bw/2,fy-16,bw,16,'f-conc');rect(g,fx-14,ground-40,28,fy-ground+24,'f-conc');
 const wedge=bw/2*Math.tan(rad(45+p/2));poly(g,[[fx-bw/2,fy],[fx+bw/2,fy],[fx,fy+Math.min(wedge,220)]],{class:'f-push'});
 path(g,'M'+(fx+bw/2)+','+fy+' Q'+(fx+bw/2+Math.min(wedge,170))+','+(fy+Math.min(wedge,170)*.9)+' '+(fx+bw/2+Math.min(wedge*1.8,260))+','+fy,'s-push',{'stroke-dasharray':'7 5'});
 path(g,'M'+(fx-bw/2)+','+fy+' Q'+(fx-bw/2-Math.min(wedge,170))+','+(fy+Math.min(wedge,170)*.9)+' '+(fx-bw/2-Math.min(wedge*1.8,260))+','+fy,'s-push',{'stroke-dasharray':'7 5'});
 dimH(g,fx-bw/2,fx+bw/2,fy+34,'B = '+f2(B)+' m',{});
 arrow(g,fx,ground-90,fx,ground-48,'s-push','ah',{'stroke-width':5});
 const tot=Math.max(t1+t2+t3,1);
 bars(L.out,[{l:'Cohesion',v:t1,max:tot,c:'warn',t:f0(t1)},{l:'Overburden',v:t2,max:tot,c:'push',t:f0(t2)},{l:'Soil weight',v:t3,max:tot,c:'water',t:f0(t3)}]);
 L.out.insertAdjacentHTML('beforeend','<div style="height:1rem"></div>');
 const m=document.createElement('div');L.out.appendChild(m);
 tiles(m,[{l:'Ultimate qu',v:f0(qu),u:'kPa'},{l:'Net safe (FS 3)',v:f0(qns),u:'kPa'},{l:'Gross safe',v:f0(gross),u:'kPa',s:'incl. overburden'},{l:'Nγ / Nq / Nc',v:f1(N.Ng)+' / '+f1(N.Nq)+' / '+f1(N.Nc)}])}
d();
""")],
 quiz=[dict(q='A saturated soil has…', o=['No air in the voids','No water in the voids','No solids'], a=0, w='Saturated means the voids are full of water. Degree of saturation = 100%.'),
  dict(q='Bearing capacity rises most quickly when you…', o=['Widen a footing on clay','Go deeper in sand, or widen it','Raise the water table'], a=1, w='In sand, both depth (overburden) and width (soil weight) add capacity. In clay, width adds almost nothing.'),
  dict(q='A rising water table typically…', o=['Increases bearing capacity','Reduces it by about half in sand','Does nothing'], a=1, w='Buoyancy cuts the effective weight of the soil above and below the footing, so both terms fall.')],
 rules=['Bearing capacity comes from the soil investigation report: use its numbers, and ask for the water table range.','Settlement often governs before strength. Soft clays under big rafts settle for years.','Always check the worst water table, not the one on the day of the borehole.','Net safe pressure is what the footing can add on top of the soil already removed.'],
 codes=['IS 6403:1981 (bearing capacity)','IS 1904:1986 (shallow foundations)','IS 2131 (SPT), IS 2720 (soil tests)','IS 8009 (settlement)']))

# ---------------------------------------------------------------- 21
PAGES.append(dict(n=21, slug='foundation-types', group='Geotechnical and foundations',
 title='Shallow versus deep foundations',
 lede='A foundation is a way of spreading load into the ground. If the ground near the surface is good, spread it wide. If not, reach down to something better.',
 sections=[
 dict(h='Pick a foundation for the site', p='Set the column load, the grid and the ground. The footings grow until they touch, then a raft is cheaper. If the soil is poor, piles reach past it.', js=r"""
const L=Lab(H,{h:470,label:'Plan of footings and elevation of the chosen foundation',note:'Rule-of-thumb selection. Footing coverage = footing area ÷ grid area. Isolated below 25% coverage, strip or combined to 50%, raft above that. Piles when even a raft would overload the soil.'});
const sP=slider(L.sl,{label:'Service load per column',min:500,max:30000,step:500,value:6000,fmt:v=>f0(v)+' kN',on:d});
const sS=slider(L.sl,{label:'Column spacing',min:4,max:12,step:.5,value:8,fmt:v=>f1(v)+' m',on:d});
const sB=slider(L.sl,{label:'Safe bearing capacity',min:80,max:600,step:10,value:200,fmt:v=>v+' kPa',on:d});
const sH=slider(L.sl,{label:'Depth to hard strata',min:2,max:40,step:1,value:18,fmt:v=>v+' m',on:d});
function d(){const g=L.svg,P=sP.v(),s=sS.v(),q=sB.v(),Hd=sH.v();clear(g);
 const af=P*1.1/q,side=Math.sqrt(af),cov=af/(s*s),qr=P/(s*s);
 let kind;if(cov<.25)kind='Isolated footings';else if(cov<.5)kind='Strip / combined footings';else if(qr<=q*.9)kind='Raft';else kind='Piles';
 // plan
 const pk=Math.min(5.5,160/(3*s)*1);const sc2=Math.min(150/(3*s),28);
 const ox=70,oy=40;
 for(let i=0;i<3;i++)for(let j=0;j<3;j++){const cx=ox+(i+.5)*s*sc2,cy=oy+(j+.5)*s*sc2,w=Math.min(side,s)*sc2;
  if(kind==='Raft')rect(g,ox,oy,3*s*sc2,3*s*sc2,'f-slab',{stroke:'var(--ink)'});else if(kind==='Piles'){for(let a=-1;a<=1;a+=2)for(let b2=-1;b2<=1;b2+=2)circ(g,cx+a*5,cy+b2*5,4,'f-steel')}else rect(g,cx-w/2,cy-w/2,w,w,'f-conc');
  rect(g,cx-4,cy-4,8,8,'f-ink')}
 T(g,ox,oy+3*s*sc2+28,'plan, 3 × 3 columns',{'font-size':19});
 // elevation
 const ex=330,ey=60,ew=280,gh=330;rect(g,ex,ey,ew,gh,'f-sand');
 const hd=ey+Math.min(Hd,40)/40*gh*.9;rect(g,ex,hd,ew,ey+gh-hd,'f-conc');T(g,ex+ew-8,hd+26,'hard strata',{'text-anchor':'end','font-size':19});
 const cols=[ex+50,ex+140,ex+230];
 cols.forEach(x=>{rect(g,x-8,ey-40,16,60,'f-ink')});
 if(kind==='Raft'){rect(g,ex+20,ey+20,ew-40,24,'f-conc')}else if(kind.indexOf('Piles')===0){rect(g,ex+20,ey+20,ew-40,24,'f-conc');cols.forEach(x=>{for(let k=-1;k<=1;k+=2)rect(g,x+k*20-6,ey+44,12,Math.max(10,hd-ey-44+14),'f-conc')})}
 else cols.forEach(x=>{const w2=Math.min(100,side*14);rect(g,x-w2/2,ey+20,w2,18,'f-conc')});
 T(g,ex,ey-52,'elevation: '+kind,{'font-size':22,'font-weight':700});
 const lp=kind==='Piles'?Math.round(Hd+1):null;
 tiles(L.out,[{l:'Recommended',v:kind,c:kind==='Piles'?'warn':'ok'},{l:'Footing size each',v:f1(side),u:'m',s:'if isolated'},{l:'Coverage',v:Math.round(cov*100),u:'%',c:cov>=.5?'warn':'ok'},{l:'Raft pressure',v:f0(qr),u:'kPa',c:qr>q?'bad':'ok',st:qr>q?'Over the safe bearing':'Under it'}].concat(lp?[{l:'Pile length',v:lp,u:'m',s:'to reach hard strata'}]:[]))}
d();
"""),
 dict(h='Load spreads wide as it goes down', p='Under any foundation the pressure fades with depth. A small footing’s influence dies at about twice its width. A big raft reaches many metres deeper.', js=r"""
const L=Lab(H,{h:440,label:'Pressure fading with depth under a foundation',note:'2:1 method for a square foundation: Δσ = q B² / (B + z)². The shaded zone is where pressure is still above 10% of the contact pressure: the zone that matters for settlement.'});
const sB=slider(L.sl,{label:'Foundation width B',min:2,max:60,step:1,value:3,fmt:v=>v+' m',on:d});
const sq=slider(L.sl,{label:'Contact pressure q',min:50,max:500,step:10,value:200,fmt:v=>v+' kPa',on:d});
chips(L.sl,[['Footing 3 m',3],['Pile cap 8 m',8],['Raft 30 m',30],['Large raft 50 m',50]],v=>sB.set(v),undefined,'Quick set');
function d(){const g=L.svg,B=sB.v(),q=sq.v();clear(g);
 const zmax=Math.max(30,B*2.5),P=plot(g,{x0:0,x1:q,y0:zmax,y1:0,xt:5,yt:6,xl:'added pressure, kPa',yl:'depth, m'});
 const dz=z=>q*B*B/((B+z)**2);
 const zi=B*(Math.sqrt(10)-1);const pts=[];for(let z=0;z<=zmax;z+=zmax/100)pts.push([P.X(dz(z)),P.Y(z)]);
 poly(g,[[P.x,P.Y(0)]].concat(pts.filter((p,i)=>i*zmax/100<=zi)).concat([[P.X(dz(zi)),P.Y(zi)],[P.x,P.Y(zi)]]),{class:'f-push'});
 pline(g,pts,'s-thick');
 line(g,P.x,P.Y(zi),P.x+P.w,P.Y(zi),'s-push',{'stroke-dasharray':'7 5'});T(g,P.x+P.w-4,P.Y(zi)-10,'10% depth '+f1(zi)+' m',{'text-anchor':'end','font-size':21,'font-weight':600});
 tiles(L.out,[{l:'10% depth',v:f1(zi),u:'m'},{l:'Ratio to width',v:f1(zi/B),u:'× B'},{l:'Pressure at B',v:f0(dz(B)),u:'kPa',s:'≈ 25% of q'}]);
 L.out.insertAdjacentHTML('beforeend','<p>A footing only “sees” soil for about 2B below it. A tower raft sees tens of metres. Soft clay deep down matters for the raft but not the footing.</p>')}
d();
""")],
 quiz=[dict(q='Footings cover more than half of the building plan. The usual next step is…', o=['Bigger footings','A raft','More columns'], a=1, w='When footings nearly touch, a raft is simpler and uses less excavation and formwork.'),
  dict(q='A deep soft clay layer under a site: which foundation reaches past it?', o=['Isolated footing','Piles to hard strata','Strip footing'], a=1, w='Piles carry load through the weak layers to firmer ground.'),
  dict(q='The influence of a square footing’s load fades to about 10% at what depth?', o=['B','About 2 B','About 5 B'], a=1, w='Near 2B for a square footing. This is why settlement checks look at twice the width below the base.')],
 rules=['Start shallow. Move to a raft, then piles, only when the soil or the loads demand it.','Differential settlement matters more than total settlement. Keep the foundation type uniform within a building.','Check the water table level and rise over the life of the building, including construction dewatering.','Tall towers usually use piled rafts: piles carry most of the load, the raft spreads the rest.'],
 codes=['IS 1904:1986','IS 2950 (rafts)','IS 2911 (piles)','IS 8009 (settlement)']))

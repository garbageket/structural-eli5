CSS = r"""
:root{
  --bg:#EEF1EC; --ink:#1D2925; --muted:#53615B; --line:#C3CBC2; --panel:#E2E8E0;
  --sand:#E6CD98; --sand2:#C6A668; --soil:#A38058; --soil2:#7F613D;
  --conc:#C6CCCA; --conc2:#848E8B; --water:#1A6BA4; --push:#B01E2C; --ok:#2A7842; --warn:#9C5D00; --steel:#2B3A55;
  --pf:.2; --wf:.22; --halo:#EEF1EC;
  color-scheme:light; box-sizing:border-box;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#111715; --ink:#E6ECE7; --muted:#A3B1AA; --line:#2C3833; --panel:#19221F;
    --sand:#3A3122; --sand2:#55472F; --soil:#4D3C29; --soil2:#665037;
    --conc:#4C5553; --conc2:#808B88; --water:#5DB2EE; --push:#FF707A; --ok:#6DCC88; --warn:#F3AE48; --steel:#9DB4E0;
    --pf:.3; --wf:.3; --halo:#111715; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#111715; --ink:#E6ECE7; --muted:#A3B1AA; --line:#2C3833; --panel:#19221F;
  --sand:#3A3122; --sand2:#55472F; --soil:#4D3C29; --soil2:#665037;
  --conc:#4C5553; --conc2:#808B88; --water:#5DB2EE; --push:#FF707A; --ok:#6DCC88; --warn:#F3AE48; --steel:#9DB4E0;
  --pf:.3; --wf:.3; --halo:#111715; color-scheme:dark;
}
*,*::before,*::after{box-sizing:inherit}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Barlow',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:1.0625rem;line-height:1.55;-webkit-font-smoothing:antialiased}
main{max-width:1140px;margin:0 auto;padding:0 1.25rem 4rem}
h1,h2,h3,.big{font-family:'Barlow Condensed','Arial Narrow',system-ui,sans-serif;font-weight:700;letter-spacing:-.01em;line-height:1.04;margin:0}
h1{font-size:clamp(2.6rem,7.5vw,5.6rem);max-width:15ch}
h2{font-size:clamp(2rem,4.6vw,3.2rem);max-width:22ch}
h3{font-size:1.4rem;font-weight:600}
p{margin:.6rem 0 0;max-width:64ch}
sub{font-size:.72em;line-height:0} sup{font-size:.72em;line-height:0}
.lede{font-size:1.25rem;color:var(--muted);max-width:46ch;margin-top:1rem}
section{padding:4rem 0 0}
.note{color:var(--muted);font-size:.95rem}
a{color:var(--ink)}
svg{display:block;width:100%;height:auto}
svg text{font-family:'Barlow',system-ui,sans-serif;fill:var(--ink);paint-order:stroke;stroke:var(--halo);stroke-width:5px;stroke-linejoin:round}
figure{margin:0}
.top{display:flex;justify-content:space-between;align-items:center;gap:1rem;padding-top:1.1rem;flex-wrap:wrap}
.top a.back{font-weight:600;text-decoration:none;border:1.5px solid var(--line);border-radius:999px;padding:.3rem .9rem;font-size:.95rem}
.top a.back:hover{border-color:var(--ink)}
.kick{color:var(--muted);font-weight:600;font-size:.95rem;margin-top:1.6rem;letter-spacing:.02em}
.seg{display:inline-flex;border:1.5px solid var(--line);border-radius:999px;padding:3px;gap:2px}
.seg button{font:inherit;font-size:.9rem;border:0;background:transparent;color:var(--ink);padding:.3rem .8rem;border-radius:999px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
/* fills & strokes */
.f-sand{fill:url(#dots)} .f-clay{fill:url(#clay)}
.f-conc{fill:url(#conc);stroke:var(--conc2);stroke-width:1.5}
.f-slab{fill:var(--panel);stroke:var(--line);stroke-width:1.5}
.f-gravel{fill:url(#gravel)}
.f-push{fill:var(--push);fill-opacity:var(--pf);stroke:var(--push);stroke-width:2}
.f-water{fill:var(--water);fill-opacity:var(--wf);stroke:var(--water);stroke-width:2}
.f-ok{fill:var(--ok);fill-opacity:var(--pf);stroke:var(--ok);stroke-width:2}
.f-warn{fill:var(--warn);fill-opacity:var(--pf);stroke:var(--warn);stroke-width:2}
.f-steel{fill:var(--steel)} .f-ink{fill:var(--ink)} .f-pushs{fill:var(--push)} .f-oks{fill:var(--ok)} .f-warns{fill:var(--warn)} .f-waters{fill:var(--water)} .f-none{fill:none}
.s-push{stroke:var(--push);stroke-width:2.5;fill:none}
.s-water{stroke:var(--water);stroke-width:2.5;fill:none}
.s-ok{stroke:var(--ok);stroke-width:2.5;fill:none}
.s-warn{stroke:var(--warn);stroke-width:2.5;fill:none}
.s-ink{stroke:var(--ink);stroke-width:1.8;fill:none}
.s-thick{stroke:var(--ink);stroke-width:4;fill:none}
.s-beam{stroke:var(--conc2);stroke-width:6;fill:none;stroke-linecap:round}
.s-muted{stroke:var(--muted);stroke-width:1.6;fill:none;stroke-dasharray:6 5}
.s-grid{stroke:var(--line);stroke-width:1;fill:none}
.s-steel{stroke:var(--steel);stroke-width:3.5;fill:none;stroke-linecap:round}
.ghost{fill:none;stroke:var(--muted);stroke-width:1.8;stroke-dasharray:6 5}
/* layout */
.lab{display:grid;gap:1.6rem 2.4rem;grid-template-columns:minmax(0,1.7fr) minmax(0,1fr);margin-top:2rem;align-items:start}
.lab+.lab{margin-top:3rem}
.ctl{display:grid;gap:1.2rem;align-content:start}
.sls{display:grid;gap:1.1rem}
.sl .slh{display:flex;justify-content:space-between;align-items:baseline;gap:1rem}
.sl label{font-weight:600;font-size:1.02rem}
.sl output{font-variant-numeric:tabular-nums;font-weight:600;color:var(--push);white-space:nowrap}
input[type=range]{width:100%;accent-color:var(--push);height:2rem;margin:.1rem 0 0;cursor:pointer}
.cl{font-weight:600;font-size:1.02rem;margin-bottom:.1rem}
.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.35rem}
.btn,.chips button{font:inherit;font-size:.92rem;padding:.4rem .85rem;border:1.5px solid var(--line);background:transparent;color:var(--ink);border-radius:999px;cursor:pointer}
.btn:hover,.chips button:hover{border-color:var(--ink)}
.btn.solid{background:var(--ink);color:var(--bg);border-color:var(--ink);font-weight:600}
.chips button[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.chk{display:flex;gap:.6rem;align-items:center;font-weight:500;cursor:pointer}
.chk input{width:1.15rem;height:1.15rem;accent-color:var(--push)}
:focus-visible{outline:3px solid var(--water);outline-offset:2px}
.metrics{display:grid;gap:1rem 1.2rem;grid-template-columns:repeat(auto-fit,minmax(128px,1fr))}
.m{border-top:4px solid var(--line);padding-top:.5rem}
.m.ok{border-color:var(--ok)} .m.bad{border-color:var(--push)} .m.warn{border-color:var(--warn)}
.m .lbl{font-size:.9rem;color:var(--muted);font-weight:500}
.m .val{font-family:'Barlow Condensed',sans-serif;font-size:2.1rem;font-weight:700;line-height:1.05;font-variant-numeric:tabular-nums}
.m .val small{font-size:.95rem;font-weight:500;color:var(--muted);margin-left:.25rem}
.m .st{font-size:.9rem;font-weight:600}
.m.ok .st{color:var(--ok)} .m.bad .st{color:var(--push)} .m.warn .st{color:var(--warn)}
.m .sb{font-size:.85rem;color:var(--muted)}
.bars{display:grid;gap:.5rem}
.bar{display:grid;grid-template-columns:8.2rem 1fr 3.2rem;align-items:center;gap:.6rem;font-size:.93rem}
.bar i{display:block;height:.8rem;background:var(--line);border-radius:2px;position:relative;overflow:hidden}
.bar i b{position:absolute;inset:0 auto 0 0;background:var(--muted);border-radius:2px}
.bar.push i b{background:var(--push)} .bar.ok i b{background:var(--ok)} .bar.warn i b{background:var(--warn)} .bar.water i b{background:var(--water)}
.bar span:last-child{text-align:right;font-variant-numeric:tabular-nums}
.bar.on{font-weight:600}
.said{font-family:'Barlow Condensed',sans-serif;font-size:1.7rem;font-weight:600;line-height:1.15;max-width:26ch}
.hints{margin:.2rem 0 0;padding:0;list-style:none;display:grid;gap:.35rem}
.hints li{padding-left:1.1rem;position:relative;max-width:70ch}
.hints li::before{content:"";position:absolute;left:0;top:.62em;width:.5rem;height:.5rem;border-radius:50%;background:var(--push)}
.hints li.good::before{background:var(--ok)}
.step{border:1.5px solid var(--line);border-radius:10px;padding:.5rem .8rem;transition:background .25s,border-color .25s}
.step.on{border-color:var(--push);background:var(--panel)}
/* quiz */
.q{border-top:1px solid var(--line);padding:1rem 0}
.q h3{font-size:1.35rem;margin-bottom:.6rem;max-width:34ch}
.opts{display:flex;flex-wrap:wrap;gap:.5rem}
.opts .btn{border-radius:10px;text-align:left}
.opts .btn.right{border-color:var(--ok);box-shadow:inset 0 0 0 1.5px var(--ok)}
.opts .btn.right::before{content:"✓ "}
.opts .btn.wrong{border-color:var(--push);box-shadow:inset 0 0 0 1.5px var(--push)}
.opts .btn.wrong::before{content:"✗ "}
.why{margin:.6rem 0 0}
.score{font-weight:600;margin-top:.8rem}
/* lists */
.rules{margin:1.5rem 0 0;padding:0;list-style:none;display:grid;gap:0}
.rules li{display:grid;grid-template-columns:2.2rem 1fr;gap:.8rem;padding:.8rem 0;border-top:1px solid var(--line);max-width:70ch}
.rules li:last-child{border-bottom:1px solid var(--line)}
.rules li b.n{font-family:'Barlow Condensed',sans-serif;font-size:1.7rem;color:var(--push);line-height:1}
.codes{margin:1.2rem 0 0;display:flex;flex-wrap:wrap;gap:.5rem;padding:0;list-style:none}
.codes li{border:1.5px solid var(--line);border-radius:999px;padding:.25rem .8rem;font-size:.92rem}
.tbl{overflow-x:auto;margin-top:1.2rem}
table{border-collapse:collapse;width:100%;min-width:480px;font-size:.98rem}
th,td{text-align:left;padding:.55rem .8rem .55rem 0;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:.9rem}
footer{max-width:1140px;margin:0 auto;padding:2rem 1.25rem 3rem;color:var(--muted);font-size:.92rem;border-top:1px solid var(--line)}
footer a{font-weight:600}
@media (max-width:860px){.lab{grid-template-columns:1fr}}
"""

import json, os, sys, importlib
from lib_css import CSS
from lib_js import JS

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600&family=Barlow+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>%(css)s</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <defs>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><rect width="16" height="16" style="fill:var(--sand)"/><circle cx="4" cy="4" r="1.5" style="fill:var(--sand2)"/><circle cx="12" cy="11" r="1.1" style="fill:var(--sand2)"/><circle cx="9" cy="2" r=".8" style="fill:var(--sand2)"/></pattern>
    <pattern id="clay" width="18" height="10" patternUnits="userSpaceOnUse"><rect width="18" height="10" style="fill:var(--soil)"/><line x1="2" y1="5" x2="10" y2="5" style="stroke:var(--soil2);stroke-width:1.4"/></pattern>
    <pattern id="conc" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="10" height="10" style="fill:var(--conc)"/><line x1="0" y1="0" x2="0" y2="10" style="stroke:var(--conc2);stroke-width:1.2"/></pattern>
    <pattern id="gravel" width="20" height="20" patternUnits="userSpaceOnUse"><rect width="20" height="20" style="fill:var(--conc)"/><circle cx="5" cy="5" r="3.6" style="fill:var(--bg);stroke:var(--conc2);stroke-width:1"/><circle cx="15" cy="13" r="4.2" style="fill:var(--bg);stroke:var(--conc2);stroke-width:1"/></pattern>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--push)"/></marker>
    <marker id="ahw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--water)"/></marker>
    <marker id="ahk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ink)"/></marker>
    <marker id="aho" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--ok)"/></marker>
  </defs>
</svg>
<main>
<div class="top"><a class="back" href="eli5-index.html">← All topics</a>
<div class="seg" role="group" aria-label="Colour theme"><button type="button" data-th="auto" aria-pressed="true">Auto</button><button type="button" data-th="light" aria-pressed="false">Light</button><button type="button" data-th="dark" aria-pressed="false">Dark</button></div></div>
"""

def build_page(p):
    n = p['n']
    h = HEAD % dict(title=p['title'], css=CSS)
    h += '<div class="kick">%02d · %s</div>\n<h1>%s</h1>\n<p class="lede">%s</p>\n' % (n, p['group'], p['title'], p['lede'])
    js = []
    for i, s in enumerate(p['sections']):
        h += '<section><h2>%s</h2><p>%s</p><div id="h%d"></div></section>\n' % (s['h'], s['p'], i)
        js.append('try{(function(H){\n%s\n})($("h%d"))}catch(e){console.error("section %d",e)}' % (s['js'], i, i))
    if p.get('quiz'):
        h += '<section><h2>Check yourself</h2><div id="hq"></div></section>\n'
        js.append('quiz($("hq"),%s);' % json.dumps(p['quiz']))
    if p.get('rules'):
        h += '<section><h2>Keep in mind</h2><ul class="rules">' + ''.join('<li><b class="n">%d</b><span>%s</span></li>' % (i+1, r) for i, r in enumerate(p['rules'])) + '</ul>'
        if p.get('codes'):
            h += '<ul class="codes">' + ''.join('<li>%s</li>' % c for c in p['codes']) + '</ul>'
        h += '</section>\n'
    h += '</main>\n<footer>For learning and quick sense-checks. Design from the project design basis, the geotechnical report and the governing codes. <a href="eli5-index.html">All topics</a></footer>\n<script>\n' + JS + '\n' + '\n'.join(js) + '\n</script>\n</body></html>\n'
    return h

def fname(p):
    return 'eli5-%02d-%s.html' % (p['n'], p['slug'])

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    mods = sys.argv[2:]
    for m in mods:
        mod = importlib.import_module(m)
        for p in mod.PAGES:
            open(os.path.join(out, fname(p)), 'w').write(build_page(p))
            print('built', fname(p))

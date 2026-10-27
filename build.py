import os, html
from cities import C, CHECKED, CHECKED_BY
NCITY=len(C)
BASE = os.environ.get("BASE","https://nater79.github.io/mattress-couch-disposal-guide")
OUT="site"; os.makedirs(OUT,exist_ok=True)
SITE="Bulky Item Guide"
CONTACT="navexiateam [at] navexia [dot] net"  # FLAG: Nate must supply a real contact address
# PAID: slot name -> dict(kind="Sponsored"|"Affiliate link", url=..., text=...). Fill only with real, approved deals.
PAID={}
BANNED=("recommended","best","top-rated","#1")
SLOTS=["top-banner","footer-ad","hauler-referral","featured-local-hauler","mattress-brand-haulaway"]
# Visible, honest placeholders for empty slots (no businesses, no links). Remove an entry to hide that slot.
# Counsel Fix first 2026-10-25: visible placeholders hidden. Kept for later, re-enable only after Counsel clears:
# PLACEHOLDER={
#  "featured-local-hauler":("Featured hauler spot &mdash; available","This space is empty. No business is featured here and no one has paid us. If a hauler is ever listed here, it will be labeled Sponsored and will not change the city rules above."),
#  "mattress-brand-haulaway":("Affiliate disclosure &mdash; placeholder","No affiliate links on this page yet. Any future affiliate link will carry an Affiliate link label right next to it."),
# }
PLACEHOLDER={}
def SLOT(name):
    p=PAID.get(name)
    if not p:
        ph=PLACEHOLDER.get(name)
        if ph: return f'<div class="slot slot-open" data-slot="{name}"><span class="label label-open">{ph[0]}</span><p>{ph[1]}</p></div>'
        return f'<div class="slot" data-slot="{name}"><!-- MONETIZATION SLOT: {name}. Empty. --></div>'
    assert p["kind"] in ("Sponsored","Affiliate link")
    assert not any(w in p["text"].lower() for w in BANNED), "paid placements may not be called recommended/best"
    note="We earn a fee if you book through this link." if p["kind"]=="Affiliate link" else "This business paid to be listed here. We do not rate or review it."
    return f'<div class="slot paid" data-slot="{name}"><span class="label label-paid">{p["kind"]}</span> <a href="{p["url"]}" rel="sponsored nofollow noopener">{p["text"]}</a> <small>{note}</small></div>'
def disc():
    n=sum(1 for k in SLOTS if PAID.get(k))
    state="Right now this page has no paid links, ads, or sponsored listings." if n==0 else f"This page has {n} paid placement(s), each labeled Sponsored or Affiliate link right next to it."
    return ('<aside class="disc" id="ftc-disclosure"><strong>Disclosure:</strong> This site may earn money from clearly labeled ads, affiliate links, or sponsored listings. '
            f'Paid placements never change what the city rules say. {state}</aside>')

# --- Redesign helpers: hand-drawn SVG art (no outside assets) ---
SKY="""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 300" role="img" aria-label="Drawing of a city skyline with a small truck"><rect width="640" height="300" fill="#e8f6f4"/><circle cx="520" cy="70" r="34" fill="#ffd36e"/><g fill="#b9e3dd"><rect x="20" y="120" width="60" height="140"/><rect x="90" y="80" width="50" height="180"/><rect x="150" y="140" width="70" height="120"/><rect x="230" y="60" width="44" height="200"/><rect x="284" y="110" width="66" height="150"/><rect x="360" y="90" width="40" height="170"/><rect x="410" y="130" width="80" height="130"/><rect x="500" y="100" width="54" height="160"/><rect x="564" y="140" width="60" height="120"/></g><g fill="#fff" opacity=".8"><rect x="100" y="95" width="10" height="12"/><rect x="120" y="95" width="10" height="12"/><rect x="100" y="120" width="10" height="12"/><rect x="240" y="80" width="8" height="12"/><rect x="256" y="80" width="8" height="12"/><rect x="240" y="104" width="8" height="12"/><rect x="368" y="110" width="8" height="12"/><rect x="384" y="110" width="8" height="12"/><rect x="512" y="120" width="10" height="12"/><rect x="530" y="120" width="10" height="12"/></g><rect y="258" width="640" height="42" fill="#0f766e"/><rect y="276" width="640" height="4" fill="#fff" opacity=".5"/><g transform="translate(190 186)"><rect x="0" y="10" width="150" height="62" rx="6" fill="#14b8a6"/><path d="M150 30h42l26 26v16h-68z" fill="#0d9488"/><path d="M160 36h28l18 18h-46z" fill="#e8f6f4"/><rect x="20" y="24" width="40" height="30" rx="3" fill="#fff" opacity=".9"/><rect x="70" y="30" width="60" height="24" rx="3" fill="#fff" opacity=".7"/><circle cx="40" cy="76" r="14" fill="#1f2937"/><circle cx="40" cy="76" r="6" fill="#e5e7eb"/><circle cx="180" cy="76" r="14" fill="#1f2937"/><circle cx="180" cy="76" r="6" fill="#e5e7eb"/></g></svg>"""
ICONS={
 "heart":'<path d="M12 21s-7-4.5-9.5-9A5 5 0 0 1 12 6a5 5 0 0 1 9.5 6C19 16.5 12 21 12 21z"/>',
 "doc":'<path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h7M9 8h4"/>',
 "cal":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "truck":'<path d="M2 7h12v9H2zM14 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 "pin":'<path d="M12 22s7-7 7-12a7 7 0 0 0-14 0c0 5 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>'}
def ico(n): return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[n]}</svg>'
def cards(items): return '<ul class="cards">'+"".join(f'<li class="card"><span class="ico-wrap">{ico(i)}</span><strong>{t}</strong><span>{d}</span></li>' for i,t,d in items)+'</ul>'
# Hero image slots: drop a file at site-src/img/<name> and it replaces the SVG drawing.
def hero_art(fn):
    name={"index.html":"hero-home.webp","junk-removal-springfield-ozark-mo.html":"hero-junk.webp"}.get(fn)
    src=os.path.join(os.path.dirname(os.path.abspath(__file__)),"img",name) if name else None
    if src and os.path.exists(src):
        os.makedirs(f"{OUT}/img",exist_ok=True); shutil.copy(src,f"{OUT}/img/{name}")
        return f'<img class="hero-img" src="img/{name}" width="1200" height="800" alt="" loading="eager">'
    return '<img class="hero-img" src="img/skyline.svg" width="640" height="300" alt="">'
def herofy(fn,body):
    m=re.match(r'\s*(<h1>.*?</h1>)\s*(<p class="lede">.*?</p>)?',body,re.S)
    if not m: return body
    return f'<section class="hero"><div class="hero-text">{m.group(1)}{m.group(2) or ""}</div><div class="hero-art">{hero_art(fn)}</div></section>'+body[m.end():]
CSS=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"design.css")).read()
import json as _json, re, shutil, html as _html
# Security headers (Counsel rule 14) - keep on every page. No inline styles/scripts allowed; JSON-LD is data, not executed.
HEAD_SEC=("<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'\">"
          '<meta name="referrer" content="strict-origin-when-cross-origin">')
ROOT=BASE.rstrip("/")+"/"
def jsonld(fn,title):
    if fn=="index.html":
        d={"@context":"https://schema.org","@type":"WebSite","name":_html.unescape(SITE),"url":ROOT,"inLanguage":"en-US"}
    else:
        crumb="About" if fn=="about.html" else _html.unescape(title.split(" in ",1)[-1].split(" (")[0])
        d={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
           {"@type":"ListItem","position":1,"name":_html.unescape(SITE),"item":ROOT},
           {"@type":"ListItem","position":2,"name":crumb,"item":ROOT+fn}]}
    return '<script type="application/ld+json">'+_json.dumps(d).replace("</","<\\/")+'</script>'
def crumbs(fn,title):
    if fn=="index.html": return ""
    name="About" if fn=="about.html" else title.split(" in ",1)[-1].split(" (")[0]
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li><li aria-current="page">{name}</li></ol></nav>'
GSV='<meta name="google-site-verification" content="jSNJgTCUMSGQc1nbqHnKFmYa5zyTqizhnxAj2pmnIpA">'  # Nate's Search Console verification
MOD={}  # fn -> dateModified (real last-checked date)
REL={}  # fn -> related-links html
def og(fn,title,desc,canon):
    img=ROOT+"img/og.png"
    t=_html.escape(_html.unescape(title),quote=True); d=_html.escape(_html.unescape(desc),quote=True)
    return (f'<meta property="og:type" content="{"website" if fn=="index.html" else "article"}"><meta property="og:site_name" content="{SITE}">'
            f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{canon}">'
            f'<meta property="og:image" content="{img}"><meta property="og:image:alt" content="Bulky Item Guide logo"><meta name="twitter:card" content="summary_large_image">')
def article(fn,title,desc,canon):
    if fn not in MOD: return ""
    d={"@context":"https://schema.org","@type":"Article","headline":_html.unescape(title)[:110],"description":_html.unescape(desc),
       "dateModified":MOD[fn],"mainEntityOfPage":canon,"inLanguage":"en-US","image":ROOT+"img/og.png",
       "author":{"@type":"Organization","name":_html.unescape(SITE),"url":ROOT},"publisher":{"@type":"Organization","name":_html.unescape(SITE),"url":ROOT}}
    return '<script type="application/ld+json">'+_json.dumps(d).replace("</","<\\/")+'</script>'
def page(fn,title,desc,body):
    body=herofy(fn,body)+REL.get(fn,"")
    canon=ROOT if fn=="index.html" else ROOT+fn
    open(f"{OUT}/{fn}","w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{HEAD_SEC}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}"><link rel="stylesheet" href="style.css"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png"><link rel="apple-touch-icon" sizes="180x180" href="img/favicon-180.png">{GSV if fn=="index.html" else ""}{og(fn,title,desc,canon)}{jsonld(fn,title)}{article(fn,title,desc,canon)}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap bar"><a class="brand" href="index.html"><picture><source srcset="img/logo-header.webp" type="image/webp"><img class="brand-logo" src="img/logo-header.png" width="98" height="40" alt="Bulky Item Guide"></picture></a>
<nav aria-label="Main"><ul class="nav"><li><a href="index.html#cities"{' aria-current="page"' if fn=="index.html" else ''}>Find your city</a></li><li><a href="junk-removal-springfield-ozark-mo.html">Junk removal: Springfield &amp; Ozark</a></li><li><a href="how-to-videos.html">How-to videos</a></li><li><a href="about.html"{' aria-current="page"' if fn=="about.html" else ''}>About &amp; how we check</a></li></ul></nav></div></header>
<div class="wrap">{crumbs(fn,title)}{disc()}{SLOT('top-banner')}<main id="main" class="{'home' if fn=='index.html' else 'content'}">{body}</main>{SLOT('footer-ad')}</div>
<footer class="site-footer"><div class="wrap"><p class="foot-brand"><img class="foot-logo" src="img/favicon-32.png" width="24" height="24" alt=""> {SITE}</p><p><strong>Not affiliated with any city government. Rules change; check with your city before you act.</strong> Information may be out of date or wrong. We are not responsible for fines or missed pickups. Always confirm with your city.</p><p>Found a mistake? Contact us: {CONTACT}</p>{disc()}<p class="foot-nav"><a href="index.html">{SITE}</a> &middot; <a href="about.html">About &amp; how we check</a> &middot; <a href="sitemap.xml">Sitemap</a></p></div></footer></body></html>""")
open(f"{OUT}/style.css","w").write(CSS)
os.makedirs(f"{OUT}/img",exist_ok=True); open(f"{OUT}/img/skyline.svg","w").write(SKY)
_I=os.path.join(os.path.dirname(os.path.abspath(__file__)),"img")
for _f in ("og.png","logo-header.webp","logo-header.png","favicon-32.png","favicon-180.png"): shutil.copy(os.path.join(_I,_f),f"{OUT}/img/{_f}")
shutil.copy(os.path.join(_I,"favicon.ico"),f"{OUT}/favicon.ico")
DON="""<section class="step donate"><h2>Step 1: Can someone else use it? Donate first</h2>
<p>If your couch or mattress is clean and in good shape, giving it away helps a neighbor and keeps it out of the landfill.</p>
<ul><li>Offer it free to neighbors (Buy Nothing groups, Nextdoor, Facebook Marketplace, Craigslist "free").</li>
<li>Call a local thrift store, church, shelter, or furniture bank. Ask if they take it and if they pick up.</li>
<li><strong>Call first.</strong> Many charities do not take used mattresses.</li>{extra}</ul></section>"""
urls=["index.html","about.html"]
rows=""
for slug,name,st,pop,agency,src,rules,notes in C:
    CK=CHECKED_BY.get(slug,CHECKED)
    fn=f"{slug}.html"; urls.append(fn)
    ex="".join(f"<li>{n}</li>" for n in notes if "Bye Bye" in n)
    rl="".join(f"<li>{r}</li>" for r in rules)
    other="".join(f'<p class="check">{n}</p>' for n in notes if "Bye Bye" not in n)
    status="Partly verified" if (not rules or other) else "Verified on official page"
    body=f"""<h1>How to get rid of a mattress or couch in {name}, {st}</h1>
<div class="glance"><div><span class="k">Official source</span><a href="{src}" rel="nofollow">{agency}</a></div><div><span class="k">Last checked</span><time datetime="{CK}">{CK}</time></div><div><span class="k">Status</span><span class="pill {'pill-warn' if status!='Verified on official page' else 'pill-ok'}">{status}</span></div></div>
{cards([("heart","Donate first","Help a neighbor"),("doc","Official rules","Linked source"),("cal","Last checked","Dated every page"),("truck","Hauler options","Ask for a written price")])}
{DON.format(extra=ex)}
<section class="step step-city"><h2>Step 2: City pickup and drop-off rules</h2>
{'<ul>'+rl+'</ul>' if rules else ''}{other}
<p>Anything not listed here: <strong>check with the city</strong>. We only list rules we could confirm on an official page.</p>
<p><strong>Official source:</strong> <a href="{src}" rel="nofollow">{agency}</a><br><strong>Last checked:</strong> {CK}</p>
</section><section class="step step-other"><h2>Step 3: Other options</h2>
<p>If the city cannot help, you can hire a licensed hauler. Ask for a written price first. Never pay someone who might dump it illegally.</p>
{SLOT('hauler-referral')}{SLOT('featured-local-hauler')}{SLOT('mattress-brand-haulaway')}</section>"""
    MOD[fn]=CK
    near=[c for c in C if c[2]==st and c[0]!=slug][:3] or []
    others=near+[c for c in C if c[0]!=slug and c not in near][:max(0,4-len(near))]
    REL[fn]='<nav class="related" aria-label="Related pages"><h2>Other city guides</h2><ul>'+"".join(f'<li><a href="{c[0]}.html">Mattress and couch disposal in {c[1]}, {c[2]}</a></li>' for c in others[:4])+'<li><a href="junk-removal-springfield-ozark-mo.html">Junk removal in Springfield and Ozark, MO</a></li></ul></nav>'
    page(fn,f"Get rid of a mattress or couch in {name} ({CK[:4]} city rules)",f"Free and low-cost ways to get rid of a mattress or couch in {name}: donate first, then official city pickup rules with a source link.",body)
    rows+=f'<li><a class="city" href="{fn}"><span class="cname">{name}, {st}</span>{"" if rules and not other else " <span class=\'pill pill-warn\'>(partly verified)</span>"}</a></li>'
# --- Junk removal page: Springfield / Ozark, MO. Every fact read on the linked page on JCHECK. ---
JCHECK="2026-10-26"
SGF_M="https://www.springfieldmo.gov/5939/Mattress-Recycling"
SGF_R="https://www.springfieldmo.gov/recycling"
SGF_L="https://www.springfieldmo.gov/486/Noble-Hill-Sanitary-Landfill"
SGF_LG="https://www.springfieldmo.gov/DocumentCenter/View/3101/Springfield-Sanitary-Landfill-PDF"
SGF_C="https://www.springfieldmo.gov/5555/Curbside-Trash-Recycling"
OZ_B="https://www.ozarkmissouri.com/138/Trash-and-Recycling-Billing-Information"
OZ_C="https://www.ozarkmissouri.com/107/Code-Compliance"
REP="https://www.republicservices.com/residents/recycling-and-solid-waste/bulk-waste"
def S(u,t): return f' <a class="src" href="{u}" rel="nofollow">({t})</a>'
JFN="junk-removal-springfield-ozark-mo.html"; urls.append(JFN)
jbody=f"""<h1>Junk removal in Springfield and Ozark, Missouri</h1>
<p class="lede">Need to get rid of an old couch, mattress, or a pile of junk? Here are the real options near Springfield and Ozark, with fees, addresses, and hours from official pages. Cheapest options come first.</p>
<div class="glance"><div><span class="k">Sources</span>City of Springfield, City of Ozark, Republic Services</div><div><span class="k">Last checked</span><time datetime="{JCHECK}">{JCHECK}</time></div><div><span class="k">Status</span><span class="pill pill-ok">Checked on official pages</span></div></div>
{cards([("heart","Give it away","Free and kind"),("pin","Drop-off sites","Hours and addresses"),("doc","Real fees","From city pages"),("truck","Hire a hauler","Get a price first")])}
<section class="step donate"><h2>Step 1: Can someone else use it? Give it away first</h2>
<ul><li>Offer good items free to neighbors (Buy Nothing groups, Nextdoor, Facebook Marketplace, Craigslist "free").</li>
<li>Call a local thrift store, church, or shelter and ask if they take it and if they pick up. <strong>Call first.</strong> Many charities do not take used mattresses.</li></ul></section>
<section class="step step-city"><h2>Step 2: Springfield rules and drop-off sites</h2>
<ul><li><strong>No city curbside junk pickup.</strong> Trash in Springfield is picked up by more than 10 private, licensed hauling companies. Ask your own hauler about bulky items.{S(SGF_C,"City of Springfield")}</li>
<li><strong>Mattresses and box springs: $20 per piece</strong>, any size. They are recycled (through a contract with Victory Mission), not buried. They must be clean, dry, and free of bugs. Wet or heavily soiled ones are refused.{S(SGF_M,"Mattress Recycling page")}</li>
<li>Mattress drop-off sites:{S(SGF_M,"same page")}
<ul><li>Lone Pine Avenue Recycling Center, 3020 S. Lone Pine Ave. Tuesday&ndash;Saturday, 8 a.m.&ndash;4:30 p.m.</li>
<li>Franklin Avenue Recycling Center, 731 N. Franklin Ave. Tuesday&ndash;Saturday, 8 a.m.&ndash;4:30 p.m.</li>
<li>Noble Hill Sanitary Landfill, 3545 W. Farm Road 34, Willard. Monday&ndash;Friday 7 a.m.&ndash;3:30 p.m.; Saturday 7 a.m.&ndash;2:30 p.m.</li></ul></li>
<li><strong>Couches, furniture, and other junk:</strong> the Noble Hill Sanitary Landfill charges <strong>$43.85 per ton, with a $20 minimum</strong> per vehicle. It takes cash, check, and cards.{S(SGF_L,"Landfill page")} Small loads you unload by hand go to the Small Load Drop-off. Phone 417-742-3536.{S(SGF_LG,"Landfill guide")}</li>
<li><strong>Recycling centers</strong> (cans, cardboard, glass, paper, plastic, yard waste) are free, with donations welcome. They are generally open Tuesday&ndash;Saturday, 8 a.m.&ndash;5 p.m. Franklin Avenue and Lone Pine take only cash or check.{S(SGF_R,"Recycling Centers page")}</li></ul></section>
<section class="step step-city"><h2>Step 3: Ozark rules</h2>
<ul><li>Ozark lets you pick any trash company. The city partners with <strong>Republic Services</strong> and puts that bill on your water bill. Republic customer service: 800-627-1717.{S(OZ_B,"City of Ozark")}</li>
<li>Republic Services offers bulk pickup in some areas. It asks you to wrap mattresses in plastic, leave sofas and chairs in one piece, and take doors off fridges and washers. Ask them if it is offered at your address and what it costs.{S(REP,"Republic Services")}</li>
<li>Do not leave junk in the yard. Ozark's code says furniture, appliances, and other junk must be properly disposed of. Questions: 417-581-2407.{S(OZ_C,"Ozark Code Compliance")}</li></ul>
<p class="check">We could not find a current Ozark citywide cleanup date on an official page. Please call the city to ask.</p></section>
<section class="step step-other"><h2>Step 4: Hire a junk removal company</h2>
<p>If you can't haul it yourself, a company can load it for you. Get a written price first. Never pay someone who might dump it illegally. Not every company serves every town, so check your ZIP code on their site.</p>
<ul><li><a href="https://www.1800gotjunk.com/us_en" rel="nofollow">1-800-GOT-JUNK?</a></li><li><a href="https://goloadup.com/" rel="nofollow">LoadUp</a></li><li><a href="https://www.collegehunkshaulingjunk.com/" rel="nofollow">College HUNKS Hauling Junk &amp; Moving</a></li><li><a href="https://www.angi.com/" rel="nofollow">Angi</a> (to compare local pros)</li></ul>
<p><small>Listed in no special order. These are plain links, not affiliate links. No one paid to be here, and we have not used or tested these companies. If we ever earn money from a link, it will carry an "Affiliate link" label right next to it.</small></p>
{SLOT('hauler-referral')}</section>
<p>Anything not listed here: <strong>check with the city or your hauler</strong>. Fees and hours change. Last checked {JCHECK}.</p>"""
MOD[JFN]=JCHECK
REL[JFN]='<nav class="related" aria-label="Related pages"><h2>Related guides</h2><ul><li><a href="index.html#cities">Mattress and couch rules in the 25 biggest US cities</a></li><li><a href="about.html">How we check our facts</a></li></ul></nav>'
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"local_pages.py")).read())
page(JFN,f"Junk removal in Springfield and Ozark, MO ({JCHECK[:4]} fees and drop-off sites)","How to get rid of junk, couches, and mattresses in Springfield and Ozark, Missouri: drop-off sites, hours, fees, and pickup options, with official sources.",jbody)

page("index.html",f"{SITE}: get rid of a mattress or couch in your city","How to get rid of a mattress or couch in the 25 biggest US cities. Donate first, then official city rules with sources.",
 f"<h1>Get rid of your old mattress or couch, the right way</h1><p class=\"lede\">Every city has different rules. Pick your city. Each page starts with donation ideas, then shows the city's own rules with a link to the official page and the date we checked it.</p><p class='ctas'><a class='btn' href='#cities'>Find my city's rules</a> <a class='btn btn-ghost' href='junk-removal-springfield-ozark-mo.html'>New: Junk removal in Springfield &amp; Ozark, MO</a></p>{cards([('doc','Official rules','Linked on every page'),('cal','Last checked','Date on every page'),('shield','No paid rankings','No reviews or ratings'),('heart','Donate first','Keep it out of the landfill')])}<section id='cities' aria-labelledby='cities-h'><h2 id='cities-h' class='sr-only'>Cities</h2><ul class='city-grid'>{rows}</ul><p class='note'>Cities are the {NCITY} largest in the US by 2023 Census Bureau population estimates.</p></section>")
page("about.html",f"About {SITE}","How the Bulky Item Guide checks city rules: official sources only, a last-checked date on every page, and clear labels on any paid link.",f"""<h1>About this guide and how we check it</h1>
<p>We want to make it easy to do the right thing with old furniture: give it away if you can, and follow city rules if you can't. That helps neighbors and cuts down on illegal dumping.</p>
<h2>How we check</h2><ul><li>Every rule comes from an official city (or city-contracted) web page. We link to it.</li>
<li>Each page shows the date we last checked it.</li><li>If we could not confirm a rule, we leave it out and tell you to check with the city. We never guess.</li>
<li>We do not post reviews or ratings.</li></ul>
<h2>Money and honesty</h2><p>This site may later earn money from clearly labeled ads, affiliate links, or labeled "featured" listings. Paid content will always be marked and will never change the city rules we show. This follows the FTC's rules on endorsements.</p>
<h2>Found a mistake?</h2><p>Please tell us: {CONTACT}. City rules change often.</p><h2>Paid links</h2><p>Every paid link will carry a visible Sponsored or Affiliate link label right next to it. We will not praise a business just because it paid us.</p>""")
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{ROOT if u=='index.html' else BASE+'/'+u}</loc><lastmod>{MOD.get(u,CHECKED)}</lastmod></url>" for u in urls)+"</urlset>\n")
open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
INDEXNOW_KEY="b7e4c1a9d2f84e6a9c3b5d7f1e2a4c6b"  # public by design (IndexNow protocol); not a secret
open(f"{OUT}/{INDEXNOW_KEY}.txt","w").write(INDEXNOW_KEY)
open(f"{OUT}/indexnow-urls.txt","w").write("\n".join(ROOT if u=="index.html" else f"{BASE}/{u}" for u in urls)+"\n")
print(len(urls),"pages")
# Guard (Counsel rule 14): fail the build if any page lacks the security/SEO head tags or uses inline style/script/forms.
import glob as _g, re as _re
for _f in _g.glob(f"{OUT}/*.html"):
    _h=open(_f).read()
    assert "Content-Security-Policy" in _h and "script-src 'none'" in _h and 'name="referrer"' in _h and 'rel="canonical"' in _h and "application/ld+json" in _h, f"missing head tags: {_f}"
    assert _h.count("<title>")==1 and 'property="og:title"' in _h, f"missing title/og: {_f}"
    assert not _re.search(r'style=|<style|<form|<iframe|<script(?! type="application/ld\+json")',_h), f"inline style/script/form: {_f}"

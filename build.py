import os, html
from cities import C, CHECKED
BASE = os.environ.get("BASE","https://nater79.github.io/mattress-couch-disposal-guide")
OUT="site"; os.makedirs(OUT,exist_ok=True)
SITE="Bulky Item Guide"
CONTACT="[CONTACT EMAIL PLACEHOLDER - not set up yet]"  # FLAG: Nate must supply a real contact address
# PAID: slot name -> dict(kind="Sponsored"|"Affiliate link", url=..., text=...). Fill only with real, approved deals.
PAID={}
BANNED=("recommended","best","top-rated","#1")
SLOTS=["top-banner","footer-ad","hauler-referral","featured-local-hauler","mattress-brand-haulaway"]
def SLOT(name):
    p=PAID.get(name)
    if not p: return f'<div class="slot" data-slot="{name}"><!-- MONETIZATION SLOT: {name}. Empty. --></div>'
    assert p["kind"] in ("Sponsored","Affiliate link")
    assert not any(w in p["text"].lower() for w in BANNED), "paid placements may not be called recommended/best"
    note="We earn a fee if you book through this link." if p["kind"]=="Affiliate link" else "This business paid to be listed here. We do not rate or review it."
    return f'<div class="slot paid" data-slot="{name}"><span class="label">{p["kind"]}</span> <a href="{p["url"]}" rel="sponsored nofollow noopener">{p["text"]}</a> <small>{note}</small></div>'
def disc():
    n=sum(1 for k in SLOTS if PAID.get(k))
    state="Right now this page has no paid links, ads, or sponsored listings." if n==0 else f"This page has {n} paid placement(s), each labeled Sponsored or Affiliate link right next to it."
    return ('<aside class="disc" id="ftc-disclosure"><strong>Disclosure:</strong> This site may earn money from clearly labeled ads, affiliate links, or sponsored listings. '
            f'Paid placements never change what the city rules say. {state}</aside>')
CSS="""body{font-family:system-ui,sans-serif;max-width:760px;margin:auto;padding:1em;line-height:1.6;color:#222}
a{color:#0645ad}.disc{background:#fff8e1;border:1px solid #f0d27a;padding:.6em;font-size:.9em;margin:1em 0}
.donate{background:#e8f5e9;border-left:5px solid #43a047;padding:.6em 1em}.check{background:#fdecea;padding:.6em 1em}
.slot:empty{display:none}.label{background:#333;color:#fff;font-size:.8em;padding:1px 6px;border-radius:3px}footer{font-size:.85em;color:#555;border-top:1px solid #ddd;margin-top:2em;padding-top:1em}"""
import json as _json, html as _html
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
def page(fn,title,desc,body):
    canon=ROOT if fn=="index.html" else ROOT+fn
    open(f"{OUT}/{fn}","w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{HEAD_SEC}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}"><link rel="stylesheet" href="style.css">{jsonld(fn,title)}</head><body>
<header><a href="index.html">{SITE}</a> &middot; <a href="about.html">About &amp; how we check</a></header>
{disc()}{SLOT('top-banner')}<main>{body}</main>{SLOT('footer-ad')}
<footer><p><strong>Not affiliated with any city government. Rules change; check with your city before you act.</strong> Information may be out of date or wrong. We are not responsible for fines or missed pickups. Always confirm with your city.</p><p>Found a mistake? Contact us: {CONTACT}</p>{disc()}</footer></body></html>""")
open(f"{OUT}/style.css","w").write(CSS)
DON="""<section class="donate"><h2>Step 1: Can someone else use it? Donate first</h2>
<p>If your couch or mattress is clean and in good shape, giving it away helps a neighbor and keeps it out of the landfill.</p>
<ul><li>Offer it free to neighbors (Buy Nothing groups, Nextdoor, Facebook Marketplace, Craigslist "free").</li>
<li>Call a local thrift store, church, shelter, or furniture bank. Ask if they take it and if they pick up.</li>
<li><strong>Call first.</strong> Many charities do not take used mattresses.</li>{extra}</ul></section>"""
urls=["index.html","about.html"]
rows=""
for slug,name,st,pop,agency,src,rules,notes in C:
    fn=f"{slug}.html"; urls.append(fn)
    ex="".join(f"<li>{n}</li>" for n in notes if "Bye Bye" in n)
    rl="".join(f"<li>{r}</li>" for r in rules)
    other="".join(f'<p class="check">{n}</p>' for n in notes if "Bye Bye" not in n)
    body=f"""<h1>How to get rid of a mattress or couch in {name}, {st}</h1>
{DON.format(extra=ex)}
<h2>Step 2: City pickup and drop-off rules</h2>
{'<ul>'+rl+'</ul>' if rules else ''}{other}
<p>Anything not listed here: <strong>check with the city</strong>. We only list rules we could confirm on an official page.</p>
<p><strong>Official source:</strong> <a href="{src}" rel="nofollow">{agency}</a><br><strong>Last checked:</strong> {CHECKED}</p>
<h2>Step 3: Other options</h2>
<p>If the city cannot help, you can hire a licensed hauler. Ask for a written price first. Never pay someone who might dump it illegally.</p>
{SLOT('hauler-referral')}{SLOT('featured-local-hauler')}{SLOT('mattress-brand-haulaway')}"""
    page(fn,f"Get rid of a mattress or couch in {name} ({CHECKED[:4]} city rules)",f"Free and low-cost ways to get rid of a mattress or couch in {name}: donate first, then official city pickup rules with a source link.",body)
    rows+=f'<li><a href="{fn}">{name}, {st}</a>{"" if rules and not other else " (partly verified)"}</li>'
page("index.html",f"{SITE}: get rid of a mattress or couch in your city","How to get rid of a mattress or couch in the 25 biggest US cities. Donate first, then official city rules with sources.",
 f"<h1>How to get rid of a mattress or couch</h1><p>Every city has different rules. Pick your city. Each page starts with donation ideas, then shows the city's own rules with a link to the official page and the date we checked it.</p><ul>{rows}</ul><p>Cities are the 25 largest in the US by 2023 Census Bureau population estimates.</p>")
page("about.html",f"About {SITE}","How we build and check this guide.",f"""<h1>About this guide and how we check it</h1>
<p>We want to make it easy to do the right thing with old furniture: give it away if you can, and follow city rules if you can't. That helps neighbors and cuts down on illegal dumping.</p>
<h2>How we check</h2><ul><li>Every rule comes from an official city (or city-contracted) web page. We link to it.</li>
<li>Each page shows the date we last checked it.</li><li>If we could not confirm a rule, we leave it out and tell you to check with the city. We never guess.</li>
<li>We do not post reviews or ratings.</li></ul>
<h2>Money and honesty</h2><p>This site may later earn money from clearly labeled ads, affiliate links, or labeled "featured" listings. Paid content will always be marked and will never change the city rules we show. This follows the FTC's rules on endorsements.</p>
<h2>Found a mistake?</h2><p>Please tell us: {CONTACT}. City rules change often.</p><h2>Paid links</h2><p>Every paid link will carry a visible Sponsored or Affiliate link label right next to it. We will not praise a business just because it paid us.</p>""")
open(f"{OUT}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}/{u}</loc><lastmod>{CHECKED}</lastmod></url>" for u in urls)+"</urlset>\n")
open(f"{OUT}/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
print(len(urls),"pages")
# Guard (Counsel rule 14): fail the build if any page lacks the security/SEO head tags or uses inline style/script/forms.
import glob as _g, re as _re
for _f in _g.glob(f"{OUT}/*.html"):
    _h=open(_f).read()
    assert "Content-Security-Policy" in _h and "script-src 'none'" in _h and 'name="referrer"' in _h and 'rel="canonical"' in _h and "application/ld+json" in _h, f"missing head tags: {_f}"
    assert not _re.search(r'style=|<style|<form|<iframe|<script(?! type="application/ld\+json")',_h), f"inline style/script/form: {_f}"

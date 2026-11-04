import os, html
from cities import C, CHECKED, CHECKED_BY
try:
    from cities import CHECKED_NOTE
except ImportError:
    CHECKED_NOTE = {}
NCITY=len(C)
import sys as _sys; _sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import v2
for _d in v2.EXPIRED: print("expired dated item hidden:",_d["slug"],_d["end_date"])
NO_NL=set()
BASE = os.environ.get("BASE","https://nater79.github.io/mattress-couch-disposal-guide")
OUT="site"; os.makedirs(OUT,exist_ok=True)
SITE="Bulky Item Guide"
CONTACT="navexiateam [at] navexia [dot] net"  # Monitored contact chosen by Nate 2026-10-28 (t102u); replies only, Navexia outbound hard stop applies
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
def disc(where="top"):
    n=sum(1 for k in SLOTS if PAID.get(k))
    state="Right now this page has no paid links, ads, or sponsored listings." if n==0 else f"This page has {n} paid placement(s), each labeled Sponsored or Affiliate link right next to it."
    did="ftc-disclosure" if where=="top" else "ftc-disclosure-footer"
    if where=="top":  # v3: one short line near the top; full disclosure stays in the footer
        short="No paid links or ads on this page." if n==0 else f"This page has {n} labeled paid placement(s)."
        return f'<aside class="disc disc-top" id="ftc-disclosure"><strong>Disclosure:</strong> {short} <a href="#ftc-disclosure-footer">Details</a></aside>'
    return (f'<aside class="disc" id="{did}"><strong>Disclosure:</strong> This site may earn money from clearly labeled ads, affiliate links, or sponsored listings. '
            f'Paid placements never change what the city rules say. {state}</aside>')

# --- 2026-11-01 redesign (STAGED; pending Counsel). Only pages in REDESIGN get the new header/hero/cards. ---
REDESIGN_ON=os.environ.get("ATLAS_REDESIGN","1")=="1"
REDESIGN={"how-to-videos.html","newsletter.html"} if REDESIGN_ON else set()
PLAY_SVG='<svg class="ico-s" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>'
INFO_SVG='<svg class="ico-info" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 11v6M12 7.5v.5" stroke-linecap="round"/></svg>'
SEARCH_SVG='<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
RICONS={"film":'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/><path d="M10.5 9.5l4 2.5-4 2.5z"/>',
 "doc":'<path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h7M9 8h4"/>',
 "bank":'<path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>',
 "truck":'<path d="M2 7h12v9H2zM14 10h4l3 3v3h-7z"/><circle cx="6" cy="18" r="2"/><circle cx="17" cy="18" r="2"/>',
 "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'}
def rico(n): return f'<svg class="fico" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{RICONS[n]}</svg>'
def features(items,cls=""): return f'<ul class="features {cls}">'+"".join(f'<li>{rico(i)}<div><strong>{t}</strong><span>{d}</span></div></li>' for i,t,d in items)+'</ul>'
def header2(fn):
    cur=lambda f:' class="active" aria-current="page"' if fn==f else ''
    return ('<header class="site-header hdr2"><div class="wrap bar2"><a class="brand" href="index.html"><picture><source srcset="img/logo-header.webp" type="image/webp"><img class="brand-logo" src="img/logo-header.png" width="98" height="40" alt="Bulky Item Guide"></picture></a>'
     '<nav aria-label="Main"><ul class="nav2"><li class="dd"><details><summary>Find your city</summary><ul class="dd-menu"><li><a href="index.html#cities">All cities (A to Z)</a></li><li><a href="springfield-mo-bulk-trash-pickup.html">Springfield, MO bulk pickup</a></li><li><a href="where-to-dump-a-couch-springfield-mo.html">Where to dump a couch (Springfield)</a></li><li><a href="mattress-recycling-fee-springfield-mo.html">Mattress recycling fee (Springfield)</a></li></ul></details></li>'
     f'<li><a href="junk-removal-springfield-ozark-mo.html">Junk removal: Springfield &amp; Ozark</a></li><li><a href="how-to-videos.html"{cur("how-to-videos.html")}>How-to videos</a></li><li><a href="newsletter.html"{cur("newsletter.html")}>Newsletter</a></li><li><a href="about.html">About &amp; how we check</a></li></ul></nav>'
     f'<a class="search" href="index.html#cities" aria-label="Search: find your city in the full list">{SEARCH_SVG}</a></div></header>')
def disc2(): return disc().replace('<aside class="disc" id="ftc-disclosure">','<aside class="disc disc2" id="ftc-disclosure">'+INFO_SVG+'<div>',1).replace('</aside>','</div></aside>')
HERO2={"how-to-videos.html":dict(eyebrow="How-to videos",img="hero-couch-curb",alt="Photo of a worn couch left on a street curb",w=1200,h=900,credit='Photo: &ldquo;<a href="https://commons.wikimedia.org/wiki/File:Couch_left_on_a_curb.jpg" rel="nofollow">Couch left on a curb</a>&rdquo; by Bluestspruce, dedicated to the public domain under <a href="https://creativecommons.org/publicdomain/zero/1.0/" rel="nofollow">CC0 1.0</a>.',
  feats=[("film","Watch videos","Short step-by-step guides"),("doc","Read transcripts","Every word, written out"),("bank","City rules","From official Springfield pages"),("truck","Junk removal","Local options")]),
 "newsletter.html":dict(eyebrow="Free newsletter",img="nl-moving-boxes",alt="Photo of stacked cardboard moving boxes",w=1200,h=900,credit='Photo: &ldquo;<a href="https://commons.wikimedia.org/wiki/File:Some_old_moving_boxes_from_Sweden.jpg" rel="nofollow">Some old moving boxes from Sweden</a>&rdquo; by Boivie, licensed under <a href="https://creativecommons.org/licenses/by/4.0/" rel="nofollow">CC BY 4.0</a>. Cropped.',feats=None)}
def herofy2(fn,body):
    h=HERO2[fn]
    if fn=="newsletter.html":
        m=re.search(r'<div class="nl-hero-art">.*?</div></section>',body,re.S)
        body=body.replace('<section class="nl-hero">','<section class="hero2 nl-hero2">',1).replace('<p class="nl-kicker">Free newsletter</p>','<p class="eyebrow">Free newsletter</p>',1)
        body=re.sub(r'<div class="nl-hero-art">.*?</div></section>',f'<figure class="hero2-art"><picture><source srcset="img/photos/{h["img"]}.webp" type="image/webp"><img src="img/photos/{h["img"]}.jpg" width="{h["w"]}" height="{h["h"]}" alt="{h["alt"]}" loading="eager"></picture><figcaption class="credit">{h["credit"]}</figcaption></figure></section>',body,count=1,flags=re.S)
        return body
    m=re.match(r'\s*(<h1>.*?</h1>)\s*(<p class="lede">.*?</p>)?',body,re.S)
    return (f'<section class="hero2"><div class="hero2-text"><p class="eyebrow">{h["eyebrow"]}</p>{m.group(1)}{m.group(2) or ""}</div>'
     f'<figure class="hero2-art"><picture><source srcset="img/photos/{h["img"]}.webp" type="image/webp"><img src="img/photos/{h["img"]}.jpg" width="{h["w"]}" height="{h["h"]}" alt="{h["alt"]}" loading="eager"></picture><figcaption class="credit">{h["credit"]}</figcaption></figure></section>'
     +(features(h["feats"]) if h["feats"] else "")+body[m.end():])

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
NL_CARD=('<aside class="nl-card" aria-labelledby="nl-card-h"><div><p class="nl-kicker">Free email newsletter</p><h2 id="nl-card-h">Declutter, Move &amp; Downsize Smart</h2>'
 '<p>One short email every other week: what to keep, what to give away, and how to get rid of the rest without a fine. About a 3-minute read.</p></div>'
 '<p><a class="btn" href="https://lucca-4.kit.com/a1f664d024" rel="noopener">Subscribe free</a> <a class="nl-more" href="newsletter.html">See what is inside</a></p><p class="nl-status">Signup is handled by Kit (our email service). <a href="privacy.html">Privacy</a></p></aside>')
# --- Lead-magnet signup (Counsel-cleared 2026-10-31). Forms appear ONLY on city pages listed in form_gate.json,
# which update_form_gate.py rewrites from verify_page --staged results (PASS -> form; FAIL -> no form).
KIT_FORM_ID="10123997"
# A/B test 2026-11-02 (headline only): group B cities get a task-first headline; group A keeps the control.
# Measured by the page URL Kit records as each subscriber's signup source. Same form, same copy otherwise.
AB_HEADLINE_B={"boston","dallas","el-paso","indianapolis","nashville","philadelphia","seattle"}
_AB_CUR=[None]
def SIGNUP(pos, city):
    hid=f"lm-{pos}-h"
    head=(f"Free {city} checklist: get rid of a mattress or couch the easy way" if _AB_CUR[0] in AB_HEADLINE_B else f"Free checklist for {city}")
    return (f'<aside class="lm-signup lm-{pos}" aria-labelledby="{hid}"><h2 id="{hid}">{head}</h2>'
     '<p>Get a free one-page checklist: how to get rid of a mattress or couch for free or cheap in your city.</p>'
     f'<form class="lm-form" action="https://app.kit.com/forms/{KIT_FORM_ID}/subscriptions" method="post">'
     f'<label for="lm-email-{pos}">Email address</label> <input id="lm-email-{pos}" type="email" name="email_address" required autocomplete="email"> '
     '<button class="btn" type="submit">Send me the checklist</button></form>'
     '<p class="lm-fine">We\'ll email you the checklist and occasional tips. Unsubscribe anytime. We never sell your email. '
     'Signup is handled by Kit (our email service). <a href="privacy.html">Privacy</a> &middot; <a href="#ftc-disclosure">Disclosure</a></p></aside>')
import json as _gj
FORM_GATE=set(_gj.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"form_gate.json")))["slugs"]) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"form_gate.json")) else set()
def SIG(pos,slug,city):
    _AB_CUR[0]=slug
    return SIGNUP(pos,city) if slug in FORM_GATE else ""
def header1(fn): return f"""<header class="site-header"><div class="wrap bar"><a class="brand" href="index.html"><picture><source srcset="img/logo-header.webp" type="image/webp"><img class="brand-logo" src="img/logo-header.png" width="98" height="40" alt="Bulky Item Guide"></picture></a>
<nav aria-label="Main"><ul class="nav"><li><a href="index.html#cities"{' aria-current="page"' if fn=="index.html" else ''}>Find your city</a></li><li><a href="junk-removal-springfield-ozark-mo.html">Junk removal: Springfield &amp; Ozark</a></li><li><a href="how-to-videos.html">How-to videos</a></li><li><a href="newsletter.html">Newsletter</a></li><li><a href="about.html"{' aria-current="page"' if fn=="about.html" else ''}>About &amp; how we check</a></li></ul></nav></div></header>"""
CITYFN={f"{c[0]}.html" for c in C}
NAVL=[("index.html#cities","Find your city"),("junk-removal-springfield-ozark-mo.html","Junk removal: Springfield &amp; Ozark"),("how-to-videos.html","How-to videos"),("newsletter.html","Newsletter"),("about.html","About &amp; how we check")]
def header3(fn):
    li="".join(f'<li><a href="{h}"{' aria-current="page"' if h==fn else ''}>{t}</a></li>' for h,t in NAVL)
    return ('<header class="site-header hdr3"><div class="wrap bar3"><a class="brand" href="index.html"><picture><source srcset="img/logo-header.webp" type="image/webp"><img class="brand-logo" src="img/logo-header.png" width="98" height="40" alt="Bulky Item Guide"></picture></a>'
      f'<nav class="nav3-desk" aria-label="Main"><ul>{li}</ul></nav><a class="find3" href="index.html#cities">Find your city</a>'
      f'<details class="nav3-mob"><summary aria-label="Menu"><span class="burger3" aria-hidden="true"></span><span class="sr-only">Menu</span></summary><nav aria-label="Main (mobile)"><ul>{li}</ul></nav></details></div></header>')
def page(fn,title,desc,body):
    body=(herofy2(fn,body) if fn in REDESIGN else herofy(fn,body))+REL.get(fn,"")+(NL_CARD if fn!="newsletter.html" and fn not in CITYFN else "")
    canon=ROOT if fn=="index.html" else ROOT+fn
    open(f"{OUT}/{fn}","w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{HEAD_SEC.replace("form-action 'none'","form-action https://app.kit.com") if fn[:-5] in FORM_GATE else HEAD_SEC}
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="v2.css">{'<link rel="stylesheet" href="redesign.css">' if fn in REDESIGN else ''}<link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="img/favicon-32.png"><link rel="apple-touch-icon" sizes="180x180" href="img/favicon-180.png">{GSV if fn=="index.html" else ""}{og(fn,title,desc,canon)}{jsonld(fn,title)}{article(fn,title,desc,canon)}</head><body>
<a class="skip" href="#main">Skip to content</a>
{header3(fn)}
<div class="wrap">{crumbs(fn,title)}{disc2() if fn in REDESIGN else disc()}{SLOT('top-banner')}<main id="main" class="{'home' if fn=='index.html' else 'content'}{' city3' if fn in CITYFN else ''}">{body}</main>{SLOT('footer-ad')}</div>
<footer class="site-footer"><div class="wrap"><p class="foot-brand"><img class="foot-logo" src="img/favicon-32.png" width="24" height="24" alt=""> {SITE}</p><p><strong>Not affiliated with any city government. Rules change; check with your city before you act.</strong> Information may be out of date or wrong. We are not responsible for fines or missed pickups. Always confirm with your city.</p><p>Found a mistake? Contact us: {CONTACT}</p>{disc("footer")}<p class="foot-nav"><a href="index.html">{SITE}</a> &middot; <a href="about.html">About &amp; how we check</a> &middot; <a href="privacy.html">Privacy</a> &middot; <a href="newsletter.html">Newsletter</a> &middot; <a href="sitemap.xml">Sitemap</a></p></div></footer></body></html>""")
if REDESIGN_ON:
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"redesign.css"),f"{OUT}/redesign.css")
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","photos"),f"{OUT}/img/photos",dirs_exist_ok=True)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","video2"),f"{OUT}/img/video2",dirs_exist_ok=True)
shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"v2.css"),f"{OUT}/v2.css"); shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","city"),f"{OUT}/img/city",dirs_exist_ok=True); shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"img","photos"),f"{OUT}/img/photos",dirs_exist_ok=True)
open(f"{OUT}/style.css","w").write(CSS+(("\n"+open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"signup-style.css")).read()) if FORM_GATE else ""))
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
rows=""; ROWS3=[]
for slug,name,st,pop,agency,src,rules,notes in C:
    CK=CHECKED_BY.get(slug,CHECKED)
    if slug in CHECKED_NOTE:
        _l,_u,_d=CHECKED_NOTE[slug]
        CKG=f'<div><span class="k">Checked</span><a href="{_u}" rel="nofollow"><time datetime="{_d}">{_l}</time></a></div>'
        CKP=f'<a href="{_u}" rel="nofollow">{_l}</a>'
    else:
        CKG=f'<div><span class="k">Last checked</span><time datetime="{CK}">{CK}</time></div>'
        CKP=f'<strong>Last checked:</strong> {CK}'
    fn=f"{slug}.html"; urls.append(fn)
    ex="".join(f"<li>{n}</li>" for n in notes if "Bye Bye" in n)
    rl="".join(f"<li>{r}</li>" for r in rules)
    other="".join(f'<p class="check">{n}</p>' for n in notes if "Bye Bye" not in n)
    status="Partly verified" if (not rules or other) else "Verified on official page"
    warn=" ".join(n for n in notes if "Bye Bye" not in n and "California" not in n)
    canote="".join(f'<p class="good3"><strong>Buying a new mattress?</strong> {n.split(" You can also")[0]}</p>' for n in notes if "California" in n)
    other_nc="".join(f'<p class="check">{n}</p>' for n in notes if "Bye Bye" not in n and "California" not in n)
    meta=f'Source: <a href="{src}" rel="nofollow">{agency}</a> &middot; {"Last checked " if slug not in CHECKED_NOTE else ""}{CKP.replace("<strong>Last checked:</strong> ","")} &middot; <span class="dot3 {"dot-ok" if status=="Verified on official page" else "dot-warn"}"></span>{status}'
    sig=SIG("rail",slug,name)
    if not sig: NO_NL.add(fn)
    _src_card=f'<div class="railcard3"><h2>Official source</h2><p><a href="{src}" rel="nofollow">{agency}</a></p><p class="small3">{CKP}</p><p class="small3">Status: {status}</p></div>'
    rail=f'<aside class="rail3" aria-label="Page details">{v2.dropcard(slug) or _src_card}{sig or NL_CARD}</aside>'
    body=f"""{v2.hero(slug,name,st,meta)}<div class="layout3"><div class="main3">{v2.glance(slug,src,agency,rules,warn)}{canote}
<section class="step step-city"><h2>City pickup and drop-off rules</h2>
{v2.blocks(slug,rules)}
<p class="small3 inblk3">Anything not listed here: <strong>check with the city</strong>. We only list rules we could confirm on an official page.</p>
<p class="small3"><strong>Official source:</strong> <a href="{src}" rel="nofollow">{agency}</a><br>{CKP}</p>
</section>
{DON.format(extra=ex).replace("Step 1: Can someone else use it? Donate first","Still in good shape? Donate it")}
<section class="step step-other"><h2>Hiring a hauler instead</h2>
<p>If the city cannot help, you can hire a licensed hauler. Ask for a written price first. Never pay someone who might dump it illegally.</p>
{SLOT('hauler-referral')}{SLOT('featured-local-hauler')}{SLOT('mattress-brand-haulaway')}</section></div>{rail}</div>"""
    MOD[fn]=CK
    near=[c for c in C if c[2]==st and c[0]!=slug][:3] or []
    others=near+[c for c in C if c[0]!=slug and c not in near][:max(0,4-len(near))]
    REL[fn]='<nav class="related" aria-label="Related pages"><h2>Other city guides</h2><ul>'+"".join(f'<li><a href="{c[0]}.html">Mattress and couch disposal in {c[1]}, {c[2]}</a></li>' for c in others[:4])+'<li><a href="junk-removal-springfield-ozark-mo.html">Junk removal in Springfield and Ozark, MO</a></li></ul></nav>'
    page(fn,f"Get rid of a mattress or couch in {name} ({CK[:4]} city rules)",f"Free and low-cost ways to get rid of a mattress or couch in {name}: donate first, then official city pickup rules with a source link.",body)
    ROWS3.append((st,name,fn,status))
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

STN={"AZ":"Arizona","CA":"California","CO":"Colorado","DC":"District of Columbia","FL":"Florida","IL":"Illinois","IN":"Indiana","KY":"Kentucky","MA":"Massachusetts","MD":"Maryland","MI":"Michigan","NC":"North Carolina","NM":"New Mexico","NV":"Nevada","NY":"New York","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","TN":"Tennessee","TX":"Texas","WA":"Washington"}
_g={}
for st,name,fn,status in ROWS3: _g.setdefault(st,[]).append((name,fn,status))
_stnav='<nav class="stnav3" aria-label="Jump to a state"><ul>'+"".join(f'<li><a href="#st-{st.lower()}" title="{STN.get(st,st)}">{st}</a></li>' for st in sorted(_g,key=lambda x:STN.get(x,x)))+'</ul></nav>'
_groups="".join(f'<div class="stgroup3" id="st-{st.lower()}"><h3>{STN.get(st,st)}</h3><ul>'+"".join(f'<li><a href="{fn}"><span class="dot3 {"dot-ok" if status=="Verified on official page" else "dot-warn"}" aria-hidden="true"></span>{n}<span class="sr-only"> ({status})</span></a></li>' for n,fn,status in sorted(v))+'</ul></div>' for st,v in sorted(_g.items(),key=lambda x:STN.get(x[0],x[0])))
_jump="".join(f'<li><a href="{fn}">{n}</a></li>' for n,fn in [("Fresno","fresno.html"),("Chicago","chicago.html"),("Houston","houston.html"),("Long Beach","long-beach.html"),("Albuquerque","albuquerque.html"),("New York City","new-york.html")])
page("index.html",f"{SITE}: get rid of a mattress or couch in your city","How to get rid of a mattress or couch in the 25 biggest US cities. Donate first, then official city rules with sources.",
 f"""<section class="home3-hero"><picture class="hero3-img"><source srcset="img/photos/hero-couch-curb.webp" type="image/webp"><img src="img/photos/hero-couch-curb.jpg" width="1200" height="900" alt="Photo of a worn couch left on a street curb" loading="eager" fetchpriority="high"></picture>
<div class="home3-text"><h1>Get rid of your old mattress or couch, the right way</h1><p class="lede">Official city rules, with the source and the date we checked.</p>
<p class="ctas"><a class="btn3" href="#cities">Find my city's rules</a></p><p class="popular3" id="pop3">Popular:</p><ul class="quick3" aria-labelledby="pop3">{_jump}</ul></div></section>
<p class="credit3">Photo: &ldquo;<a href="https://commons.wikimedia.org/wiki/File:Couch_left_on_a_curb.jpg" rel="nofollow">Couch left on a curb</a>&rdquo; by Bluestspruce, dedicated to the public domain under <a href="https://creativecommons.org/publicdomain/zero/1.0/" rel="nofollow">CC0 1.0</a>. Cropped; shown with a teal overlay.</p>
<a class="feat3" href="junk-removal-springfield-ozark-mo.html"><span class="feat3-k">Local guide</span><strong>Junk removal in Springfield &amp; Ozark, MO</strong><span>Drop-off sites, hours and real fees from city pages</span></a>
<section id="cities" aria-labelledby="cities-h" class="cities3"><h2 id="cities-h">Find your city</h2><p class="legend3"><span class="dot3 dot-ok" aria-hidden="true"></span> Verified on official page <span class="legsep3"></span><span class="dot3 dot-warn" aria-hidden="true"></span> Partly verified</p>
{_stnav}<div class="stgrid3">{_groups}</div><p class="note">Cities are picked from the largest in the US by 2023 Census Bureau population estimates. More are added as we check them.</p></section>
<ul class="trust3"><li><strong>Official rules</strong> Linked on every page</li><li><strong>Dated</strong> Last-checked date on every page</li><li><strong>No paid rankings</strong> No reviews or ratings</li></ul>""")
page("about.html",f"About {SITE}","How the Bulky Item Guide checks city rules: official sources only, a last-checked date on every page, and clear labels on any paid link.",f"""<h1>About this guide and how we check it</h1>
<p>We want to make it easy to do the right thing with old furniture: give it away if you can, and follow city rules if you can't. That helps neighbors and cuts down on illegal dumping.</p>
<h2>How we check</h2><ul><li>Every rule comes from an official city (or city-contracted) web page. We link to it.</li>
<li>Each page shows the date we last checked it.</li><li>If we could not confirm a rule, we leave it out and tell you to check with the city. We never guess.</li>
<li>We do not post reviews or ratings.</li></ul>
<h2>Money and honesty</h2><p>This site may later earn money from clearly labeled ads, affiliate links, or labeled "featured" listings. Paid content will always be marked and will never change the city rules we show. This follows the FTC's rules on endorsements.</p>
<h2>Found a mistake?</h2><p>Please tell us: {CONTACT}. City rules change often.</p><h2>Paid links</h2><p>Every paid link will carry a visible Sponsored or Affiliate link label right next to it. We will not praise a business just because it paid us.</p>""")

# --- Newsletter page (signup via Kit hosted page link; no embedded form/scripts) ---
NFN="newsletter.html"; urls.append(NFN); MOD[NFN]="2026-10-27"
shutil.copy(os.path.join(_I,"newsletter-hero.webp"),f"{OUT}/img/newsletter-hero.webp")
nbody="""<section class="nl-hero"><div class="nl-hero-text"><p class="nl-kicker">Free newsletter</p>
<h1>Clear out your home in less time, with fewer headaches</h1>
<p class="lede">A short, free email every other week for people who are moving, downsizing, or just tired of clutter. About a 3-minute read.</p>
<div class="nl-signup"><p><a class="btn" href="https://lucca-4.kit.com/a1f664d024" rel="noopener">Subscribe free</a></p>
<p class="nl-status">The button opens our signup page on Kit, our email service. We only ask for your email. See our <a href="privacy.html">privacy page</a>.</p></div>
<ul class="nl-trust"><li>Free</li><li>Leave anytime with one click</li><li>No spam, and we never sell your email</li></ul></div>
<div class="nl-hero-art"><img src="img/newsletter-hero.webp" width="1200" height="672" alt="Drawing of a tidy room with packed moving boxes and a donate box" loading="eager"></div></section>
<section class="step"><h2>What is in each email</h2>"""+cards([("heart","Give it a new home","One easy way to donate or sell"),("doc","Rule check","One real city rule, with the source"),("cal","Room of the week","A small 15-minute task"),("truck","Haul-away tips","How to get a fair price")])+"""</section>
<section class="step nl-sample"><h2>A look at a sample issue</h2><p>This is a made-up preview so you know what to expect. It is not a real past issue.</p>
<ol class="nl-sections"><li><strong>&#x1F4E6; The quick list</strong> &mdash; three short tips, two lines each.</li>
<li><strong>&#x1F3E0; Room of the week</strong> &mdash; one closet, drawer, or garage corner, step by step.</li>
<li><strong>&#x1F4CD; City rule check</strong> &mdash; one city's bulky-item rule, with a link to the official page and the date we checked.</li>
<li><strong>&#x1F91D; Give it away</strong> &mdash; ideas for donating things people actually want.</li>
<li><strong>&#x1F4E3; Sponsor spot</strong> &mdash; if we ever have one, it will be labeled <em>Sponsored</em> at the top. Right now there are none.</li></ol></section>
<section class="step"><h2>Honest notes</h2><ul><li><strong>Who we are:</strong> the same small team that writes this site's city guides. We do not show subscriber counts or reviews we don't have.</li>
<li><strong>Money:</strong> some future emails may have clearly labeled affiliate links or a labeled sponsor. That never changes the city rules we share.</li>
<li><strong>Privacy:</strong> we only ask for your email. We use it only to send this newsletter, we never sell or share it, and every email has a one-click unsubscribe link. Details: <a href="privacy.html">privacy page</a>. Questions: """+CONTACT+""".</li></ul></section>"""
page(NFN,"Declutter, Move & Downsize Smart: a free newsletter","A free email every other week with simple tips for decluttering, moving, and downsizing, plus real city rules for bulky items. Subscribe free.",nbody)
# --- Privacy page (Counsel 2026-10-27 newsletter fixes) ---
PFN="privacy.html"; urls.append(PFN); MOD[PFN]="2026-10-28"
pbody="""<h1>Privacy</h1><p>Last updated: October 31, 2026.</p>
<h2>This website</h2><p>This site has no accounts, no ads trackers, and no analytics. The only form on the site is the free checklist signup, which sends your email straight to Kit (see below). Our web host (GitHub Pages) may keep basic server logs, like IP addresses, for security.</p>
<h2>Checklist signup and newsletter</h2><ul><li><strong>What we collect:</strong> your email address, plus the signup source that Kit records (which page or form you signed up on). Kit also logs basic data it needs to run email, like signup date, opens and clicks, and IP address.</li>
<li><strong>Why:</strong> to send you the free checklist you asked for, and occasional tips about getting rid of bulky items. Nothing else.</li>
<li><strong>Who processes it:</strong> Kit (formerly ConvertKit) stores your email and sends our emails for us, as our processor. Kit's privacy policy: <a href="https://kit.com/privacy" rel="noopener">kit.com/privacy</a>.</li>
<li><strong>Double opt-in:</strong> after you sign up, Kit sends a confirmation email. You are not added to the list until you click the link in it.</li>
<li><strong>Unsubscribe:</strong> every email has a one-click unsubscribe link. No login or password is needed. We stop emailing you right away, and always within 10 business days, as the law requires.</li>
<li><strong>We never sell, share, rent or swap your email.</strong> No one gets it except Kit, which sends the emails for us.</li>
<li><strong>Sponsors:</strong> any paid spot or affiliate link in an email will be labeled Sponsored or Affiliate link.</li></ul>
<h2>Children</h2><p>This newsletter is not meant for children under 13.</p>
<h2>Contact</h2><p>To see or delete your data, email us at the address below.</p><p>Email: <a href="mailto:navexiateam@navexia.net">navexiateam@navexia.net</a> (for replies to our emails only).<br>Mailing address: 117 S Lexington St, Ste 100, Harrisonville, MO 64701-2444.</p>"""
page(PFN,"Privacy | "+SITE,"How Bulky Item Guide handles your email for the free checklist and newsletter: run by Kit, double opt-in, one-click unsubscribe, never sold, shared, rented or swapped.",pbody)
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
    assert not _re.search(r'style=|<style|<form|<iframe|<script(?! type="application/ld\+json")',_re.sub(r'<form class="lm-form" action="https://app\.kit\.com/forms/[A-Za-z0-9_]+/subscriptions" method="post">','',_h)), f"inline style/script/form: {_f}"

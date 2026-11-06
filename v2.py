# Redesign v2 (STAGING 2026-11-04). Imported by build.py. Uses only facts already in cities.py.
import re, json, os, datetime
HERE=os.path.dirname(os.path.abspath(__file__))
PHOTOS=json.load(open(os.path.join(HERE,"city_photos.json")))
TODAY=datetime.date.today().isoformat()
def credit(p):
    lic=f'<a href="{p["license_url"]}" rel="nofollow">{p["license"]}</a>' if p.get("license_url") else p["license"]
    sa=" Our cropped version is shared under the same license." if "SA" in p["license"] else ""
    return f'Photo: &ldquo;<a href="{p["page"]}" rel="nofollow">{p["name"]}</a>&rdquo; by {p["artist"]}, {lic}, via Wikimedia Commons. Cropped; shown with a teal overlay.{sa}'
def hero(slug,name,st,meta):
    p=PHOTOS.get(slug)
    if p:
        art=(f'<picture class="hero3-img"><source media="(max-width:640px)" srcset="img/city/{slug}-m.webp" type="image/webp"><source srcset="img/city/{slug}.webp" type="image/webp">'
             f'<img src="img/city/{slug}.jpg" width="1600" height="640" alt="{p["alt"]}" loading="eager" fetchpriority="high"></picture>')
        cr=f'<p class="credit3">{credit(p)}</p>'; cls="hero3 has-photo"
    else:
        art='<div class="hero3-pattern" aria-hidden="true"></div>'; cr=""; cls="hero3 no-photo"
    return (f'<section class="{cls}">{art}<div class="hero3-text"><p class="eyebrow3">{st} &middot; Mattress &amp; couch disposal</p>'
            f'<h1>How to get rid of a mattress or couch in {name}, {st}</h1><p class="meta3">{meta}</p></div></section>{cr}')
# Date-bound items (v3): each has an end_date (inclusive). The build drops it once TODAY > end_date.
# A rebuild is needed for expiry to take effect (weekly rebuild schedule: owner to set up).
DATED=[dict(slug="fresno",end_date="2026-11-15",html="Next free dump days: Nov 14&ndash;15"),dict(slug="sacramento",end_date="2027-01-31",html="Free junk pickups pause for leaf season (Nov&ndash;Jan). Paid pickups may be available."),dict(slug="tulsa",end_date="2027-01-31",html="New fee: $20 as of Oct 1, 2026.")]
def dated(slug): return [d for d in DATED if d["slug"]==slug and TODAY<=d["end_date"]]
EXPIRED=[d for d in DATED if TODAY>d["end_date"]]
# Drop-off cards for the sidebar (v3). Addresses restate cities.py text.
DROP={"fresno":("Free Dump Event drop-off","CARTS, 3457 S. Cedar Ave., Fresno, CA","Open on Free Dump Event days only.","3457 S. Cedar Ave, Fresno, CA"),
 "sacramento":("Self-haul with a dump coupon","Sacramento Recycling and Transfer Station, 8491 Fruitridge Road","Ask 311 for a free dump coupon first, and check that your item is taken.","8491 Fruitridge Road, Sacramento, CA 95826"),
 "long-beach":("24/7 mattress drop-off","970 W. Chester Place, Long Beach, CA","Free for residents.","970 W. Chester Place, Long Beach, CA")}
def dropcard(slug):
    d=DROP.get(slug)
    if not d: return ""
    from urllib.parse import quote
    return f'<div class="railcard3"><h2>{d[0]}</h2><p><strong>{d[1]}</strong></p><p class="small3">{d[2]}</p><p><a class="btn3 btn3-ghost btn3-full" href="https://www.google.com/maps/dir/?api=1&amp;destination={quote(d[3])}" rel="nofollow noopener">Directions</a></p></div>'
# Hand-written at-a-glance summaries. Every value restates a rule already shown below on the page (from cities.py).
G={
"tulsa":{"rows":[["Cost","$20 per 8 cubic yards (fee as of Oct 1, 2026); each extra 8 cubic yards is another $20"],["When","On your regular refuse day; book at least 3 days ahead"],["How to book","City Bulky Waste app, call 311, or email Tulsa311@cityoftulsa.org"],["Set-out time","By 5:00 a.m. on pickup day"],["Limits","Mattresses and sofas accepted; separate electronics, appliances, and tires"]],"tel":[["311","Call 311"],["Tulsa311@cityoftulsa.org","Email to schedule"]]},

"fresno":dict(rows=[("Cost","Free, once a year, for City of Fresno trash customers"),("How to book","Call 311 or use the FresGO app. The city calls you back within 7 business days."),("Set-out time","No more than 36 hours before your date, and by 6:00 a.m. on the day"),("Limits","Single bulky items (couch, mattress, box spring). Larger loads: Operation Clean Up, up to 10 cubic yards"),("Drop-off","Free Dump Events at CARTS, 3457 S. Cedar Ave.")],
  tel=[("311","Call 311"),("559-621-2489","From outside Fresno")]),
"long-beach":dict(rows=[("Cost","Free: 12 Special Collections per year for homes with city trash service"),("How to book","Online request form or the Call Center. Wait for them to confirm your date."),("Set-out time","By 6 a.m. on your confirmed day"),("Limits","Up to 8 large items or 25 bags per pickup; items up to 72 by 48 inches"),("Drop-off","Free 24/7 mattress drop-off at 970 W. Chester Place (residents)")],
  tel=[("562-570-2876","Call Center")]),
"sacramento":dict(rows=[("Cost","Free: 2 Household Junk Pickups per year for homes with city trash service"),("When","Free appointments February through October. Nov&ndash;Jan: paid pickups may be available (minimum $39.48)."),("How to book","Sac311 online, the Sac311 app, or call 311"),("Set-out time","No earlier than 24 hours before, and by 6:00 a.m. on the day"),("Limits","One pile up to 4 by 4 by 9 feet; appliances and e-waste need a separate appointment")],
  tel=[("311","Call 311"),("916-264-5011","From outside city limits"),("916-808-5454","Paid pickups (Utility Billing)")]),
"chicago":dict(rows=[("Who is served","City crews serve homes and buildings with 4 units or fewer. 5+ units: hire a private hauler."),("How to book","Arrange a bulk pickup with your ward superintendent through 311"),("Fridges &amp; freezers","Take the doors or lids off first")],
  tel=[("311","Call 311"),("312-744-5000","From outside Chicago")]),
"houston":dict(rows=[("How often","Every other month, in even-numbered months"),("Who is served","Occupied homes with city curbside service (not buildings over 8 units)"),("Set-out time","6 p.m. the Friday before to 7 a.m. on collection day, behind the curb"),("Limits","8 cubic yards per set-out (about a minivan)"),("Drop-off","City Residential Drop-Off locations between pickups (bring proof of address)")],tel=[]),
"albuquerque":dict(rows=[("Cost","Free curb pickup when you ask for one"),("How to book","Online form or 311, at least 24 hours before your next trash day"),("Pickup day","Your next normal trash day"),("Limits","About one standard pickup-truck load"),("Drop-off","$5.00 per load plus tax at 3 city Convenience Centers (residents)")],
  tel=[("311","Call 311"),("505-768-2000","From outside Albuquerque")]),
}
H={
"tulsa":["Bulky Waste Pick Up","Fee","How to book","Setting it out","Also accepted","Not accepted","Canceling","Questions"],

"fresno":["One-Time Bulky Item Pickup","How to book","Setting it out","Not taken, and second pickups","Operation Clean Up","Apartments (4+ units)","Free Dump Events","Questions"],
"long-beach":["Special Collections","How to book","What fits in one pickup","Mattresses and set-out time","Appliances, TVs and tires","24/7 mattress drop-off","Illegal dumping","Questions"],
"sacramento":["Household Junk Pickup","How to book","Setting it out","Pile size and what is not taken","Canceling","Paid pickups and self-haul","Apartments (5+ units)","Illegal dumping","Questions"],
"chicago":["Who the city serves","Book a bulk pickup","Refrigerators and freezers"],
"houston":["Pickup schedule","What is accepted","Limits","Set-out time","Between pickup months"],
"albuquerque":["Free curb pickup","How to book","Setting it out","Drop-off for a small fee","Convenience Center locations","Mattress limit","Questions"],
}
NUM=re.compile(r'(\$\d[\d,.]*(?: per [a-z ]+?)?(?= |,|\.|$)|\b\d+(?:\.\d+)? (?:cubic yards|business days|hours|large items|bags|mattresses|Special Collections)\b|\b\d{1,2}(?::\d{2})? ?[ap]\.m\.)')
def boldnums(h):
    parts=re.split(r'(<[^>]+>)',h); out=[]; inA=False
    for x in parts:
        if x.startswith("<a"): inA=True
        elif x.startswith("</a"): inA=False
        out.append(x if x.startswith("<") or inA else re.sub(r'\b(\d{3})-(\d{3})-(\d{4})\b',r'<a href="tel:\1\2\3">\1-\2-\3</a>',NUM.sub(r'<strong>\1</strong>',x)))
    return "".join(out)
def phones(rules):
    seen=[]
    for r in rules:
        for p in re.findall(r'\b\d{3}-\d{3}-\d{4}\b',re.sub(r'<[^>]+>','',r)):
            if p not in seen: seen.append(p)
    return seen
def glance(slug,src,agency,rules,warn):
    g=G.get(slug)
    if g:
        rows="".join(f'<div class="g3-row"><dt>{k}</dt><dd>{v}</dd></div>' for k,v in g["rows"])
        tel=g["tel"]
    else:
        tel=[(p,f"Call {p}") for p in phones(rules)[:1]]
        first=re.sub(r'<[^>]+>','',rules[0]) if rules else "The city page does not list mattress or couch rules we could confirm."
        first=first if len(first)<170 else first[:first.rfind(" ",0,165)]+"&hellip;"
        rows=f'<div class="g3-row"><dt>Start here</dt><dd>{first}</dd></div><div class="g3-row"><dt>Official page</dt><dd>{agency}</dd></div>'
    chip="".join(f'<p class="chip3">{d["html"]}</p>' for d in dated(slug))
    T=lambda n: "311" if n=="311" else re.sub(r"\D","",n)
    btns=f'<a class="btn3 btn3-full" href="{src}" rel="nofollow">Book or read the official rules</a>'
    if tel:
        n,lbl=tel[0]; main=lbl if (lbl.endswith(n) or n=="311") else f"{lbl}: {n}"
        sub="".join(f'<span class="tel3-sub">{l}: <a href="tel:{T(x)}">{x}</a></span>' for x,l in tel[1:])
        btns+=f'<div class="tel3"><a class="btn3 btn3-ghost btn3-full" href="tel:{T(n)}">{main}</a>{sub}</div>'
    w=f'<p class="warn3">{warn}</p>' if warn else ""
    return f'<section class="glance3" aria-labelledby="g3h"><h2 id="g3h">At a glance</h2>{chip}<dl>{rows}</dl>{w}<div class="btns3">{btns}</div></section>'
ABBR=re.compile(r'\b(a\.m|p\.m|S|N|E|W|St|Ave|Blvd|Rd|Dr|Pl|No|U\.S|e\.g|i\.e|approx|Mt|Ft|Jr)\.')
def sentences(h):
    prot=ABBR.sub(lambda m:m.group(0)[:-1]+"\u2024",h)
    parts=re.split(r'(?<=[.!?)])\s+(?=[A-Z(<])',prot)
    # do not split inside a tag/link
    out=[];buf=""
    for x in parts:
        buf=(buf+" "+x) if buf else x
        if buf.count("<a")==buf.count("</a>") and buf.count("(")<=buf.count(")"): out.append(buf);buf=""
    if buf: out.append(buf)
    return [x.replace("\u2024",".") for x in out]
def trim_lead(h,r):
    """Drop a lead-in only when it repeats the heading (e.g. 'Free once a year: the city's <Heading> picks up...')."""
    if not h: return r
    pat=r"^(?:[A-Z][^:<.]{0,60}:\s+)?(?:the city's |the |a )?"+re.escape(h)+r"(?: program)?\s+(?=[a-z])"
    r2=re.sub(pat,'',r,flags=re.I)
    if r2!=r and r2: r2=r2[0].upper()+r2[1:]
    elif re.match(r'^'+re.escape(h)+r':\s+',r): r2=re.sub(r'^'+re.escape(h)+r':\s+','',r); r2=r2[0].upper()+r2[1:]
    return r2 or r
def blk(h,r,cap=3):
    r=trim_lead(h,r); ss=sentences(r)
    vis=" ".join(ss[:cap]); more=" ".join(ss[cap:])
    hh=f'<h3>{h}</h3>' if h else ""
    det=f'<details class="more3"><summary>More details</summary><p>{boldnums(more)}</p></details>' if more else ""
    return f'<section class="blk3">{hh}<p>{boldnums(vis)}</p>{det}</section>'
def blocks(slug,rules):
    if not rules: return ""
    hs=H.get(slug)
    if hs and len(hs)==len(rules):
        return '<div class="blocks3">'+"".join(blk(h,r) for h,r in zip(hs,rules))+'</div>'
    out=[]
    for r in rules:
        m=re.match(r'([A-Z][^:<.]{2,45}):\s+(.*)$',r,re.S)
        out.append(blk(m.group(1),m.group(2)) if m else blk(None,r))
    return '<div class="blocks3">'+"".join(out)+'</div>'

#!/usr/bin/env python3
"""Live check for the Atlas site. Footer match uses the exact strings build.py emits."""
import json,re,sys,urllib.request,os,glob
BASE=os.environ.get("BASE","https://nater79.github.io/mattress-couch-disposal-guide/")
SITE=os.path.join(os.path.dirname(__file__),"..","site")
FOOTER=["Not affiliated with any city government","Information may be out of date","navexiateam [at] navexia [dot] net"]
CSP="Content-Security-Policy"; REF='name="referrer" content="strict-origin-when-cross-origin"'
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"atlas-live-check"}),timeout=20); return r.status,r.read().decode()
    except urllib.error.HTTPError as e: return e.code,""
fails=0; out=[]
files=sorted(os.path.basename(f) for f in glob.glob(SITE+"/*.html"))
links=set()
for f in files:
    s,h=get(BASE+f); r={"code":s}
    r["disc"]="ftc-disclosure" in h
    m=re.search(r"<footer[^>]*>(.*?)</footer>",h,re.S); r["footer"]=bool(m) and all(x in m.group(1) for x in FOOTER)
    r["csp"]=CSP in h and "script-src 'none'" in h; r["referrer"]=REF in h
    c=re.search(r'<link rel="canonical" href="([^"]+)"',h); exp=BASE if f=="index.html" else BASE+f
    r["canonical"]=bool(c) and c.group(1)==exp
    j=re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S)
    try: d=[json.loads(x) for x in j]; r["jsonld"]=len(d)==1 and d[0]["@type"]==("WebSite" if f=="index.html" else "BreadcrumbList")
    except Exception: r["jsonld"]=False
    r["no_inline_or_3p"]=not re.search(r'style=|<style|<form|<iframe|<script(?! type="application/ld\+json")',h)
    links|=set(re.findall(r'href="([^"#:]+)"',h))
    ok=s==200 and all(v for k,v in r.items() if k!="code"); fails+=not ok
    out.append(("PASS " if ok else "FAIL ")+f+" "+" ".join(f"{k}={'Y' if v is True else 'N' if v is False else v}" for k,v in r.items()))
for f in ["sitemap.xml","robots.txt","style.css"]:
    s,_=get(BASE+f); fails+=s!=200; out.append(f"{'PASS' if s==200 else 'FAIL'} {f} code={s}")
for l in sorted(links):
    s,_=get(BASE+l); fails+=s!=200; out.append(f"{'PASS' if s==200 else 'FAIL'} link {l} code={s}")
print("\n".join(out)); print(f"failures={fails}"); sys.exit(1 if fails else 0)

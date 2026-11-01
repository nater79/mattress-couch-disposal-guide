#!/usr/bin/env python3
"""Nightly form gate: a city page shows the Kit signup form only if verify_page --staged PASSES on it.
Writes form_gate.json; exits 3 if the gate changed (caller rebuilds). FETCH_ERROR/any FAIL => no form (conservative)."""
import json,os,subprocess,sys,datetime
from concurrent.futures import ThreadPoolExecutor
H=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,H)
from cities import C
G=os.path.join(H,"form_gate.json"); old=set(json.load(open(G))["slugs"]) if os.path.exists(G) else set()
def run(slug):
    r=subprocess.run(["python3","/workspace/ops/bin/verify_page.py",slug,"--staged","--docs",os.path.join(H,"site"),"--no-state"],capture_output=True,text=True)
    return slug, f"RESULT {slug} --staged: PASS" in r.stdout
with ThreadPoolExecutor(4) as ex: res=dict(ex.map(run,[c[0] for c in C]))
CL=set(json.load(open(os.path.join(H,"form_cleared.json")))["cleared"])
new={s for s,ok in res.items() if ok and s in CL}  # never add a page Counsel has not cleared
json.dump({"note":"City slugs allowed to show the Kit signup form. Rewritten by update_form_gate.py from verify_page --staged; a page gets a form only if it PASSES.","updated":datetime.date.today().isoformat(),"slugs":sorted(new)},open(G,"w"),indent=1)
print("gate:",len(new),"added:",sorted(new-old),"removed:",sorted(old-new)); sys.exit(3 if new!=old else 0)

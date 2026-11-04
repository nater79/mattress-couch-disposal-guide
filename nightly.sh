#!/usr/bin/env bash
# Nightly publish for the Atlas site. Rebuilds (build.py enforces CSP/referrer/canonical/JSON-LD), pushes to Pages, runs live check.
set -euo pipefail
cd /workspace/atlas-directory
python3 build.py
set +e; python3 tools/update_form_gate.py; GATE_RC=$?; set -e  # forms only on pages that pass verify_page --staged
if [ $GATE_RC -eq 3 ]; then python3 build.py; elif [ $GATE_RC -ne 0 ]; then echo "form gate errored ($GATE_RC); keeping previous gate" >&2; fi
R=/tmp/repo; [ -d $R/.git ] || gh repo clone nater79/mattress-couch-disposal-guide $R
cd $R && git pull -q && rm -rf docs && cp -r /workspace/atlas-directory/site docs && touch docs/.nojekyll && cp /workspace/atlas-directory/{build.py,cities.py,nightly.sh,local_pages.py,videos.json,form_gate.json,form_cleared.json,signup-style.css,v2.py,v2.css,city_photos.json} . && cp -r /workspace/atlas-directory/tools . && mkdir -p img && cp -r /workspace/atlas-directory/img/. img/
git add -A; git diff --cached --quiet || { git -c user.name=nater79 -c user.email=nater79@users.noreply.github.com commit -qm "Nightly update $(date +%F)"; git push -q; sleep 90; }
python3 /workspace/atlas-directory/tools/live_check.py

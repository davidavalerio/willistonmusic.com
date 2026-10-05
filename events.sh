#!/bin/bash
# Site refresh (launchd: com.davalerio.wmi-events, every 10 minutes on the mini).
# Rewrites the upcoming-events list on events.html from Alma's public Google Calendar
# (events.py) and the Marketplace listings in marketplace.csv from her sheet
# (marketplace.py), and pushes them to main when either changed; GitHub Pages publishes
# within a minute. A checkout that is off main or has local changes is left alone.
# One line per run in ~/.claude/maintenance/wmi-events.log.
set -uo pipefail
export PATH="/Users/valerio/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd /Users/valerio/Projects/willistonmusic.com || exit 1
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

[ "$(git branch --show-current)" = main ] || { log "skip: checkout is not on main"; exit 0; }
[ -z "$(git status --porcelain)" ] || { log "skip: checkout has local changes"; exit 0; }
git pull -q --ff-only || { log "skip: pull failed"; exit 1; }
ev=$(uv run -q events.py 2>&1); ev=${ev##*$'\n'}
mk=$(uv run -q marketplace.py 2>&1); mk=${mk##*$'\n'}
out="$ev; $mk"
if git diff --quiet events.html marketplace.csv; then log "$out"; exit 0; fi
git commit -q -m "Update the events and Marketplace listings from Alma's calendar and sheet" events.html marketplace.csv \
  && git push -q origin main || { log "$out, push failed"; exit 1; }
log "$out, published"

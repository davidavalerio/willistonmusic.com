#!/bin/bash
# Events page refresh (launchd: com.davalerio.wmi-events, hourly on the mini).
# Rewrites the upcoming-events list on events.html from Alma's public Google Calendar
# (events.py) and pushes it to main when it changed; GitHub Pages publishes it within a
# minute. A checkout that is off main or has local changes is left alone.
# One line per run in ~/.claude/maintenance/wmi-events.log.
set -uo pipefail
export PATH="/Users/valerio/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd /Users/valerio/Projects/willistonmusic.com || exit 1
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

[ "$(git branch --show-current)" = main ] || { log "skip: checkout is not on main"; exit 0; }
[ -z "$(git status --porcelain)" ] || { log "skip: checkout has local changes"; exit 0; }
git pull -q --ff-only || { log "skip: pull failed"; exit 1; }
out=$(uv run -q events.py 2>&1) || { log "${out##*$'\n'}"; exit 1; }
if git diff --quiet events.html; then log "$out"; exit 0; fi
git commit -q -m "Update the events from Alma's calendar" events.html && git push -q origin main \
  || { log "$out, push failed"; exit 1; }
log "$out, published"

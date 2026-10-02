# willistonmusic.com

The Williston Music Intensive website: Alma's music venture (the full-band workshop, the Mic Check singer's workshop, the Spotlight open mic). David runs the site; Alma's changes come through him. It is a like-for-like rebuild of the site she made in GoDaddy's website builder, so the look and the wording are hers: dark band with the WMI logo, Archivo Black headings, Montserrat text, white ground. A change of wording, a new sponsor, or a new year's page starts here; a redesign is Alma's call.

## GoDaddy's old plan

The site is served from this repo. The "Websites + Marketing Basic" plan that used to serve it, in Alma's GoDaddy account, no longer does; if it is still listed there it renews automatically on or about October 15, 2026 ($203.88 in 2025), and cancelling it does not touch this site, the domain, or the mail.

## Stack

Static HTML, one shared stylesheet (`site.css`), no build step and no script in the pages. The header, menu, and footer are repeated in each page, so a change to them is made in all six. Fonts come from Google Fonts. One layout: links across the top from 1024px, a menu button with a full-screen drawer below (a checkbox, no JavaScript); columns stack below 768px. The sponsor wall is written twice on each page that has it, three columns (`.sponsors.d`) and two (`.sponsors.p`), to keep the staggered arrangement of the original at both widths.

## Files

- `index.html`, `about.html`, `events.html`, `sponsor.html`, `2026.html`, `404.html`. GitHub Pages serves each at its name without `.html`, so the addresses are `/about`, `/events`, `/sponsor`, `/2026`, as they were on GoDaddy. `/2026` is the participants' songs-and-links page and is in no menu.
- `img/`: the photos at web size and the sponsor logos. `originals/` holds the full-size photos as downloaded from GoDaddy.
- `downloads/`: the two PDFs on the Sponsor page (the sponsorship booklet, the 2024 donor report). A new year's booklet replaces the file under the same name.
- `favicon.png`, `apple-touch-icon.png`: the W mark on black, from `1-Practice/3-WMI/Branding/WMI-r12-dark.png` in the Drive.
- `events.py`: `uv run events.py` writes the upcoming events from Alma's Google Calendar into `events.html`, between the `<!-- events -->` markers, in the page's own style (date, title, day and time, place, her description with its links); an event leaves the list once it ends, and with none ahead the page says so. It writes only when the list changed and leaves the page alone if the calendar can't be read. `events.sh` runs it hourly on the mini (`com.davalerio.wmi-events.plist`, loaded with `/mini load`; log `~/.claude/maintenance/wmi-events.log`, one line per run): it pulls main, and when the list changed commits `events.html` and pushes, so an event Alma adds or changes is live within the hour. It leaves the mini's checkout alone while that is off main or has uncommitted work, so a dev session there pauses it.
- `preview.py`: `python3 preview.py` serves the site at `http://127.0.0.1:8765/` with the same extensionless addresses.
- `CNAME`: `willistonmusic.com`.

## Outside the repo

Registration and the sponsor form are Alma's Jotform forms. `register.willistonmusic.com` and `sponsor.willistonmusic.com` are forwards set in GoDaddy's DNS to those forms; the Sponsor page's "donor form" link uses the second. The song charts on `/2026` are files in Alma's Google Drive. The events are her public Google Calendar "Williston Music Intensive" (the one GoDaddy's calendar widget read; its address is in `events.py`): she adds or changes an event there, not on the site.

## Deployment

GitHub Pages from `main`, repo `davidavalerio/willistonmusic.com`. `/deploy` ships changes.

## Domain

Registered at GoDaddy in Alma's account, paid through September 8, 2027; David manages the DNS there (web UI, no API access). Records for the site: four A records on `@` (`185.199.108.153` through `185.199.111.153`) and `www` as a CNAME to `davidavalerio.github.io`. `team@willistonmusic.com` runs on GoDaddy's mail records, so the MX and TXT records are left alone, as are the two forwards above.

HTTPS is enforced in the Pages settings, and it has to stay working: the GoDaddy site told browsers to use only the secure address for two years, subdomains included, so a browser that visited it refuses the site outright whenever the certificate is missing. GitHub issues and renews the certificate itself. If it ever fails to, removing the custom domain in the Pages settings and adding it back makes GitHub recheck the DNS and issue one; that writes a "Delete CNAME" and a "Create CNAME" commit to `main`, so pull afterward.

# willistonmusic.com

The Williston Music Intensive website: Alma's music venture (the full-band workshop, the Mic Check singer's workshop, the Spotlight open mic). David runs the site; Alma's changes come through him. It is a like-for-like rebuild of the site she made in GoDaddy's website builder, so the look and the wording are hers: dark band with the WMI logo, Archivo Black headings, Montserrat text, white ground. A change of wording, a new sponsor, or a new year's page starts here; a redesign is Alma's call.

## GoDaddy's old plan

The site is served from this repo. The "Websites + Marketing Basic" plan that used to serve it, in Alma's GoDaddy account, no longer does; if it is still listed there it renews automatically on or about October 15, 2026 ($203.88 in 2025), and cancelling it does not touch this site, the domain, or the mail.

## Stack

Static HTML, one shared stylesheet (`site.css`), no build step, and no script in the pages except the Marketplace's. The header, menu, and footer are repeated in each page, so a change to them is made in all seven. Fonts come from Google Fonts. One layout: links across the top from 1024px, a menu button with a full-screen drawer below (a checkbox, no JavaScript); columns stack below 768px. The sponsor wall is written twice on each page that has it, three columns (`.sponsors.d`) and two (`.sponsors.p`), to keep the staggered arrangement of the original at both widths.

## Files

- `index.html`, `about.html`, `events.html`, `marketplace.html`, `sponsor.html`, `2026.html`, `404.html`. GitHub Pages serves each at its name without `.html`, so the addresses are `/about`, `/events`, `/marketplace`, `/sponsor`, `/2026`, as they were on GoDaddy. `/2026` is the participants' songs-and-links page and is in no menu.
- `marketplace.html`: Alma's community classifieds. Her intro, then a "Post a listing" button that opens and closes her posting text and her Marketplace form (closed by default; the form loads on first open), then the listings, which the page's one script reads from `marketplace.csv` each time it opens and lays out as cards, newest first, with a filter by "Seeking…" in the form's order. Which listings appear and when they expire is decided in her sheet, so approving one needs nothing here.
- `marketplace.py`: `uv run marketplace.py` writes `marketplace.csv` from Alma's sheet: the rows she marked Approved whose Expired column is FALSE, columns A–L only. The sheet's address is in `~/.config/wmi/marketplace-sheet` on the mini, never in this repo, which is public: the page never touches the sheet, so submissions she hasn't approved and the feedback column stay out of reach. It writes only when the listings changed and leaves the file alone if the sheet can't be read or Status and Expired are no longer columns O and Q. Every listing that has ever gone up stays in the repo's history after it comes down.
- `img/`: the photos at web size and the sponsor logos. `originals/` holds the full-size photos as downloaded from GoDaddy.
- `downloads/`: the two PDFs on the Sponsor page (the sponsorship booklet, the 2024 donor report). A new year's booklet replaces the file under the same name.
- `favicon.png`, `apple-touch-icon.png`: the W mark on black, from `1-Practice/3-WMI/Branding/WMI-r12-dark.png` in the Drive.
- `events.py`: `uv run events.py` writes the upcoming events from Alma's Google Calendar into `events.html`, between the `<!-- events -->` markers, in the page's own style (date, title, day and time, place, her description with its links); an event leaves the list once it ends, and with none ahead the page says so. It writes only when the list changed and leaves the page alone if the calendar can't be read. `events.sh` runs it and `marketplace.py` every 10 minutes on the mini (`com.davalerio.wmi-events.plist`, loaded with `/mini load`; log `~/.claude/maintenance/wmi-events.log`, one line per run): it pulls main, and when either changed commits `events.html` and `marketplace.csv` and pushes, so an event or a listing Alma approves is live within about ten minutes. It leaves the mini's checkout alone while that is off main or has uncommitted work, so a dev session there pauses it.
- `preview.py`: `python3 preview.py` serves the site at `http://127.0.0.1:8765/` with the same extensionless addresses.
- `CNAME`: `willistonmusic.com`.

## Outside the repo

Registration, the sponsor form, and the Marketplace form are Alma's Jotform forms. Marketplace submissions land in the Submissions tab of her Google Sheet "WMI – Marketplace Listings", where she sets Status (column O) and the sheet works out Expired (column Q); `marketplace.py` reads it through its anyone-with-the-link address. `register.willistonmusic.com` and `sponsor.willistonmusic.com` are forwards set in GoDaddy's DNS to those forms; the Sponsor page's "donor form" link uses the second. The song charts on `/2026` are files in Alma's Google Drive. The events are her public Google Calendar "Williston Music Intensive" (the one GoDaddy's calendar widget read; its address is in `events.py`): she adds or changes an event there, not on the site.

## Deployment

GitHub Pages from `main`, repo `davidavalerio/willistonmusic.com`. `/deploy` ships changes.

## Domain

Registered at GoDaddy in Alma's account, paid through September 8, 2027; David manages the DNS there (web UI, no API access). Records for the site: four A records on `@` (`185.199.108.153` through `185.199.111.153`) and `www` as a CNAME to `davidavalerio.github.io`. `team@willistonmusic.com` runs on GoDaddy's mail records, so the MX and TXT records are left alone, as are the two forwards above.

HTTPS is enforced in the Pages settings, and it has to stay working: the GoDaddy site told browsers to use only the secure address for two years, subdomains included, so a browser that visited it refuses the site outright whenever the certificate is missing. GitHub issues and renews the certificate itself. If it ever fails to, removing the custom domain in the Pages settings and adding it back makes GitHub recheck the DNS and issue one; that writes a "Delete CNAME" and a "Create CNAME" commit to `main`, so pull afterward.

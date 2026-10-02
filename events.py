# /// script
# requires-python = ">=3.12"
# dependencies = ["icalendar>=6", "recurring-ical-events>=3"]
# ///
"""Write the upcoming events from Alma's Google Calendar into events.html.

    uv run events.py

The list sits between the <!-- events --> and <!-- /events --> markers; the rest of the
page is left as it is, and the file is written only when the list changed. If the
calendar can't be read, the page is not touched. Prints one line saying what it found.
"""
import html
import sys
import urllib.request
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

import icalendar
import recurring_ical_events

CALENDAR = "https://calendar.google.com/calendar/ical/c_5fpgd82d95tfe99g8vhc6iupds%40group.calendar.google.com/public/basic.ics"
TZ = ZoneInfo("America/Chicago")
PAGE = Path(__file__).with_name("events.html")
OPEN, CLOSE = "<!-- events -->", "<!-- /events -->"


class Description(HTMLParser):
    """Google stores a description as HTML; keep its links and emphasis, drop the rest."""

    KEEP = {"b", "strong", "i", "em"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.links = [], []

    def handle_starttag(self, tag, attrs):
        if tag in self.KEEP:
            self.out.append(f"<{tag}>")
        elif tag == "br":
            self.out.append("<br>")
        elif tag == "a":
            href = dict(attrs).get("href") or ""
            ok = href.startswith(("http://", "https://", "mailto:"))
            self.links.append(ok)
            if ok:
                self.out.append(f'<a href="{html.escape(href)}" target="_blank" rel="noopener">')

    def handle_endtag(self, tag):
        if tag in self.KEEP:
            self.out.append(f"</{tag}>")
        elif tag == "a" and self.links and self.links.pop():
            self.out.append("</a>")

    def handle_data(self, data):
        self.out.append(html.escape(data, quote=False).replace("\n", "<br>"))


def moment(value):
    """A start or end as a Chicago datetime; an all-day date is its midnight."""
    if isinstance(value, datetime):
        return value.astimezone(TZ) if value.tzinfo else value.replace(tzinfo=TZ)
    return datetime(value.year, value.month, value.day, tzinfo=TZ)


def clock(t):
    h = t.hour % 12 or 12
    return f"{h}:{t.minute:02d}" if t.minute else str(h)


def ampm(t):
    return "a.m." if t.hour < 12 else "p.m."


def when(start, end, all_day):
    if all_day:
        last = end - timedelta(days=1)
        return f"{start:%A}, all day" if last <= start else f"{start:%A} to {last:%A}, {last:%B} {last.day}"
    if (end - timedelta(microseconds=1)).date() != start.date():
        return f"{start:%A}, {clock(start)} {ampm(start)} to {end:%A}, {clock(end)} {ampm(end)}"
    if end == start:
        return f"{start:%A}, {clock(start)} {ampm(start)}"
    first = clock(start) if ampm(start) == ampm(end) else f"{clock(start)} {ampm(start)}"
    return f"{start:%A}, {first}–{clock(end)} {ampm(end)}"


def place(location):
    text = " ".join(str(location).replace("\n", ", ").split())
    for suffix in (", USA", ", United States"):
        text = text.removesuffix(suffix)
    return text


def item(event):
    all_day = not isinstance(event.start, datetime)
    start, end = moment(event.start), moment(event.end)
    lines = [
        f'<time datetime="{start.isoformat() if not all_day else start.date().isoformat()}"><span>{start:%b}</span> {start.day}</time>',
        "<div>",
        f"  <h3>{html.escape(str(event.get('SUMMARY', '')).strip(), quote=False)}</h3>",
        f'  <p class="when">{when(start, end, all_day)}</p>',
    ]
    if where := place(event.get("LOCATION", "")):
        lines.append(f'  <p class="where">{html.escape(where, quote=False)}</p>')
    if text := str(event.get("DESCRIPTION", "")).strip():
        parser = Description()
        parser.feed(text)
        parser.close()
        lines.append(f'  <p class="about">{"".join(parser.out).strip()}</p>')
    lines.append("</div>")
    return "      <li>\n" + "".join(f"        {line}\n" for line in lines) + "      </li>"


def main():
    with urllib.request.urlopen(CALENDAR, timeout=30) as response:
        calendar = icalendar.Calendar.from_ical(response.read())
    now = datetime.now(TZ)
    events = [
        e for e in recurring_ical_events.of(calendar).between(now - timedelta(days=2), now + timedelta(days=366))
        if str(e.get("STATUS", "")).upper() != "CANCELLED" and moment(e.end) > now
    ]
    events.sort(key=lambda e: moment(e.start))

    if events:
        block = '<ol class="events">\n' + "\n".join(map(item, events)) + "\n    </ol>"
    else:
        block = '<p class="center events-none">No upcoming events right now.</p>'

    page = PAGE.read_text()
    head, rest = page.split(OPEN, 1)
    tail = rest.split(CLOSE, 1)[1]
    new = f"{head}{OPEN}\n    {block}\n    {CLOSE}{tail}"
    if new != page:
        PAGE.write_text(new)
    count = f"{len(events)} upcoming event{'s' if len(events) != 1 else ''}" if events else "no upcoming events"
    print(f"{count}, page {'updated' if new != page else 'unchanged'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"calendar not read, page untouched: {e}")

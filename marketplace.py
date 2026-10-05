# /// script
# requires-python = ">=3.12"
# ///
"""Write the approved, unexpired Marketplace listings from Alma's sheet into marketplace.csv.

    uv run marketplace.py

The sheet is her "WMI – Marketplace Listings" (Submissions tab); its CSV address lives in
~/.config/wmi/marketplace-sheet on the mini, never in this public repo, so only what she
approved reaches the site. A row is kept when Status (column O) is "Approved" and Expired
(column Q, worked out in the sheet) is FALSE; only columns A–L are written. The file is
written only when it changed, and left alone if the sheet can't be read. Prints one line
saying what it found.
"""
import csv
import io
import sys
import urllib.request
from pathlib import Path

SOURCE = Path.home() / ".config/wmi/marketplace-sheet"
OUT = Path(__file__).with_name("marketplace.csv")


def main():
    try:
        url = SOURCE.read_text().strip()
        with urllib.request.urlopen(url, timeout=30) as r:
            rows = list(csv.reader(io.StringIO(r.read().decode("utf-8"))))
    except Exception as e:
        print(f"listings: sheet not read ({e}), file unchanged")
        sys.exit(1)
    header, body = rows[0], rows[1:]
    if len(header) < 17 or header[14].strip() != "Status" or header[16].strip() != "Expired":
        print("listings: sheet columns have moved (Status not O or Expired not Q), file unchanged")
        sys.exit(1)
    keep = [r[:12] for r in body if len(r) > 16
            and r[14].strip().lower() == "approved" and r[16].strip().upper() == "FALSE"]
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows([header[:12], *keep])
    new = buf.getvalue()
    if OUT.exists() and OUT.read_text() == new:
        print(f"{len(keep)} active listings, file unchanged")
        return
    OUT.write_text(new)
    print(f"{len(keep)} active listings, file written")


main()

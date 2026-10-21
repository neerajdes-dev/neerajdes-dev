"""Generate an SVG GitHub contribution calendar from the public profile page."""
from __future__ import annotations
import html
import os
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_PROFILE_USER", "neerajdes-dev")
OUT = Path("assets/contributions.svg")
PALETTE = ["#182821", "#174f39", "#267b4e", "#3ebc73", "#81efab"]

def fetch_days() -> dict[str, int]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    response = requests.get(url, timeout=25, headers={"User-Agent": "profile-readme-generator/1.0", "Accept": "text/html"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days: dict[str, int] = {}
    for node in soup.select("[data-date]"):
        day = node.get("data-date")
        level = node.get("data-level")
        if not day or level is None:
            continue
        try:
            date.fromisoformat(day)
            days[day] = max(0, min(4, int(level)))
        except ValueError:
            continue
    if not days:
        raise RuntimeError("No contribution cells found; GitHub may have changed its HTML.")
    return days

def main() -> None:
    days = fetch_days()
    end = date.today()
    start = end - timedelta(days=364)
    monday = start - timedelta(days=start.weekday())
    cells = []
    for i in range((end - monday).days + 1):
        current = monday + timedelta(days=i)
        if current < start:
            continue
        x = 30 + (i // 7) * 16
        y = 77 + current.weekday() * 16
        level = days.get(current.isoformat(), 0)
        cells.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="3" fill="{PALETTE[level]}"><title>{current.isoformat()}: activity level {level}</title></rect>')
    width = 30 + (((end - monday).days // 7) + 1) * 16 + 20
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="218" viewBox="0 0 {width} 218" role="img" aria-label="GitHub contribution calendar for {html.escape(USERNAME)}">
<style>text{{font-family:Arial,sans-serif;fill:#bbd0c4}}.dot{{animation:pulse 3s ease-in-out infinite}}@keyframes pulse{{50%{{opacity:.58}}}}@media(prefers-reduced-motion:reduce){{.dot{{animation:none}}}}</style>
<rect width="100%" height="100%" rx="18" fill="#0d1117"/>
<text x="30" y="39" font-size="19" font-weight="bold">CONTRIBUTION ACTIVITY</text>
<text x="30" y="59" font-size="11">Public GitHub contribution levels · refreshed daily</text>
<g class="dot">{''.join(cells)}</g>
<text x="30" y="205" font-size="12">Less</text>
{''.join(f'<rect x="{72 + i*17}" y="194" width="11" height="11" rx="3" fill="{color}"/>' for i,color in enumerate(PALETTE))}
<text x="167" y="205" font-size="12">More</text>
</svg>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print(f"Wrote {OUT} from {len(days)} days of public contribution data")

if __name__ == "__main__":
    main()

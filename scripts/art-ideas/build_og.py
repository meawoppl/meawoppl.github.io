#!/usr/bin/env python3
"""Render a 1200x630 social-share card for every art idea.

Cards are laid out as HTML, screenshotted with headless Chrome, then converted
to JPEG (OG unfurlers accept JPEG and it is a fraction of the PNG size).

    python scripts/art-ideas/build_og.py           # only rebuild what changed
    python scripts/art-ideas/build_og.py --force   # rebuild everything
"""

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "public" / "art-ideas"
OUT = ART / "og"

WIDTH, HEIGHT = 1200, 630
JPEG_QUALITY = 82

CHROME_CANDIDATES = ["google-chrome", "chromium", "chromium-browser", "google-chrome-stable"]


def slugify(title: str) -> str:
    """Must match slugify() in public/art-ideas/app.js."""
    return re.sub(r"^-+|-+$", "", re.sub(r"[^a-z0-9]+", "-", title.lower()))


def theme_hue(name: str) -> int:
    """Same string hash as themeColor() in app.js, so chip colours line up."""
    h = 0
    for ch in name:
        h = ((h << 5) - h + ord(ch)) & 0xFFFFFFFF
        if h >= 0x80000000:
            h -= 0x100000000
    return abs(h) % 360


def find_chrome() -> str:
    for name in CHROME_CANDIDATES:
        path = shutil.which(name)
        if path:
            return path
    sys.exit("No Chrome/Chromium found; install one or set PATH.")


def truncate(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def card_html(item: dict, doc: dict | None, slug: str) -> str:
    title = item["title"]
    themes = item.get("themes") or []
    accent = f"hsl({theme_hue(themes[0])}, 55%, 45%)" if themes else "hsl(210, 55%, 45%)"

    first_para = ""
    for block in (doc or {}).get("blocks", []):
        if block.get("type") != "list" and block.get("text"):
            first_para = block["text"]
            break
    summary = truncate(item.get("summary") or first_para, 190)

    # Long titles need to shrink or they overflow the card.
    size = 66 if len(title) <= 28 else 56 if len(title) <= 44 else 46

    badges = ""
    if item.get("burning_man") is True:
        badges += '<span class="badge bm">Burning Man</span>'
    if item.get("business") == "yes":
        badges += '<span class="badge biz">Business</span>'
    elif item.get("business") == "maybe":
        badges += '<span class="badge biz-maybe">Business?</span>'

    chips = "".join(
        f'<span class="chip" style="--c:hsl({theme_hue(t)}, 55%, 45%)">{html.escape(t)}</span>'
        for t in themes[:4]
    )

    art = ""
    images = (doc or {}).get("images") or []
    if images:
        src = (ART / "docs" / slug / images[0]).resolve().as_uri()
        art = f'<div class="art"><img src="{html.escape(src)}"></div>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {WIDTH}px; height: {HEIGHT}px; }}
  body {{
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    background: #fafafa;
    display: flex;
    overflow: hidden;
  }}
  .bar {{ width: 18px; background: {accent}; flex: none; }}
  .body {{
    flex: 1;
    padding: 56px 56px 44px;
    display: flex;
    flex-direction: column;
    min-width: 0;
  }}
  .kicker {{
    font-size: 20px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {accent};
    margin-bottom: 20px;
  }}
  h1 {{
    font-size: {size}px;
    line-height: 1.12;
    color: #141414;
    letter-spacing: -0.015em;
    margin-bottom: 22px;
  }}
  .summary {{
    font-size: 26px;
    line-height: 1.45;
    color: #4a4a4a;
    max-width: 30ch;
  }}
  .foot {{ margin-top: auto; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .badge, .chip {{
    font-size: 19px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 4px;
    white-space: nowrap;
  }}
  .badge.bm {{ background: #ffe8cc; color: #a04a00; }}
  .badge.biz {{ background: #d4edda; color: #155724; }}
  .badge.biz-maybe {{ background: #e2e3e5; color: #383d41; }}
  .chip {{
    font-weight: 500;
    background: #fff;
    color: #333;
    border: 1px solid #e2e2e2;
    border-left: 5px solid var(--c, #999);
  }}
  .site {{
    margin-left: auto;
    font-size: 20px;
    color: #8a8a8a;
    white-space: nowrap;
  }}
  .art {{
    width: 400px;
    flex: none;
    border-left: 1px solid #ececec;
    background: #f0f0f0;
  }}
  .art img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
</style></head>
<body>
  <div class="bar"></div>
  <div class="body">
    <div class="kicker">Art Ideas</div>
    <h1>{html.escape(title)}</h1>
    {f'<div class="summary">{html.escape(summary)}</div>' if summary else ''}
    <div class="foot">{badges}{chips}<span class="site">meawoppl.github.io</span></div>
  </div>
  {art}
</body></html>"""


def fingerprint(markup: str) -> str:
    return hashlib.sha256(markup.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rebuild every card")
    args = ap.parse_args()

    chrome = find_chrome()
    ideas = json.loads((ART / "data" / "ideas.json").read_text())
    try:
        docs_index = json.loads((ART / "docs" / "index.json").read_text())
    except FileNotFoundError:
        docs_index = {}

    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / ".manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        manifest = {}

    built = skipped = 0
    seen = set()

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for item in ideas:
            slug = slugify(item["title"])
            seen.add(slug)
            doc = None
            if slug in docs_index:
                try:
                    doc = json.loads((ART / "docs" / f"{slug}.json").read_text())
                except FileNotFoundError:
                    doc = None

            markup = card_html(item, doc, slug)
            stamp = fingerprint(markup)
            dest = OUT / f"{slug}.jpg"

            if not args.force and manifest.get(slug) == stamp and dest.exists():
                skipped += 1
                continue

            src_html = tmpdir / f"{slug}.html"
            src_html.write_text(markup)
            shot = tmpdir / f"{slug}.png"

            subprocess.run(
                [
                    chrome,
                    "--headless",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--hide-scrollbars",
                    "--force-device-scale-factor=1",
                    f"--window-size={WIDTH},{HEIGHT}",
                    f"--screenshot={shot}",
                    src_html.resolve().as_uri(),
                ],
                check=True,
                capture_output=True,
            )

            with Image.open(shot) as img:
                img.convert("RGB").save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)

            manifest[slug] = stamp
            built += 1
            print(f"  built {dest.relative_to(ROOT)}")

    # Drop cards for ideas that no longer exist.
    removed = 0
    for stale in OUT.glob("*.jpg"):
        if stale.stem not in seen:
            stale.unlink()
            manifest.pop(stale.stem, None)
            removed += 1
            print(f"  removed {stale.relative_to(ROOT)}")

    manifest = {k: v for k, v in manifest.items() if k in seen}
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    print(f"\n{built} built, {skipped} unchanged, {removed} removed -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

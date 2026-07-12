#!/usr/bin/env python3
"""Extract a Notion-exported PDF into structured content for the Art Ideas modal.

Usage: python scripts/art-ideas/extract_doc.py <pdf> <slug> "<Idea Title>"

Writes:
  public/art-ideas/docs/<slug>/<slug>-NN.(png|jpg)   extracted images (keyed prefix)
  public/art-ideas/docs/<slug>.json                  {slug, title, blocks, images}
and registers <slug> in public/art-ideas/docs/index.json.
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent.parent
DOCS = REPO / "public" / "art-ideas" / "docs"

MIN_IMG_DIM = 100  # px — drop page icons / emoji / tiny decorations
MAX_IMG_DIM = 1600  # px — cap the long edge for web delivery

# Extracted images that are actually 2x2 grids (e.g. Midjourney 4-ups), keyed by
# their output stem "<slug>-NN". These get split into four quadrants (a-d) with the
# center gutter trimmed. Verified visually; see the contact sheet in the PR.
GRID_STEMS = {
    "dirt-for-children-02",
    "family-platonics-01",
    "illuminated-manuscripts-01",
    "universal-ring-01",
}
SUBLEVEL_INDENT = 8  # leading spaces beyond this mark a nested (sub) list item

BULLET_RE = re.compile(r"^([●○•▪‣◦⁃*—–\-])\s+(.*)$")
ORDERED_RE = re.compile(r"^((?:\d{1,3}|[a-zA-Z]|[ivxlcIVXLC]{1,4})\.)\s+(.*)$")
JUNK_RE = re.compile(r"^[\s•\-–—*.·]*$")  # empty / punctuation-only fragments


def parse_blocks(text: str) -> list[dict]:
    """Turn `pdftotext -layout` output into paragraph / list blocks.

    Uses leading indentation to join wrapped lines and to nest sub-list items.
    """
    text = text.replace("​", "").replace("\xa0", " ")
    blocks: list[dict] = []
    para: list[str] = []
    items: list[dict] = []
    last_indent = 0

    def flush_para():
        nonlocal para
        if para:
            text = " ".join(para).strip()
            if not JUNK_RE.match(text):
                blocks.append({"type": "p", "text": text})
            para = []

    def flush_list():
        nonlocal items
        clean = [
            {"level": it["level"], "marker": it["marker"], "text": it["text"].strip()}
            for it in items
            if not JUNK_RE.match(it["text"].strip())
        ]
        if clean:
            blocks.append({"type": "list", "items": clean})
        items = []

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped:
            flush_para()
            flush_list()
            last_indent = 0
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        bullet = BULLET_RE.match(stripped)
        ordered = None if bullet else ORDERED_RE.match(stripped)

        if bullet or ordered:
            flush_para()
            marker, body = (("•", bullet.group(2)) if bullet
                            else (ordered.group(1), ordered.group(2)))
            level = 1 if indent >= SUBLEVEL_INDENT else 0
            items.append({"level": level, "marker": marker, "text": body, "indent": indent})
            last_indent = indent
        elif items and indent > last_indent:
            items[-1]["text"] += " " + stripped  # wrapped continuation of current item
        else:
            flush_list()
            para.append(stripped)

    flush_para()
    flush_list()
    return blocks


def _save(im: Image.Image, out_dir: Path, stem: str) -> str:
    has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
    if has_alpha:
        name = f"{stem}.png"
        im.save(out_dir / name, "PNG", optimize=True)
    else:
        name = f"{stem}.jpg"
        im.convert("RGB").save(out_dir / name, "JPEG", quality=85, optimize=True)
    return name


def _split_grid(im: Image.Image) -> dict[str, Image.Image]:
    """Split a 2x2 grid into four quadrants, trimming the center gutter."""
    w, h = im.size
    gx, gy = max(2, round(w * 0.006)), max(2, round(h * 0.006))
    mx, my = w // 2, h // 2
    return {
        "a": im.crop((0, 0, mx - gx, my - gy)),
        "b": im.crop((mx + gx, 0, w, my - gy)),
        "c": im.crop((0, my + gy, mx - gx, h)),
        "d": im.crop((mx + gx, my + gy, w, h)),
    }


def extract_images(pdf: str, slug: str, out_dir: Path) -> list[str]:
    for old in out_dir.glob(f"{slug}-*"):
        old.unlink()
    tmp = out_dir / ".tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)

    subprocess.run(["pdfimages", "-all", pdf, str(tmp / "img")], check=True)

    images: list[str] = []
    seen: set[str] = set()
    idx = 1
    for f in sorted(tmp.iterdir()):
        try:
            im = Image.open(f)
            im.load()
        except Exception:
            continue
        w, h = im.size
        if min(w, h) < MIN_IMG_DIM:
            continue
        if im.mode == "1":  # bilevel — almost always a mask / scanned text layer
            continue
        digest = hashlib.md5(im.tobytes()).hexdigest()
        if digest in seen:
            continue
        seen.add(digest)

        if max(im.size) > MAX_IMG_DIM:
            im.thumbnail((MAX_IMG_DIM, MAX_IMG_DIM), Image.LANCZOS)

        stem = f"{slug}-{idx:02d}"
        if stem in GRID_STEMS:
            for q, quad in _split_grid(im).items():
                images.append(_save(quad, out_dir, f"{stem}-{q}"))
        else:
            images.append(_save(im, out_dir, stem))
        idx += 1

    shutil.rmtree(tmp)
    return images


def register(slug: str, title: str):
    index_path = DOCS / "index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {}
    index[slug] = title
    index = dict(sorted(index.items()))
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    pdf, slug, title = sys.argv[1], sys.argv[2], sys.argv[3]
    out_dir = DOCS / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    raw = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    blocks = parse_blocks(raw)
    images = extract_images(pdf, slug, out_dir)

    manifest = {"slug": slug, "title": title, "blocks": blocks, "images": images}
    (DOCS / f"{slug}.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    register(slug, title)

    print(f"{slug}: {len(blocks)} block(s), {len(images)} image(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

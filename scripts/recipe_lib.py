"""Shared parsing for recipe markdown files (stdlib only)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
IMAGES = ROOT / "images"


def parse_header(text):
    """Return (meta, body) from a file with a --- header block."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    meta = {}
    for line in text[3:end].splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        val = val.split("  #")[0].strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        meta[key.strip()] = val
    body = text[end + 4:].lstrip("\n")
    return meta, body


def parse_body(body):
    """Split the markdown body into intro and named sections."""
    intro, sections, current = [], {}, None
    for line in body.splitlines():
        if line.startswith("# ") and current is None and not intro:
            continue
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
            continue
        (sections[current] if current else intro).append(line)
    return "\n".join(intro).strip(), sections


def list_items(lines):
    out = []
    for line in lines:
        m = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", line)
        if m:
            out.append(m.group(1).strip())
        elif line.strip() and out and line.startswith("  "):
            out[-1] += " " + line.strip()
    return [x for x in out if x]


def load_recipes(include_retired=False):
    recipes = []
    for f in sorted(RECIPES.glob("*.md")):
        meta, body = parse_header(f.read_text(encoding="utf-8"))
        if not include_retired and meta.get("status") == "retired":
            continue
        intro, sections = parse_body(body)
        slug = f.stem
        img_dir = IMAGES / slug
        images = sorted(p.name for p in img_dir.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")) if img_dir.is_dir() else []
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        recipes.append({
            "slug": slug,
            "file": f.name,
            "meta": meta,
            "tags": tags,
            "intro": intro,
            "ingredients": list_items(sections.get("ingredients", [])),
            "steps": list_items(sections.get("steps", [])),
            "notes": list_items(sections.get("notes", [])),
            "images": images,
        })
    return recipes

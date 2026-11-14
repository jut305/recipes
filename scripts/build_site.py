#!/usr/bin/env python3
"""Build the cookbook website into dist/ from recipes/*.md and images/ (stdlib only).

Netlify runs this on every push (see netlify.toml). Locally:
    python3 scripts/build_site.py && open dist/index.html
"""
import json
import shutil

from recipe_lib import IMAGES, ROOT, load_recipes

DIST = ROOT / "dist"
TEMPLATE = ROOT / "site" / "template.html"


def main():
    recipes = load_recipes()
    data = []
    for r in recipes:
        m = r["meta"]
        data.append({
            "slug": r["slug"],
            "title": m.get("title") or r["slug"].replace("-", " ").title(),
            "course": (m.get("course") or "").lower(),
            "cuisine": m.get("cuisine") or "",
            "tags": r["tags"],
            "from": m.get("from") or "",
            "servings": m.get("servings") or "",
            "total_time": m.get("total_time") or "",
            "source": m.get("source") or "",
            "status": m.get("status") or "active",
            "made": str(m.get("made", "")).lower() == "true",
            "rating": m.get("rating") or "",
            "added": m.get("added") or "",
            "intro": r["intro"],
            "ingredients": r["ingredients"],
            "steps": r["steps"],
            "notes": r["notes"],
            "images": [f"images/{r['slug']}/{name}" for name in r["images"]],
        })

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__RECIPES__*/[]", payload)
    (DIST / "index.html").write_text(html, encoding="utf-8")

    for r in recipes:
        if r["images"]:
            dest = DIST / "images" / r["slug"]
            dest.mkdir(parents=True, exist_ok=True)
            for name in r["images"]:
                shutil.copy2(IMAGES / r["slug"] / name, dest / name)

    print(f"dist/: {len(data)} recipes")


if __name__ == "__main__":
    main()

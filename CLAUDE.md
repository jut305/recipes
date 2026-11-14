# Recipe Box — rules for Claude

This repo is Justin's recipe database. Claude is the only interface: Justin sends
notes, photos, links, screenshots or rough descriptions in chat, and Claude files
them here, keeps them consistent, and answers questions from them. Follow these
rules every time so the collection stays searchable.

## Layout

```
recipes/<slug>.md        one file per recipe (flat; no category folders)
images/<slug>/           photos for that recipe (source page, finished dish)
templates/recipe.md      the format every recipe follows
scripts/build_index.py   regenerates INDEX.md from the recipe headers
INDEX.md                 generated catalogue — never edit by hand
```

- **Slug:** lowercase, hyphenated, descriptive: `green-chile-pork-stew.md`.
  If the slug already exists for a different dish, add a qualifier
  (`chili-moms.md`, `chili-smoked-brisket.md`).
- Categories live in the header (`course`, `cuisine`, `tags`), not in folders,
  so a recipe can belong to several at once.

## Tags and people

- **Tags** are lowercase and hyphenated, and cover what Justin would search by:
  main protein or ingredient (`salmon`, `halibut`), method (`grill`, `smoker`,
  `instant-pot`), occasion (`weeknight`, `party`, `holiday`), and traits
  (`make-ahead`, `freezer`, `spicy`, `kid-friendly`). Aim for 3–8 per recipe.
- Before inventing a tag, list the existing ones
  (`grep -h '^tags:' recipes/*.md`) and reuse a match: `bbq` not a second
  `barbecue`.
- **Recipes from a person** ("Becca's poke"): put the name in `from:`
  (`from: Becca`), add the tag `from-becca`, and use the possessive in the title
  and slug: `title: Becca's Poke`, `recipes/beccas-poke.md`. Keep the name
  spelled exactly as Justin spells it, and reuse it consistently.
- "Becca's recipes" or "what did Becca give me?" → search `from:`.

## Adding a recipe

1. `git pull` first.
2. Search `recipes/` for the same dish (title, key ingredients). If a match
   exists, update that file instead of creating a duplicate, and say so.
3. Build the file from `templates/recipe.md`. Fill every header field you can;
   leave unknowns empty instead of guessing. Never invent quantities, times or
   temperatures that the source doesn't give — put `?` and mention it.
4. From a photo or scan: transcribe faithfully, then normalise formatting
   (ingredient list, numbered steps). Save the original image to
   `images/<slug>/source-1.jpg` (and -2, -3…) and link it under **Source**.
5. From a link: record the URL in `source`. Write the recipe in Claude's own
   words as a working kitchen version (ingredients + concise steps), not a copy
   of the page's prose.
6. Justin's own comments ("too salty, halve the soy", "Barbara's version") go
   under **Notes**, dated, verbatim where possible.
7. Run `python3 scripts/build_index.py`, then commit and push:
   `git add -A && git commit -m "Add: <title>" && git push`.

## Updating a recipe

- Edit in place; add a dated line under **Notes** describing the change
  (e.g. `- 2026-11-20: cut sugar to 1/2 cup — better`).
- Bump `updated:` in the header. Rebuild the index, commit `Update: <title>`.
- Mark a recipe Justin has actually cooked with `made: true` and add `rating`
  (1–5) if he gives one.

## Answering questions

- `git pull`, then search the header fields and bodies (grep is fine).
- Answer from the files; name the recipes used. If nothing matches, say so —
  then optionally suggest from general knowledge, clearly labelled as not from
  the collection.
- Units: keep the source's units; convert on request.

## Commit hygiene

- One recipe per commit where practical. Messages: `Add:`, `Update:`, `Fix:`.
- Don't delete recipes unless Justin asks; set `status: retired` instead.

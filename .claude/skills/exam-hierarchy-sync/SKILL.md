---
name: exam-hierarchy-sync
description: Find real exam/question papers for a topic (e.g. "Solar System Div B 2025"), download them into a readable local archive, extract the entities they discuss, and merge any missing ones into a hierarchy.json knowledge graph with correctly linked relationships. Use when the user asks to sync, refresh, cross-check, or update a hierarchy against recent exams/question papers, or asks "does our hierarchy cover everything on this year's test."
---

# Exam → Hierarchy Sync

Keeps a `hierarchy.json` knowledge graph (entities + relationships + a
grouped hierarchy tree, see schema below) up to date with what real exam
papers for a topic actually test. This mirrors work already validated on
this repo's Science Olympiad "Solar System" hierarchy — reuse that judgment,
don't rediscover it from scratch each run.

## Inputs

Parse from the invocation (`args`) or ask the user if ambiguous:
1. **Topic / search scope** - e.g. "Science Olympiad Division B Solar System
   2025-2026". Be specific about division/level and season year; question
   papers for the same nominal topic vary a lot by season.
2. **Target hierarchy.json path** - default to a `hierarchy.json` at the repo
   root if exactly one exists; ask if there are zero or multiple.

## Step 1 — Find real papers, don't guess

Use WebSearch (and WebFetch on promising result pages) to find actual
downloadable papers. Search variations that have worked well:
- `"<topic>" test pdf`
- `"<topic>" "<division>" <season> test pdf`
- `"<topic>" filetype:pdf`

Prioritize, in order:
1. The official governing body's site (e.g. `soinc.org` for Science
   Olympiad) — look for an official "event guide + practice test" bundle;
   these are often a `.zip` containing an exam, an answer key, and an image
   set. **The answer key matters as much as the exam** — many questions
   reference "Image 3" or "the object shown" without naming it in the
   question text; the entity name only appears in the key.
2. Named invitational tournament tests hosted on stable domains (university
   sites, `chandra.harvard.edu`, etc.) with direct PDF links.
3. Community archives (e.g. `scioly.org` test exchange) — expect some links
   to be dead or access-denied; don't burn time retrying a page that returns
   an access-denied error.

Deprioritize/avoid Scribd, Studocu, Quizlet, and other user-upload sites
unless nothing better exists — they're frequently paywalled, unverified, or
mis-scanned.

If nothing recent is found for the exact season requested, say so
explicitly and fall back to the most recent available season rather than
silently substituting — the user should know if "2025" resolved to a 2023
paper.

## Step 2 — Download into a readable archive

Store under `data/raw/question_papers/<topic-slug>/<source-slug>/`, e.g.:

```
data/raw/question_papers/
  solar-system-div-b/
    soinc-official-2025-2026-sample-test/
      SS-Exam.pdf
      SS-Key.pdf
      SS-EventGuide.pdf
      SS-Images.pdf
    wichita-state-national-exam-2023/
      test.pdf
```

Before downloading, `curl -sL -o /dev/null -w "%{http_code} %{content_type}"`
the URL to confirm it's actually a PDF/zip (200, right content-type) rather
than an HTML error page — search engines return dead links often enough
that this check is worth the round trip. Unzip archives in place. Skip
re-downloading a file that's already present with the same name (idempotent
re-runs).

## Step 3 — Extract text

No PDF tooling is assumed to be installed. Use the bundled helpers instead
of adding project dependencies:

```bash
PY=$(bash .claude/skills/exam-hierarchy-sync/scripts/setup_pdf_env.sh)
$PY .claude/skills/exam-hierarchy-sync/scripts/extract_pdf_text.py <file.pdf> > /tmp/out.txt
```

`setup_pdf_env.sh` creates/reuses an isolated venv at
`~/.cache/exam-hierarchy-sync/venv` (override with
`EXAM_HIERARCHY_SYNC_VENV`) — this never touches system Python or adds to
`requirements.txt`. Extract the exam, the key, and the event guide
separately; read them together since the key is often where entity names
actually appear.

## Step 4 — Extract candidate entities, judge what belongs

Read the extracted text yourself (don't shell out to a second model) and
list every concrete, named thing the paper tests:
- named celestial bodies (planets, moons, dwarf planets, comets, asteroids,
  KBOs, exoplanets, host stars, star systems)
- named surface/atmospheric features and terrain types
- spacecraft missions and observatories/instruments
- named theories/models

Match the granularity already present in the existing `entities[].type`
values — reuse a `type` string that already exists whenever a new entity
fits it, and only introduce a new one when nothing existing applies.

**Deliberately exclude** generic pedagogical/physics vocabulary that isn't
a distinct named entity (e.g. "gravitational force," "blueshift," "the
electromagnetic spectrum," generic acronyms like "RTG" used as a concept
rather than a named thing) — these clutter the graph without adding
retrievable knowledge-store value. Tell the user what category of thing you
excluded and why, so they can ask for it explicitly if they disagree.

Then diff your candidate list against `entities[].name` **and** all
`aliases[].aliases` in the current hierarchy (case-insensitive) to find
what's genuinely missing. Don't re-add something already present under an
alias.

## Step 5 — Merge, using the script — never hand-edit the JSON

`hierarchy.json` files in this project have previously shipped with
malformed relationship entries (a bare relation string instead of a
`"relation"` key) — `merge_hierarchy.py` auto-repairs that pattern before
parsing, so a still-broken file won't block you, but don't rely on that as
a substitute for keeping the file valid going forward.

Write your additions to a scratch JSON file matching this shape:

```json
{
  "entities": [{"id": "...", "name": "...", "type": "...", "description": "..."}],
  "relationships": [{"subject": "...", "relation": "...", "object": "...", "confidence": 0.9}],
  "aliases": [{"canonical": "...", "aliases": ["..."]}],
  "hierarchy_sections": [{"title": "...", "children": ["entity_id", "..."]}]
}
```

Conventions to follow, matching the existing file:
- `id`: `snake_case`, prefixed by a short type hint (`moon_`, `mission_`,
  `feature_`, `theory_`, `exoplanet_`, `star_`, ...).
- `relation`: reuse an existing verb (`contains`, `orbits`, `has_satellite`,
  `visited`, `depends_on`, `studied`, `formed_from`) before inventing a new
  one; `located_on`, `observed`, and `classified_as` have already been
  introduced for features/observatories/exoplanet-class links and are safe
  to reuse.
- Every relationship must reference `id`s that exist (either already in the
  hierarchy or newly added in the same batch) — the merge script will
  refuse to write otherwise.
- Group new entities into one or more `hierarchy_sections`; if a section
  with the same `title` already exists, your children are appended into it
  rather than creating a duplicate section (safe to re-run).

Then run:

```bash
python3 .claude/skills/exam-hierarchy-sync/scripts/merge_hierarchy.py <hierarchy.json> <additions.json>
```

It validates (no duplicate ids, no dangling references) before writing, and
reports exactly what was added vs. skipped as already-present.

## Step 6 — Report back

Summarize for the user: which papers were used (with source URLs and local
paths), counts of new entities/relationships by category, anything
intentionally excluded and why, and whether the target hierarchy.json
needed the relation-key bug repaired. Don't commit anything — leave the
result staged for the user to review and commit themselves.

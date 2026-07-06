# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A knowledge store / ingestion pipeline that crawls sources on a topic, extracts and cleans text, chunks it, scores relevance, and derives a topic hierarchy from it. The current concrete use case (see `docs/scope.md`) is building a knowledge store for the **Science Olympiad Division B "Solar System" 2026** event. The `solar-system` branch (an actually-running crawl→extract→chunk→relevance→hierarchy pipeline) was merged into `main` on top of an in-progress **generic, topic-agnostic trainer** effort (`src/pipeline/knowledge_store_builder.py`), so `main` now contains both side by side — see "Architecture" below for how they relate and where each is broken.

## Setup & running

```bash
pip install -r requirements.txt

# Run the wired part of the crawl pipeline (crawl -> extract -> chunk)
python src/run_pipeline.py
```

Run it as `python src/run_pipeline.py` from the repo root, **not** `python -m src.run_pipeline` — the stage modules (`crawler.crawler`, `extractor.extractor`, `processor.chunker`) are imported unqualified (e.g. `from crawler.crawler import Crawler`), which only resolves because running a script directly puts its own directory (`src/`) on `sys.path`. The old `-m src.run_pipeline` invocation from this repo's earlier history no longer works.

There is no test suite, linter config, or build step in this repo.

`data/output/*.json` (10 files: `sources.json`, `chunks.json`, `relevant_chunks.json`, `relevance_report.json`, `candidate_topics.json`, `canonical_topics.json`, `topic_hierarchy_v1.json`, `topic_hierarchy_draft.json`, `refined_syllabus_draft.json`, `scope_validation.json`) are **committed to the repo**, not gitignored — the `solar-system` branch dropped the `data/output/*` line from `.gitignore` when it merged. `data/raw/*` and `data/processed/*` are still gitignored. Several of these committed files are stale snapshots with no current script that reproduces them (see the "missing stage" note below) — don't assume regenerating the pipeline will reproduce them byte-for-byte.

Only three stages are wired together by `run_pipeline.py` (crawl → extract → chunk). Everything past chunking is a standalone script, run manually, each reading/writing hardcoded `data/output/...` or `data/processed/...` paths — and **not** all of them agree on how they expect to be invoked:

```bash
# Chunks -> relevance-scored/filtered chunks + a report (writes data/output/relevant_chunks.json, relevance_report.json)
# Must be run with relevance/ itself as the working directory - it does `from relevance_engine import RelevanceEngine`,
# a same-directory import, not a package-qualified one:
cd src/relevance && python filter_chunks.py && cd -

# candidate_topics.json -> canonical_topics.json (topic name cleanup/merging)
python src/hierarchy/canonicalizer.py

# canonical_topics.json -> topic_hierarchy_v1.json (buckets topics into a fixed category tree)
python src/hierarchy/hierarchy_generator.py

# topic_hierarchy_v1.json -> scope_validation.json (rule-based in/out-of-scope check against a hardcoded whitelist)
python src/hierarchy/scope_validator.py
```

**There is currently no script that produces `data/output/candidate_topics.json`.** The topic-extraction step that used to generate it (`src/topic_extractor.py`) was deleted by the `solar-system` merge, and no replacement was added — `src/hierarchy/canonicalizer.py` just assumes the file already exists. The checked-in `candidate_topics.json` is a snapshot from before that deletion, not something you can regenerate from current code. If you're asked to fix or extend topic extraction, this gap is probably why.

## Architecture

### The wired crawl pipeline (`src/run_pipeline.py` + `src/crawler/`, `src/extractor/`, `src/processor/`)

```
SEED_URLS (hardcoded in src/run_pipeline.py)
  → Crawler.crawl        (src/crawler/crawler.py: BFS over links, filtered by an inline
                           ALLOWED_DOMAINS set and an inline KEYWORDS set - both duplicate,
                           slightly different copies of what src/config.py used to own)
  → Extractor.extract     (src/extractor/extractor.py: trafilatura only, HTML text only)
  → Chunker.split_text    (src/processor/chunker.py: 500-word chunks, no overlap)
  → writes data/output/sources.json and data/output/chunks.json
```

Compared to what CLAUDE.md previously documented here, note what's now gone:
- **No HTML/PDF/YouTube/social triage.** The Link Classification table that used to live in `docs/architecture.md` (HTML→process, PDF→process, YouTube→defer, social→ignore) has no code implementing it anymore — `Crawler.crawl` only filters by domain + keyword match and always attempts an HTML fetch; there's no PDF handling and no special-casing of YouTube links. `docs/scope.md` still describes the intended HTML/PDF/YouTube/social policy, but the code doesn't enforce it.
- **No `event`/`division`/`season_year` tagging.** The old `run_pipeline.py` attached `EVENT_SCOPE` metadata (`event`, `division`, `season_year`) to every source/chunk record. The new `Chunker.process_documents` output shape is just `{chunk_id, url, text}` — none of that tagging happens. If you're asked to extend this pipeline, check `docs/scope.md` before assuming it's fine that this tagging is gone; it looks like an unintentional regression from the merge, not a deliberate scope change.
- **`src/config.py` (`EVENT_SCOPE`, `ALLOWED_DOMAINS`, `IGNORED_DOMAINS`) is now orphaned** — nothing imports it. `Crawler`, `RelevanceEngine`, and `scope_validator.py` each hardcode their own separate domain/keyword/topic-whitelist constants instead of sharing one source of truth.

Downstream of chunking (not wired into `run_pipeline.py`, run manually, in order):
- `src/relevance/relevance_engine.py` + `filter_chunks.py` — scores each chunk via hardcoded `CORE_TERMS`/`OUT_OF_SCOPE` term lists (+5/-15 per mention), classifies `high`/`medium`/`low`, keeps `high`+`medium`.
- `src/hierarchy/canonicalizer.py` — merges near-duplicate topic names via a hardcoded `CANONICAL_MAP` and drops noise via `BAD_TOPICS`. (Reads `candidate_topics.json`, which nothing currently produces — see above.)
- `src/hierarchy/hierarchy_generator.py` — buckets canonical topics into a fixed `CATEGORY_MAPPING` tree (Planets / Dwarf Planets & Small Bodies / Moons / Planet Formation / Orbital Mechanics / Space Missions / History of Astronomy / Uncategorized).
- `src/hierarchy/scope_validator.py` — the "rule-based whitelist validator": classifies every topic in the hierarchy as `IN_SCOPE`/`LIKELY_IN_SCOPE`/`REVIEW`/`OUT_OF_SCOPE`/`NOISE` against hardcoded `SOLAR_SYSTEM_CORE_TOPICS`/`KNOWN_MOONS`/`DISCOVERER_NAMES`/pattern lists, and computes an overall `scope_score`.

### The in-progress generic builder (`src/pipeline/`)

A `KnowledgeStoreState` dataclass (`src/pipeline/state.py`) threaded through a `KnowledgeStoreBuilder` class (`src/pipeline/knowledge_store_builder.py`) with stages: scope → refine scope → generate queries → acquire documents → process → filter relevance → extract topics → canonicalize topics → generate hierarchy → build graph. Most stages past query generation are still `# TODO` stubs.

Before the merge, this module couldn't even import (`scope.scope_builder`, `scope.scope_refiner`, `search.query_generator` didn't exist). They exist now (`src/scope/scope_builder.py`, `src/scope/scope_refiner.py`, `src/search/query_generator.py`, all added by the `solar-system` merge) — but the builder still doesn't run, for a different reason:
- `KnowledgeStoreBuilder.build_scope` calls `self.scope_builder.build_scope(...)`, but `ScopeBuilder` only defines `.build(...)` — an `AttributeError` waiting to happen.
- Even fixing that name, `ScopeBuilder.build()` returns `{raw_query, normalized_query, tokens}`, while `QueryGenerator.generate()` expects `refined_scope["scope"]["topic"]`/`["domain"]`/`["year"]` — a shape `ScopeBuilder` never produces. The three modules were evidently written independently against different assumed schemas.
- `knowledge_store_builder.py`'s `__main__` block also still has a pre-existing indentation/syntax error, independent of the above.

Treat `src/pipeline/` as the target architecture being built out incrementally, not working code — but note it's now one dependency-fix and one schema-alignment away from at least running the scope/query stages, which wasn't true before the merge.

When asked to extend ingestion/topic logic, check which of these two you're being asked to work in.

## Scope discipline (docs/scope.md)

The Solar System knowledge store is deliberately scoped to the **2026** event version — sources, chunks, and topics are meant to be tagged/linked to `season_year: 2026` because the Science Olympiad event focus changes yearly. As noted above, the current chunking code doesn't actually do this tagging anymore; check `docs/scope.md` before deciding whether to restore it or treat its removal as intentional.

Current phase is **text-only**: HTML and PDF are meant to be in scope, YouTube/video and image-only resources deferred, social/store/login/unrelated links ignored — but (again, see above) the current `Crawler` doesn't implement this triage at all, it only does domain+keyword filtering. `docs/scope.md` is still the source of truth for the intended policy; the code has drifted from it.

## Other branches

`origin/solar-system` was merged into `main` in this history (merge commit `Merge branch 'solar-system'`) — its crawler/extractor/chunking pipeline, hierarchy validator, and rule-based whitelist validator are now part of `main` directly (see "Architecture" above). There should be no need to go looking at that branch separately anymore; if you find yourself about to reimplement crawler/validator logic from scratch, it's almost certainly already here under `src/crawler/`, `src/hierarchy/`, or `src/relevance/`.

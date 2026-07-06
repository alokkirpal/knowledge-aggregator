#!/usr/bin/env python3
"""
Merge a batch of new entities/relationships/aliases/hierarchy sections into a
hierarchy.json knowledge graph, safely and idempotently.

Usage:
    python3 merge_hierarchy.py <hierarchy.json> <additions.json>

<additions.json> shape:
{
  "entities": [ {"id": ..., "name": ..., "type": ..., "description": ...}, ... ],
  "relationships": [ {"subject": ..., "relation": ..., "object": ..., "confidence": ...}, ... ],
  "aliases": [ {"canonical": ..., "aliases": [...]}, ... ],
  "hierarchy_sections": [
      {"title": "...", "children": ["entity_id_1", "entity_id_2", ...]},
      ...
  ]
}

Behavior:
- Auto-repairs the historically recurring bug where relationship objects were
  written as {"subject": ..., "<relation>", "object": ...} (bare string instead
  of a "relation" key) before parsing, so a still-broken hierarchy.json doesn't
  block a merge.
- Entities are de-duped by id; an id that already exists is left untouched
  (existing description/type wins) and reported as skipped.
- Relationships are de-duped by the (subject, relation, object) triple.
- Aliases are merged per canonical name, de-duping the alias list.
- hierarchy_sections are appended as new top-level children of the
  hierarchy tree, expanding each id into the same stub shape used elsewhere
  in the file ({id, name, type, description}).
- Refuses to write if the merged result would contain dangling
  subject/object references or duplicate entity ids.
"""
import json
import re
import sys


def load_hierarchy(path):
    text = open(path, encoding="utf-8").read()
    pattern = re.compile(r'("subject": "[^"]+",\n\s+)"([a-zA-Z_]+)",(\n\s+"object")')
    fixed, n = pattern.subn(r'\1"relation": "\2",\3', text)
    if n:
        print(f"[merge_hierarchy] auto-repaired {n} malformed relationship entr{'y' if n == 1 else 'ies'} "
              f"(bare relation string -> \"relation\" key)")
    return json.loads(fixed)


def merge(hierarchy, additions):
    entity_by_id = {e["id"]: e for e in hierarchy["entities"]}
    existing_names_lower = {e["name"].strip().lower() for e in hierarchy["entities"]}
    for alias_entry in hierarchy.get("aliases", []):
        existing_names_lower.update(a.strip().lower() for a in alias_entry.get("aliases", []))

    added_entities, skipped_entities = [], []
    for e in additions.get("entities", []):
        if e["id"] in entity_by_id:
            skipped_entities.append(e["id"])
            continue
        if e["name"].strip().lower() in existing_names_lower:
            print(f"[merge_hierarchy] WARNING: '{e['name']}' (id={e['id']}) matches an existing "
                  f"entity/alias name under a different id - check for a duplicate before relying on this entry")
        hierarchy["entities"].append(e)
        entity_by_id[e["id"]] = e
        added_entities.append(e["id"])

    existing_rel_keys = {(r["subject"], r["relation"], r["object"]) for r in hierarchy["relationships"]}
    added_relationships = []
    for r in additions.get("relationships", []):
        key = (r["subject"], r["relation"], r["object"])
        if key in existing_rel_keys:
            continue
        if r["subject"] not in entity_by_id or r["object"] not in entity_by_id:
            raise ValueError(f"relationship references unknown entity id: {r}")
        hierarchy["relationships"].append(r)
        existing_rel_keys.add(key)
        added_relationships.append(key)

    alias_by_canonical = {a["canonical"]: a for a in hierarchy.get("aliases", [])}
    added_aliases = []
    for a in additions.get("aliases", []):
        canonical = a["canonical"]
        if canonical in alias_by_canonical:
            current = set(alias_by_canonical[canonical]["aliases"])
            new = [x for x in a["aliases"] if x not in current]
            alias_by_canonical[canonical]["aliases"].extend(new)
        else:
            hierarchy.setdefault("aliases", []).append(a)
            alias_by_canonical[canonical] = a
        added_aliases.append(canonical)

    def stub(entity_id):
        e = entity_by_id[entity_id]
        return {"id": e["id"], "name": e["name"], "type": e["type"], "description": e["description"]}

    section_by_title = {c["title"]: c for c in hierarchy["hierarchy"]["children"] if "title" in c}
    added_sections = []
    for section in additions.get("hierarchy_sections", []):
        missing = [i for i in section["children"] if i not in entity_by_id]
        if missing:
            raise ValueError(f"hierarchy_section '{section['title']}' references unknown entity ids: {missing}")
        if section["title"] in section_by_title:
            target = section_by_title[section["title"]]
            present_ids = {c["id"] for c in target["children"]}
            target["children"].extend(stub(i) for i in section["children"] if i not in present_ids)
        else:
            new_section = {"title": section["title"], "children": [stub(i) for i in section["children"]]}
            hierarchy["hierarchy"]["children"].append(new_section)
            section_by_title[section["title"]] = new_section
        added_sections.append(section["title"])

    return {
        "added_entities": added_entities,
        "skipped_entities": skipped_entities,
        "added_relationships": len(added_relationships),
        "added_aliases": added_aliases,
        "added_sections": added_sections,
    }


def validate(hierarchy):
    ids = [e["id"] for e in hierarchy["entities"]]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate entity ids after merge: {dupes}")
    id_set = set(ids)
    dangling = [r for r in hierarchy["relationships"] if r["subject"] not in id_set or r["object"] not in id_set]
    if dangling:
        raise ValueError(f"dangling relationship references after merge: {dangling}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    hierarchy_path, additions_path = sys.argv[1], sys.argv[2]

    hierarchy = load_hierarchy(hierarchy_path)
    additions = json.load(open(additions_path, encoding="utf-8"))

    report = merge(hierarchy, additions)
    validate(hierarchy)

    with open(hierarchy_path, "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=4)
        f.write("\n")

    print(f"[merge_hierarchy] added {len(report['added_entities'])} entities: {report['added_entities']}")
    if report["skipped_entities"]:
        print(f"[merge_hierarchy] skipped {len(report['skipped_entities'])} already-present ids: "
              f"{report['skipped_entities']}")
    print(f"[merge_hierarchy] added {report['added_relationships']} relationships")
    print(f"[merge_hierarchy] touched aliases for: {report['added_aliases']}")
    print(f"[merge_hierarchy] added hierarchy sections: {report['added_sections']}")
    print(f"[merge_hierarchy] total entities: {len(hierarchy['entities'])}, "
          f"total relationships: {len(hierarchy['relationships'])}")


if __name__ == "__main__":
    main()

import json

with open("data/output/sources.json") as f:
    sources = json.load(f)

print(f"Sources discovered: {len(sources)}")
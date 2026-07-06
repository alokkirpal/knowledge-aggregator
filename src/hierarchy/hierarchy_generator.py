import json

ROOT = "Solar System 2026"

CATEGORY_MAPPING = {
    "Planets": {
        "Mercury",
        "Venus",
        "Earth",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune"
    },

    "Dwarf Planets & Small Bodies": {
        "Pluto",
        "Ceres",
        "Kuiper Belt",
        "Oort Cloud",
        "Trojan"
    },

    "Moons": {
        "Europa",
        "Ganymede",
        "Callisto",
        "Titan",
        "Enceladus",
        "Charon",
        "Mimas",
        "Tethys",
        "Dione",
        "Atlas",
        "Pandora",
        "Styx"
    },

    "Planet Formation": {
        "Planet Formation",
        "Hot Jupiters",
        "Hot Neptunes"
    },

    "Orbital Mechanics": {
        "Orbital Period",
        "Planetary Motion",
        "Resonance",
        "Kepler",
        "Kepler's Laws"
    },

    "Space Missions": {
        "Voyager",
        "Cassini",
        "Juno",
        "New Horizons",
        "Huygens"
    },

    "History of Astronomy": {
        "Galileo",
        "Nicholas Copernicus",
        "Tycho Brahe",
        "Herschel"
    }
}


def load_topics():
    with open(
        "data/output/canonical_topics.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def build_hierarchy(topics):
    hierarchy = {
        "name": ROOT,
        "children": []
    }

    categorized = set()

    for category, known_topics in CATEGORY_MAPPING.items():

        node = {
            "name": category,
            "children": []
        }

        for topic in topics:

            topic_name = topic["topic"]

            if topic_name in known_topics:

                node["children"].append({
                    "name": topic_name,
                    "mentions": topic["mentions"]
                })

                categorized.add(topic_name)

        if node["children"]:
            hierarchy["children"].append(node)

    uncategorized = []

    for topic in topics:

        if topic["topic"] not in categorized:

            uncategorized.append({
                "name": topic["topic"],
                "mentions": topic["mentions"]
            })

    hierarchy["children"].append({
        "name": "Uncategorized",
        "children": uncategorized
    })

    return hierarchy


def save_hierarchy(hierarchy):

    with open(
        "data/output/topic_hierarchy_v1.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            hierarchy,
            f,
            indent=2,
            ensure_ascii=False
        )


if __name__ == "__main__":

    topics = load_topics()

    hierarchy = build_hierarchy(topics)

    save_hierarchy(hierarchy)

    print(
        "Hierarchy saved to "
        "data/output/topic_hierarchy_v1.json"
    )
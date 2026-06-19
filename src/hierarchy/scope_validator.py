import json
from collections import defaultdict

SUSPICIOUS_PATTERNS = [

    "starter",
    "stack",
    "packet",
    "practice",
    "committee",
    "created",
    "textbook",
    "guide"
]

KNOWN_MOONS = {

    "Atlas",
    "Styx",
    "Pandora",
    "Laomedeia",
    "Psamathe"
}

DISCOVERER_NAMES = {

    "Holman",
    "Lassell",
    "Showalter",
    "Sheppard",
    "Hall",
    "Tempel",
    "Weaver"
}

SCOPE_PATTERNS = [

    "planet",
    "moon",
    "asteroid",
    "comet",

    "orbit",
    "orbital",

    "formation",
    "evolution",

    "mission",

    "satellite",

    "solar",

    "jupiter",
    "saturn",
    "mars",
    "venus",
    "mercury",
    "uranus",
    "neptune",
    "pluto",

    "europa",
    "ganymede",
    "callisto",
    "titan",

    "voyager",
    "cassini",
    "juno",
    "kepler",
    "galileo"
]


OUT_OF_SCOPE_PATTERNS = [

    "black hole",
    "supernova",
    "neutron star",

    "dark matter",
    "dark energy",

    "galaxy",
    "galaxies",

    "cosmology",

    "big bang",

    "string theory",

    "quantum"
]

SOLAR_SYSTEM_CORE_TOPICS = {

    # Planets
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",

    # Dwarf planets
    "Pluto",
    "Ceres",
    "Eris",
    "Haumea",
    "Makemake",
    "Sedna",

    # Small bodies
    "Asteroids",
    "Kuiper Belt",
    "Oort Cloud",
    "Trojan",
    "Arrokoth",
    "Vesta",
    "Itokawa",

    # Moons
    "Moon",
    "Europa",
    "Ganymede",
    "Callisto",
    "Titan",
    "Enceladus",
    "Charon",
    "Mimas",
    "Tethys",
    "Dione",
    "Rhea",
    "Hyperion",
    "Triton",
    "Hydra",
    "Kerberos",
    "Deimos",

    # Formation
    "Planet Formation",
    "Hot Jupiters",
    "Hot Neptunes",
    "Dust",

    # Orbital mechanics
    "Orbital Period",
    "Kepler",
    "Kepler's Laws",
    "Orbital Mechanics",
    "Resonance",
    "Lagrangian",
    "Escape Velocity",

    # Missions
    "Voyager",
    "Cassini",
    "Juno",
    "New Horizons",
    "Huygens",
    "Hubble Space Telescope",

    # History
    "Galileo",
    "Galileo Galilei",
    "Johannes Kepler",
    "Tycho Brahe",
    "Nicholas Copernicus",
    "Herschel",
    "Clyde Tombaugh",
    "Edmond Halley",

    # Solar system science
    "Solar System",
    "The Sun",
    "Hydrogen",
    "Helium",
    "Gas Giants",
    "Inner Planets",
    "Terrestrial Bodies",
    "Extraterrestrial Water",
    "Distance",
    "Diameter",
    "Mass",
    "Positions"
}


KNOWN_NOISE = {

    "This",
    "These",
    "There",
    "Some",
    "Most",
    "However",
    "After",
    "Finally",
    "Very",
    "Their",
    "Because",
    "Since",
    "Later",
    "Even",
    "Note",
    "September",
    "July",
    "Year",
    "Name",
    "Main",
    "University",
    "Microsoft Excel",
    "Practice Test",
    "Recommended Textbook",
    "National Test Packet",
    "National Test Packet Practice",
    "Problems",
    "Tests",
    "Learning",
    "Links"
}

def classify_topic(topic):

    topic_lower = topic.lower()

    if topic in KNOWN_NOISE:

        return (
            "NOISE",
            "Known noise topic"
        )

    if topic in SOLAR_SYSTEM_CORE_TOPICS:

        return (
            "IN_SCOPE",
            "Explicitly known Solar System topic"
        )
    if topic in DISCOVERER_NAMES:

        return (
            "LIKELY_IN_SCOPE",
            "Known astronomy discoverer"
        )
    if topic in KNOWN_MOONS:

        return (
            "IN_SCOPE",
            "Known Solar System moon"
        )
    for pattern in SUSPICIOUS_PATTERNS:

        if pattern in topic_lower:

            return (
                "SUSPICIOUS",
                f"Matched suspicious pattern: {pattern}"
            )

    for pattern in OUT_OF_SCOPE_PATTERNS:

        if pattern in topic_lower:

            return (
                "OUT_OF_SCOPE",
                f"Matched out-of-scope pattern: {pattern}"
            )

    for pattern in SCOPE_PATTERNS:

        if pattern in topic_lower:

            return (
                "LIKELY_IN_SCOPE",
                f"Matched scope pattern: {pattern}"
            )

    return (
        "REVIEW",
        "No rule matched"
    )
def get_all_topics(node):

    topics = []

    children = node.get("children", [])

    for child in children:

        if "children" in child:

            topics.extend(
                get_all_topics(child)
            )

        else:

            topics.append(
                child["name"]
            )

    return topics


def validate_scope(hierarchy):

    topics = get_all_topics(
        hierarchy
    )

    report = {

        "total_topics": len(topics),

        "in_scope": [],

        "likely_in_scope": [],

        "review": [],

        "out_of_scope": [],

        "noise": [],

        "scope_score": 0
    }

    total_score = 0

    for topic in topics:

        status, reason = classify_topic(
            topic
        )

        entry = {

            "topic": topic,

            "reason": reason
        }

        if status == "IN_SCOPE":

            report["in_scope"].append(
                entry
            )

            total_score += 1.0

        elif status == "LIKELY_IN_SCOPE":

            report[
                "likely_in_scope"
            ].append(
                entry
            )

            total_score += 0.8

        elif status == "REVIEW":

            report["review"].append(
                entry
            )

            total_score += 0.3

        elif status == "OUT_OF_SCOPE":

            report[
                "out_of_scope"
            ].append(
                entry
            )

        elif status == "NOISE":

            report["noise"].append(
                entry
            )

    report["scope_score"] = round(

        total_score /

        max(len(topics), 1),

        3
    )

    return report

def print_report(report):

    print("\n" + "=" * 60)
    print("SOLAR SYSTEM SCOPE VALIDATION")
    print("=" * 60)

    print(
        f"\nTotal Topics: {report['total_topics']}"
    )

    print(
        f"In Scope: "
        f"{len(report['in_scope'])}"
    )

    print(
        f"Likely In Scope: "
        f"{len(report['likely_in_scope'])}"
    )

    print(
        f"Review: "
        f"{len(report['review'])}"
    )

    print(
        f"Out Of Scope: "
        f"{len(report['out_of_scope'])}"
    )

    print(
        f"Noise: "
        f"{len(report['noise'])}"
    )



if __name__ == "__main__":

    with open(
        "data/output/topic_hierarchy_v1.json",
        "r",
        encoding="utf-8"
    ) as f:

        hierarchy = json.load(f)

    report = validate_scope(
        hierarchy
    )

    print_report(report)

    with open(
        "data/output/scope_validation.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2
        )

    print(
        "\nSaved report to "
        "data/output/scope_validation.json"
    )
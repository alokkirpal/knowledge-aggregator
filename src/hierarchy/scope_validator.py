import json
from collections import defaultdict


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

    topics = get_all_topics(hierarchy)

    report = {

        "total_topics": len(topics),

        "in_scope": [],

        "out_of_scope": [],

        "unknown": [],

        "scope_score": 0
    }

    for topic in topics:

        if topic in SOLAR_SYSTEM_CORE_TOPICS:

            report["in_scope"].append(topic)

        elif topic in KNOWN_NOISE:

            report["out_of_scope"].append(topic)

        else:

            report["unknown"].append(topic)

    report["scope_score"] = round(

        len(report["in_scope"])
        / max(len(topics), 1),

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
        f"In Scope: {len(report['in_scope'])}"
    )

    print(
        f"Unknown: {len(report['unknown'])}"
    )

    print(
        f"Out Of Scope: {len(report['out_of_scope'])}"
    )

    print(
        f"\nScope Score: "
        f"{report['scope_score']:.3f}"
    )

    print("\n--- Out Of Scope ---")

    for topic in sorted(
        report["out_of_scope"]
    ):
        print(topic)

    print("\n--- Unknown ---")

    for topic in sorted(
        report["unknown"]
    ):
        print(topic)


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
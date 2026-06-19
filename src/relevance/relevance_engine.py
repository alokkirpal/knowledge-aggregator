from collections import Counter


CORE_TERMS = {

    # Event focus
    "solar system",
    "planet formation",
    "planetary evolution",
    "planet structure",

    # Planets
    "mercury",
    "venus",
    "earth",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",

    # Dwarf planets
    "pluto",
    "ceres",
    "eris",
    "haumea",
    "makemake",
    "sedna",

    # Small bodies
    "asteroid",
    "asteroids",
    "comet",
    "comets",
    "kuiper belt",
    "oort cloud",

    # Moons
    "moon",
    "europa",
    "ganymede",
    "callisto",
    "titan",
    "enceladus",
    "charon",
    "triton",

    # Formation / evolution
    "protoplanetary disk",
    "accretion",
    "planetesimal",
    "protoplanet",

    # Orbital mechanics
    "orbital",
    "orbit",
    "kepler",
    "resonance",
    "gravity",

    # Missions
    "voyager",
    "cassini",
    "juno",
    "new horizons",
    "galileo",
    "huygens",

    # Sun
    "sun",
    "hydrogen",
    "helium"
}


OUT_OF_SCOPE = {

    "supernova",
    "supernovae",

    "neutron star",
    "neutron stars",

    "black hole",
    "black holes",

    "dark matter",
    "dark energy",

    "galaxy",
    "galaxies",

    "cosmology",

    "big bang",

    "quantum mechanics",

    "string theory"
}


class RelevanceEngine:

    def score(self, chunk_text):

        text = chunk_text.lower()

        score = 0

        matched_core = []
        matched_out = []

        for term in CORE_TERMS:

            count = text.count(term)

            if count > 0:

                score += count * 5

                matched_core.append(term)

        for term in OUT_OF_SCOPE:

            count = text.count(term)

            if count > 0:

                score -= count * 15

                matched_out.append(term)

        return {

            "score": score,

            "matched_core": matched_core,

            "matched_out_of_scope": matched_out

        }

    def classify(self, score):

        if score >= 25:
            return "high"

        if score >= 10:
            return "medium"

        return "low"
import json

BAD_TOPICS = {
    "This",
    "There",
    "They",
    "When",
    "Where",
    "Also",
    "Some",
    "Many",
    "Mainly",
    "Here",
    "Year",
    "Name",
    "Type",
    "Main",
    "Updated",
    "Links",
    "Problems",
    "Tests",
    "Learning",
    "University",
    "Continuing",
    "Sept",
    "Recommended Textbook",
    "National Test Packet",
    "National Test Packet Practice",
    "Invitational",
    "Practice Test"
}

CANONICAL_MAP = {
    "Kuiper": "Kuiper Belt",
    "Oort": "Oort Cloud",
    "Jovian": "Gas Giants",
    "Planetary Motion": "Orbital Mechanics",
    "Laws": "Kepler's Laws"
}


def canonicalize_topic(topic):
    if topic in BAD_TOPICS:
        return None

    return CANONICAL_MAP.get(topic, topic)


def canonicalize_topics(candidate_topics):
    cleaned = {}

    for priority_group in ["high_priority", "medium_priority"]:

        for item in candidate_topics.get(priority_group, []):

            topic = canonicalize_topic(item["topic"])

            if topic is None:
                continue

            mentions = item["mentions"]

            if topic not in cleaned:
                cleaned[topic] = 0

            cleaned[topic] += mentions

    return cleaned


if __name__ == "__main__":

    with open(
        "data/output/candidate_topics.json",
        "r",
        encoding="utf-8"
    ) as f:
        topics = json.load(f)

    cleaned = canonicalize_topics(topics)

    sorted_topics = sorted(
        cleaned.items(),
        key=lambda x: x[1],
        reverse=True
    )

    output = [
        {
            "topic": topic,
            "mentions": mentions
        }
        for topic, mentions in sorted_topics
    ]

    with open(
        "data/output/canonical_topics.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(output, f, indent=2)

    print(
        f"Generated {len(output)} canonical topics"
    )
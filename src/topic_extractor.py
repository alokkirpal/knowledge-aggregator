import json
import re
from collections import Counter

KNOWN_SOLAR_SYSTEM_TOPICS = {
    "Planet Formation",
    "Nebular Hypothesis",
    "Terrestrial Planets",
    "Gas Giants",
    "Ice Giants",
    "Dwarf Planets",
    "Asteroid Belt",
    "Kuiper Belt",
    "Oort Cloud",
    "Comets",
    "Asteroids",
    "Meteorites",
    "Planetary Atmospheres",
    "Planetary Interiors",
    "Moons",
    "Rings",
    "Orbital Motion"
}
STOPWORDS = {
    "solar",
    "system",
    "science",
    "olympiad",
    "division",
    "event",
    "participants",
    "knowledge",
    "study",
    "page",
    "information",
    "planet"
}


def normalize_topic(topic):
    topic = topic.strip()

    topic = re.sub(r"\s+", " ", topic)

    return topic.title()


def extract_candidate_topics(chunks):
    topic_counter = Counter()

    pattern = re.compile(
        r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b"
    )

    for chunk in chunks:
        content = chunk.get("content", "")

        matches = pattern.findall(content)

        for match in matches:
            topic = normalize_topic(match)

            if len(topic) < 4:
                continue

            if topic.lower() in STOPWORDS:
                continue

            topic_counter[topic] += 1

    return topic_counter


def build_topic_registry(topic_counter):
    high_priority = []
    medium_priority = []

    for topic, count in topic_counter.most_common():
        if count >= 5:
            high_priority.append(
                {
                    "topic": topic,
                    "mentions": count
                }
            )

        elif count >= 2:
            medium_priority.append(
                {
                    "topic": topic,
                    "mentions": count
                }
            )

    return {
        "high_priority": high_priority,
        "medium_priority": medium_priority
    }


def generate_candidate_topics(
        chunk_file,
        output_file):

    with open(chunk_file, "r",
              encoding="utf-8") as f:
        chunks = json.load(f)

    topic_counter = extract_candidate_topics(
        chunks
    )

    registry = build_topic_registry(
        topic_counter
    )

    with open(output_file,
              "w",
              encoding="utf-8") as f:

        json.dump(
            registry,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Generated {len(registry['high_priority'])} "
        f"high-priority topics"
    )

    print(
        f"Generated {len(registry['medium_priority'])} "
        f"medium-priority topics"
    )


if __name__ == "__main__":

    generate_candidate_topics(
        "data/output/chunks.json",
        "data/output/candidate_topics.json"
    )
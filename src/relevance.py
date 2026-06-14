from urllib.parse import urlparse


SOURCE_PRIORITIES = {
    "soinc.org": 10,
    "www.soinc.org": 10,

    "nasa.gov": 9,
    "www.nasa.gov": 9,

    "jpl.nasa.gov": 9,

    "scioly.org": 7,
    "www.scioly.org": 7,
}


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower()


def get_source_priority(url: str) -> int:
    domain = get_domain(url)

    for known_domain, score in SOURCE_PRIORITIES.items():
        if known_domain in domain:
            return score

    return 3


def add_relevance_scores(sources):
    for source in sources:
        source["source_priority"] = get_source_priority(
            source.get("url", "")
        )

    return sources
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from collections import deque
from urllib.parse import urlparse


class Crawler:

    def __init__(self):

        self.visited = set()

    def fetch(self, url):

        try:

            response = requests.get(
                url,
                timeout=20,
                headers={
                    "User-Agent":
                    "KnowledgeStoreBot/1.0"
                }
            )

            response.raise_for_status()

            return response.text

        except Exception as e:

            print(f"Failed: {url}")
            print(e)

            return None

    def extract_links(self, html, base_url):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        links = []

        for a in soup.find_all("a", href=True):

            href = a["href"]

            if href.startswith("http"):

                links.append(href)

        return links

    def crawl(
        self,
        seed_urls,
        max_pages=50
    ):

        sources = []

        queue = deque(seed_urls)

        KEYWORDS = {

            "solar",
            "planet",
            "planetary",

            "jupiter",
            "saturn",
            "mars",
            "venus",
            "mercury",
            "uranus",
            "neptune",

            "pluto",

            "asteroid",
            "comet",

            "kuiper",
            "oort",

            "moon",
            "europa",
            "titan",

            "voyager",
            "cassini",
            "juno",

            "kepler",
            "tess"
        }

        ALLOWED_DOMAINS = {

            "soinc.org",
            "scioly.org",
            "nasa.gov",
            "jpl.nasa.gov",
            "solarsystem.nasa.gov"
        }

        while queue and len(self.visited) < max_pages:

            url = queue.popleft()

            if url in self.visited:
                continue

            self.visited.add(url)

            print(
                f"[{len(self.visited)}] "
                f"{url}"
            )

            html = self.fetch(url)

            if not html:
                continue

            sources.append({

                "url": url,

                "html": html
            })

            links = self.extract_links(
                html,
                url
            )

            for link in links:

                if link in self.visited:
                    continue

                parsed = urlparse(link)

                domain = parsed.netloc.lower()

                if domain.startswith(
                    "www."
                ):
                    domain = domain[4:]

                allowed = any(
                    domain.endswith(d)
                    for d in ALLOWED_DOMAINS
                )

                if not allowed:
                    continue

                link_lower = link.lower()

                relevant = any(
                    keyword in link_lower
                    for keyword in KEYWORDS
                )

                if not relevant:
                    continue

                queue.append(link)

        return sources

if __name__ == "__main__":

    seed_urls = [

        "https://www.soinc.org/solar-system-b",

        "https://scioly.org/wiki/Solar_System"

    ]

    crawler = Crawler()

    sources = crawler.crawl(seed_urls)

    Path(
        "data/output"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        "data/output/sources.json",
        "w"
    ) as f:

        json.dump(
            sources,
            f,
            indent=2
        )

    print(
        f"Saved {len(sources)} sources"
    )
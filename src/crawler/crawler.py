import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path


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

    def crawl(self, seed_urls):

        sources = []

        for url in seed_urls:

            if url in self.visited:
                continue

            self.visited.add(url)

            html = self.fetch(url)

            if not html:
                continue

            sources.append({

                "url": url,

                "html": html

            })

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
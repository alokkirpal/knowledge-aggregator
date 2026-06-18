import json

from crawler.crawler import Crawler
from extractor.extractor import Extractor
from processor.chunker import Chunker


SEED_URLS = [

    "https://www.soinc.org/solar-system-b",

    "https://scioly.org/wiki/Solar_System"

]


def main():

    crawler = Crawler()

    extractor = Extractor()

    chunker = Chunker()

    print("Crawling...")

    sources = crawler.crawl(
        SEED_URLS
    )

    print(
        f"Sources: {len(sources)}"
    )

    print("Extracting...")

    docs = extractor.process_sources(
        sources
    )

    print(
        f"Documents: {len(docs)}"
    )

    print("Chunking...")

    chunks = chunker.process_documents(
        docs
    )

    print(
        f"Chunks: {len(chunks)}"
    )


if __name__ == "__main__":

    main()
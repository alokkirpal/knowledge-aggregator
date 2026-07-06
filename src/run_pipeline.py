import json
import os
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
        SEED_URLS,
        max_pages=50
    )

    print(
        f"Sources: {len(sources)}"
    )
    
    os.makedirs(
        "data/output",
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
        "Saved sources.json"
    )
    
    print("Extracting...")

    docs = extractor.process_sources(
        sources
    )

    print(
        f"Documents: {len(docs)}"
    )
    
    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    with open(
        "data/processed/documents.json",
        "w"
    ) as f:

        json.dump(
            docs,
            f,
            indent=2
        )

    print(
        "Saved documents.json"
    )

    print("Chunking...")

    chunks = chunker.process_documents(
        docs
    )

    print(
        f"Chunks: {len(chunks)}"
    )
    

    with open(
        "data/output/chunks.json",
        "w"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2
        )

    print(
        "Saved chunks.json"
    )

if __name__ == "__main__":

    main()
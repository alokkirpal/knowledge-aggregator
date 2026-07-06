import json
import trafilatura


class Extractor:

    def extract(self, html):

        text = trafilatura.extract(

            html,

            include_links=False,

            include_images=False

        )

        return text

    def process_sources(self, sources):

        documents = []

        for source in sources:

            text = self.extract(
                source["html"]
            )

            if not text:
                continue

            documents.append({

                "url":
                source["url"],

                "text":
                text

            })

        return documents


if __name__ == "__main__":

    with open(
        "data/output/sources.json"
    ) as f:

        sources = json.load(f)

    extractor = Extractor()

    docs = extractor.process_sources(
        sources
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
        f"Processed {len(docs)} docs"
    )
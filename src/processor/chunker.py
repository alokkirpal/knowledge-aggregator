import json


class Chunker:

    def __init__(
        self,
        chunk_size=500
    ):

        self.chunk_size = chunk_size

    def split_text(self, text):

        words = text.split()

        chunks = []

        for i in range(

            0,

            len(words),

            self.chunk_size

        ):

            chunk = " ".join(

                words[
                    i:
                    i+self.chunk_size
                ]

            )

            chunks.append(chunk)

        return chunks

    def process_documents(
        self,
        documents
    ):

        results = []

        chunk_id = 0

        for doc in documents:

            chunks = self.split_text(
                doc["text"]
            )

            for chunk in chunks:

                results.append({

                    "chunk_id":
                    chunk_id,

                    "url":
                    doc["url"],

                    "text":
                    chunk

                })

                chunk_id += 1

        return results


if __name__ == "__main__":

    with open(
        "data/processed/documents.json"
    ) as f:

        docs = json.load(f)

    chunker = Chunker()

    chunks = chunker.process_documents(
        docs
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
        f"Created {len(chunks)} chunks"
    )
import json

from relevance_engine import RelevanceEngine


INPUT_FILE = "data/output/chunks.json"

OUTPUT_FILE = "data/output/relevant_chunks.json"

REPORT_FILE = "data/output/relevance_report.json"


def main():

    engine = RelevanceEngine()

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    relevant_chunks = []

    report = {

        "total_chunks": len(chunks),

        "high": 0,

        "medium": 0,

        "low": 0
    }

    for chunk in chunks:

        content = chunk.get(
            "content",
            ""
        )

        result = engine.score(
            content
        )

        label = engine.classify(
            result["score"]
        )

        enriched_chunk = {

            **chunk,

            "relevance_score":
                result["score"],

            "relevance_label":
                label,

            "matched_core":
                result["matched_core"],

            "matched_out_of_scope":
                result["matched_out_of_scope"]
        }

        if label in {

            "high",

            "medium"

        }:

            relevant_chunks.append(
                enriched_chunk
            )

        report[label] += 1

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            relevant_chunks,
            f,
            indent=2
        )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2
        )

    print("\n===== RELEVANCE REPORT =====")

    print(
        f"Total Chunks: "
        f"{report['total_chunks']}"
    )

    print(
        f"High: "
        f"{report['high']}"
    )

    print(
        f"Medium: "
        f"{report['medium']}"
    )

    print(
        f"Low: "
        f"{report['low']}"
    )

    print(
        f"\nSaved: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()
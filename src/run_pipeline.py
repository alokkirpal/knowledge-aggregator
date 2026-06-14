import json
import os
from urllib.parse import urlparse

from src.config import EVENT_SCOPE
from src.classifier import classify_url, get_domain
from src.fetcher import fetch_html, extract_title, extract_main_text, extract_links
from src.processor import clean_text, chunk_text


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    output_dir = EVENT_SCOPE["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    all_sources = []
    all_chunks = []
    discovered_urls = set()

    for seed_url in EVENT_SCOPE["seed_urls"]:
        print(f"\nProcessing seed URL: {seed_url}")

        seed_classification = classify_url(seed_url)

        source_record = {
            "url": seed_url,
            "domain": get_domain(seed_url),
            "event": EVENT_SCOPE["event"],
            "division": EVENT_SCOPE["division"],
            "season_year": EVENT_SCOPE["season_year"],
            **seed_classification
        }

        if not seed_classification["is_text_extractable"]:
            all_sources.append(source_record)
            continue

        try:
            html = fetch_html(seed_url)
            title = extract_title(html)
            raw_text = extract_main_text(html, seed_url)
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text)

            source_record.update({
                "title": title,
                "crawl_status": "processed",
                "raw_text_length": len(raw_text),
                "cleaned_text_length": len(cleaned_text),
                "num_chunks": len(chunks)
            })

            all_sources.append(source_record)

            for index, chunk in enumerate(chunks):
                all_chunks.append({
                    "source_url": seed_url,
                    "chunk_index": index,
                    "event": EVENT_SCOPE["event"],
                    "division": EVENT_SCOPE["division"],
                    "season_year": EVENT_SCOPE["season_year"],
                    "content": chunk
                })

            links = extract_links(html, seed_url)

            for link in links:
                if link in discovered_urls:
                    continue

                discovered_urls.add(link)
                classification = classify_url(link)

                all_sources.append({
                    "url": link,
                    "domain": get_domain(link),
                    "parent_seed_url": seed_url,
                    "event": EVENT_SCOPE["event"],
                    "division": EVENT_SCOPE["division"],
                    "season_year": EVENT_SCOPE["season_year"],
                    **classification
                })

        except Exception as e:
            source_record.update({
                "crawl_status": "failed",
                "error": str(e)
            })
            all_sources.append(source_record)

    save_json(os.path.join(output_dir, "sources.json"), all_sources)
    save_json(os.path.join(output_dir, "chunks.json"), all_chunks)

    print("\nPipeline completed.")
    print(f"Sources saved: {len(all_sources)}")
    print(f"Chunks saved: {len(all_chunks)}")
    print(f"Output folder: {output_dir}")


if __name__ == "__main__":
    main()
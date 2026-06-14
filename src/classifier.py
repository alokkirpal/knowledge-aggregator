from urllib.parse import urlparse


def get_domain(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


def classify_url(url: str) -> dict:
    parsed = urlparse(url)
    domain = get_domain(url)
    path = parsed.path.lower()

    if "youtube.com" in domain or "youtu.be" in domain:
        return {
            "content_type": "youtube",
            "crawl_status": "deferred",
            "is_text_extractable": False,
            "reason": "YouTube/video links are deferred in text-only phase"
        }

    if any(social in domain for social in [
        "facebook.com", "instagram.com", "twitter.com", "x.com", "linkedin.com"
    ]):
        return {
            "content_type": "social",
            "crawl_status": "ignored",
            "is_text_extractable": False,
            "reason": "Social media links are ignored"
        }

    if path.endswith(".pdf"):
        return {
            "content_type": "pdf",
            "crawl_status": "pending",
            "is_text_extractable": True,
            "reason": "PDF text source"
        }

    if parsed.scheme in ["http", "https"]:
        return {
            "content_type": "html",
            "crawl_status": "pending",
            "is_text_extractable": True,
            "reason": "HTML text source"
        }

    return {
        "content_type": "unknown",
        "crawl_status": "ignored",
        "is_text_extractable": False,
        "reason": "Unsupported URL type"
    }
 import requests
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": "TopicTrainerBot/0.1 educational research crawler"
}


def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.text


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return ""


def extract_main_text(html: str, url: str) -> str:
    text = trafilatura.extract(html, url=url)
    return text or ""


def extract_links(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])
        if absolute_url.startswith("http"):
            links.add(absolute_url)

    return sorted(list(links))
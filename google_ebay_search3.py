import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time
import re

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Mobile Safari/537.36",
]


def fetch_google(url):
    """Request Google SAFELY with headers that avoid blocking."""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }
    time.sleep(random.uniform(1.0, 1.8))
    resp = requests.get(url, headers=headers)
    return resp.text


def extract_ebay_links(html):
    """Extract ALL eBay URLs from raw HTML using regex + soup."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    # 1) Extract links from <a>
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "ebay.com" in href:
            links.add(href)

    # 2) Extract hidden redirect URLs (Google uses /url?q=...)
    matches = re.findall(r"/url\?q=(https://[^&]+)", html)
    for url in matches:
        if "ebay.com" in url:
            links.add(url)

    return list(links)


def google_ebay_search(query):
    encoded = urllib.parse.quote_plus(f"{query} site:ebay.com")

    urls_to_try = [
        f"https://www.google.com/search?q={encoded}",
        f"https://www.google.com/search?q={encoded}&udm=14",  # mobile/lite mode
        f"https://www.google.com/search?q={encoded}&noforce=1&igu=1",  # bypass AI
    ]

    all_results = []

    print(f"\n🔎 GOOGLE UNIVERSAL SEARCH: {query}")

    for url in urls_to_try:
        print(f"\nTrying → {url}")
        html = fetch_google(url)
        links = extract_ebay_links(html)

        print(f"   → Found {len(links)} eBay links in this mode.")

        all_results.extend(links)

    # Remove duplicates
    all_results = list(set(all_results))

    print(f"\n✅ FINAL UNIQUE RESULTS: {len(all_results)}")
    return all_results


if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    results = google_ebay_search(query)

    print("\nRESULT LINKS:")
    for r in results:
        print("🔗", r)

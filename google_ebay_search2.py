import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

def google_ebay_search(query):
    """
    Uses normal Google search (NOT Shopping) and extracts eBay links.
    Much harder for Google to block.
    """

    encoded = urllib.parse.quote_plus(f"{query} site:ebay.com")
    url = f"https://www.google.com/search?q={encoded}"

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    print(f"\n🔎 GOOGLE SEARCH: {query}")
    print(f"URL → {url}")

    # Request with delay (Google friendly)
    time.sleep(random.uniform(1.2, 2.0))

    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    results = []

    # Google search results selector
    for g in soup.select("div.g"):
        link_tag = g.find("a")
        title_tag = g.find("h3")

        if not link_tag or not title_tag:
            continue

        link = link_tag["href"]
        title = title_tag.get_text(strip=True)

        # Only keep eBay listings
        if "ebay.com" not in link:
            continue

        results.append({
            "title": title,
            "link": link
        })

    print(f"✅ Found {len(results)} eBay results.")
    return results


if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    data = google_ebay_search(query)

    print("\nRESULTS:")
    for item in data:
        print("---------------------------")
        print("📦", item["title"])
        print("🔗", item["link"])

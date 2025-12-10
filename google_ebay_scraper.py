import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import time

HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
    ])
}


def google_ebay_search(query):
    """
    Search Google Shopping for eBay listings.
    Google query: "<keywords> site:ebay.com"
    """

    encoded = urllib.parse.quote_plus(f"{query} site:ebay.com")
    url = f"https://www.google.com/search?q={encoded}&tbm=shop"

    print(f"\n🔎 GOOGLE SHOPPING SEARCH: {query}")
    print(f"URL → {url}")

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # Google Shopping listing selector
    items = soup.select("div.sh-dgr__content")

    if not items:
        print("⚠ No Google Shopping results found.")
        return []

    for item in items:
        title_el = item.select_one("h4")
        price_el = item.select_one(".T14wmb")
        link_el = item.select_one("a.shntl")
        img_el = item.select_one("img")

        if not title_el or not price_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        price = price_el.get_text(strip=True)

        # Full link
        link = "https://www.google.com" + link_el.get("href")

        # Try extracting image URL
        img = img_el.get("src") if img_el else None

        results.append({
            "title": title,
            "price": price,
            "link": link,
            "image": img
        })

    print(f"✅ Found {len(results)} results.")
    return results


if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    data = google_ebay_search(query)

    print("\nRESULTS:")
    for item in data:
        print("-----------------------------")
        print("📦", item["title"])
        print("💲", item["price"])
        print("🔗", item["link"])
        if item["image"]:
            print("🖼 Image:", item["image"])

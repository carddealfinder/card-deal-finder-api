import requests
from bs4 import BeautifulSoup
import time

TOR_PROXY = {
    "http":  "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def tor_request(url):
    """Send GET request through Tor."""
    try:
        response = requests.get(url, headers=HEADERS, proxies=TOR_PROXY, timeout=25)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"❌ Tor Request Error: {e}")
        return None

def scrape_ebay(query):
    print(f"\n🔎 TOR-POWERED SEARCH: {query}")

    url = (
        "https://www.ebay.com/sch/i.html"
        f"?_nkw={query.replace(' ', '+')}"
        "&LH_BIN=1&_sop=10"
    )

    html = tor_request(url)
    if not html:
        print("❌ No HTML returned.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".s-item")

    print(f"➡ Found {len(items)} items via Tor")

    results = []

    for item in items:
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        link = item.select_one("a.s-item__link")

        if title and price and link:
            results.append({
                "title": title.get_text(strip=True),
                "price": price.get_text(strip=True),
                "url": link["href"]
            })

    return results


# ============================
# RUN THE SCRAPER
# ============================
if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    results = scrape_ebay(query)

    print("\nRESULTS:")
    for r in results:
        print(f"- {r['title']} | {r['price']}")
        print(f"  {r['url']}")

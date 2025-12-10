import requests
from bs4 import BeautifulSoup
import urllib.parse

def ebay_rss_search(query):
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.ebay.com/sch/i.html?_nkw={encoded}&_sop=10&_rss=1"

    print(f"\n🔎 eBay RSS SEARCH: {query}")
    print(f"URL → {url}")

    resp = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    soup = BeautifulSoup(resp.text, "xml")

    items = soup.find_all("item")
    results = []

    for item in items:
        title = item.title.text if item.title else ""
        link = item.link.text if item.link else ""
        price = ""

        # Extract price from description if present
        if item.description:
            desc = BeautifulSoup(item.description.text, "html.parser").text
            if "$" in desc:
                price = desc.strip()

        results.append({
            "title": title,
            "link": link,
            "price": price
        })

    print(f"✅ Found {len(results)} items\n")
    return results


if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    results = ebay_rss_search(query)

    for r in results:
        print("----------------------------------------------------")
        print("TITLE:", r["title"])
        print("PRICE INFO:", r["price"])
        print("LINK:", r["link"])

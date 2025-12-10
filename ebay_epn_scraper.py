import requests
import urllib.parse

def ebay_epn_search(query):
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.ebay.com/sch/i.html?_nkw={encoded}&_sop=10&_view=json"

    print(f"\n🔎 EPN JSON SEARCH: {query}")
    print(f"URL → {url}")

    resp = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    try:
        data = resp.json()
    except:
        print("❌ Not JSON — likely blocked by eBay filtering.")
        print("Response length:", len(resp.text))
        return []

    items = data.get("itemSummaries", [])
    results = []

    for item in items:
        results.append({
            "title": item.get("title", ""),
            "price": item.get("price", {}).get("value", ""),
            "currency": item.get("price", {}).get("currency", ""),
            "url": item.get("itemWebUrl", "")
        })

    print(f"✅ Found {len(results)} items\n")
    return results


if __name__ == "__main__":
    query = "Prizm Silver Rookie"
    results = ebay_epn_search(query)

    for r in results:
        print("----------------------------------------------------")
        print("TITLE:", r["title"])
        print("PRICE:", r["price"], r["currency"])
        print("URL:", r["url"])

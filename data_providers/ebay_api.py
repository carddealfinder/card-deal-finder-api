import os
import requests

EBAY_TOKEN = os.getenv("EBAY_BROWSE_TOKEN")

BASE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


def ebay_search(query: str, limit: int = 50):
    if not EBAY_TOKEN:
        print("❌ Missing EBAY_BROWSE_TOKEN")
        return []

    headers = {
        "Authorization": f"Bearer {EBAY_TOKEN}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "Content-Type": "application/json"
    }

    params = {
        "q": query,
        "limit": limit
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    print("EBAY STATUS:", response.status_code)

    if response.status_code != 200:
        print("EBAY ERROR:", response.text)
        return []

    data = response.json()
    items = data.get("itemSummaries", [])

    results = []
    for item in items:
        try:
            price = float(item["price"]["value"])
        except:
            price = None

        try:
            seller_score = float(item["seller"]["feedbackPercentage"])
        except:
            seller_score = None

        results.append({
            "title": item.get("title"),
            "url": item.get("itemWebUrl"),
            "price": price,
            "seller_score": seller_score,
            "source": "eBay"
        })

    return results

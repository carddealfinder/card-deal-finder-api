import os
import requests

EBAY_TOKEN = os.getenv("EBAY_BROWSE_TOKEN")

if not EBAY_TOKEN:
    print("❌ Missing eBay token. Set EBAY_BROWSE_TOKEN in Render env!")
    EBAY_TOKEN = ""

BASE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


def search_ebay(query: str, limit: int = 50):
    if not EBAY_TOKEN:
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

    print("EBAY RESPONSE STATUS:", response.status_code)

    if response.status_code != 200:
        print("EBAY ERROR:", response.text)
        return []

    data = response.json()

    if "itemSummaries" not in data:
        print("❌ No itemSummaries field in response")
        print(data)
        return []

    results = []
    for item in data.get("itemSummaries", []):
        price = None
        seller_score = None

        if "price" in item and "value" in item["price"]:
            try:
                price = float(item["price"]["value"])
            except:
                price = None

        if "seller" in item and "feedbackPercentage" in item["seller"]:
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

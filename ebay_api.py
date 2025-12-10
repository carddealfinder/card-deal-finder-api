import os
import requests

# ============================================================
#  eBay Browse API Client (OAuth Token Only)
# ============================================================

EBAY_OAUTH_TOKEN = os.getenv("EBAY_OAUTH_TOKEN")

if not EBAY_OAUTH_TOKEN:
    print("❌ ERROR: Missing EBAY_OAUTH_TOKEN in environment!")
else:
    print("✅ eBay OAuth token loaded.")

BASE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


def search_ebay(query: str, limit: int = 50):
    """
    Runs an eBay Browse API search for live listings.
    Returns normalized results for aggregator.py.
    """

    if not EBAY_OAUTH_TOKEN:
        return {"error": "Missing eBay OAuth token"}

    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }

    params = {
        "q": query,
        "limit": limit,
        "filter": "price:[0..10000]",  # avoid garbage listings
        "sort": "-price",              # sort highest → lowest (we re-rank later)
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        items = data.get("itemSummaries", [])

        cleaned = []

        for item in items:
            price_info = item.get("price", {})
            price_value = float(price_info.get("value", 0))

            cleaned.append({
                "title": item.get("title"),
                "price": price_value,
                "url": item.get("itemWebUrl"),
                "seller_score": item.get("seller", {}).get("feedbackScore", 0),
                "source": "eBay",
            })

        return cleaned

    except requests.exceptions.HTTPError as e:
        print("❌ eBay API error:", e.response.text)
        return {"error": e.response.text}
    except Exception as e:
        print("❌ Unexpected error:", str(e))
        return {"error": str(e)}

import os
import requests
from dotenv import load_dotenv

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


def get_access_token():
    """
    Retrieve a fresh OAuth token using Client Credentials.
    """
    if not EBAY_CLIENT_ID or not EBAY_CLIENT_SECRET:
        print("❌ Missing eBay API credentials in .env")
        return None

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    try:
        response = requests.post(
            TOKEN_URL,
            headers=headers,
            data=data,
            auth=(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET)
        )
        response.raise_for_status()
        token = response.json().get("access_token")
        return token

    except Exception as e:
        print("❌ Failed to get eBay token:", e)
        return None


def ebay_search(query, limit=20):
    """
    Run a Browse API search and normalize results.
    """

    access_token = get_access_token()
    if not access_token:
        return []

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": query, "limit": limit}

    try:
        resp = requests.get(SEARCH_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("❌ eBay Search Error:", e)
        return []

    items = data.get("itemSummaries", [])
    results = []

    for item in items:
        # Normalize price
        raw_price = item.get("price")
        price_value = None

        if isinstance(raw_price, (int, float)):
            price_value = float(raw_price)
        elif isinstance(raw_price, dict):
            val = raw_price.get("value")
            if val is not None:
                try:
                    price_value = float(val)
                except:
                    price_value = None

        # Extract seller score
        seller = item.get("seller", {})
        seller_score = seller.get("feedbackScore", 0)

        results.append({
            "title": item.get("title"),
            "price": price_value,
            "seller_score": seller_score,
            "url": item.get("itemWebUrl"),
            "source": "eBay"
        })

    return results

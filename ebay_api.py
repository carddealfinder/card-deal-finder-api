import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
EBAY_REFRESH_TOKEN = os.getenv("EBAY_REFRESH_TOKEN")

TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
BROWSE_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"


def get_access_token():
    """Exchange refresh token for a short-lived access_token."""
    auth = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
    encoded_auth = base64.b64encode(auth.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


def search_ebay(query):
    """Search eBay Buy API and return simplified pricing data."""
    try:
        token = get_access_token()
    except Exception as e:
        print("❌ Error retrieving eBay access token:", e)
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    params = {
        "q": query,
        "limit": 20,
    }

    try:
        response = requests.get(BROWSE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print("❌ Error calling eBay Browse API:", e)
        return []

    items = data.get("itemSummaries", [])
    results = []

    for item in items:
        price = item.get("price", {}).get("value")
        title = item.get("title")
        item_id = item.get("itemId")

        if price:
            results.append({
                "title": title,
                "price": float(price),
                "source": "eBay",
                "item_id": item_id,
                "url": item.get("itemWebUrl")
            })

    return results

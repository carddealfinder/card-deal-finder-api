import requests
import json
from ebay_api import get_access_token

CONFIG = json.load(open("config.json"))

def get_sold_comps(query):
    token = get_access_token()

    url = "https://api.ebay.com/buy/marketplace_insights/v1_beta/item_sales/search"

    params = {
        "q": query,
        "limit": 20
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, params=params)
    
    try:
        return response.json().get("itemSales", [])
    except:
        return []

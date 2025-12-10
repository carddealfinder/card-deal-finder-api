# src/ebay_search.py

from src.ebay_oauth import get_access_token

def search_items(query):
    """
    Placeholder search function.
    When Buy API is approved, this will call:
    https://api.ebay.com/buy/browse/v1/item_summary/search
    """
    print(f"🔎 Searching for: {query}")

    # TODO when approved:
    # token = get_access_token()
    #
    # headers = { "Authorization": f"Bearer {token}", "Content-Type": "application/json" }
    #
    # response = requests.get(
    #     f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={query}",
    #      headers=headers
    # )
    #
    # return response.json()

    # Temporary mocked result so the logic works:
    return [
        {"title": "2023 Prizm Rookie Auto", "price": 25.00},
        {"title": "2023 Prizm Base Rookie", "price": 3.50},
        {"title": "2023 Prizm Silver Rookie", "price": 14.00},
    ]

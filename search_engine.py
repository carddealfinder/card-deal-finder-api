from data_providers.ebay_api import ebay_search
from utils.normalize import normalize_title


def search_cards(query: str, limit: int = 20):
    """
    High-level search engine that normalizes results,
    enriches them, and returns a clean structure.
    """

    raw_items = ebay_search(query, limit=limit)

    normalized_results = []

    for item in raw_items:
        # Normalized card title (removes junk, fixes spacing, etc)
        clean_title = normalize_title(item.get("title", ""))

        normalized_results.append({
            "item_id": item.get("itemId"),
            "title": clean_title,
            "price": float(item["price"]["value"]),
            "currency": item["price"]["currency"],
            "image": item.get("image", {}).get("imageUrl"),
            "condition": item.get("condition"),
            "seller_score": item.get("seller", {}).get("feedbackScore"),
            "item_url": item.get("itemWebUrl"),
        })

    return normalized_results

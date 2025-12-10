from .scorers import score_card
from .deal_ranking import sort_by_deal_score
from data_providers.ebay_api import ebay_search


def compute_metrics(results):
    """
    Safely compute high/low/avg metrics.
    Ensures price is always a float.
    """

    prices = []

    for r in results:
        raw_price = r.get("price")

        if isinstance(raw_price, (int, float)):
            prices.append(float(raw_price))
            continue

        if isinstance(raw_price, dict):
            val = raw_price.get("value")
            if val:
                try:
                    prices.append(float(val))
                except:
                    pass

    if not prices:
        return {
            "count": 0,
            "avg_price": None,
            "low_price": None,
            "high_price": None
        }

    avg_price = sum(prices) / len(prices)

    return {
        "count": len(prices),
        "avg_price": round(avg_price, 2),
        "low_price": round(min(prices), 2),
        "high_price": round(max(prices), 2)
    }


def aggregate_search(query):
    """
    Collect raw results, score them, compute metrics,
    rank results, and return final response package.
    """

    # Step 1 — Call all providers (eBay only for now)
    ebay_results = ebay_search(query)

    # Step 2 — Score every result
    for card in ebay_results:
        card["score"] = score_card(card)

    # Step 3 — Compute metrics
    metrics = compute_metrics(ebay_results)

    # Step 4 — Rank deals
    ranked_results = sort_by_deal_score(ebay_results)

    # Step 5 — Return final structure used by API
    return {
        "query": query,
        "metrics": metrics,
        "results": ranked_results
    }

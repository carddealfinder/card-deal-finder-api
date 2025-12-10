def sort_by_deal_score(results):
    """
    Sort cards by best deal.
    Lower price = stronger deal.
    Higher seller score also boosts ranking.
    """
    ranked = []

    for item in results:
        price = item.get("price")
        seller_score = item.get("seller_score", 0)

        if price is None:
            continue

        # Cheap items + good sellers rise to the top
        deal_score = (seller_score / 1000) - (price / 100)

        ranked.append({
            **item,
            "deal_score": round(deal_score, 4)
        })

    # Highest deal score FIRST
    ranked.sort(key=lambda x: x["deal_score"], reverse=True)

    return ranked

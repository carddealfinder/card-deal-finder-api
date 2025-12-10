def score_card(card):
    """
    Compute a 'deal score' based on price + seller reputation.
    Score is 0–100.
    """

    price = card.get("price")
    seller_score = card.get("seller_score", 0)

    # ---- PRICE FACTOR ----
    if price is None:
        price_factor = 0
    else:
        try:
            price_value = float(price.get("value")) if isinstance(price, dict) else float(price)
            price_factor = max(0, min(1.0, 50 / price_value))  # cheaper = better
        except Exception:
            price_factor = 0

    # ---- SELLER FACTOR ----
    try:
        seller_score = int(seller_score)
        seller_factor = min(seller_score / 5000, 1.0)
    except Exception:
        seller_factor = 0

    # ---- FINAL SCORE ----
    final_score = (price_factor * 0.6 + seller_factor * 0.4) * 100
    return round(final_score, 2)

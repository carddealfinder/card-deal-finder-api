def calculate_market_value(sold_comps):
    if not sold_comps:
        return None

    prices = []
    for sale in sold_comps:
        try:
            price = float(sale["price"]["value"])
            prices.append(price)
        except:
            pass

    if not prices:
        return None

    return sum(prices) / len(prices)


def score_listing(listing, market_value):
    try:
        price = float(listing["price"]["value"])
    except:
        return None

    if not market_value or market_value <= 0:
        return None

    undervalued_score = (market_value - price) / market_value
    potential_profit = market_value - price

    return {
        "price": price,
        "market_value": market_value,
        "profit": potential_profit,
        "score": undervalued_score
    }

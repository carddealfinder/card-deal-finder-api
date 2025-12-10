# src/deal_logic.py

def find_undervalued_items(items, max_price=20):
    """
    Simple example logic:
    show only items below max_price
    """
    deals = [item for item in items if item["price"] <= max_price]

    # Sort cheapest → most expensive
    deals_sorted = sorted(deals, key=lambda x: x["price"])

    return deals_sorted

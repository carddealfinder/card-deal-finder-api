# main.py

from src.ebay_search import search_items
from src.deal_logic import find_undervalued_items

def main():
    print("🔥 Card Deal Finder Engine Started")

    query = "prizm rookie"
    items = search_items(query)

    print(f"\nFound {len(items)} items")

    deals = find_undervalued_items(items, max_price=20)

    print("\n💰 Undervalued Deals:")
    for item in deals:
        print(f"- {item['title']} — ${item['price']}")

if __name__ == "__main__":
    main()

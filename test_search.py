from search_engine import search_cards

print("🔎 Testing Card Search Engine\n")

query = "2020 Prizm Silver Rookie"

results = search_cards(query, limit=10)

print(f"Found {len(results)} results:\n")

for i, r in enumerate(results, 1):
    print(f"{i}. {r['title']}")
    print(f"   Price: {r['price']} {r['currency']}")
    print(f"   Seller Score: {r['seller_score']}")
    print(f"   URL: {r['item_url']}")
    print()

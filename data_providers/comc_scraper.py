import requests
import json

def search_comc(query, max_results=20):
    print(f"🔎 Searching COMC for: {query}")

    url = "https://www.comc.com/rest/search"

    payload = {
        "q": query,
        "start": 0,
        "limit": max_results,
        "sort": {"field": "price", "order": "asc"},
        "filters": []
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://www.comc.com",
        "Referer": "https://www.comc.com/",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    print(f"🔍 STATUS: {response.status_code}")
    print(f"🔍 CONTENT-TYPE: {response.headers.get('Content-Type')}")

    # If JSON fails, dump raw body to debug
    try:
        data = response.json()
    except Exception:
        print("❌ JSON decode failed. Raw response below:\n")
        print(response.text[:2000])  # print first 2000 chars
        return []

    if "items" not in data:
        print("⚠ Unexpected response structure:")
        print(data)
        return []

    items = data["items"]
    results = []

    for item in items:
        price = item.get("price", {}).get("amount")
        results.append({
            "title": item.get("title", "No title"),
            "price": price,
            "url": "https://www.comc.com" + item.get("url", ""),
        })

    print(f"📦 COMC results: {len(results)} found")
    return results


if __name__ == "__main__":
    cards = search_comc("Prizm Silver Rookie")
    for c in cards:
        print(c)

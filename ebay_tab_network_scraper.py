from playwright.sync_api import sync_playwright
import json
import time
import re

SEARCH_API_REGEX = re.compile(r"api.*_search", re.IGNORECASE)

def scrape_ebay_network():
    print("\n🔎 ATTACHING TO REAL CHROME TAB & CAPTURING NETWORK DATA...\n")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        pages = context.pages

        ebay_pages = [pg for pg in pages if "ebay.com" in pg.url]

        if not ebay_pages:
            print("❌ No eBay tab found. Open the search page manually!")
            return []

        page = ebay_pages[0]
        print(f"✅ Using tab: {page.url}\n")

        results = []

        # Capture responses
        def handle_response(response):
            url = response.url
            if SEARCH_API_REGEX.search(url):
                print(f"📡 Captured eBay API call: {url}")
                try:
                    data = response.json()
                    # Extract item Summaries
                    items = data.get("itemSummaries", [])
                    print(f"   → Found {len(items)} items in API JSON.")
                    for item in items:
                        results.append({
                            "title": item.get("title"),
                            "price": item.get("price", {}).get("value"),
                            "currency": item.get("price", {}).get("currency"),
                            "url": item.get("itemWebUrl")
                        })
                except:
                    pass

        page.on("response", handle_response)

        print("🔁 Reloading page to trigger API calls...\n")
        page.reload(wait_until="networkidle")
        time.sleep(3)

        print("\nFINAL RESULTS:")
        print(json.dumps(results, indent=2))

        return results


if __name__ == "__main__":
    scrape_ebay_network()

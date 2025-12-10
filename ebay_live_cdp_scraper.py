import time
from playwright.sync_api import sync_playwright

SEARCH_QUERY = "Prizm Silver Rookie"

ANTI_BOT_JS = """
Object.defineProperty(navigator, 'webdriver', { get: () => false });
window.chrome = { runtime: {} };
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4] });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
"""

def run_search(query):
    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}&LH_BIN=1&_sop=10"

    print(f"\n🔎 Connecting to LIVE Chrome (CDP)...")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")

        # Use existing open tab OR create a new one
        context = browser.contexts[0]
        page = context.new_page()

        # Anti-bot protections injected
        page.add_init_script(ANTI_BOT_JS)

        print(f"🔎 Searching eBay for: {query}")
        print(f"URL → {url}")

        page.goto(url, wait_until="domcontentloaded")

        time.sleep(3)

        # Scroll to load listings
        for _ in range(4):
            page.mouse.wheel(0, 2500)
            time.sleep(1)

        print("\nExtracting results...")

        items = page.query_selector_all(".s-item")
        results = []

        for item in items:
            title = item.query_selector(".s-item__title")
            price = item.query_selector(".s-item__price")
            link  = item.query_selector("a.s-item__link")

            if title and price and link:
                results.append({
                    "title": title.inner_text(),
                    "price": price.inner_text(),
                    "url": link.get_attribute("href")
                })

        print(f"\n✅ Found {len(results)} listings.\n")

        for r in results[:10]:
            print(f"- {r['title']} | {r['price']}")
            print(f"  {r['url']}\n")

        return results


if __name__ == "__main__":
    run_search(SEARCH_QUERY)

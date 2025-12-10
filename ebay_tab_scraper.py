from playwright.sync_api import sync_playwright
import json
import time

def scrape_open_tab():
    print("\n🔎 ATTACHING TO REAL CHROME TAB...\n")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        pages = context.pages

        print(f"Found {len(pages)} open tabs.")

        # pick the tab that has eBay loaded
        ebay_pages = [pg for pg in pages if "ebay.com" in pg.url]

        if not ebay_pages:
            print("\n❌ No eBay tab found. Open eBay in Chrome first!\n")
            return []
        
        page = ebay_pages[0]
        print(f"✅ Using tab: {page.url}")

        # wait for items to load
        time.sleep(2)

        # attempt extraction
        items = page.query_selector_all(".s-item")

        if not items:
            print("\n❌ No .s-item elements found — but since this is YOUR tab, eBay is filtering via script.\n")
            print("➡ Try scrolling manually in the Chrome window, then run again.\n")
            return []

        print(f"\n✅ Extracted {len(items)} items!\n")

        results = []
        for itm in items[:20]:  # limit to 20
            title_el = itm.query_selector(".s-item__title")
            price_el = itm.query_selector(".s-item__price")
            link_el = itm.query_selector("a")
            
            results.append({
                "title": title_el.inner_text() if title_el else None,
                "price": price_el.inner_text() if price_el else None,
                "url": link_el.get_attribute("href") if link_el else None
            })

        print("\nFINAL RESULTS:\n")
        print(json.dumps(results, indent=2))

        return results


if __name__ == "__main__":
    scrape_open_tab()

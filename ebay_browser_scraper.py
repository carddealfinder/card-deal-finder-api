from playwright.sync_api import sync_playwright
import time
import re

SEARCH_URL = (
    "https://www.ebay.com/sch/i.html"
    "?_nkw={query}"
    "&LH_BIN=1"
    "&_sop=10"
)

def scrape_ebay_browser(query):
    with sync_playwright() as p:

        # ----- Launch browser with stealth-like flags -----
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-gpu",
                "--no-sandbox"
            ]
        )

        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            java_script_enabled=True
        )

        page = context.new_page()

        url = SEARCH_URL.format(query=query.replace(" ", "+"))
        print(f"\n🔎 Browser scraping: {query}")
        print(f"URL → {url}")

        # ----- Navigate without requiring networkidle -----
        try:
            page.goto(url, timeout=60000)
        except:
            print("⚠ Page load timeout ignored — continuing.")

        # ----- Scroll to load dynamic content -----
        for _ in range(5):
            page.mouse.wheel(0, 2500)
            time.sleep(1.2)

        # ----- Try to detect listing blocks -----
        try:
            page.wait_for_selector(".s-item__wrapper", timeout=15000)
            print("✅ Found listing selectors!")
        except:
            print("⚠ No .s-item__wrapper found — attempting fallback JS parse.")

        # ----- Primary scrape via DOM -----
        items = page.locator("css=div.s-item__wrapper").all()
        results = []

        for item in items:
            try:
                title = item.locator(".s-item__title").inner_text()
                price = item.locator(".s-item__price").inner_text()
                link = item.locator("a.s-item__link").get_attribute("href")

                if title and price:
                    results.append({
                        "title": title.strip(),
                        "price": price.strip(),
                        "url": link
                    })
            except:
                continue

        if results:
            print(f"🟢 DOM scrape found {len(results)} items.")
            browser.close()
            return results

        # ----- Fallback: deep HTML scrape -----
        html = page.evaluate("() => document.body.innerHTML")

        pattern = r's-item__title">(.+?)<.*?s-item__price">(.+?)<'
        matches = re.findall(pattern, html, re.DOTALL)

        fallback_results = []
        for m in matches:
            fallback_results.append({
                "title": m[0],
                "price": m[1],
                "url": url
            })

        print(f"🟡 JS deep scrape found {len(fallback_results)} items.")

        browser.close()
        return fallback_results


# ---- Test Run ----
if __name__ == "__main__":
    listings = scrape_ebay_browser("Prizm Silver Rookie")
    print("\nFINAL RESULTS:")
    print(listings)

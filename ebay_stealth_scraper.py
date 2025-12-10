from playwright.sync_api import sync_playwright
import time

SEARCH_QUERY = "Prizm Silver Rookie"


def full_stealth(page):
    """
    Full fingerprint spoofing to defeat eBay bot detection.
    """
    page.add_init_script("""
        // 1. Remove webdriver
        Object.defineProperty(navigator, 'webdriver', { get: () => false });

        // 2. Fake plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });

        // 3. Fake languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en']
        });

        // 4. Fake hardware concurrency
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => 8
        });

        // 5. Fake platform
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32'
        });

        // 6. Fake GPU fingerprint
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) return "Intel Inc.";
            if (parameter === 37446) return "Intel Iris OpenGL Engine";
            return getParameter(parameter);
        };

        // 7. Fake canvas fingerprint
        const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
        HTMLCanvasElement.prototype.toDataURL = function() {
            return originalToDataURL.apply(this, arguments).replace("AAAA", "AAAB");
        };

        // 8. Fake audio fingerprint
        const audioContext = window.AudioContext || window.webkitAudioContext;
        if (audioContext) {
            const originalOsc = audioContext.prototype.createOscillator;
            audioContext.prototype.createOscillator = function() {
                const osc = originalOsc.apply(this, arguments);
                Object.defineProperty(osc.frequency, 'value', { get: () => 440 });
                return osc;
            };
        }

        // 9. Remove automation flags
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;

        // 10. Fake chrome runtime
        window.chrome = { runtime: {} };

        // 11. Clean user agent
        Object.defineProperty(navigator, 'userAgent', {
            get: () => navigator.userAgent.replace("HeadlessChrome", "Chrome")
        });
    """)


def scrape_ebay(query):
    print(f"\n🔎 STEALTH SEARCH: {query}\n")

    url = f"https://www.ebay.com/sch/i.html?_nkw={query.replace(' ', '+')}&LH_BIN=1&_sop=10"
    print("Loading URL:", url)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--start-maximized"
            ]
        )

        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # Inject stealth
        full_stealth(page)

        # Load eBay
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Human-like scrolling
        for _ in range(6):
            page.mouse.wheel(0, 1200)
            time.sleep(1)

        # Attempt to extract listings
        items = page.query_selector_all(".s-item__wrapper")

        if not items:
            print("\n❌ Still blocked — no listings detected.")
            browser.close()
            return []

        print(f"\n✅ SUCCESS! Found {len(items)} items.\n")

        results = []
        for itm in items:
            title_el = itm.query_selector(".s-item__title")
            price_el = itm.query_selector(".s-item__price")
            link_el = itm.query_selector("a.s-item__link")

            results.append({
                "title": title_el.inner_text() if title_el else None,
                "price": price_el.inner_text() if price_el else None,
                "url": link_el.get_attribute("href") if link_el else None
            })

        browser.close()
        return results


if __name__ == "__main__":
    data = scrape_ebay(SEARCH_QUERY)

    print("\nRESULTS:")
    for d in data:
        print(d)

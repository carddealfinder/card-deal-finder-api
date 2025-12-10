import requests
from bs4 import BeautifulSoup
import random
import time
import re

# -----------------------------------------------------------
# USER AGENTS – ROTATE TO AVOID EBAY BOT DETECTION
# -----------------------------------------------------------
USER_AGENTS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    # Mobile
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile Safari/604.1",
]

# -----------------------------------------------------------
# BUILD STEALTH HEADERS
# -----------------------------------------------------------
def build_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Referer": "https://www.ebay.com/",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
    }


# -----------------------------------------------------------
# FUNCTION TO EXTRACT PRICE STRING INTO FLOAT
# -----------------------------------------------------------
def extract_price(text):
    if not text:
        return None
    match = re.search(r"\$([\d,]+\.\d{2})", text.replace(",", ""))
    return float(match.group(1)) if match else None


# -----------------------------------------------------------
# STEALTH REQUEST WITH RETRIES + SESSION
# -----------------------------------------------------------
def stealth_get(url):
    session = requests.Session()

    for attempt in range(1, 4):
        try:
            headers = build_headers()
            print(f"   → Attempt {attempt}: Using User-Agent = {headers['User-Agent'][:30]}...")

            response = session.get(url, headers=headers, timeout=12)

            # Basic bot-block detection
            txt = response.text.lower()
            if "captcha" in txt or "robot check" in txt or "verify you are human" in txt:
                print("🛑 eBay returned CAPTCHA / robot block. Retrying...")
                time.sleep(random.uniform(2, 4))
                continue

            return response.text

        except Exception as e:
            print("⚠️ Request failed:", e)
            time.sleep(random.uniform(1, 3))

    print("❌ All attempts failed — eBay blocking the session.")
    return None


# -----------------------------------------------------------
# SCRAPE ACTIVE LISTINGS
# -----------------------------------------------------------
def scrape_active_listings(keyword):
    print(f"\n🔎 Scraping ACTIVE listings for '{keyword}'...")

    q = keyword.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={q}&_sop=10"

    html = stealth_get(url)
    if html is None:
        return []

    soup = BeautifulSoup(html, "lxml")

    items = soup.select(".s-item")
    if not items:
        print("⚠️ No .s-item results found — likely still blocked.")
        return []

    results = []

    for item in items[:20]:
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        link = item.select_one("a.s-item__link")

        if not title or not price or not link:
            continue

        results.append({
            "title": title.get_text(strip=True),
            "price": extract_price(price.get_text(strip=True)),
            "url": link["href"],
        })

    print(f"   → Found {len(results)} listings.")
    return results


# -----------------------------------------------------------
# SCRAPE SOLD COMPS
# -----------------------------------------------------------
def scrape_sold_comps(keyword):
    print(f"\n📊 Scraping SOLD comps for '{keyword}'...")

    q = keyword.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={q}&LH_Sold=1&LH_Complete=1"

    html = stealth_get(url)
    if html is None:
        return []

    soup = BeautifulSoup(html, "lxml")

    items = soup.select(".s-item")
    if not items:
        print("⚠️ No sold comps found — likely still blocked.")
        return []

    prices = []
    for item in items[:30]:
        price = item.select_one(".s-item__price")
        if not price:
            continue

        value = extract_price(price.get_text(strip=True))
        if value:
            prices.append(value)

    print(f"   → Found {len(prices)} sold prices.")
    return prices


# -----------------------------------------------------------
# DEBUG MODE (RUN FILE DIRECTLY)
# -----------------------------------------------------------
if __name__ == "__main__":
    print(scrape_active_listings("Prizm Silver Rookie"))
    print(scrape_sold_comps("Prizm Silver Rookie"))

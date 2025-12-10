import requests
from bs4 import BeautifulSoup
import random
import time
import re

# ----------------------
# ROTATING PROXY LIST (FREE HTTP PROXIES)
# ----------------------
PROXIES = [
    "http://51.159.115.233:3128",
    "http://185.199.231.45:80",
    "http://34.146.64.228:3128",
    "http://159.203.61.169:8080",
    "http://165.22.6.190:8080",
]

def get_random_proxy():
    return {"http": random.choice(PROXIES), "https": random.choice(PROXIES)}

# ----------------------
# ROTATING USER AGENTS
# ----------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 Mobile Safari/604.1",
]

def build_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html",
        "Connection": "keep-alive",
    }

# ----------------------
# COOKIE HARVESTER
# ----------------------
def get_fresh_cookies():
    try:
        resp = requests.get(
            "https://www.ebay.com",
            headers=build_headers(),
            proxies=get_random_proxy(),
            timeout=10,
        )
        return resp.cookies
    except:
        return None

# ----------------------
# PRICE PARSER
# ----------------------
def extract_price(txt):
    if not txt:
        return None
    m = re.search(r"\$([\d,]+(\.\d{2})?)", txt.replace(",", ""))
    return float(m.group(1)) if m else None

# ----------------------
# SUPER STEALTH GET
# ----------------------
def stealth_get(url):
    for attempt in range(1, 5):
        try:
            headers = build_headers()
            cookies = get_fresh_cookies()
            proxy = get_random_proxy()

            print(f"   → Attempt {attempt} | Proxy = {proxy['http']} | UA = {headers['User-Agent'][:25]}...")

            r = requests.get(
                url,
                headers=headers,
                cookies=cookies,
                proxies=proxy,
                timeout=12,
            )

            text = r.text.lower()

            # Debug partial HTML preview
            print("   → HTML preview:", r.text[:400].replace("\n", " "), "...")

            # Hard CAPTCHA block
            if "captcha" in text or "robot" in text:
                print("   🛑 CAPTCHA detected.")
                time.sleep(random.uniform(1, 2))
                continue

            return r.text

        except Exception as e:
            print("   ⚠ Error:", e)
            time.sleep(random.uniform(1, 2))

    print("❌ FAILED: All requests blocked.")
    return None

# ----------------------
# SCRAPE ACTIVE LISTINGS
# ----------------------
def scrape_active(keyword):
    print(f"\n🔎 ACTIVE SEARCH: {keyword}")
    q = keyword.replace(" ", "+")
    url = f"https://www.ebay.com/sch/i.html?_nkw={q}&_sop=10&rt=nc&LH_BIN=1"

    html = stealth_get(url)
    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    items = soup.select(".s-item")

    print(f"   → Parsed items: {len(items)}")
    data = []

    for it in items[:20]:
        title = it.select_one(".s-item__title")
        price = it.select_one(".s-item__price")
        link = it.select_one("a.s-item__link")

        if not title or not price or not link:
            continue

        data.append({
            "title": title.get_text(strip=True),
            "price": extract_price(price.get_text(strip=True)),
            "url": link["href"],
        })

    return data

# ----------------------
# TEST DIRECT RUN
# ----------------------
if __name__ == "__main__":
    print(scrape_active("Prizm Silver Rookie"))

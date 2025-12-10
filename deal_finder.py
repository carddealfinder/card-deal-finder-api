import time
import json
from statistics import mean
from twilio.rest import Client

# ----------------------------------------
# Load config file
# ----------------------------------------
CONFIG = json.load(open("config.json"))

EBAY_KEYWORDS = CONFIG["keywords"]
UNDERVALUE_THRESHOLD = 0.20  # 20% below comps

# ----------------------------------------
# MODE SWITCH
# ----------------------------------------
USE_SCRAPER = True  # Set True to use scraper instead of API

# Import API version by default
from ebay_api import search_active_listings, get_sold_comps

# If scraper mode is enabled, override functions
if USE_SCRAPER:
    from ebay_scraper import scrape_active_listings as search_active_listings
    from ebay_scraper import scrape_sold_comps as get_sold_comps

# ----------------------------------------
# Twilio Setup
# ----------------------------------------
twilio_client = Client(
    CONFIG["twilio_account_sid"],
    CONFIG["twilio_auth_token"]
)

def send_sms(msg):
    """Send SMS using Twilio"""
    try:
        twilio_client.messages.create(
            body=msg,
            from_=CONFIG["twilio_phone_number"],
            to=CONFIG["your_phone_number"]
        )
        print("📨 SMS sent!")
    except Exception as e:
        print("❌ Error sending SMS:", e)

# ----------------------------------------
# Deal evaluation logic
# ----------------------------------------
def calculate_market_value(sold_comps):
    """Return average sold comp value."""
    if not sold_comps:
        return None
    return mean(sold_comps)

def is_good_deal(price, market_value, threshold=UNDERVALUE_THRESHOLD):
    """Return True if price is under threshold margin."""
    if market_value is None:
        return False
    return price <= market_value * (1 - threshold)

def alert_deal(listing, market_value, keyword):
    """Format SMS and send."""
    message = (
        f"🔥 DEAL FOUND ({keyword}) 🔥\n"
        f"{listing['title']}\n"
        f"💲 Price: ${listing['price']}\n"
        f"📊 Market Avg: ${market_value:.2f}\n"
        f"🔗 {listing['url']}"
    )
    send_sms(message)

# ----------------------------------------
# MAIN LOOP
# ----------------------------------------
def main():
    print("🔍 Starting AI Deal Finder...\n")

    for keyword in EBAY_KEYWORDS:
        print(f"Searching: {keyword}")

        # Get active listings (API or scraper)
        listings = search_active_listings(keyword)
        if not listings:
            print("No listings or API error.\n")
            continue

        # Get sold comps (API or scraper)
        sold_comps = get_sold_comps(keyword)
        market_value = calculate_market_value(sold_comps)

        if market_value is None:
            print("⚠ No comps found for:", keyword)
            continue

        # Check each listing for deal opportunities
        for listing in listings:
            price = listing["price"]

            if is_good_deal(price, market_value):
                alert_deal(listing, market_value, keyword)

        time.sleep(1)  # Avoid rate limits for API mode


if __name__ == "__main__":
    main()

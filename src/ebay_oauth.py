# src/ebay_oauth.py

import base64
import requests
from src import config

def get_access_token():
    print("🔐 Getting new Production access token...")

    basic_auth = f"{config.CLIENT_ID}:{config.CLIENT_SECRET}"
    encoded_auth = base64.b64encode(basic_auth.encode()).decode()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}",
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": config.REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(config.TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Access token acquired\n")
        return token
    else:
        print("❌ ERROR getting access token")
        print(response.text)
        return None

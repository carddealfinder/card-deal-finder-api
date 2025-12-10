import requests
import logging

def http_get(url, headers=None, params=None):
    """Simple wrapper for GET requests with error handling."""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"HTTP GET Error: {e}")
        return None


def http_post(url, headers=None, data=None):
    """Simple wrapper for POST requests with error handling."""
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"HTTP POST Error: {e}")
        return None

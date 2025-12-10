import re

def normalize_title(title: str) -> str:
    """
    Cleans up eBay card titles:
    - Removes extra punctuation
    - Normalizes whitespace
    - Capitalizes words
    - Removes duplicate spaces
    """

    t = title.strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"[^A-Za-z0-9#:/\-\s]", "", t)

    # Optional: capitalize first letter of each word
    t = " ".join(word.capitalize() for word in t.split())

    return t

import json
import re
from collections import Counter

def extract_keywords_from_sold(sold_data):
    """Extract possible trending keywords from sold listings."""
    words = []

    for sale in sold_data:
        title = sale.get("title", "").lower()

        # Remove punctuation
        title = re.sub(r"[^a-zA-Z0-9 ]", " ", title)

        for word in title.split():
            # Ignore useless or generic words
            if len(word) < 3:
                continue
            if word in ["the", "and", "for", "lot", "with", "this", "that",
                        "psa", "bgs", "sgc", "rookie", "auto", "card"]:
                continue
            words.append(word)

    # Count frequency
    counter = Counter(words)

    # Return words that appeared 3+ times (filter noise)
    return [word for word, count in counter.items() if count >= 3]


def update_keyword_list(new_keywords):
    """Add new AI-discovered keywords to config.json."""
    config = json.load(open("config.json"))
    existing_keywords = set(config["keywords"])

    added_count = 0

    for kw in new_keywords:
        if kw not in existing_keywords:
            config["keywords"].append(kw)
            added_count += 1

    # Save updated keyword list
    json.dump(config, open("config.json", "w"), indent=2)

    return added_count

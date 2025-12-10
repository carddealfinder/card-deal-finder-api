import sqlite3

def init_db():
    conn = sqlite3.connect("deals.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            market_value REAL,
            profit REAL,
            url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_deal(item_id, title, price, market_value, profit, url):
    conn = sqlite3.connect("deals.db")
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO deals (id, title, price, market_value, profit, url) VALUES (?, ?, ?, ?, ?, ?)",
            (item_id, title, price, market_value, profit, url)
        )
        conn.commit()
    except:
        pass

    conn.close()

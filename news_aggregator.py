import feedparser
import sqlite3
import re

# ─────────────────────────────────────────
# RSS FEED SOURCES
# Add or remove URLs here to change sources
# ─────────────────────────────────────────
FEEDS = {
    "HR News": [
        "https://www.hrdive.com/feeds/news/",
        "https://hrexecutive.com/feed/",
        "https://www.hrinasia.com/feed/",
        "https://hr.asia/feed",
        "https://www.theedgemarkets.com/feed",

    ],
    "HR Tech & AI News": [
        "https://www.unleash.ai/feed/",
        "https://joshbersin.com/feed/",
        "https://e27.co/feed/",
        "https://www.techinasia.com/feed",
        "https://www.digitalnewsasia.com/feed"
    ],
    "Data Science & AI News": [
        "https://towardsdatascience.com/feed",
        "https://www.deeplearning.ai/the-batch/feed/",
        "https://www.analyticsvidhya.com/feed",
        "https://aimalaysia.org/feed/"
    ]
}

# ─────────────────────────────────────────
# DATABASE SETUP
# Creates news.db and articles table
# if they don't already exist
# ─────────────────────────────────────────
def create_database():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                source TEXT,
                title TEXT,
                link TEXT UNIQUE,
                published TEXT,
                summary TEXT
            )
    """)
    
    conn.commit()
    conn.close()

create_database()

# ─────────────────────────────────────────
# SAVE ARTICLES
# Inserts articles into the database
# IGNORE skips duplicates automatically
# ─────────────────────────────────────────
def save_articles(category, source, entries):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    for entry in entries:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO articles (category, source, title, link, published, summary)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                category,
                source,
                entry.get("title", ""),
                entry.get("link", ""),
                entry.get("published", ""),
                strip_html(entry.get("summary", ""))[:200]
            ))
        except Exception as e:
            print(f"Error saving article: {e}")
    conn.commit()
    conn.close()

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text)

# ─────────────────────────────────────────
# FETCH & SAVE ALL FEEDS
# Loops through every category and URL,
# fetches articles and saves to database
# ─────────────────────────────────────────
for category, urls in FEEDS.items():
    print(f"\n=== {category} ===")
    for url in urls:
        feed = feedparser.parse(url)
        source = feed.feed.get("title", url)
        save_articles(category, source, feed.entries[:10])
        for entry in feed.entries[:5]:
            print(entry.title)
            print('---')

# ─────────────────────────────────────────
# CHECK IF SQLITE3 IS POPULATED
# ─────────────────────────────────────────
# conn = sqlite3.connect("news.db")
# cursor = conn.cursor()
# cursor.execute("SELECT category, source, title FROM articles LIMIT 10")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
# conn.close()
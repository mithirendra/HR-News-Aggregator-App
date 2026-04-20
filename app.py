from flask import Flask, render_template, flash, redirect, url_for
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
from dotenv import load_dotenv
import os
from news_aggregator import create_database
from email.utils import parsedate_to_datetime

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

def get_articles(category=None):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT category, source, title, link, summary, published FROM articles WHERE category = ? ORDER BY published DESC", (category,))
    else:
        cursor.execute("SELECT category, source, title, link, summary, published FROM articles ORDER BY published DESC")
    rows = cursor.fetchall()
    conn.close()

    articles = []

    for row in rows:
        articles.append({
            "category": row[0],
            "source": row[1],
            "title": row[2],
            "link": row[3],
            "summary": row[4],
            "published": row[5]
        })

    def sort_key(a):
        try:
            return parsedate_to_datetime(a["published"])
        except:
            return datetime.min

    from datetime import datetime
    articles.sort(key=sort_key, reverse=True)

    return articles

@app.route("/")
def index():
    articles = get_articles()
    return render_template("index.html", articles=articles, current_category="All")

@app.route("/category/<category>")
def by_category(category):
    articles = get_articles(category)
    return render_template("index.html", articles=articles, current_category=category)

def refresh_feeds():
    subprocess.run(["python", "news_aggregator.py"])

@app.route("/refresh")
def refresh():
    subprocess.run(["python", "news_aggregator.py"])
    flash("Database refreshed!")
    return redirect(url_for('index'))
    # return "Database refreshed! <br><br><a href='/'>Go back</a>"

@app.route("/clear")
def clear_db():
    subprocess.run(["python", "clear_db.py"])
    subprocess.run(["python", "news_aggregator.py"])
    flash("Database cleared and refreshed!")
    return redirect(url_for('index'))
    # return "Database cleared and refreshed! <br><br><a href='/'>Go back</a>"


scheduler = BackgroundScheduler()
scheduler.add_job(refresh_feeds, 'interval', hours=1)
scheduler.start()

# Example of other pages
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

# Run on startup
create_database()
refresh_feeds()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
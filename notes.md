# HR News Aggregator - Build Notes

## Project Structure
news_aggregator_project/
├── app.py                  # Flask web app
├── news_aggregator.py      # RSS fetcher + database populator
├── clear_db.py             # Clears all articles from database
├── check_all_db.py         # Checks how many articles in database
├── news.db                 # SQLite database
├── templates/
│   └── index.html          # HTML template
└── news_agg_env/           # Virtual environment

## Steps Completed
- Step 1 ✅ Fetch one RSS feed
- Step 2 ✅ Fetch all 3 categories
- Step 3 ✅ Save to SQLite database
- Step 4 ✅ Flask app running at http://127.0.0.1:5000
- Step 5 ✅ HTML template with category tabs

## Steps Remaining
- Step 6 — Basic styling (CSS)
- Step 7 — Auto-refresh scheduler
- Step 8 — Test everything locally
- Step 9 — Deploy to Railway (another day)

## Key Commands
# Activate environment
news_agg_env\Scripts\activate

# Populate database
python news_aggregator.py

# Run web app
python app.py

# Check database
python check_all_db.py

# Clear database
python clear_db.py

## RSS Feed Sources
### HR News
- HR Dive: https://www.hrdive.com/feeds/news/
- HR Executive: https://hrexecutive.com/feed/
- HR in Asia: https://www.hrinasia.com/feed/
- HR Asia: https://hr.asia/feed
- The Edge Markets: https://www.theedgemarkets.com/feed

### HR Tech & AI News
- Unleash: https://www.unleash.ai/feed/
- Josh Bersin: https://joshbersin.com/feed/
- e27: https://e27.co/feed/
- Tech in Asia: https://www.techinasia.com/feed
- Digital News Asia: https://www.digitalnewsasia.com/feed

### Data Science & AI News
- Towards Data Science: https://towardsdatascience.com/feed
- The Batch (deeplearning.ai): https://www.deeplearning.ai/the-batch/feed/
- Analytics Vidhya: https://www.analyticsvidhya.com/feed
- AI Malaysia: https://aimalaysia.org/feed/

## Notes
- Database: SQLite, file called news.db
- Articles table columns: id, category, source, title, link, published, summary
- link column is UNIQUE to prevent duplicates
- Summaries are stripped of HTML tags on save
- Flask runs on http://127.0.0.1:5000
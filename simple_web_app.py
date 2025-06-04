from flask import Flask, render_template, jsonify
from scrapers.simple_scraper import scrape_all, CATEGORY_DESCRIPTIONS
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Store articles in memory
articles = []
categories = set()
sources = set()

def update_articles():
    """Update the articles list and extract unique categories and sources."""
    global articles, categories, sources
    logger.info("Starting to scrape articles...")
    articles = scrape_all()
    categories = {article['category'] for article in articles}
    sources = {article['source_name'] for article in articles}
    logger.info(f"Scraped {len(articles)} articles")
    logger.info(f"Found {len(categories)} categories: {categories}")
    logger.info(f"Found {len(sources)} sources: {sources}")

@app.route('/')
def index():
    """Render the main page."""
    return render_template('simple_index.html',
                         categories=sorted(categories),
                         sources=sorted(sources),
                         category_descriptions=CATEGORY_DESCRIPTIONS)

@app.route('/get_articles')
def get_articles():
    """API endpoint to get articles."""
    if not articles:
        update_articles()
    return jsonify({'articles': articles})

if __name__ == '__main__':
    # Initial scrape
    update_articles()
    app.run(debug=True) 
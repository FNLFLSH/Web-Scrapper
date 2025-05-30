from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS
from scrapers.accounting_today import scrape_all_sources
from db_utils import save_bulk
import json
from datetime import datetime
from config.categories import CATEGORY_KEYWORDS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# HTML template for displaying articles with category filter
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Horizon Scanner</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            color: #1a1a1a;
        }
        .header {
            background-color: #ffffff;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .feed {
            max-width: 800px;
            margin: 40px auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            padding: 30px;
        }
        .article {
            border-bottom: 1px solid #eee;
            padding: 18px 0;
        }
        .article:last-child {
            border-bottom: none;
        }
        .title {
            font-size: 1.2em;
            font-weight: 600;
            color: #2a4d8f;
            text-decoration: none;
        }
        .meta {
            font-size: 0.95em;
            color: #888;
            margin-top: 4px;
        }
        .category {
            display: inline-block;
            background: #e3e9f7;
            color: #2a4d8f;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.85em;
            margin-right: 8px;
        }
        .filter {
            margin-bottom: 20px;
        }
        select {
            font-size: 1em;
            padding: 6px 10px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
    </style>
    <script>
        function filterByCategory() {
            var selected = document.getElementById('categoryFilter').value;
            var articles = document.getElementsByClassName('article');
            for (var i = 0; i < articles.length; i++) {
                var cat = articles[i].getAttribute('data-category');
                if (selected === 'all' || cat === selected) {
                    articles[i].style.display = '';
                } else {
                    articles[i].style.display = 'none';
                }
            }
        }
    </script>
</head>
<body>
    <div class="header">
        <h1>Horizon Scanner</h1>
        <form method="get">
            <div class="filter">
                <label for="categoryFilter">Filter by category:</label>
                <select id="categoryFilter" name="category" onchange="filterByCategory()">
                    <option value="all">All</option>
                    {% for cat in categories %}
                    <option value="{{cat}}">{{cat}}</option>
                    {% endfor %}
                </select>
            </div>
        </form>
    </div>
    <div class="feed">
        {% for article in articles %}
        <div class="article" data-category="{{article['category']}}">
            <a class="title" href="{{article['url']}}" target="_blank">{{article['title']}}</a>
            <div class="meta">
                <span class="category">{{article['category']}}</span>
                <span>Source: {{article['source']}}</span>
                <span> | {{article['scraped_at']}}</span>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def index():
    articles = scrape_all_sources()
    categories = list(CATEGORY_KEYWORDS.keys())
    return render_template_string(HTML_TEMPLATE, articles=articles, categories=categories)

@app.route('/api/horizon-scan', methods=['GET'])
def get_horizon_articles():
    articles = scrape_all_sources()
    save_bulk(articles)
    return jsonify(articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 
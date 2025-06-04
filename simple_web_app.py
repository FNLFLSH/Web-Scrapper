from flask import Flask, render_template, jsonify, request
from scrapers.simple_scraper import scrape_all, CATEGORY_DESCRIPTIONS
import logging
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import defaultdict
import uuid

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

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
    # Add unique IDs to articles
    for article in articles:
        article['id'] = str(uuid.uuid4())
    categories = {article['category'] for article in articles}
    sources = {article['source_name'] for article in articles}
    logger.info(f"Scraped {len(articles)} articles")
    logger.info(f"Found {len(categories)} categories: {categories}")
    logger.info(f"Found {len(sources)} sources: {sources}")

def generate_summary(text, num_sentences=3):
    """Generate a summary of the text using extractive summarization."""
    # Tokenize sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words and remove stopwords
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word.isalnum() and word not in stop_words]
    
    # Calculate word frequencies
    freq_dist = FreqDist(filtered_words)
    
    # Score sentences based on word frequencies
    sentence_scores = defaultdict(float)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                sentence_scores[i] += freq_dist[word]
        sentence_scores[i] /= len(word_tokenize(sentence))
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    return ' '.join(sentences[i] for i, _ in top_sentences)

def extract_key_points(text, num_points=5):
    """Extract key points from the text."""
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    
    # Score sentences based on word importance
    sentence_scores = defaultdict(float)
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence.lower())
        important_words = [word for word in words if word.isalnum() and word not in stop_words]
        sentence_scores[i] = len(important_words)
    
    # Get top sentences as key points
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_points]
    top_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    return [sentences[i] for i, _ in top_sentences]

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

@app.route('/article/<article_id>')
def view_article(article_id):
    """View a specific article with summarization."""
    # Find the article by ID
    article = next((a for a in articles if a.get('id') == article_id), None)
    if not article:
        logger.error(f"Article not found with ID: {article_id}")
        return "Article not found", 404
    
    try:
        # Generate summary and key points from the article title and description
        text = f"{article['title']} {article.get('description', '')}"
        summary = generate_summary(text)
        key_points = extract_key_points(text)
        
        return render_template('article_view.html',
                             article=article,
                             summary=summary,
                             key_points=key_points)
    except Exception as e:
        logger.error(f"Error processing article {article_id}: {str(e)}")
        return "Error processing article", 500

@app.route('/article_chat', methods=['POST'])
def article_chat():
    """Handle chat messages about articles."""
    data = request.get_json()
    message = data.get('message', '').lower()
    article_id = data.get('article_id')
    
    article = next((a for a in articles if a.get('id') == article_id), None)
    if not article:
        return jsonify({'response': 'Article not found'})
    
    # Simple response generation based on keywords
    if 'summary' in message or 'summarize' in message:
        text = f"{article['title']} {article.get('description', '')}"
        summary = generate_summary(text)
        return jsonify({'response': summary})
    
    elif 'key points' in message or 'main points' in message:
        text = f"{article['title']} {article.get('description', '')}"
        key_points = extract_key_points(text)
        return jsonify({'response': 'Here are the key points:\n' + '\n'.join(f'• {point}' for point in key_points)})
    
    elif 'category' in message:
        return jsonify({'response': f'This article is categorized under {article["category"]}.'})
    
    elif 'source' in message:
        return jsonify({'response': f'This article is from {article["source_name"]}.'})
    
    else:
        return jsonify({'response': "I can help you with:\n• Getting a summary\n• Finding key points\n• Information about the category\n• Information about the source"})

if __name__ == '__main__':
    # Initial scrape
    update_articles()
    app.run(debug=True) 
import requests
from bs4 import BeautifulSoup
from config.categories import CATEGORY_KEYWORDS, TRACKED_COMPANIES
import time
import os
import re

NEWS_SOURCES = [
    {
        'name': 'Accounting Today',
        'url': 'https://www.accountingtoday.com',
        'domain': 'https://www.accountingtoday.com'
    },
    {
        'name': 'CFO Dive',
        'url': 'https://www.cfodive.com',
        'domain': 'https://www.cfodive.com'
    },
    {
        'name': 'Journal of Accountancy',
        'url': 'https://www.journalofaccountancy.com',
        'domain': 'https://www.journalofaccountancy.com'
    },
    {
        'name': 'AccountingWEB',
        'url': 'https://www.accountingweb.com',
        'domain': 'https://www.accountingweb.com'
    },
    # Add more sources as needed
]

def classify_article(title, content):
    """Classify article into one or more categories based on content."""
    title_lower = title.lower()
    content_lower = content.lower()
    categories = set()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in content_lower:
                categories.add(category)
    
    # If no categories found, default to 'accounting'
    return list(categories) if categories else ['accounting']

def find_mentioned_companies(content):
    """Find mentions of tracked companies in the content."""
    content_lower = content.lower()
    mentioned_companies = []
    
    for company_id, company_info in TRACKED_COMPANIES.items():
        for keyword in company_info['keywords']:
            if keyword.lower() in content_lower:
                mentioned_companies.append(company_info['name'])
                break
    
    return mentioned_companies

def universal_scraper(url, domain):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []
        seen = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            title = a.get_text(strip=True)
            if not title or href.startswith('#') or len(title) < 6:
                continue
            if not href.startswith('http'):
                href = domain.rstrip('/') + '/' + href.lstrip('/')
            if href in seen:
                continue
            seen.add(href)
            article = {
                'title': title,
                'url': href,
                'source': domain,
                'category': 'news',
                'content': '',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'companies': [],
            }
            article['category'] = classify_article(title, '')[0]
            articles.append(article)
        return articles
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

def scrape_all_sources():
    all_articles = []
    for source in NEWS_SOURCES:
        print(f"Scraping: {source['name']} ({source['url']})")
        articles = universal_scraper(source['url'], source['domain'])
        all_articles.extend(articles)
    print(f"Total articles scraped: {len(all_articles)}")
    return all_articles

if __name__ == "__main__":
    articles = scrape_all_sources()
    print(f"\nTotal articles found: {len(articles)}")
    if articles:
        print("\nSample article:")
        print(articles[0])
        if len(articles) > 1:
            print("\nSecond sample article:")
            print(articles[1]) 
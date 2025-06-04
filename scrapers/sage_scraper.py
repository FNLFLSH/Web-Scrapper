import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define sources
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
    }
]

INCUBATOR_SOURCES = [
    {
        'name': 'Y Combinator',
        'url': 'https://www.ycombinator.com/companies',
        'domain': 'https://www.ycombinator.com'
    },
    {
        'name': 'Techstars',
        'url': 'https://www.techstars.com/portfolio',
        'domain': 'https://www.techstars.com'
    },
    {
        'name': '500 Startups',
        'url': 'https://500.co/companies',
        'domain': 'https://500.co'
    }
]

# Define categories for filtering
CATEGORIES = {
    'fintech': ['fintech', 'finance', 'banking', 'payments', 'blockchain', 'crypto'],
    'accounting': ['accounting', 'bookkeeping', 'audit', 'tax'],
    'analytics': ['analytics', 'data', 'bi', 'business intelligence'],
    'sales': ['sales', 'crm', 'customer relationship'],
    'supply_chain': ['supply chain', 'logistics', 'inventory', 'procurement']
}

def classify_article(title, content, source_name=None):
    """Classify article into one or more categories based on content, with source-based fallback."""
    title_lower = title.lower()
    content_lower = content.lower()
    categories = set()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in content_lower:
                categories.add(category)
    if categories:
        return list(categories)
    # Fallback: assign a default category based on the source
    if source_name:
        if 'accounting' in source_name.lower():
            return ['accounting']
        if 'fintech' in source_name.lower():
            return ['fintech']
        if 'analytics' in source_name.lower():
            return ['analytics']
        if 'sales' in source_name.lower():
            return ['sales']
        if 'supply' in source_name.lower():
            return ['supply_chain']
    return ['uncategorized']

def scrape_news_sources():
    """Scrape articles from news sources using requests and BeautifulSoup."""
    all_articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Common navigation and non-article links to exclude
    NAV_LINKS = {
        'home', 'about', 'contact', 'login', 'sign up', 'subscribe', 'advertise', 
        'privacy policy', 'terms of use', 'cookie policy', 'sitemap', 'rss', 'feed',
        'latest', 'trending', 'popular', 'newsletter', 'search', 'account', 'profile',
        'settings', 'help', 'support', 'faq', 'subscription', 'subscription agreement'
    }
    
    for source in NEWS_SOURCES:
        logger.info(f"Scraping news source: {source['name']} ({source['url']})")
        try:
            # Disable SSL verification for AccountingWEB
            verify_ssl = False if 'accountingweb.com' in source['url'] else True
            response = requests.get(source['url'], headers=headers, timeout=10, verify=verify_ssl)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            seen_urls = set()
            seen_titles = set()
            articles_found = 0
            
            # Look for article links in common locations
            article_links = []
            
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=['content', 'main', 'article'])
            if main_content:
                article_links.extend(main_content.find_all('a', href=True))
            
            # Also look for article lists
            article_lists = soup.find_all(['div', 'section'], class_=['article-list', 'news-list', 'stories', 'posts'])
            for article_list in article_lists:
                article_links.extend(article_list.find_all('a', href=True))
            
            # If we didn't find enough links, look everywhere
            if len(article_links) < 5:
                article_links = soup.find_all('a', href=True)
            
            logger.info(f"Found {len(article_links)} potential links on {source['name']}")
            
            for a in article_links:
                href = a['href']
                title = a.get_text(strip=True)
                
                # Skip if no title or too short
                if not title or len(title) < 10:  # Increased minimum length
                    continue
                    
                # Skip if it's just a navigation link
                if title.lower() in NAV_LINKS:
                    continue
                
                # Skip if it's a duplicate title
                if title.lower() in seen_titles:
                    continue
                
                # Handle relative URLs
                if not href.startswith('http'):
                    href = source['domain'].rstrip('/') + '/' + href.lstrip('/')
                
                # Skip if we've seen this URL before
                if href in seen_urls:
                    continue
                
                # Skip if it's not an article URL (e.g., category pages, tag pages)
                if any(x in href.lower() for x in ['/tag/', '/category/', '/author/', '/page/', '/feed/', '/rss/']):
                    continue
                
                seen_urls.add(href)
                seen_titles.add(title.lower())
                categories = classify_article(title, '', source['name'])
                
                for category in categories:
                    article = {
                        'title': title,
                        'url': href,
                        'source': 'news',
                        'source_detail': source['name'],
                        'category': category,
                        'content': '',
                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    all_articles.append(article)
                    articles_found += 1
                    
            logger.info(f"Found {articles_found} unique articles from {source['name']}")
            
        except Exception as e:
            logger.error(f"Error scraping {source['url']}: {e}")
    
    logger.info(f"Total news articles collected: {len(all_articles)}")
    return all_articles

def scrape_incubator_sources():
    """Scrape companies from incubator sources (e.g., Y Combinator) using Selenium."""
    all_articles = []
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    
    # Common navigation and non-company links to exclude
    NAV_LINKS = {
        'home', 'about', 'contact', 'login', 'sign up', 'subscribe', 'advertise', 
        'privacy policy', 'terms of use', 'cookie policy', 'sitemap', 'rss', 'feed',
        'latest', 'trending', 'popular', 'newsletter', 'search', 'account', 'profile',
        'settings', 'help', 'support', 'faq', 'subscription'
    }
    
    try:
        for source in INCUBATOR_SOURCES:
            logger.info(f"Scraping incubator source: {source['name']} ({source['url']})")
            driver.get(source['url'])
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Wait a bit for dynamic content to load
            time.sleep(5)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            seen_urls = set()
            seen_titles = set()
            articles_found = 0
            
            # Look for company links in common locations
            company_links = []
            
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=['content', 'main', 'companies'])
            if main_content:
                company_links.extend(main_content.find_all('a', href=True))
            
            # Also look for company lists
            company_lists = soup.find_all(['div', 'section'], class_=['company-list', 'portfolio', 'companies'])
            for company_list in company_lists:
                company_links.extend(company_list.find_all('a', href=True))
            
            # If we didn't find enough links, look everywhere
            if len(company_links) < 5:
                company_links = soup.find_all('a', href=True)
            
            logger.info(f"Found {len(company_links)} potential links on {source['name']}")
            
            for a in company_links:
                href = a['href']
                title = a.get_text(strip=True)
                
                # Skip if no title or too short
                if not title or len(title) < 10:  # Increased minimum length
                    continue
                    
                # Skip if it's just a navigation link
                if title.lower() in NAV_LINKS:
                    continue
                
                # Skip if it's a duplicate title
                if title.lower() in seen_titles:
                    continue
                
                # Handle relative URLs
                if not href.startswith('http'):
                    href = source['domain'].rstrip('/') + '/' + href.lstrip('/')
                
                # Skip if we've seen this URL before
                if href in seen_urls:
                    continue
                
                # Skip if it's not a company URL
                if any(x in href.lower() for x in ['/tag/', '/category/', '/author/', '/page/', '/feed/', '/rss/']):
                    continue
                
                seen_urls.add(href)
                seen_titles.add(title.lower())
                categories = classify_article(title, '', source['name'])
                
                for category in categories:
                    article = {
                        'title': title,
                        'url': href,
                        'source': 'incubator',
                        'source_detail': source['name'],
                        'category': category,
                        'content': '',
                        'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    all_articles.append(article)
                    articles_found += 1
                    
            logger.info(f"Found {articles_found} unique companies from {source['name']}")
            
    except Exception as e:
        logger.error(f"Error during incubator scraping: {e}")
    finally:
        driver.quit()
    
    logger.info(f"Total incubator articles collected: {len(all_articles)}")
    return all_articles

def scrape_all_sources():
    """Scrape articles from both news and incubator sources."""
    news_articles = scrape_news_sources()
    incubator_articles = scrape_incubator_sources()
    all_articles = news_articles + incubator_articles
    logger.info(f"Total articles scraped: {len(all_articles)}")
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from horizon_scanner.config.categories import CATEGORY_KEYWORDS
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def classify_article(title, content):
    title_lower = title.lower()
    content_lower = content.lower()
    categories = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in content_lower:
                categories.add(category)
    return list(categories) if categories else ['accounting']

def scrape_accounting_today_selenium():
    url = 'https://www.accountingtoday.com/'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)  # 20 second timeout
    
    try:
        logger.info(f"Navigating to {url}")
        driver.get(url)
        
        # Wait for the main content to load
        logger.info("Waiting for main content to load...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # Try multiple selectors that might match articles
        selectors = [
            'article a',  # Generic article links
            '.article-list-item a',  # Article list items
            '.headline a',  # Headline links
            'a[href*="/news/"]',  # News links
            'a[href*="/article/"]',  # Article links
            '.card a',  # Card links
            '.story a'  # Story links
        ]
        
        articles = []
        for selector in selectors:
            logger.info(f"Trying selector: {selector}")
            try:
                # Wait for elements to be present
                elements = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                logger.info(f"Found {len(elements)} elements with selector {selector}")
                
                for elem in elements:
                    try:
                        title = elem.text.strip()
                        link = elem.get_attribute('href')
                        
                        # Only process if we have both title and link
                        if title and link and 'accountingtoday.com' in link:
                            categories = classify_article(title, "")
                            for category in categories:
                                articles.append({
                                    'title': title,
                                    'url': link,
                                    'source': 'AccountingToday',
                                    'category': category,
                                    'content': ''
                                })
                                logger.info(f"Added article: {title}")
                    except Exception as e:
                        logger.error(f"Error processing element: {str(e)}")
                        continue
                        
            except TimeoutException:
                logger.warning(f"Timeout waiting for selector: {selector}")
                continue
            except Exception as e:
                logger.error(f"Error with selector {selector}: {str(e)}")
                continue
        
        # Remove duplicates based on URL
        unique_articles = {article['url']: article for article in articles}.values()
        return list(unique_articles)
        
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return []
        
    finally:
        driver.quit()

if __name__ == "__main__":
    articles = scrape_accounting_today_selenium()
    print(f"\nTotal articles found: {len(articles)}")
    if articles:
        print("\nSample article:")
        print(articles[0])
        if len(articles) > 1:
            print("\nSecond sample article:")
            print(articles[1]) 
import requests
from bs4 import BeautifulSoup
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define sources with clear categorization
SOURCES = {
    'news': [
        {
            'name': 'Accounting Today',
            'url': 'https://www.accountingtoday.com',
            'category': 'accounting'
        },
        {
            'name': 'CFO Dive',
            'url': 'https://www.cfodive.com',
            'category': 'fintech'
        },
        {
            'name': 'Journal of Accountancy',
            'url': 'https://www.journalofaccountancy.com',
            'category': 'accounting'
        },
        {
            'name': 'AccountingWEB',
            'url': 'https://www.accountingweb.com',
            'category': 'practice_mgmt'
        },
        {
            'name': 'Tax Notes',
            'url': 'https://www.taxnotes.com',
            'category': 'tax'
        },
        {
            'name': 'CPA Practice Advisor',
            'url': 'https://www.cpapracticeadvisor.com',
            'category': 'practice_mgmt'
        },
        {
            'name': 'Accounting Today - Tax',
            'url': 'https://www.accountingtoday.com/tax',
            'category': 'tax'
        },
        {
            'name': 'Accounting Today - Technology',
            'url': 'https://www.accountingtoday.com/technology',
            'category': 'tech'
        },
        {
            'name': 'Accounting Today - Audit',
            'url': 'https://www.accountingtoday.com/audit',
            'category': 'audit'
        },
        {
            'name': 'Accounting Today - Practice Management',
            'url': 'https://www.accountingtoday.com/practice-management',
            'category': 'practice_mgmt'
        }
    ],
    'incubator': [
        {
            'name': 'Y Combinator',
            'url': 'https://www.ycombinator.com/companies',
            'category': 'startups',
            'requires_js': True
        },
        {
            'name': 'Techstars',
            'url': 'https://www.techstars.com/portfolio',
            'category': 'startups'
        },
        {
            'name': '500 Startups',
            'url': 'https://500.co/companies',
            'category': 'startups'
        }
    ]
}

# Define category descriptions for reference
CATEGORY_DESCRIPTIONS = {
    'accounting': 'General accounting news and updates',
    'tax': 'Tax law, tax policy, IRS, and tax tech',
    'audit': 'Auditing standards, news, and automation',
    'fintech': 'Financial technology, payments, digital banking',
    'SaaS': 'Software-as-a-Service industry news',
    'AI': 'Artificial intelligence in accounting/finance',
    'automation': 'Workflow, RPA, and process automation',
    'enterprise': 'Enterprise software, ERP, large org tech',
    'startups': 'Startup launches, funding, and innovation',
    'regulation': 'Compliance, legal, and regulatory news',
    'cybersecurity': 'Security, data privacy, and risk',
    'analytics': 'Data analytics, BI, and reporting',
    'cloud': 'Cloud computing, migration, and services',
    'tech': 'General technology news',
    'practice_mgmt': 'Practice management, firm operations',
    'payroll': 'Payroll tech and news',
    'blockchain': 'Blockchain, crypto, and distributed ledger'
}

def setup_selenium():
    """Set up and return a configured Selenium WebDriver."""
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        # Use webdriver_manager to handle Chrome driver installation
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logger.error(f"Error setting up Selenium: {e}")
        raise

def scrape_source_with_selenium(source, source_type):
    """Scrape a source that requires JavaScript rendering."""
    articles = []
    driver = None
    
    try:
        driver = setup_selenium()
        wait = WebDriverWait(driver, 30)
        
        logger.info(f"Scraping {source['name']} with Selenium")
        driver.get(source['url'])
        
        # Wait for content to load
        time.sleep(10)
        
        if source['name'] == 'Y Combinator':
            try:
                # Wait for company cards to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'company-card')))
                
                # Scroll to load more companies
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    # Scroll down
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)  # Wait for content to load
                    
                    # Calculate new scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                
                # Find all company cards
                company_cards = driver.find_elements(By.CLASS_NAME, 'company-card')
                logger.info(f"Found {len(company_cards)} companies on Y Combinator")
                
                for card in company_cards:
                    try:
                        # Try different selectors for company name
                        title = None
                        for selector in ['.company-name', 'h3', '.name']:
                            try:
                                title = card.find_element(By.CSS_SELECTOR, selector).text
                                if title:
                                    break
                            except:
                                continue
                        
                        # Try different selectors for URL
                        url = None
                        for selector in ['a', '.company-link']:
                            try:
                                url = card.find_element(By.CSS_SELECTOR, selector).get_attribute('href')
                                if url:
                                    break
                            except:
                                continue
                        
                        if title and url:
                            article = {
                                'title': title,
                                'url': url,
                                'source_type': source_type,
                                'source_name': source['name'],
                                'category': source['category'],
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing YC company card: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error scraping Y Combinator companies: {e}")
                # Take screenshot for debugging
                try:
                    driver.save_screenshot('yc_error.png')
                    logger.info("Saved error screenshot to yc_error.png")
                except:
                    pass
        elif source['name'] == 'TechCrunch':
            try:
                # Wait for article cards to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'post-block')))
                article_cards = driver.find_elements(By.CLASS_NAME, 'post-block')
                logger.info(f"Found {len(article_cards)} articles on TechCrunch")
                
                for card in article_cards:
                    try:
                        title = card.find_element(By.CLASS_NAME, 'post-block__title').text
                        url = card.find_element(By.CSS_SELECTOR, 'a.post-block__title__link').get_attribute('href')
                        if title and url:
                            article = {
                                'title': title,
                                'url': url,
                                'source_type': source_type,
                                'source_name': source['name'],
                                'category': source['category'],
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing TechCrunch article: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error scraping TechCrunch: {e}")
                # Take screenshot for debugging
                try:
                    driver.save_screenshot('techcrunch_error.png')
                    logger.info("Saved error screenshot to techcrunch_error.png")
                except:
                    pass
        elif source['name'] == 'VentureBeat':
            try:
                # Wait for article cards to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Article')))
                article_cards = driver.find_elements(By.CLASS_NAME, 'Article')
                logger.info(f"Found {len(article_cards)} articles on VentureBeat")
                
                for card in article_cards:
                    try:
                        title = card.find_element(By.CLASS_NAME, 'Article__title').text
                        url = card.find_element(By.CSS_SELECTOR, 'a.Article__title-link').get_attribute('href')
                        if title and url:
                            article = {
                                'title': title,
                                'url': url,
                                'source_type': source_type,
                                'source_name': source['name'],
                                'category': source['category'],
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing VentureBeat article: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error scraping VentureBeat: {e}")
                try:
                    driver.save_screenshot('venturebeat_error.png')
                    logger.info("Saved error screenshot to venturebeat_error.png")
                except:
                    pass
        elif source['name'] == 'Business Insider':
            try:
                # Wait for article cards to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tout')))
                article_cards = driver.find_elements(By.CLASS_NAME, 'tout')
                logger.info(f"Found {len(article_cards)} articles on Business Insider")
                
                for card in article_cards:
                    try:
                        title = card.find_element(By.CLASS_NAME, 'tout__title').text
                        url = card.find_element(By.CSS_SELECTOR, 'a.tout__link').get_attribute('href')
                        if title and url:
                            article = {
                                'title': title,
                                'url': url,
                                'source_type': source_type,
                                'source_name': source['name'],
                                'category': source['category'],
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing Business Insider article: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error scraping Business Insider: {e}")
                try:
                    driver.save_screenshot('businessinsider_error.png')
                    logger.info("Saved error screenshot to businessinsider_error.png")
                except:
                    pass
        elif source['name'] == 'Bloomberg':
            try:
                # Wait for article cards to load
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'story-list-story')))
                article_cards = driver.find_elements(By.CLASS_NAME, 'story-list-story')
                logger.info(f"Found {len(article_cards)} articles on Bloomberg")
                
                for card in article_cards:
                    try:
                        title = card.find_element(By.CLASS_NAME, 'headline__text').text
                        url = card.find_element(By.CSS_SELECTOR, 'a.headline__text').get_attribute('href')
                        if title and url:
                            article = {
                                'title': title,
                                'url': url,
                                'source_type': source_type,
                                'source_name': source['name'],
                                'category': source['category'],
                                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }
                            articles.append(article)
                    except Exception as e:
                        logger.error(f"Error processing Bloomberg article: {e}")
                        continue
            except Exception as e:
                logger.error(f"Error scraping Bloomberg: {e}")
                try:
                    driver.save_screenshot('bloomberg_error.png')
                    logger.info("Saved error screenshot to bloomberg_error.png")
                except:
                    pass
        
        logger.info(f"Found {len(articles)} unique articles from {source['name']}")
        
    except Exception as e:
        logger.error(f"Error scraping {source['url']} with Selenium: {e}")
    finally:
        if driver:
            driver.quit()
    
    return articles

def scrape_source(source, source_type):
    """Scrape a single source and return its articles."""
    # If source is Y Combinator, use the public JSON API
    if source['name'] == 'Y Combinator':
        logger.info('Fetching Y Combinator companies from public JSON API')
        articles = []
        try:
            resp = requests.get('https://yc-oss.github.io/api/companies/all.json', timeout=20)
            resp.raise_for_status()
            companies = resp.json()
            logger.info(f"Fetched {len(companies)} companies from YC API")
            for company in companies:
                # Use company name, website, and YC profile URL
                title = company.get('name')
                url = company.get('website') or company.get('url')
                yc_url = company.get('url')
                industry = company.get('industry') or 'startups'
                
                # Skip companies not related to accounting/fintech
                if industry.lower() in ['healthcare', 'consumer', 'retail', 'food', 'fashion', 'entertainment', 'media', 'sports']:
                    continue
                
                # Map industry to our categories
                category_mapping = {
                    'fintech': 'fintech',
                    'financial services': 'fintech',
                    'software': 'SaaS',
                    'enterprise software': 'enterprise',
                    'artificial intelligence': 'AI',
                    'blockchain': 'blockchain',
                    'cybersecurity': 'cybersecurity',
                    'data': 'analytics',
                    'cloud': 'cloud',
                    'payroll': 'payroll',
                    'accounting': 'accounting',
                    'tax': 'tax',
                    'audit': 'audit',
                    'compliance': 'regulation',
                    'automation': 'automation'
                }
                
                category = category_mapping.get(industry.lower(), 'startups')
                
                if title and url:
                    article = {
                        'title': title,
                        'url': url,
                        'source_type': source_type,
                        'source_name': source['name'],
                        'category': category,
                        'yc_url': yc_url,
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    articles.append(article)
            logger.info(f"Returning {len(articles)} YC companies from API")
        except Exception as e:
            logger.error(f"Error fetching YC companies from API: {e}")
        return articles
    
    # If source requires JavaScript, use Selenium
    if source.get('requires_js', False):
        return scrape_source_with_selenium(source, source_type)
    
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Disable SSL verification for AccountingWEB
        verify_ssl = False if 'accountingweb.com' in source['url'] else True
        response = requests.get(source['url'], headers=headers, timeout=10, verify=verify_ssl)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        seen_urls = set()
        
        # Find all links
        links = soup.find_all('a', href=True)
        logger.info(f"Found {len(links)} potential links on {source['name']}")
        
        for link in links:
            href = link['href']
            title = link.get_text(strip=True)
            
            # Skip if no title or too short
            if not title or len(title) < 10:
                continue
            
            # Handle relative URLs
            if not href.startswith('http'):
                href = source['url'].rstrip('/') + '/' + href.lstrip('/')
            
            # Skip if we've seen this URL
            if href in seen_urls:
                continue
            
            # Skip navigation links and irrelevant categories
            skip_keywords = ['/tag/', '/category/', '/author/', '/page/', '/feed/', '/rss/',
                           'healthcare', 'medical', 'consumer', 'retail', 'food', 'fashion',
                           'entertainment', 'media', 'sports']
            if any(x in href.lower() for x in skip_keywords):
                continue
            
            seen_urls.add(href)
            
            article = {
                'title': title,
                'url': href,
                'source_type': source_type,
                'source_name': source['name'],
                'category': source['category'],
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            articles.append(article)
            
        logger.info(f"Found {len(articles)} unique articles from {source['name']}")
        
    except Exception as e:
        logger.error(f"Error scraping {source['url']}: {e}")
    
    return articles

def scrape_all():
    """Scrape all sources and return all articles."""
    all_articles = []
    
    # Scrape news sources
    for source in SOURCES['news']:
        articles = scrape_source(source, 'news')
        all_articles.extend(articles)
    
    # Scrape incubator sources
    for source in SOURCES['incubator']:
        articles = scrape_source(source, 'incubator')
        all_articles.extend(articles)
    
    logger.info(f"Total articles collected: {len(all_articles)}")
    return all_articles

if __name__ == '__main__':
    articles = scrape_all()
    print(f"\nScraped {len(articles)} articles:")
    for article in articles[:5]:  # Print first 5 articles as sample
        print(f"\nTitle: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Source: {article['source_name']} ({article['source_type']})")
        print(f"Category: {article['category']}")
        print(f"Scraped at: {article['scraped_at']}") 
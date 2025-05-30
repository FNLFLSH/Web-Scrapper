from setup_dynamodb import create_dynamodb_table
from scrapers.accounting_today import scrape_accounting_today
from db_utils import save_bulk
import time

def test_scraper():
    print("1. Creating DynamoDB table...")
    create_dynamodb_table()
    
    print("\n2. Scraping Accounting Today...")
    articles = scrape_accounting_today()
    print(f"Found {len(articles)} articles")
    
    if articles:
        print("\nSample article:")
        print(f"Title: {articles[0]['title']}")
        print(f"Category: {articles[0]['category']}")
        print(f"URL: {articles[0]['url']}")
    
    print("\n3. Saving articles to DynamoDB...")
    save_bulk(articles)
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    test_scraper() 
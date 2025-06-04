from scrapers.accounting_today import scrape_all_sources
from db_utils import save_bulk

def main():
    articles = scrape_all_sources()
    save_bulk(articles)

if __name__ == '__main__':
    main() 
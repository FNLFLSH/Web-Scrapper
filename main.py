from scrapers.accounting_today import scrape_accounting_today
from db_utils import save_bulk

def main():
    articles = scrape_accounting_today()
    save_bulk(articles)

if __name__ == '__main__':
    main() 
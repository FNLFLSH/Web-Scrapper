# Sage Webscraper

A specialized web scraper for accounting and fintech news, built with Python and Flask.

## Features

- Real-time scraping of accounting and fintech news sources
- Category-based filtering
- Source-based filtering
- Modern, responsive UI with loading states
- Support for both news and incubator sources

## Sources

### News Sources
- Accounting Today
- CFO Dive
- Journal of Accountancy
- AccountingWEB
- Tax Notes
- CPA Practice Advisor

### Incubator Sources
- Y Combinator
- Techstars
- 500 Startups

## Categories

- Accounting
- Tax
- Audit
- Fintech
- SaaS
- AI
- Automation
- Enterprise
- Startups
- Regulation
- Cybersecurity
- Analytics
- Cloud
- Tech
- Practice Management
- Payroll
- Blockchain

## Setup

1. Clone the repository:
```bash
git clone https://github.com/FNLFLSH/sage-webscraper.git
cd sage-webscraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python simple_web_app.py
```

The application will be available at `http://localhost:5000`

## Dependencies

- Flask
- BeautifulSoup4
- Requests
- Selenium (for JavaScript-rendered content)

## License

MIT License
from src.utils.scraping_utils import scrape_domain_urls_with_selenium

class CrawlerService:
    def __init__(self):
        pass

    def scrape(self, domain):
        return scrape_domain_urls_with_selenium(domain)

    def crawl_page(self, domain):
        return scrape_domain_urls_with_selenium(domain)
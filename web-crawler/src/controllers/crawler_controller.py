from flask import request, jsonify
from src.services.crawler_service import CrawlerService

crawler_service = CrawlerService()


def start_scraping(initial_urls):
    scraped_urls = set()  # Set to store unique URLs
    urls_to_scrape = initial_urls.copy()

    while urls_to_scrape:
        url = urls_to_scrape.pop(0)  # Take the first URL from the list
        if url not in scraped_urls:
            scraped_urls.add(url)
            new_urls = crawler_service.crawl_page(url)  # Scrape the URL and get new URLs
            # Add new URLs to the list to scrape if not already scraped
            urls_to_scrape.extend([new_url for new_url in new_urls if new_url not in scraped_urls])

    return scraped_urls



def scrape():
    try:
        initial_urls = request.json.get("urls", [])
        if not initial_urls:
            return jsonify({"error": "No initial URLs provided"}), 400

        scraped_urls = start_scraping(initial_urls)
        return jsonify({"scraped_urls": list(scraped_urls)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
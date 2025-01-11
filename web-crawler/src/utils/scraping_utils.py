import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


logging.basicConfig(level=logging.INFO)


def setup_driver():
    options = Options()
    options.headless = True  # Run in headless mode (no UI)

    # Use Service to specify the ChromeDriver location
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_domain_urls_with_selenium(domain):
    """Scrapes all URLs from a given domain with Selenium."""
    try:
        logging.info(f"Starting scraping for {domain}")
        driver = setup_driver()
        driver.get(domain)

        logging.info(f"Waiting for page to load for {domain}...")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

        time.sleep(5)

        urls = set()

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logging.info(f"Page scroll completed for {domain}")
                break
            last_height = new_height

        links = driver.find_elements(By.TAG_NAME, 'a')
        logging.info(f"Extracting {len(links)} links from {domain}")
        for link in links:
            href = link.get_attribute('href')
            if href:
                if href.startswith('http') or href.startswith('www'):
                    urls.add(href)
                elif href.startswith('/'):  # Handle relative URLs
                    full_url = domain + href
                    urls.add(full_url)

        driver.quit()

        logging.info(f"Scraping completed for {domain}. Found {len(urls)} URLs.")
        return list(urls)
    except Exception as e:
        logging.error(f"Error occurred while scraping {domain}: {str(e)}")
        return []
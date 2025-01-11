from flask import Blueprint
from src.controllers.crawler_controller import scrape

scraper_bp = Blueprint('scraper', __name__)

# Define the route to start scraping
scraper_bp.route('/scrape', methods=['POST'])(scrape)
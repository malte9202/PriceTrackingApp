import requests  # used for http-requests
from bs4 import BeautifulSoup  # for scraping the websites


# create scraper class
class Scraper:
    @staticmethod  # static
    def scrape_price(url: str) -> float:
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 '
                          '(KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'
        }
        page = requests.get(url, headers=headers)
        scrape = BeautifulSoup(page.content, 'html.parser')
        price_range = scrape.select_one('.variant__header__pricehistory__pricerange').get_text(strip=True).split('b')
        price = float(price_range[0][2:].replace(",", "."))
        return price

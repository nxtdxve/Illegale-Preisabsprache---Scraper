import requests
from bs4 import BeautifulSoup
from app.utils.price_cleaner import clean_price
from app.utils.selector_util import get_domain_selector
import logging

def scrape_universal(url):
    """
    Ermittelt den Preis eines Produkts von einer Website anhand der URL und des passenden Selektors.
    
    :param url: Die URL der Produktseite.
    :return: Den ermittelten Preis als String oder None, falls nicht ermittelbar.
    """
    selector = get_domain_selector(url)
    if selector is None:
        return None

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.select_one(selector)
        if price_element:
            return clean_price(price_element.text)
        else:
            logging.warning(f"Preiselement für URL {url} nicht gefunden.")
            return None
    except requests.RequestException as e:
        logging.error(f"Fehler bei der Anfrage: {e}")
        return None

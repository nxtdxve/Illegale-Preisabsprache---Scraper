import requests
import logging
from bs4 import BeautifulSoup
from app.utils.price_cleaner import clean_price

def scrape_hornbach_price(url):
    """
    Ermittelt den Preis eines Produkts von der Hornbach-Website.
    
    :param url: Die URL der Produktseite auf der Hornbach-Website.
    :return: Den ermittelten Preis als String oder None, falls nicht ermittelbar.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('div', {'data-testid': 'prices'}).find('span')
        if price_element:
            return clean_price(price_element.text)
        else:
            logging.warning("Preiselement bei Hornbach nicht gefunden.")
            return None
    except requests.RequestException as e:
        logging.error(f"Fehler bei der Anfrage an Hornbach: {e}")
        return None

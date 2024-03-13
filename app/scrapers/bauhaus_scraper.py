import requests
import logging
from bs4 import BeautifulSoup
from app.utils.price_cleaner import clean_price

def scrape_bauhaus_price(url):
    """
    Ermittelt den Preis eines Produkts von der Bauhaus-Website.
    
    :param url: Die URL der Produktseite auf der Bauhaus-Website.
    :return: Den ermittelten Preis als String oder None, falls nicht ermittelbar.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_element = soup.find('wc-price', {'id': 'wc-product-detail-price'})
        if price_element:
            return clean_price(price_element.get('price'))
        else:
            logging.warning("Preiselement bei Bauhaus nicht gefunden.")
            return None
    except requests.RequestException as e:
        logging.error(f"Fehler bei der Anfrage an Bauhaus: {e}")
        return None

import logging
import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from dotenv import load_dotenv

# Grundkonfiguration für Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Laden der .env-Datei zur Konfiguration
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Verbindung zur MongoDB herstellen
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    logging.critical("Die MONGO_URI Umgebungsvariable ist nicht gesetzt.")
    raise ValueError("Die MONGO_URI Umgebungsvariable ist nicht gesetzt.")
else:
    client = MongoClient(MONGO_URI)
    db = client.PriceTracker
    logging.info("Erfolgreich mit der MongoDB verbunden.")

def clean_price(price_str):
    """
    Bereinigt einen gegebenen Preis-String und konvertiert ihn in ein Dezimalformat.
    
    :param price_str: Der zu bereinigende Preis-String.
    :return: Den bereinigten Preis als String im Dezimalformat.
    """
    match = re.search(r'\d+(\.\d+)?', price_str)
    return f"{float(match.group(0)):.2f}" if match else None

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

def update_price_records():
    """
    Durchläuft alle Produkte in der Datenbank und aktualisiert ihre Preisdatensätze.
    
    Es werden die aktuellen Preise von den jeweiligen Einzelhändler-Webseiten gescraped und,
    falls sich der Preis geändert hat, wird ein neuer Preisdatensatz erstellt.
    """
    logging.info("Beginne mit der Aktualisierung der Preisdatensätze.")
    products = db.products.find({})
    for product in products:
        for retailer_url in product['retailer_urls']:
            retailer_id = retailer_url['retailer_id']
            url = retailer_url['url']
            if db.retailers.find_one({"_id": retailer_id})['name'] == 'Bauhaus':
                price = scrape_bauhaus_price(url)
            elif db.retailers.find_one({"_id": retailer_id})['name'] == 'Hornbach':
                price = scrape_hornbach_price(url)
            else:
                price = None
            if price:
                latest_record = db.price_records.find_one(
                    {"product_id": product['_id'], "retailer_id": retailer_id},
                    sort=[("timestamp", -1)]
                )
                if not latest_record or Decimal128(price) != latest_record['price']:
                    db.price_records.insert_one({
                        "product_id": product['_id'],
                        "retailer_id": retailer_id,
                        "timestamp": datetime.now(),
                        "price": Decimal128(price)
                    })
                    logging.info(f"Preis für Produkt {product['_id']} aktualisiert: {price}")
    logging.info("Aktualisierung der Preisdatensätze abgeschlossen.")

if __name__ == "__main__":
    try:
        update_price_records()
    except Exception as e:
        logging.exception("Ein Fehler ist aufgetreten beim Ausführen des Skripts.", exc_info=e)
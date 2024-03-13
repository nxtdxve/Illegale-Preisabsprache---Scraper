import logging
from app.database.db_connection import get_db_connection
from app.scrapers.bauhaus_scraper import scrape_bauhaus_price
from app.scrapers.hornbach_scraper import scrape_hornbach_price
from app.utils.logging_config import setup_logging
from bson.decimal128 import Decimal128
from datetime import datetime

setup_logging()

def update_price_records():
    """
    Durchläuft alle Produkte in der Datenbank und aktualisiert ihre Preisdatensätze.
    
    Es werden die aktuellen Preise von den jeweiligen Einzelhändler-Webseiten gescraped und,
    falls sich der Preis geändert hat, wird ein neuer Preisdatensatz erstellt.
    """
    db = get_db_connection()
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

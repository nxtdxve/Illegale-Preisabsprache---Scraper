import sched
import time
import logging
from app.database.db_connection import get_db_connection
from app.scrapers.universal_scraper import scrape_universal
from bson.decimal128 import Decimal128
from datetime import datetime
from app import config

# Initialisiere Scheduler
scheduler = sched.scheduler(time.time, time.sleep)

def update_price_records(sched_time=None):
    """
    Durchläuft alle Produkte in der Datenbank und aktualisiert ihre Preisdatensätze mit dem universellen Scraper.
    """
    try:
        db = get_db_connection()
        logging.info("Beginne mit der Aktualisierung der Preisdatensätze.")
        products = db.products.find({})
        for product in products:
            for retailer_url in product['retailer_urls']:
                url = retailer_url['url']
                price = scrape_universal(url)
                if price:
                    retailer_id = retailer_url['retailer_id']
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
        # Planen des nächsten Laufs
        schedule_next_run()
    except Exception as e:
        logging.exception("Ein unerwarteter Fehler ist aufgetreten: ", exc_info=e)

def schedule_next_run():
    """
    Plant die nächste Ausführung der `update_price_records`-Funktion basierend auf dem Zeitintervall in der Konfiguration.
    """
    try:
        frequency = int(config['Scheduler']['frequency']) * 60  # Konvertiere Minuten in Sekunden
        scheduler.enter(frequency, 1, update_price_records)
    except Exception as e:
        logging.exception("Fehler beim Planen des nächsten Laufs: ", exc_info=e)

if __name__ == "__main__":
    try:
        # Führe die Funktion direkt aus, um sofort zu starten
        update_price_records()
        # Starte den Scheduler
        scheduler.run()
    except Exception as e:
        logging.exception("Ein Fehler ist beim Starten des Schedulers aufgetreten: ", exc_info=e)

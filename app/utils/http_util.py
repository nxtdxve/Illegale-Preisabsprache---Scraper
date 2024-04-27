import requests
from app import config
import os
import logging
from dotenv import load_dotenv

load_dotenv()


def send_price_change_notification(product_id, retailer_id, new_price):
    """
    Sendet eine Benachrichtigung über eine Preisänderung an das Backend.

    :param product_id: Die ID des Produkts, dessen Preis sich geändert hat.
    :param retailer_id: Die ID des Einzelhändlers, bei dem der Preis gefunden wurde.
    :param new_price: Der neue Preis des Produkts.
    """
    url = config['API']['URL'] + "/notify_price_change"
    headers = {"X-API-KEY": os.environ.get("API_KEY")}
    data = {
        "product_id": str(product_id),
        "retailer_id": str(retailer_id),
        "new_price": str(new_price),
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        logging.info(f"Preisänderung erfolgreich an das Backend gemeldet: {response.text}")
    else:
        logging.error(f"Fehler beim Senden der Preisänderung: {response.status_code} - {response.text}")
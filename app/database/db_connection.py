import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv
from app import config

load_dotenv()

def get_db_connection():
    """
    Verbindung zur MongoDB herstellen
    """
    # Lädt die Konfiguration
    db_name = config['Database']['db_name']

    mongo_uri = os.environ.get("MONGO_URI")
    if not mongo_uri:
        logging.critical("Die MONGO_URI Umgebungsvariable ist nicht gesetzt.")
        raise ValueError("Die MONGO_URI Umgebungsvariable ist nicht gesetzt.")
    try:
        client = MongoClient(mongo_uri)
        # Verbindung testen
        client.admin.command('ping')
        logging.info("Erfolgreich mit der MongoDB verbunden.")
    except Exception as e:
        logging.error(f"Fehler bei der Verbindung zur MongoDB: {e}")
        raise e
    return client.get_database(db_name)

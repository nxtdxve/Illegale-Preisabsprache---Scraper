import os
import logging
from logging.handlers import RotatingFileHandler
from app.utils.load_config import load_config
from app import config

def setup_logging():
    """
    Konfiguriert das Logging-System mit den Einstellungen aus der Konfigurationsdatei.
    """
    # Lädt die Konfiguration
    log_format = config['Logging']['format']
    log_folder = config['Logging']['folder']
    log_datefmt = config['Logging']['datefmt']
    log_file_path = os.path.join(os.path.dirname(__file__), '..', '..', log_folder, 'application.log')
    
    # Erstellt den Log-Ordner, falls er nicht existiert
    if not os.path.exists(os.path.dirname(log_file_path)):
        os.makedirs(os.path.dirname(log_file_path))

    # Konfiguriert das Logging-System mit dem spezifizierten Format und Pfad
    logging.basicConfig(level=logging.INFO,
                        format=log_format,
                        datefmt=log_datefmt,
                        handlers=[RotatingFileHandler(log_file_path, maxBytes=10485760, backupCount=5, encoding='utf-8'),
                                logging.StreamHandler()])

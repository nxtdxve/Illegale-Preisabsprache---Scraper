import os
import logging
from logging.handlers import RotatingFileHandler
from app.utils.load_config import load_config

def setup_logging():
    """
    Konfiguriert das Logging-System mit den Einstellungen aus der Konfigurationsdatei.
    """
    try:
        config = load_config()
        log_format = config['Logging']['format']
        log_folder = config['Logging']['folder']
        log_datefmt = config['Logging']['datefmt']
        log_file_path = os.path.join(os.path.dirname(__file__), '..', '..', log_folder, 'application.log')
        
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))

        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            datefmt=log_datefmt,
                            handlers=[RotatingFileHandler(log_file_path, maxBytes=10485760, backupCount=5, encoding='utf-8'),
                                    logging.StreamHandler()])
    except Exception as e:
        logging.error(f"Fehler beim Setup des Loggings: {e}")
        raise

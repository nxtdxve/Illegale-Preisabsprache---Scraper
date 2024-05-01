import os
import logging
from logging.handlers import RotatingFileHandler
from app import config

def setup_logging(log_format=None, log_folder=None, log_datefmt=None):
    """
    Konfiguriert das Logging-System mit den Einstellungen aus der Konfigurationsdatei.
    """
    # Löscht alle bestehenden Handler
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    try:
        if log_format is None:
            log_format = config['Logging']['format']
        if log_folder is None:
            log_folder = config['Logging']['folder']
        if log_datefmt is None:
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

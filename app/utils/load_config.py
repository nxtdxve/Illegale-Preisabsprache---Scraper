import configparser
import os
import logging

def load_config(config_file='config.ini'):
    """
    Lädt die Konfigurationsdatei und gibt sie zurück.
    :param config_file: Der Name der Konfigurationsdatei
    :return: Die geladene Konfiguration
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../..', config_file)

    if not os.path.exists(config_path):
        logging.error(f"Konfigurationsdatei {config_file} nicht gefunden.")
        raise FileNotFoundError(f"Konfigurationsdatei {config_file} nicht gefunden.")

    config.read(config_path)
    return config

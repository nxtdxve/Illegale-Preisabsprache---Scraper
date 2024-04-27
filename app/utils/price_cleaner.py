import re
import logging

def clean_price(price_str):
    """
    Bereinigt einen gegebenen Preis-String und konvertiert ihn in ein Dezimalformat.
    
    :param price_str: Der zu bereinigende Preis-String.
    :return: Den bereinigten Preis als String im Dezimalformat, oder None bei einem Fehler.
    """
    try:
        match = re.search(r'\d+(\.\d+)?', price_str)
        if match:
            return f"{float(match.group(0)):.2f}"
        else:
            logging.warning(f"Keine Zahl im Preis-String {price_str} gefunden.")
            return None
    except Exception as e:
        logging.error(f"Fehler beim Bereinigen des Preis-Strings {price_str}: {e}")
        return None

import re

def clean_price(price_str):
    """
    Bereinigt einen gegebenen Preis-String und konvertiert ihn in ein Dezimalformat.
    
    :param price_str: Der zu bereinigende Preis-String.
    :return: Den bereinigten Preis als String im Dezimalformat.
    """
    match = re.search(r'\d+(\.\d+)?', price_str)
    return f"{float(match.group(0)):.2f}" if match else None

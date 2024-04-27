import logging
from urllib.parse import urlparse
from app import config

def get_domain_selector(url):
    """
    Bestimmt den korrekten Selektor für die gegebene URL basierend auf der Konfigurationsdatei.

    :param url: Die URL der Produktseite.
    :return: Den passenden Selektor als String oder None, falls kein Selektor gefunden wurde.
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    # Unterstützt Subdomains und entfernt das "www."
    domain_parts = domain.replace("www.", "").split('.')
    if len(domain_parts) > 2:
        domain_key = domain_parts[-2]  # Nimmt den Domainnamen vor der TLD
    else:
        domain_key = domain_parts[0]

    selector_key = f"{domain_key}_selector"
    selector = config['Scraper'].get(selector_key, None)

    if selector is None:
        logging.error(f"Kein Selector für {domain} in der Konfiguration gefunden.")
        return None
    return selector

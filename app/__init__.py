#Initialisierung der Konfiguration
from .utils.load_config import load_config
config = load_config()

# Initialisierung des Logging-Systems
from .utils.logging_config import setup_logging
setup_logging()
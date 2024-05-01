# Preisverlauf-Scraper

## Beschreibung

Dies ist der Scraper-Teil der IDPA-Projektarbeit, der darauf ausgelegt ist, die Preise verschiedener Produkte von Baumarkt-Websites zu erfassen und in einer MongoDB-Datenbank zu speichern. Der Scraper ist eine Komponente eines grösseren Systems, das auch ein Backend und ein Frontend umfasst, welche die Darstellung der Preisverläufe und Benachrichtigungen über Preisänderungen ermöglichen.

## Technologien

- Python 3.12
- MongoDB
- PyMongo
- BeautifulSoup
- Requests
- Pytest

## Features

- Automatisches Scrapen von Produktpreisen von verschiedenen Baumarkt-Websites.
- Speicherung der Preisdaten in einer MongoDB-Datenbank.
- Konfigurierbare Scraping-Frequenz, Logging-Details und Datenbankzugriff über eine `config.ini` Datei.
- Integration einer API zur Benachrichtigung über Preisänderungen.

## Installation

Klonen Sie das Repository und installieren Sie die erforderlichen Abhängigkeiten:

```bash
git clone https://github.com/nxtdxve/Illegale-Preisabsprache-Scraper.git
cd Illegale-Preisabsprache-Scraper
pip install -r requirements.txt
```

## Konfiguration

Die Anwendung benötigt eine `.env` Datei für Umgebungsvariablen und eine `config.ini` für spezifische Einstellungen.

Beispiel für eine `.env` Datei:

```env
MONGO_URI=mongodb://dein_user:dein_passwort@dein_host:dein_port/dein_db
API_KEY=dein_api_schlüssel
```

Inhalte der `config.ini` Datei:

```ini
[Scraper]
bauhaus_selector = wc-price[id='wc-product-detail-price']
hornbach_selector = div[data-testid='prices'] span

[Scheduler]
frequency = 10

[Logging]
format = %%(asctime)s - %%(levelname)s - %%(message)s
datefmt = %%Y-%%m-%%d %%H:%%M:%%S
folder = logs

[Database]
db_name = dein_db

[API]
URL = https://api.example.com
```

## Verwendung

Um den Scraper zu starten und die Preisdaten zu erfassen:

```bash
python main.py
```

## Testing

Zum Ausführen der Tests:

```bash
pytest
```

## Deployment

Das Projekt wurde auf Heroku gehostet und dafür angepasst.

## Verwandte Projekte

- Backend: [Illegale Preisabsprache Backend](https://github.com/nxtdxve/Illegale-Preisabsprache-Backend)
- Frontend: [Illegale Preisabsprache Frontend](https://github.com/nxtdxve/Illegale-Preisabsprache-Frontend)

## Autoren

- David Zettler
- Ava Reindl

import pytest
import logging
from app.utils.load_config import load_config
from app.utils.logging_config import setup_logging

@pytest.fixture
def temp_logging_env(tmp_path):
    temp_folder = tmp_path / "logs"
    temp_folder.mkdir()
    temp_config_file = tmp_path / "config.ini"
    config_content = """
[Logging]
format = %%(asctime)s - %%(levelname)s - %%(message)s
datefmt = %%Y-%%m-%%d %%H:%%M:%%S
folder = {temp_folder}
""".format(temp_folder=temp_folder)
    temp_config_file.write_text(config_content)
    return str(temp_config_file), temp_folder

def test_setup_logging(temp_logging_env):
    config_file, temp_folder = temp_logging_env

    # Aktualisiert die globale Konfiguration mit der temporären Konfigurationsdatei
    load_config(config_file)

    # Verwendet die temporäre Konfiguration für das Logging
    setup_logging(log_folder=str(temp_folder))

    test_message = "Testnachricht für Logging-Konfiguration"
    # Schreibt eine Test-Log-Nachricht
    logging.info(test_message)

    # Überprüft, ob Log-Dateien im temporären Ordner erstellt wurden
    log_files = list(temp_folder.glob("*.log"))
    assert log_files, "Es wurde erwartet, dass eine Log-Datei erstellt wird."

    # Überprüft, ob die Test-Log-Nachricht in der Log-Datei enthalten ist
    with open(log_files[0], 'r', encoding='utf-8') as log_file:
        log_content = log_file.read()
        assert test_message in log_content, "Die Test-Log-Nachricht sollte im Log-File enthalten sein."

    # Setzt das Logging-System zurück, um Seiteneffekte in anderen Tests zu vermeiden
    logging.getLogger().handlers.clear()

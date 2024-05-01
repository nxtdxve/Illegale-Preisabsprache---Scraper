import os
import pytest
from app.utils.load_config import load_config

def test_load_config_success(tmp_path):
    # Erstelle eine temporäre Konfigurationsdatei
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_config.ini"
    p.write_text("[Test]\nkey=value\n")

    config = load_config(config_file=str(p))
    assert config['Test']['key'] == 'value'

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config(config_file="nonexistent_config.ini")

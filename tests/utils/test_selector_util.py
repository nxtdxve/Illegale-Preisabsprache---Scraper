import pytest
from app.utils.selector_util import get_domain_selector
from app.utils.load_config import load_config

# Temporäre Konfigurationsdatei für Tests einrichten
@pytest.fixture
def setup_test_config(tmp_path):
    config_file = tmp_path / "config.ini"
    config_content = """
[Scraper]
bauhaus_selector = wc-price[id='wc-product-detail-price']
hornbach_selector = div[data-testid='prices'] span
"""
    config_file.write_text(config_content)
    return str(config_file)

# Testfälle für gültige URLs
@pytest.mark.parametrize("url,expected_selector", [
    ("https://www.bauhaus.ch/product/someitem", "wc-price[id='wc-product-detail-price']"),
    ("https://www.hornbach.ch/product/anotheritem", "div[data-testid='prices'] span"),
])
def test_get_domain_selector_valid(setup_test_config, url, expected_selector):
    config = load_config(setup_test_config)
    # Patch the global `config` variable inside `selector_util` module with the temporary config loaded
    import app.utils.selector_util
    app.utils.selector_util.config = config

    selector = get_domain_selector(url)
    assert selector == expected_selector, f"Erwarteter Selektor für URL {url} war {expected_selector}, erhalten wurde {selector}"

# Testfälle für ungültige URLs
@pytest.mark.parametrize("url", [
    ("https://www.unknownsite.com/product/item"),
    ("https://example.com/"),
    ("https://bauhaus.anotherunconfiguredsite.com/product")
])
def test_get_domain_selector_invalid(setup_test_config, url):
    config = load_config(setup_test_config)
    # Patch the global `config` variable inside `selector_util` module with the temporary config loaded
    import app.utils.selector_util
    app.utils.selector_util.config = config

    selector = get_domain_selector(url)
    assert selector is None, f"Für die URL {url} wurde ein Selector erwartet, der None ist, aber erhalten wurde {selector}"

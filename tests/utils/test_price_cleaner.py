import pytest
from app.utils.price_cleaner import clean_price

# Testfälle für gültige Preis-Strings
@pytest.mark.parametrize("price_str, expected", [
    ("$23.45", "23.45"),
    ("23.45€", "23.45"),
    ("1234", "1234.00"),
    ("68 CHF*", "68.00"),
])

def test_clean_price_valid(price_str, expected):
    assert clean_price(price_str) == expected

# Testfälle für ungültige Preis-Strings
@pytest.mark.parametrize("price_str", [
    ("abc"),
    (""),
    ("$"),
])

def test_clean_price_invalid(price_str):
    assert clean_price(price_str) is None

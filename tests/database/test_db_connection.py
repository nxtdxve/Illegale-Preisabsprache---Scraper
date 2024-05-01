import pytest
from app.database.db_connection import get_db_connection

@pytest.fixture(scope="module")
def db():
    db_connection = get_db_connection()
    yield db_connection

def test_db_connection(db):
    assert db is not None
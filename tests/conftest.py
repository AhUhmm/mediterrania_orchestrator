import pytest
import json

@pytest.fixture
def ricette_test():
    with open("ricette.json", "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def db_mock():
    return Mock()
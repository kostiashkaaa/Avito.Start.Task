import pytest
import random
import string

@pytest.fixture
def base_url():
    return "https://qa-internship.avito.com/api/1"

@pytest.fixture
def new_item():
    return {
        "sellerID": random.randint(111111, 999999),
        "name": "Phone " + "".join(random.choices(string.ascii_lowercase, k=5)),
        "price": random.randint(1000, 50000),
        "statistics": {
            "likes": random.randint(1, 10),
            "viewCount": random.randint(11, 100),
            "contacts": random.randint(1, 5)
        }
    }
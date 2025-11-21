import requests
import pytest
import uuid


def get_item_id(response):
    resp_json = response.json()
    if "status" in resp_json:
        return resp_json["status"].split(" - ")[-1]
    return resp_json.get("id")


def test_create_item(base_url, new_item):
    url = f"{base_url}/item"
    r = requests.post(url, json=new_item)

    assert r.status_code == 200
    assert "status" in r.json()
    assert "Сохранили объявление" in r.json()["status"]


def test_get_item(base_url, new_item):
    post_r = requests.post(f"{base_url}/item", json=new_item)
    item_id = get_item_id(post_r)

    r = requests.get(f"{base_url}/item/{item_id}")
    assert r.status_code == 200

    data = r.json()
    if isinstance(data, list):
        data = data[0]

    assert data["id"] == item_id
    assert data["name"] == new_item["name"]
    assert data["price"] == new_item["price"]
    assert data["sellerId"] == new_item["sellerID"]


def test_get_item_by_seller(base_url, new_item):
    requests.post(f"{base_url}/item", json=new_item)
    seller_id = new_item["sellerID"]

    r = requests.get(f"{base_url}/{seller_id}/item")
    assert r.status_code == 200

    data = r.json()
    assert isinstance(data, list)

    ids = [i["id"] for i in data]
    assert len(ids) > 0


def test_get_statistic(base_url, new_item):
    post_r = requests.post(f"{base_url}/item", json=new_item)
    item_id = get_item_id(post_r)

    r = requests.get(f"{base_url}/statistic/{item_id}")
    assert r.status_code == 200

    stats = r.json()
    if isinstance(stats, list):
        stats = stats[0]

    assert stats["likes"] == new_item["statistics"]["likes"]
    assert stats["viewCount"] == new_item["statistics"]["viewCount"]
    assert stats["contacts"] == new_item["statistics"]["contacts"]


def test_create_item_no_price(base_url, new_item):
    del new_item["price"]
    r = requests.post(f"{base_url}/item", json=new_item)
    assert r.status_code == 400


def test_get_not_found(base_url):
    random_id = str(uuid.uuid4())
    r = requests.get(f"{base_url}/item/{random_id}")
    assert r.status_code == 404
import pytest
from unittest.mock import Mock, patch

from app import app, inventory


@pytest.fixture
def client():
    original_inventory = [item.copy() for item in inventory]

    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    inventory.clear()
    inventory.extend(original_inventory)


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Welcome to the Inventory Management API"
    )


def test_get_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_one_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/9999")

    assert response.status_code == 404


def test_add_item(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "price": 200,
            "quantity": 15,
            "barcode": "",
            "brand": "Local Store"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Rice"
    assert data["price"] == 200
    assert data["quantity"] == 15


def test_add_item_missing_name(client):
    response = client.post(
        "/inventory",
        json={
            "price": 200,
            "quantity": 10
        }
    )

    assert response.status_code == 400


def test_add_item_negative_price(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "price": -10,
            "quantity": 5
        }
    )

    assert response.status_code == 400


def test_add_item_negative_quantity(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "price": 100,
            "quantity": -5
        }
    )

    assert response.status_code == 400


def test_add_item_invalid_price(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "price": "cheap",
            "quantity": 5
        }
    )

    assert response.status_code == 400


def test_add_item_invalid_quantity(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Sugar",
            "price": 100,
            "quantity": "five"
        }
    )

    assert response.status_code == 400


def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 400,
            "quantity": 5
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["price"] == 400
    assert data["quantity"] == 5


def test_update_item_name(client):
    response = client.patch(
        "/inventory/1",
        json={
            "name": "Updated Milk"
        }
    )

    assert response.status_code == 200
    assert response.get_json()["name"] == "Updated Milk"


def test_update_missing_item(client):
    response = client.patch(
        "/inventory/9999",
        json={
            "price": 100
        }
    )

    assert response.status_code == 404


def test_update_invalid_field(client):
    response = client.patch(
        "/inventory/1",
        json={
            "color": "red"
        }
    )

    assert response.status_code == 400


def test_update_negative_price(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": -50
        }
    )

    assert response.status_code == 400


def test_update_negative_quantity(client):
    response = client.patch(
        "/inventory/1",
        json={
            "quantity": -5
        }
    )

    assert response.status_code == 400


def test_delete_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 204

    response = client.get("/inventory/1")

    assert response.status_code == 404


def test_delete_missing_item(client):
    response = client.delete("/inventory/9999")

    assert response.status_code == 404


@patch("app.requests.get")
def test_find_product_by_barcode(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Test Milk",
            "brands": "Test Brand",
            "ingredients_text": "Water, milk",
            "quantity": "1 litre"
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.get(
        "/external/barcode/123456"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Test Milk"
    assert data["brand"] == "Test Brand"


@patch("app.requests.get")
def test_barcode_product_not_found(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.get(
        "/external/barcode/000000"
    )

    assert response.status_code == 404


@patch("app.requests.get")
def test_search_product_by_name(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Test Bread",
                "brands": "Test Bakery",
                "code": "12345",
                "ingredients_text": "Wheat, water"
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.get(
        "/external/search?name=bread"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data[0]["name"] == "Test Bread"
    assert data[0]["brand"] == "Test Bakery"


def test_search_without_name(client):
    response = client.get("/external/search")

    assert response.status_code == 400


@patch("app.requests.get")
def test_import_product(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Imported Juice",
            "brands": "Fresh Brand"
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.post(
        "/external/import/987654321"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["item"]["name"] == "Imported Juice"
    assert data["item"]["barcode"] == "987654321"


@patch("app.requests.get")
def test_import_product_not_found(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 0
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.post(
        "/external/import/000000000"
    )

    assert response.status_code == 404


@patch("app.requests.get")
def test_import_product_missing_name(mock_get, client):
    mock_response = Mock()

    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "",
            "brands": "Test Brand"
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    response = client.post(
        "/external/import/111111111"
    )

    assert response.status_code == 422


@patch("app.requests.get")
def test_external_api_failure(mock_get, client):
    mock_get.side_effect = Exception("API error")

    response = client.get(
        "/external/barcode/123456"
    )

    assert response.status_code == 500


def test_cli_has_main():
    import cli

    assert callable(cli.main)
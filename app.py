from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "price": 350.0,
        "quantity": 10,
        "barcode": "3017620422003",
        "brand": "Silk"
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "price": 120.0,
        "quantity": 20,
        "barcode": "",
        "brand": "Local Bakery"
    }
]

OPENFOODFACTS_HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0"
}


def find_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def next_id():
    return max(
        [item["id"] for item in inventory],
        default=0
    ) + 1


def fetch_product(url, params=None):
    response = requests.get(
        url,
        params=params,
        headers=OPENFOODFACTS_HEADERS,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def validate_item_data(data, partial=False):
    if not isinstance(data, dict):
        return "Valid JSON object is required"

    if not partial and "name" not in data:
        return "Name is required"

    if not partial and "price" not in data:
        return "Price is required"

    if not partial and "quantity" not in data:
        return "Quantity is required"

    allowed_fields = {
        "name",
        "price",
        "quantity",
        "barcode",
        "brand"
    }

    for field in data:
        if field not in allowed_fields:
            return f"Invalid field: {field}"

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "Invalid name"

    if "price" in data:
        if (
            isinstance(data["price"], bool)
            or not isinstance(data["price"], (int, float))
            or data["price"] < 0
        ):
            return "Invalid price"

    if "quantity" in data:
        if (
            isinstance(data["quantity"], bool)
            or not isinstance(data["quantity"], int)
            or data["quantity"] < 0
        ):
            return "Invalid quantity"

    for field in ["barcode", "brand"]:
        if field in data and not isinstance(data[field], str):
            return f"Invalid {field}"

    return None


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Inventory Management API"
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item)


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True)

    error = validate_item_data(data)

    if error:
        return jsonify({"error": error}), 400

    item = {
        "id": next_id(),
        "name": data["name"].strip(),
        "price": data["price"],
        "quantity": data["quantity"],
        "barcode": data.get("barcode", "").strip(),
        "brand": data.get("brand", "").strip()
    }

    inventory.append(item)

    return jsonify(item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Valid update data is required"
        }), 400

    error = validate_item_data(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    for field, value in data.items():
        if isinstance(value, str):
            item[field] = value.strip()
        else:
            item[field] = value

    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)

    return "", 204


@app.route("/external/barcode/<barcode>", methods=["GET"])
def find_by_barcode(barcode):
    url = (
        "https://world.openfoodfacts.org/"
        f"api/v2/product/{barcode}.json"
    )

    try:
        result = fetch_product(url)
    except (requests.RequestException, ValueError):
        return jsonify({
            "error": "Could not fetch product from OpenFoodFacts"
        }), 502

    if result.get("status") != 1:
        return jsonify({
            "error": "Product not found"
        }), 404

    product = result.get("product", {})

    return jsonify({
        "barcode": barcode,
        "name": product.get("product_name", ""),
        "brand": product.get("brands", ""),
        "ingredients": product.get("ingredients_text", ""),
        "quantity": product.get("quantity", "")
    })


@app.route("/external/search", methods=["GET"])
def search_product():
    name = request.args.get("name", "").strip()

    if not name:
        return jsonify({
            "error": "Product name is required"
        }), 400

    try:
        result = fetch_product(
            "https://world.openfoodfacts.org/cgi/search.pl",
            params={
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 5
            }
        )
    except (requests.RequestException, ValueError):
        return jsonify({
            "error": "Could not search OpenFoodFacts"
        }), 502

    products = []

    for product in result.get("products", []):
        products.append({
            "name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "barcode": product.get("code", ""),
            "ingredients": product.get("ingredients_text", "")
        })

    return jsonify(products)


@app.route("/external/import/<barcode>", methods=["POST"])
def import_product(barcode):
    url = (
        "https://world.openfoodfacts.org/"
        f"api/v2/product/{barcode}.json"
    )

    try:
        result = fetch_product(url)
    except (requests.RequestException, ValueError):
        return jsonify({
            "error": "Could not fetch product from OpenFoodFacts"
        }), 502

    if result.get("status") != 1:
        return jsonify({
            "error": "Product not found"
        }), 404

    product = result.get("product", {})

    name = product.get("product_name", "").strip()

    if not name:
        return jsonify({
            "error": "Product name is missing"
        }), 422

    for item in inventory:
        if item["barcode"] == barcode:
            return jsonify({
                "message": "Product already exists",
                "item": item
            }), 200

    item = {
        "id": next_id(),
        "name": name,
        "price": 0,
        "quantity": 0,
        "barcode": barcode,
        "brand": product.get("brands", "").strip()
    }

    inventory.append(item)

    return jsonify({
        "message": "Product imported successfully",
        "item": item
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
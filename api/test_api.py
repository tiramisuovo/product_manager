import pytest
from fastapi.testclient import TestClient
import sqlite3

from api.api import app
from crud.crud import *
from database.schema import create_table, create_index
from database.connection import get_db
from models import QuoteDetail

# ========== API TEST SUITE MEGA BLOCK ==========

@pytest.fixture
def test_client():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    reset_database(conn, cursor)
    
    def override_get_db():
        print("Using overridden DB")
        yield conn, cursor
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    print(app.routes)

    conn.close()

@pytest.fixture
def test_client_and_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    reset_database(conn, cursor)
    
    def override_get_db():
        print("Using overridden DB")
        yield conn, cursor
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client, conn, cursor

    conn.close()

def reset_database(conn, cursor):
    with conn:
        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("DROP TABLE IF EXISTS product_images")
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS product_customers")
        cursor.execute("DROP TABLE IF EXISTS tags")
        cursor.execute("DROP TABLE IF EXISTS product_tags")
        cursor.execute("DROP TABLE IF EXISTS quotes")

        cursor.execute("DROP TABLE IF EXISTS product_manager")
        cursor.execute("PRAGMA foreign_keys = ON")
        create_table(conn, cursor)

def sample_product_payload():
    return {
        "ref_num": "TST123",
        "name": "Test Product",
        "barcode": 1234567890,
        "pcs_innerbox": 10,
        "pcs_ctn": 100,
        "weight": 1.5,
        "price_usd": 9.99,
        "price_rmb": 68.5,
        "remarks": "Testing add endpoint",
        "packing": "Boxed",
        "customers": ["CustomerA"],
        "quote": {
            "CustomerA": {
                "quote": 12,
                "remark": "bulk"
            }
        },
        "imgs": ["img1.jpg"],
        "tags": ["summer"]
    }

def invalid_product_payload():
    return {
        "ref_num": None,
        "name": 1234567,
        "barcode": "def not a number",
        "pcs_innerbox": "whyyoureading",
        "pcs_ctn": "senpai help me",
        "weight": "dont ask the weight of a girl",
        "price_usd": "legit cant afford",
        "price_rmb": "ten-ish",
        "remarks": 7654321,
        "packing": 0.001,
        "customers": [None],
        "quote": {
            "CustomerA": {
                "quote": "please just pass",
                "remark": None
            }
        },
        "imgs": ["total valid image path"],
        "tags": []
    }


# ========== CREATE ==========

def test_create_product_api(test_client):
    payload = sample_product_payload()
    response = test_client.post("/products/", json = payload)

    assert response.status_code == 201
    data = response.json()
    assert data["ref_num"] == "TST123"
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    # duplicate
    response2 = test_client.post("/products/", json=sample_product_payload())
    assert response2.status_code in (400, 409)

    # invalid fields
    invalid_payload = invalid_product_payload()
    invalid_response = test_client.post("/products/", json = invalid_payload)
    assert invalid_response.status_code == 422

    errors = invalid_response.json()["detail"]
    fields = {e["loc"][1] for e in errors if e["loc"][0] == "body"}
    assert "ref_num" in fields
    assert "barcode" in fields
    assert "pcs_innerbox" in fields
    assert "pcs_ctn" in fields
    assert "weight" in fields
    assert "price_usd" in fields
    assert "remarks" in fields
    assert "packing" in fields
    assert "customers" in fields
    assert "quote" in fields

def test_create_images_api(test_client):
    payload = sample_product_payload()
    add_result = test_client.post("/products/", json = payload)
    product_id = add_result.json()["id"]
    response = test_client.post(f"/products/{product_id}/images", json = {"imgs": ["New image.jpg"]})

    assert response.status_code == 201
    data = response.json()
    assert "New image.jpg" in data["imgs"][1]["img"]
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_create_customers_api(test_client):
    payload = sample_product_payload()
    add_result = test_client.post("/products/", json = payload)
    product_id = add_result.json()["id"]
    response = test_client.post(f"/products/{product_id}/customers", json = {"customers": ["New customer"]})

    assert response.status_code == 201
    data = response.json()
    assert "New customer" in data["customers"][1]["customer_name"]
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_create_tags_api(test_client):
    payload = sample_product_payload()
    add_result = test_client.post("/products/", json = payload)
    product_id = add_result.json()["id"]
    response = test_client.post(f"/products/{product_id}/tags", json = {"tags": ["New tag"]})

    assert response.status_code == 201
    data = response.json()
    assert "New tag" in data["tags"][1]["tag_name"]
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_create_quotes_api(test_client):
    payload = sample_product_payload()
    add_result = test_client.post("/products/", json = payload)
    product_id = add_result.json()["id"]
    response = test_client.post(f"/products/{product_id}/quotes",
                                json = {"quotes": {"CustomerA": {
                                    "quote": 13,
                                    "remark": "yes"}}})

    assert response.status_code == 201
    data = response.json()
    assert "CustomerA" in data["quote"][1]["customer_name"]
    assert data["quote"][1]["quote"] == 13
    assert data["quote"][1]["quote_remark"] == "yes"
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


# ========== DELETE ==========

def test_delete_product_api(test_client):
    payload = sample_product_payload()
    add_response = test_client.post("/products/", json = payload)
    product_id = add_response.json()["id"]

    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    invalid_id = 12345
    invalid_response = test_client.delete(f"/products/{invalid_id}")
    assert invalid_response.status_code == 404
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_delete_image_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    add_response = client.post("/products/", json = payload)
    product_id = add_response.json()["id"]
    image_path = add_response.json()["imgs"][0]["img"]
    with conn:
        image_id = cursor.execute("SELECT id FROM product_images WHERE img = ?", (image_path,)).fetchone()[0]

    response = client.delete(f"/products/{product_id}/images/{image_id}")
    assert response.status_code == 204

    invalid_id = 12345
    invalid_response = client.delete(f"/images/{invalid_id}")
    assert invalid_response.status_code == 404
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_delete_customer_from_product_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    add_response = client.post("/products/", json = payload)
    product_id = add_response.json()["id"]
    customer_name = add_response.json()["customers"][0]["customer_name"]
    with conn:
        customer_id = cursor.execute("""SELECT id FROM customers WHERE customer_name =?""",
                                     (customer_name,)).fetchone()[0]
                                
    response = client.delete(f"/products/{product_id}/customers/{customer_id}")
    assert response.status_code == 204

    invalid_id = 12345
    invalid_response = client.delete(f"/products/{product_id}/customers/{invalid_id}")
    assert invalid_response.status_code == 404
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_delete_tag_from_product_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    add_response = client.post("/products/", json = payload)
    product_id = add_response.json()["id"]
    tag_name = add_response.json()["tags"][0]["tag_name"]
    with conn:
        tag_id = cursor.execute("""SELECT id FROM tags WHERE tag_name =?""",
                                     (tag_name,)).fetchone()[0]
                                
    response = client.delete(f"/products/{product_id}/tags/{tag_id}")
    assert response.status_code == 204
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    invalid_id = 12345
    invalid_response = client.delete(f"/products/{product_id}/tags/{invalid_id}")
    assert invalid_response.status_code == 404
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_delete_quote_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    add_response = client.post("/products/", json = payload)
    product_id = add_response.json()["id"]
    quote_id = add_response.json()["quote"][0]["quote_id"]
                                
    response = client.delete(f"/products/{product_id}/quotes/{quote_id}")
    assert response.status_code == 204

    invalid_id = 12345
    invalid_response = client.delete(f"/products/{product_id}/quotes/{invalid_id}")
    assert invalid_response.status_code == 404
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


# ========== EDIT ==========

def test_edit_product_api(test_client):
    payload = sample_product_payload()
    add_response = test_client.post("/products/", json = payload)
    product_id = add_response.json()["id"]

    response = test_client.put(f"/products/{product_id}", json = {
    "name": "Updated Product Name",
    "price_usd": 12.99,
    "remarks": "Updated remark"
})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product Name"
    assert data["price_usd"] == 12.99
    assert data["remarks"] == "Updated remark"


    invalid_payload = invalid_product_payload()
    invalid_response = test_client.put(f"/products/{product_id}", json = invalid_payload)
    assert invalid_response.status_code == 422

    errors = invalid_response.json()["detail"]
    fields = {e["loc"][1] for e in errors if e["loc"][0] == "body"}
    print("Errors:", errors)
    print("Fields:", fields)
    assert "barcode" in fields
    assert "pcs_innerbox" in fields
    assert "pcs_ctn" in fields
    assert "weight" in fields
    assert "price_usd" in fields
    assert "remarks" in fields
    assert "packing" in fields
    print("STATUS:", response.status_code)
    print("BODY:", response.text)


def test_edit_tag_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    client.post("/products/", json = payload)
    tag_name = payload["tags"][0]

    tag_id = cursor.execute("SELECT id FROM tags WHERE tag_name = ?", (tag_name,)).fetchone()[0]

    response = client.patch(f"/tags/{tag_id}", json = {"new_name": "xx"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tag_id
    assert data["tag_name"] == "xx"

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_edit_customer_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    client.post("/products/", json = payload)
    customer_name = payload["customers"][0]

    customer_id = cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (customer_name,)).fetchone()[0]

    response = client.patch(f"/customers/{customer_id}", json = {"new_name": "xx"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == customer_id
    assert data["customer_name"] == "xx"

    print("STATUS:", response.status_code)
    print("BODY:", response.text)


def test_edit_quote_api(test_client_and_db):
    client, conn, cursor = test_client_and_db
    payload = sample_product_payload()
    add_response = client.post("/products/", json = payload)
    product_data = add_response.json()
    quote_id = product_data["quote"][0]["quote_id"]
  
    updated_payload = {"quote": 10, "quote_remark": "updated remark" }

    response = client.patch(f"/quotes/{quote_id}", json = updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["quote"] == 10
    assert data["quote_remark"] == "updated remark"

    # Partial data test
    partial_payload = {"quote": 999.99}
    partial_response = client.patch(f"/quotes/{quote_id}", json=partial_payload)
    assert partial_response.status_code == 200

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

# ========== SEARCH ==========

def test_get_product_api(test_client):
    payload = sample_product_payload()
    add_result = test_client.post("/products/", json = payload)
    product_id = add_result.json()["id"]
    response = test_client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["ref_num"] == "TST123"
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

def test_search_product_name_api(test_client):
    payload = sample_product_payload()
    test_client.post("/products/", json = payload)
    response = test_client.get(f"/products/search", params={"name": "Test Product"})
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == "Test Product"

def test_list_tag_api(test_client):
    payload = sample_product_payload()
    test_client.post("/products/", json = payload)
    response = test_client.get("/tags")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 200
    data = response.json()[0]["tag_name"]
    assert "summer" in data

def test_list_customer_api(test_client):
    payload = sample_product_payload()
    test_client.post("/products/", json = payload)
    response = test_client.get("/customers")
    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code == 200
    data = response.json()[0]["customer_name"]
    assert "CustomerA" in data

# ========== MISC ==========

def test_update_lock_status_api(test_client):
    payload = sample_product_payload()
    add_response = test_client.post("/products/", json = payload)
    product_id = add_response.json()["id"]

    response = test_client.patch(f"/products/{product_id}/lock?user=testuser", json={"locked": True})
    assert response.status_code == 200
    data = response.json()
    assert data["locked_by"] == "testuser"
    assert data["locked_timestamp"] is not None

    response = test_client.patch(f"/products/{product_id}/lock?user=testuser", json={"locked": False})
    assert response.status_code == 200
    data = response.json()
    assert data["locked_by"] is None
    assert data["locked_timestamp"] is None
import sqlite3
import pytest
from crud.product_crud import *
from crud.image_crud import *
from crud.customer_crud import *
from crud.tag_crud import *
from crud.quote_crud import *
from crud.misc_crud import *

from database.schema import create_table, create_index
from models import *

# ========== CRUD TEST SUITE MEGA BLOCK ==========

@pytest.fixture
def test_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    reset_database(conn, cursor)

    create_test_product(conn, cursor)

    yield conn, cursor
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
        cursor.execute("PRAGMA table_info(product_manager)")
        for row in cursor.fetchall():
            print(row)

def create_test_product(conn, cursor):
    product = ProductCreate(
        ref_num = "TEST001",
        name = "test pen",
        barcode = 111111,
        pcs_innerbox = 10,
        pcs_ctn = 100,
        weight = 0.2,
        price_usd = 1.0,
        price_rmb = 7.5,
        remarks = "test remarks",
        packing = "box",
        customers = ["Test Customer"],
        quote ={"Test Customer": {"quote": 1.1, "remark": "test"}},
        imgs = ["img1.jpg"],
        tags = ["test tag"])
    add_product(conn, cursor, product)


# Add function tests

def test_add_product(test_db):
    conn, cursor = test_db

    result = list_products(cursor)
    assert len(result) == 1
    assert result[0][1] == "TEST001"
    assert result[0][2] == "test pen"
    assert result[0][3] == 111111
    assert result[0][4] == 10
    assert result[0][5] == 100
    assert result[0][6] == 0.2
    assert result[0][7] == 1.0
    assert result[0][8] == 7.5
    assert result[0][9] == "test remarks"
    assert result[0][10] == "box"

def test_add_image(test_db):
    conn, cursor = test_db
    result_img = list_images(cursor)
    assert len(result_img) == 1
    assert result_img[0][2] == "img1.jpg"


def test_add_customer(test_db):
    conn, cursor = test_db
    result_customer = list_customer(cursor)
    assert len(result_customer) == 1
    assert result_customer[0][1] == "Test Customer"

def test_add_product_customer(test_db):
    conn, cursor = test_db
    result_product_customer = list_product_customer(cursor, 1)
    assert len(result_product_customer) == 1
    assert result_product_customer[0] == "Test Customer"

def test_add_tag(test_db):
    conn, cursor = test_db
    result_tag = list_tag(cursor)
    assert len(result_tag) == 1
    assert result_tag[0][1] == "test tag"

def test_add_product_tag(test_db):
    conn, cursor = test_db
    result_product_tag = list_product_tag(cursor, 1)
    assert len(result_product_tag) == 1
    assert result_product_tag[0] == "test tag"

def test_add_quote(test_db):
    conn, cursor = test_db
    result_quote = list_quote(cursor)
    assert len(result_quote) == 1
    assert result_quote[0]["quote"] == 1.1
    assert result_quote[0]["quote_remark"] == "test"
    assert result_quote[0]["customer_name"] == "Test Customer"

# Delete function tests

def test_delete_product(test_db):
    conn, cursor = test_db
    delete_product(conn, cursor, 1)
    result = list_products(cursor)
    assert len(result) == 0

def test_delete_image(test_db):
    conn, cursor = test_db
    delete_image(conn, cursor, 1, "img1.jpg")
    result = list_images(cursor)
    assert len(result) == 0

def test_delete_quote(test_db):
    conn, cursor = test_db
    delete_quote(conn, cursor, 1, "Test Customer", round (1.1, 2), "test")
    result = list_quote(cursor)
    assert len(result) == 0

def test_delete_tag_from_product(test_db):
    conn, cursor = test_db
    delete_tag_from_product(conn, cursor, 1, "test tag")
    result = list_product_tag(cursor, 1)
    assert len(result) == 0

def test_delete_customer_from_product(test_db):
    conn, cursor = test_db
    delete_customer_from_product(conn, cursor, 1, "Test Customer")
    result = list_product_customer(cursor, 1)
    assert len(result) == 0


# Search function tests

def test_search_product_name(test_db):
    conn, cursor = test_db
    results = search_product_name(conn, cursor, "test pen")

    assert isinstance(results, list)
    assert len(results) == 1
    product = results[0]

    assert product[1] == "TEST001"
    assert product[2] == "test pen"

def test_search_by_tag(test_db):
    conn, cursor = test_db
    results = search_by_tag(conn, cursor, "test tag")

    assert isinstance(results, list)
    assert len(results) == 1
    product = results[0]

    assert product[1] == "TEST001"
    assert product[2] == "test pen"

def test_search_by_customer(test_db):
    conn, cursor = test_db
    results = search_by_customer(conn, cursor, "Test Customer")

    assert isinstance(results, list)
    assert len(results) == 1
    product = results[0]

    assert product[1] == "TEST001"
    assert product[2] == "test pen"

def test_search_by_barcode(test_db):
    conn, cursor = test_db
    results = search_by_barcode(conn, cursor, 111111)

    assert isinstance(results, list)
    assert len(results) == 1
    product = results[0]

    assert product[1] == "TEST001"
    assert product[2] == "test pen"

def test_search_by_ref_num(test_db):
    conn, cursor = test_db
    results = search_by_ref_num(conn, cursor, "TEST001")

    assert isinstance(results, list)
    assert len(results) == 1
    product = results[0]

    assert product[1] == "TEST001"
    assert product[2] == "test pen"

# Edit function tests

def test_edit_product(test_db):
    conn, cursor = test_db
    edit_product(conn, cursor, 1, name="new name", price_rmb=3)
    result = list_products(cursor)

    assert len(result) == 1
    product = result[0]

    assert product[1] == "TEST001"
    assert product[2] == "new name"
    assert product[8] == 3

def test_edit_quote(test_db):
    conn, cursor = test_db
    edit_quote(conn, cursor, 1, "Test Customer", 2, "new remark")
    result = list_quote(cursor)

    assert len(result) == 1
    quote = result[0]

    assert quote["quote"] == 2
    assert quote["quote_remark"] == "new remark"

def test_edit_tag(test_db):
    conn, cursor = test_db
    edit_tag(conn, cursor, 1, "new tag")
    result = list_tag(cursor)

    assert len(result) == 1
    tag = result[0]

    assert tag[1] == "new tag"

def test_edit_customer(test_db):
    conn, cursor = test_db
    edit_customer(conn, cursor, 1, "new customer")
    result = list_customer(cursor)

    assert len(result) == 1
    tag = result[0]

    assert tag[1] == "new customer"
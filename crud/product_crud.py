from models import *
import logging
from fastapi import HTTPException
from crud.image_crud import add_image
from crud.customer_crud import add_customer, search_by_customer
from crud.tag_crud import add_tag, search_by_tag
from crud.quote_crud import add_quote
from crud.misc_crud import search_by_barcode, search_by_ref_num
from crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty


logging.basicConfig(level=logging.INFO)

def add_product(conn, cursor, product: ProductCreate):
    # Insert new product and link images, tags, customers, and quotes
    # Assumes product.ref_num is unique
    cursor.execute(
    """INSERT INTO product_manager(ref_num, name, barcode, pcs_innerbox, pcs_ctn, weight, 
    price_usd, price_rmb, remarks, packing, deleted, locked_by, locked_timestamp) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL, NULL)""",
    (product.ref_num,
    product.name,
    product.barcode,
    product.pcs_innerbox,
    product.pcs_ctn,
    product.weight, 
    product.price_usd,
    product.price_rmb,
    product.remarks,
    product.packing)
    )

    product_id = cursor.lastrowid
    add_image(conn, cursor, product_id, product.imgs)
    add_customer(conn, cursor, product_id, product.customers)
    add_tag(conn, cursor, product_id, product.tags)
    add_quote(conn, cursor, product_id, product.quote)

    logging.info("Added products: %s", product.ref_num)

    return {
    "id": product_id,
    "ref_num": product.ref_num,
    "name": product.name,
    "barcode": product.barcode,
    "pcs_innerbox": product.pcs_innerbox,
    "pcs_ctn": product.pcs_ctn,
    "weight": product.weight,
    "price_usd": product.price_usd,
    "price_rmb": product.price_rmb,
    "remarks": product.remarks,
    "packing": product.packing,
    "customers": product.customers,
    "quote": product.quote,
    "imgs": product.imgs,
    "tags": product.tags,
    }

def delete_product(conn, cursor, product_id):
    # Soft delete product by setting deleted = 1
    cursor.execute("UPDATE product_manager SET deleted = 1 WHERE id = ?", (product_id,))
    raise_value_error_if_not_found(cursor, msg = "Product not found")

def search_products(conn, cursor, name=None, tag=None, customer=None, barcode=None, ref_num=None):
    if name:
        return search_product_name(conn, cursor, name)
    if tag:
        return search_by_tag(conn, cursor, tag)
    if customer:
        return search_by_customer(conn, cursor, customer)
    if barcode:
        return search_by_barcode(conn, cursor, barcode)
    if ref_num:
        return search_by_ref_num(conn, cursor, ref_num)
    return []

def search_product_name(conn, cursor, name):
    # search by product name
    result = cursor.execute("SELECT * FROM product_manager WHERE name LIKE ?",
                        (f"%{name}%",)).fetchall()
    raise_value_error_if_empty(result, msg = "Resource not found")
    return result

def edit_product(conn, cursor, product_id, **kwargs):
    # Edit fields given product_id, e.g. edit_product (1, name="new name", price_rmb=3);
    # ref_num cannot be edited; auto-updates last_updated timestamp
    if "ref_num" in kwargs:
        raise ValueError("ref_num cannot be edited")
    
    fields = []
    values = []

    for key, value in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(value)

    fields.append("last_updated = CURRENT_TIMESTAMP")
    values.append(product_id)
    sql = f"UPDATE product_manager SET {','.join(fields)} WHERE id = ?"
    result = cursor.execute(sql, tuple(values))
    raise_value_error_if_empty(result, msg = "Product not found")

def list_products(cursor):
    # List all active (non-deleted) products
    cursor.execute("SELECT * FROM product_manager WHERE deleted = 0")
    return cursor.fetchall()


def format_product(conn, cursor, product_id):
    # Return full product info, including images, tags, customers, and quotes; formatted as dict
    cursor.execute("SELECT * FROM product_manager WHERE id = ?", (product_id,))
    raw_row = cursor.fetchone()
    raise_value_error_if_empty(raw_row, msg = "Product not found")
    
    column_names = [desc[0] for desc in cursor.description]
    product = dict(zip(column_names, raw_row))  # includes locked_by, locked_timestamp

    # Images
    cursor.execute("SELECT id, img FROM product_images WHERE product_id = ?", (product_id,))
    product["imgs"] = [{"id": img_id, "img": img} for img_id, img in cursor.fetchall()]

    # Tags
    cursor.execute("""SELECT t.id, t.tag_name
                      FROM product_tags pt
                      JOIN tags t ON pt.tag_id = t.id
                      WHERE pt.product_id = ?""", (product_id,))
    product["tags"] = [{"id": tag_id, "tag_name": tag_name} for tag_id, tag_name in cursor.fetchall()]

    # Customers
    cursor.execute("""SELECT c.id, c.customer_name
                      FROM product_customers pc
                      JOIN customers c ON pc.customer_id = c.id
                      WHERE pc.product_id = ?""", (product_id,))
    product["customers"] = [{"id": customer_id, "customer_name": name} for customer_id, name in cursor.fetchall()]

    # Quotes
    cursor.execute("""SELECT q.id, c.id, c.customer_name, q.quote, q.quote_remark
                      FROM quotes q
                      JOIN customers c ON q.customer_id = c.id
                      WHERE q.product_id = ?""", (product_id,))
    product["quote"] = [
        {
            "quote_id": quote_id,
            "customer_id": customer_id,
            "customer_name": customer_name,
            "quote": quote,
            "quote_remark": remark
        }
        for quote_id, customer_id, customer_name, quote, remark in cursor.fetchall()
    ]

    return product

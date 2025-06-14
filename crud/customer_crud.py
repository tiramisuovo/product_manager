from models import *
import logging
from fastapi import HTTPException
from crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty

logging.basicConfig(level=logging.INFO)

def add_customer(conn, cursor, product_id, customers):
    # Link customers to product
    # Create customer entries if they don't exist
    for c in customers:
        cursor.execute("INSERT OR IGNORE INTO customers(customer_name) VALUES(?)",
                            (c,))
        cursor.execute("SELECT id FROM customers WHERE customer_name =?", (c,))
        customer_id = cursor.fetchone()[0]
        cursor.execute("""INSERT OR IGNORE INTO product_customers (product_id, customer_id)
                            VALUES (?, ?)""", (product_id, customer_id))

def delete_customer_from_product(conn, cursor, product_id, customer_id):
    # Unlink customer from product (customer stays in table)
    cursor.execute("DELETE FROM product_customers WHERE product_id = ? AND customer_id = ?",
                    (product_id, customer_id))
    raise_value_error_if_not_found(cursor, msg = "Customer was not linked to this product")

def search_by_customer(conn, cursor, customer_name):
    cursor.execute("SELECT id FROM customers WHERE customer_name LIKE ?", (f"%{customer_name}%",))
    customer = cursor.fetchone()
    raise_value_error_if_empty(customer,"Customer not found")
    
    customer_id = customer[0]

    cursor.execute("SELECT product_id FROM product_customers WHERE customer_id = ?", (customer_id,))
    product_ids = [row[0] for row in cursor.fetchall()]

    if not product_ids:
        return []
    placeholders = ",".join("?" for _ in product_ids)
    query = f"SELECT * FROM product_manager WHERE id IN ({placeholders})"
    cursor.execute(query, tuple(product_ids))
    return cursor.fetchall()

def edit_customer(conn, cursor, customer_id, new_name):
    # Rename customer by ID
    cursor.execute("UPDATE customers SET customer_name = ? WHERE id = ?",
                    (new_name, customer_id))
    raise_value_error_if_not_found(cursor, msg = "Customer not found")
    return cursor.execute("SELECT id, customer_name FROM customers WHERE id = ?", (customer_id,)).fetchone()

def list_customer(cursor):
    result = cursor.execute("SELECT * FROM customers").fetchall()
    return result

def list_product_customer(cursor, product_id):
    # List all customers asscoiated with product_id
    cursor.execute("""SELECT customers.customer_name FROM customers
                   JOIN product_customers ON customers.id = product_customers.customer_id
                   WHERE product_customers.product_id =?""",
                   (product_id,))
    return [row[0] for row in cursor.fetchall()]
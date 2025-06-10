from models import *
import logging
from fastapi import HTTPException
from crud.utils import raise_404_if_not_found, raise_404_if_not_empty

logging.basicConfig(level=logging.INFO)

def add_quote(conn, cursor, product_id, quote_dict):
    # Add quote info per customer; raises if customer not found
    # quote_dict is a dictionary of quotes in the following structure:
    # {customer: {quote: int, remark: str}}
    for customer_name, data in quote_dict.items():
        quote_value = round(data.quote,2)
        quote_remark = data.remark
        cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (customer_name,))
        customer = cursor.fetchone()
        if customer is None:
            raise ValueError(f"Customer {customer_name} not found")
        customer_id = customer[0]
        cursor.execute("""INSERT INTO quotes(product_id, customer_id, quote, quote_remark)
                        VALUES(?, ?, ?, ?)""",
                        (product_id, customer_id, quote_value, quote_remark))
            
def delete_quote(conn, cursor, product_id, customer_name, quote, quote_remark):
    # Delete a quote by customer + content; raises if customer not found
    cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (customer_name,))
    customer = cursor.fetchone()
    if customer is None:
        raise ValueError(f"Customer {customer_name} not found")
    customer_id = customer[0]
    cursor.execute("""DELETE FROM quotes WHERE product_id = ? AND customer_id = ?
                    AND quote = ? AND quote_remark = ?""",
                    (product_id, customer_id, round(quote, 2), quote_remark))
    raise_404_if_not_found(cursor, msg = "quote not found")

def edit_quote(conn, cursor, product_id, customer_name, new_quote, new_remark):
    # Update a customer's quote/remark for a product
    # Raises if no matching quote found
    cursor.execute("SELECT id FROM customers WHERE customer_name = ?", (customer_name,))
    result = cursor.fetchone()
    if result == None:
        raise ValueError ("Customer not found")
    customer_id = result[0]
    cursor.execute("UPDATE quotes SET quote = ?, quote_remark = ? WHERE product_id = ? AND customer_id = ?",
                    (round(new_quote, 2), new_remark, product_id, customer_id))
    
    if cursor.rowcount == 0:
        raise ValueError("No matching quote found to update")


def list_quote(cursor):
    # List all quotes associated with a customer
    result = cursor.execute("""
        SELECT q.quote, q.quote_remark, c.customer_name
        FROM quotes q
        JOIN customers c ON q.customer_id = c.id
    """).fetchall()
    return result
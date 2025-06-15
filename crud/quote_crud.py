from models import *
import logging
from crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty

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
        raise_value_error_if_empty(customer, f"Customer {customer_name} not found")

        customer_id = customer[0]
        cursor.execute("""INSERT INTO quotes(product_id, customer_id, quote, quote_remark)
                        VALUES(?, ?, ?, ?)""",
                        (product_id, customer_id, quote_value, quote_remark))
            
def delete_quote(conn, cursor, quote_id):
    cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    raise_value_error_if_not_found(cursor, msg = "quote not found")

def edit_quote(conn, cursor, quote_id, quote=None, quote_remark=None):
    if quote is not None:
        quote = round(quote,2)
    cursor.execute("UPDATE quotes SET quote = ?, quote_remark = ? WHERE id = ?",
                    (quote, quote_remark, quote_id))
    
    raise_value_error_if_not_found(cursor, "No matching quote found to update")

def list_quote(cursor):
    # List all quotes associated with a customer
    result = cursor.execute("""
        SELECT q.quote, q.quote_remark, c.customer_name
        FROM quotes q
        JOIN customers c ON q.customer_id = c.id
    """).fetchall()
    return result

def get_quote_by_id(cursor, quote_id):
    # List a specific quote given quote_id
    result = cursor.execute("""
        SELECT q.id as quote_id, q. customer_id, q.quote, q.quote_remark, c.customer_name
        FROM quotes q
        JOIN customers c ON q.customer_id = c.id
        WHERE q.id =?
    """, (quote_id,)).fetchone()
    return result
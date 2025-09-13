from backend.models import *
import logging
from backend.crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty

logging.basicConfig(level=logging.INFO)

def search_by_barcode(conn, cursor, barcode):
    cursor.execute("SELECT id FROM product_manager WHERE barcode = ?", (barcode,))
    product_ids = [row[0] for row in cursor.fetchall()]
    raise_value_error_if_empty(product_ids, "No product found with that barcode")
    return product_ids

def search_by_ref_num(conn, cursor, ref_num):
    cursor.execute("SELECT id FROM product_manager WHERE ref_num = ?", (ref_num,))
    product_ids = [row[0] for row in cursor.fetchall()]
    raise_value_error_if_empty(product_ids, "No product found with that reference number")
    return product_ids

LOCKED_TTL_MIN = 2

def locked_product(conn, cursor, product_id, user) -> bool:
    """ 
    Return true if the user takes the lock - if either one of the following is true:
    - the lock expired after 2 minutes - defined by LOCKED_TTL_MIN;
    - or refreshed by the same user
    Return false if someone else is holding the lock
    """
    with conn:
        cursor.execute("""UPDATE product_manager
                       SET locked_by = ?, locked_timestamp = CURRENT_TIMESTAMP
                       WHERE id = ?
                       AND (locked_by IS NULL
                            OR locked_timestamp <= DATETIME('now', ?))""",
                       (user, product_id, f'-{LOCKED_TTL_MIN} minutes'))
        if cursor.rowcount == 1:
            return True
        
        cursor.execute("""UPDATE product_manager
                       SET locked_timestamp = CURRENT_TIMESTAMP
                       WHERE id = ?
                       AND locked_by = ?
                       AND locked_timestamp > DATETIME('now', ?)""",
                       (product_id, user, f'-{LOCKED_TTL_MIN} minutes'))
        if cursor.rowcount == 1:
            return True
        
        return False
        

def unlock_product(conn, cursor, product_id, user: str, admin = False):
    """
    Unlock the product if one of the following:
    1) admin = True
    2) if the user holds the lock, that user can unlock immediately
    3) otherwise if > LOCKED_TTL_MIN passes, unlock automatically
    """
    if admin:
        cond = "1=1"
        params = (product_id,)
    elif user:
        cond = "locked_by = ? OR locked_timestamp <= DATETIME('now', ?)"
        params = (product_id, user, f'-{LOCKED_TTL_MIN} minutes')
    else:
        cond = "locked_timestamp <= DATETIME('now', ?)"
        params = (product_id, f'-{LOCKED_TTL_MIN} minutes')
    with conn:
        cursor.execute(f"""UPDATE product_manager
                       SET locked_by = NULL, locked_timestamp = NULL
                       WHERE id = ? AND {cond}""",
                       params)

def get_lock_status(cursor, product_id):
    row = cursor.execute("""SELECT locked_by, locked_timestamp
                         FROM product_manager
                         WHERE id = ?""", (product_id,)).fetchone()
    return None if not row else {"locked_by": row[0], "locked_timestamp": row[1]}

def clean_orphaned_data(conn, cursor):
    """
    Removes unused tags, customers, and quotes not associated with any active product.
    Should be called periodically for data hygiene.
    """
    logging.info("Starting cleanup of orphaned data...")

    with conn:
        # Remove unused tags
        cursor.execute("""
            DELETE FROM tags
            WHERE id NOT IN (
                SELECT DISTINCT tag_id FROM product_tags
            )
        """)

        # Remove unused customers
        cursor.execute("""
            DELETE FROM customers
            WHERE id NOT IN (
                SELECT DISTINCT customer_id FROM product_customers
            )
            AND id NOT IN (
                SELECT DISTINCT customer_id FROM quotes
            )
        """)

        # Remove quotes whose product_id no longer exists (in theory CASCADE should handle this)
        cursor.execute("""
            DELETE FROM quotes
            WHERE product_id NOT IN (
                SELECT id FROM product_manager
            )
        """)

    logging.info("Cleanup complete.")
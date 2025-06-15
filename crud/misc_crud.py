from models import *
import logging

logging.basicConfig(level=logging.INFO)

def search_by_barcode(conn, cursor, barcode):
    cursor.execute("SELECT id FROM product_manager WHERE barcode = ?", (barcode,))
    product_ids = [row[0] for row in cursor.fetchall()]
    return product_ids

def search_by_ref_num(conn, cursor, ref_num):
    cursor.execute("SELECT id FROM product_manager WHERE ref_num = ?", (ref_num,))
    product_ids = [row[0] for row in cursor.fetchall()]
    return product_ids

def locked_product(conn, cursor, product_id, user):
    with conn:
        cursor.execute("""UPDATE product_manager
                       SET locked_by = ?, locked_timestamp = CURRENT_TIMESTAMP WHERE id = ?""",
                       (user, product_id))

def unlock_product(conn, cursor, product_id):
    with conn:
        cursor.execute("""UPDATE product_manager
                       SET locked_by = NULL, locked_timestamp = NULL WHERE id = ?""",
                       (product_id,))
        
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
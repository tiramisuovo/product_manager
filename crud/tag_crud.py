from models import *
import logging
from fastapi import HTTPException
from crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty

logging.basicConfig(level=logging.INFO)

def add_tag(conn, cursor, product_id, tags):
    # Link tags to product
    # Create tag entries if they don't exist
    for t in tags:
        cursor.execute("INSERT OR IGNORE INTO tags(tag_name) VALUES (?)",
                            (t,))
        cursor.execute("SELECT id FROM tags WHERE tag_name =?", (t,))
        tag_id = cursor.fetchone()[0]
        cursor.execute("""INSERT OR IGNORE INTO product_tags (product_id, tag_id)
                            VALUES (?, ?)""", (product_id, tag_id))

def delete_tag_from_product(conn, cursor, product_id, tag_id):
    # Unlink a tag from a product (tag stays in table)
    cursor.execute("DELETE FROM product_tags WHERE product_id = ? AND tag_id = ?",
                    (product_id, tag_id))
    raise_value_error_if_not_found(cursor, msg = "Tag was not linked to this product")

def edit_tag(conn, cursor, tag_id, new_name):
    # Rename tag by ID
    cursor.execute("UPDATE tags SET tag_name = ? WHERE id = ?",
                    (new_name, tag_id))
    raise_value_error_if_not_found(cursor, msg = "Tag not found")
    return cursor.execute("SELECT id, tag_name FROM tags WHERE id = ?", (tag_id,)).fetchone()
    
def search_by_tag(conn, cursor, tag_name):
    cursor.execute("SELECT id FROM tags WHERE tag_name LIKE ?", (f"%{tag_name}%",))
    tag = cursor.fetchone()
    raise_value_error_if_empty(tag, msg = "Tag not found")
    
    tag_id = tag[0]

    cursor.execute("SELECT product_id FROM product_tags WHERE tag_id = ?", (tag_id,))
    product_ids = [row[0] for row in cursor.fetchall()]

    if not product_ids:
        return []
    
    placeholders = ",".join("?" for _ in product_ids)
    query = f"SELECT * FROM product_manager WHERE id IN ({placeholders})"
    cursor.execute(query, tuple(product_ids))
    return cursor.fetchall()

def list_tag(cursor):
    cursor.execute("SELECT * FROM tags")
    result = cursor.fetchall()
    return result

def list_product_tag(cursor, product_id):
    # List all product tags asscoiated with product_id
    cursor.execute("""SELECT tags.tag_name FROM tags
                        JOIN product_tags ON tags.id = product_tags.tag_id
                        WHERE product_tags.product_id = ?""",
                        (product_id,))
    return [row[0] for row in cursor.fetchall()]
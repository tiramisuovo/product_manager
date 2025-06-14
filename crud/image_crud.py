from models import *
import logging
from fastapi import HTTPException
from crud.utils import raise_value_error_if_not_found, raise_value_error_if_empty

logging.basicConfig(level=logging.INFO)

def add_image(conn, cursor, product_id, img):
    # Add image paths to a product
    # img is a list of strings (paths)
    cursor.executemany("INSERT INTO product_images(product_id, img) VALUES(?, ?)",
                        [(product_id, i) for i in img])
    return {"img": img}
    
def delete_image(conn, cursor, image_id):
    cursor.execute("DELETE FROM product_images WHERE id = ?",
                        (image_id,))
    raise_value_error_if_not_found(cursor, msg = "Image was not linked to this product")
    return image_id

def list_images(cursor):
    cursor.execute("SELECT * FROM product_images")
    return cursor.fetchall()


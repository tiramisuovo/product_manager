from models import *
import logging
from fastapi import HTTPException
from crud.utils import raise_404_if_not_found, raise_404_if_not_empty

logging.basicConfig(level=logging.INFO)

def add_image(conn, cursor, product_id, img):
    # Add image paths to a product
    # img is a list of strings (paths)
    cursor.executemany("INSERT INTO product_images(product_id, img) VALUES(?, ?)",
                        [(product_id, i) for i in img])
    return {"img": img}
    
def delete_image(conn, cursor, product_id, delete_img):
    # Delete one particular img path given product_id
    cursor.execute("DELETE FROM product_images WHERE product_id = ? AND img = ?",
                        (product_id, delete_img))
    raise_404_if_not_found(cursor, msg = "Image was not linked to this product")
    return delete_img

def list_images(cursor):
    cursor.execute("SELECT * FROM product_images")
    return cursor.fetchall()


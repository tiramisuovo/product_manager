from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3
from crud.utils import raise_404_if_not_empty

router = APIRouter()

@router.post("/products/{product_id}/images/", response_model = Product, status_code = 201)
def create_images_endpoint(image:ImageList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_image(conn, cursor, product_id, image.imgs)
        conn.commit()
        logging.info(f"Image created: {image.imgs}")
        return format_product (conn, cursor, product_id)
    except Exception as e:
        logging.error(f"Failed to add image: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add image: {e}")

@router.delete("/products/{product_id}/images/{image_id}", status_code=204)
def delete_image_api(product_id: int, image_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = cursor.execute("SELECT img FROM product_images WHERE id = ?", (image_id,)).fetchone()
        raise_404_if_not_empty(result, msg = "Image not found")
        path = result[0]
        delete_image(conn, cursor, product_id, path)
        conn.commit()
        logging.info(f"Deleted image with ID: {image_id}")
    except Exception as e:
        logging.error(f"Failed to delete image: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {e}")


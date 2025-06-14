from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3

router = APIRouter()

@router.post("/products/{product_id}/images/", response_model = Product, status_code = 201)
def create_images_endpoint(image:ImageList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_image(conn, cursor, product_id, image.imgs)
        conn.commit()
        logging.info(f"Image created: {image.imgs}")
        return format_product (conn, cursor, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to add image: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add image: {e}")

@router.delete("/products/{product_id}/images/{image_id}", status_code=204)
def delete_image_api(image_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        delete_image(conn, cursor, image_id)
        conn.commit()
        logging.info(f"Deleted image with ID: {image_id}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to delete image: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {e}")


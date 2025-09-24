from fastapi import Depends, HTTPException, APIRouter
from backend.crud.crud import *
from backend.models import *
from backend.database.connection import get_db
import logging
from dotenv import load_dotenv
import os, sys
from backend.crud.utils import generate_signed_url

router = APIRouter()

def resource_path(relative_path: str):
    """Get absolute path to resource (works for dev & PyInstaller exe)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# explicitly load the bundled .env
env_path = resource_path(".env")
load_dotenv(env_path)

BASE_URL = os.getenv("BASE_URL")


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

@router.get("/products/{product_id}/images/list", response_model=List[str])
def get_images_endpoint(product_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        images = get_images(conn, cursor, product_id)
        logging.info(f"Retrieved image paths for product ID {product_id}: {images}")
        image_urls = []
        for img in images:
            signed_url = generate_signed_url(img)
            if signed_url:
                image_urls.append(signed_url)
            else:
                logging.warning(f"Failed to generate signed URL for image: {img}")
        return images
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to retrieve images: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve images: {e}")

from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3

router = APIRouter()

@router.post("/products/", response_model=Product, status_code = 201)
def create_product_endpoint(product: ProductCreate, db = Depends(get_db)):
    """404 if not found, 409 on duplication"""
    conn, cursor = db
    try:
        created_product = add_product(conn, cursor, product)
        conn.commit()
        logging.info(f"Product created with ref_num: {product.ref_num}")
        return format_product(conn, cursor, created_product["id"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.IntegrityError as e:
        logging.warning(f"Duplicate product ref_num: {product.ref_num}")
        raise HTTPException(status_code=409, detail="Product with this ref_num already exists.")
    except sqlite3.OperationalError as e:
        logging.error(f"Database operation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="A database operation failed.")
    except Exception as e:
        logging.error(f"Failed to add product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add product: {e}")

@router.delete("/products/{product_id}", status_code=204)
def delete_product_api(product_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        delete_product(conn, cursor, product_id)
        conn.commit()
        logging.info(f"Deleted product with ID: {product_id}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.OperationalError as e:
        logging.error(f"Database operation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="A database operation failed.")
    except Exception as e:
        logging.error(f"Failed to delete product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {e}")
    
@router.put("/products/{product_id}", response_model = Product)
def edit_product_api(product_id: int, updates: ProductUpdate, db: tuple = Depends(get_db)):
    """
    This endpoint only updates fields in the product_manager table.
    Nested fields like customers, tags, quotes, and imgs should be edited via their respective endpoints.
    """
    conn, cursor = db
    try:
        edit_product(conn, cursor, product_id, **updates.model_dump(exclude_unset = True))
        result = format_product(conn, cursor, product_id)
        conn.commit()
        logging.info(f"Edited product with ID: {product_id}")
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.OperationalError as e:
        logging.error(f"Database operation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="A database operation failed.")
    except Exception as e:
        logging.error(f"Failed to update product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update product: {e}")

@router.get("/products/search", response_model = List[Product])
def search_products_api(name: str = None,
                        tag: str = None,
                        customer: str = None,
                        barcode: int = None,
                        ref_num: str = None,
                        db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = search_products(conn, cursor, name, tag, customer, barcode, ref_num)
        logging.info(f"Search successful")
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.OperationalError as e:
        logging.error(f"Database operation error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="A database operation failed.")
    except Exception as e:
        logging.error(f"Failed to search: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to search: {e}")

@router.get("/products/{product_id}", response_model = Product)
def get_product_api(product_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = format_product(conn, cursor, product_id)
        logging.info(f"Searched product with ID: {product_id}")
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to retrieve product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve product: {e}")
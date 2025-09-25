from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from backend.crud.crud import *
from backend.models import *
from backend.database.connection import get_db
from backend.api.product_api import router as product_router
from backend.api.customer_api import router as customer_router
from backend.api.tag_api import router as tag_router
from backend.api.quote_api import router as quote_router
from backend.api.image_api import router as image_router
import logging
import os
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path, override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Debug check
logging.info(f"Loaded env OSS_BUCKET={os.getenv('OSS_BUCKET')}, OSS_ENDPOINT={os.getenv('OSS_ENDPOINT')}")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers = [
        logging.FileHandler("app.log",),
        logging.StreamHandler()
    ]
)


# Main routes
app.include_router(product_router)
app.include_router(customer_router)
app.include_router(tag_router)
app.include_router(quote_router)
app.include_router(image_router)


# Misc routes

# Raise 404 messages
def raise_404_if_not_found(cursor, msg = "Resource not found"):
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail = msg)

def raise_404_if_not_empty(result, msg = "Resource not found"):
    if not result:
        raise HTTPException(status_code=404, detail = msg)


@app.patch("/products/{product_id}/lock", response_model = Product)
def set_lock_status(product_id: int, lock: LockStatus, user: str, admin: bool = False, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        if lock.locked:
            acquired = locked_product(conn, cursor, product_id, user)
            if not acquired:
                holder = get_lock_status(cursor, product_id)
                raise HTTPException(
                    status_code=409,
                    detail={"message": "Product is locked by another user.",
                            "holder": holder["locked_by"] if holder else None,
                            "locked_timestamp": holder["locked_timestamp"] if holder else None}
                )
        else:
            unlock_product(conn, cursor, product_id, user, admin=admin)
        result = format_product(conn, cursor, product_id)
        raise_404_if_not_empty(result, msg = "Lock not found")
        conn.commit()
        logging.info(f"Set lock status for product ID: {product_id}")
        return result
    except HTTPException:
        conn.rollback()
        raise    
    except Exception as e:
        logging.error(f"Failed to update lock status: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update lock status: {e}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)
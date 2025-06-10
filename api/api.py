from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from crud.crud import *
from models import *
from database.connection import get_db
from api.product_api import router as product_router
from api.customer_api import router as customer_router
from api.tag_api import router as tag_router
from api.quote_api import router as quote_router
from api.image_api import router as image_router
import logging

app = FastAPI()

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
def set_lock_status(product_id: int, lock: LockStatus, user: str, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        if lock.locked == True:
            locked_product(conn, cursor, product_id, user)
        else:
            unlock_product(conn, cursor, product_id)
        result = format_product(conn, cursor, product_id)
        raise_404_if_not_empty(result, msg = "Lock not found")
        conn.commit()
        logging.info(f"Set lock status for product ID: {product_id}")
        return result
    except Exception as e:
        logging.error(f"Failed to update lock status: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update lock status: {e}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)
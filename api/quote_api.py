from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3

router = APIRouter()

@router.post("/products/{product_id}/quotes/", response_model = Product, status_code = 201)
def create_quotes_endpoint(quotes:QuoteDict, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_quote(conn, cursor, product_id, quotes.quotes)
        conn.commit()
        logging.info(f"Quote created: {quotes.quotes}")
        return format_product (conn, cursor, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to add quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add quote: {e}")

@router.delete("/products/{product_id}/quotes/{quote_id}", status_code=204)
def delete_quote_api(quote_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        delete_quote(conn, cursor, quote_id)
        conn.commit()
        logging.info(f"Deleted quote with ID: {quote_id}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to delete quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete quote: {e}")


@router.patch("/quotes/{quote_id}", response_model = QuoteOut)
def edit_quote_api(quote_id: int, new_quote: QuoteUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        update_data = new_quote.model_dump(exclude_unset = True)
        edit_quote(conn, cursor, quote_id, **update_data)
        conn.commit()
        logging.info(f"Edited quote with ID: {quote_id}")
        quote = get_quote_by_id(cursor, quote_id)
        if not quote:
            raise HTTPException(status_code=404, detail="Quote not found")
        return QuoteOut(quote_id = quote["quote_id"], customer_id=quote["customer_id"],
                        customer_name = quote["customer_name"], quote=quote["quote"],
                        quote_remark = quote["quote_remark"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to update quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update quote: {e}")


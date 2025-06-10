from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3
from crud.utils import raise_404_if_not_found, raise_404_if_not_empty


router = APIRouter()

@router.post("/products/{product_id}/quotes/", response_model = Product, status_code = 201)
def create_quotes_endpoint(quotes:QuoteDict, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_quote(conn, cursor, product_id, quotes.quotes)
        conn.commit()
        logging.info(f"Quote created: {quotes.quotes}")
        return format_product (conn, cursor, product_id)
    except Exception as e:
        logging.error(f"Failed to add quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add quote: {e}")

@router.delete("/products/{product_id}/quotes/{quote_id}", status_code=204)
def delete_quote_api(quote_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = cursor.execute("""SELECT q.product_id, c.customer_name, q.quote, q.quote_remark
                                FROM customers c
                                JOIN quotes q ON q.customer_id = c.id
                                WHERE q.id = ?""",
                                (quote_id,)).fetchone()
        raise_404_if_not_empty(result, msg = "Quote not found")
        product_id, customer_name, quote, quote_remark = result
        delete_quote(conn, cursor, product_id, customer_name, quote, quote_remark)
        conn.commit()
        logging.info(f"Deleted quote with ID: {quote_id}")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to delete quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete quote: {e}")


@router.patch("/quotes/{quote_id}", response_model = QuoteDict)
def edit_quote_api(quote_id: int, new_quote: QuoteUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = cursor.execute("""SELECT q.product_id, c.customer_name
                                FROM customers c
                                JOIN quotes q on q.customer_id = c.id
                                WHERE q.id = ?""", (quote_id,)).fetchone()
        raise_404_if_not_empty(result, msg = "Quote not found")
        product_id, customer_name = result
        edit_quote(conn, cursor, product_id, customer_name, new_quote.quote, new_quote.remark)
        quotes = list_quote(cursor)
        conn.commit()
        logging.info(f"Edited quote with ID: {quote_id}")
        return QuoteDict (quotes= {row["customer_name"]:
                                   QuoteDetail(quote = row["quote"], remark = row["quote_remark"])
                                   for row in quotes})
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to update quote: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update quote: {e}")


from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3
from crud.utils import raise_404_if_not_found, raise_404_if_not_empty

router = APIRouter()

@router.post("/products/{product_id}/customers/", response_model = Product, status_code = 201)
def create_customers_endpoint(customers:CustomerList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_customer(conn, cursor, product_id, customers.customers)
        conn.commit()
        logging.info(f"Customer created: {customers.customers}")
        return format_product (conn, cursor, product_id)
    except Exception as e:
        logging.error(f"Failed to add customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add customer: {e}")

@router.delete("/products/{product_id}/customers/{customer_id}", status_code=204)
def delete_customer_from_product_api(product_id: int, customer_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = cursor.execute("""SELECT c.customer_name
                                FROM customers c
                                JOIN product_customers pc ON pc.customer_id = c.id
                                WHERE pc.product_id = ? AND c.id = ?""", (product_id, customer_id)).fetchone()
        raise_404_if_not_empty(result, msg = "Customer not found")
        customer_name = result[0]
        delete_customer_from_product(conn, cursor, product_id, customer_name)
        conn.commit()
        logging.info(f"Deleted customer with ID: {customer_id} from product: {product_id}")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to delete customer from product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete customer from product: {e}")


@router.patch("/customers/{customer_id}", response_model = CustomerList)
def edit_customer_api(customer_id: int, new_name: CustomerUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        edit_customer(conn, cursor, customer_id, new_name.new_name)
        result = list_customer(cursor)
        conn.commit()
        logging.info(f"Edited customer with ID: {customer_id}")
        return CustomerList (customers = [row["customer_name"] for row in result])
    except Exception as e:
        logging.error(f"Failed to update customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update customer: {e}")

@router.get("/customers", response_model = CustomerList)
def list_customer_api(db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = list_customer(cursor)
        customers = [row ["customer_name"] for row in result]
        return CustomerList(customers=customers)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to retrieve customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve customer: {e}")
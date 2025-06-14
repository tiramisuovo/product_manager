from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3

router = APIRouter()

@router.post("/products/{product_id}/customers/", response_model = Product, status_code = 201)
def create_customers_endpoint(customers:CustomerList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_customer(conn, cursor, product_id, customers.customers)
        conn.commit()
        logging.info(f"Customer created: {customers.customers}")
        return format_product (conn, cursor, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to add customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add customer: {e}")

@router.delete("/products/{product_id}/customers/{customer_id}", status_code=204)
def delete_customer_from_product_api(product_id: int, customer_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        delete_customer_from_product(conn, cursor, product_id, customer_id)
        conn.commit()
        logging.info(f"Deleted customer with ID: {customer_id} from product: {product_id}")
    except ValueError as e:
        print("Caught ValueError:", str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to delete customer from product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete customer from product: {e}")


@router.patch("/customers/{customer_id}", response_model = CustomerOut)
def edit_customer_api(customer_id: int, new_name: CustomerUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        update_data = new_name.model_dump(exclude_unset = True)
        updated_customer = edit_customer(conn, cursor, customer_id, **update_data)
        conn.commit()
        logging.info(f"Edited customer with ID: {customer_id}")
        return CustomerOut(id = updated_customer["id"], customer_name = updated_customer["customer_name"] )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to update customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update customer: {e}")

@router.get("/customers", response_model = List[CustomerOut])
def list_customer_api(db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = list_customer(cursor)
        return [CustomerOut(id=row["id"], customer_name=row["customer_name"]) for row in result]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to retrieve customer: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve customer: {e}")
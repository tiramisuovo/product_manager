from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3

router = APIRouter()


@router.post("/products/{product_id}/tags/", response_model = Product, status_code = 201)
def create_tags_endpoint(tags:TagList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_tag(conn, cursor, product_id, tags.tags)
        conn.commit()
        logging.info(f"Tag created: {tags.tags}")
        return format_product (conn, cursor, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to add tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add tag: {e}")

@router.delete("/products/{product_id}/tags/{tag_id}", status_code=204)
def delete_tag_from_product_api(product_id: int, tag_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        delete_tag_from_product(conn, cursor, product_id, tag_id)
        conn.commit()
        logging.info(f"Deleted tag with ID: {tag_id} from product: {product_id}")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to delete tag from product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete tag from product: {e}")

@router.patch("/tags/{tag_id}", response_model = TagOut)
def edit_tag_api(tag_id: int, new_name: TagUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        update_data = new_name.model_dump(exclude_unset = True)
        updated_tag = edit_tag(conn, cursor, tag_id, **update_data)
        conn.commit()
        logging.info(f"Edited tag with ID: {tag_id}")
        return TagOut(id=updated_tag["id"], tag_name=updated_tag["tag_name"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to update tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update tag: {e}")

@router.get("/tags", response_model = List[TagOut])
def list_tag_api(db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = list_tag(cursor)
        return [TagOut(id=row["id"], tag_name=row["tag_name"]) for row in result]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Failed to retrieve tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tag: {e}")
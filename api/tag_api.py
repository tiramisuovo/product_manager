from fastapi import Depends, HTTPException, APIRouter
from crud.crud import *
from models import *
from database.connection import get_db
import logging
import sqlite3
from crud.utils import raise_404_if_not_found, raise_404_if_not_empty

router = APIRouter()


@router.post("/products/{product_id}/tags/", response_model = Product, status_code = 201)
def create_tags_endpoint(tags:TagList, product_id:int, db = Depends(get_db)):
    conn, cursor = db
    try:
        add_tag(conn, cursor, product_id, tags.tags)
        conn.commit()
        logging.info(f"Tag created: {tags.tags}")
        return format_product (conn, cursor, product_id)
    except Exception as e:
        logging.error(f"Failed to add tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to add tag: {e}")

@router.delete("/products/{product_id}/tags/{tag_id}", status_code=204)
def delete_tag_from_product_api(product_id: int, tag_id: int, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = cursor.execute("""SELECT t.tag_name
                                FROM tags t
                                JOIN product_tags pt ON pt.tag_id = t.id
                                WHERE pt.product_id = ? AND t.id = ?""", (product_id, tag_id)).fetchone()
        raise_404_if_not_empty(result, msg = "Tag not found")
        tag_name = result[0]
        delete_tag_from_product(conn, cursor, product_id, tag_name)
        conn.commit()
        logging.info(f"Deleted tag with ID: {tag_id} from product: {product_id}")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to delete tag from product: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to delete tag from product: {e}")

@router.patch("/tags/{tag_id}", response_model = TagList)
def edit_tag_api(tag_id: int, new_name: TagUpdate, db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        edit_tag(conn, cursor, tag_id, new_name.new_name)
        result = list_tag(cursor)
        conn.commit()
        logging.info(f"Edited tag with ID: {tag_id}")
        return TagList (tags = [row["tag_name"] for row in result])
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to update tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to update tag: {e}")

@router.get("/tags", response_model = TagList)
def list_tag_api(db: tuple = Depends(get_db)):
    conn, cursor = db
    try:
        result = list_tag(cursor)
        tags = [row ["tag_name"] for row in result]
        return TagList(tags=tags)
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Failed to retrieve tag: {e}", exc_info = True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tag: {e}")
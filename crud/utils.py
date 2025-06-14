from fastapi import HTTPException

# Raise error for udpate/delete statments
def raise_404_if_not_found(cursor, msg = "Resource not found"):
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail = msg)
    
# Raise errors for select and fetchone/fetchall
def raise_404_if_empty(result, msg = "Resource not found"):
    if not result:
        raise HTTPException(status_code=404, detail = msg)


# Raise value error if empty; select + fetchone/fetchall statements
def raise_value_error_if_empty(result, msg = "Resource not found"):
    if not result:
        raise ValueError(msg)

# Raise value error; delete/update statments
def raise_value_error_if_not_found(cursor, msg = "Resource not found"):
    if cursor.rowcount == 0:
        raise ValueError(msg)
    
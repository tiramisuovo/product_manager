from fastapi import HTTPException

# Raise error for udpate/delete statments
def raise_404_if_not_found(cursor, msg = "Resource not found"):
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail = msg)
    
# Raise errors for select and fetchone/fetchall
def raise_404_if_not_empty(result, msg = "Resource not found"):
    if not result:
        raise HTTPException(status_code=404, detail = msg)
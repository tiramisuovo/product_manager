import sqlite3
from database.schema import create_table

def init_database(db_name = "product_manager.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    create_table(conn, cursor)
    conn.close()

def get_db(db_name = "product_manager.db"):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    try:
        yield conn, cursor
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


def reset_database(db_name = "product_manager.db"):
    # for whole database reset if necessary
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    with conn:
        cursor.execute("PRAGMA foreign_keys = OFF")
        cursor.execute("DROP TABLE IF EXISTS product_images")
        cursor.execute("DROP TABLE IF EXISTS customers")
        cursor.execute("DROP TABLE IF EXISTS product_customers")
        cursor.execute("DROP TABLE IF EXISTS tags")
        cursor.execute("DROP TABLE IF EXISTS product_tags")
        cursor.execute("DROP TABLE IF EXISTS quotes")

        cursor.execute("DROP TABLE IF EXISTS product_manager")
        cursor.execute("PRAGMA foreign_keys = ON")
        create_table(conn, cursor)
    conn.close()



if __name__ == "__main__":
    init_database()
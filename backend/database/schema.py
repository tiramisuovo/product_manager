import sqlite3

def create_table(conn, cursor):
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_manager (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ref_num TEXT UNIQUE,
                name TEXT COLLATE NOCASE,
                barcode INTEGER CHECK (barcode >= 0),
                pcs_innerbox INTEGER CHECK (pcs_innerbox >= 0),
                pcs_ctn INTEGER CHECK (pcs_ctn >= 0),
                weight REAL CHECK (weight >= 0),
                price_usd REAL CHECK (price_usd >= 0),
                price_rmb REAL CHECK (price_rmb >= 0),
                remarks TEXT,
                packing TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                deleted INTEGER DEFAULT 0,
                locked_by TEXT DEFAULT NULL,
                locked_timestamp TEXT DEFAULT NULL
                )""")
        
        # Images
        cursor.execute("""CREATE TABLE IF NOT EXISTS product_images(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER,
                            img TEXT,
                            FOREIGN KEY (product_id) REFERENCES product_manager(id) ON DELETE CASCADE)""")
    
    
        # Individual customer
        cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_name TEXT COLLATE NOCASE)""")
        
    
        # Product_customers linked table
        cursor.execute("""CREATE TABLE IF NOT EXISTS product_customers(
                            product_id INTEGER,
                            customer_id INTEGER,
                            FOREIGN KEY(product_id) REFERENCES product_manager(id) ON DELETE CASCADE,
                            FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
                            PRIMARY KEY(product_id, customer_id))""")
    
        # Individual tag
        cursor.execute("""CREATE TABLE IF NOT EXISTS tags(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tag_name TEXT UNIQUE)""")

        # Product_tags linked table
        cursor.execute("""CREATE TABLE IF NOT EXISTS product_tags(
                            product_id INTEGER,
                            tag_id INTEGER,
                            FOREIGN KEY (product_id) REFERENCES product_manager(id) ON DELETE CASCADE,
                            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
                            PRIMARY KEY (product_id, tag_id))""")
    
        # Quotes that is asscociated with a customer; has quote (i.e. value), timestamp, and remark
        cursor.execute("""CREATE TABLE IF NOT EXISTS quotes(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            product_id INTEGER,
                            customer_id INTEGER,
                            quote REAL CHECK (quote>=0),
                            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                            quote_remark TEXT,
                            FOREIGN KEY (product_id) REFERENCES product_manager(id) ON DELETE CASCADE,
                            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
                            )""")
        conn.commit()

def create_index(conn, cursor):
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_ref_num ON product_manager(ref_num)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON product_manager(name COLLATE NOCASE)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_barcode ON product_manager(barcode)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tag_name ON tags(tag_name COLLATE NOCASE)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_customer_name ON customers(customer_name COLLATE NOCASE)")
        conn.commit()
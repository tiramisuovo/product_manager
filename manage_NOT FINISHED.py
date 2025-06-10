import sys, os
import sqlite3
from your_module import clean_orphaned_data  # adjust import

def cleanup():
    base_dir = os.path.dirname(__file__)
    db_path = os.path.join(base_dir, "your_database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    clean_orphaned_data(conn, cursor)
    conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "cleanup":
        cleanup()
    else:
        print(f"Unknown command: {command}")
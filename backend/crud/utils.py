import oss2
import os, sys
from dotenv import load_dotenv

# Raise value error if empty; select + fetchone/fetchall statements
def raise_value_error_if_empty(result, msg = "Resource not found"):
    if not result:
        raise ValueError(msg)

# Raise value error; delete/update statments
def raise_value_error_if_not_found(cursor, msg = "Resource not found"):
    if cursor.rowcount == 0:
        raise ValueError(msg)
    

# OSS utils
def resource_path(relative_path: str):
    """Get absolute path to resource (works for dev & PyInstaller exe)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# explicitly load the bundled .env
env_path = resource_path(".env")
load_dotenv(env_path)

ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET')
ENDPOINT = os.getenv('OSS_ENDPOINT')
BUCKET_NAME = os.getenv('OSS_BUCKET')

# Auth & Bucket instance
def get_bucket():
    auth = oss2.Auth(
        os.getenv("OSS_ACCESS_KEY_ID"),
        os.getenv("OSS_ACCESS_KEY_SECRET")
    )
    return oss2.Bucket(auth, os.getenv("OSS_ENDPOINT"), os.getenv("OSS_BUCKET"))

def generate_signed_url(oss_key, expires_in_seconds=600) -> str:
    try:
        bucket = get_bucket()
        url = bucket.sign_url("GET", oss_key, expires_in_seconds)
        return url
    except Exception as e:
        print(f"[EXCEPTION] Signed URL error: {e}")
        return None
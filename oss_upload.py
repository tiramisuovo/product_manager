import oss2
import os, sys
from dotenv import load_dotenv

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
auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)


def upload_file(local_path, oss_key) -> bool:
    """
    Upload a file to OSS with AES256 encryption
    :param local_path: Local file path (e.g. ./images/tool123.png)
    :param oss_key: OSS path (e.g. uploads/tool123.png)
    :return: True if success, False if failed
    """

    if not os.path.exists(local_path):
        print(f"[ERROR] File not found: {local_path}")
        return False

    try:
        result = bucket.put_object_from_file(oss_key, 
                                             local_path, 
                                             headers={"x-oss-server-side-encryption": "AES256"})


        if result.status in (200, 204, 201):
            print(f"[✅] Uploaded: {oss_key}")
            return True
        else:
            print(f"[❌] Upload failed: {result.status}")
            return False

    except Exception as e:
        print(f"[EXCEPTION] Upload error: {e}")
        return False


def generate_signed_url(oss_key, expires_in_seconds=600) -> str:
    """
    Generate a signed download URL (expires in X seconds)
    :param oss_key: File path in OSS
    :param expires_in_seconds: Validity duration (default 10 mins)
    :return: URL string
    """
    try:
        url = bucket.sign_url('GET', oss_key, expires_in_seconds)
        print(f"[🔗] Signed URL: {url}")
        return url
    except Exception as e:
        print(f"[EXCEPTION] Signed URL error: {e}")
        return None

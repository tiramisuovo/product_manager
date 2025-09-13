import os, tempfile
from desktop.oss_upload import upload_file, generate_signed_url
from pathlib import Path
import requests
from desktop.client import post_img_client, delete_img_client
import time

def select_and_upload_image(local_path: str, product_id: int, key_name: str) -> str:
    oss_key = f"uploads/{key_name}"

    t0 = time.perf_counter()
    uploaded = upload_file(local_path, oss_key)
    t1 = time.perf_counter()
    if uploaded:
        generate_signed_url(oss_key)
    else:
        raise Exception("Upload failed")

    # Send oss_key to backend to save in DB
    resp = post_img_client(product_id, [oss_key])
    t2 = time.perf_counter()
    print(f"[timing] upload={(t1-t0):.2f}s  backend={(t2-t1):.2f}s  total={(t2-t0):.2f}s")
    
    return oss_key

def get_signed_url_for_key(oss_key: str) -> str:
    url = generate_signed_url(oss_key)
    if not url:
        raise RuntimeError("Failed to generate signed URL")
    return url
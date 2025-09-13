import requests, logging
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


BASE_URL = os.getenv("BASE_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("client.log"),
        logging.StreamHandler()]
)

_session = requests.Session()

def api_request(method, url, **kwargs):
    try:
        response = requests.request(method=method, url=url, timeout=5, **kwargs)
        response.raise_for_status()
        logging.info(f"SUCCESS: {method.upper()} {url} | Status: {response.status_code}")
        if response.status_code == 204 or not response.content.strip():
            return {"message": "No return content"}
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API ERROR: {method.upper()} {url} | Exception: {e} | Payload: {kwargs}")
        raise

def search_product_client(name = None, tag = None, customer = None, barcode = None, ref_num = None):
    params = {
        "name": name,
        "tag": tag,
        "customer": customer,
        "barcode": barcode,
        "ref_num": ref_num
    }
    params = {key:value for key, value in params.items() if value is not None}
    return api_request("get", f"{BASE_URL}/products/search", params = params)

def post_product_client(product):
    return api_request("post", f"{BASE_URL}/products/", json=product)

def delete_product_client(product_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}")

def edit_product_client(product_id, update):
    return api_request("put", f"{BASE_URL}/products/{product_id}", json=update)

def get_product_client(product_id):
    return api_request("get", f"{BASE_URL}/products/{product_id}")

def post_customer_client(product_id, customer: list[str]):
    formatted_customer = {"customers": customer}
    return api_request("post", f"{BASE_URL}/products/{product_id}/customers/",
                       json = formatted_customer)

def delete_customer_client(product_id, customer_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/customers/{customer_id}")

def edit_customer_client(customer_id, update: str):
    payload = {"new_name": update}
    return api_request("patch", f"{BASE_URL}/customers/{customer_id}", json= payload)

def get_customer_client():
    return api_request("get", f"{BASE_URL}/customers")

def post_tag_client(product_id, tag: list[str]):
    formatted_tag = {"tags": tag}
    return api_request("post", f"{BASE_URL}/products/{product_id}/tags/",
                       json = formatted_tag)

def delete_tag_client(product_id, tag_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/tags/{tag_id}")

def edit_tag_client(tag_id, update):
    payload = {"new_name": update}
    return api_request("patch", f"{BASE_URL}/tags/{tag_id}", json=payload)

def get_tag_client():
    return api_request("get", f"{BASE_URL}/tags")

def post_quote_client(product_id, quote: list[dict]):
    formatted_quote = {"quotes": quote}
    return api_request("post", f"{BASE_URL}/products/{product_id}/quotes/",
                       json = formatted_quote)

def delete_quote_client(product_id, quote_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/quotes/{quote_id}")

def edit_quote_client(quote_id, update):
    return api_request("patch", f"{BASE_URL}/quotes/{quote_id}", json=update)

def post_img_client(product_id, img: list[str]):
    formatted_imgs = {"imgs": img}
    return api_request("post", f"{BASE_URL}/products/{product_id}/images/",
                       json = formatted_imgs)

def delete_img_client(product_id, img_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/images/{img_id}")

def product_lock_client(product_id, user: str, locked: bool, admin: bool = False):
    payload = {"locked": locked}
    params = {"user": user}
    if admin:
        params["admin"] = "true"
    return api_request("patch", f"{BASE_URL}/products/{product_id}/lock",
                       params = params, json = payload)

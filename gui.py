# GUI

import requests, sys, logging

BASE_URL = "http://47.97.40.214"

def api_request(method, url, **kwargs):
    try:
        response = requests.request(method=method, url=url, timeout=5, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
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
    formatted_customer = {"customer_name": customer}
    return api_request("post", f"{BASE_URL}/products/{product_id}/customers/",
                       json = formatted_customer)

def delete_customer_client(product_id, customer_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/customers/{customer_id}")

def edit_customer_client(customer_id, update):
    return api_request("put", f"{BASE_URL}/customers/{customer_id}", json=update)

def get_customer_client():
    return api_request("get", f"{BASE_URL}/customers")

def post_tag_client(product_id, tag: list[str]):
    formatted_tag = {"tag_name": tag}
    return api_request("post", f"{BASE_URL}/products/{product_id}/tags/",
                       json = formatted_tag)

def delete_tag_client(product_id, tag_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/tags/{tag_id}")

def edit_tag_client(tag_id, update):
    return api_request("put", f"{BASE_URL}/customers/{tag_id}", json=update)

def get_tag_client():
    return api_request("get", f"{BASE_URL}/tags")

def post_quote_client(product_id, customer_name: str, quote: float, remark: str):
    formatted_quote = {"quotes": {
        customer_name: {"quote": quote, "remark": remark}}}
    return api_request("post", f"{BASE_URL}/products/{product_id}/quotes/",
                       json = formatted_quote)

def delete_tag_client(product_id, tag_id):
    return api_request("delete", f"{BASE_URL}/products/{product_id}/tags/{tag_id}")

def edit_tag_client(tag_id, update):
    return api_request("put", f"{BASE_URL}/customers/{tag_id}", json=update)

def get_tag_client():
    return api_request("get", f"{BASE_URL}/tags")



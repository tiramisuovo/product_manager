# UI models

import os, json
from models import Product

class ProductVM():
    def __init__ (self, data: dict | Product):
        if isinstance(data, Product):
            data = data.model_dump()
        self.id = data.get("id")
        self.ref_num = data.get("ref_num")
        self.name = data.get("name")
        self.barcode = data.get("barcode")
        self.pcs_innerbox = data.get("pcs_innerbox")
        self.pcs_ctn = data.get("pcs_ctn")
        self.weight = data.get("weight")
        self.price_usd = data.get("price_usd")
        self.price_rmb = data.get("price_rmb")
        self.remarks = data.get("remark")
        self.packing = data.get("packing")
        self.customers = data.get("customers", []) or []
        self.quotes = data.get("quote", []) or []
        self.imgs = data.get("imgs", []) or []
        self.tags = data.get("tags", []) or []
        self.locked_by = data.get("locked_by")
        self.locked_timestamp = data.get("locked_timestamp")
        self.last_updated = data.get("last_updated")

    def to_create_payload (self) -> dict:
        return {
            "ref_num": self.ref_num,
            "name": self.name,
            "barcode": self.barcode,
            "pcs_innerbox": self.pcs_innerbox,
            "pcs_ctn": self.pcs_ctn,
            "weight": self.weight,
            "price_usd": self.price_usd,
            "price_rmb": self.price_rmb,
            "remarks": self.remarks,
            "packing": self.packing,
            "customers": [c["customer_name"] for c in self.customers],
            "quote": {q["customer_name"]:{
                "quote": q["quote"],
                "remark": q["remark"]
            } for q in self.quotes},
            "imgs": [i["img"] for i in self.imgs],
            "tags": [t["tag_name"] for t in self.tags],
            "locked_by": self.locked_by,
            "locked_timestamp": self.locked_timestamp,
            "last_updated": self.last_updated
        }
    
    def to_update_product_payload(self) -> dict:
        # Only product flat fields updated here
        return {
            "name": self.name,
            "barcode": self.barcode,
            "pcs_innerbox": self.pcs_innerbox,
            "pcs_ctn": self.pcs_ctn,
            "weight": self.weight,
            "price_usd": self.price_usd,
            "price_rmb": self.price_rmb,
            "remarks": self.remarks,
            "packing": self.packing,
        }

    def to_update_customer_payload(self, customer) -> dict:
        # To update 1 customer only
        return {
            "new_name": customer["customer_name"]
        }

    def to_update_tag_payload(self, tag) -> dict:
        # To update 1 tag only
        return {
            "new_name": tag["tag_name"]
        }
    
    def to_update_quote_payload(self, quote) -> dict:
        # To update 1 quote only
        return {
            "quote": quote["quote"],
            "remark": quote["remark"]
        }
    




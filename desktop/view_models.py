import os, json
from backend.models import Product
from desktop.client import *
from typing import Any
from desktop.product_draft import ProductDraft

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
        self.remarks = data.get("remarks")
        self.packing = data.get("packing")
        self.customers = data.get("customers", []) or []   
        self.quotes = [q if isinstance(q, dict) else q.model_dump()
                       for q in data.get("quote", []) or []]
        self.imgs = data.get("imgs", []) or []
        self.tags = data.get("tags", []) or []
        self.locked_by = data.get("locked_by")
        self.locked_timestamp = data.get("locked_timestamp")
        self.last_updated = data.get("last_updated")

    @classmethod
    def from_draft(cls, draft: "ProductDraft") -> "ProductVM":
        return cls(draft.to_payload())

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
            "customers": self.customers,
            "quote": [{"customer_name": q["customer_name"],
                      "quote": q["quote"],
                      "remark": q["remark"]} for q in self.quotes],
            "imgs": self.imgs,
            "tags": self.tags,
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
    

class ProductManager():
    def __init__(self):
        self._product_cache: list[ProductVM] = []

    def update_cache(self, vm: ProductVM, updated_vm: ProductVM):
        for i, p in enumerate(self._product_cache):
            if p.id == vm.id:
                self._product_cache[i] = updated_vm
                break
    
    def clear_cache(self):
        self._product_cache = []

    def find_by_ref_num(self, ref_num: str):
        for vm in self._product_cache:
            if vm.ref_num == ref_num:
                return vm
        return None

    def create_product(self, data: dict):
        temp_vm = ProductVM(data) # from user input
        payload = temp_vm.to_create_payload()
        response = post_product_client (payload)

        if isinstance(response, dict):
            new_vm = ProductVM(response) # from backend response
            self._product_cache.append(new_vm)
            return new_vm
        else:
            raise ValueError("Invalid response format from post_product_client")
    
    def update_product(self, vm: ProductVM):
        payload = vm.to_update_product_payload() #flat fields only
        response = edit_product_client(vm.id, payload)
        updated_vm = ProductVM(response)
        self.update_cache(vm, updated_vm)

        return updated_vm

    def delete_product(self, vm: ProductVM):
        delete_product_client(vm.id)
        self._product_cache = [p for p in self._product_cache if p.id != vm.id]
        return vm
    
    def fetch_product(self, vm: ProductVM):
        response = get_product_client(vm.id)

        new_vm = ProductVM(response)
        self.update_cache(vm, new_vm)
        
        return new_vm

    def search_products(self,
                       name: str = None,
                       tag: str = None,
                       customer: str = None,
                       barcode: int = None,
                       ref_num: str = None):
        response = search_product_client (name = name, tag = tag, customer = customer,
                                          barcode = barcode, ref_num = ref_num)
        result = [ProductVM(p) for p in response]

        existing_ids = {p.id for p in self._product_cache}
        for vm in result:
            if vm.id not in existing_ids:
                self._product_cache.append(vm)

        return result #list of ProductVM
    
    def get_entity_by_id(self, vm: ProductVM, entity: str, match_value: Any,
                         field_to_match: str, id_field: str = "id"):
        entity_id = None
        entity_list = getattr(vm, entity, None)
        if not entity_list:
            raise ValueError(f"No entity list '{entity}' found on product {vm.id}")
        for item in entity_list:
            if item.get(field_to_match) == match_value:
                entity_id = item[id_field]
                break
        if entity_id is None:
            raise ValueError(f"{entity} '{match_value}' not found in product {vm.id}")
        return entity_id

    def find_global_matching_entity(self, entity_name: str, new_name: str):
        # Return entity ID
        if entity_name == "tags":
            tag_list = get_tag_client()
            new_tag = next((tag for tag in tag_list if tag["tag_name"] == new_name), None)
            new_tag_id = new_tag["id"] if new_tag else None
            return new_tag_id
        elif entity_name == "customers":
            customer_list = get_customer_client()
            new_customer = next((customer for customer in customer_list if customer["customer_name"] == new_name), None)
            new_customer_id = new_customer["id"] if new_customer else None
            return new_customer_id
        else:
            return None
        
    def create_customer(self, vm: ProductVM, customer_name: str):
        # Create a single customer, can scale later to accept list as necessary
        response = post_customer_client(vm.id, [customer_name])
        updated_vm = ProductVM(response)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def update_customer(self, vm: ProductVM, old_name: str, new_name: str):
        old_customer_id = self.get_entity_by_id(vm, "customers", old_name, "customer_name", "id")
        new_customer_id = self.find_global_matching_entity("customers", new_name)

        if not new_customer_id:
            edit_customer_client(old_customer_id, new_name)
        else:
            self.create_customer(vm, new_name)
            self.delete_customer(vm, old_name)

        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def bulk_update_customer(self, vm: ProductVM, old_list: list, new_list: list):
        renamed = set()
        if len(old_list) == len(new_list):
            for old, new in zip(old_list, new_list):
                if old != new:
                    self.update_customer(vm, old, new)
                    renamed.add(old)

        old_set = set(old_list)
        new_set = set(new_list)

        for customer in (old_set - new_set) - renamed:
            self.delete_customer(vm, customer)
        
        for customer in new_set - old_set:
            self.create_customer(vm, customer)
    
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def delete_customer(self, vm: ProductVM, customer_name: str):
        customer_id = self.get_entity_by_id(vm, "customers", customer_name, "customer_name", "id")
        delete_customer_client(vm.id, customer_id)
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        
        return updated_vm

    def fetch_all_customers(self):
        return get_customer_client()

    def create_tag(self, vm: ProductVM, tag_name: str):
        # Create a single tag, can scale later to accept list as necessary
        response = post_tag_client(vm.id, [tag_name])
        updated_vm = ProductVM(response)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def update_tag(self, vm: ProductVM, old_name: str, new_name: str):
        old_tag_id = self.get_entity_by_id(vm, "tags", old_name, "tag_name", "id")
        new_tag_id = self.find_global_matching_entity("tags", new_name)

        if not new_tag_id:
            edit_tag_client(old_tag_id, new_name)
        else:
            self.create_tag(vm, new_name)
            self.delete_tag(vm, old_name)

        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def bulk_update_tag(self, vm: ProductVM, old_list: list, new_list: list):
        renamed = set()
        if len(old_list) == len(new_list):
            for old, new in zip(old_list, new_list):
                if old != new:
                    self.update_tag(vm, old, new)
                    renamed.add(old)

        old_set = set(old_list)
        new_set = set(new_list)

        for tag in (old_set - new_set) - renamed:
            self.delete_tag(vm, tag)
        
        for tag in new_set - old_set:
            self.create_tag(vm, tag)

        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def delete_tag(self, vm: ProductVM, tag_name: str):
        tag_id = self.get_entity_by_id(vm, "tags", tag_name, "tag_name", "id")
        delete_tag_client(vm.id, tag_id)
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def fetch_all_tags(self):
        return get_tag_client()
    
    def create_quote(self, vm: ProductVM, quote: dict):
        # Create a single quote, can scale later to accept list as necessary
        response = post_quote_client(vm.id, [quote])
        updated_vm = ProductVM(response)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def update_quote(self, vm: ProductVM, quote_id: int, new_quote: float, new_remark: str):
        edit_quote_client(quote_id, {"quote": new_quote, "remark": new_remark})
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def bulk_update_quote(self, vm: ProductVM, old_list: list[dict], new_list: list[dict]):
        def quote_identity(q):
            return q.get("quote_id")
        
        if len(old_list) == len(new_list):
            for old, new in zip(old_list, new_list):
                if "quote_id" in old:
                    quote_changed = old.get("quote") != new.get("quote")
                    remark_changed = old.get("remark") != new.get("remark")

                    if quote_changed or remark_changed:
                        self.update_quote(vm,
                                        quote_id = old["quote_id"],
                                        new_quote = new.get("quote"),
                                        new_remark = new.get("remark"))
    
        new_ids = set(quote_identity(q) for q in new_list if "quote_id" in q)
        for q in old_list:
            if "quote_id" in q and q["quote_id"] not in new_ids:
                self.delete_quote(vm, q["quote_id"])

        for q in new_list:
            if "quote_id" not in q:
                self.create_quote(vm, q)

        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm

    def delete_quote(self, vm: ProductVM, quote_id: int):
        delete_quote_client(vm.id, quote_id)
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm

    def create_img(self, vm: ProductVM, img_path: str):
        # Create a single img, can scale later to accept list as necessary
        response = post_img_client(vm.id, [img_path])
        updated_vm = ProductVM(response)
        self.update_cache(vm, updated_vm)
        return updated_vm

    def delete_img(self, vm: ProductVM, img_path: str):
        img_id = self.get_entity_by_id(vm, "imgs", img_path, "img", "id")
        delete_img_client(vm.id, img_id)
        updated_vm = self.fetch_product(vm)
        self.update_cache(vm, updated_vm)
        return updated_vm
    
    def product_lock(self, vm: ProductVM, user: str, locked: bool):
        return product_lock_client(vm.id, user, locked)

from crud.product_crud import *
from crud.image_crud import *
from crud.customer_crud import *
from crud.tag_crud import *
from crud.quote_crud import *
from crud.misc_crud import *


"""Entry file for all CRUD functions at database level.
Following naming convention e.g. add_product in this layer"""


"""
Here are all function names, up to date as of June 8, 2025
from crud.product_crud import add_product, delete_product, search_products, search_product_name, edit_product, format_product, list_products
from crud.image_crud import add_image, delete_image, list_images
from crud.customer_crud import add_customer, delete_customer_from_product, search_by_customer, edit_customer, list_customer, list_product_customer
from crud.tag_crud import add_tag, delete_tag_from_product, edit_tag, list_tag, list_product_tag
from crud.quote_crud import add_quote, delete_quote, edit_quote, list_quote
from crud.misc_crud import search_by_barcode, search_by_ref_num, locked_product, unlock_product, clean_orphaned_data

"""
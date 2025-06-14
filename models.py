from pydantic import BaseModel, field_validator, StrictStr
from typing import List, Dict, Optional

class ProductBase(BaseModel):
    ref_num: StrictStr
    name: Optional[str] = None
    barcode: Optional[int] = None
    pcs_innerbox: Optional[int] = None
    pcs_ctn: Optional[int] = None
    weight: Optional[float] = None
    price_usd: Optional[float] = None
    price_rmb: Optional[float] = None
    remarks: Optional[str] = None
    packing: Optional[str] = None
    locked_by: Optional[str] = None
    locked_timestamp: Optional[str] = None

    @field_validator ("barcode", "pcs_innerbox", "pcs_ctn", "weight", "price_usd", "price_rmb", mode="before")
    def non_negative(cls, v, info):
        if v is None:
            return v
        if isinstance(v, str):
            raise ValueError(f"{info.field_name} must be a number, not a string")
        if v < 0:
            raise ValueError(f"{info.field_name} must be zero or positive")
        return v
    
    @field_validator("ref_num", "name", "remarks", "packing", mode="before")
    @classmethod
    def strip_strings(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

# Post models

class QuoteDetail(BaseModel):
    quote: Optional[float] = None
    remark: Optional[str] = None
    
    @field_validator ("quote")
    def non_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be zero or positive")
        return v

class ProductCreate(ProductBase):
    customers: Optional[List[StrictStr]] = None
    quote: Optional[Dict[str, QuoteDetail]] = None
    imgs: Optional[List[StrictStr]] = None
    tags: Optional[List[StrictStr]] = None

class ImageList(BaseModel):
    imgs: Optional[List[StrictStr]] = None

class CustomerList(BaseModel):
    customers: Optional[List[StrictStr]] = None

class TagList(BaseModel):
    tags: Optional[List[StrictStr]] = None

class QuoteDict(BaseModel):
    quotes: Optional[Dict[str, QuoteDetail]] = None


# Update models

class CustomerUpdate(BaseModel):
    new_name: Optional[str] = None

class TagUpdate(BaseModel):
    new_name: Optional[str] = None

class QuoteUpdate(BaseModel):
    customer_id: Optional[int] = None
    quote: Optional[float] = None
    quote_remark: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    barcode: Optional[int] = None
    pcs_innerbox: Optional[int] = None
    pcs_ctn: Optional[int] = None
    weight: Optional[float] = None
    price_usd: Optional[float] = None
    price_rmb: Optional[float] = None
    remarks: Optional[str] = None
    packing: Optional[str] = None
    customers: Optional[List[CustomerUpdate]] = None
    quote: Optional[List[QuoteUpdate]] = None
    imgs: Optional[List[int]] = None
    tags: Optional[List[TagUpdate]] = None


# View models

class ImageOut(BaseModel):
    id: int
    img: str

class TagOut(BaseModel):
    id: int
    tag_name: str

class CustomerOut(BaseModel):
    id: int
    customer_name: str

class QuoteOut(BaseModel):
    quote_id: int
    customer_id: int
    customer_name: str
    quote: float
    quote_remark: Optional[str]

class Product(ProductBase):
    id: int
    customers: Optional[List[CustomerOut]] = None
    tags: Optional[List[TagOut]] = None
    imgs: Optional[List[ImageOut]] = None
    quote: Optional[List[QuoteOut]] = None

    
# Lock status

class LockStatus(BaseModel):
    locked: bool
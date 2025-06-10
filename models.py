from pydantic import BaseModel, field_validator, StrictStr
from typing import List, Dict, Optional

class QuoteDetail(BaseModel):
    quote: Optional[float] = None
    remark: Optional[str] = None
    
    @field_validator ("quote")
    def non_negative(cls, v, info):
        if v is not None and v < 0:
            raise ValueError(f"{info.field_name} must be zero or positive")
        return v

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
    customers: Optional[List[StrictStr]] = None
    quote: Optional[Dict[str, QuoteDetail]] = None
    imgs: Optional[List[StrictStr]] = None
    tags: Optional[List[StrictStr]] = None
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

class ProductCreate(ProductBase):
    pass

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
    customers: Optional[List[str]] = None
    quote: Optional[Dict[str, QuoteDetail]] = None
    imgs: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
    
class ImageList(BaseModel):
    imgs: Optional[List[StrictStr]] = None

class CustomerList(BaseModel):
    customers: Optional[List[StrictStr]] = None

class CustomerUpdate(BaseModel):
    new_name: StrictStr

class TagList(BaseModel):
    tags: Optional[List[StrictStr]] = None

class TagUpdate(BaseModel):
    new_name: StrictStr

class QuoteDict(BaseModel):
    quotes: Optional[Dict[str, QuoteDetail]] = None

class QuoteUpdate(QuoteDetail):
    pass

class LockStatus(BaseModel):
    locked: bool
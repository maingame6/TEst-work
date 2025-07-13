from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    supplier: str
    name: str
    sku: str
    tile_size: Optional[str] = None
    box_size: Optional[float] = None
    price: float
    category: Optional[str] = None
    description: Optional[str] = None
    image_base64: Optional[str] = None
    in_stock: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProductCreate(BaseModel):
    supplier: str
    name: str
    sku: str
    tile_size: Optional[str] = None
    box_size: Optional[float] = None
    price: float
    category: Optional[str] = None
    description: Optional[str] = None
    image_base64: Optional[str] = None
    in_stock: bool = True

class ProductUpdate(BaseModel):
    supplier: Optional[str] = None
    name: Optional[str] = None
    sku: Optional[str] = None
    tile_size: Optional[str] = None
    box_size: Optional[float] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image_base64: Optional[str] = None
    in_stock: Optional[bool] = None

class ProductFilter(BaseModel):
    supplier: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    search: Optional[str] = None

class AdminUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminUserCreate(BaseModel):
    username: str
    email: str
    password: str

class AdminUserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
from fastapi import FastAPI, APIRouter, HTTPException, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class Product(BaseModel):
    id: str
    name: str
    display_name: str
    price: float
    area_m2: Optional[float] = None
    product_code: Optional[str] = None
    dimensions: Optional[str] = None
    product_type: str
    brand: str
    category: str
    section: Optional[str] = None  # Add section field
    subsection: Optional[str] = None  # Add subsection field
    thickness: Optional[str] = None  # Add thickness field
    series: Optional[str] = None  # Add series field
    image_url: str
    image_base64: str
    description: str
    features: List[str]
    in_stock: bool
    created_at: str

# Load product data on startup
products_data = []

def load_product_data():
    """Load product data from JSON file"""
    global products_data
    try:
        # Try to load the ultimate catalog first
        ultimate_file = ROOT_DIR.parent / 'bearfoot_ultimate_catalog.json'
        if ultimate_file.exists():
            with open(ultimate_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products_data = [Product(**product) for product in data['products']]
                print(f"Loaded {len(products_data)} products from ultimate catalog")
                return
        
        # Fallback to other files
        products_file = ROOT_DIR.parent / 'bearfoot_final_products.json'
        if products_file.exists():
            with open(products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products_data = [Product(**product) for product in data['products']]
                print(f"Loaded {len(products_data)} products from final catalog")
                return
                
        print("No product data files found")
        products_data = []
    except Exception as e:
        print(f"Error loading product data: {e}")
        products_data = []

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Bearfoot Flooring API", "total_products": len(products_data)}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Product endpoints
@api_router.get("/products", response_model=List[Product])
async def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    product_type: Optional[str] = Query(None, description="Filter by product type"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    search: Optional[str] = Query(None, description="Search in product names"),
    limit: Optional[int] = Query(50, description="Maximum number of products to return")
):
    """Get all products with optional filtering"""
    filtered_products = products_data.copy()
    
    # Apply filters
    if category:
        filtered_products = [p for p in filtered_products if p.category.lower() == category.lower()]
    
    if product_type:
        filtered_products = [p for p in filtered_products if p.product_type.lower() == product_type.lower()]
    
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p.price >= min_price]
    
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p.price <= max_price]
    
    if search:
        search_lower = search.lower()
        filtered_products = [p for p in filtered_products if search_lower in p.name.lower() or search_lower in p.display_name.lower()]
    
    # Apply limit
    if limit:
        filtered_products = filtered_products[:limit]
    
    return filtered_products

@api_router.get("/products/categories")
async def get_categories():
    """Get all available product categories"""
    categories = list(set(p.category for p in products_data))
    return {"categories": categories}

@api_router.get("/products/types")
async def get_product_types():
    """Get all available product types"""
    types = list(set(p.product_type for p in products_data))
    return {"product_types": types}

@api_router.get("/products/search")
async def search_products(q: str = Query(..., description="Search query")):
    """Search products by name, description, or features"""
    if not q:
        return {"products": [], "total": 0}
    
    search_lower = q.lower()
    results = []
    
    for product in products_data:
        # Search in multiple fields
        search_fields = [
            product.name.lower(),
            product.display_name.lower(),
            product.description.lower(),
            product.brand.lower(),
            product.category.lower(),
            product.product_type.lower()
        ]
        
        # Also search in features
        search_fields.extend([feature.lower() for feature in product.features])
        
        if any(search_lower in field for field in search_fields):
            results.append(product)
    
    return {"products": results, "total": len(results), "query": q}

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = next((p for p in products_data if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Load product data on startup"""
    load_product_data()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

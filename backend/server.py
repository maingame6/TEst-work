from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
import json

# Import our models and auth
from models import (
    Product, ProductCreate, ProductUpdate, ProductFilter, 
    AdminUser, AdminUserLogin, Token
)
from auth import (
    authenticate_user, create_access_token, get_current_active_user, 
    create_default_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Tiles & Wood Floor Store API", description="API for tiles and wood flooring products")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()

# AUTHENTICATION ENDPOINTS
@api_router.post("/auth/login", response_model=Token)
async def login(user_credentials: AdminUserLogin):
    user = await authenticate_user(user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/auth/me", response_model=AdminUser)
async def read_users_me(current_user: AdminUser = Depends(get_current_active_user)):
    return current_user

# PRODUCT ENDPOINTS
@api_router.get("/products", response_model=List[Product])
async def get_products(
    supplier: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Get products with optional filtering"""
    query = {}
    
    if supplier:
        query["supplier"] = supplier
    if category:
        query["category"] = category
    if min_price is not None:
        query["price"] = query.get("price", {})
        query["price"]["$gte"] = min_price
    if max_price is not None:
        query["price"] = query.get("price", {})
        query["price"]["$lte"] = max_price
    if in_stock is not None:
        query["in_stock"] = in_stock
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"sku": {"$regex": search, "$options": "i"}}
        ]
    
    products = await db.products.find(query).skip(skip).limit(limit).to_list(length=limit)
    return [Product(**product) for product in products]

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get a specific product by ID"""
    product = await db.products.find_one({"id": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**product)

@api_router.post("/products", response_model=Product)
async def create_product(
    product: ProductCreate,
    current_user: AdminUser = Depends(get_current_active_user)
):
    """Create a new product (admin only)"""
    product_obj = Product(**product.dict())
    await db.products.insert_one(product_obj.dict())
    return product_obj

@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    current_user: AdminUser = Depends(get_current_active_user)
):
    """Update a product (admin only)"""
    existing_product = await db.products.find_one({"id": product_id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.products.update_one({"id": product_id}, {"$set": update_data})
    updated_product = await db.products.find_one({"id": product_id})
    return Product(**updated_product)

@api_router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: AdminUser = Depends(get_current_active_user)
):
    """Delete a product (admin only)"""
    result = await db.products.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# CATEGORY AND SUPPLIER ENDPOINTS
@api_router.get("/suppliers")
async def get_suppliers():
    """Get all unique suppliers"""
    suppliers = await db.products.distinct("supplier")
    return {"suppliers": suppliers}

@api_router.get("/categories")
async def get_categories():
    """Get all unique categories"""
    categories = await db.products.distinct("category")
    return {"categories": categories}

# STATISTICS ENDPOINT
@api_router.get("/admin/stats")
async def get_admin_stats(current_user: AdminUser = Depends(get_current_active_user)):
    """Get admin statistics"""
    total_products = await db.products.count_documents({})
    in_stock_products = await db.products.count_documents({"in_stock": True})
    suppliers = await db.products.distinct("supplier")
    categories = await db.products.distinct("category")
    
    return {
        "total_products": total_products,
        "in_stock_products": in_stock_products,
        "out_of_stock_products": total_products - in_stock_products,
        "total_suppliers": len(suppliers),
        "total_categories": len(categories),
        "suppliers": suppliers,
        "categories": categories
    }

# HEALTH CHECK
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Tiles & Wood Floor Store API is running"}

# Include the router in the main app
app.include_router(api_router)

# CORS middleware
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
    """Initialize the application"""
    logger.info("Starting Tiles & Wood Floor Store API")
    
    # Create default admin user
    await create_default_admin()
    
    # Run data migration if no products exist
    products_count = await db.products.count_documents({})
    if products_count == 0:
        logger.info("No products found. Running data migration...")
        try:
            from data_migration import migrate_products
            await migrate_products()
            logger.info("Data migration completed successfully")
        except Exception as e:
            logger.error(f"Data migration failed: {e}")
    
    logger.info("API startup completed")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

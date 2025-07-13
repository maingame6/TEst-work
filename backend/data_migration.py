import json
import asyncio
import base64
import os
from motor.motor_asyncio import AsyncIOMotorClient
from models import Product
from datetime import datetime
from parse_products import get_twfsfitting_products_from_curl

# Database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def parse_twfsfitting_products():
    """Parse products from the scraped twfsfitting.co.uk data"""
    try:
        products_data = get_twfsfitting_products_from_curl()
        products = []
        
        for product_data in products_data:
            product = Product(
                supplier=product_data["supplier"],
                name=product_data["name"],
                sku=product_data["sku"],
                tile_size=product_data["tile_size"],
                box_size=product_data["box_size"],
                price=product_data["price"],
                category=product_data["category"],
                description=product_data["description"],
                in_stock=product_data["in_stock"]
            )
            products.append(product)
        
        return products
    except Exception as e:
        print(f"Error parsing twfsfitting products: {e}")
        return []

def parse_tileswoodfloorni_products():
    """Parse products from the scraped tileswoodfloorni.com data"""
    products = []
    
    try:
        # Load the scraped data
        with open('/app/tileswoodfloorni_final_dataset.json', 'r') as f:
            data = json.load(f)
        
        # Extract company info
        company_info = data.get('company_info', {})
        company_name = company_info.get('name', 'Tiles & Wood Floor Store')
        
        # Process products from the scraped data
        scraped_products = data.get('products', [])
        
        # Create some sample products based on the category data
        categories = data.get('product_categories', {})
        
        # Create products for tiles
        tile_categories = categories.get('tiles', [])
        for i, tile_type in enumerate(tile_categories):
            product = Product(
                supplier=company_name,
                name=f"{tile_type} Tiles",
                sku=f"TWF-TILE-{i+1:03d}",
                tile_size="600x600",
                box_size=1.44,
                price=35.99 + (i * 5),  # Variable pricing
                category="Tiles",
                description=f"Premium {tile_type.lower()} tiles from {company_name}",
                in_stock=True
            )
            products.append(product)
        
        # Create products for flooring
        flooring_categories = categories.get('flooring', [])
        for i, flooring_type in enumerate(flooring_categories):
            product = Product(
                supplier=company_name,
                name=f"{flooring_type} Flooring",
                sku=f"TWF-FLOOR-{i+1:03d}",
                tile_size="1200x200",
                box_size=2.16,
                price=45.99 + (i * 8),  # Variable pricing
                category="Flooring",
                description=f"High-quality {flooring_type.lower()} flooring from {company_name}",
                in_stock=True
            )
            products.append(product)
        
        # Create products for different rooms
        room_categories = categories.get('rooms', [])
        for i, room_type in enumerate(room_categories):
            product = Product(
                supplier=company_name,
                name=f"{room_type} Specialty Tiles",
                sku=f"TWF-ROOM-{i+1:03d}",
                tile_size="300x300",
                box_size=1.08,
                price=29.99 + (i * 3),  # Variable pricing
                category=f"{room_type} Tiles",
                description=f"Perfect tiles for {room_type.lower()} applications from {company_name}",
                in_stock=True
            )
            products.append(product)
    
    except Exception as e:
        print(f"Error parsing tileswoodfloorni data: {e}")
    
    return products

async def migrate_products():
    """Migrate all products to the database"""
    try:
        # Clear existing products
        await db.products.delete_many({})
        print("Cleared existing products")
        
        # Parse and migrate products from both sources
        twfsfitting_products = parse_twfsfitting_products()
        tileswoodfloorni_products = parse_tileswoodfloorni_products()
        
        all_products = twfsfitting_products + tileswoodfloorni_products
        
        # Insert products into database
        for product in all_products:
            await db.products.insert_one(product.dict())
        
        print(f"Successfully migrated {len(all_products)} products:")
        print(f"- {len(twfsfitting_products)} from twfsfitting.co.uk")
        print(f"- {len(tileswoodfloorni_products)} from tileswoodfloorni.com")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        raise

async def main():
    """Main migration function"""
    await migrate_products()
    client.close()

if __name__ == "__main__":
    asyncio.run(main())
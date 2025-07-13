import json
import asyncio
import base64
import os
from motor.motor_asyncio import AsyncIOMotorClient
from models import Product
from datetime import datetime

# Database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def parse_twfsfitting_products():
    """Parse products from the scraped twfsfitting.co.uk data"""
    products = []
    
    # Sample data from the scraped HTML - would need to be parsed from actual HTML
    # This is the structure from the curl response
    sample_products = [
        {
            "supplier": "Bearfoot",
            "name": "10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank",
            "sku": "L915",
            "tile_size": "nan",
            "box_size": 1.8,
            "price": 66.66
        },
        {
            "supplier": "Bearfoot",
            "name": "10mm XT+ BERGEN OAK GREY 1.8m2 D4792 long plank",
            "sku": "L913",
            "tile_size": "nan",
            "box_size": 1.8,
            "price": 66.66
        },
        {
            "supplier": "Bearfoot",
            "name": "10mm XT+ CASTLE OAK SILVER 1.8m2 D4797 long plank",
            "sku": "L914",
            "tile_size": "nan",
            "box_size": 1.8,
            "price": 66.66
        }
    ]
    
    for product_data in sample_products:
        product = Product(
            supplier=product_data["supplier"],
            name=product_data["name"],
            sku=product_data["sku"],
            tile_size=product_data["tile_size"] if product_data["tile_size"] != "nan" else None,
            box_size=product_data["box_size"] if product_data["box_size"] != 0.0 else None,
            price=product_data["price"],
            category="Flooring",
            description=f"High-quality flooring from {product_data['supplier']}",
            in_stock=True
        )
        products.append(product)
    
    return products

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
        
        for i, product_data in enumerate(scraped_products):
            if product_data.get('type') == 'gallery_product':
                product = Product(
                    supplier=company_name,
                    name=product_data.get('name', f"Product {i+1}"),
                    sku=f"TWF{product_data.get('id', i+1)}",
                    tile_size=None,
                    box_size=None,
                    price=50.0,  # Default price as not in scraped data
                    category=product_data.get('category', 'Tiles'),
                    description=f"Premium {product_data.get('category', 'tiles')} from {company_name}",
                    in_stock=True
                )
                products.append(product)
            elif product_data.get('type') == 'extracted_from_content':
                # Create products from content mentions
                product = Product(
                    supplier=company_name,
                    name=product_data.get('name', f"Product {i+1}"),
                    sku=f"TWF-EXT-{i+1}",
                    tile_size=None,
                    box_size=None,
                    price=45.0,
                    category="General",
                    description=f"Quality flooring and tiles from {company_name}",
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
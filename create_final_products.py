#!/usr/bin/env python3
"""
Create final matched product data with proper images
"""

import json
import requests
import base64
import time
from typing import List, Dict

def download_image_as_base64(image_url: str) -> str:
    """Download image and convert to base64"""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Get the image content and encode as base64
        image_content = response.content
        base64_content = base64.b64encode(image_content).decode('utf-8')
        
        # Determine the MIME type
        content_type = response.headers.get('content-type', 'image/jpeg')
        
        # Return data URL format
        return f"data:{content_type};base64,{base64_content}"
        
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")
        return None

def get_provided_product_data():
    """Parse the provided product data into structured format"""
    product_text = """Bearfoot 10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank L915 nan 1.8 66.66
Bearfoot 10mm XT+ BERGEN OAK GREY 1.8m2 D4792 long plank L913 nan 1.8 66.66
Bearfoot 10mm XT+ CASTLE OAK SILVER 1.8m2 D4797 long plank L914 nan 1.8 66.66
Bearfoot 10mm XT+ OAK BROWN D1010 1.8m2 long plank (d4791) L918 nan 1.8 66.66
Bearfoot 10mm XT+ OAK CREME D1031 1.8m2 long plank (d40752) L921 nan 1.8 73.92
Bearfoot 10mm XT+ OAK LIGHT D1012 1.8m2 long plank L919 nan 1.8 73.92
Bearfoot 10mm XT+ OAK NATURE D1008 1.8m2 long plank (d4794) L917 nan 1.8 66.66
Bearfoot 12mm ALICANTE X-LOC HERRINGBONE LAMINATE 1.20m2 H954 nan 1.2 61.2
Bearfoot 12mm BELGIAN BEIGE D3081- 1.387M2 LONG PLANK (PROV) L908 nan 1.387 54.08
Bearfoot 12mm BELGIAN BROWN D3076 1.387m2 LONG PLANK (PHOENIX) L909 nan 1.387 54.08
Bearfoot 12mm CASTLE ORIGINAL D4752 1.387m2 LONG PLANK L920 nan 1.387 54.08
Bearfoot 12mm CASTLE SILVER D4797 1.387m2 LONG PLANK (LINC) L906 nan 1.387 54.08
Bearfoot 12mm CORK X-LOC HERRINGBONE LAMINATE 1.20m2 H955 nan 1.2 61.2
Bearfoot 12mm GALWAY X-LOC HERRINGBONE LAMINATE 1.20m2 H950 nan 1.2 61.2
Bearfoot 12mm GLASGOW X-LOC HERRINGBONE LAMINATE 1.20m2 H957 nan 1.2 61.2
Bearfoot 12mm JAIPUR X-LOC HERRINGBONE LAMINATE 1.20m2 H951 nan 1.2 61.2
Bearfoot 12mm NOTTINGHAM X-LOC HERRINGBONE LAMINATE 1.20m2 H953 nan 1.2 61.2
Bearfoot 12mm OBAN X-LOC HERRINGBONE LAMINATE 1.20m2 H956 nan 1.2 61.2
Bearfoot 12mm SYMPHONIA ALLEGRO AQUA ZERO D40244 1.32M2 (60) L159 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA FORTE AQUA ZERO D40074 1.32M2 (60) L158 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA LARGO AQUA ZERO D4526 1.32M2 (60) L150 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA LEGATO AQUA ZERO D4528 1.32M2 (60) L152 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA PRESTO AQUA ZERO D4530 1.32M2 (60) L154 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA SOLO AQUA ZERO D4529 1.32M2 (60) L153 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA SONATA AQUA ZERO D4531 1.32M2 (60) L155 nan 1.32 45.72
Bearfoot 12mm SYMPHONIA VIVO AQUA ZERO D4527 1.32M2 (60) L151 nan 1.32 45.72
Bearfoot 12mm VICENCE X-LOC HERRINGBONE LAMINATE 1.20m2 H952 nan 1.2 61.2"""
    
    products = []
    
    # Professional laminate flooring images from vision expert
    image_urls = [
        "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwxfHxsYW1pbmF0ZSUyMGZsb29yaW5nfGVufDB8fHx8MTc1MjM2Mjc2N3ww&ixlib=rb-4.1.0&q=85",
        "https://images.unsplash.com/photo-1519393890420-f28727375fa5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwyfHxsYW1pbmF0ZSUyMGZsb29yaW5nfGVufDB8fHx8MTc1MjM2Mjc2N3ww&ixlib=rb-4.1.0&q=85",
        "https://images.unsplash.com/photo-1575204015311-0fe377370780?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Nzh8MHwxfHNlYXJjaHwzfHxsYW1pbmF0ZSUyMGZsb29yaW5nfGVufDB8fHx8MTc1MjM2Mjc2N3ww&ixlib=rb-4.1.0&q=85",
        "https://images.pexels.com/photos/1249611/pexels-photo-1249611.jpeg",
        "https://images.pexels.com/photos/3935340/pexels-photo-3935340.jpeg"
    ]
    
    # Download all images as base64
    print("Downloading professional laminate flooring images...")
    image_base64_list = []
    for url in image_urls:
        print(f"Downloading: {url}")
        base64_image = download_image_as_base64(url)
        if base64_image:
            image_base64_list.append(base64_image)
        time.sleep(0.5)  # Be respectful
    
    print(f"Successfully downloaded {len(image_base64_list)} images")
    
    # Parse products and assign images
    lines = product_text.strip().split('\n')
    
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        
        # Split by spaces and try to extract components
        parts = line.strip().split()
        
        if len(parts) < 3:
            continue
            
        # The last part should be the price
        try:
            price = float(parts[-1])
        except ValueError:
            continue
            
        # The second to last should be the area (m2)
        try:
            area = float(parts[-2])
        except ValueError:
            area = None
            
        # Everything before the area and price is the product name
        if area:
            name_parts = parts[:-2]
        else:
            name_parts = parts[:-1]
            
        name = ' '.join(name_parts)
        
        # Extract product details
        product_id = f"bearfoot_{i+1:03d}"
        
        # Extract product code if present
        product_code = None
        import re
        code_match = re.search(r'\b([DLH]\d{3,4})\b', name)
        if code_match:
            product_code = code_match.group(1)
            
        # Extract dimensions if present
        dimensions = None
        dim_match = re.search(r'(\d+)mm', name)
        if dim_match:
            dimensions = f"{dim_match.group(1)}mm"
            
        # Extract type (long plank, herringbone, etc.)
        product_type = "Long Plank"
        if "HERRINGBONE" in name.upper():
            product_type = "Herringbone"
        elif "X-LOC" in name.upper():
            product_type = "X-LOC"
            
        # Assign image based on product characteristics
        image_index = i % len(image_base64_list)  # Distribute images evenly
        
        # For specific colors, try to match appropriate images
        if "BEIGE" in name.upper() or "LIGHT" in name.upper():
            image_index = 2  # Light colored flooring
        elif "GREY" in name.upper() or "GRAY" in name.upper():
            image_index = 1  # Grey laminate planks
        elif "BROWN" in name.upper() or "DARK" in name.upper():
            image_index = 0  # Modern dark flooring
        elif "HERRINGBONE" in name.upper():
            image_index = 3  # Professional installation
        else:
            image_index = 4  # Clean room interior
            
        # Ensure we don't go out of bounds
        image_index = image_index % len(image_base64_list)
        
        product = {
            'id': product_id,
            'name': name,
            'display_name': name.replace('Bearfoot ', ''),
            'price': price,
            'area_m2': area,
            'product_code': product_code,
            'dimensions': dimensions,
            'product_type': product_type,
            'brand': 'Bearfoot',
            'category': 'Laminate Flooring',
            'image_url': image_urls[image_index],
            'image_base64': image_base64_list[image_index],
            'description': f"High-quality {product_type.lower()} laminate flooring with premium finish and easy installation.",
            'features': [
                "Water resistant",
                "Easy click installation", 
                "Scratch resistant surface",
                "Realistic wood grain texture"
            ],
            'in_stock': True,
            'created_at': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        products.append(product)
        
    return products

def main():
    """Create final product data with images"""
    products = get_provided_product_data()
    
    output_data = {
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": "Bearfoot product data with professional images",
        "total_products": len(products),
        "image_source": "Professional laminate flooring images from Unsplash/Pexels",
        "products": products
    }
    
    # Save the final data
    with open('/app/bearfoot_final_products.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
        
    print(f"Created final product data with {len(products)} products")
    print("Saved to: /app/bearfoot_final_products.json")
    
    # Create a summary
    print("\nProduct Summary:")
    for i, product in enumerate(products[:5]):
        print(f"{i+1}. {product['display_name']} - €{product['price']:.2f}")
    print(f"... and {len(products)-5} more products")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Enhanced scraper to extract better product information from the JavaScript
"""

import json
import re
import subprocess
from urllib.parse import urljoin
import time
import base64
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_product_data_from_js(js_content):
    """Enhanced extraction of product data from JavaScript"""
    products = []
    
    # Look for the gallery data array (gn) which contains product information
    gallery_pattern = r'gn=(\[[\s\S]*?\])'
    match = re.search(gallery_pattern, js_content)
    
    if match:
        gallery_data = match.group(1)
        
        # Extract individual product objects
        product_pattern = r'\{[^}]*id:\s*(\d+)[^}]*category:\s*"([^"]*)"[^}]*url:\s*[^,]+\.([^,]+)[^}]*alt:\s*"([^"]*)"[^}]*\}'
        
        products_raw = re.findall(product_pattern, gallery_data, re.DOTALL)
        
        for product_raw in products_raw:
            product_id, category, file_ext, alt_text = product_raw
            
            # Extract the actual image URL pattern
            url_pattern = r'url:\s*([^,]+\.' + file_ext + r')'
            url_match = re.search(url_pattern, gallery_data)
            
            product = {
                'id': product_id,
                'category': category,
                'alt_text': alt_text,
                'file_extension': file_ext,
                'type': 'gallery_product'
            }
            
            products.append(product)
    
    # Also look for other product data patterns
    # Product arrays or objects
    other_patterns = [
        r'all_product\s*[:=]\s*(\[[\s\S]*?\])',
        r'products\s*[:=]\s*(\[[\s\S]*?\])',
        r'productData\s*[:=]\s*(\[[\s\S]*?\])',
    ]
    
    for pattern in other_patterns:
        matches = re.findall(pattern, js_content, re.IGNORECASE)
        for match in matches:
            # Try to extract product names from the match
            name_matches = re.findall(r'name\s*:\s*["\']([^"\']{3,})["\']', match, re.IGNORECASE)
            for name in name_matches:
                if len(name) > 2 and len(name) < 100:
                    products.append({
                        'name': name,
                        'type': 'js_product_data'
                    })
    
    return products

def get_js_content():
    """Get the main JavaScript file content"""
    js_url = "https://tileswoodfloorni.com/static/js/main.46874d7f.js"
    
    try:
        cmd = [
            'curl', '-k', '-L', 
            '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            js_url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Failed to get JS content: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error getting JS content: {e}")
        return None

def extract_image_urls_from_js(js_content):
    """Extract image URLs from JavaScript content"""
    images = []
    
    # Pattern for static media files
    static_pattern = r'static/media/[^"\']+\.(jpg|jpeg|png|webp|gif)'
    matches = re.findall(static_pattern, js_content, re.IGNORECASE)
    
    for match in matches:
        if isinstance(match, tuple):
            # Take the full match (not just the extension)
            full_match = re.search(static_pattern, js_content).group(0)
            image_url = f"https://tileswoodfloorni.com/{full_match}"
        else:
            image_url = f"https://tileswoodfloorni.com/{match}"
        
        if image_url not in images:
            images.append(image_url)
    
    # Also look for direct image references
    image_patterns = [
        r'"([^"]*\.(jpg|jpeg|png|webp|gif))"',
        r"'([^']*\.(jpg|jpeg|png|webp|gif))'",
    ]
    
    for pattern in image_patterns:
        matches = re.findall(pattern, js_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                image_url = match[0]
            else:
                image_url = match
            
            if not image_url.startswith('http'):
                if image_url.startswith('/'):
                    image_url = f"https://tileswoodfloorni.com{image_url}"
                else:
                    image_url = f"https://tileswoodfloorni.com/{image_url}"
            
            if image_url not in images:
                images.append(image_url)
    
    return list(set(images))

def enhance_product_data():
    """Enhanced product data extraction"""
    print("Getting enhanced product data...")
    
    js_content = get_js_content()
    if not js_content:
        print("Failed to get JavaScript content")
        return
    
    # Extract products and images
    products = extract_product_data_from_js(js_content)
    images = extract_image_urls_from_js(js_content)
    
    print(f"Found {len(products)} products from enhanced extraction")
    print(f"Found {len(images)} images from enhanced extraction")
    
    # Create enhanced data structure
    enhanced_data = {
        'products': products,
        'images': images,
        'metadata': {
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'tileswoodfloorni.com',
            'method': 'enhanced_js_analysis',
            'ssl_bypassed': True
        }
    }
    
    # Save enhanced data
    with open('/app/enhanced_tileswoodfloorni_data.json', 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print("Enhanced data saved to enhanced_tileswoodfloorni_data.json")
    
    # Print some examples
    print("\nProduct examples:")
    for i, product in enumerate(products[:10]):
        if 'name' in product:
            print(f"  {i+1}. {product['name']} ({product['type']})")
        else:
            print(f"  {i+1}. Category: {product.get('category', 'N/A')}, Alt: {product.get('alt_text', 'N/A')}")

if __name__ == "__main__":
    enhance_product_data()
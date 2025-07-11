#!/usr/bin/env python3
"""
Final comprehensive scraper that combines all extracted data
"""

import json
import subprocess
import time
import base64
import requests
import urllib3
from urllib.parse import urljoin

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_image(url, session):
    """Download a single image and convert to base64"""
    try:
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            # Convert to base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            
            # Determine file type
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                mime_type = 'image/jpeg'
            elif 'png' in content_type:
                mime_type = 'image/png'
            elif 'webp' in content_type:
                mime_type = 'image/webp'
            else:
                # Try to determine from URL
                if '.png' in url.lower():
                    mime_type = 'image/png'
                elif '.webp' in url.lower():
                    mime_type = 'image/webp'
                else:
                    mime_type = 'image/jpeg'
            
            return {
                'url': url,
                'base64': f"data:{mime_type};base64,{image_data}",
                'size': len(response.content),
                'mime_type': mime_type,
                'filename': url.split('/')[-1]
            }
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def create_final_dataset():
    """Create the final comprehensive dataset"""
    print("Creating final comprehensive dataset...")
    
    # Load both data files
    try:
        with open('/app/tileswoodfloorni_scraped_data.json', 'r') as f:
            basic_data = json.load(f)
        
        with open('/app/enhanced_tileswoodfloorni_data.json', 'r') as f:
            enhanced_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return
    
    # Combine all unique images
    all_images = set()
    all_images.update(basic_data.get('images', []))
    all_images.update(enhanced_data.get('images', []))
    all_images = list(all_images)
    
    # Combine products
    all_products = []
    all_products.extend(basic_data.get('products', []))
    all_products.extend(enhanced_data.get('products', []))
    
    # Create session for downloading
    session = requests.Session()
    session.verify = False
    
    # Download all images
    print(f"Downloading {len(all_images)} images...")
    downloaded_images = []
    
    for i, url in enumerate(all_images):
        print(f"Downloading {i+1}/{len(all_images)}: {url}")
        result = download_image(url, session)
        if result:
            downloaded_images.append(result)
    
    # Create comprehensive dataset
    final_data = {
        'metadata': {
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source_website': 'tileswoodfloorni.com',
            'ssl_bypassed': True,
            'total_images': len(all_images),
            'successfully_downloaded': len(downloaded_images),
            'total_products': len(all_products),
            'scraping_method': 'comprehensive_curl_based_with_js_analysis'
        },
        'company_info': {
            'name': 'Tiles & Wood Floor Store',
            'locations': ['Bangor', 'Ballymena'],
            'country': 'Northern Ireland',
            'services': ['Tiles', 'Laminate Flooring', 'Real Wood Flooring', 'LVT'],
            'phone': '02891225400',
            'email': 'sales@tileswoodfloorni.com'
        },
        'product_categories': {
            'tiles': ['Ceramic', 'Porcelain', 'Natural Stone', 'Kitchen Tiles', 'Wall Tiles', 'Vintage Tiles'],
            'flooring': ['Laminate', 'Real Wood', 'LVT', 'Vinyl'],
            'rooms': ['Kitchen', 'Bathroom', 'Living Room', 'Bedroom', 'Hallway', 'Stairs']
        },
        'products': all_products,
        'images': {
            'total_found': len(all_images),
            'successfully_downloaded': len(downloaded_images),
            'image_urls': all_images,
            'downloaded_images': downloaded_images
        }
    }
    
    # Save the final dataset
    with open('/app/tileswoodfloorni_final_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"Final dataset saved to tileswoodfloorni_final_dataset.json")
    print(f"Total images downloaded: {len(downloaded_images)}")
    print(f"Total products found: {len(all_products)}")
    
    # Create a summary report
    create_summary_report(final_data)

def create_summary_report(data):
    """Create a human-readable summary report"""
    report = f"""
TILESWOODFLOORNI.COM SCRAPING REPORT
===================================

Scraped: {data['metadata']['scraped_at']}
Source: {data['metadata']['source_website']}

COMPANY INFORMATION:
- Name: {data['company_info']['name']}
- Locations: {', '.join(data['company_info']['locations'])}
- Country: {data['company_info']['country']}
- Phone: {data['company_info']['phone']}
- Email: {data['company_info']['email']}

SERVICES:
{chr(10).join(f"- {service}" for service in data['company_info']['services'])}

PRODUCT CATEGORIES:
- Tiles: {', '.join(data['product_categories']['tiles'])}
- Flooring: {', '.join(data['product_categories']['flooring'])}
- Rooms: {', '.join(data['product_categories']['rooms'])}

SCRAPING RESULTS:
- Total Images Found: {data['images']['total_found']}
- Successfully Downloaded: {data['images']['successfully_downloaded']}
- Total Products Found: {data['metadata']['total_products']}

IMAGES DOWNLOADED:
"""
    
    for i, img in enumerate(data['images']['downloaded_images'][:20]):  # Show first 20
        report += f"- {i+1}. {img['filename']} ({img['mime_type']}, {img['size']} bytes)\n"
    
    if len(data['images']['downloaded_images']) > 20:
        report += f"... and {len(data['images']['downloaded_images']) - 20} more images\n"
    
    report += f"""
PRODUCT EXAMPLES:
"""
    
    for i, product in enumerate(data['products'][:10]):  # Show first 10
        if 'name' in product:
            report += f"- {i+1}. {product['name']} ({product['type']})\n"
        else:
            report += f"- {i+1}. Category: {product.get('category', 'N/A')}, ID: {product.get('id', 'N/A')}\n"
    
    report += f"""
TECHNICAL DETAILS:
- SSL Certificate: Bypassed (expired certificate)
- Scraping Method: {data['metadata']['scraping_method']}
- Data Format: JSON with base64 encoded images
- Total File Size: Approximately {sum(img['size'] for img in data['images']['downloaded_images']) / 1024 / 1024:.2f} MB

This dataset contains all product images and information scraped from tileswoodfloorni.com
and is ready for upload to another agent or system.
"""
    
    with open('/app/tileswoodfloorni_scraping_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Summary report saved to tileswoodfloorni_scraping_report.txt")

if __name__ == "__main__":
    create_final_dataset()
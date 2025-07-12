#!/usr/bin/env python3
"""
Bearfoot Laminate Scraper
Scrapes product images and details from https://www.bearfoot.ie/floors/laminates/
"""

import requests
import json
import base64
import re
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os

class BearfootScraper:
    def __init__(self):
        self.base_url = "https://www.bearfoot.ie"
        self.laminate_url = "https://www.bearfoot.ie/floors/laminates/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def get_page_content(self, url: str) -> Optional[str]:
        """Get page content with retry logic"""
        try:
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
            
    def download_image_as_base64(self, image_url: str) -> Optional[str]:
        """Download image and convert to base64"""
        try:
            # Make sure it's a full URL
            if not image_url.startswith('http'):
                image_url = urljoin(self.base_url, image_url)
                
            response = self.session.get(image_url, timeout=30, verify=False)
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
            
    def clean_product_name(self, name: str) -> str:
        """Clean and standardize product names for matching"""
        # Remove extra spaces and normalize
        name = ' '.join(name.split())
        # Remove common prefixes like "Bearfoot"
        name = re.sub(r'^Bearfoot\s+', '', name, flags=re.IGNORECASE)
        return name.strip()
        
    def scrape_laminate_products(self) -> List[Dict]:
        """Scrape laminate products from Bearfoot website"""
        print("Starting Bearfoot laminate scraping...")
        
        content = self.get_page_content(self.laminate_url)
        if not content:
            print("Failed to get laminate page content")
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        
        # Look for different possible product containers
        product_selectors = [
            '.product-item',
            '.product',
            '.product-card',
            '.product-grid-item',
            '.item',
            '.product-container',
            '[data-product]',
            '.woocommerce-LoopProduct-link',
            '.product-inner',
            'article'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} products using selector: {selector}")
                product_elements = elements
                break
                
        if not product_elements:
            # Fallback: look for any elements with product images
            print("No standard product containers found, looking for images...")
            img_elements = soup.find_all('img', src=True)
            
            for img in img_elements:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                # Skip logos, icons, etc.
                if any(skip in src.lower() for skip in ['logo', 'icon', 'button', 'arrow']):
                    continue
                    
                if any(skip in alt.lower() for skip in ['logo', 'icon', 'button', 'arrow']):
                    continue
                    
                # Look for product-like images
                if any(prod in src.lower() for prod in ['product', 'floor', 'laminate']) or \
                   any(prod in alt.lower() for prod in ['laminate', 'floor', 'oak', 'wood']):
                    
                    product_name = alt or 'Unknown Product'
                    product_name = self.clean_product_name(product_name)
                    
                    image_base64 = self.download_image_as_base64(src)
                    if image_base64:
                        products.append({
                            'name': product_name,
                            'image_url': src,
                            'image_base64': image_base64,
                            'source': 'bearfoot_laminate'
                        })
                        print(f"Added product: {product_name}")
                        time.sleep(0.5)  # Be respectful
                        
        else:
            # Process structured product elements
            for element in product_elements:
                try:
                    # Extract product name
                    name_selectors = [
                        '.product-title',
                        '.product-name',
                        'h2', 'h3', 'h4',
                        '.title',
                        '.name',
                        'a[title]'
                    ]
                    
                    product_name = None
                    for name_sel in name_selectors:
                        name_elem = element.select_one(name_sel)
                        if name_elem:
                            product_name = name_elem.get_text(strip=True) or name_elem.get('title', '')
                            break
                            
                    if not product_name:
                        continue
                        
                    product_name = self.clean_product_name(product_name)
                    
                    # Extract product image
                    img_selectors = [
                        'img',
                        '.product-image img',
                        '.product-img img',
                        '.image img'
                    ]
                    
                    image_url = None
                    for img_sel in img_selectors:
                        img_elem = element.select_one(img_sel)
                        if img_elem:
                            image_url = img_elem.get('src') or img_elem.get('data-src')
                            break
                            
                    if not image_url:
                        continue
                        
                    # Download and convert image
                    image_base64 = self.download_image_as_base64(image_url)
                    if image_base64:
                        products.append({
                            'name': product_name,
                            'image_url': image_url,
                            'image_base64': image_base64,
                            'source': 'bearfoot_laminate'
                        })
                        print(f"Added product: {product_name}")
                        time.sleep(0.5)  # Be respectful
                        
                except Exception as e:
                    print(f"Error processing product element: {e}")
                    continue
                    
        print(f"Successfully scraped {len(products)} products")
        return products
        
    def save_products(self, products: List[Dict], filename: str = "bearfoot_laminate_products.json"):
        """Save scraped products to JSON file"""
        output_data = {
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "bearfoot.ie/floors/laminates/",
            "total_products": len(products),
            "products": products
        }
        
        filepath = os.path.join('/app', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(products)} products to {filepath}")
        return filepath

def main():
    """Main scraping function"""
    scraper = BearfootScraper()
    products = scraper.scrape_laminate_products()
    
    if products:
        filepath = scraper.save_products(products)
        print(f"Scraping completed. Products saved to: {filepath}")
    else:
        print("No products found or scraping failed")

if __name__ == "__main__":
    main()
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
        
    def get_category_links(self) -> List[str]:
        """Get category links from the main laminate page"""
        print("Getting category links from main laminate page...")
        
        # Known category links from the crawl data
        known_categories = [
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-quatro/",
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-king-floor/", 
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-sound/",
            "https://www.bearfoot.ie/floors/laminates/12mm/xtreme-long-plank/",
            "https://www.bearfoot.ie/floors/laminates/10mm/krono-marine/",
            "https://www.bearfoot.ie/floors/laminates/10mm/krono-aroma/",
            "https://www.bearfoot.ie/floors/laminates/10mm/xtreme-wide-and-long/",
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-sigma/",
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-exclusive/",
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-testa/"
        ]
        
        # Also try to scrape for additional links
        content = self.get_page_content(self.laminate_url)
        additional_links = []
        
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                if '/floors/laminates/' in href and href not in known_categories:
                    full_url = urljoin(self.base_url, href)
                    additional_links.append(full_url)
                    
        all_links = known_categories + additional_links
        all_links = list(set(all_links))  # Remove duplicates
        print(f"Found {len(all_links)} category links")
        
        return all_links
        
    def scrape_category_page(self, category_url: str) -> List[Dict]:
        """Scrape products from a specific category page"""
        print(f"Scraping category: {category_url}")
        
        content = self.get_page_content(category_url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        
        # Look for product images and names on the category page
        img_elements = soup.find_all('img', src=True)
        
        for img in img_elements:
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Skip logos, icons, etc.
            if any(skip in src.lower() for skip in ['logo', 'icon', 'button', 'arrow', 'banner']):
                continue
                
            # Look for product-like images
            if any(prod in src.lower() for prod in ['floor', 'laminate', 'wood', 'oak', 'plank']):
                product_name = alt or 'Unknown Product'
                
                # Try to get a better product name from nearby elements
                parent = img.parent
                if parent:
                    # Look for text in the same container
                    text_elements = parent.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span'])
                    for text_elem in text_elements:
                        text = text_elem.get_text(strip=True)
                        if text and len(text) > len(product_name) and any(wood in text.lower() for wood in ['oak', 'beige', 'brown', 'grey', 'wood', 'plank']):
                            product_name = text
                            break
                
                product_name = self.clean_product_name(product_name)
                
                if len(product_name) > 3:  # Skip very short names
                    image_base64 = self.download_image_as_base64(src)
                    if image_base64:
                        products.append({
                            'name': product_name,
                            'image_url': src,
                            'image_base64': image_base64,
                            'source': f'bearfoot_category_{category_url.split("/")[-2] if category_url.endswith("/") else category_url.split("/")[-1]}',
                            'category_url': category_url
                        })
                        print(f"  Added product: {product_name}")
                        time.sleep(0.3)  # Be respectful
                        
        return products
        
    def scrape_laminate_products(self) -> List[Dict]:
        """Scrape laminate products from Bearfoot website"""
        print("Starting Bearfoot laminate scraping...")
        
        all_products = []
        
        # First get category links
        category_links = self.get_category_links()
        
        if not category_links:
            print("No category links found, trying direct scraping...")
            # Fallback to direct scraping
            content = self.get_page_content(self.laminate_url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                img_elements = soup.find_all('img', src=True)
                
                for img in img_elements:
                    src = img.get('src', '')
                    alt = img.get('alt', '')
                    
                    if any(prod in src.lower() for prod in ['floor', 'laminate', 'wood', 'oak']):
                        product_name = alt or 'Unknown Product'
                        product_name = self.clean_product_name(product_name)
                        
                        if len(product_name) > 3:
                            image_base64 = self.download_image_as_base64(src)
                            if image_base64:
                                all_products.append({
                                    'name': product_name,
                                    'image_url': src,
                                    'image_base64': image_base64,
                                    'source': 'bearfoot_main'
                                })
                                print(f"Added product: {product_name}")
                                time.sleep(0.3)
        else:
            # Scrape each category page
            for category_url in category_links[:10]:  # Limit to first 10 categories
                category_products = self.scrape_category_page(category_url)
                all_products.extend(category_products)
                time.sleep(1)  # Be respectful between category requests
                
        print(f"Successfully scraped {len(all_products)} products total")
        return all_products
        
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
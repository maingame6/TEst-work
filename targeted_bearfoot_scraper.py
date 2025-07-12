#!/usr/bin/env python3
"""
Enhanced Bearfoot Scraper - Search for specific product names
"""

import requests
import json
import base64
import re
import time
from urllib.parse import urljoin, urlparse, quote_plus
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os

class EnhancedBearfootScraper:
    def __init__(self):
        self.base_url = "https://www.bearfoot.ie"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Extract product names from the provided data
        self.target_products = self.get_target_product_names()
        
    def get_target_product_names(self) -> List[str]:
        """Extract the key product names we're looking for"""
        provided_data = """Bearfoot 10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank L915 nan 1.8 66.66
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
        for line in provided_data.strip().split('\n'):
            if not line.strip():
                continue
            
            # Extract key search terms from each product name
            # Remove common prefixes and extract the main product name
            name = line.replace('Bearfoot', '').strip()
            
            # Extract key terms like BERGEN BEIGE, OAK BROWN, etc.
            search_terms = []
            
            # Look for specific patterns
            if 'BERGEN BEIGE' in name:
                search_terms = ['BERGEN', 'BEIGE']
            elif 'BERGEN OAK GREY' in name:
                search_terms = ['BERGEN', 'GREY', 'GRAY']
            elif 'CASTLE OAK SILVER' in name:
                search_terms = ['CASTLE', 'SILVER']
            elif 'OAK BROWN' in name:
                search_terms = ['OAK', 'BROWN']
            elif 'OAK CREME' in name:
                search_terms = ['OAK', 'CREME', 'CREAM']
            elif 'OAK LIGHT' in name:
                search_terms = ['OAK', 'LIGHT']
            elif 'OAK NATURE' in name:
                search_terms = ['OAK', 'NATURE', 'NATURAL']
            elif 'ALICANTE' in name:
                search_terms = ['ALICANTE']
            elif 'BELGIAN BEIGE' in name:
                search_terms = ['BELGIAN', 'BEIGE']
            elif 'BELGIAN BROWN' in name:
                search_terms = ['BELGIAN', 'BROWN']
            elif 'CASTLE ORIGINAL' in name:
                search_terms = ['CASTLE', 'ORIGINAL']
            elif 'CASTLE SILVER' in name:
                search_terms = ['CASTLE', 'SILVER']
            elif 'CORK' in name:
                search_terms = ['CORK']
            elif 'GALWAY' in name:
                search_terms = ['GALWAY']
            elif 'GLASGOW' in name:
                search_terms = ['GLASGOW']
            elif 'JAIPUR' in name:
                search_terms = ['JAIPUR']
            elif 'NOTTINGHAM' in name:
                search_terms = ['NOTTINGHAM']
            elif 'OBAN' in name:
                search_terms = ['OBAN']
            elif 'SYMPHONIA' in name:
                if 'ALLEGRO' in name:
                    search_terms = ['SYMPHONIA', 'ALLEGRO']
                elif 'FORTE' in name:
                    search_terms = ['SYMPHONIA', 'FORTE']
                elif 'LARGO' in name:
                    search_terms = ['SYMPHONIA', 'LARGO']
                elif 'LEGATO' in name:
                    search_terms = ['SYMPHONIA', 'LEGATO']
                elif 'PRESTO' in name:
                    search_terms = ['SYMPHONIA', 'PRESTO']
                elif 'SOLO' in name:
                    search_terms = ['SYMPHONIA', 'SOLO']
                elif 'SONATA' in name:
                    search_terms = ['SYMPHONIA', 'SONATA']
                elif 'VIVO' in name:
                    search_terms = ['SYMPHONIA', 'VIVO']
            elif 'VICENCE' in name:
                search_terms = ['VICENCE']
                
            if search_terms:
                products.append({
                    'original': line.strip(),
                    'search_terms': search_terms,
                    'primary_term': search_terms[0] if search_terms else None
                })
                
        return products
        
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
            
    def search_for_product(self, search_terms: List[str]) -> List[Dict]:
        """Search for a specific product using search terms"""
        products = []
        
        # Try different search strategies
        for term in search_terms:
            # Search in laminate section
            search_url = f"{self.base_url}/search?q={quote_plus(term)}"
            print(f"Searching for: {term} at {search_url}")
            
            content = self.get_page_content(search_url)
            if content:
                products.extend(self.extract_products_from_search(content, search_terms))
                
            time.sleep(0.5)
            
        return products
        
    def extract_products_from_search(self, content: str, search_terms: List[str]) -> List[Dict]:
        """Extract products from search results"""
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        
        # Look for product containers in search results
        selectors = [
            '.product-item', '.product', '.search-result',
            '.product-card', 'article', '[data-product]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    product = self.extract_product_from_element(element, search_terms)
                    if product:
                        products.append(product)
                break
                
        # Also look for any images that might be products
        img_elements = soup.find_all('img', src=True)
        for img in img_elements:
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            # Check if the image matches our search terms
            text_to_check = f"{src} {alt}".lower()
            if any(term.lower() in text_to_check for term in search_terms):
                image_base64 = self.download_image_as_base64(src)
                if image_base64:
                    # Try to get a better name from surrounding context
                    name = alt or 'Unknown Product'
                    if not alt:
                        parent = img.parent
                        if parent:
                            text_elements = parent.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'span'])
                            for elem in text_elements:
                                text = elem.get_text(strip=True)
                                if text and len(text) > 3:
                                    name = text
                                    break
                    
                    products.append({
                        'name': name,
                        'image_url': src,
                        'image_base64': image_base64,
                        'source': 'search_result',
                        'search_terms': search_terms
                    })
                    
        return products
        
    def extract_product_from_element(self, element, search_terms: List[str]) -> Optional[Dict]:
        """Extract product info from a DOM element"""
        try:
            # Get product name
            name_selectors = [
                '.product-title', '.product-name', 'h2', 'h3', 'h4',
                '.title', '.name', 'a[title]'
            ]
            
            product_name = None
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    product_name = name_elem.get_text(strip=True) or name_elem.get('title', '')
                    break
                    
            if not product_name:
                return None
                
            # Get product image
            img_selectors = ['img', '.product-image img', '.product-img img']
            image_url = None
            for selector in img_selectors:
                img_elem = element.select_one(selector)
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src')
                    break
                    
            if not image_url:
                return None
                
            # Download and convert image
            image_base64 = self.download_image_as_base64(image_url)
            if image_base64:
                return {
                    'name': product_name,
                    'image_url': image_url,
                    'image_base64': image_base64,
                    'source': 'search_result',
                    'search_terms': search_terms
                }
                
        except Exception as e:
            print(f"Error extracting product: {e}")
            
        return None
        
    def scrape_target_products(self) -> List[Dict]:
        """Search for all target products"""
        print(f"Searching for {len(self.target_products)} target products...")
        
        all_products = []
        
        for target in self.target_products:
            print(f"\nLooking for: {target['primary_term']}")
            products = self.search_for_product(target['search_terms'])
            
            for product in products:
                product['target_product'] = target['original']
                all_products.append(product)
                
            time.sleep(1)  # Be respectful between searches
            
        print(f"\nFound {len(all_products)} product matches total")
        return all_products
        
    def save_products(self, products: List[Dict], filename: str = "bearfoot_targeted_products.json"):
        """Save found products to JSON file"""
        output_data = {
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "bearfoot.ie - targeted search",
            "total_products": len(products),
            "target_products_searched": len(self.target_products),
            "products": products
        }
        
        filepath = os.path.join('/app', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(products)} products to {filepath}")
        return filepath

def main():
    """Main scraping function"""
    scraper = EnhancedBearfootScraper()
    products = scraper.scrape_target_products()
    
    if products:
        filepath = scraper.save_products(products)
        print(f"Targeted scraping completed. Products saved to: {filepath}")
    else:
        print("No target products found")

if __name__ == "__main__":
    main()
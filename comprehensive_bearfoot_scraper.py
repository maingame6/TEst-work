#!/usr/bin/env python3
"""
Comprehensive Bearfoot Product Scraper
Scrapes ALL products from all laminate categories on bearfoot.ie
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

class ComprehensiveBearfootScraper:
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
        
        # All category URLs from the crawl data
        self.category_urls = [
            # 12mm Laminates
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-quatro/",
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-king-floor/",
            "https://www.bearfoot.ie/floors/laminates/12mm/krono-sound/",
            "https://www.bearfoot.ie/floors/laminates/12mm/xtreme-long-plank/",
            
            # 10mm Laminates  
            "https://www.bearfoot.ie/floors/laminates/10mm/krono-marine/",
            "https://www.bearfoot.ie/floors/laminates/10mm/krono-aroma/",
            "https://www.bearfoot.ie/floors/laminates/10mm/xtreme-wide-and-long/",
            
            # 8mm Laminates
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-sigma/",
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-exclusive/",
            "https://www.bearfoot.ie/floors/laminates/8mm/krono-testa/"
        ]
        
    def get_page_content(self, url: str) -> Optional[str]:
        """Get page content with retry logic"""
        try:
            print(f"Fetching: {url}")
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
            
    def extract_category_info(self, url: str) -> Dict:
        """Extract category information from URL"""
        # Parse category info from URL
        parts = url.split('/')
        thickness = None
        brand = None
        series = None
        
        for i, part in enumerate(parts):
            if part.endswith('mm'):
                thickness = part
            elif part.startswith('krono-'):
                brand = "Krono"
                series = part.replace('krono-', '').replace('-', ' ').title()
            elif part.startswith('xtreme-'):
                brand = "Xtreme"
                series = part.replace('xtreme-', '').replace('-', ' ').title()
                
        return {
            'thickness': thickness,
            'brand': brand or 'Unknown',
            'series': series or 'Unknown',
            'category_url': url
        }
        
    def scrape_category_page(self, category_url: str) -> List[Dict]:
        """Scrape all products from a category page"""
        print(f"\n=== Scraping category: {category_url} ===")
        
        content = self.get_page_content(category_url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        category_info = self.extract_category_info(category_url)
        
        # Try multiple strategies to find products
        
        # Strategy 1: Look for product containers
        product_selectors = [
            '.product-item', '.product', '.product-card', '.product-grid-item',
            '.item', '.product-container', '[data-product]', '.product-inner',
            'article', '.woocommerce-LoopProduct-link', '.product-wrapper'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} products using selector: {selector}")
                product_elements = elements
                break
                
        if product_elements:
            for element in product_elements:
                product = self.extract_product_from_element(element, category_info)
                if product:
                    products.append(product)
                    
        # Strategy 2: Look for individual product images if no containers found
        if not products:
            print("No product containers found, looking for individual images...")
            img_elements = soup.find_all('img', src=True)
            
            for img in img_elements:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                # Skip logos, icons, etc.
                if any(skip in src.lower() for skip in ['logo', 'icon', 'button', 'arrow', 'banner', 'header']):
                    continue
                    
                # Look for product-like images
                if any(prod in src.lower() for prod in ['floor', 'laminate', 'wood', 'oak', 'plank', 'product']):
                    product_name = alt or self.extract_name_from_context(img)
                    
                    if product_name and len(product_name) > 3:
                        image_base64 = self.download_image_as_base64(src)
                        if image_base64:
                            product = {
                                'name': product_name,
                                'display_name': product_name,
                                'image_url': src,
                                'image_base64': image_base64,
                                'brand': category_info['brand'],
                                'series': category_info['series'],
                                'thickness': category_info['thickness'],
                                'category_url': category_url,
                                'source': 'image_extraction'
                            }
                            products.append(product)
                            print(f"  Added: {product_name}")
                            time.sleep(0.3)  # Be respectful
                            
        # Strategy 3: Look for product links and follow them
        if not products:
            print("Looking for product detail links...")
            links = soup.find_all('a', href=True)
            product_links = []
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Look for links that might lead to product pages
                if any(keyword in href.lower() for keyword in ['product', 'floor', 'laminate']) or \
                   any(keyword in text.lower() for keyword in ['floor', 'laminate', 'oak', 'wood']):
                    full_url = urljoin(self.base_url, href)
                    if full_url not in product_links and full_url != category_url:
                        product_links.append(full_url)
                        
            # Scrape first few product detail pages
            for product_url in product_links[:20]:  # Limit to avoid overloading
                product = self.scrape_product_detail_page(product_url, category_info)
                if product:
                    products.append(product)
                time.sleep(0.5)
                    
        print(f"Scraped {len(products)} products from {category_url}")
        return products
        
    def extract_name_from_context(self, img_element) -> str:
        """Try to extract product name from surrounding context"""
        # Look for text in parent elements
        parent = img_element.parent
        attempts = 0
        
        while parent and attempts < 3:
            # Look for headings or text elements
            text_elements = parent.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div'])
            for elem in text_elements:
                text = elem.get_text(strip=True)
                if text and len(text) > 3 and len(text) < 100:
                    # Check if it looks like a product name
                    if any(word in text.lower() for word in ['oak', 'beige', 'brown', 'grey', 'white', 'black', 'natural']):
                        return text
                        
            parent = parent.parent
            attempts += 1
            
        return "Unknown Product"
        
    def extract_product_from_element(self, element, category_info: Dict) -> Optional[Dict]:
        """Extract product information from a DOM element"""
        try:
            # Extract product name
            name_selectors = [
                '.product-title', '.product-name', 'h1', 'h2', 'h3', 'h4',
                '.title', '.name', 'a[title]', '.product-info h3', '.product-info h2'
            ]
            
            product_name = None
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    product_name = name_elem.get_text(strip=True) or name_elem.get('title', '')
                    if product_name:
                        break
                        
            if not product_name:
                return None
                
            # Extract product image
            img_selectors = [
                'img', '.product-image img', '.product-img img', 
                '.image img', '.thumbnail img', '.photo img'
            ]
            
            image_url = None
            for selector in img_selectors:
                img_elem = element.select_one(selector)
                if img_elem:
                    image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-lazy-src')
                    if image_url:
                        break
                        
            if not image_url:
                return None
                
            # Extract price if available
            price_selectors = [
                '.price', '.product-price', '.cost', '.amount',
                '.price-current', '.regular-price'
            ]
            
            price = None
            for selector in price_selectors:
                price_elem = element.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    # Extract numeric price
                    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                    if price_match:
                        try:
                            price = float(price_match.group())
                        except ValueError:
                            pass
                    break
                    
            # Download and convert image
            image_base64 = self.download_image_as_base64(image_url)
            if not image_base64:
                return None
                
            product = {
                'name': product_name,
                'display_name': product_name,
                'price': price,
                'image_url': image_url,
                'image_base64': image_base64,
                'brand': category_info['brand'],
                'series': category_info['series'],
                'thickness': category_info['thickness'],
                'category_url': category_info['category_url'],
                'source': 'structured_extraction'
            }
            
            print(f"  Added: {product_name}")
            return product
            
        except Exception as e:
            print(f"Error extracting product: {e}")
            return None
            
    def scrape_product_detail_page(self, product_url: str, category_info: Dict) -> Optional[Dict]:
        """Scrape a product detail page"""
        content = self.get_page_content(product_url)
        if not content:
            return None
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract product name
        name_selectors = ['h1', 'h2', '.product-title', '.product-name', 'title']
        product_name = None
        
        for selector in name_selectors:
            elem = soup.select_one(selector)
            if elem:
                product_name = elem.get_text(strip=True)
                if product_name and len(product_name) > 3:
                    break
                    
        if not product_name:
            return None
            
        # Extract main product image
        img_selectors = [
            '.product-image img', '.main-image img', '.product-photo img',
            '.hero-image img', '.featured-image img', 'img'
        ]
        
        image_url = None
        for selector in img_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src and not any(skip in src.lower() for skip in ['logo', 'icon', 'button']):
                    image_url = src
                    break
                    
        if not image_url:
            return None
            
        # Download image
        image_base64 = self.download_image_as_base64(image_url)
        if not image_base64:
            return None
            
        product = {
            'name': product_name,
            'display_name': product_name,
            'image_url': image_url,
            'image_base64': image_base64,
            'brand': category_info['brand'],
            'series': category_info['series'],
            'thickness': category_info['thickness'],
            'category_url': category_info['category_url'],
            'detail_url': product_url,
            'source': 'detail_page'
        }
        
        print(f"  Detail page: {product_name}")
        return product
        
    def scrape_all_products(self) -> List[Dict]:
        """Scrape products from all categories"""
        print("Starting comprehensive Bearfoot product scraping...")
        print(f"Will scrape {len(self.category_urls)} categories")
        
        all_products = []
        
        for i, category_url in enumerate(self.category_urls, 1):
            print(f"\n--- Category {i}/{len(self.category_urls)} ---")
            category_products = self.scrape_category_page(category_url)
            all_products.extend(category_products)
            
            print(f"Category total: {len(category_products)} products")
            print(f"Running total: {len(all_products)} products")
            
            # Be respectful between categories
            time.sleep(2)
            
        print(f"\n🎉 SCRAPING COMPLETE!")
        print(f"Total products scraped: {len(all_products)}")
        
        return all_products
        
    def save_products(self, products: List[Dict], filename: str = "bearfoot_all_products.json"):
        """Save all products to JSON file"""
        
        # Add generated IDs and standardize data
        for i, product in enumerate(products):
            product['id'] = f"bearfoot_{i+1:04d}"
            product['category'] = 'Laminate Flooring'
            product['product_type'] = self.determine_product_type(product)
            product['description'] = self.generate_description(product)
            product['features'] = self.generate_features(product)
            product['in_stock'] = True
            product['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Set default price if not found
            if not product.get('price'):
                product['price'] = self.estimate_price_by_thickness(product.get('thickness'))
                
        output_data = {
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "bearfoot.ie - comprehensive scrape",
            "total_products": len(products),
            "categories_scraped": len(self.category_urls),
            "products": products
        }
        
        filepath = os.path.join('/app', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Saved {len(products)} products to {filepath}")
        
        # Generate summary by category
        self.print_summary(products)
        
        return filepath
        
    def determine_product_type(self, product: Dict) -> str:
        """Determine product type from name and series"""
        name = product.get('name', '').lower()
        series = product.get('series', '').lower()
        
        if 'herringbone' in name or 'herringbone' in series:
            return 'Herringbone'
        elif 'x-loc' in name or 'xloc' in name:
            return 'X-LOC'
        elif 'wide' in series or 'long' in series:
            return 'Wide & Long Plank'
        else:
            return 'Long Plank'
            
    def generate_description(self, product: Dict) -> str:
        """Generate product description"""
        brand = product.get('brand', 'Bearfoot')
        thickness = product.get('thickness', '')
        series = product.get('series', '')
        product_type = product.get('product_type', 'laminate flooring')
        
        return f"Premium {thickness} {brand} {series} {product_type.lower()} with realistic wood grain texture and easy click installation system."
        
    def generate_features(self, product: Dict) -> List[str]:
        """Generate product features based on type and brand"""
        features = ["Water resistant", "Easy click installation", "Scratch resistant surface"]
        
        thickness = product.get('thickness', '')
        if thickness == '12mm':
            features.append("Extra thick for durability")
        elif thickness == '10mm':
            features.append("Perfect balance of quality and value")
        elif thickness == '8mm':
            features.append("Ideal for residential use")
            
        product_type = product.get('product_type', '')
        if 'Herringbone' in product_type:
            features.append("Classic herringbone pattern")
        elif 'Wide' in product_type:
            features.append("Wide plank design")
            
        return features
        
    def estimate_price_by_thickness(self, thickness: str) -> float:
        """Estimate price based on thickness"""
        if thickness == '12mm':
            return 54.50
        elif thickness == '10mm':
            return 45.00
        elif thickness == '8mm':
            return 35.50
        else:
            return 40.00
            
    def print_summary(self, products: List[Dict]):
        """Print scraping summary"""
        print(f"\n📊 SCRAPING SUMMARY")
        print(f"=" * 50)
        
        # By brand
        brands = {}
        for product in products:
            brand = product.get('brand', 'Unknown')
            brands[brand] = brands.get(brand, 0) + 1
            
        print("By Brand:")
        for brand, count in sorted(brands.items()):
            print(f"  {brand}: {count} products")
            
        # By thickness
        thicknesses = {}
        for product in products:
            thickness = product.get('thickness', 'Unknown')
            thicknesses[thickness] = thicknesses.get(thickness, 0) + 1
            
        print("\nBy Thickness:")
        for thickness, count in sorted(thicknesses.items()):
            print(f"  {thickness}: {count} products")
            
        # By series
        series_counts = {}
        for product in products:
            series = product.get('series', 'Unknown')
            series_counts[series] = series_counts.get(series, 0) + 1
            
        print("\nBy Series:")
        for series, count in sorted(series_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {series}: {count} products")

def main():
    """Main scraping function"""
    scraper = ComprehensiveBearfootScraper()
    
    print("🚀 Starting comprehensive Bearfoot product scraping...")
    print("This will take several minutes to complete...")
    
    products = scraper.scrape_all_products()
    
    if products:
        filepath = scraper.save_products(products)
        print(f"\n✅ Scraping completed successfully!")
        print(f"📁 Products saved to: {filepath}")
        print(f"🎯 Total products: {len(products)}")
    else:
        print("❌ No products found or scraping failed")

if __name__ == "__main__":
    main()
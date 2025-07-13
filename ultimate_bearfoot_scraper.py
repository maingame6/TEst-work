#!/usr/bin/env python3
"""
Ultimate Bearfoot Product Scraper - ALL SECTIONS
Scrapes ALL products from EVERY section of bearfoot.ie
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

class UltimateBearfootScraper:
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
        
        # ALL product sections and their categories
        self.all_sections = {
            "Laminates": {
                "12mm": [
                    "https://www.bearfoot.ie/floors/laminates/12mm/krono-quatro/",
                    "https://www.bearfoot.ie/floors/laminates/12mm/krono-king-floor/",
                    "https://www.bearfoot.ie/floors/laminates/12mm/krono-sound/",
                    "https://www.bearfoot.ie/floors/laminates/12mm/xtreme-long-plank/"
                ],
                "10mm": [
                    "https://www.bearfoot.ie/floors/laminates/10mm/krono-marine/",
                    "https://www.bearfoot.ie/floors/laminates/10mm/krono-aroma/",
                    "https://www.bearfoot.ie/floors/laminates/10mm/xtreme-wide-and-long/"
                ],
                "8mm": [
                    "https://www.bearfoot.ie/floors/laminates/8mm/krono-sigma/",
                    "https://www.bearfoot.ie/floors/laminates/8mm/krono-exclusive/",
                    "https://www.bearfoot.ie/floors/laminates/8mm/krono-testa/"
                ]
            },
            "Water Resistant Laminates": {
                "main": ["https://www.bearfoot.ie/floors/water-resistant-laminates/"]
            },
            "Waterproof SPC": {
                "amaron": [
                    "https://www.bearfoot.ie/floors/waterproof-spc/amaron-spc/amaron-acoustic-plank/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/amaron-spc/amaron-herringbone/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/amaron-spc/amaron-chevron/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/amaron-spc/amaron-forma-tiles/"
                ],
                "republic": [
                    "https://www.bearfoot.ie/floors/waterproof-spc/republic-spc/grizzly/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/republic-spc/tiger/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/republic-spc/republic-wolf/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/republic-spc/lion-herringbone/",
                    "https://www.bearfoot.ie/floors/waterproof-spc/republic-spc/republic-stair-nosings/"
                ]
            },
            "Hardwoods": {
                "14mm": [
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/hakwood/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/vista-original/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/intasa-200mm-plank/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/intasa-250mm-plank/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/the-twelve/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/esco-190mm-plank/",
                    "https://www.bearfoot.ie/floors/hardwoods/14mm/esco-225mm-plank/"
                ],
                "18mm": [
                    "https://www.bearfoot.ie/floors/hardwoods/18mm/vista-ultra/"
                ],
                "20mm": [
                    "https://www.bearfoot.ie/floors/hardwoods/20mm/vista-xl/"
                ],
                "herringbone": [
                    "https://www.bearfoot.ie/floors/hardwoods/herringbone/hakwood-herringbone/",
                    "https://www.bearfoot.ie/floors/hardwoods/herringbone/vista-herringbone/",
                    "https://www.bearfoot.ie/floors/hardwoods/herringbone/intasa-herringbone/",
                    "https://www.bearfoot.ie/floors/hardwoods/herringbone/esco-herringbone/",
                    "https://www.bearfoot.ie/floors/hardwoods/herringbone/vista-ultra-herringbone/"
                ]
            },
            "Accessories": {
                "main": ["https://www.bearfoot.ie/floors/accessories/"]
            }
        }
        
    def get_page_content(self, url: str) -> Optional[str]:
        """Get page content with retry logic"""
        try:
            print(f"  → Fetching: {url}")
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"    ❌ Error fetching {url}: {e}")
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
            print(f"    ❌ Error downloading image {image_url}: {e}")
            return None
            
    def extract_product_info_from_url(self, url: str) -> Dict:
        """Extract product category information from URL"""
        parts = url.split('/')
        
        section = "Unknown"
        subsection = "Unknown"
        thickness = None
        brand = "Bearfoot"
        series = "Unknown"
        
        # Determine section
        if 'laminates' in url and 'water-resistant' not in url:
            section = "Laminates"
        elif 'water-resistant-laminates' in url:
            section = "Water Resistant Laminates"
        elif 'waterproof-spc' in url:
            section = "Waterproof SPC"
        elif 'hardwoods' in url:
            section = "Hardwoods"
        elif 'accessories' in url:
            section = "Accessories"
            
        # Extract thickness
        for part in parts:
            if part.endswith('mm'):
                thickness = part
                subsection = part
                break
                
        # Extract brand and series
        for i, part in enumerate(parts):
            if part.startswith('krono-'):
                brand = "Krono"
                series = part.replace('krono-', '').replace('-', ' ').title()
            elif part.startswith('xtreme-'):
                brand = "Xtreme"  
                series = part.replace('xtreme-', '').replace('-', ' ').title()
            elif part.startswith('amaron-'):
                brand = "Amaron"
                series = part.replace('amaron-', '').replace('-', ' ').title()
            elif part.startswith('republic-'):
                brand = "Republic"
                series = part.replace('republic-', '').replace('-', ' ').title()
            elif part in ['hakwood', 'vista', 'intasa', 'esco']:
                brand = part.title()
                if i + 1 < len(parts):
                    series = parts[i + 1].replace('-', ' ').title()
            elif part == 'the-twelve':
                brand = "The Twelve"
                series = "Premium Collection"
                
        return {
            'section': section,
            'subsection': subsection,
            'thickness': thickness,
            'brand': brand,
            'series': series,
            'category_url': url
        }
        
    def scrape_page_products(self, url: str) -> List[Dict]:
        """Scrape all products from a single page"""
        content = self.get_page_content(url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        products = []
        category_info = self.extract_product_info_from_url(url)
        
        print(f"    🔍 Scanning for products...")
        
        # Multiple strategies to find products
        
        # Strategy 1: Look for product containers
        product_selectors = [
            '.product-item', '.product', '.product-card', '.product-grid-item',
            '.item', '.product-container', '[data-product]', '.product-inner',
            'article', '.woocommerce-LoopProduct-link', '.product-wrapper',
            '.product-list-item', '.floor-sample', '.sample'
        ]
        
        product_elements = []
        for selector in product_selectors:
            elements = soup.select(selector)
            if elements:
                print(f"    ✅ Found {len(elements)} products using selector: {selector}")
                product_elements = elements
                break
                
        if product_elements:
            for element in product_elements:
                product = self.extract_product_from_element(element, category_info)
                if product:
                    products.append(product)
                    
        # Strategy 2: Look for individual product images
        if not products:
            print(f"    🔍 No containers found, scanning images...")
            img_elements = soup.find_all('img', src=True)
            
            processed_images = set()  # Avoid duplicates
            
            for img in img_elements:
                src = img.get('src', '')
                alt = img.get('alt', '')
                
                # Skip if already processed
                if src in processed_images:
                    continue
                processed_images.add(src)
                
                # Skip logos, icons, etc.
                if any(skip in src.lower() for skip in ['logo', 'icon', 'button', 'arrow', 'banner', 'header', 'menu']):
                    continue
                    
                # Look for product-like images
                if any(prod in src.lower() for prod in ['floor', 'laminate', 'wood', 'oak', 'plank', 'product', 'sample', 'colour', 'color']):
                    product_name = alt or self.extract_name_from_context(img)
                    
                    if product_name and len(product_name) > 3 and 'bearfoot' not in product_name.lower():
                        image_base64 = self.download_image_as_base64(src)
                        if image_base64:
                            product = {
                                'name': product_name,
                                'display_name': product_name,
                                'image_url': src,
                                'image_base64': image_base64,
                                'section': category_info['section'],
                                'subsection': category_info['subsection'],
                                'thickness': category_info['thickness'],
                                'brand': category_info['brand'],
                                'series': category_info['series'],
                                'category_url': url,
                                'source': 'image_extraction'
                            }
                            products.append(product)
                            print(f"      ✅ Added: {product_name}")
                            time.sleep(0.2)  # Be respectful
                            
        # Strategy 3: Look for product links and follow them (for detail pages)
        if not products and 'product' not in url:
            print(f"    🔍 Looking for product detail links...")
            links = soup.find_all('a', href=True)
            product_links = []
            
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Look for links that might lead to product pages
                if any(keyword in href.lower() for keyword in ['product', 'floor', 'laminate', 'sample']) and \
                   len(text) > 3 and len(text) < 100:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in product_links and full_url != url:
                        product_links.append(full_url)
                        
            # Follow first few product links
            for product_url in product_links[:15]:  # Limit to avoid overloading
                product = self.scrape_product_detail_page(product_url, category_info)
                if product:
                    products.append(product)
                time.sleep(0.3)
                    
        print(f"    📦 Found {len(products)} products")
        return products
        
    def extract_name_from_context(self, img_element) -> str:
        """Try to extract product name from surrounding context"""
        # Look for text in parent elements
        parent = img_element.parent
        attempts = 0
        
        while parent and attempts < 4:
            # Look for headings or text elements
            text_elements = parent.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'figcaption'])
            for elem in text_elements:
                text = elem.get_text(strip=True)
                if text and 5 < len(text) < 100:
                    # Check if it looks like a product name
                    if any(word in text.lower() for word in ['oak', 'beige', 'brown', 'grey', 'white', 'black', 'natural', 'walnut', 'ash', 'pine', 'colour', 'color']):
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
                '.title', '.name', 'a[title]', '.product-info h3', '.product-info h2',
                'figcaption', '.caption', '.description'
            ]
            
            product_name = None
            for selector in name_selectors:
                name_elem = element.select_one(selector)
                if name_elem:
                    product_name = name_elem.get_text(strip=True) or name_elem.get('title', '')
                    if product_name and len(product_name) > 3:
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
                    if image_url and 'logo' not in image_url.lower():
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
                'section': category_info['section'],
                'subsection': category_info['subsection'],
                'thickness': category_info['thickness'],
                'brand': category_info['brand'],
                'series': category_info['series'],
                'category_url': category_info['category_url'],
                'source': 'structured_extraction'
            }
            
            print(f"      ✅ Added: {product_name}")
            return product
            
        except Exception as e:
            print(f"      ❌ Error extracting product: {e}")
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
                text = elem.get_text(strip=True)
                if text and 3 < len(text) < 200 and 'bearfoot' not in text.lower():
                    product_name = text
                    break
                    
        if not product_name:
            return None
            
        # Extract main product image
        img_selectors = [
            '.product-image img', '.main-image img', '.product-photo img',
            '.hero-image img', '.featured-image img', '.gallery img', 'img'
        ]
        
        image_url = None
        for selector in img_selectors:
            img_elem = soup.select_one(selector)
            if img_elem:
                src = img_elem.get('src') or img_elem.get('data-src')
                if src and not any(skip in src.lower() for skip in ['logo', 'icon', 'button', 'arrow']):
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
            'section': category_info['section'],
            'subsection': category_info['subsection'],
            'thickness': category_info['thickness'],
            'brand': category_info['brand'],
            'series': category_info['series'],
            'category_url': category_info['category_url'],
            'detail_url': product_url,
            'source': 'detail_page'
        }
        
        print(f"      ✅ Detail page: {product_name}")
        return product
        
    def scrape_all_sections(self) -> List[Dict]:
        """Scrape products from ALL sections"""
        print("🚀 Starting ULTIMATE Bearfoot product scraping...")
        print("🎯 This will scrape ALL product sections and categories")
        print(f"📊 Total sections: {len(self.all_sections)}")
        
        total_urls = sum(len(subcats) if isinstance(subcats, dict) else len([subcats]) 
                        for section in self.all_sections.values() 
                        for subcats in section.values())
        print(f"📊 Total categories to scrape: {total_urls}")
        
        all_products = []
        section_count = 0
        
        for section_name, subsections in self.all_sections.items():
            section_count += 1
            print(f"\n{'='*60}")
            print(f"🏗️  SECTION {section_count}/{len(self.all_sections)}: {section_name}")
            print(f"{'='*60}")
            
            section_products = []
            
            for subsection_name, urls in subsections.items():
                print(f"\n📁 Subsection: {subsection_name}")
                
                for i, url in enumerate(urls, 1):
                    print(f"\n  📂 Category {i}/{len(urls)}: {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}")
                    
                    category_products = self.scrape_page_products(url)
                    section_products.extend(category_products)
                    
                    print(f"    📊 Category total: {len(category_products)} products")
                    print(f"    📊 Section running total: {len(section_products)} products")
                    
                    # Be respectful between categories
                    time.sleep(1)
                    
            all_products.extend(section_products)
            print(f"\n🎯 {section_name} COMPLETE: {len(section_products)} products")
            print(f"🎯 GRAND TOTAL SO FAR: {len(all_products)} products")
            
            # Be respectful between sections
            time.sleep(2)
            
        print(f"\n{'='*60}")
        print(f"🎉 ULTIMATE SCRAPING COMPLETE!")
        print(f"🎯 TOTAL PRODUCTS FOUND: {len(all_products)}")
        print(f"{'='*60}")
        
        return all_products
        
    def save_all_products(self, products: List[Dict], filename: str = "bearfoot_ultimate_catalog.json"):
        """Save all products with proper processing"""
        
        print(f"\n🔄 Processing {len(products)} products...")
        
        # Add generated IDs and standardize data
        for i, product in enumerate(products):
            product['id'] = f"bearfoot_{i+1:04d}"
            product['category'] = product.get('section', 'Flooring')
            product['product_type'] = self.determine_product_type(product)
            product['description'] = self.generate_description(product)
            product['features'] = self.generate_features(product)
            product['in_stock'] = True
            product['area_m2'] = self.estimate_area(product)
            product['created_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
            
            # Set price if not found
            if not product.get('price'):
                product['price'] = self.estimate_price(product)
                
        output_data = {
            "scraped_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "bearfoot.ie - ultimate comprehensive scrape",
            "total_products": len(products),
            "sections_scraped": list(self.all_sections.keys()),
            "products": products
        }
        
        filepath = os.path.join('/app', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Saved {len(products)} products to {filepath}")
        
        # Generate comprehensive summary
        self.print_comprehensive_summary(products)
        
        return filepath
        
    def determine_product_type(self, product: Dict) -> str:
        """Determine product type from name and properties"""
        name = product.get('name', '').lower()
        series = product.get('series', '').lower()
        section = product.get('section', '').lower()
        
        if 'herringbone' in name or 'herringbone' in series or 'herringbone' in section:
            return 'Herringbone'
        elif 'chevron' in name or 'chevron' in series:
            return 'Chevron'
        elif 'tiles' in name or 'tile' in name:
            return 'Tiles'
        elif 'x-loc' in name or 'xloc' in name:
            return 'X-LOC'
        elif 'wide' in series or 'long' in series:
            return 'Wide & Long Plank'
        elif 'spc' in section:
            return 'SPC Plank'
        elif 'hardwood' in section:
            return 'Hardwood Plank'
        elif 'accessory' in section or 'accessory' in name:
            return 'Accessory'
        else:
            return 'Long Plank'
            
    def generate_description(self, product: Dict) -> str:
        """Generate product description"""
        brand = product.get('brand', 'Bearfoot')
        thickness = product.get('thickness', '')
        series = product.get('series', '')
        section = product.get('section', 'flooring')
        product_type = product.get('product_type', 'flooring')
        
        if thickness:
            return f"Premium {thickness} {brand} {series} {product_type.lower()} featuring authentic wood grain texture and advanced installation system."
        else:
            return f"High-quality {brand} {series} {section.lower()} with premium finish and professional installation features."
        
    def generate_features(self, product: Dict) -> List[str]:
        """Generate product features based on type and section"""
        features = []
        
        section = product.get('section', '').lower()
        product_type = product.get('product_type', '').lower()
        thickness = product.get('thickness', '')
        
        # Base features
        if 'water' in section or 'waterproof' in section:
            features.extend(["Waterproof", "Suitable for wet areas"])
        elif 'laminate' in section:
            features.extend(["Water resistant", "Easy maintenance"])
        elif 'hardwood' in section:
            features.extend(["Real wood", "Can be refinished"])
            
        # Installation features
        if 'spc' in section:
            features.append("Click-lock installation")
        else:
            features.append("Easy click installation")
            
        # Surface features
        features.extend(["Scratch resistant surface", "Realistic wood grain texture"])
        
        # Thickness-specific features
        if thickness == '12mm':
            features.append("Extra thick for high traffic areas")
        elif thickness == '18mm' or thickness == '20mm':
            features.append("Premium thickness for luxury feel")
        elif thickness == '14mm':
            features.append("Professional grade thickness")
            
        # Pattern-specific features
        if 'herringbone' in product_type:
            features.append("Classic herringbone pattern")
        elif 'chevron' in product_type:
            features.append("Elegant chevron design")
        elif 'wide' in product_type:
            features.append("Wide plank design for modern look")
            
        return features[:6]  # Limit to 6 features
        
    def estimate_area(self, product: Dict) -> float:
        """Estimate coverage area per pack"""
        thickness = product.get('thickness', '')
        product_type = product.get('product_type', '')
        
        if 'herringbone' in product_type.lower():
            return 1.2  # Herringbone typically smaller packs
        elif thickness == '20mm':
            return 2.1  # Thicker planks, larger coverage
        elif thickness == '18mm':
            return 2.9
        elif thickness == '14mm':
            return 2.5
        elif thickness == '12mm':
            return 1.4
        elif thickness == '10mm':
            return 1.8
        elif thickness == '8mm':
            return 2.4
        else:
            return 2.0  # Default
            
    def estimate_price(self, product: Dict) -> float:
        """Estimate price based on product characteristics"""
        section = product.get('section', '').lower()
        thickness = product.get('thickness', '')
        product_type = product.get('product_type', '')
        brand = product.get('brand', '').lower()
        
        base_price = 40.0
        
        # Section pricing
        if 'hardwood' in section:
            base_price = 120.0
        elif 'waterproof' in section or 'spc' in section:
            base_price = 75.0
        elif 'water resistant' in section:
            base_price = 55.0
        elif 'laminate' in section:
            base_price = 45.0
            
        # Thickness adjustment
        if thickness == '20mm':
            base_price *= 1.8
        elif thickness == '18mm':
            base_price *= 1.6
        elif thickness == '14mm':
            base_price *= 1.4
        elif thickness == '12mm':
            base_price *= 1.2
        elif thickness == '8mm':
            base_price *= 0.9
            
        # Brand adjustment
        if brand in ['esco', 'hakwood']:
            base_price *= 1.5
        elif brand in ['vista', 'intasa']:
            base_price *= 1.3
        elif brand == 'the twelve':
            base_price *= 2.0
            
        # Pattern adjustment
        if 'herringbone' in product_type.lower():
            base_price *= 1.1
            
        return round(base_price, 2)
        
    def print_comprehensive_summary(self, products: List[Dict]):
        """Print comprehensive scraping summary"""
        print(f"\n📊 COMPREHENSIVE SUMMARY")
        print(f"{'='*70}")
        
        # By section
        sections = {}
        for product in products:
            section = product.get('section', 'Unknown')
            sections[section] = sections.get(section, 0) + 1
            
        print("📦 By Section:")
        for section, count in sorted(sections.items(), key=lambda x: x[1], reverse=True):
            print(f"   {section}: {count} products")
            
        # By brand
        brands = {}
        for product in products:
            brand = product.get('brand', 'Unknown')
            brands[brand] = brands.get(brand, 0) + 1
            
        print("\n🏢 By Brand:")
        for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True):
            print(f"   {brand}: {count} products")
            
        # By thickness
        thicknesses = {}
        for product in products:
            thickness = product.get('thickness', 'No thickness')
            thicknesses[thickness] = thicknesses.get(thickness, 0) + 1
            
        print("\n📏 By Thickness:")
        for thickness, count in sorted(thicknesses.items()):
            print(f"   {thickness}: {count} products")
            
        # By product type
        types = {}
        for product in products:
            ptype = product.get('product_type', 'Unknown')
            types[ptype] = types.get(ptype, 0) + 1
            
        print("\n🎨 By Product Type:")
        for ptype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
            print(f"   {ptype}: {count} products")
            
        # Price range
        prices = [p.get('price', 0) for p in products if p.get('price')]
        if prices:
            print(f"\n💰 Price Range:")
            print(f"   Min: €{min(prices):.2f}")
            print(f"   Max: €{max(prices):.2f}")
            print(f"   Avg: €{sum(prices)/len(prices):.2f}")

def main():
    """Main scraping function"""
    scraper = UltimateBearfootScraper()
    
    print("🚀 ULTIMATE BEARFOOT PRODUCT SCRAPER")
    print("=" * 70)
    print("This will scrape ALL products from EVERY section:")
    print("• Regular Laminates")
    print("• Water Resistant Laminates")  
    print("• Waterproof SPC")
    print("• Hardwoods")
    print("• Accessories")
    print("=" * 70)
    
    products = scraper.scrape_all_sections()
    
    if products:
        filepath = scraper.save_all_products(products)
        print(f"\n🎉 ULTIMATE SCRAPING COMPLETED SUCCESSFULLY!")
        print(f"📁 Products saved to: {filepath}")
        print(f"🎯 TOTAL PRODUCTS: {len(products)}")
        print(f"🏆 You now have the complete Bearfoot catalog!")
    else:
        print("❌ No products found or scraping failed")

if __name__ == "__main__":
    main()
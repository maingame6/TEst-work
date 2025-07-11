#!/usr/bin/env python3
"""
Alternative scraper for tileswoodfloorni.com using curl and parsing
"""

import requests
import json
import re
import subprocess
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import urllib3
import time
import base64

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SimpleTilesScraper:
    def __init__(self):
        self.base_url = "https://tileswoodfloorni.com"
        self.session = requests.Session()
        self.session.verify = False
        self.products = []
        
    def get_page_with_curl(self, url):
        """Get page content using curl with SSL bypass"""
        try:
            cmd = [
                'curl', '-k', '-L', 
                '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                url
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Curl failed for {url}: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error with curl for {url}: {e}")
            return None
    
    def extract_images_from_content(self, content):
        """Extract image URLs from content"""
        images = []
        
        # Different patterns to find images
        patterns = [
            r'"([^"]*\.(jpg|jpeg|png|webp|gif))"',
            r"'([^']*\.(jpg|jpeg|png|webp|gif))'",
            r'static/media/[^"\s]+\.(jpg|jpeg|png|webp|gif)',
            r'src:([^,\s]+\.(jpg|jpeg|png|webp|gif))',
            r'url\(([^)]+\.(jpg|jpeg|png|webp|gif))\)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    image_url = match[0]
                else:
                    image_url = match
                
                # Clean and normalize URL
                image_url = image_url.strip('"\'()').split('?')[0]
                
                # Make it a full URL
                if image_url.startswith('//'):
                    image_url = 'https:' + image_url
                elif image_url.startswith('/'):
                    image_url = self.base_url + image_url
                elif not image_url.startswith('http'):
                    image_url = self.base_url + '/' + image_url
                
                if image_url not in images and any(ext in image_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                    images.append(image_url)
        
        return images
    
    def extract_product_names_from_content(self, content):
        """Extract potential product names from content"""
        products = []
        
        # Look for common tile/flooring related terms
        tile_keywords = [
            r'(\w+\s*\d+[x×]\d+\s*(?:cm|mm)?\s*(?:tile|tiles|porcelain|ceramic))',
            r'(\w+\s*laminate\s*flooring?)',
            r'(\w+\s*wood\s*flooring?)',
            r'(\w+\s*vinyl\s*(?:tile|plank))',
            r'(\w+\s*(?:marble|granite|slate|travertine))',
            r'([\w\s]+(?:tile|tiles|flooring|laminate|vinyl|wood)[\w\s]*)',
        ]
        
        for pattern in tile_keywords:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    product_name = match[0]
                else:
                    product_name = match
                
                product_name = product_name.strip()
                if len(product_name) > 3 and len(product_name) < 100:
                    products.append({
                        'name': product_name,
                        'type': 'extracted_from_content'
                    })
        
        return products
    
    def get_js_files(self, html_content):
        """Extract and fetch JavaScript files"""
        js_files = []
        
        # Find JavaScript file references
        js_patterns = [
            r'src="([^"]*\.js[^"]*)"',
            r"src='([^']*\.js[^']*)'",
            r'static/js/[^"\s]+\.js'
        ]
        
        for pattern in js_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                js_url = match.strip('"\'')
                
                if js_url.startswith('/'):
                    js_url = self.base_url + js_url
                elif not js_url.startswith('http'):
                    js_url = self.base_url + '/' + js_url
                
                if js_url not in js_files:
                    js_files.append(js_url)
        
        return js_files
    
    def analyze_js_content(self, js_content):
        """Analyze JavaScript content for product data"""
        images = []
        products = []
        
        if not js_content:
            return images, products
        
        # Extract images from JS
        images = self.extract_images_from_content(js_content)
        
        # Look for product data structures in JS
        # Try to find arrays that might contain product information
        try:
            # Look for common product data patterns
            product_array_patterns = [
                r'products\s*[:=]\s*(\[[\s\S]*?\])',
                r'all_product\s*[:=]\s*(\[[\s\S]*?\])',
                r'items\s*[:=]\s*(\[[\s\S]*?\])',
                r'catalogue\s*[:=]\s*(\[[\s\S]*?\])'
            ]
            
            for pattern in product_array_patterns:
                matches = re.findall(pattern, js_content, re.IGNORECASE)
                for match in matches:
                    try:
                        # Try to extract readable product names from the JS data
                        # Look for name patterns
                        name_matches = re.findall(r'name\s*:\s*["\']([^"\']+)["\']', match, re.IGNORECASE)
                        for name in name_matches:
                            products.append({
                                'name': name,
                                'type': 'from_js_data',
                                'source': 'javascript'
                            })
                    except:
                        continue
        except Exception as e:
            print(f"Error analyzing JS content: {e}")
        
        return images, products
    
    def scrape_comprehensive(self):
        """Comprehensive scraping approach"""
        print("Starting comprehensive scraping...")
        
        all_data = {
            'products': [],
            'images': [],
            'metadata': {
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'tileswoodfloorni.com',
                'ssl_bypassed': True,
                'method': 'curl_based_scraping'
            }
        }
        
        # Pages to scrape
        pages = [
            self.base_url,
            self.base_url + "/tiles",
            self.base_url + "/laminate", 
            self.base_url + "/real-wood",
            self.base_url + "/lvt"
        ]
        
        for url in pages:
            print(f"Scraping: {url}")
            html_content = self.get_page_with_curl(url)
            
            if html_content:
                # Extract images from HTML
                page_images = self.extract_images_from_content(html_content)
                all_data['images'].extend(page_images)
                print(f"Found {len(page_images)} images on {url}")
                
                # Extract product names from HTML
                page_products = self.extract_product_names_from_content(html_content)
                all_data['products'].extend(page_products)
                print(f"Found {len(page_products)} potential products on {url}")
                
                # Get and analyze JavaScript files
                js_files = self.get_js_files(html_content)
                print(f"Found {len(js_files)} JS files on {url}")
                
                for js_url in js_files:
                    print(f"Analyzing JS file: {js_url}")
                    js_content = self.get_page_with_curl(js_url)
                    if js_content:
                        js_images, js_products = self.analyze_js_content(js_content)
                        all_data['images'].extend(js_images)
                        all_data['products'].extend(js_products)
                        print(f"JS file yielded {len(js_images)} images and {len(js_products)} products")
        
        # Remove duplicates
        all_data['images'] = list(set(all_data['images']))
        
        # Filter and clean products
        seen_names = set()
        filtered_products = []
        for product in all_data['products']:
            name = product['name'].lower().strip()
            if name not in seen_names and len(name) > 3:
                seen_names.add(name)
                filtered_products.append(product)
        
        all_data['products'] = filtered_products
        
        print(f"Total found: {len(all_data['products'])} products, {len(all_data['images'])} images")
        
        return all_data
    
    def download_images(self, image_urls, max_images=50):
        """Download images and convert to base64"""
        downloaded_images = []
        
        print(f"Downloading up to {max_images} images...")
        
        for i, url in enumerate(image_urls[:max_images]):
            try:
                print(f"Downloading {i+1}/{min(len(image_urls), max_images)}: {url}")
                
                response = self.session.get(url, timeout=10)
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
                    
                    downloaded_images.append({
                        'url': url,
                        'base64': f"data:{mime_type};base64,{image_data}",
                        'size': len(response.content),
                        'mime_type': mime_type
                    })
                    
                else:
                    print(f"Failed to download {url}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"Error downloading {url}: {e}")
        
        return downloaded_images
    
    def save_results(self, data, filename="tileswoodfloorni_scraped_data.json"):
        """Save results to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")
        return filename

def main():
    scraper = SimpleTilesScraper()
    
    # Scrape the website
    data = scraper.scrape_comprehensive()
    
    print(f"\n=== SCRAPING RESULTS ===")
    print(f"Found {len(data['products'])} unique products")
    print(f"Found {len(data['images'])} unique images")
    
    # Download images
    if data['images']:
        print("\nDownloading images...")
        downloaded_images = scraper.download_images(data['images'])
        data['downloaded_images'] = downloaded_images
        print(f"Successfully downloaded {len(downloaded_images)} images")
    
    # Save results
    filename = scraper.save_results(data)
    
    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Scraping completed successfully!")
    print(f"Results saved to: {filename}")
    print(f"- {len(data['products'])} products found")
    print(f"- {len(data['images'])} image URLs found")
    print(f"- {len(data.get('downloaded_images', []))} images downloaded")
    
    # Print first few products as example
    if data['products']:
        print(f"\nFirst few products found:")
        for i, product in enumerate(data['products'][:10]):
            print(f"  {i+1}. {product['name']} ({product['type']})")

if __name__ == "__main__":
    main()
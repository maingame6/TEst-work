#!/usr/bin/env python3
"""
Web scraper for tileswoodfloorni.com
Bypasses SSL certificate validation to extract product information
"""

import requests
import json
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import urllib3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import base64

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TilesWoodFloorScraper:
    def __init__(self):
        self.base_url = "https://tileswoodfloorni.com"
        self.session = requests.Session()
        self.session.verify = False  # Bypass SSL verification
        self.products = []
        
    def setup_driver(self):
        """Setup Chrome driver with options to bypass SSL"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        try:
            # Use chromium instead of chrome
            driver = webdriver.Chrome(options=chrome_options, executable_path="/usr/bin/chromium")
            return driver
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            # Try with default chromium
            try:
                chrome_options.binary_location = "/usr/bin/chromium"
                driver = webdriver.Chrome(options=chrome_options)
                return driver
            except Exception as e2:
                print(f"Error setting up Chromium driver: {e2}")
                return None
    
    def get_page_content(self, url, wait_time=10):
        """Get page content using Selenium"""
        driver = self.setup_driver()
        if not driver:
            return None
            
        try:
            print(f"Loading page: {url}")
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for React to render
            time.sleep(5)
            
            # Get page source
            page_source = driver.page_source
            return page_source
            
        except Exception as e:
            print(f"Error getting page content: {e}")
            return None
        finally:
            driver.quit()
    
    def extract_images_from_js(self, html_content):
        """Extract image URLs from JavaScript code"""
        images = []
        
        # Find all image references in the HTML/JS
        image_patterns = [
            r'static/media/[^"\']+\.(jpg|jpeg|png|webp|gif)',
            r'src:([^,]+\.(jpg|jpeg|png|webp|gif))',
            r'"([^"]+\.(jpg|jpeg|png|webp|gif))"',
            r"'([^']+\.(jpg|jpeg|png|webp|gif))'"
        ]
        
        for pattern in image_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    image_url = match[0]
                else:
                    image_url = match
                
                # Clean up the URL
                image_url = image_url.strip('"\'')
                
                # Make sure it's a full URL
                if image_url.startswith('/'):
                    image_url = self.base_url + image_url
                elif not image_url.startswith('http'):
                    image_url = self.base_url + '/' + image_url
                
                if image_url not in images:
                    images.append(image_url)
        
        return images
    
    def extract_product_info_from_js(self, html_content):
        """Extract product information from JavaScript"""
        products = []
        
        # Try to find product arrays or objects in the JS
        # Look for common product data patterns
        product_patterns = [
            r'products\s*[:=]\s*(\[[\s\S]*?\])',
            r'all_product\s*[:=]\s*(\[[\s\S]*?\])',
            r'productData\s*[:=]\s*(\[[\s\S]*?\])',
            r'items\s*[:=]\s*(\[[\s\S]*?\])'
        ]
        
        for pattern in product_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    # Try to parse as JSON
                    product_data = json.loads(match)
                    if isinstance(product_data, list):
                        products.extend(product_data)
                except:
                    continue
        
        return products
    
    def scrape_with_selenium(self):
        """Main scraping method using Selenium"""
        print("Starting scrape with Selenium...")
        
        # Try different pages that might contain product data
        pages_to_try = [
            self.base_url,
            self.base_url + "/tiles",
            self.base_url + "/laminate", 
            self.base_url + "/real-wood",
            self.base_url + "/lvt"
        ]
        
        all_data = {
            'products': [],
            'images': [],
            'categories': [],
            'metadata': {
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'tileswoodfloorni.com',
                'ssl_bypassed': True
            }
        }
        
        for url in pages_to_try:
            print(f"Scraping: {url}")
            html_content = self.get_page_content(url)
            
            if html_content:
                # Extract images
                images = self.extract_images_from_js(html_content)
                all_data['images'].extend(images)
                
                # Extract product info
                products = self.extract_product_info_from_js(html_content)
                all_data['products'].extend(products)
                
                # Extract text content for product names/descriptions
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Look for product elements
                product_elements = soup.find_all(['div', 'article', 'section'], 
                                               class_=re.compile(r'product|item|tile|floor', re.I))
                
                for element in product_elements:
                    text = element.get_text(strip=True)
                    if len(text) > 10:  # Filter out empty or very short text
                        all_data['products'].append({
                            'type': 'text_content',
                            'content': text,
                            'url': url
                        })
        
        # Remove duplicates
        all_data['images'] = list(set(all_data['images']))
        
        return all_data
    
    def download_images(self, image_urls, max_images=50):
        """Download images and convert to base64"""
        downloaded_images = []
        
        for i, url in enumerate(image_urls[:max_images]):
            try:
                print(f"Downloading image {i+1}/{min(len(image_urls), max_images)}: {url}")
                
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
                        mime_type = 'image/jpeg'  # Default
                    
                    downloaded_images.append({
                        'url': url,
                        'base64': f"data:{mime_type};base64,{image_data}",
                        'size': len(response.content)
                    })
                    
            except Exception as e:
                print(f"Error downloading image {url}: {e}")
        
        return downloaded_images
    
    def save_results(self, data, filename="tileswoodfloorni_products.json"):
        """Save results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Results saved to {filename}")

def main():
    scraper = TilesWoodFloorScraper()
    
    # Scrape the website
    data = scraper.scrape_with_selenium()
    
    print(f"Found {len(data['products'])} product items")
    print(f"Found {len(data['images'])} image URLs")
    
    # Download images
    if data['images']:
        print("Downloading images...")
        downloaded_images = scraper.download_images(data['images'])
        data['downloaded_images'] = downloaded_images
        print(f"Downloaded {len(downloaded_images)} images")
    
    # Save results
    scraper.save_results(data)
    
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
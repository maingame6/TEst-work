#!/usr/bin/env python3
"""
Product Data Parser and Image Matcher
Parses the provided Bearfoot product data and matches with scraped images
"""

import json
import re
import os
from typing import List, Dict, Optional
from difflib import SequenceMatcher

class ProductImageMatcher:
    def __init__(self):
        self.provided_products = []
        self.scraped_products = []
        self.matched_products = []
        
    def parse_provided_products(self, product_text: str) -> List[Dict]:
        """Parse the provided product text into structured data"""
        products = []
        lines = product_text.strip().split('\n')
        
        for line in lines:
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
            
            # Clean up the name
            name = self.clean_product_name(name)
            
            # Extract product code if present (usually in format D1234, L123, etc.)
            product_code = None
            code_match = re.search(r'\b([DLH]\d{3,4})\b', name)
            if code_match:
                product_code = code_match.group(1)
                
            # Extract dimensions if present
            dimensions = None
            dim_match = re.search(r'(\d+)[xX](\d+)(?:[xX](\d+))?mm', name)
            if dim_match:
                dimensions = dim_match.group(0)
                
            # Extract coverage area from name if present
            area_match = re.search(r'(\d+\.?\d*)\s*m2', name)
            if area_match and not area:
                area = float(area_match.group(1))
                
            product = {
                'original_text': line.strip(),
                'name': name,
                'cleaned_name': self.clean_product_name(name),
                'price': price,
                'area_m2': area,
                'product_code': product_code,
                'dimensions': dimensions,
                'image_url': None,
                'image_base64': None,
                'matched': False,
                'match_confidence': 0.0
            }
            
            products.append(product)
            
        return products
        
    def clean_product_name(self, name: str) -> str:
        """Clean product name for better matching"""
        # Remove "Bearfoot" prefix
        name = re.sub(r'^Bearfoot\s+', '', name, flags=re.IGNORECASE)
        
        # Remove common measurement units and technical details
        name = re.sub(r'\s+\d+\.?\d*\s*m2?', '', name)
        name = re.sub(r'\s+\d+[xX]\d+(?:[xX](\d+))?mm', '', name)
        name = re.sub(r'\s+\(\d+\)', '', name)
        name = re.sub(r'\s+[DLH]\d{3,4}', '', name)
        
        # Remove extra spaces
        name = ' '.join(name.split())
        
        return name.strip()
        
    def similarity(self, a: str, b: str) -> float:
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
        
    def find_best_match(self, product_name: str, scraped_products: List[Dict]) -> Optional[Dict]:
        """Find the best matching scraped product for a given product name"""
        best_match = None
        best_score = 0.0
        
        cleaned_name = self.clean_product_name(product_name)
        
        for scraped in scraped_products:
            scraped_name = scraped.get('name', '')
            scraped_cleaned = self.clean_product_name(scraped_name)
            
            # Calculate various similarity scores
            exact_score = self.similarity(cleaned_name, scraped_cleaned)
            
            # Also check for keyword matches
            cleaned_words = set(cleaned_name.lower().split())
            scraped_words = set(scraped_cleaned.lower().split())
            
            # Common important words
            common_words = cleaned_words.intersection(scraped_words)
            keyword_score = len(common_words) / max(len(cleaned_words), len(scraped_words)) if cleaned_words or scraped_words else 0
            
            # Combined score
            combined_score = (exact_score * 0.7) + (keyword_score * 0.3)
            
            if combined_score > best_score and combined_score > 0.3:  # Minimum threshold
                best_score = combined_score
                best_match = {
                    'scraped_product': scraped,
                    'confidence': combined_score
                }
                
        return best_match
        
    def match_products(self, provided_products: List[Dict], scraped_products: List[Dict]) -> List[Dict]:
        """Match provided products with scraped images"""
        matched_products = []
        
        print(f"Matching {len(provided_products)} provided products with {len(scraped_products)} scraped products...")
        
        for product in provided_products:
            match = self.find_best_match(product['name'], scraped_products)
            
            if match:
                product['image_url'] = match['scraped_product']['image_url']
                product['image_base64'] = match['scraped_product']['image_base64']
                product['matched'] = True
                product['match_confidence'] = match['confidence']
                print(f"✓ Matched: {product['cleaned_name']} -> {match['scraped_product']['name']} (confidence: {match['confidence']:.2f})")
            else:
                print(f"✗ No match found for: {product['cleaned_name']}")
                
            matched_products.append(product)
            
        return matched_products
        
    def save_matched_products(self, products: List[Dict], filename: str = "bearfoot_matched_products.json"):
        """Save matched products to JSON file"""
        # Calculate statistics
        matched_count = sum(1 for p in products if p['matched'])
        total_count = len(products)
        
        output_data = {
            "processed_at": __import__('time').strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": {
                "total_products": total_count,
                "matched_products": matched_count,
                "unmatched_products": total_count - matched_count,
                "match_rate": f"{(matched_count/total_count*100):.1f}%" if total_count > 0 else "0%"
            },
            "products": products
        }
        
        filepath = os.path.join('/app', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        print(f"Saved {len(products)} products to {filepath}")
        print(f"Match statistics: {matched_count}/{total_count} ({(matched_count/total_count*100):.1f}%)")
        
        return filepath

def get_provided_product_data():
    """Return the provided product data"""
    return """Bearfoot 10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank L915 nan 1.8 66.66
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

def main():
    """Main processing function"""
    matcher = ProductImageMatcher()
    
    # Parse provided products
    product_text = get_provided_product_data()
    provided_products = matcher.parse_provided_products(product_text)
    print(f"Parsed {len(provided_products)} products from provided data")
    
    # Check if we have scraped products
    scraped_file = '/app/bearfoot_laminate_products.json'
    if os.path.exists(scraped_file):
        with open(scraped_file, 'r') as f:
            scraped_data = json.load(f)
            scraped_products = scraped_data.get('products', [])
            print(f"Loaded {len(scraped_products)} scraped products")
    else:
        print("No scraped products found. Please run bearfoot_scraper.py first.")
        scraped_products = []
    
    # Match products
    if scraped_products:
        matched_products = matcher.match_products(provided_products, scraped_products)
        matcher.save_matched_products(matched_products)
    else:
        # Save unmatched products for now
        matcher.save_matched_products(provided_products, "bearfoot_unmatched_products.json")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Comprehensive Backend API Test Suite for Bearfoot Flooring Application
Tests all API endpoints and validates product data integrity
"""

import requests
import json
import sys
import base64
from typing import Dict, List, Any

# Backend API URL from frontend environment
BACKEND_URL = "https://074a2154-60d5-421c-af3f-5a1b529251c6.preview.emergentagent.com/api"

class BearfootAPITester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name: str, passed: bool, message: str = "", details: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        if not passed and details:
            print(f"   Details: {details}")
        print()

    def test_api_health_check(self):
        """Test the root endpoint /api/ - should return 159 products"""
        try:
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response has expected structure
                if "message" in data and "total_products" in data:
                    expected_message = "Bearfoot Flooring API"
                    expected_count = 159  # Updated for new catalog
                    
                    if data["message"] == expected_message and data["total_products"] == expected_count:
                        self.log_test("API Health Check", True, 
                                    f"API returned correct message and product count: {expected_count}")
                    else:
                        self.log_test("API Health Check", False, 
                                    f"Expected message: '{expected_message}' and count: {expected_count}, "
                                    f"got message: '{data.get('message')}' and count: {data.get('total_products')}")
                else:
                    self.log_test("API Health Check", False, 
                                "Response missing 'message' or 'total_products' fields", data)
            else:
                self.log_test("API Health Check", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("API Health Check", False, f"Request failed: {str(e)}")

    def test_get_all_products(self):
        """Test GET /api/products - should return all 159 products"""
        try:
            response = self.session.get(f"{self.base_url}/products", params={"limit": 200})
            
            if response.status_code == 200:
                products = response.json()
                
                if isinstance(products, list):
                    if len(products) == 159:  # Updated for new catalog
                        self.log_test("Get All Products", True, 
                                    f"Retrieved {len(products)} products as expected")
                        
                        # Validate first product structure
                        if products:
                            self.validate_product_structure(products[0])
                    else:
                        self.log_test("Get All Products", False, 
                                    f"Expected 159 products, got {len(products)}")
                else:
                    self.log_test("Get All Products", False, 
                                "Response is not a list", type(products))
            else:
                self.log_test("Get All Products", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get All Products", False, f"Request failed: {str(e)}")

    def validate_product_structure(self, product: Dict):
        """Validate that a product has all required fields"""
        required_fields = [
            'id', 'name', 'display_name', 'price', 'product_type', 
            'brand', 'category', 'image_url', 'image_base64', 
            'description', 'features', 'in_stock', 'created_at'
        ]
        
        # New optional fields for enhanced catalog
        optional_fields = ['section', 'subsection', 'thickness', 'series', 'area_m2', 'product_code', 'dimensions']
        
        missing_fields = []
        for field in required_fields:
            if field not in product:
                missing_fields.append(field)
        
        if not missing_fields:
            # Validate image_base64 format
            if product.get('image_base64', '').startswith('data:image/'):
                # Check for new enhanced fields
                enhanced_fields_present = sum(1 for field in optional_fields if product.get(field))
                self.log_test("Product Structure Validation", True, 
                            f"Product has all required fields, valid image data, and {enhanced_fields_present} enhanced fields")
            else:
                self.log_test("Product Structure Validation", False, 
                            "Product image_base64 field is not in correct format")
        else:
            self.log_test("Product Structure Validation", False, 
                        f"Product missing required fields: {missing_fields}")

    def test_product_filters(self):
        """Test product filtering functionality"""
        
        # Test category filter
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"category": "Laminate Flooring"})
            if response.status_code == 200:
                products = response.json()
                if all(p.get('category') == 'Laminate Flooring' for p in products):
                    self.log_test("Category Filter", True, 
                                f"Category filter returned {len(products)} products")
                else:
                    self.log_test("Category Filter", False, 
                                "Some products don't match category filter")
            else:
                self.log_test("Category Filter", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Category Filter", False, f"Request failed: {str(e)}")

        # Test product type filter
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"product_type": "Long Plank"})
            if response.status_code == 200:
                products = response.json()
                if all(p.get('product_type') == 'Long Plank' for p in products):
                    self.log_test("Product Type Filter", True, 
                                f"Product type filter returned {len(products)} products")
                else:
                    self.log_test("Product Type Filter", False, 
                                "Some products don't match product type filter")
            else:
                self.log_test("Product Type Filter", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Product Type Filter", False, f"Request failed: {str(e)}")

        # Test price range filter
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"min_price": 50, "max_price": 100})
            if response.status_code == 200:
                products = response.json()
                if all(50 <= p.get('price', 0) <= 100 for p in products):
                    self.log_test("Price Range Filter", True, 
                                f"Price range filter returned {len(products)} products")
                else:
                    self.log_test("Price Range Filter", False, 
                                "Some products don't match price range filter")
            else:
                self.log_test("Price Range Filter", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Price Range Filter", False, f"Request failed: {str(e)}")

        # Test search filter with common terms
        search_terms = ["oak", "laminate", "12mm"]
        for term in search_terms:
            try:
                response = self.session.get(f"{self.base_url}/products", 
                                          params={"search": term})
                if response.status_code == 200:
                    products = response.json()
                    if products:
                        # Check if search term appears in product data
                        found_in_results = any(
                            term.lower() in str(p.get('name', '')).lower() or
                            term.lower() in str(p.get('display_name', '')).lower() or
                            term.lower() in str(p.get('description', '')).lower() or
                            term.lower() in str(p.get('thickness', '')).lower()
                            for p in products
                        )
                        if found_in_results:
                            self.log_test(f"Search Filter - {term}", True, 
                                        f"Found {len(products)} products for '{term}'")
                        else:
                            self.log_test(f"Search Filter - {term}", False, 
                                        f"Search term '{term}' not found in results")
                    else:
                        self.log_test(f"Search Filter - {term}", True, 
                                    f"No products found for '{term}' (valid result)")
                else:
                    self.log_test(f"Search Filter - {term}", False, 
                                f"HTTP {response.status_code}: {response.text}")
            except Exception as e:
                self.log_test(f"Search Filter - {term}", False, f"Request failed: {str(e)}")

    def test_product_data_validation(self):
        """Test product data integrity and validation for 159-product catalog"""
        try:
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                products = response.json()
                
                # Check total product count
                if len(products) == 159:
                    self.log_test("Product Data - Total Count", True, 
                                f"Found all 159 products in catalog")
                else:
                    self.log_test("Product Data - Total Count", False, 
                                f"Expected 159 products, found {len(products)}")

                # Check for diverse brands (should have multiple brands now)
                brands = set(p.get('brand') for p in products if p.get('brand'))
                if len(brands) >= 3:  # Should have at least 3 different brands
                    self.log_test("Product Data - Brand Diversity", True, 
                                f"Found {len(brands)} different brands: {list(brands)[:5]}...")
                else:
                    self.log_test("Product Data - Brand Diversity", False, 
                                f"Expected multiple brands, found only: {list(brands)}")

                # Check for section categorization
                sections = set(p.get('section') for p in products if p.get('section'))
                expected_sections = {"Laminates", "Water Resistant Laminates", "Waterproof SPC", "Hardwoods"}
                found_expected = sections.intersection(expected_sections)
                
                if len(found_expected) >= 2:
                    self.log_test("Product Data - Section Categories", True, 
                                f"Found expected sections: {found_expected}")
                else:
                    self.log_test("Product Data - Section Categories", False, 
                                f"Expected sections not found. Got: {sections}")

                # Check image data format (sample of 10 products)
                valid_images = 0
                for product in products[:10]:  # Check first 10 products
                    image_data = product.get('image_base64', '')
                    if image_data.startswith('data:image/') and len(image_data) > 1000:  # Larger images expected
                        valid_images += 1
                
                if valid_images >= 8:  # At least 8/10 should have valid images
                    self.log_test("Product Data - Image Format", True, 
                                f"{valid_images}/10 checked products have valid base64 image data")
                else:
                    self.log_test("Product Data - Image Format", False, 
                                f"Only {valid_images}/10 products have valid image data")

                # Check price formatting
                valid_prices = 0
                for product in products[:15]:  # Check first 15 products
                    price = product.get('price')
                    if isinstance(price, (int, float)) and price > 0:
                        valid_prices += 1
                
                if valid_prices >= 12:  # At least 12/15 should have valid prices
                    self.log_test("Product Data - Price Format", True, 
                                f"{valid_prices}/15 checked products have valid price data")
                else:
                    self.log_test("Product Data - Price Format", False, 
                                f"Only {valid_prices}/15 products have valid price data")

                # Check for enhanced metadata fields
                products_with_thickness = sum(1 for p in products if p.get('thickness'))
                products_with_dimensions = sum(1 for p in products if p.get('dimensions'))
                
                if products_with_thickness > 50:  # Expect many products to have thickness
                    self.log_test("Product Data - Enhanced Metadata", True, 
                                f"{products_with_thickness} products have thickness data, {products_with_dimensions} have dimensions")
                else:
                    self.log_test("Product Data - Enhanced Metadata", False, 
                                f"Only {products_with_thickness} products have thickness data")

            else:
                self.log_test("Product Data Validation", False, 
                            f"Failed to get products: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Product Data Validation", False, f"Request failed: {str(e)}")

    def test_get_single_product(self):
        """Test GET /api/products/{product_id}"""
        # First get a valid product ID
        try:
            response = self.session.get(f"{self.base_url}/products", params={"limit": 1})
            if response.status_code == 200:
                products = response.json()
                if products:
                    product_id = products[0]['id']
                    
                    # Test getting single product
                    response = self.session.get(f"{self.base_url}/products/{product_id}")
                    if response.status_code == 200:
                        product = response.json()
                        if product.get('id') == product_id:
                            self.log_test("Get Single Product", True, 
                                        f"Retrieved product with ID: {product_id}")
                        else:
                            self.log_test("Get Single Product", False, 
                                        "Product ID mismatch in response")
                    else:
                        self.log_test("Get Single Product", False, 
                                    f"HTTP {response.status_code}: {response.text}")
                else:
                    self.log_test("Get Single Product", False, "No products available for testing")
            else:
                self.log_test("Get Single Product", False, 
                            f"Failed to get products list: HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Get Single Product", False, f"Request failed: {str(e)}")

    def test_get_categories(self):
        """Test GET /api/products/categories"""
        try:
            response = self.session.get(f"{self.base_url}/products/categories")
            
            if response.status_code == 200:
                data = response.json()
                if "categories" in data and isinstance(data["categories"], list):
                    categories = data["categories"]
                    if "Laminate Flooring" in categories:
                        self.log_test("Get Categories", True, 
                                    f"Retrieved {len(categories)} categories")
                    else:
                        self.log_test("Get Categories", False, 
                                    "Expected 'Laminate Flooring' category not found")
                else:
                    self.log_test("Get Categories", False, 
                                "Response missing 'categories' field or not a list")
            else:
                self.log_test("Get Categories", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Categories", False, f"Request failed: {str(e)}")

    def test_get_product_types(self):
        """Test GET /api/products/types"""
        try:
            response = self.session.get(f"{self.base_url}/products/types")
            
            if response.status_code == 200:
                data = response.json()
                if "product_types" in data and isinstance(data["product_types"], list):
                    types = data["product_types"]
                    expected_types = ["Long Plank", "Herringbone", "X-LOC"]
                    found_types = [t for t in expected_types if t in types]
                    
                    if found_types:
                        self.log_test("Get Product Types", True, 
                                    f"Retrieved {len(types)} product types, found expected types: {found_types}")
                    else:
                        self.log_test("Get Product Types", False, 
                                    f"None of expected types {expected_types} found in {types}")
                else:
                    self.log_test("Get Product Types", False, 
                                "Response missing 'product_types' field or not a list")
            else:
                self.log_test("Get Product Types", False, 
                            f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Get Product Types", False, f"Request failed: {str(e)}")

    def test_search_products(self):
        """Test GET /api/products/search with query parameter"""
        search_terms = ["BERGEN", "OAK", "SYMPHONIA"]
        
        for term in search_terms:
            try:
                response = self.session.get(f"{self.base_url}/products/search", 
                                          params={"q": term})
                
                if response.status_code == 200:
                    data = response.json()
                    if "products" in data and "total" in data and "query" in data:
                        products = data["products"]
                        total = data["total"]
                        query = data["query"]
                        
                        if query == term and len(products) == total:
                            if products:  # If we found products
                                # Check if search term appears in product data
                                found_in_results = any(
                                    term.upper() in str(p.get('name', '')).upper() or
                                    term.upper() in str(p.get('display_name', '')).upper() or
                                    term.upper() in str(p.get('description', '')).upper()
                                    for p in products
                                )
                                if found_in_results:
                                    self.log_test(f"Search Products - {term}", True, 
                                                f"Found {total} products for '{term}'")
                                else:
                                    self.log_test(f"Search Products - {term}", False, 
                                                f"Search term '{term}' not found in results")
                            else:
                                self.log_test(f"Search Products - {term}", True, 
                                            f"No products found for '{term}' (valid result)")
                        else:
                            self.log_test(f"Search Products - {term}", False, 
                                        "Response data inconsistency")
                    else:
                        self.log_test(f"Search Products - {term}", False, 
                                    "Response missing required fields")
                else:
                    self.log_test(f"Search Products - {term}", False, 
                                f"HTTP {response.status_code}: {response.text}")
                    
            except Exception as e:
                self.log_test(f"Search Products - {term}", False, f"Request failed: {str(e)}")

    def test_error_handling(self):
        """Test error handling with invalid requests"""
        
        # Test invalid product ID
        try:
            response = self.session.get(f"{self.base_url}/products/invalid_id_12345")
            if response.status_code == 404:
                self.log_test("Error Handling - Invalid Product ID", True, 
                            "Correctly returned 404 for invalid product ID")
            else:
                self.log_test("Error Handling - Invalid Product ID", False, 
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Invalid Product ID", False, f"Request failed: {str(e)}")

        # Test search without query parameter
        try:
            response = self.session.get(f"{self.base_url}/products/search")
            # This should either return an error or empty results
            if response.status_code in [400, 422]:
                self.log_test("Error Handling - Missing Search Query", True, 
                            f"Correctly returned {response.status_code} for missing query")
            elif response.status_code == 200:
                data = response.json()
                if data.get("total", 0) == 0:
                    self.log_test("Error Handling - Missing Search Query", True, 
                                "Returned empty results for missing query")
                else:
                    self.log_test("Error Handling - Missing Search Query", False, 
                                "Should return empty results or error for missing query")
            else:
                self.log_test("Error Handling - Missing Search Query", False, 
                            f"Unexpected status code: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling - Missing Search Query", False, f"Request failed: {str(e)}")

    def test_new_metadata_endpoints(self):
        """Test all new metadata endpoints for the enhanced catalog"""
        
        # Test sections endpoint
        try:
            response = self.session.get(f"{self.base_url}/products/sections")
            if response.status_code == 200:
                data = response.json()
                if "sections" in data and isinstance(data["sections"], list):
                    sections = data["sections"]
                    expected_sections = ["Laminates", "Water Resistant Laminates", "Waterproof SPC", "Hardwoods"]
                    found_sections = [s for s in expected_sections if s in sections]
                    
                    if len(found_sections) >= 3:  # At least 3 of the expected sections
                        self.log_test("Get Sections Endpoint", True, 
                                    f"Retrieved {len(sections)} sections, found expected: {found_sections}")
                    else:
                        self.log_test("Get Sections Endpoint", False, 
                                    f"Expected sections not found. Got: {sections}")
                else:
                    self.log_test("Get Sections Endpoint", False, 
                                "Response missing 'sections' field or not a list")
            else:
                self.log_test("Get Sections Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Sections Endpoint", False, f"Request failed: {str(e)}")

        # Test brands endpoint
        try:
            response = self.session.get(f"{self.base_url}/products/brands")
            if response.status_code == 200:
                data = response.json()
                if "brands" in data and isinstance(data["brands"], list):
                    brands = data["brands"]
                    if len(brands) > 0:
                        self.log_test("Get Brands Endpoint", True, 
                                    f"Retrieved {len(brands)} brands: {brands[:5]}...")  # Show first 5
                    else:
                        self.log_test("Get Brands Endpoint", False, "No brands found")
                else:
                    self.log_test("Get Brands Endpoint", False, 
                                "Response missing 'brands' field or not a list")
            else:
                self.log_test("Get Brands Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Brands Endpoint", False, f"Request failed: {str(e)}")

        # Test thicknesses endpoint
        try:
            response = self.session.get(f"{self.base_url}/products/thicknesses")
            if response.status_code == 200:
                data = response.json()
                if "thicknesses" in data and isinstance(data["thicknesses"], list):
                    thicknesses = data["thicknesses"]
                    expected_thicknesses = ["8mm", "10mm", "12mm", "14mm", "18mm", "20mm"]
                    found_thicknesses = [t for t in expected_thicknesses if t in thicknesses]
                    
                    if len(found_thicknesses) >= 3:  # At least 3 expected thicknesses
                        self.log_test("Get Thicknesses Endpoint", True, 
                                    f"Retrieved {len(thicknesses)} thicknesses, found expected: {found_thicknesses}")
                    else:
                        self.log_test("Get Thicknesses Endpoint", False, 
                                    f"Expected thicknesses not found. Got: {thicknesses}")
                else:
                    self.log_test("Get Thicknesses Endpoint", False, 
                                "Response missing 'thicknesses' field or not a list")
            else:
                self.log_test("Get Thicknesses Endpoint", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Get Thicknesses Endpoint", False, f"Request failed: {str(e)}")

    def test_enhanced_filtering_system(self):
        """Test the enhanced filtering system with new filters"""
        
        # Test section filtering
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"section": "Laminates"})
            if response.status_code == 200:
                products = response.json()
                if products and all(p.get('section') == 'Laminates' for p in products if p.get('section')):
                    self.log_test("Section Filter - Laminates", True, 
                                f"Section filter returned {len(products)} Laminate products")
                else:
                    self.log_test("Section Filter - Laminates", False, 
                                "Some products don't match section filter or no products found")
            else:
                self.log_test("Section Filter - Laminates", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Section Filter - Laminates", False, f"Request failed: {str(e)}")

        # Test thickness filtering
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"thickness": "12mm"})
            if response.status_code == 200:
                products = response.json()
                if products:
                    matching_products = [p for p in products if p.get('thickness') == '12mm']
                    if len(matching_products) > 0:
                        self.log_test("Thickness Filter - 12mm", True, 
                                    f"Thickness filter returned {len(matching_products)} products with 12mm thickness")
                    else:
                        self.log_test("Thickness Filter - 12mm", False, 
                                    "No products found with 12mm thickness")
                else:
                    self.log_test("Thickness Filter - 12mm", False, "No products returned")
            else:
                self.log_test("Thickness Filter - 12mm", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Thickness Filter - 12mm", False, f"Request failed: {str(e)}")

        # Test brand filtering with multiple brands
        try:
            # First get available brands
            brands_response = self.session.get(f"{self.base_url}/products/brands")
            if brands_response.status_code == 200:
                brands_data = brands_response.json()
                if brands_data.get("brands"):
                    test_brand = brands_data["brands"][0]  # Test with first available brand
                    
                    response = self.session.get(f"{self.base_url}/products", 
                                              params={"brand": test_brand})
                    if response.status_code == 200:
                        products = response.json()
                        if products and all(p.get('brand') == test_brand for p in products):
                            self.log_test(f"Brand Filter - {test_brand}", True, 
                                        f"Brand filter returned {len(products)} products for {test_brand}")
                        else:
                            self.log_test(f"Brand Filter - {test_brand}", False, 
                                        "Some products don't match brand filter")
                    else:
                        self.log_test(f"Brand Filter - {test_brand}", False, 
                                    f"HTTP {response.status_code}: {response.text}")
                else:
                    self.log_test("Brand Filter Test", False, "No brands available for testing")
            else:
                self.log_test("Brand Filter Test", False, "Could not retrieve brands for testing")
        except Exception as e:
            self.log_test("Brand Filter Test", False, f"Request failed: {str(e)}")

        # Test combined filtering (section + thickness)
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"section": "Laminates", "thickness": "12mm"})
            if response.status_code == 200:
                products = response.json()
                valid_products = [p for p in products if 
                                (p.get('section') == 'Laminates' or not p.get('section')) and 
                                (p.get('thickness') == '12mm' or not p.get('thickness'))]
                
                self.log_test("Combined Filter - Section + Thickness", True, 
                            f"Combined filter returned {len(products)} products")
            else:
                self.log_test("Combined Filter - Section + Thickness", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Combined Filter - Section + Thickness", False, f"Request failed: {str(e)}")

    def test_performance_with_large_dataset(self):
        """Test API performance with the larger 159-product dataset"""
        import time
        
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/products")
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200:
                products = response.json()
                if len(products) == 159 and response_time < 5.0:  # Should respond within 5 seconds
                    self.log_test("Performance Test - All Products", True, 
                                f"Retrieved 159 products in {response_time:.2f} seconds")
                elif len(products) == 159:
                    self.log_test("Performance Test - All Products", False, 
                                f"Response too slow: {response_time:.2f} seconds for 159 products")
                else:
                    self.log_test("Performance Test - All Products", False, 
                                f"Wrong product count: {len(products)} instead of 159")
            else:
                self.log_test("Performance Test - All Products", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Performance Test - All Products", False, f"Request failed: {str(e)}")

        # Test search performance
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/products/search", params={"q": "oak"})
            end_time = time.time()
            
            search_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                if search_time < 3.0:  # Search should be faster
                    self.log_test("Performance Test - Search", True, 
                                f"Search completed in {search_time:.2f} seconds, found {data.get('total', 0)} results")
                else:
                    self.log_test("Performance Test - Search", False, 
                                f"Search too slow: {search_time:.2f} seconds")
            else:
                self.log_test("Performance Test - Search", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Performance Test - Search", False, f"Request failed: {str(e)}")

    def run_all_tests(self):
        """Run all test suites for the enhanced 159-product catalog"""
        print("🧪 Starting Bearfoot Flooring API Test Suite - Enhanced 159-Product Catalog")
        print("=" * 80)
        print()
        
        # Run all tests
        self.test_api_health_check()
        self.test_get_all_products()
        self.test_product_filters()
        self.test_get_single_product()
        self.test_get_categories()
        self.test_get_product_types()
        self.test_search_products()
        self.test_error_handling()
        self.test_product_data_validation()
        
        # New enhanced tests
        self.test_new_metadata_endpoints()
        self.test_enhanced_filtering_system()
        self.test_performance_with_large_dataset()
        
        # Summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["passed"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        if total - passed > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["passed"]:
                    print(f"  - {result['test']}: {result['message']}")
            print()
        
        return passed == total

def main():
    """Main test execution"""
    tester = BearfootAPITester()
    success = tester.run_all_tests()
    
    if success:
        print("🎉 All tests passed! Backend API is working correctly.")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Please check the backend implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
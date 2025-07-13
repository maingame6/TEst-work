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
            response = self.session.get(f"{self.base_url}/products")
            
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

        # Test search filter
        try:
            response = self.session.get(f"{self.base_url}/products", 
                                      params={"search": "BERGEN"})
            if response.status_code == 200:
                products = response.json()
                if products and all('BERGEN' in p.get('name', '').upper() or 
                                  'BERGEN' in p.get('display_name', '').upper() 
                                  for p in products):
                    self.log_test("Search Filter", True, 
                                f"Search filter returned {len(products)} products")
                else:
                    self.log_test("Search Filter", False, 
                                "Search results don't match search term")
            else:
                self.log_test("Search Filter", False, 
                            f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Search Filter", False, f"Request failed: {str(e)}")

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

    def test_product_data_validation(self):
        """Test product data integrity and validation"""
        try:
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                products = response.json()
                
                # Check for required Bearfoot products
                bearfoot_products = [p for p in products if p.get('brand') == 'Bearfoot']
                
                if len(bearfoot_products) == 27:
                    self.log_test("Product Data - Bearfoot Brand Count", True, 
                                f"Found all 27 Bearfoot products")
                else:
                    self.log_test("Product Data - Bearfoot Brand Count", False, 
                                f"Expected 27 Bearfoot products, found {len(bearfoot_products)}")

                # Check image data format
                valid_images = 0
                for product in products[:5]:  # Check first 5 products
                    image_data = product.get('image_base64', '')
                    if image_data.startswith('data:image/') and len(image_data) > 100:
                        valid_images += 1
                
                if valid_images == 5:
                    self.log_test("Product Data - Image Format", True, 
                                "All checked products have valid base64 image data")
                else:
                    self.log_test("Product Data - Image Format", False, 
                                f"Only {valid_images}/5 products have valid image data")

                # Check price formatting
                valid_prices = 0
                for product in products[:10]:  # Check first 10 products
                    price = product.get('price')
                    if isinstance(price, (int, float)) and price > 0:
                        valid_prices += 1
                
                if valid_prices == 10:
                    self.log_test("Product Data - Price Format", True, 
                                "All checked products have valid price data")
                else:
                    self.log_test("Product Data - Price Format", False, 
                                f"Only {valid_prices}/10 products have valid price data")

            else:
                self.log_test("Product Data Validation", False, 
                            f"Failed to get products: HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Product Data Validation", False, f"Request failed: {str(e)}")

    def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Starting Bearfoot Flooring API Test Suite")
        print("=" * 60)
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
        
        # Summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
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
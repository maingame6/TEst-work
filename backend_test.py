#!/usr/bin/env python3
"""
Backend API Testing Script for Tiles & Wood Flooring Website
Tests all backend endpoints as specified in the review request.
"""

import requests
import json
import sys
import os
from typing import Dict, Any, Optional

# Get the backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

BACKEND_URL = get_backend_url()
if not BACKEND_URL:
    print("ERROR: Could not get backend URL from frontend/.env")
    sys.exit(1)

API_BASE = f"{BACKEND_URL}/api"
print(f"Testing backend API at: {API_BASE}")

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = {
            "health": {"status": "PENDING", "details": ""},
            "products": {"status": "PENDING", "details": ""},
            "auth_login": {"status": "PENDING", "details": ""},
            "suppliers": {"status": "PENDING", "details": ""},
            "categories": {"status": "PENDING", "details": ""},
            "admin_stats": {"status": "PENDING", "details": ""}
        }
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with error handling"""
        url = f"{API_BASE}{endpoint}"
        try:
            response = self.session.request(method, url, timeout=30, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {method} {url}: {e}")
            return None
    
    def test_health_endpoint(self):
        """Test /api/health endpoint"""
        print("\n=== Testing Health Endpoint ===")
        
        response = self.make_request("GET", "/health")
        if not response:
            self.test_results["health"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to health endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if data.get("status") == "healthy":
                    self.test_results["health"] = {
                        "status": "PASSED", 
                        "details": f"Health check returned status: {data.get('status')}"
                    }
                else:
                    self.test_results["health"] = {
                        "status": "FAILED", 
                        "details": f"Expected status 'healthy', got: {data.get('status')}"
                    }
            except json.JSONDecodeError:
                self.test_results["health"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from health endpoint"
                }
        else:
            self.test_results["health"] = {
                "status": "FAILED", 
                "details": f"Expected status 200, got {response.status_code}"
            }
    
    def test_products_endpoint(self):
        """Test /api/products endpoint"""
        print("\n=== Testing Products Endpoint ===")
        
        response = self.make_request("GET", "/products")
        if not response:
            self.test_results["products"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to products endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                products = response.json()
                print(f"Found {len(products)} products")
                
                if len(products) > 0:
                    # Check for products from both sources
                    suppliers = set(product.get("supplier", "") for product in products)
                    print(f"Suppliers found: {list(suppliers)}")
                    
                    # Expected suppliers from migration
                    expected_suppliers = ["Bearfoot", "V8 Allstyle", "Tiles & Wood Floor Store"]
                    found_suppliers = [s for s in expected_suppliers if s in suppliers]
                    
                    # Show sample products
                    print("\nSample products:")
                    for i, product in enumerate(products[:3]):
                        print(f"  {i+1}. {product.get('name')} - {product.get('supplier')} - £{product.get('price')}")
                    
                    if len(found_suppliers) >= 2:  # At least 2 of the expected suppliers
                        self.test_results["products"] = {
                            "status": "PASSED", 
                            "details": f"Found {len(products)} products from suppliers: {list(suppliers)}"
                        }
                    else:
                        self.test_results["products"] = {
                            "status": "FAILED", 
                            "details": f"Expected suppliers from both sources, found: {list(suppliers)}"
                        }
                else:
                    self.test_results["products"] = {
                        "status": "FAILED", 
                        "details": "No products found - data migration may have failed"
                    }
            except json.JSONDecodeError:
                self.test_results["products"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from products endpoint"
                }
        else:
            self.test_results["products"] = {
                "status": "FAILED", 
                "details": f"Expected status 200, got {response.status_code}"
            }
    
    def test_auth_login(self):
        """Test /api/auth/login endpoint with admin/admin123"""
        print("\n=== Testing Authentication Endpoint ===")
        
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = self.make_request("POST", "/auth/login", json=login_data)
        if not response:
            self.test_results["auth_login"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to auth endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                if "access_token" in data and data.get("token_type") == "bearer":
                    self.auth_token = data["access_token"]
                    self.test_results["auth_login"] = {
                        "status": "PASSED", 
                        "details": "Successfully authenticated with admin/admin123"
                    }
                else:
                    self.test_results["auth_login"] = {
                        "status": "FAILED", 
                        "details": "Login response missing access_token or incorrect token_type"
                    }
            except json.JSONDecodeError:
                self.test_results["auth_login"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from auth endpoint"
                }
        else:
            try:
                error_data = response.json()
                self.test_results["auth_login"] = {
                    "status": "FAILED", 
                    "details": f"Authentication failed: {error_data.get('detail', 'Unknown error')}"
                }
            except:
                self.test_results["auth_login"] = {
                    "status": "FAILED", 
                    "details": f"Authentication failed with status {response.status_code}"
                }
    
    def test_suppliers_endpoint(self):
        """Test /api/suppliers endpoint"""
        print("\n=== Testing Suppliers Endpoint ===")
        
        response = self.make_request("GET", "/suppliers")
        if not response:
            self.test_results["suppliers"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to suppliers endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                suppliers = data.get("suppliers", [])
                print(f"Response: {json.dumps(data, indent=2)}")
                
                expected_suppliers = ["Bearfoot", "V8 Allstyle", "Tiles & Wood Floor Store"]
                found_suppliers = [s for s in expected_suppliers if s in suppliers]
                
                if len(found_suppliers) >= 2:  # At least 2 expected suppliers
                    self.test_results["suppliers"] = {
                        "status": "PASSED", 
                        "details": f"Found suppliers: {suppliers}"
                    }
                else:
                    self.test_results["suppliers"] = {
                        "status": "FAILED", 
                        "details": f"Expected suppliers {expected_suppliers}, found: {suppliers}"
                    }
            except json.JSONDecodeError:
                self.test_results["suppliers"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from suppliers endpoint"
                }
        else:
            self.test_results["suppliers"] = {
                "status": "FAILED", 
                "details": f"Expected status 200, got {response.status_code}"
            }
    
    def test_categories_endpoint(self):
        """Test /api/categories endpoint"""
        print("\n=== Testing Categories Endpoint ===")
        
        response = self.make_request("GET", "/categories")
        if not response:
            self.test_results["categories"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to categories endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                categories = data.get("categories", [])
                print(f"Response: {json.dumps(data, indent=2)}")
                
                # Check for flooring and tile categories
                flooring_categories = [c for c in categories if "flooring" in c.lower() or "laminate" in c.lower()]
                tile_categories = [c for c in categories if "tile" in c.lower()]
                
                if len(categories) > 0 and (flooring_categories or tile_categories):
                    self.test_results["categories"] = {
                        "status": "PASSED", 
                        "details": f"Found {len(categories)} categories including flooring and tile categories"
                    }
                else:
                    self.test_results["categories"] = {
                        "status": "FAILED", 
                        "details": f"Expected flooring and tile categories, found: {categories}"
                    }
            except json.JSONDecodeError:
                self.test_results["categories"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from categories endpoint"
                }
        else:
            self.test_results["categories"] = {
                "status": "FAILED", 
                "details": f"Expected status 200, got {response.status_code}"
            }
    
    def test_admin_stats_endpoint(self):
        """Test /api/admin/stats endpoint (requires authentication)"""
        print("\n=== Testing Admin Stats Endpoint ===")
        
        if not self.auth_token:
            self.test_results["admin_stats"] = {
                "status": "FAILED", 
                "details": "Cannot test admin stats - authentication failed"
            }
            return
        
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        response = self.make_request("GET", "/admin/stats", headers=headers)
        
        if not response:
            self.test_results["admin_stats"] = {
                "status": "FAILED", 
                "details": "Request failed - could not connect to admin stats endpoint"
            }
            return
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
                
                required_fields = ["total_products", "in_stock_products", "total_suppliers", "total_categories"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields and data.get("total_products", 0) > 0:
                    self.test_results["admin_stats"] = {
                        "status": "PASSED", 
                        "details": f"Stats: {data.get('total_products')} products, {data.get('total_suppliers')} suppliers, {data.get('total_categories')} categories"
                    }
                else:
                    self.test_results["admin_stats"] = {
                        "status": "FAILED", 
                        "details": f"Missing fields: {missing_fields} or no products found"
                    }
            except json.JSONDecodeError:
                self.test_results["admin_stats"] = {
                    "status": "FAILED", 
                    "details": "Invalid JSON response from admin stats endpoint"
                }
        elif response.status_code == 401:
            self.test_results["admin_stats"] = {
                "status": "FAILED", 
                "details": "Authentication failed for admin stats endpoint"
            }
        else:
            self.test_results["admin_stats"] = {
                "status": "FAILED", 
                "details": f"Expected status 200, got {response.status_code}"
            }
    
    def run_all_tests(self):
        """Run all backend API tests"""
        print("Starting Backend API Tests...")
        print(f"Backend URL: {API_BASE}")
        
        # Test endpoints in order
        self.test_health_endpoint()
        self.test_products_endpoint()
        self.test_auth_login()
        self.test_suppliers_endpoint()
        self.test_categories_endpoint()
        self.test_admin_stats_endpoint()
        
        # Print summary
        print("\n" + "="*60)
        print("BACKEND API TEST RESULTS SUMMARY")
        print("="*60)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.test_results.items():
            status = result["status"]
            details = result["details"]
            
            if status == "PASSED":
                print(f"✅ {test_name.upper()}: {status}")
                passed += 1
            elif status == "FAILED":
                print(f"❌ {test_name.upper()}: {status}")
                print(f"   Details: {details}")
                failed += 1
            else:
                print(f"⏳ {test_name.upper()}: {status}")
        
        print(f"\nTotal: {passed} passed, {failed} failed")
        
        return passed, failed

if __name__ == "__main__":
    tester = BackendTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)
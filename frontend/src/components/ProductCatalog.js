import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProductCatalog = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    supplier: '',
    category: '',
    search: '',
    min_price: '',
    max_price: ''
  });
  const [suppliers, setSuppliers] = useState([]);
  const [categories, setCategories] = useState([]);

  // Fetch products
  const fetchProducts = async (queryParams = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(queryParams).forEach(([key, value]) => {
        if (value && value !== '') {
          params.append(key, value);
        }
      });
      
      const response = await axios.get(`${API}/products?${params}&limit=1000`);
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch products');
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch suppliers and categories
  const fetchFilters = async () => {
    try {
      const [suppliersRes, categoriesRes] = await Promise.all([
        axios.get(`${API}/suppliers`),
        axios.get(`${API}/categories`)
      ]);
      setSuppliers(suppliersRes.data.suppliers || []);
      setCategories(categoriesRes.data.categories || []);
    } catch (err) {
      console.error('Error fetching filters:', err);
    }
  };

  useEffect(() => {
    fetchProducts();
    fetchFilters();
  }, []);

  // Handle filter changes
  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    fetchProducts(newFilters);
  };

  // Clear filters
  const clearFilters = () => {
    setFilters({
      supplier: '',
      category: '',
      search: '',
      min_price: '',
      max_price: ''
    });
    fetchProducts();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-100">
        <div className="text-red-600 text-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Product Catalog</h1>
          <p className="mt-2 text-gray-600">Discover our premium tiles and flooring solutions</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <h2 className="text-lg font-semibold mb-4">Filters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
              <input
                type="text"
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                placeholder="Search products..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Supplier</label>
              <select
                value={filters.supplier}
                onChange={(e) => handleFilterChange('supplier', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">All Suppliers</option>
                {suppliers.map(supplier => (
                  <option key={supplier} value={supplier}>{supplier}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Min Price</label>
              <input
                type="number"
                value={filters.min_price}
                onChange={(e) => handleFilterChange('min_price', e.target.value)}
                placeholder="£0"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Price</label>
              <input
                type="number"
                value={filters.max_price}
                onChange={(e) => handleFilterChange('max_price', e.target.value)}
                placeholder="£1000"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
          <div className="mt-4">
            <button
              onClick={clearFilters}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition duration-200"
            >
              Clear Filters
            </button>
          </div>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>

        {products.length === 0 && (
          <div className="text-center py-16">
            <div className="text-gray-400 text-6xl mb-4">📦</div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No products found</h3>
            <p className="text-gray-500">Try adjusting your filters or search terms</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Product Card Component matching the reference design
const ProductCard = ({ product }) => {
  const [calculatorArea, setCalculatorArea] = useState('');
  const [calculatedPrice, setCalculatedPrice] = useState(null);

  const calculatePrice = () => {
    if (calculatorArea && product.box_size) {
      const area = parseFloat(calculatorArea);
      const boxesNeeded = Math.ceil(area / product.box_size);
      const totalPrice = boxesNeeded * product.price;
      setCalculatedPrice(totalPrice.toFixed(2));
    } else {
      alert('Please enter a valid area');
    }
  };

  // Generate placeholder images based on category
  const getPlaceholderImage = (category) => {
    const images = {
      'Laminate': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop',
      'LVT': 'https://images.unsplash.com/photo-1581618047521-b0dbaef3e272?w=400&h=300&fit=crop',
      'Tiles': 'https://images.unsplash.com/photo-1615971677499-5467cbab01c2?w=400&h=300&fit=crop',
      'Various': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop'
    };
    return images[category] || images['Various'];
  };

  return (
    <div className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-lg transition duration-200">
      <div className="h-48 bg-gray-200 overflow-hidden">
        {product.image_base64 ? (
          <img 
            src={`data:image/jpeg;base64,${product.image_base64}`} 
            alt={product.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <img 
            src={getPlaceholderImage(product.category)} 
            alt={product.name}
            className="w-full h-full object-cover"
          />
        )}
      </div>
      
      <div className="p-4">
        {/* Product Title */}
        <h3 className="font-semibold text-lg mb-2 line-clamp-2 text-gray-900">{product.name}</h3>
        
        {/* Product Details */}
        <div className="text-sm text-gray-600 mb-3 space-y-1">
          <div className="flex justify-between">
            <span>{product.category}</span>
            <span className={`px-2 py-1 rounded-full text-xs ${product.in_stock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {product.in_stock ? 'In Stock' : 'Out of Stock'}
            </span>
          </div>
          {product.tile_size && (
            <div>Size: {product.tile_size}</div>
          )}
          {product.box_size && (
            <div>Box Size: {product.box_size}m²</div>
          )}
          <div>Thickness: 8mm</div>
          <div>Finish: Matt</div>
        </div>
        
        {/* Price */}
        <div className="text-2xl font-bold text-green-600 mb-4">
          £{product.price.toFixed(2)}/m²
        </div>
        
        {/* Price Calculator */}
        <div className="border-t pt-4">
          <div className="mb-3">
            <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <span className="text-sm font-medium">Calculate Price</span>
          </div>
          
          <div className="flex gap-2">
            <input
              type="number"
              value={calculatorArea}
              onChange={(e) => setCalculatorArea(e.target.value)}
              placeholder="Area (m²)"
              className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            />
            <button
              onClick={calculatePrice}
              className="px-4 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 transition duration-200"
            >
              Calculate
            </button>
          </div>
          
          {calculatedPrice && (
            <div className="mt-2 text-center">
              <div className="text-lg font-bold text-green-600">
                Total: £{calculatedPrice}
              </div>
              <div className="text-xs text-gray-500">
                For {calculatorArea}m² area
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCatalog;
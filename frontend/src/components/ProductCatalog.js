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
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
        <div className="relative">
          <div className="animate-spin rounded-full h-32 w-32 border-4 border-gradient-to-r from-amber-500 to-orange-600 border-t-transparent"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="animate-pulse text-slate-600">Loading...</div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
        <div className="text-red-600 text-xl bg-white p-8 rounded-2xl shadow-xl">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
      {/* Hero Header */}
      <div className="relative bg-gradient-to-r from-slate-900 via-gray-900 to-zinc-900 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-amber-500/10 to-orange-600/10"></div>
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-full h-full bg-gradient-to-br from-white/5 to-transparent"></div>
        </div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 tracking-tight">
              Premium Collection
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Discover exquisite tiles and flooring solutions crafted for modern living
            </p>
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 text-white">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              <span className="text-sm font-medium">{products.length} Premium Products Available</span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Modern Filter Panel */}
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 p-8 mb-12">
          <div className="flex items-center mb-6">
            <div className="w-1 h-8 bg-gradient-to-b from-amber-500 to-orange-600 rounded-full mr-4"></div>
            <h2 className="text-2xl font-bold text-gray-900">Filter & Discover</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Search Products</label>
              <div className="relative">
                <input
                  type="text"
                  value={filters.search}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                  placeholder="Find your perfect tile..."
                  className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 group-hover:border-gray-300"
                />
                <svg className="absolute right-3 top-3 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Supplier</label>
              <select
                value={filters.supplier}
                onChange={(e) => handleFilterChange('supplier', e.target.value)}
                className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 group-hover:border-gray-300 appearance-none"
              >
                <option value="">All Suppliers</option>
                {suppliers.map(supplier => (
                  <option key={supplier} value={supplier}>{supplier}</option>
                ))}
              </select>
            </div>

            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Category</label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 group-hover:border-gray-300 appearance-none"
              >
                <option value="">All Categories</option>
                {categories.map(category => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </div>

            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Min Price</label>
              <input
                type="number"
                value={filters.min_price}
                onChange={(e) => handleFilterChange('min_price', e.target.value)}
                placeholder="£0"
                className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 group-hover:border-gray-300"
              />
            </div>

            <div className="group">
              <label className="block text-sm font-semibold text-gray-700 mb-3">Max Price</label>
              <input
                type="number"
                value={filters.max_price}
                onChange={(e) => handleFilterChange('max_price', e.target.value)}
                placeholder="£1000"
                className="w-full px-4 py-3 bg-white border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 group-hover:border-gray-300"
              />
            </div>
          </div>
          
          <div className="mt-8 flex justify-between items-center">
            <button
              onClick={clearFilters}
              className="px-6 py-3 bg-gray-100 text-gray-700 rounded-2xl hover:bg-gray-200 transition-all duration-300 font-medium"
            >
              Clear All Filters
            </button>
            <div className="text-sm text-gray-600">
              Showing <span className="font-bold text-gray-900">{products.length}</span> products
            </div>
          </div>
        </div>

        {/* Premium Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>

        {products.length === 0 && (
          <div className="text-center py-24">
            <div className="w-32 h-32 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-8">
              <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-700 mb-4">No products found</h3>
            <p className="text-gray-500 max-w-md mx-auto">Try adjusting your search criteria or explore different categories to find what you're looking for.</p>
          </div>
        )}
      </div>
    </div>
  );
};

// Premium Product Card Component
const ProductCard = ({ product }) => {
  const [calculatorArea, setCalculatorArea] = useState('');
  const [calculatedPrice, setCalculatedPrice] = useState(null);
  const [isHovered, setIsHovered] = useState(false);

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

  // Generate luxury placeholder images based on category
  const getPlaceholderImage = (category) => {
    const images = {
      'Laminate': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&auto=format&q=80',
      'LVT': 'https://images.unsplash.com/photo-1581618047521-b0dbaef3e272?w=400&h=300&fit=crop&auto=format&q=80',
      'Tiles': 'https://images.unsplash.com/photo-1615971677499-5467cbab01c2?w=400&h=300&fit=crop&auto=format&q=80',
      'Various': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop&auto=format&q=80'
    };
    return images[category] || images['Various'];
  };

  const getCategoryColor = (category) => {
    const colors = {
      'Laminate': 'from-amber-500 to-orange-600',
      'LVT': 'from-emerald-500 to-teal-600',
      'Tiles': 'from-blue-500 to-indigo-600',
      'Various': 'from-purple-500 to-pink-600'
    };
    return colors[category] || colors['Various'];
  };

  return (
    <div 
      className={`group bg-white rounded-3xl shadow-xl overflow-hidden transition-all duration-500 transform ${isHovered ? 'scale-105 shadow-2xl' : 'hover:scale-102'} border border-gray-100`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Product Image */}
      <div className="relative h-64 overflow-hidden">
        <img 
          src={product.image_base64 ? `data:image/jpeg;base64,${product.image_base64}` : getPlaceholderImage(product.category)}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        <div className={`absolute top-4 left-4 px-3 py-1 rounded-full bg-gradient-to-r ${getCategoryColor(product.category)} text-white text-xs font-semibold tracking-wide`}>
          {product.category}
        </div>
        <div className={`absolute top-4 right-4 px-3 py-1 rounded-full text-xs font-semibold ${product.in_stock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {product.in_stock ? '✓ In Stock' : '✗ Out of Stock'}
        </div>
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      
      <div className="p-6">
        {/* Product Title */}
        <h3 className="font-bold text-lg mb-3 text-gray-900 line-clamp-2 group-hover:text-amber-600 transition-colors duration-300">
          {product.name}
        </h3>
        
        {/* Product Details */}
        <div className="space-y-2 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Supplier</span>
            <span className="font-medium text-gray-900">{product.supplier}</span>
          </div>
          {product.tile_size && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Size</span>
              <span className="font-medium text-gray-900">{product.tile_size}</span>
            </div>
          )}
          {product.box_size && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Coverage</span>
              <span className="font-medium text-gray-900">{product.box_size}m²/box</span>
            </div>
          )}
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Thickness</span>
            <span className="font-medium text-gray-900">8mm</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Finish</span>
            <span className="font-medium text-gray-900">Matt</span>
          </div>
        </div>
        
        {/* Price */}
        <div className="text-3xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent mb-6">
          £{product.price.toFixed(2)}<span className="text-lg text-gray-500 font-normal">/m²</span>
        </div>
        
        {/* Premium Calculator */}
        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-5 border border-gray-200">
          <div className="flex items-center mb-4">
            <div className="w-8 h-8 bg-gradient-to-r from-amber-500 to-orange-600 rounded-lg flex items-center justify-center mr-3">
              <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
            </div>
            <span className="font-semibold text-gray-900">Price Calculator</span>
          </div>
          
          <div className="flex gap-3 mb-4">
            <input
              type="number"
              value={calculatorArea}
              onChange={(e) => setCalculatorArea(e.target.value)}
              placeholder="Enter area (m²)"
              className="flex-1 px-4 py-3 bg-white border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 text-sm"
            />
            <button
              onClick={calculatePrice}
              className="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 font-semibold text-sm shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              Calculate
            </button>
          </div>
          
          {calculatedPrice && (
            <div className="bg-white rounded-xl p-4 border-2 border-amber-200 animate-fade-in">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900 mb-1">
                  £{calculatedPrice}
                </div>
                <div className="text-sm text-gray-600">
                  Total cost for {calculatorArea}m²
                </div>
                <div className="text-xs text-amber-600 mt-2">
                  {Math.ceil(calculatorArea / (product.box_size || 1))} boxes needed
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Action Button */}
        <button className="w-full mt-6 bg-gradient-to-r from-gray-900 to-black text-white py-4 rounded-2xl font-semibold hover:from-gray-800 hover:to-gray-900 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl">
          View Details & Order
        </button>
      </div>
    </div>
  );
};

export default ProductCatalog;
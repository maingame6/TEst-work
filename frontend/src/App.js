import React, { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Hero Section Component
const Hero = ({ totalProducts, onExploreClick }) => {
  return (
    <div className="relative bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 text-white">
      <div className="absolute inset-0 bg-black opacity-50"></div>
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Bearfoot Flooring
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-300 max-w-3xl mx-auto">
            Discover our premium collection of {totalProducts} exquisite flooring solutions. 
            From elegant laminates to luxury hardwoods, find the perfect floor for your space.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={onExploreClick}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-4 rounded-lg text-lg font-medium transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              Explore Collection
            </button>
            <button className="border-2 border-white text-white hover:bg-white hover:text-gray-900 px-8 py-4 rounded-lg text-lg font-medium transition-all duration-200">
              View Catalog
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

// Stats Section
const StatsSection = ({ sections, brands, totalProducts }) => {
  const stats = [
    { label: "Total Products", value: totalProducts, icon: "📦" },
    { label: "Product Categories", value: sections.length, icon: "🏗️" },
    { label: "Premium Brands", value: brands.length, icon: "⭐" },
    { label: "Customer Satisfaction", value: "99%", icon: "😊" }
  ];

  return (
    <div className="bg-gray-50 py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-4xl mb-2">{stat.icon}</div>
              <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Product Card Component
const ProductCard = ({ product }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 group">
      <div className="relative overflow-hidden">
        <div className={`w-full h-64 bg-gray-200 flex items-center justify-center ${!imageLoaded ? 'animate-pulse' : ''}`}>
          {!imageLoaded && (
            <div className="text-gray-400">Loading...</div>
          )}
          <img
            src={product.image_base64}
            alt={product.display_name}
            className={`w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500 ${imageLoaded ? 'block' : 'hidden'}`}
            onLoad={() => setImageLoaded(true)}
            onError={(e) => {
              e.target.style.display = 'none';
              setImageLoaded(true);
            }}
          />
        </div>
        
        {/* Badges */}
        <div className="absolute top-4 left-4 flex flex-col gap-2">
          {product.section && (
            <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-medium">
              {product.section}
            </span>
          )}
          {product.thickness && (
            <span className="bg-green-600 text-white px-3 py-1 rounded-full text-xs font-medium">
              {product.thickness}
            </span>
          )}
        </div>
        
        {!product.in_stock && (
          <div className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-medium">
            Out of Stock
          </div>
        )}
      </div>
      
      <div className="p-6">
        <div className="flex justify-between items-start mb-3">
          <h3 className="font-bold text-lg text-gray-900 line-clamp-2 flex-1">
            {product.display_name}
          </h3>
          <span className="text-2xl font-bold text-blue-600 ml-4">
            €{product.price.toFixed(2)}
          </span>
        </div>
        
        <div className="flex items-center gap-2 mb-3 text-sm text-gray-600">
          <span className="font-medium">{product.brand}</span>
          {product.series && (
            <>
              <span>•</span>
              <span>{product.series}</span>
            </>
          )}
        </div>
        
        <div className="flex gap-2 mb-4 flex-wrap">
          <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs">
            {product.product_type}
          </span>
          {product.area_m2 && (
            <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs">
              {product.area_m2}m²
            </span>
          )}
        </div>
        
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {product.description}
        </p>
        
        <div className="flex flex-wrap gap-1 mb-4">
          {product.features.slice(0, 3).map((feature, index) => (
            <span key={index} className="bg-green-50 text-green-700 px-2 py-1 rounded text-xs">
              {feature}
            </span>
          ))}
          {product.features.length > 3 && (
            <span className="text-xs text-gray-500">
              +{product.features.length - 3} more
            </span>
          )}
        </div>
        
        <button 
          className={`w-full py-3 px-4 rounded-lg font-medium transition-all duration-200 ${
            product.in_stock
              ? 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          disabled={!product.in_stock}
        >
          {product.in_stock ? 'View Details' : 'Out of Stock'}
        </button>
      </div>
    </div>
  );
};

// Advanced Filter Component
const ProductFilters = ({ filters, onFilterChange, productTypes, sections, brands, thicknesses, isVisible }) => {
  return (
    <div className={`bg-white rounded-xl shadow-lg p-6 mb-8 transition-all duration-300 ${isVisible ? 'block' : 'hidden'}`}>
      <div className="flex justify-between items-center mb-6">
        <h3 className="font-bold text-xl text-gray-900">Filter Products</h3>
        <button
          onClick={() => onFilterChange('reset')}
          className="text-blue-600 hover:text-blue-800 font-medium"
        >
          Reset All
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Section
          </label>
          <select
            value={filters.section || ''}
            onChange={(e) => onFilterChange('section', e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Sections</option>
            {sections.map(section => (
              <option key={section} value={section}>{section}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Product Type
          </label>
          <select
            value={filters.product_type || ''}
            onChange={(e) => onFilterChange('product_type', e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Types</option>
            {productTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Brand
          </label>
          <select
            value={filters.brand || ''}
            onChange={(e) => onFilterChange('brand', e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Brands</option>
            {brands.map(brand => (
              <option key={brand} value={brand}>{brand}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Thickness
          </label>
          <select
            value={filters.thickness || ''}
            onChange={(e) => onFilterChange('thickness', e.target.value)}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Thicknesses</option>
            {thicknesses.map(thickness => (
              <option key={thickness} value={thickness}>{thickness}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Search
          </label>
          <input
            type="text"
            value={filters.search || ''}
            onChange={(e) => onFilterChange('search', e.target.value)}
            placeholder="Search products..."
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Price Range
          </label>
          <div className="flex gap-2">
            <input
              type="number"
              value={filters.min_price || ''}
              onChange={(e) => onFilterChange('min_price', e.target.value)}
              placeholder="Min €"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="number"
              value={filters.max_price || ''}
              onChange={(e) => onFilterChange('max_price', e.target.value)}
              placeholder="Max €"
              className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

// Home Page Component
const Home = () => {
  const [products, setProducts] = useState([]);
  const [productTypes, setProductTypes] = useState([]);
  const [sections, setSections] = useState([]);
  const [brands, setBrands] = useState([]);
  const [thicknesses, setThicknesses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});
  const [showFilters, setShowFilters] = useState(false);
  const [totalProducts, setTotalProducts] = useState(0);

  const fetchProducts = async (filterParams = {}) => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      Object.entries(filterParams).forEach(([key, value]) => {
        if (value && value !== '') {
          params.append(key, value);
        }
      });
      
      const response = await axios.get(`${API}/products?${params.toString()}`);
      setProducts(response.data);
    } catch (err) {
      console.error('Error fetching products:', err);
      setError('Failed to load products. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const fetchFilterOptions = async () => {
    try {
      const [typesRes, sectionsRes, brandsRes, thicknessesRes, apiRes] = await Promise.all([
        axios.get(`${API}/products/types`),
        axios.get(`${API}/products/sections`),
        axios.get(`${API}/products/brands`),
        axios.get(`${API}/products/thicknesses`),
        axios.get(`${API}/`)
      ]);
      
      setProductTypes(typesRes.data.product_types || []);
      setSections(sectionsRes.data.sections || []);
      setBrands(brandsRes.data.brands || []);
      setThicknesses(thicknessesRes.data.thicknesses || []);
      setTotalProducts(apiRes.data.total_products || 0);
    } catch (err) {
      console.error('Error fetching filter options:', err);
    }
  };

  const handleFilterChange = (key, value) => {
    if (key === 'reset') {
      setFilters({});
      fetchProducts({});
      return;
    }
    
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    
    // Debounce the API call
    clearTimeout(window.filterTimeout);
    window.filterTimeout = setTimeout(() => {
      fetchProducts(newFilters);
    }, 500);
  };

  const scrollToProducts = () => {
    document.getElementById('products-section').scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    fetchProducts();
    fetchFilterOptions();
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-xl shadow-lg">
          <div className="text-6xl mb-4">😞</div>
          <h2 className="text-2xl font-bold text-red-600 mb-4">Oops! Something went wrong</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <Hero totalProducts={totalProducts} onExploreClick={scrollToProducts} />
      
      {/* Stats Section */}
      <StatsSection sections={sections} brands={brands} totalProducts={totalProducts} />
      
      {/* Main Products Section */}
      <div id="products-section" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Our Product Collection
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Browse through our extensive catalog of premium flooring solutions. 
            Use the filters below to find exactly what you're looking for.
          </p>
          
          <button
            onClick={() => setShowFilters(!showFilters)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium inline-flex items-center gap-2"
          >
            <span>🔍</span>
            {showFilters ? 'Hide Filters' : 'Show Filters'}
          </button>
        </div>

        {/* Filters */}
        <ProductFilters
          filters={filters}
          onFilterChange={handleFilterChange}
          productTypes={productTypes}
          sections={sections}
          brands={brands}
          thicknesses={thicknesses}
          isVisible={showFilters}
        />

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
              <p className="text-gray-600 text-lg">Loading amazing products...</p>
            </div>
          </div>
        ) : (
          <>
            {/* Product Count */}
            <div className="mb-8 text-center">
              <p className="text-gray-600 text-lg">
                Showing <span className="font-bold text-blue-600">{products.length}</span> product{products.length !== 1 ? 's' : ''}
                {Object.keys(filters).length > 0 && (
                  <span className="ml-2 text-sm bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                    Filtered
                  </span>
                )}
              </p>
            </div>

            {/* Products Grid */}
            {products.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <div className="text-center py-20 bg-white rounded-xl shadow-lg">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">No products found</h3>
                <p className="text-gray-500 text-lg mb-6">
                  Try adjusting your filters or search terms
                </p>
                <button
                  onClick={() => handleFilterChange('reset')}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium"
                >
                  Clear All Filters
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
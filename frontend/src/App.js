import React, { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Product Card Component
const ProductCard = ({ product }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <div className="relative">
        <img
          src={product.image_base64}
          alt={product.display_name}
          className="w-full h-48 object-cover"
          onError={(e) => {
            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjNmNGY2Ii8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5YTNhZiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPk5vIEltYWdlPC90ZXh0Pjwvc3ZnPg==';
          }}
        />
        {!product.in_stock && (
          <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-xs">
            Out of Stock
          </div>
        )}
        <div className="absolute bottom-2 left-2 bg-blue-500 text-white px-2 py-1 rounded text-xs">
          {product.product_type}
        </div>
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-lg text-gray-800 mb-2 line-clamp-2">
          {product.display_name}
        </h3>
        
        <div className="flex justify-between items-center mb-2">
          <span className="text-2xl font-bold text-blue-600">
            €{product.price.toFixed(2)}
          </span>
          {product.area_m2 && (
            <span className="text-sm text-gray-500">
              {product.area_m2}m²
            </span>
          )}
        </div>
        
        <div className="flex gap-2 mb-3">
          {product.product_code && (
            <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
              {product.product_code}
            </span>
          )}
          {product.dimensions && (
            <span className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
              {product.dimensions}
            </span>
          )}
        </div>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-3">
          {product.description}
        </p>
        
        <div className="flex flex-wrap gap-1 mb-3">
          {product.features.slice(0, 2).map((feature, index) => (
            <span key={index} className="bg-green-100 text-green-600 px-2 py-1 rounded text-xs">
              {feature}
            </span>
          ))}
          {product.features.length > 2 && (
            <span className="text-xs text-gray-500">
              +{product.features.length - 2} more
            </span>
          )}
        </div>
        
        <button 
          className={`w-full py-2 px-4 rounded font-medium transition-colors ${
            product.in_stock
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
          }`}
          disabled={!product.in_stock}
        >
          {product.in_stock ? 'Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </div>
  );
};

// Filter Component
const ProductFilters = ({ filters, onFilterChange, productTypes, sections, brands, thicknesses }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md mb-6">
      <h3 className="font-semibold text-lg mb-4">Filters</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Section
          </label>
          <select
            value={filters.section || ''}
            onChange={(e) => onFilterChange('section', e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="">All Sections</option>
            {sections.map(section => (
              <option key={section} value={section}>{section}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Product Type
          </label>
          <select
            value={filters.product_type || ''}
            onChange={(e) => onFilterChange('product_type', e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="">All Types</option>
            {productTypes.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Brand
          </label>
          <select
            value={filters.brand || ''}
            onChange={(e) => onFilterChange('brand', e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="">All Brands</option>
            {brands.map(brand => (
              <option key={brand} value={brand}>{brand}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Thickness
          </label>
          <select
            value={filters.thickness || ''}
            onChange={(e) => onFilterChange('thickness', e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2"
          >
            <option value="">All Thicknesses</option>
            {thicknesses.map(thickness => (
              <option key={thickness} value={thickness}>{thickness}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <input
            type="text"
            value={filters.search || ''}
            onChange={(e) => onFilterChange('search', e.target.value)}
            placeholder="Search products..."
            className="w-full border border-gray-300 rounded px-3 py-2"
          />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Min Price (€)
          </label>
          <input
            type="number"
            value={filters.min_price || ''}
            onChange={(e) => onFilterChange('min_price', e.target.value)}
            placeholder="0"
            className="w-full border border-gray-300 rounded px-3 py-2"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Max Price (€)
          </label>
          <input
            type="number"
            value={filters.max_price || ''}
            onChange={(e) => onFilterChange('max_price', e.target.value)}
            placeholder="1000"
            className="w-full border border-gray-300 rounded px-3 py-2"
          />
        </div>
      </div>
      
      <button
        onClick={() => onFilterChange('reset')}
        className="mt-4 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
      >
        Reset Filters
      </button>
    </div>
  );
};

// Home Page Component
const Home = () => {
  const [products, setProducts] = useState([]);
  const [productTypes, setProductTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({});

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

  const fetchProductTypes = async () => {
    try {
      const response = await axios.get(`${API}/products/types`);
      setProductTypes(response.data.product_types || []);
    } catch (err) {
      console.error('Error fetching product types:', err);
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

  useEffect(() => {
    fetchProducts();
    fetchProductTypes();
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">Bearfoot Flooring</h1>
            </div>
            <nav className="flex space-x-8">
              <Link to="/" className="text-blue-600 hover:text-blue-700 font-medium">
                Products
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Premium Laminate Flooring Collection
          </h2>
          <p className="text-gray-600">
            Discover our extensive range of high-quality laminate flooring solutions
          </p>
        </div>

        {/* Filters */}
        <ProductFilters
          filters={filters}
          onFilterChange={handleFilterChange}
          productTypes={productTypes}
        />

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            {/* Product Count */}
            <div className="mb-6">
              <p className="text-gray-600">
                Showing {products.length} product{products.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Products Grid */}
            {products.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No products found matching your criteria.</p>
                <button
                  onClick={() => handleFilterChange('reset')}
                  className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                >
                  Clear Filters
                </button>
              </div>
            )}
          </>
        )}
      </main>
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

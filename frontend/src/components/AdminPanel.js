import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminPanel = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loginData, setLoginData] = useState({ username: '', password: '' });
  const [activeTab, setActiveTab] = useState('overview');
  const [products, setProducts] = useState([]);
  const [stats, setStats] = useState({});
  const [editingProduct, setEditingProduct] = useState(null);
  const [isAddingProduct, setIsAddingProduct] = useState(false);

  // Check if user is logged in
  useEffect(() => {
    const token = localStorage.getItem('admin_token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      verifyToken();
    } else {
      setLoading(false);
    }
  }, []);

  const verifyToken = async () => {
    try {
      await axios.get(`${API}/auth/me`);
      setIsLoggedIn(true);
      fetchData();
    } catch (err) {
      localStorage.removeItem('admin_token');
      delete axios.defaults.headers.common['Authorization'];
      setIsLoggedIn(false);
    }
    setLoading(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/auth/login`, loginData);
      const { access_token } = response.data;
      
      localStorage.setItem('admin_token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setIsLoggedIn(true);
      fetchData();
    } catch (err) {
      alert('Login failed. Please check your credentials.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    delete axios.defaults.headers.common['Authorization'];
    setIsLoggedIn(false);
    setProducts([]);
    setStats({});
  };

  const fetchData = async () => {
    try {
      const [productsRes, statsRes] = await Promise.all([
        axios.get(`${API}/products?limit=1000`),
        axios.get(`${API}/admin/stats`)
      ]);
      setProducts(productsRes.data);
      setStats(statsRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
    }
  };

  const handleSaveProduct = async (productData) => {
    try {
      if (editingProduct) {
        await axios.put(`${API}/products/${editingProduct.id}`, productData);
        setEditingProduct(null);
      } else {
        await axios.post(`${API}/products`, productData);
        setIsAddingProduct(false);
      }
      fetchData();
    } catch (err) {
      alert('Error saving product');
    }
  };

  const handleDeleteProduct = async (productId) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await axios.delete(`${API}/products/${productId}`);
        fetchData();
      } catch (err) {
        alert('Error deleting product');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
        <div className="relative">
          <div className="animate-spin rounded-full h-32 w-32 border-4 border-gradient-to-r from-amber-500 to-orange-600 border-t-transparent"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="animate-pulse text-slate-600 font-semibold">Loading...</div>
          </div>
        </div>
      </div>
    );
  }

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        {/* Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gradient-to-br from-amber-500/10 to-orange-600/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-br from-emerald-500/10 to-teal-600/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="relative sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-amber-500 to-orange-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h2 className="text-3xl font-bold text-white mb-2">
              Admin Access
            </h2>
            <p className="text-gray-300">
              Enter your credentials to access the admin panel
            </p>
          </div>
        </div>
        
        <div className="relative mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white/10 backdrop-blur-xl py-8 px-4 shadow-2xl sm:rounded-3xl sm:px-10 border border-white/20">
            <form onSubmit={handleLogin} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-white mb-3">Username</label>
                <input
                  type="text"
                  required
                  value={loginData.username}
                  onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                  className="w-full px-4 py-3 bg-white/20 border-2 border-white/30 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 text-white placeholder-gray-300"
                  placeholder="Enter username"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-white mb-3">Password</label>
                <input
                  type="password"
                  required
                  value={loginData.password}
                  onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                  className="w-full px-4 py-3 bg-white/20 border-2 border-white/30 rounded-2xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300 text-white placeholder-gray-300"
                  placeholder="Enter password"
                />
              </div>
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-amber-500 to-orange-600 text-white py-4 rounded-2xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105"
              >
                Sign In to Admin Panel
              </button>
            </form>
            <div className="mt-6 text-center">
              <div className="inline-flex items-center space-x-2 bg-amber-100/20 rounded-full px-4 py-2">
                <svg className="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-sm text-amber-200">Default: admin / admin123</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-gray-900 to-zinc-900 shadow-2xl">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-8">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-gradient-to-r from-amber-500 to-orange-600 rounded-xl flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Admin Dashboard</h1>
                <p className="text-gray-300">Manage your products and inventory</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-500/80 hover:bg-red-600 text-white px-6 py-3 rounded-2xl transition-all duration-300 font-semibold backdrop-blur-sm border border-red-400/30"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Modern Tabs */}
        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/50 mb-12">
          <div className="border-b border-gray-200/50">
            <nav className="flex">
              {['overview', 'products'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`py-6 px-8 border-b-4 font-semibold text-sm transition-all duration-300 ${
                    activeTab === tab
                      ? 'border-amber-500 text-amber-600 bg-amber-50/50'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50/50'
                  }`}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-8">
            {activeTab === 'overview' && (
              <div>
                <div className="flex items-center mb-8">
                  <div className="w-1 h-10 bg-gradient-to-b from-amber-500 to-orange-600 rounded-full mr-4"></div>
                  <h2 className="text-3xl font-bold text-gray-900">Dashboard Overview</h2>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                  <StatCard
                    title="Total Products"
                    value={stats.total_products || 0}
                    gradient="from-blue-500 to-blue-600"
                    icon="📦"
                  />
                  <StatCard
                    title="In Stock"
                    value={stats.in_stock_products || 0}
                    gradient="from-green-500 to-green-600"
                    icon="✅"
                  />
                  <StatCard
                    title="Out of Stock"
                    value={stats.out_of_stock_products || 0}
                    gradient="from-red-500 to-red-600"
                    icon="❌"
                  />
                  <StatCard
                    title="Suppliers"
                    value={stats.total_suppliers || 0}
                    gradient="from-purple-500 to-purple-600"
                    icon="🏢"
                  />
                </div>
              </div>
            )}

            {activeTab === 'products' && (
              <div>
                <div className="flex justify-between items-center mb-8">
                  <div className="flex items-center">
                    <div className="w-1 h-10 bg-gradient-to-b from-amber-500 to-orange-600 rounded-full mr-4"></div>
                    <h2 className="text-3xl font-bold text-gray-900">Product Management</h2>
                  </div>
                  <button
                    onClick={() => setIsAddingProduct(true)}
                    className="bg-gradient-to-r from-amber-500 to-orange-600 text-white px-6 py-3 rounded-2xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                  >
                    Add New Product
                  </button>
                </div>
                
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gradient-to-r from-gray-50 to-gray-100">
                        <tr>
                          <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Product</th>
                          <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Supplier</th>
                          <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Price</th>
                          <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Stock</th>
                          <th className="px-6 py-4 text-left text-xs font-bold text-gray-700 uppercase tracking-wider">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {products.map((product, index) => (
                          <tr key={product.id} className={`hover:bg-gray-50 transition-colors duration-200 ${index % 2 === 0 ? 'bg-white' : 'bg-gray-50/30'}`}>
                            <td className="px-6 py-4">
                              <div className="flex items-center">
                                <div className="w-12 h-12 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl flex items-center justify-center mr-4">
                                  <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                                  </svg>
                                </div>
                                <div>
                                  <div className="text-sm font-semibold text-gray-900 line-clamp-2">{product.name}</div>
                                  <div className="text-sm text-gray-500">{product.sku}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-900 font-medium">{product.supplier}</td>
                            <td className="px-6 py-4 text-sm font-bold text-gray-900">£{product.price}</td>
                            <td className="px-6 py-4">
                              <span className={`px-3 py-1 rounded-full text-xs font-semibold ${product.in_stock ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                {product.in_stock ? '✓ In Stock' : '✗ Out of Stock'}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm font-medium space-x-3">
                              <button
                                onClick={() => setEditingProduct(product)}
                                className="text-amber-600 hover:text-amber-900 font-semibold"
                              >
                                Edit
                              </button>
                              <button
                                onClick={() => handleDeleteProduct(product.id)}
                                className="text-red-600 hover:text-red-900 font-semibold"
                              >
                                Delete
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Product Form Modal */}
      {(editingProduct || isAddingProduct) && (
        <ProductForm
          product={editingProduct}
          onSave={handleSaveProduct}
          onCancel={() => {
            setEditingProduct(null);
            setIsAddingProduct(false);
          }}
        />
      )}
    </div>
  );
};

// Stat Card Component
const StatCard = ({ title, value, gradient, icon }) => (
  <div className="group bg-white/80 backdrop-blur-xl rounded-2xl p-6 shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 border border-white/50">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-semibold text-gray-600 mb-2">{title}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
      <div className={`w-12 h-12 bg-gradient-to-r ${gradient} rounded-xl flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300`}>
        {icon}
      </div>
    </div>
  </div>
);

// Product Form Component (simplified for space - keeping the same structure)
const ProductForm = ({ product, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    supplier: product?.supplier || '',
    name: product?.name || '',
    sku: product?.sku || '',
    tile_size: product?.tile_size || '',
    box_size: product?.box_size || '',
    price: product?.price || '',
    category: product?.category || '',
    description: product?.description || '',
    in_stock: product?.in_stock !== undefined ? product.in_stock : true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-3xl p-8 w-full max-w-md shadow-2xl border border-gray-200">
        <h3 className="text-2xl font-bold mb-6 text-gray-900">
          {product ? 'Edit Product' : 'Add Product'}
        </h3>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Supplier</label>
            <input
              type="text"
              required
              value={formData.supplier}
              onChange={(e) => setFormData({...formData, supplier: e.target.value})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">SKU</label>
            <input
              type="text"
              required
              value={formData.sku}
              onChange={(e) => setFormData({...formData, sku: e.target.value})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Price</label>
            <input
              type="number"
              step="0.01"
              required
              value={formData.price}
              onChange={(e) => setFormData({...formData, price: parseFloat(e.target.value)})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300"
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Category</label>
            <input
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({...formData, category: e.target.value})}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-amber-500 focus:ring-4 focus:ring-amber-500/20 transition-all duration-300"
            />
          </div>
          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.in_stock}
                onChange={(e) => setFormData({...formData, in_stock: e.target.checked})}
                className="mr-3 w-4 h-4 text-amber-600 bg-gray-100 border-gray-300 rounded focus:ring-amber-500 focus:ring-2"
              />
              <span className="text-sm font-semibold text-gray-700">In Stock</span>
            </label>
          </div>
          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="px-6 py-3 border-2 border-gray-300 rounded-xl text-gray-700 hover:bg-gray-50 transition-all duration-300 font-semibold"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-xl hover:from-amber-600 hover:to-orange-700 transition-all duration-300 font-semibold shadow-lg hover:shadow-xl"
            >
              Save Product
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminPanel;
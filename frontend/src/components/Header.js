import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="text-2xl font-bold text-blue-600">
              Tiles & Wood Floor Store
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link
              to="/"
              className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                isActive('/') ? 'text-blue-600 font-semibold' : ''
              }`}
            >
              Home
            </Link>
            <Link
              to="/products"
              className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                isActive('/products') ? 'text-blue-600 font-semibold' : ''
              }`}
            >
              Products
            </Link>
            <Link
              to="/admin"
              className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                isActive('/admin') ? 'text-blue-600 font-semibold' : ''
              }`}
            >
              Admin
            </Link>
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-gray-700 hover:text-blue-600 focus:outline-none focus:text-blue-600"
            >
              <svg className="h-6 w-6" fill="none" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" viewBox="0 0 24 24" stroke="currentColor">
                {isMenuOpen ? (
                  <path d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4">
            <div className="flex flex-col space-y-4">
              <Link
                to="/"
                className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                  isActive('/') ? 'text-blue-600 font-semibold' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                Home
              </Link>
              <Link
                to="/products"
                className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                  isActive('/products') ? 'text-blue-600 font-semibold' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                Products
              </Link>
              <Link
                to="/admin"
                className={`text-gray-700 hover:text-blue-600 transition duration-200 ${
                  isActive('/admin') ? 'text-blue-600 font-semibold' : ''
                }`}
                onClick={() => setIsMenuOpen(false)}
              >
                Admin
              </Link>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
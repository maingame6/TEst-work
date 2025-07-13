import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="bg-white/95 backdrop-blur-xl shadow-xl border-b border-gray-200/50 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="group flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-amber-500 to-orange-600 rounded-xl flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <span className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                  Tiles & Wood Floor Store
                </span>
                <div className="text-xs text-gray-500 font-medium tracking-wide">Premium Quality Since 1995</div>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-2">
            <NavLink to="/" isActive={isActive('/')}>
              Home
            </NavLink>
            <NavLink to="/products" isActive={isActive('/products')}>
              Products
            </NavLink>
            <NavLink to="/admin" isActive={isActive('/admin')}>
              Admin
            </NavLink>
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 text-gray-700 hover:text-amber-600 focus:outline-none focus:text-amber-600 rounded-xl hover:bg-gray-100 transition-all duration-300"
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
          <div className="md:hidden py-4 border-t border-gray-200">
            <div className="flex flex-col space-y-2">
              <MobileNavLink to="/" isActive={isActive('/')} onClick={() => setIsMenuOpen(false)}>
                Home
              </MobileNavLink>
              <MobileNavLink to="/products" isActive={isActive('/products')} onClick={() => setIsMenuOpen(false)}>
                Products
              </MobileNavLink>
              <MobileNavLink to="/admin" isActive={isActive('/admin')} onClick={() => setIsMenuOpen(false)}>
                Admin
              </MobileNavLink>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

// Desktop Navigation Link Component
const NavLink = ({ to, isActive, children }) => (
  <Link
    to={to}
    className={`px-6 py-3 rounded-2xl font-semibold transition-all duration-300 transform hover:scale-105 ${
      isActive
        ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white shadow-lg'
        : 'text-gray-700 hover:text-amber-600 hover:bg-amber-50'
    }`}
  >
    {children}
  </Link>
);

// Mobile Navigation Link Component
const MobileNavLink = ({ to, isActive, onClick, children }) => (
  <Link
    to={to}
    onClick={onClick}
    className={`px-4 py-3 rounded-xl font-semibold transition-all duration-300 ${
      isActive
        ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white'
        : 'text-gray-700 hover:text-amber-600 hover:bg-amber-50'
    }`}
  >
    {children}
  </Link>
);

export default Header;
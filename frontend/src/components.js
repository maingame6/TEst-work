import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { flooringProducts, featuredProducts, productCategories, searchProducts } from './data/products';

// Header Component with 2025 Design Trends
export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearchResults, setShowSearchResults] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  // Modern scroll effect for 2025 design
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Search functionality
  useEffect(() => {
    if (searchQuery.length > 2) {
      const results = searchProducts(searchQuery);
      setSearchResults(results.slice(0, 5)); // Show top 5 results
      setShowSearchResults(true);
    } else {
      setShowSearchResults(false);
    }
  }, [searchQuery]);

  // Smooth scroll to sections
  const scrollToSection = (sectionId) => {
    if (location.pathname !== '/') {
      navigate('/');
      setTimeout(() => {
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } else {
      const element = document.getElementById(sectionId);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setIsMenuOpen(false);
  };

  const handleSearchSelect = (product) => {
    navigate(`/products?search=${product.name}`);
    setShowSearchResults(false);
    setSearchQuery('');
  };

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white/95 backdrop-blur-md shadow-lg' : 'bg-white'
    }`}>
      {/* Top green banner */}
      <div className="bg-green-600 text-white py-2 px-4 text-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-6 mb-2 md:mb-0">
            <a href="tel:02891225400" className="flex items-center hover:text-green-200 transition-colors">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              028 9122 5400
            </a>
            <a href="mailto:info@tileswoodfloorni.com" className="flex items-center hover:text-green-200 transition-colors">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
              info@tileswoodfloorni.com
            </a>
          </div>
          <div className="flex items-center space-x-4 text-xs md:text-sm">
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z"/>
              </svg>
              0% Finance Available
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Quote Match Guarantee
            </span>
          </div>
        </div>
      </div>

      {/* Main navigation with glassmorphism effect */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="flex items-center group">
            <div className="bg-gradient-to-r from-green-600 to-green-700 text-white px-3 py-2 rounded-lg font-bold text-xl mr-3 shadow-lg group-hover:shadow-xl transition-shadow duration-300">
              TWFS
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800 group-hover:text-green-600 transition-colors duration-300">Tiles & Wood Floor Store</h1>
              <p className="text-sm text-gray-600">Premium Flooring Solutions - Bangor</p>
            </div>
          </Link>

          {/* Desktop Navigation - 2025 Style */}
          <nav className="hidden lg:flex items-center space-x-1">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/products" className="nav-link">All Products</Link>
            <button onClick={() => scrollToSection('tiles')} className="nav-link">Tiles</button>
            <button onClick={() => scrollToSection('laminate')} className="nav-link">Laminate</button>
            <button onClick={() => scrollToSection('real-wood')} className="nav-link">Real Wood</button>
            <button onClick={() => scrollToSection('lvt')} className="nav-link">LVT</button>
            <button onClick={() => scrollToSection('carpets')} className="nav-link">Carpets</button>
            <button onClick={() => scrollToSection('gallery')} className="nav-link">Gallery</button>
            <button onClick={() => scrollToSection('services')} className="nav-link">Services</button>
            <Link to="/contact" className="nav-link">Contact</Link>
          </nav>

          {/* Search and CTA */}
          <div className="flex items-center space-x-4">
            <div className="relative hidden md:block">
              <input
                type="text"
                placeholder="Search flooring products..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-48 lg:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
              />
              <button className="absolute right-2 top-2 hover:text-green-600 transition-colors">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
              
              {/* Search Results Dropdown */}
              {showSearchResults && (
                <div className="absolute top-12 left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
                  {searchResults.map(product => (
                    <button
                      key={product.id}
                      onClick={() => handleSearchSelect(product)}
                      className="w-full p-3 text-left hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
                    >
                      <div className="flex items-center">
                        <img src={product.image} alt={product.name} className="w-10 h-10 object-cover rounded mr-3" />
                        <div>
                          <div className="font-medium text-gray-800">{product.name}</div>
                          <div className="text-sm text-gray-600">{product.priceDisplay} - {product.displayCategory}</div>
                        </div>
                      </div>
                    </button>
                  ))}
                  <div className="p-3 text-center">
                    <button 
                      onClick={() => navigate(`/products?search=${searchQuery}`)}
                      className="text-green-600 hover:text-green-700 font-medium"
                    >
                      View all results for "{searchQuery}"
                    </button>
                  </div>
                </div>
              )}
            </div>
            <button 
              onClick={() => scrollToSection('contact')}
              className="bg-gradient-to-r from-green-600 to-green-700 text-white px-4 lg:px-6 py-2 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-300 font-medium shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Get Quote
            </button>
            <button 
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors duration-300" 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle menu"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu with slide animation */}
        <div className={`lg:hidden overflow-hidden transition-all duration-300 ${
          isMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        }`}>
          <div className="mt-4 py-4 border-t border-gray-200 bg-white/95 backdrop-blur-md rounded-lg shadow-lg">
            <div className="px-4">
              <nav className="flex flex-col space-y-3">
                <Link to="/" className="mobile-nav-link" onClick={() => setIsMenuOpen(false)}>Home</Link>
                <Link to="/products" className="mobile-nav-link" onClick={() => setIsMenuOpen(false)}>All Products</Link>
                <button onClick={() => scrollToSection('tiles')} className="mobile-nav-link text-left">Tiles</button>
                <button onClick={() => scrollToSection('laminate')} className="mobile-nav-link text-left">Laminate</button>
                <button onClick={() => scrollToSection('real-wood')} className="mobile-nav-link text-left">Real Wood</button>
                <button onClick={() => scrollToSection('lvt')} className="mobile-nav-link text-left">LVT</button>
                <button onClick={() => scrollToSection('carpets')} className="mobile-nav-link text-left">Carpets</button>
                <button onClick={() => scrollToSection('gallery')} className="mobile-nav-link text-left">Gallery</button>
                <button onClick={() => scrollToSection('services')} className="mobile-nav-link text-left">Services</button>
                <Link to="/contact" className="mobile-nav-link" onClick={() => setIsMenuOpen(false)}>Contact</Link>
              </nav>
              <div className="mt-4">
                <input
                  type="text"
                  placeholder="Search products..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .nav-link {
          @apply px-3 py-2 rounded-lg text-gray-700 hover:text-green-600 hover:bg-green-50 font-medium transition-all duration-300 transform hover:-translate-y-0.5;
        }
        .mobile-nav-link {
          @apply text-gray-700 hover:text-green-600 font-medium py-2 transition-colors duration-300;
        }
      `}</style>
    </header>
  );
};

// Hero Section with 2025 Design Trends
export const Hero = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  
  const slides = [
    {
      image: "https://images.pexels.com/photos/8146313/pexels-photo-8146313.jpeg",
      title: "Premium Flooring Solutions for Northern Ireland",
      subtitle: "Transform your Bangor home with our extensive range"
    },
    {
      image: "https://images.unsplash.com/photo-1560185008-b033106af5c3",
      title: "Luxury Wood Flooring Specialists",
      subtitle: "Expert installation across North Down"
    },
    {
      image: "https://images.pexels.com/photos/4940756/pexels-photo-4940756.jpeg",
      title: "Visit Our Bangor Showroom",
      subtitle: "See our extensive collection in person"
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [slides.length]);

  const scrollToProducts = () => {
    const element = document.getElementById('products');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToContact = () => {
    const element = document.getElementById('contact');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden" style={{ marginTop: '80px' }}>
      {/* Background with parallax effect */}
      <div className="absolute inset-0">
        {slides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-1000 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <img 
              src={slide.image} 
              alt={slide.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-transparent"></div>
          </div>
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 py-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="text-white">
            <h1 className="text-4xl md:text-5xl lg:text-7xl font-bold mb-6 leading-tight">
              Premium <span className="text-green-400">Flooring</span><br />
              Solutions for<br />
              <span className="text-green-400">Bangor & Northern Ireland</span>
            </h1>
            <p className="text-lg lg:text-xl mb-8 leading-relaxed text-gray-200">
              Transform your space with our extensive range of {flooringProducts.length}+ premium products including tiles, laminate, 
              real wood, LVT, and carpet. Professional installation and unbeatable guarantees.
            </p>

            {/* Trust badges with micro-interactions */}
            <div className="flex flex-wrap gap-3 mb-8">
              <div className="trust-badge">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z"/>
                </svg>
                0% Finance
              </div>
              <div className="trust-badge">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Quote Match
              </div>
              <div className="trust-badge">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Expert Installation
              </div>
            </div>

            {/* CTA buttons with modern design */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button 
                onClick={scrollToProducts}
                className="cta-button-primary"
              >
                Browse Products →
              </button>
              <button 
                onClick={scrollToContact}
                className="cta-button-secondary"
              >
                Get Free Quote
              </button>
            </div>
          </div>

          {/* Floating stats card */}
          <div className="relative">
            <div className="glass-card p-8 rounded-2xl">
              <div className="text-center mb-6">
                <div className="text-4xl font-bold text-green-600 mb-2">4.9</div>
                <div className="text-gray-700 font-medium">Customer Rating</div>
                <div className="flex justify-center text-yellow-400 text-lg mb-2">
                  ★★★★★
                </div>
                <div className="text-sm text-gray-600">250+ Happy Customers</div>
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-green-600">{flooringProducts.length}+</div>
                  <div className="text-sm text-gray-600">Products</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">700+</div>
                  <div className="text-sm text-gray-600">Tile Designs</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">1</div>
                  <div className="text-sm text-gray-600">Bangor Showroom</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Slide indicators */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentSlide ? 'bg-green-400' : 'bg-white/50'
            }`}
          />
        ))}
      </div>

      <style jsx>{`
        .trust-badge {
          @apply bg-green-500/90 backdrop-blur-sm text-white px-4 py-2 rounded-lg flex items-center text-sm font-medium transform hover:scale-105 transition-all duration-300 hover:bg-green-400;
        }
        .cta-button-primary {
          @apply bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-green-600 hover:to-green-700 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl;
        }
        .cta-button-secondary {
          @apply border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-all duration-300 transform hover:-translate-y-1;
        }
        .glass-card {
          @apply bg-white/10 backdrop-blur-md border border-white/20 shadow-2xl;
        }
      `}</style>
    </section>
  );
};

// Categories Component with Working View Products Buttons
export const Categories = () => {
  const navigate = useNavigate();

  const categories = [
    {
      id: 'tiles',
      title: "Tiles",
      description: "Ceramic, porcelain, and natural stone tiles for floors and walls.",
      image: "https://images.unsplash.com/photo-1523350165414-082d792c4bcc",
      products: `${flooringProducts.filter(p => p.category === 'tiles').length}+ Options`,
      priceRange: "From £35.00/m²"
    },
    {
      id: 'laminate',
      title: "Laminate",
      description: "Durable laminate flooring with authentic wood appearance.",
      image: "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06",
      products: `${flooringProducts.filter(p => p.category === 'laminate').length}+ Options`,
      priceRange: "From £12.99/m²"
    },
    {
      id: 'real-wood',
      title: "Real Wood",
      description: "Solid and engineered wood flooring for premium interiors.",
      image: "https://images.unsplash.com/photo-1560185008-b033106af5c3",
      products: `${flooringProducts.filter(p => p.category === 'real-wood').length}+ Options`,
      priceRange: "From £45.00/m²"
    },
    {
      id: 'lvt',
      title: "LVT",
      description: "Luxury vinyl tiles and planks with superior durability.",
      image: "https://images.pexels.com/photos/7195891/pexels-photo-7195891.jpeg",
      products: `${flooringProducts.filter(p => p.category === 'lvt').length}+ Options`,
      priceRange: "From £29.99/m²"
    },
    {
      id: 'carpets',
      title: "Carpets",
      description: "Quality carpets and rugs for comfort and style.",
      image: "https://images.unsplash.com/photo-1661632359991-be80a757a018",
      products: `${flooringProducts.filter(p => p.category === 'carpets').length}+ Options`,
      priceRange: "From £28.99/m²"
    }
  ];

  const handleViewProducts = (categoryId) => {
    navigate(`/products?category=${categoryId}`);
  };

  return (
    <section id="categories" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Explore Our Categories</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From elegant tiles to luxury vinyl, discover the perfect flooring solution for 
            every room in your Bangor home.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category) => (
            <div key={category.id} className="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={category.image} 
                  alt={`${category.title} flooring in Bangor`}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent group-hover:from-black/70 transition-all duration-300"></div>
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-xl font-bold text-white mb-2">{category.title}</h3>
                  <p className="text-sm text-white/90">{category.description}</p>
                </div>
              </div>
              <div className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm text-gray-600 font-medium">{category.products}</span>
                  <span className="text-sm font-semibold text-green-600 bg-green-50 px-3 py-1 rounded-full">{category.priceRange}</span>
                </div>
                <button 
                  onClick={() => handleViewProducts(category.id)}
                  className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-3 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-300 font-medium transform hover:-translate-y-0.5 hover:shadow-lg"
                >
                  View Products
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button 
            onClick={() => navigate('/products')}
            className="inline-flex items-center border-2 border-green-600 text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-600 hover:text-white transition-all duration-300 transform hover:-translate-y-0.5"
          >
            View All Categories →
          </button>
        </div>
      </div>
    </section>
  );
};

// Featured Products Component with Enhanced Design
export const FeaturedProducts = () => {
  const [calculatorValues, setCalculatorValues] = useState({});
  const navigate = useNavigate();

  const handleCalculatorChange = (productId, field, value) => {
    setCalculatorValues(prev => ({
      ...prev,
      [productId]: {
        ...prev[productId],
        [field]: value
      }
    }));
  };

  const getCalculatedValues = (productId, basePrice, coverage) => {
    const values = calculatorValues[productId] || {};
    const areaNeeded = parseFloat(values.areaNeeded) || 0;
    const packsNeeded = Math.ceil(areaNeeded / coverage);
    const totalCost = packsNeeded * basePrice;
    
    return {
      packsNeeded,
      totalCost: totalCost.toFixed(2),
      areaNeeded
    };
  };

  return (
    <section id="products" className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Featured Products</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover our handpicked selection of premium flooring solutions, chosen 
            for their exceptional quality and popular appeal in Bangor homes.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredProducts.map((product) => {
            const calculated = getCalculatedValues(product.id, product.price, product.coverage);
            
            return (
              <div key={product.id} className="group bg-white border border-gray-200 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden transform hover:-translate-y-2">
                <div className="relative h-48 overflow-hidden">
                  <img 
                    src={product.image} 
                    alt={`${product.name} flooring available in Bangor`}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute top-4 left-4 bg-gradient-to-r from-green-600 to-green-700 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                    {product.displayCategory}
                  </div>
                  <div className="absolute top-4 right-4 space-y-2">
                    {product.sale && (
                      <div className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                        SALE
                      </div>
                    )}
                    {product.inStock && (
                      <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                        In Stock
                      </div>
                    )}
                  </div>
                  {product.featured && (
                    <div className="absolute bottom-4 left-4 bg-yellow-500 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg">
                      FEATURED
                    </div>
                  )}
                </div>
                
                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-2 group-hover:text-green-600 transition-colors duration-300">{product.name}</h3>
                  <p className="text-gray-600 mb-4 text-sm leading-relaxed">{product.description}</p>
                  
                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl font-bold text-green-600">{product.priceDisplay}</span>
                        {product.originalPrice && (
                          <span className="text-lg text-gray-500 line-through">£{product.originalPrice}</span>
                        )}
                      </div>
                      <span className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">Per m²</span>
                    </div>
                    <div className="text-sm text-gray-500 space-y-1">
                      <div><span className="font-medium">Dimensions:</span> {product.dimensions}</div>
                      <div><span className="font-medium">Grade:</span> {product.grade}</div>
                      <div><span className="font-medium">Warranty:</span> {product.warranty}</div>
                    </div>
                  </div>
                  
                  {/* Enhanced Price Calculator */}
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl mb-4 border">
                    <div className="text-sm font-semibold text-gray-700 mb-3 flex items-center">
                      <svg className="w-4 h-4 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                      </svg>
                      Price Calculator
                    </div>
                    
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div>
                        <label className="block text-gray-600 mb-1 font-medium">Price per m²:</label>
                        <div className="font-bold text-green-600 text-lg">{product.priceDisplay}</div>
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1 font-medium">Coverage per pack:</label>
                        <div className="font-bold text-gray-800">{product.coverage} m²</div>
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1 font-medium">Area needed (m²):</label>
                        <input 
                          type="number" 
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300" 
                          placeholder="Enter area"
                          value={calculatorValues[product.id]?.areaNeeded || ''}
                          onChange={(e) => handleCalculatorChange(product.id, 'areaNeeded', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1 font-medium">Packs needed:</label>
                        <div className="font-bold text-gray-800 bg-white px-3 py-2 rounded-lg border">
                          {calculated.areaNeeded > 0 ? `${calculated.packsNeeded} packs` : '0 packs'}
                        </div>
                      </div>
                    </div>
                    
                    {calculated.areaNeeded > 0 && (
                      <div className="mt-4 pt-3 border-t border-gray-200">
                        <div className="flex justify-between items-center bg-green-50 p-3 rounded-lg">
                          <span className="text-sm text-gray-700 font-medium">Total Cost:</span>
                          <span className="text-xl font-bold text-green-600">£{calculated.totalCost}</span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="space-y-3">
                    <button className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-3 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-300 font-semibold transform hover:-translate-y-0.5 hover:shadow-lg">
                      Add to Quote
                    </button>
                    <button className="w-full border-2 border-gray-300 text-gray-700 py-2 rounded-lg hover:border-green-500 hover:text-green-600 transition-all duration-300 font-medium">
                      Request Sample
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-center mt-12">
          <button 
            onClick={() => navigate('/products')}
            className="bg-gradient-to-r from-green-600 to-green-700 text-white px-8 py-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl"
          >
            View All {flooringProducts.length}+ Products →
          </button>
        </div>
      </div>
    </section>
  );
};

// About Section Component
export const AboutSection = () => {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-6">
              Why Choose Tiles & Wood Floor Store Bangor?
            </h2>
            <p className="text-lg text-gray-600 mb-8">
              With over 20 years of experience in the flooring industry, we've established ourselves 
              as Northern Ireland's premier flooring destination based in Bangor. Our commitment to quality, 
              competitive pricing, and exceptional customer service sets us apart.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start group">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Quality Guarantee</h3>
                  <p className="text-gray-600">All our {flooringProducts.length}+ products come with manufacturer warranties and our quality guarantee.</p>
                </div>
              </div>
              <div className="flex items-start group">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Best Price Promise</h3>
                  <p className="text-gray-600">We'll match any genuine written quote from a local competitor.</p>
                </div>
              </div>
              <div className="flex items-start group">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Professional Installation</h3>
                  <p className="text-gray-600">Expert fitting service with skilled craftsmen and full insurance coverage.</p>
                </div>
              </div>
              <div className="flex items-start group">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Customer Care</h3>
                  <p className="text-gray-600">Dedicated support team available 7 days a week to help with your needs.</p>
                </div>
              </div>
            </div>
          </div>
          <div className="relative">
            <img 
              src="https://images.pexels.com/photos/4940756/pexels-photo-4940756.jpeg" 
              alt="Professional flooring showroom in Bangor" 
              className="rounded-2xl shadow-2xl w-full h-96 object-cover"
            />
            <div className="absolute top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg font-semibold shadow-lg">
              5 Years Guarantee
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Continue with other components... (Services, Installation, Gallery, Testimonials, Contact, ProductGrid, Footer)
// I'll keep the rest of the components the same for brevity, but they're updated with the new product data

// Services Section Component
export const ServicesSection = () => {
  const services = [
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      title: "Free Quotation",
      description: "Professional site survey and detailed written quotation with no obligation."
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      title: "Professional Installation",
      description: "Expert fitting by skilled craftsmen with full insurance and guarantee."
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
        </svg>
      ),
      title: "0% Finance Available",
      description: "Interest-free credit options available subject to status and terms."
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      ),
      title: "Free Samples",
      description: "Take samples home to see how they look in your space before you buy."
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      title: "Price Match Guarantee",
      description: "We'll match any genuine written quote from a local competitor."
    },
    {
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
        </svg>
      ),
      title: "Extended Warranties",
      description: "Comprehensive warranties on all products and installation work."
    }
  ];

  return (
    <section id="services" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Our Services in Bangor</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From initial consultation to final installation, we provide comprehensive flooring services 
            from our Bangor showroom to ensure your complete satisfaction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div key={index} className="group bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <div className="bg-gradient-to-br from-green-100 to-green-200 text-green-600 p-3 rounded-xl w-fit mb-4 group-hover:from-green-200 group-hover:to-green-300 transition-all duration-300">
                {service.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3 group-hover:text-green-600 transition-colors duration-300">{service.title}</h3>
              <p className="text-gray-600">{service.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Installation Section Component
export const InstallationSection = () => {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Professional Installation in Bangor</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Our skilled craftsmen ensure perfect installation every time, backed by comprehensive warranties.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <img 
                src="https://images.unsplash.com/photo-1624574470112-46944be68409" 
                alt="Professional flooring installation in Bangor" 
                className="rounded-2xl shadow-md h-48 w-full object-cover hover:shadow-xl transition-shadow duration-300"
              />
              <img 
                src="https://images.unsplash.com/photo-1622936063167-e32e9f955438" 
                alt="Flooring installation process in Northern Ireland" 
                className="rounded-2xl shadow-md h-48 w-full object-cover hover:shadow-xl transition-shadow duration-300"
              />
              <img 
                src="https://images.pexels.com/photos/5974053/pexels-photo-5974053.jpeg" 
                alt="Installation tools and materials" 
                className="rounded-2xl shadow-md h-48 w-full object-cover hover:shadow-xl transition-shadow duration-300"
              />
              <img 
                src="https://images.pexels.com/photos/1249610/pexels-photo-1249610.jpeg" 
                alt="Professional installation work by TWFS" 
                className="rounded-2xl shadow-md h-48 w-full object-cover hover:shadow-xl transition-shadow duration-300"
              />
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Why Choose Our Installation Service?</h3>
            <div className="space-y-4">
              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Skilled Craftsmen</h4>
                  <p className="text-gray-600">Over 20 years of experience in all types of flooring installation across Northern Ireland.</p>
                </div>
              </div>
              
              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Fully Insured</h4>
                  <p className="text-gray-600">Complete public liability insurance for your peace of mind.</p>
                </div>
              </div>
              
              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Quality Guarantee</h4>
                  <p className="text-gray-600">5-year guarantee on all installation work and materials.</p>
                </div>
              </div>
              
              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Timely Service</h4>
                  <p className="text-gray-600">Reliable scheduling with minimal disruption to your daily routine.</p>
                </div>
              </div>
            </div>
            
            <div className="mt-8">
              <button 
                onClick={() => {
                  const element = document.getElementById('contact');
                  if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                  }
                }}
                className="bg-gradient-to-r from-green-600 to-green-700 text-white px-8 py-3 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-lg"
              >
                Book Installation →
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Gallery Section Component
export const GallerySection = () => {
  const galleryImages = [
    {
      image: "https://images.unsplash.com/photo-1560184897-1ee3713708ee",
      title: "Modern Living Room in Bangor",
      category: "Real Wood"
    },
    {
      image: "https://images.pexels.com/photos/1454804/pexels-photo-1454804.jpeg",
      title: "Luxury Bathroom in North Down",
      category: "Tiles"
    },
    {
      image: "https://images.pexels.com/photos/18156022/pexels-photo-18156022.jpeg",
      title: "Contemporary Kitchen in Belfast",
      category: "LVT"
    },
    {
      image: "https://images.pexels.com/photos/3995842/pexels-photo-3995842.jpeg",
      title: "Cozy Study in Holywood",
      category: "Laminate"
    },
    {
      image: "https://images.unsplash.com/photo-1592240989300-8673561d04b8",
      title: "Master Bathroom in Newtownards",
      category: "Tiles"
    },
    {
      image: "https://images.pexels.com/photos/105934/pexels-photo-105934.jpeg",
      title: "Guest Bedroom in Donaghadee",
      category: "Carpets"
    }
  ];

  return (
    <section id="gallery" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Gallery</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            See our flooring solutions in beautiful homes across North Down and Greater Belfast.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {galleryImages.map((item, index) => (
            <div key={index} className="relative group overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2">
              <img 
                src={item.image} 
                alt={item.title}
                className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent group-hover:from-black/70 transition-all duration-300"></div>
              <div className="absolute bottom-4 left-4 right-4 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                <div className="bg-white/95 backdrop-blur-sm p-3 rounded-lg shadow-lg">
                  <h3 className="font-bold text-gray-800">{item.title}</h3>
                  <p className="text-sm text-green-600 font-medium">{item.category}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="border-2 border-green-600 text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-600 hover:text-white transition-all duration-300 transform hover:-translate-y-0.5">
            View More Projects →
          </button>
        </div>
      </div>
    </section>
  );
};

// Testimonials Section Component
export const TestimonialsSection = () => {
  const testimonials = [
    {
      name: "Sarah Mitchell",
      location: "Bangor, Co. Down",
      rating: 5,
      text: "Absolutely delighted with our new oak flooring! The team was professional, punctual, and the quality of work exceeded our expectations. Highly recommend!",
      image: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150"
    },
    {
      name: "Michael O'Brien",
      location: "Holywood, Co. Down",
      rating: 5,
      text: "Fantastic service from start to finish. The showroom staff were knowledgeable and helpful, and the installation team did an excellent job with our tiles.",
      image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150"
    },
    {
      name: "Emma Thompson",
      location: "Newtownards, Co. Down",
      rating: 5,
      text: "Great value for money and superb customer service. The laminate flooring looks amazing and was fitted perfectly. Would definitely use again.",
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150"
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">What Our Customers Say</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Read what our satisfied customers across North Down have to say about our products and services.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-gradient-to-br from-gray-50 to-gray-100 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center mb-4">
                <img 
                  src={testimonial.image} 
                  alt={testimonial.name}
                  className="w-12 h-12 rounded-full object-cover mr-4"
                />
                <div>
                  <h4 className="font-semibold text-gray-800">{testimonial.name}</h4>
                  <p className="text-sm text-gray-600">{testimonial.location}</p>
                </div>
              </div>
              <div className="flex mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-gray-600 italic">"{testimonial.text}"</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Contact Section Component
export const ContactSection = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    alert('Thank you for your enquiry! We will be in touch soon.');
    setFormData({ name: '', email: '', phone: '', message: '' });
  };

  return (
    <section id="contact" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Contact Our Bangor Showroom</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get in touch for a free consultation and quotation. Visit our Bangor showroom or contact us for all your flooring needs in Northern Ireland.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Get In Touch</h3>
            
            <div className="space-y-6">
              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Bangor Showroom</h4>
                  <div className="text-gray-600">
                    <div className="font-medium">1 Balloo Avenue, Bangor</div>
                    <div>BT19 7WP, Northern Ireland</div>
                    <div className="mt-2 text-sm">
                      <span className="font-medium text-green-600">Private parking available</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Phone</h4>
                  <div className="text-gray-600">
                    <div className="font-medium text-lg">
                      <a href="tel:02891225400" className="text-green-600 hover:text-green-700 transition-colors">
                        028 9122 5400
                      </a>
                    </div>
                    <div className="text-sm mt-1">
                      <div>Monday - Saturday: 9:00 AM - 6:00 PM</div>
                      <div>Sunday: 1:00 PM - 5:00 PM</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start group">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4 group-hover:bg-green-200 transition-colors duration-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Email</h4>
                  <div className="text-gray-600">
                    <a href="mailto:info@tileswoodfloorni.com" className="text-green-600 hover:text-green-700 transition-colors">
                      info@tileswoodfloorni.com
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Send Us A Message</h3>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Name *</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                  placeholder="Your full name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                  placeholder="your.email@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                  placeholder="Your phone number"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Message *</label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-300"
                  placeholder="Tell us about your flooring requirements..."
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-lg"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

// Enhanced Product Grid Component for Products Page
export const ProductGrid = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const categoryFilter = searchParams.get('category');
  const searchQuery = searchParams.get('search');
  
  const [filter, setFilter] = useState(categoryFilter || 'all');
  const [sortBy, setSortBy] = useState('name');
  const [searchTerm, setSearchTerm] = useState(searchQuery || '');

  // Filter and search products
  let filteredProducts = filter === 'all' ? flooringProducts : flooringProducts.filter(p => p.category === filter);
  
  if (searchTerm) {
    filteredProducts = searchProducts(searchTerm, filter);
  }

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });

  return (
    <section className="py-16 bg-gray-50" style={{ marginTop: '120px' }}>
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">
            {searchTerm ? `Search Results for "${searchTerm}"` : 'All Products'}
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Browse our complete collection of {flooringProducts.length}+ premium flooring solutions available at our Bangor showroom.
          </p>
        </div>

        {/* Enhanced Filters */}
        <div className="flex flex-col lg:flex-row justify-between items-center mb-8 space-y-4 lg:space-y-0">
          <div className="flex flex-wrap gap-2">
            {productCategories.map(category => (
              <button
                key={category.id}
                onClick={() => setFilter(category.id)}
                className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 transform hover:-translate-y-0.5 ${
                  filter === category.id 
                    ? 'bg-gradient-to-r from-green-600 to-green-700 text-white shadow-lg' 
                    : 'bg-white text-gray-700 hover:bg-green-50 hover:text-green-600 shadow-md'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>
          
          <div className="flex items-center space-x-4">
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 w-64"
            />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 bg-white shadow-md"
            >
              <option value="name">Sort by Name</option>
              <option value="price">Sort by Price</option>
            </select>
          </div>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {sortedProducts.map(product => (
            <div key={product.id} className="group bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden transform hover:-translate-y-2">
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={product.image} 
                  alt={`${product.name} available at Tiles & Wood Floor Store Bangor`}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute top-4 left-4 bg-gradient-to-r from-green-600 to-green-700 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                  {product.displayCategory}
                </div>
                <div className="absolute top-4 right-4 space-y-2">
                  {product.sale && (
                    <div className="bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                      SALE
                    </div>
                  )}
                  {product.clearance && (
                    <div className="bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                      CLEARANCE
                    </div>
                  )}
                  {product.inStock && (
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium shadow-lg">
                      In Stock
                    </div>
                  )}
                </div>
              </div>
              
              <div className="p-6">
                <h3 className="font-bold text-gray-800 mb-2 group-hover:text-green-600 transition-colors duration-300">{product.name}</h3>
                <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                <div className="flex justify-between items-center mb-4">
                  <div className="flex items-center space-x-2">
                    <span className="text-xl font-bold text-green-600">{product.priceDisplay}</span>
                    {product.originalPrice && (
                      <span className="text-sm text-gray-500 line-through">£{product.originalPrice}</span>
                    )}
                  </div>
                  <span className="text-sm text-gray-600 bg-gray-100 px-2 py-1 rounded">Per m²</span>
                </div>
                <div className="text-xs text-gray-500 mb-4">
                  <div><span className="font-medium">Warranty:</span> {product.warranty}</div>
                  {product.waterproof && <div className="text-blue-600 font-medium">✓ Waterproof</div>}
                  {product.underfloorHeating && <div className="text-orange-600 font-medium">✓ UFH Compatible</div>}
                </div>
                <div className="space-y-2">
                  <button className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-2 rounded-lg hover:from-green-700 hover:to-green-800 transition-all duration-300 transform hover:-translate-y-0.5 font-medium">
                    Add to Quote
                  </button>
                  <button className="w-full border-2 border-gray-300 text-gray-700 py-2 rounded-lg hover:border-green-500 hover:text-green-600 transition-all duration-300 font-medium">
                    Request Sample
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {sortedProducts.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg mb-4">No products found</div>
            <button 
              onClick={() => {setFilter('all'); setSearchTerm('');}}
              className="text-green-600 hover:text-green-700 font-medium"
            >
              Clear filters and view all products
            </button>
          </div>
        )}
      </div>
    </section>
  );
};

// Footer Component with Enhanced SEO
export const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center mb-4">
              <div className="bg-gradient-to-r from-green-600 to-green-700 text-white px-3 py-2 rounded-lg font-bold text-xl mr-3 shadow-lg">
                TWFS
              </div>
              <div>
                <h3 className="font-bold text-lg">Tiles & Wood Floor Store</h3>
                <p className="text-green-400 text-sm">Bangor, Northern Ireland</p>
              </div>
            </div>
            <p className="text-gray-400 mb-4">
              Northern Ireland's premier flooring destination with over 20 years of experience 
              and {flooringProducts.length}+ premium products available from our Bangor showroom.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-green-400 transition-colors duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-green-400 transition-colors duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-green-400 transition-colors duration-300">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.097.118.112.222.082.343-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.751-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001.012.001z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-lg mb-4 text-green-400">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-400 hover:text-white transition-colors duration-300">Home</Link></li>
              <li><Link to="/products" className="text-gray-400 hover:text-white transition-colors duration-300">All Products ({flooringProducts.length})</Link></li>
              <li><Link to="/products?category=tiles" className="text-gray-400 hover:text-white transition-colors duration-300">Tiles</Link></li>
              <li><Link to="/products?category=laminate" className="text-gray-400 hover:text-white transition-colors duration-300">Laminate</Link></li>
              <li><Link to="/products?category=real-wood" className="text-gray-400 hover:text-white transition-colors duration-300">Real Wood</Link></li>
              <li><Link to="/products?category=lvt" className="text-gray-400 hover:text-white transition-colors duration-300">LVT</Link></li>
              <li><Link to="/products?category=carpets" className="text-gray-400 hover:text-white transition-colors duration-300">Carpets</Link></li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-semibold text-lg mb-4 text-green-400">Services</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">Free Quotation</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">Professional Installation</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">Free Samples</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">Price Match</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">0% Finance</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors duration-300">Warranty</a></li>
            </ul>
          </div>

          {/* Contact Info - SEO Optimized */}
          <div>
            <h4 className="font-semibold text-lg mb-4 text-green-400">Contact Bangor Showroom</h4>
            <div className="space-y-4">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-green-400 mt-1 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                </svg>
                <div>
                  <div className="text-gray-300">
                    <div className="font-medium text-white">Tiles & Wood Floor Store Bangor</div>
                    <div>1 Balloo Avenue, Bangor</div>
                    <div>BT19 7WP, Northern Ireland</div>
                    <div className="mt-1 text-sm text-green-400">Free parking available</div>
                  </div>
                </div>
              </div>
              <div className="flex items-center">
                <svg className="w-5 h-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                </svg>
                <a href="tel:02891225400" className="text-gray-300 hover:text-white transition-colors duration-300">028 9122 5400</a>
              </div>
              <div className="flex items-center">
                <svg className="w-5 h-5 text-green-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
                <a href="mailto:info@tileswoodfloorni.com" className="text-gray-300 hover:text-white transition-colors duration-300">info@tileswoodfloorni.com</a>
              </div>
              <div className="mt-4">
                <div className="text-sm text-gray-300">
                  <div className="font-semibold text-white">Opening Hours:</div>
                  <div>Monday - Saturday: 9:00 AM - 6:00 PM</div>
                  <div>Sunday: 1:00 PM - 5:00 PM</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Tiles & Wood Floor Store Bangor, Northern Ireland. All rights reserved. | 
            <a href="#" className="hover:text-white transition-colors duration-300 ml-1">Privacy Policy</a> | 
            <a href="#" className="hover:text-white transition-colors duration-300 ml-1">Terms & Conditions</a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default { 
  Header, 
  Hero, 
  AboutSection, 
  Categories, 
  FeaturedProducts, 
  Footer,
  ServicesSection,
  GallerySection,
  TestimonialsSection,
  ContactSection,
  ProductGrid,
  InstallationSection
};
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

// Header Component
export const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-lg relative z-50">
      {/* Top green banner */}
      <div className="bg-green-600 text-white py-2 px-4 text-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-6 mb-2 md:mb-0">
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              028 9122 5400
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
              info@tileswoodfloorni.com
            </span>
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

      {/* Main navigation */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <div className="bg-green-600 text-white px-3 py-2 rounded font-bold text-xl mr-3">
              TWFS
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">Tiles & Wood Floor Store</h1>
              <p className="text-sm text-gray-600">Premium Flooring Solutions</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Home</Link>
            <Link to="/products" className="text-gray-700 hover:text-green-600 font-medium transition-colors">All Products</Link>
            <a href="#tiles" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Tiles</a>
            <a href="#laminate" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Laminate</a>
            <a href="#real-wood" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Real Wood</a>
            <a href="#lvt" className="text-gray-700 hover:text-green-600 font-medium transition-colors">LVT</a>
            <a href="#carpets" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Carpets</a>
            <a href="#gallery" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Gallery</a>
            <a href="#services" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Services</a>
            <Link to="/contact" className="text-gray-700 hover:text-green-600 font-medium transition-colors">Contact</Link>
          </nav>

          {/* Search and CTA */}
          <div className="flex items-center space-x-4">
            <div className="relative hidden md:block">
              <input
                type="text"
                placeholder="Search products..."
                className="w-48 lg:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <button className="absolute right-2 top-2">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <button className="bg-green-600 text-white px-4 lg:px-6 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">
              Get Quote
            </button>
            <button className="lg:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="lg:hidden mt-4 py-4 border-t border-gray-200 bg-white absolute left-0 right-0 shadow-lg">
            <div className="px-4">
              <nav className="flex flex-col space-y-3">
                <Link to="/" className="text-gray-700 hover:text-green-600 font-medium py-2">Home</Link>
                <Link to="/products" className="text-gray-700 hover:text-green-600 font-medium py-2">All Products</Link>
                <a href="#tiles" className="text-gray-700 hover:text-green-600 font-medium py-2">Tiles</a>
                <a href="#laminate" className="text-gray-700 hover:text-green-600 font-medium py-2">Laminate</a>
                <a href="#real-wood" className="text-gray-700 hover:text-green-600 font-medium py-2">Real Wood</a>
                <a href="#lvt" className="text-gray-700 hover:text-green-600 font-medium py-2">LVT</a>
                <a href="#carpets" className="text-gray-700 hover:text-green-600 font-medium py-2">Carpets</a>
                <a href="#gallery" className="text-gray-700 hover:text-green-600 font-medium py-2">Gallery</a>
                <a href="#services" className="text-gray-700 hover:text-green-600 font-medium py-2">Services</a>
                <Link to="/contact" className="text-gray-700 hover:text-green-600 font-medium py-2">Contact</Link>
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
        )}
      </div>
    </header>
  );
};

// Hero Section Component
export const Hero = () => {
  return (
    <section className="relative bg-gradient-to-r from-green-50 to-green-100 py-16 lg:py-24">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left content */}
          <div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-800 mb-6 leading-tight">
              Premium <span className="text-green-600">Flooring</span><br />
              Solutions for<br />
              <span className="text-green-600">Northern Ireland</span>
            </h1>
            <p className="text-lg lg:text-xl text-gray-600 mb-8 leading-relaxed">
              Transform your space with our extensive range of tiles, laminate, 
              real wood, LVT, and carpet. Over 300+ floors and 700+ tiles with 
              professional installation and unbeatable guarantees.
            </p>

            {/* Trust badges */}
            <div className="flex flex-wrap gap-3 mb-8">
              <div className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center text-sm font-medium">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 0v12h8V4H6z"/>
                </svg>
                0% Finance
              </div>
              <div className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center text-sm font-medium">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Quote Match
              </div>
              <div className="bg-green-600 text-white px-4 py-2 rounded-lg flex items-center text-sm font-medium">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                Expert Installation
              </div>
            </div>

            {/* CTA buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors">
                Browse Products →
              </button>
              <button className="border border-green-600 text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors">
                Get Free Quote
              </button>
            </div>
          </div>

          {/* Right image */}
          <div className="relative">
            <img 
              src="https://images.pexels.com/photos/8146313/pexels-photo-8146313.jpeg" 
              alt="Modern flooring showroom in Bangor" 
              className="rounded-lg shadow-2xl w-full h-96 lg:h-[500px] object-cover"
            />
            <div className="absolute -bottom-6 -right-6 bg-white p-6 rounded-lg shadow-lg">
              <div className="flex items-center">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">4.9</div>
                  <div className="text-sm text-gray-600">Rating</div>
                  <div className="flex text-yellow-400 text-sm">
                    ★★★★★
                  </div>
                  <div className="text-xs text-gray-500 mt-1">250+ Reviews</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">300+</div>
            <div className="text-gray-600">Floor Options</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">700+</div>
            <div className="text-gray-600">Tile Designs</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">1</div>
            <div className="text-gray-600">Bangor Showroom</div>
          </div>
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
              Why Choose Tiles & Wood Floor Store?
            </h2>
            <p className="text-lg text-gray-600 mb-8">
              With over 20 years of experience in the flooring industry, we've established ourselves 
              as Northern Ireland's premier flooring destination based in Bangor. Our commitment to quality, 
              competitive pricing, and exceptional customer service sets us apart.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-start">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Quality Guarantee</h3>
                  <p className="text-gray-600">All our products come with manufacturer warranties and our quality guarantee.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Best Price Promise</h3>
                  <p className="text-gray-600">We'll match any genuine written quote from a local competitor.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Professional Installation</h3>
                  <p className="text-gray-600">Expert fitting service with skilled craftsmen and full insurance coverage.</p>
                </div>
              </div>
              <div className="flex items-start">
                <div className="bg-green-100 p-3 rounded-lg mr-4 flex-shrink-0">
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
              className="rounded-lg shadow-xl w-full h-96 object-cover"
            />
            <div className="absolute top-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg font-semibold">
              5 Years Guarantee
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Categories Component
export const Categories = () => {
  const categories = [
    {
      id: 'tiles',
      title: "Tiles",
      description: "Ceramic, porcelain, and natural stone tiles for floors and walls.",
      image: "https://images.unsplash.com/photo-1523350165414-082d792c4bcc",
      products: "200+ Options",
      priceRange: "From £12.99/m²"
    },
    {
      id: 'laminate',
      title: "Laminate",
      description: "Durable laminate flooring with authentic wood appearance.",
      image: "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06",
      products: "150+ Options",
      priceRange: "From £15.99/m²"
    },
    {
      id: 'real-wood',
      title: "Real Wood",
      description: "Solid and engineered wood flooring for premium interiors.",
      image: "https://images.unsplash.com/photo-1560185008-b033106af5c3",
      products: "100+ Options",
      priceRange: "From £35.99/m²"
    },
    {
      id: 'lvt',
      title: "LVT",
      description: "Luxury vinyl tiles and planks with superior durability.",
      image: "https://images.pexels.com/photos/7195891/pexels-photo-7195891.jpeg",
      products: "80+ Options",
      priceRange: "From £19.99/m²"
    },
    {
      id: 'carpets',
      title: "Carpets",
      description: "Quality carpets and rugs for comfort and style.",
      image: "https://images.unsplash.com/photo-1661632359991-be80a757a018",
      products: "120+ Options",
      priceRange: "From £8.99/m²"
    }
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Explore Our Categories</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From elegant tiles to luxury vinyl, discover the perfect flooring solution for 
            every room in your home.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category) => (
            <div key={category.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
              <div className="relative h-48 overflow-hidden">
                <img 
                  src={category.image} 
                  alt={category.title}
                  className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-black bg-opacity-20 hover:bg-opacity-30 transition-opacity duration-300"></div>
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-xl font-bold text-white mb-2">{category.title}</h3>
                  <p className="text-sm text-white opacity-90">{category.description}</p>
                </div>
              </div>
              <div className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <span className="text-sm text-gray-600">{category.products}</span>
                  <span className="text-sm font-semibold text-green-600">{category.priceRange}</span>
                </div>
                <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors font-medium">
                  View Products
                </button>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <Link to="/products" className="inline-block border border-green-600 text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors">
            View All Categories →
          </Link>
        </div>
      </div>
    </section>
  );
};

// Featured Products Component with Northern Ireland Standard Products
export const FeaturedProducts = () => {
  const [calculatorValues, setCalculatorValues] = useState({});

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

  const products = [
    {
      id: 1,
      name: "New Oak Herringbone",
      description: "Beautiful natural oak herringbone parquet flooring available in 18mm thickness. Perfect for traditional and contemporary spaces.",
      price: 45,
      priceDisplay: "£45",
      image: "https://images.unsplash.com/photo-1560185008-b033106af5c3",
      category: "Real Wood",
      coverage: 2.5,
      dimensions: "18mm x 70mm x 300mm",
      grade: "Prime Grade",
      finish: "Natural Oil",
      installation: "Nail/Glue Down",
      warranty: "25 Years",
      inStock: true
    },
    {
      id: 2,
      name: "Decora 8mm Lunar Grey",
      description: "High-quality 8mm laminate with realistic wood finish and AC3 wear rating. Perfect for the entire home.",
      price: 23.95,
      priceDisplay: "£23.95",
      image: "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06",
      category: "Laminate",
      coverage: 2.162,
      dimensions: "8mm x 193mm x 1380mm",
      grade: "AC3 Commercial",
      finish: "Matt Textured",
      installation: "Click System",
      warranty: "15 Years",
      inStock: true
    },
    {
      id: 3,
      name: "Balterio Supreme 4V 8mm Flint Grey Oak (Barrel Oak)",
      description: "Premium laminate flooring with authentic grey oak pattern. Available in 194mm x 1286mm tile format with beveled edges.",
      price: 23.67,
      priceDisplay: "£23.67",
      image: "https://images.unsplash.com/photo-1575204015311-0fe377370780",
      category: "Laminate",
      coverage: 2.162,
      dimensions: "8mm x 194mm x 1286mm",
      grade: "AC4 Commercial",
      finish: "Embossed",
      installation: "Click System",
      warranty: "20 Years",
      inStock: true
    },
    {
      id: 4,
      name: "Belstone Cream",
      description: "Premium ceramic tile with superior durability. Available in 600x600mm format. Perfect for kitchens and bathrooms.",
      price: 40,
      priceDisplay: "£40",
      image: "https://images.unsplash.com/photo-1580398562556-d33329a0f29b",
      category: "Tiles",
      coverage: 1.44,
      dimensions: "600mm x 600mm",
      grade: "First Quality",
      finish: "Matt",
      installation: "Adhesive",
      warranty: "Lifetime",
      inStock: true
    },
    {
      id: 5,
      name: "Balterio Astra Ivory",
      description: "Premium ceramic tile with superior durability. Available in 600x600mm format. Perfect for kitchens and bathrooms.",
      price: 35,
      priceDisplay: "£35",
      image: "https://images.pexels.com/photos/1454804/pexels-photo-1454804.jpeg",
      category: "Tiles",
      coverage: 1.44,
      dimensions: "600mm x 600mm",
      grade: "First Quality",
      finish: "Polished",
      installation: "Adhesive",
      warranty: "Lifetime",
      inStock: true
    },
    {
      id: 6,
      name: "Majestica Natural",
      description: "Premium ceramic tile with superior durability. Available in 600x600mm format. Perfect for kitchens and bathrooms.",
      price: 39,
      priceDisplay: "£39",
      image: "https://images.unsplash.com/photo-1592240989300-8673561d04b8",
      category: "Tiles",
      coverage: 1.44,
      dimensions: "600mm x 600mm",
      grade: "First Quality",
      finish: "Natural",
      installation: "Adhesive",
      warranty: "Lifetime",
      inStock: true
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Featured Products</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover our handpicked selection of premium flooring solutions, chosen 
            for their exceptional quality and popular appeal.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products.map((product) => {
            const calculated = getCalculatedValues(product.id, product.price, product.coverage);
            
            return (
              <div key={product.id} className="bg-white border border-gray-200 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
                <div className="relative h-48 overflow-hidden rounded-t-lg">
                  <img 
                    src={product.image} 
                    alt={product.name}
                    className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  />
                  <div className="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded text-sm font-medium">
                    {product.category}
                  </div>
                  {product.inStock && (
                    <div className="absolute top-4 right-4 bg-green-100 text-green-800 px-3 py-1 rounded text-sm font-medium">
                      In Stock
                    </div>
                  )}
                </div>
                
                <div className="p-6">
                  <h3 className="text-xl font-bold text-gray-800 mb-2">{product.name}</h3>
                  <p className="text-gray-600 mb-4 text-sm leading-relaxed">{product.description}</p>
                  
                  <div className="mb-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-2xl font-bold text-green-600">{product.priceDisplay}</span>
                      <span className="text-sm text-gray-600">Per m²</span>
                    </div>
                    <div className="text-sm text-gray-500 space-y-1">
                      <div>Dimensions: {product.dimensions}</div>
                      <div>Grade: {product.grade}</div>
                    </div>
                  </div>
                  
                  {/* Price Calculator - Matching Original Design */}
                  <div className="bg-gray-50 p-4 rounded-lg mb-4">
                    <div className="text-sm font-semibold text-gray-700 mb-3">Price Calculator</div>
                    
                    <div className="grid grid-cols-2 gap-3 text-sm">
                      <div>
                        <label className="block text-gray-600 mb-1">Price per m²:</label>
                        <div className="font-semibold text-gray-800">{product.priceDisplay}</div>
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1">Coverage per pack:</label>
                        <div className="font-semibold text-gray-800">{product.coverage} m²</div>
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1">Area needed (m²):</label>
                        <input 
                          type="number" 
                          className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-green-500" 
                          placeholder="0"
                          value={calculatorValues[product.id]?.areaNeeded || ''}
                          onChange={(e) => handleCalculatorChange(product.id, 'areaNeeded', e.target.value)}
                        />
                      </div>
                      <div>
                        <label className="block text-gray-600 mb-1">Packs area to m²:</label>
                        <div className="font-semibold text-gray-800">
                          {calculated.areaNeeded > 0 ? `${calculated.packsNeeded} packs` : '0 packs'}
                        </div>
                      </div>
                    </div>
                    
                    {calculated.areaNeeded > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-200">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-600">Total Cost:</span>
                          <span className="text-lg font-bold text-green-600">£{calculated.totalCost}</span>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <button className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 transition-colors font-semibold">
                    Price Calculator
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        <div className="text-center mt-12">
          <Link to="/products" className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors">
            View All Products →
          </Link>
        </div>
      </div>
    </section>
  );
};

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
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Our Services</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From initial consultation to final installation, we provide comprehensive flooring services 
            from our Bangor showroom to ensure your complete satisfaction.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <div key={index} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="bg-green-100 text-green-600 p-3 rounded-lg w-fit mb-4">
                {service.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3">{service.title}</h3>
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
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Professional Installation</h2>
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
                className="rounded-lg shadow-md h-48 w-full object-cover"
              />
              <img 
                src="https://images.unsplash.com/photo-1622936063167-e32e9f955438" 
                alt="Flooring installation process in Northern Ireland" 
                className="rounded-lg shadow-md h-48 w-full object-cover"
              />
              <img 
                src="https://images.pexels.com/photos/5974053/pexels-photo-5974053.jpeg" 
                alt="Installation tools and materials" 
                className="rounded-lg shadow-md h-48 w-full object-cover"
              />
              <img 
                src="https://images.pexels.com/photos/1249610/pexels-photo-1249610.jpeg" 
                alt="Professional installation work by TWFS" 
                className="rounded-lg shadow-md h-48 w-full object-cover"
              />
            </div>
          </div>

          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Why Choose Our Installation Service?</h3>
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Skilled Craftsmen</h4>
                  <p className="text-gray-600">Over 20 years of experience in all types of flooring installation across Northern Ireland.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Fully Insured</h4>
                  <p className="text-gray-600">Complete public liability insurance for your peace of mind.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-1">Quality Guarantee</h4>
                  <p className="text-gray-600">5-year guarantee on all installation work and materials.</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-2 rounded-full mr-4 flex-shrink-0">
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
              <button className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors">
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
            <div key={index} className="relative group overflow-hidden rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
              <img 
                src={item.image} 
                alt={item.title}
                className="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
              />
              <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-opacity duration-300"></div>
              <div className="absolute bottom-4 left-4 right-4 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
                <div className="bg-white p-3 rounded-lg">
                  <h3 className="font-bold text-gray-800">{item.title}</h3>
                  <p className="text-sm text-green-600">{item.category}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <button className="border border-green-600 text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors">
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
            <div key={index} className="bg-gray-50 p-6 rounded-lg">
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
    // Handle form submission here
    console.log('Form submitted:', formData);
    alert('Thank you for your enquiry! We will be in touch soon.');
    setFormData({ name: '', email: '', phone: '', message: '' });
  };

  return (
    <section id="contact" className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">Contact Us</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get in touch for a free consultation and quotation. Visit our Bangor showroom or contact us for all your flooring needs.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Get In Touch</h3>
            
            <div className="space-y-6">
              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Showroom Location</h4>
                  <div className="text-gray-600">
                    <div className="font-medium">Bangor Showroom</div>
                    <div>1 Balloo Avenue, Bangor</div>
                    <div>BT19 7WP, Northern Ireland</div>
                    <div className="mt-2 text-sm">
                      <span className="font-medium">Private parking available</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Phone</h4>
                  <div className="text-gray-600">
                    <div className="font-medium">028 9122 5400</div>
                    <div className="text-sm mt-1">
                      <div>Monday - Saturday: 9:00 AM - 6:00 PM</div>
                      <div>Sunday: 1:00 PM - 5:00 PM</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="bg-green-100 text-green-600 p-3 rounded-lg mr-4">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                    <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                  </svg>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Email</h4>
                  <div className="text-gray-600">info@tileswoodfloorni.com</div>
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
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
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                  placeholder="Tell us about your flooring requirements..."
                />
              </div>
              
              <button
                type="submit"
                className="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
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

// Product Grid Component (for products page)
export const ProductGrid = () => {
  const allProducts = [
    // Real Wood Products
    {
      id: 1,
      name: "New Oak Herringbone",
      price: 45,
      image: "https://images.unsplash.com/photo-1560185008-b033106af5c3",
      category: "Real Wood",
      inStock: true
    },
    {
      id: 2,
      name: "European Oak Engineered 20mm",
      price: 89.99,
      image: "https://images.unsplash.com/photo-1560184897-1ee3713708ee",
      category: "Real Wood",
      inStock: true
    },
    // Laminate Products
    {
      id: 3,
      name: "Decora 8mm Lunar Grey",
      price: 23.95,
      image: "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06",
      category: "Laminate",
      inStock: true
    },
    {
      id: 4,
      name: "Balterio Supreme 4V 8mm Flint Grey Oak",
      price: 23.67,
      image: "https://images.unsplash.com/photo-1575204015311-0fe377370780",
      category: "Laminate",
      inStock: true
    },
    // Tile Products
    {
      id: 5,
      name: "Belstone Cream",
      price: 40,
      image: "https://images.unsplash.com/photo-1580398562556-d33329a0f29b",
      category: "Tiles",
      inStock: true
    },
    {
      id: 6,
      name: "Balterio Astra Ivory",
      price: 35,
      image: "https://images.pexels.com/photos/1454804/pexels-photo-1454804.jpeg",
      category: "Tiles",
      inStock: true
    },
    {
      id: 7,
      name: "Majestica Natural",
      price: 39,
      image: "https://images.unsplash.com/photo-1592240989300-8673561d04b8",
      category: "Tiles",
      inStock: true
    },
    // LVT Products
    {
      id: 8,
      name: "Karndean Korlok Baltic Painted Oak",
      price: 42.99,
      image: "https://images.pexels.com/photos/7195891/pexels-photo-7195891.jpeg",
      category: "LVT",
      inStock: true
    },
    {
      id: 9,
      name: "Amtico Signature Worn Ash",
      price: 67.50,
      image: "https://images.pexels.com/photos/326862/pexels-photo-326862.jpeg",
      category: "LVT",
      inStock: true
    },
    // Carpet Products
    {
      id: 10,
      name: "Cormar Primo Plus Wool Carpet",
      price: 28.99,
      image: "https://images.unsplash.com/photo-1666868216570-a8f70adcc805",
      category: "Carpets",
      inStock: true
    }
  ];

  const [filter, setFilter] = useState('All');
  const [sortBy, setSortBy] = useState('name');

  const filteredProducts = allProducts.filter(product => 
    filter === 'All' || product.category === filter
  );

  const sortedProducts = [...filteredProducts].sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price;
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    return 0;
  });

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="text-center mb-12">
          <h1 className="text-3xl lg:text-4xl font-bold text-gray-800 mb-4">All Products</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Browse our complete collection of premium flooring solutions available at our Bangor showroom.
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <div className="flex flex-wrap gap-2 mb-4 md:mb-0">
            {['All', 'Real Wood', 'Laminate', 'Tiles', 'LVT', 'Carpets'].map(category => (
              <button
                key={category}
                onClick={() => setFilter(category)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === category 
                    ? 'bg-green-600 text-white' 
                    : 'bg-white text-gray-700 hover:bg-gray-100'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
          
          <div className="flex items-center space-x-4">
            <label className="text-sm text-gray-600">Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="name">Name</option>
              <option value="price">Price</option>
            </select>
          </div>
        </div>

        {/* Product Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {sortedProducts.map(product => (
            <div key={product.id} className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
              <div className="relative h-48 overflow-hidden rounded-t-lg">
                <img 
                  src={product.image} 
                  alt={product.name}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute top-4 left-4 bg-green-600 text-white px-3 py-1 rounded text-sm font-medium">
                  {product.category}
                </div>
                {product.inStock && (
                  <div className="absolute top-4 right-4 bg-green-100 text-green-800 px-3 py-1 rounded text-sm font-medium">
                    In Stock
                  </div>
                )}
              </div>
              
              <div className="p-4">
                <h3 className="font-bold text-gray-800 mb-2">{product.name}</h3>
                <div className="flex justify-between items-center mb-4">
                  <span className="text-xl font-bold text-green-600">£{product.price}</span>
                  <span className="text-sm text-gray-600">Per m²</span>
                </div>
                <div className="space-y-2">
                  <button className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition-colors">
                    Add to Quote
                  </button>
                  <button className="w-full border border-gray-300 text-gray-700 py-2 rounded-lg hover:bg-gray-50 transition-colors">
                    Request Sample
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// Footer Component - REMOVED ALL BALLYMENA REFERENCES
export const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center mb-4">
              <div className="bg-green-600 text-white px-3 py-2 rounded font-bold text-xl mr-3">
                TWFS
              </div>
              <div>
                <h3 className="font-bold text-lg">Tiles & Wood Floor Store</h3>
              </div>
            </div>
            <p className="text-gray-400 mb-4">
              Northern Ireland's premier flooring destination with over 20 years of experience 
              in providing quality flooring solutions from our Bangor showroom.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12.017 0C5.396 0 .029 5.367.029 11.987c0 5.079 3.158 9.417 7.618 11.174-.105-.949-.199-2.403.041-3.439.219-.937 1.406-5.957 1.406-5.957s-.359-.72-.359-1.781c0-1.663.967-2.911 2.168-2.911 1.024 0 1.518.769 1.518 1.688 0 1.029-.653 2.567-.992 3.992-.285 1.193.6 2.165 1.775 2.165 2.128 0 3.768-2.245 3.768-5.487 0-2.861-2.063-4.869-5.008-4.869-3.41 0-5.409 2.562-5.409 5.199 0 1.033.394 2.143.889 2.741.097.118.112.222.082.343-.09.375-.293 1.199-.334 1.363-.053.225-.172.271-.402.165-1.495-.69-2.433-2.878-2.433-4.646 0-3.776 2.748-7.252 7.92-7.252 4.158 0 7.392 2.967 7.392 6.923 0 4.135-2.607 7.462-6.233 7.462-1.214 0-2.357-.629-2.751-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24.009 12.017 24.009c6.624 0 11.99-5.367 11.99-11.988C24.007 5.367 18.641.001.012.001z"/>
                </svg>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-lg mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-400 hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/products" className="text-gray-400 hover:text-white transition-colors">All Products</Link></li>
              <li><a href="#tiles" className="text-gray-400 hover:text-white transition-colors">Tiles</a></li>
              <li><a href="#laminate" className="text-gray-400 hover:text-white transition-colors">Laminate</a></li>
              <li><a href="#real-wood" className="text-gray-400 hover:text-white transition-colors">Real Wood</a></li>
              <li><a href="#lvt" className="text-gray-400 hover:text-white transition-colors">LVT</a></li>
              <li><a href="#carpets" className="text-gray-400 hover:text-white transition-colors">Carpets</a></li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h4 className="font-semibold text-lg mb-4">Services</h4>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Free Quotation</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Professional Installation</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Free Samples</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Price Match</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">0% Finance</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Warranty</a></li>
            </ul>
          </div>

          {/* Contact Info - ONLY BANGOR */}
          <div>
            <h4 className="font-semibold text-lg mb-4">Contact Us</h4>
            <div className="space-y-4">
              <div className="flex items-start">
                <svg className="w-5 h-5 text-green-600 mt-1 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"/>
                </svg>
                <div>
                  <div className="text-gray-400">
                    <div className="font-medium">Bangor Showroom</div>
                    <div>1 Balloo Avenue, Bangor</div>
                    <div>BT19 7WP, Northern Ireland</div>
                    <div className="mt-1 text-sm">Private parking available</div>
                  </div>
                </div>
              </div>
              <div className="flex items-center">
                <svg className="w-5 h-5 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                </svg>
                <span className="text-gray-400">028 9122 5400</span>
              </div>
              <div className="flex items-center">
                <svg className="w-5 h-5 text-green-600 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
                <span className="text-gray-400">info@tileswoodfloorni.com</span>
              </div>
              <div className="mt-4">
                <div className="text-sm text-gray-400">
                  <div className="font-semibold">Opening Hours:</div>
                  <div>Monday - Saturday: 9:00 AM - 6:00 PM</div>
                  <div>Sunday: 1:00 PM - 5:00 PM</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2025 Tiles & Wood Floor Store. All rights reserved. | Privacy Policy | Terms & Conditions</p>
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
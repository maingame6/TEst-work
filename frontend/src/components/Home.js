import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-gray-50 to-stone-100">
      {/* Hero Section - Modern Luxury Design */}
      <section className="relative bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900 overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-amber-500/20 to-orange-600/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-gradient-to-br from-emerald-500/20 to-teal-600/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>
        
        {/* Geometric Pattern Overlay */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"%3E%3Cpolygon fill="%23ffffff" fill-opacity="0.05" points="0,1000 1000,0 1000,1000"/%3E%3C/svg%3E')]"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <div className="inline-flex items-center space-x-2 bg-white/10 backdrop-blur-sm rounded-full px-6 py-3 text-white mb-8">
              <span className="w-2 h-2 bg-amber-400 rounded-full animate-pulse"></span>
              <span className="text-sm font-medium tracking-wide">Premium Quality Since 1995</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-8 tracking-tight leading-tight">
              <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                Luxury Tiles &amp; Premium Flooring
              </span>
              <br />
              <span className="bg-gradient-to-r from-amber-400 via-orange-500 to-amber-600 bg-clip-text text-transparent">
                Premium Flooring
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-300 mb-12 max-w-4xl mx-auto leading-relaxed">
              Transform your space with our exquisite collection of handcrafted tiles and premium flooring solutions, 
              carefully curated for the modern lifestyle.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
              <Link
                to="/products"
                className="group px-10 py-4 bg-gradient-to-r from-amber-500 to-orange-600 text-white rounded-2xl font-semibold hover:from-amber-600 hover:to-orange-700 transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-amber-500/25"
              >
                <span className="flex items-center">
                  Explore Collection
                  <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </span>
              </Link>
              
              <a
                href="#services"
                className="group px-10 py-4 border-2 border-white/30 text-white rounded-2xl font-semibold hover:bg-white/10 backdrop-blur-sm transition-all duration-300 transform hover:scale-105"
              >
                <span className="flex items-center">
                  Our Services
                  <svg className="w-5 h-5 ml-2 group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </span>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section - Modern Grid Layout */}
      <section id="services" className="py-24 bg-white relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-amber-50/50 to-orange-50/50"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <div className="inline-flex items-center space-x-2 bg-amber-100 rounded-full px-6 py-3 text-amber-800 mb-6">
              <span className="w-2 h-2 bg-amber-500 rounded-full"></span>
              <span className="text-sm font-semibold tracking-wide uppercase">Our Expertise</span>
            </div>
            
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 tracking-tight">
              Premium <span className="bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">Solutions</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              From luxury ceramic tiles to authentic hardwood flooring, we provide comprehensive solutions for every space and style preference.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <ServiceCard
              icon="🏛️"
              gradient="from-amber-500 to-orange-600"
              title="Premium Tiles"
              description="Handcrafted ceramic, porcelain, and natural stone tiles with exceptional quality and unique designs."
            />
            
            <ServiceCard
              icon="🪵"
              gradient="from-emerald-500 to-teal-600"
              title="Laminate Flooring"
              description="Durable, water-resistant laminate flooring that combines beauty with practical functionality."
            />
            
            <ServiceCard
              icon="🌿"
              gradient="from-blue-500 to-indigo-600"
              title="Real Wood Flooring"
              description="Authentic hardwood flooring sourced from sustainable forests for timeless elegance."
            />
            
            <ServiceCard
              icon="✨"
              gradient="from-purple-500 to-pink-600"
              title="Luxury Vinyl (LVT)"
              description="Premium vinyl tiles offering superior durability and authentic wood and stone aesthetics."
            />
          </div>
        </div>
      </section>

      {/* Features Section - Modern Cards */}
      <section className="py-24 bg-gradient-to-br from-gray-50 to-slate-100 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 tracking-tight">
              Why Choose <span className="bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">Excellence</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the difference with our commitment to quality, service, and customer satisfaction.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon="⭐"
              title="Premium Quality"
              description="Only the finest materials from trusted global suppliers, ensuring lasting beauty and durability in every product."
              gradient="from-emerald-400 to-emerald-600"
            />
            
            <FeatureCard
              icon="💰"
              title="Best Value"
              description="Competitive pricing without compromising quality, offering exceptional value for your investment."
              gradient="from-blue-400 to-blue-600"
            />
            
            <FeatureCard
              icon="🎯"
              title="Expert Guidance"
              description="Professional consultation and installation support from our experienced team of flooring specialists."
              gradient="from-purple-400 to-purple-600"
            />
          </div>
        </div>
      </section>

      {/* Contact Section - Modern Design */}
      <section className="py-24 bg-gradient-to-br from-slate-900 via-gray-900 to-zinc-900 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-amber-500/10 to-orange-600/10 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-gradient-to-br from-emerald-500/10 to-teal-600/10 rounded-full blur-3xl"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 tracking-tight">
              Visit Our <span className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">Showrooms</span>
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Experience our products firsthand and get expert advice from our knowledgeable team.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <ContactCard
              location="Bangor Showroom"
              address="Bangor, Northern Ireland"
              phone="02891225400"
              email="sales@tileswoodfloorni.com"
              isMain={true}
            />
            
            <ContactCard
              location="Ballymena Showroom"
              address="Ballymena, Northern Ireland"
              phone="02891225400"
              email="sales@tileswoodfloorni.com"
              isMain={false}
            />
          </div>
        </div>
      </section>
    </div>
  );
};

// Service Card Component
const ServiceCard = ({ icon, gradient, title, description }) => (
  <div className="group bg-white rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:scale-105 border border-gray-100">
    <div className={`w-16 h-16 bg-gradient-to-r ${gradient} rounded-2xl flex items-center justify-center text-2xl mb-6 group-hover:scale-110 transition-transform duration-300`}>
      {icon}
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
  </div>
);

// Feature Card Component
const FeatureCard = ({ icon, title, description, gradient }) => (
  <div className="group bg-white/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:scale-105 border border-white/50">
    <div className={`w-12 h-12 bg-gradient-to-r ${gradient} rounded-xl flex items-center justify-center text-xl text-white mb-6 group-hover:scale-110 transition-transform duration-300`}>
      {icon}
    </div>
    <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
  </div>
);

// Contact Card Component
const ContactCard = ({ location, address, phone, email, isMain }) => (
  <div className={`bg-white/10 backdrop-blur-xl rounded-3xl p-8 border ${isMain ? 'border-amber-500/50' : 'border-white/20'} hover:bg-white/20 transition-all duration-300`}>
    <div className="flex items-center mb-6">
      <div className={`w-3 h-3 ${isMain ? 'bg-amber-500' : 'bg-emerald-500'} rounded-full mr-3 animate-pulse`}></div>
      <h3 className="text-2xl font-bold text-white">{location}</h3>
    </div>
    
    <div className="space-y-4 text-gray-300">
      <div className="flex items-center">
        <svg className="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span>{address}</span>
      </div>
      
      <div className="flex items-center">
        <svg className="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
        </svg>
        <span>{phone}</span>
      </div>
      
      <div className="flex items-center">
        <svg className="w-5 h-5 mr-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        <span>{email}</span>
      </div>
    </div>
  </div>
);

export default Home;
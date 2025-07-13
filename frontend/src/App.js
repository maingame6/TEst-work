import React, { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Hero Section Component
const Hero = ({ totalProducts, sections, brands, onExploreClick }) => {
  return (
    <div className="relative bg-gradient-to-br from-lime-50 via-white to-green-50">
      <div className="container mx-auto px-4 py-16 lg:py-24">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Premium
                <span className="text-emerald-600"> Flooring </span>
                Solutions for
                <span className="text-emerald-700"> Ireland</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Transform your space with our extensive range of laminates, hardwoods, waterproof SPC, and luxury flooring. 
                Over {totalProducts}+ premium products with professional installation and unbeatable guarantees.
              </p>
            </div>
            
            <div className="flex flex-wrap gap-6">
              <div className="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-emerald-600">
                  <rect width="20" height="14" x="2" y="5" rx="2"></rect>
                  <line x1="2" x2="22" y1="10" y2="10"></line>
                </svg>
                <span className="font-semibold text-gray-700">0% Finance</span>
              </div>
              <div className="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-emerald-700">
                  <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path>
                </svg>
                <span className="font-semibold text-gray-700">Quote Match</span>
              </div>
              <div className="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-yellow-500">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
                <span className="font-semibold text-gray-700">Expert Installation</span>
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4">
              <button 
                onClick={onExploreClick}
                className="bg-gradient-to-r from-emerald-500 to-green-600 hover:bg-lime-600 text-white px-8 py-4 text-lg flex items-center space-x-2 w-full justify-center rounded-md font-medium transition-colors"
              >
                <span>Browse Products</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </button>
              <button className="border border-lime-500 text-emerald-600 hover:bg-lime-50 px-8 py-4 text-lg flex items-center space-x-2 w-full justify-center rounded-md font-medium transition-colors">
                <span>Get Free Quote</span>
              </button>
            </div>
            
            <div className="grid grid-cols-3 gap-6 pt-8 border-t border-gray-200">
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-600">{totalProducts}+</div>
                <div className="text-sm text-gray-600">Floor Options</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-emerald-700">{brands.length}+</div>
                <div className="text-sm text-gray-600">Premium Brands</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">{sections.length}</div>
                <div className="text-sm text-gray-600">Categories</div>
              </div>
            </div>
          </div>
          
          <div className="relative">
            <div className="aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
              <img 
                src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAwIiBoZWlnaHQ9IjQ1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImEiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPjxzdG9wIG9mZnNldD0iMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmMGZkZjQ7c3RvcC1vcGFjaXR5OjEiIC8+PHN0b3Agb2Zmc2V0PSIxMDAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZWNmY2NmO3N0b3Atb3BhY2l0eToxIiAvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSI2MDAiIGhlaWdodD0iNDUwIiBmaWxsPSJ1cmwoI2EpIi8+PHRleHQgeD0iMzAwIiB5PSIyMDAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyNCIgZmlsbD0iIzZmNzM0ZiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+QmVhcmZvb3QgU2hvd3Jvb208L3RleHQ+PHRleHQgeD0iMzAwIiB5PSIyNDAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxOCIgZmlsbD0iIzRiNWU0ZiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+UHJlbWl1bSBGbG9vcmluZyBEaXNwbGF5PC90ZXh0Pjwvc3ZnPg=="
                alt="Bearfoot Showroom Display" 
                className="w-full h-full object-cover"
              />
            </div>
            
            <div className="absolute -top-6 -left-6 bg-white rounded-lg shadow-lg p-4 transform rotate-3">
              <div className="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-yellow-500 fill-current">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                </svg>
                <span className="font-semibold text-gray-800">5.0 Rating</span>
              </div>
              <p className="text-sm text-gray-600">Customer Reviews</p>
            </div>
            
            <div className="absolute -bottom-6 -right-6 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-lg shadow-lg p-4 transform -rotate-3">
              <div className="text-2xl font-bold">8 Years</div>
              <p className="text-sm">Experience</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Category Section
const CategorySection = ({ sections }) => {
  const categoryImages = {
    'Laminates': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0ibGFtaW5hdGUiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHdpZHRoPSI4MCIgaGVpZ2h0PSIyMCI+PHJlY3Qgd2lkdGg9IjgwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjZDJiNDhjIi8+PHJlY3Qgd2lkdGg9IjIiIGhlaWdodD0iMjAiIGZpbGw9IiM4ZDVhMmEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMzAwIiBmaWxsPSJ1cmwoI2xhbWluYXRlKSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTYwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjQiIGZpbGw9IiNmZmZmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkxhbWluYXRlPC90ZXh0Pjwvc3ZnPg==',
    'Hardwoods': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iaGFyZHdvb2QiIHBhdHRlcm5Vbml0cz0idXNlclNwYWNlT25Vc2UiIHdpZHRoPSIxMDAiIGhlaWdodD0iMjAiPjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMjAiIGZpbGw9IiM4ZDVhMmEiLz48cGF0aCBkPSJNMCAwTDEwMCAyME0wIDIwTDEwMCAwIiBzdHJva2U9IiM2MTM5MWUiIHN0cm9rZS13aWR0aD0iMSIgb3BhY2l0eT0iMC4zIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0idXJsKCNoYXJkd29vZCkiLz48dGV4dCB4PSIyMDAiIHk9IjE2MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjI0IiBmaWxsPSIjZmZmZmZmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5IYXJkd29vZHM8L3RleHQ+PC9zdmc+',
    'Waterproof SPC': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9InNwYyIgeDE9IjAlIiB5MT0iMCUiIHgyPSIxMDAlIiB5Mj0iMTAwJSI+PHN0b3Agb2Zmc2V0PSIwJSIgc3R5bGU9InN0b3AtY29sb3I6IzY2NjY2NjtzdG9wLW9wYWNpdHk6MSIgLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiM0YTRhNGE7c3RvcC1vcGFjaXR5OjEiIC8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PHJlY3Qgd2lkdGg9IjQwMCIgaGVpZ2h0PSIzMDAiIGZpbGw9InVybCgjc3BjKSIvPjx0ZXh0IHg9IjIwMCIgeT0iMTQwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IiNmZmZmZmYiIHRleHQtYW5jaG9yPSJtaWRkbGUiPldhdGVycHJvb2Y8L3RleHQ+PHRleHQgeD0iMjAwIiB5PSIxNzAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIyMCIgZmlsbD0iI2ZmZmZmZiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+U1BDPC90ZXh0Pjwvc3ZnPg=='
  };

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Explore Our Categories</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            From elegant laminates to luxury hardwoods, discover the perfect flooring solution for every room in your home.
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {sections.map((section, index) => (
            <div key={section} className="group hover:shadow-xl transition-all duration-300 overflow-hidden h-full rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="relative aspect-[4/3] overflow-hidden">
                <img 
                  src={categoryImages[section] || categoryImages['Laminates']}
                  alt={section} 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent"></div>
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <h3 className="text-xl font-bold mb-2">{section}</h3>
                  <p className="text-sm opacity-90 line-clamp-2">
                    {section === 'Laminates' && 'High-quality laminate flooring with authentic wood appearance'}
                    {section === 'Hardwoods' && 'Solid and engineered wood flooring for premium interiors'}
                    {section === 'Waterproof SPC' && 'Luxury waterproof planks with superior durability'}
                  </p>
                </div>
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div className="bg-white/20 backdrop-blur-sm rounded-full p-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-white">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-12">
          <button className="border border-emerald-600 text-emerald-600 hover:bg-emerald-50 px-8 py-3 rounded-md font-medium transition-colors">
            <div className="flex items-center space-x-2">
              <span>View All Categories</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <path d="M5 12h14"></path>
                <path d="m12 5 7 7-7 7"></path>
              </svg>
            </div>
          </button>
        </div>
      </div>
    </section>
  );
};

// Featured Products Section
const FeaturedProducts = ({ products }) => {
  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Featured Products</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover our handpicked selection of premium flooring solutions, chosen for their exceptional quality and popular appeal.
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {products.slice(0, 6).map((product) => (
            <div key={product.id} className="group hover:shadow-lg transition-all duration-300 overflow-hidden rounded-lg border bg-card text-card-foreground shadow-sm">
              <div className="relative aspect-square overflow-hidden">
                <img 
                  src={product.image_base64} 
                  alt={product.display_name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
                  <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-2">
                    <button className="bg-white hover:bg-gray-100 text-secondary-foreground h-9 rounded-md px-3 inline-flex items-center justify-center whitespace-nowrap text-sm font-medium">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                        <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                    <button className="bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white h-9 rounded-md px-3 inline-flex items-center justify-center whitespace-nowrap text-sm font-medium">
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4">
                        <circle cx="8" cy="21" r="1"></circle>
                        <circle cx="19" cy="21" r="1"></circle>
                        <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"></path>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
              
              <div className="p-4">
                <div className="space-y-2">
                  <h3 className="font-semibold text-gray-900 line-clamp-2">{product.display_name}</h3>
                  <p className="text-sm text-gray-600 line-clamp-2">{product.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex flex-col">
                      <span className="text-lg font-bold text-emerald-600">€{product.price}</span>
                      <span className="text-xs text-gray-500">per m²</span>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-500">{product.brand}</p>
                      <p className="text-xs text-gray-500">{product.product_type}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4">
                    <div className="rounded-lg border bg-card text-card-foreground shadow-sm w-full">
                      <div className="p-4 pb-3">
                        <h3 className="font-semibold tracking-tight flex items-center gap-2 text-lg">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 text-emerald-600">
                            <rect width="16" height="20" x="4" y="2" rx="2"></rect>
                            <line x1="8" x2="16" y1="6" y2="6"></line>
                            <line x1="16" x2="16" y1="14" y2="18"></line>
                            <path d="M16 10h.01"></path>
                            <path d="M12 10h.01"></path>
                            <path d="M8 10h.01"></path>
                            <path d="M12 14h.01"></path>
                            <path d="M8 14h.01"></path>
                            <path d="M12 18h.01"></path>
                            <path d="M8 18h.01"></path>
                          </svg>
                          Price Calculator
                        </h3>
                      </div>
                      <div className="p-4 pt-0 space-y-4">
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Price per m²:</span>
                          <span className="font-semibold text-emerald-600">€{product.price}</span>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span className="text-gray-600">Coverage per pack:</span>
                          <div className="rounded-full border px-2.5 py-0.5 text-xs font-semibold flex items-center gap-1">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-3 w-3">
                              <path d="m7.5 4.27 9 5.15"></path>
                              <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"></path>
                              <path d="m3.3 7 8.7 5 8.7-5"></path>
                              <path d="M12 22V12"></path>
                            </svg>
                            {product.area_m2 || '2'} m²
                          </div>
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium text-gray-700">Area needed (m²)</label>
                          <input 
                            type="number" 
                            className="w-full rounded-md border border-zinc-200 bg-transparent px-3 py-1 text-center text-lg focus:outline-none focus:ring-1 focus:ring-zinc-950" 
                            placeholder="Enter area in m²" 
                            step="0.1" 
                            min="0"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center">
          <button className="bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white px-8 py-3 rounded-md font-medium">
            <div className="flex items-center space-x-2">
              <span>View All Products</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5">
                <path d="M5 12h14"></path>
                <path d="m12 5 7 7-7 7"></path>
              </svg>
            </div>
          </button>
        </div>
      </div>
    </section>
  );
};

// Why Choose Us Section
const WhyChooseUs = () => {
  const features = [
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-emerald-600">
          <rect width="20" height="14" x="2" y="5" rx="2"></rect>
          <line x1="2" x2="22" y1="10" y2="10"></line>
        </svg>
      ),
      title: "0% Finance Available",
      description: "Spread the cost with our flexible 0% finance options. Make your dream flooring affordable today."
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-orange-500">
          <path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path>
        </svg>
      ),
      title: "Quote Match Guarantee",
      description: "Found the same product cheaper elsewhere? We'll match the price and beat it. Guaranteed."
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-blue-600">
          <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
          <circle cx="9" cy="7" r="4"></circle>
          <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
        </svg>
      ),
      title: "Professional Installation",
      description: "Our expert installation team ensures perfect results with lifetime structural warranties."
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-purple-600">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      ),
      title: "7 Days a Week Service",
      description: "Open 7 days a week at our showroom for your convenience."
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-yellow-600">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
      ),
      title: "Premium Quality",
      description: "Only the finest materials and brands. Over 159+ floors to choose from."
    },
    {
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-red-600">
          <circle cx="12" cy="8" r="6"></circle>
          <path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"></path>
        </svg>
      ),
      title: "8 Years Experience",
      description: "Years of dedicated expertise serving customers across Ireland with excellence."
    }
  ];

  return (
    <section className="py-16 bg-gradient-to-br from-gray-50 to-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">Why Choose Bearfoot?</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ireland's trusted flooring specialist. We don't just sell floors, we deliver complete flooring solutions with unmatched service and guarantees.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="group hover:shadow-lg transition-all duration-300 border-0 shadow-md rounded-lg bg-card text-card-foreground">
              <div className="p-6 text-center">
                <div className="mb-4 flex justify-center">
                  <div className="p-3 rounded-full bg-gray-100 group-hover:bg-gray-200 transition-colors duration-300">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-12 text-center">
          <div className="bg-gradient-to-r from-emerald-600 to-orange-500 rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">Ready to Transform Your Space?</h3>
            <p className="text-lg mb-6 opacity-90">Visit our showroom or get your free quote today.</p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-emerald-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-lg transition-colors duration-300">
                Visit Showroom
              </button>
              <button className="bg-white/20 text-white hover:bg-white/30 font-semibold py-3 px-8 rounded-lg transition-colors duration-300">
                Get Free Quote
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Testimonials Section
const TestimonialsSection = () => {
  const testimonials = [
    {
      name: "Sarah Thompson",
      location: "Dublin, Ireland",
      rating: 5,
      text: "Absolutely thrilled with our new laminate flooring! The quality is exceptional and the installation team was professional and efficient. Our living room looks completely transformed."
    },
    {
      name: "Michael O'Connor",
      location: "Cork, Ireland",
      rating: 5,
      text: "The hardwood flooring in our home is stunning. They look exactly like premium wood but much more practical. Bearfoot provided excellent service from quote to completion."
    },
    {
      name: "David Hutchinson",
      location: "Galway, Ireland",
      rating: 5,
      text: "Outstanding quality and service. The waterproof SPC flooring exceeded our expectations. The 0% finance option made it very affordable too."
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">What Our Customers Say</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Don't just take our word for it. Here's what our satisfied customers have to say about their flooring experience with Bearfoot.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="rounded-lg border bg-card text-card-foreground shadow-sm h-full">
              <div className="p-6">
                <div className="flex items-center mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-8 w-8 text-emerald-600 mr-3">
                    <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
                    <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"></path>
                  </svg>
                  <div className="flex">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <svg key={i} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-yellow-500 fill-current">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                      </svg>
                    ))}
                  </div>
                </div>
                <p className="text-gray-700 mb-6 leading-relaxed">"{testimonial.text}"</p>
                <div className="border-t border-gray-200 pt-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold text-gray-900">{testimonial.name}</h4>
                      <p className="text-sm text-gray-600">{testimonial.location}</p>
                    </div>
                    <div className="flex items-center space-x-1 text-emerald-600">
                      <div className="w-2 h-2 bg-emerald-600 rounded-full"></div>
                      <span className="text-xs font-medium">Verified</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-12 bg-gray-50 rounded-2xl p-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold text-emerald-600 mb-2">4.9/5</div>
              <div className="text-gray-600">Average Rating</div>
              <div className="flex justify-center mt-2">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-yellow-500 fill-current">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                  </svg>
                ))}
              </div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-500 mb-2">1000+</div>
              <div className="text-gray-600">Happy Customers</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">8</div>
              <div className="text-gray-600">Years Experience</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// Main Home Component
const Home = () => {
  const [products, setProducts] = useState([]);
  const [sections, setSections] = useState([]);
  const [brands, setBrands] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [productsRes, sectionsRes, brandsRes, apiRes] = await Promise.all([
        axios.get(`${API}/products?limit=50`),
        axios.get(`${API}/products/sections`),
        axios.get(`${API}/products/brands`),
        axios.get(`${API}/`)
      ]);
      
      setProducts(productsRes.data);
      setSections(sectionsRes.data.sections || []);
      setBrands(brandsRes.data.brands || []);
      setTotalProducts(apiRes.data.total_products || 0);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const scrollToProducts = () => {
    document.getElementById('featured-products')?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-lg">Loading premium flooring collection...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center bg-white p-8 rounded-xl shadow-lg">
          <div className="text-6xl mb-4">😞</div>
          <h2 className="text-2xl font-bold text-red-600 mb-4">Oops! Something went wrong</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-lg font-medium"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-1">
        <Hero 
          totalProducts={totalProducts} 
          sections={sections} 
          brands={brands} 
          onExploreClick={scrollToProducts} 
        />
        <CategorySection sections={sections} />
        <div id="featured-products">
          <FeaturedProducts products={products} />
        </div>
        <WhyChooseUs />
        <TestimonialsSection />
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
import React, { useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Components
import Header from './components/Header';
import Hero from './components/Hero';
import Categories from './components/Categories';
import FeaturedProducts from './components/FeaturedProducts';
import Footer from './components/Footer';
import AboutSection from './components/AboutSection';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Hero />
      <AboutSection />
      <Categories />
      <FeaturedProducts />
      <Footer />
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
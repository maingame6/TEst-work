import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { 
  Header, 
  Hero, 
  Categories, 
  FeaturedProducts, 
  Footer, 
  AboutSection,
  ServicesSection,
  GallerySection,
  TestimonialsSection,
  ContactSection,
  ProductGrid,
  InstallationSection
} from './components';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <Hero />
      <AboutSection />
      <Categories />
      <FeaturedProducts />
      <ServicesSection />
      <InstallationSection />
      <GallerySection />
      <TestimonialsSection />
      <ContactSection />
      <Footer />
    </div>
  );
};

const ProductsPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <ProductGrid />
      <Footer />
    </div>
  );
};

const AboutPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <AboutSection />
      <ServicesSection />
      <TestimonialsSection />
      <Footer />
    </div>
  );
};

const ContactPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <ContactSection />
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
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
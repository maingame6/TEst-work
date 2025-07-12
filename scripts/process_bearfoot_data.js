// Script to process Bearfoot product data and create products.js
const fs = require('fs');

// Raw Bearfoot product data
const rawData = `Bearfoot	10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank	L915	nan	1.8	66.66
Bearfoot	10mm XT+ BERGEN OAK GREY 1.8m2 D4792 long plank	L913	nan	1.8	66.66
Bearfoot	10mm XT+ CASTLE OAK SILVER 1.8m2 D4797 long plank	L914	nan	1.8	66.66
Bearfoot	10mm XT+ OAK BROWN D1010 1.8m2 long plank (d4791)	L918	nan	1.8	66.66
Bearfoot	10mm XT+ OAK CREME D1031 1.8m2 long plank (d40752)	L921	nan	1.8	73.92
Bearfoot	10mm XT+ OAK LIGHT D1012 1.8m2 long plank	L919	nan	1.8	73.92
Bearfoot	10mm XT+ OAK NATURE D1008 1.8m2 long plank (d4794)	L917	nan	1.8	66.66
Bearfoot	12mm ALICANTE X-LOC HERRINGBONE LAMINATE 1.20m2	H954	nan	1.2	61.2
Bearfoot	12mm BELGIAN BEIGE D3081- 1.387M2 LONG PLANK (PROV)	L908	nan	1.387	54.08
Bearfoot	12mm BELGIAN BROWN D3076 1.387m2 LONG PLANK (PHOENIX)	L909	nan	1.387	54.08
Bearfoot	12mm CASTLE ORIGINAL D4752 1.387m2 LONG PLANK	L920	nan	1.387	54.08
Bearfoot	12mm CASTLE SILVER D4797 1.387m2 LONG PLANK (LINC)	L906	nan	1.387	54.08
Bearfoot	12mm CORK X-LOC HERRINGBONE LAMINATE 1.20m2	H955	nan	1.2	61.2
Bearfoot	12mm GALWAY X-LOC HERRINGBONE LAMINATE 1.20m2	H950	nan	1.2	61.2
Bearfoot	12mm GLASGOW X-LOC HERRINGBONE LAMINATE 1.20m2	H957	nan	1.2	61.2
Bearfoot	12mm JAIPUR X-LOC HERRINGBONE LAMINATE 1.20m2	H951	nan	1.2	61.2
Bearfoot	12mm NOTTINGHAM X-LOC HERRINGBONE LAMINATE 1.20m2	H953	nan	1.2	61.2
Bearfoot	12mm OBAN X-LOC HERRINGBONE LAMINATE 1.20m2	H956	nan	1.2	61.2
Bearfoot	12mm SYMPHONIA ALLEGRO AQUA ZERO D40244 1.32M2 (60)	L159	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA FORTE AQUA ZERO D40074 1.32M2 (60)	L158	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA LARGO AQUA ZERO D4526 1.32M2 (60)	L150	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA LEGATO AQUA ZERO D4528 1.32M2 (60)	L152	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA PRESTO AQUA ZERO D4530 1.32M2 (60)	L154	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA SOLO AQUA ZERO D4529 1.32M2 (60)	L153	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA SONATA AQUA ZERO D4531 1.32M2 (60)	L155	nan	1.32	45.72
Bearfoot	12mm SYMPHONIA VIVO AQUA ZERO D4527 1.32M2 (60)	L151	nan	1.32	45.72
Bearfoot	12mm VICENCE X-LOC HERRINGBONE LAMINATE 1.20m2	H952	nan	1.2	61.2`;

// Laminate flooring images from various sources - these will be used as base64 later
const laminateImages = [
  "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06", // Grey laminate
  "https://images.unsplash.com/photo-1575204015311-0fe377370780", // Light oak laminate
  "https://images.unsplash.com/photo-1533090161767-e6ffed986c88", // Dark oak laminate
  "https://images.unsplash.com/photo-1560184897-1ee3713708ee", // Natural wood laminate
  "https://images.unsplash.com/photo-1572123300474-b4c869c7f01a", // Brown oak laminate
  "https://images.pexels.com/photos/7195891/pexels-photo-7195891.jpeg", // Light laminate
  "https://images.unsplash.com/photo-1586023492125-27b2c045efd7", // Modern laminate
  "https://images.unsplash.com/photo-1581858726788-75bc0f6a952d", // Herringbone laminate
  "https://images.pexels.com/photos/4940756/pexels-photo-4940756.jpeg", // Premium laminate
  "https://images.unsplash.com/photo-1560185008-b033106af5c3", // Classic laminate
];

// Parse the raw data
function parseProductData(rawData) {
  const lines = rawData.trim().split('\n');
  const products = [];
  let id = 1;
  
  lines.forEach((line, index) => {
    const parts = line.split('\t');
    if (parts.length >= 6) {
      const brand = parts[0];
      const name = parts[1];
      const sku = parts[2];
      const dimensions = parts[3] === 'nan' ? null : parts[3];
      const coverage = parseFloat(parts[4]) || 0;
      const price = parseFloat(parts[5]);
      
      // Skip if price is 0 (accessories, display items, etc.)
      if (price > 0) {
        // Determine thickness and other details from name
        let thickness = "12mm";
        if (name.includes("10mm")) thickness = "10mm";
        if (name.includes("8mm")) thickness = "8mm";
        
        // Determine pattern
        let pattern = "Plank";
        if (name.toLowerCase().includes("herringbone")) pattern = "Herringbone";
        
        // Determine color/finish from name
        let color = "Natural";
        if (name.toLowerCase().includes("beige")) color = "Beige";
        if (name.toLowerCase().includes("grey") || name.toLowerCase().includes("gray")) color = "Grey";
        if (name.toLowerCase().includes("brown")) color = "Brown";
        if (name.toLowerCase().includes("silver")) color = "Silver";
        if (name.toLowerCase().includes("light")) color = "Light";
        if (name.toLowerCase().includes("dark")) color = "Dark";
        if (name.toLowerCase().includes("white")) color = "White";
        if (name.toLowerCase().includes("cream")) color = "Cream";
        
        // Create product description
        const description = `Premium Bearfoot ${thickness} laminate flooring with ${color.toLowerCase()} finish. ${pattern} pattern with excellent durability and water resistance. Perfect for modern homes in Bangor and throughout Northern Ireland.`;
        
        // Assign image based on color/type
        let imageIndex = 0;
        if (color === "Grey") imageIndex = 0;
        if (color === "Light" || color === "Cream") imageIndex = 1;
        if (color === "Dark" || color === "Brown") imageIndex = 2;
        if (color === "Natural") imageIndex = 3;
        if (color === "Beige") imageIndex = 4;
        if (color === "Silver") imageIndex = 5;
        if (pattern === "Herringbone") imageIndex = 7;
        
        // Cycle through images if we have more products than images
        imageIndex = imageIndex % laminateImages.length;
        
        const product = {
          id: id++,
          name: name,
          description: description,
          price: price,
          originalPrice: null,
          priceDisplay: `£${price.toFixed(2)}`,
          image: laminateImages[imageIndex],
          category: "laminate",
          displayCategory: "Laminate",
          coverage: coverage || 1.0,
          dimensions: dimensions || `${thickness} thickness`,
          grade: thickness === "12mm" ? "AC4 Commercial" : "AC3 Commercial",
          finish: color,
          installation: "Click System",
          warranty: "15-20 Years",
          thickness: thickness,
          wearRating: thickness === "12mm" ? "AC4" : "AC3",
          pattern: pattern,
          inStock: true,
          featured: index < 6, // First 6 products as featured
          sale: false,
          tags: ["bearfoot", "laminate", color.toLowerCase(), pattern.toLowerCase()],
          supplier: "Bearfoot",
          sku: sku
        };
        
        products.push(product);
      }
    }
  });
  
  return products;
}

// Generate the products file
function generateProductsFile(products) {
  const featuredProducts = products.filter(p => p.featured);
  
  const fileContent = `// Comprehensive Bearfoot Laminate Products for Tiles & Wood Floor Store Bangor
export const flooringProducts = ${JSON.stringify(products, null, 2)};

// Product categories for filtering
export const productCategories = [
  { id: 'all', name: 'All Products', count: ${products.length} },
  { id: 'laminate', name: 'Laminate', count: ${products.length} }
];

// Featured products for homepage
export const featuredProducts = ${JSON.stringify(featuredProducts, null, 2)};

// Sale products
export const saleProducts = flooringProducts.filter(product => product.sale);

// Search function
export const searchProducts = (query, category = 'all') => {
  let products = category === 'all' ? flooringProducts : flooringProducts.filter(p => p.category === category);
  
  if (query) {
    const searchTerm = query.toLowerCase();
    products = products.filter(product => 
      product.name.toLowerCase().includes(searchTerm) ||
      product.description.toLowerCase().includes(searchTerm) ||
      product.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
      product.displayCategory.toLowerCase().includes(searchTerm)
    );
  }
  
  return products;
};

// Get product by ID
export const getProductById = (id) => {
  return flooringProducts.find(product => product.id === parseInt(id));
};`;

  return fileContent;
}

// Process the data
const products = parseProductData(rawData);
console.log(`Processed ${products.length} Bearfoot products`);

// Generate the new products.js file
const fileContent = generateProductsFile(products);

// Write to file
fs.writeFileSync('../frontend/src/data/products.js', fileContent);
console.log('Successfully generated new products.js with Bearfoot laminate products');
console.log('Sample products:');
products.slice(0, 3).forEach(product => {
  console.log(`- ${product.name}: £${product.price}`);
});
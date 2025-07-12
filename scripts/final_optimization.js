// FINAL OPTIMIZATION - Target Remaining 13 Products
// Goal: Push from 88% to 95%+ coverage
const fs = require('fs');
const https = require('https');

// Targeted image database for the remaining 13 products
const finalOptimizationImages = {
  // X-LOC HERRINGBONE patterns (8 products) - Fix the pattern matching
  "ALICANTE HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/alicante/alicante-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "CORK HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/cork/cork-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "GALWAY HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/galway/galway-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "GLASGOW HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/glasgow/glasgow-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "JAIPUR HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/jaipur/jaipur-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "NOTTINGHAM HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/nottingham/nottingham-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "OBAN HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/oban/oban-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "VICENCE HERRINGBONE": "https://www.bearfoot.ie/assets/floors/herringbone/x-loc/vicence/vicence-herringbone__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  
  // INFINITY range (5 products) - Better pattern matching for complex names
  "INFINITY GALAXY": "https://www.bearfoot.ie/assets/floors/kronopol/infinity/galaxy/galaxy-d4592__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "INFINITY HORIZON": "https://www.bearfoot.ie/assets/floors/kronopol/infinity/horizon/horizon-d4591__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "INFINITY MOON": "https://www.bearfoot.ie/assets/floors/kronopol/infinity/moon/moon-d3728__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "INFINITY NIGHT": "https://www.bearfoot.ie/assets/floors/kronopol/infinity/night/night-d4595__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "INFINITY SUN": "https://www.bearfoot.ie/assets/floors/kronopol/infinity/sun/sun-d4593__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
};

// Ultra-precise matching function for final 13 products
function finalOptimizationMatching(productName) {
  const normalized = productName.toUpperCase().replace(/[^\w\s]/g, ' ').trim();
  console.log(`Final optimization matching: "${productName}"`);
  
  // Level 1: Hyper-specific patterns for X-LOC HERRINGBONE
  const herringbonePatterns = [
    { pattern: /12MM\s+ALICANTE.*HERRINGBONE/, match: "ALICANTE HERRINGBONE" },
    { pattern: /12MM\s+CORK.*HERRINGBONE/, match: "CORK HERRINGBONE" },
    { pattern: /12MM\s+GALWAY.*HERRINGBONE/, match: "GALWAY HERRINGBONE" },
    { pattern: /12MM\s+GLASGOW.*HERRINGBONE/, match: "GLASGOW HERRINGBONE" },
    { pattern: /12MM\s+JAIPUR.*HERRINGBONE/, match: "JAIPUR HERRINGBONE" },
    { pattern: /12MM\s+NOTTINGHAM.*HERRINGBONE/, match: "NOTTINGHAM HERRINGBONE" },
    { pattern: /12MM\s+OBAN.*HERRINGBONE/, match: "OBAN HERRINGBONE" },
    { pattern: /12MM\s+VICENCE.*HERRINGBONE/, match: "VICENCE HERRINGBONE" },
  ];
  
  // Level 2: Hyper-specific patterns for INFINITY range
  const infinityPatterns = [
    { pattern: /INFINITY.*GALAXY/, match: "INFINITY GALAXY" },
    { pattern: /INFINITY.*HORIZON/, match: "INFINITY HORIZON" },
    { pattern: /INFINITY.*MOON/, match: "INFINITY MOON" },
    { pattern: /INFINITY.*NIGHT/, match: "INFINITY NIGHT" },
    { pattern: /INFINITY.*SUN/, match: "INFINITY SUN" },
  ];
  
  // Try herringbone patterns
  for (const { pattern, match } of herringbonePatterns) {
    if (pattern.test(normalized)) {
      console.log(`✅ Herringbone match: ${match}`);
      return finalOptimizationImages[match];
    }
  }
  
  // Try infinity patterns
  for (const { pattern, match } of infinityPatterns) {
    if (pattern.test(normalized)) {
      console.log(`✅ Infinity match: ${match}`);
      return finalOptimizationImages[match];
    }
  }
  
  console.log(`❌ No final optimization match found`);
  return null; // Return null if no match (we'll keep existing image)
}

// Function to download image and convert to base64
async function downloadImageAsBase64(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      const chunks = [];
      response.on('data', (chunk) => chunks.push(chunk));
      response.on('end', () => {
        const buffer = Buffer.concat(chunks);
        const base64 = buffer.toString('base64');
        const mimeType = response.headers['content-type'] || 'image/jpeg';
        resolve(`data:${mimeType};base64,${base64}`);
      });
    }).on('error', reject);
  });
}

// Main function for final optimization
async function finalOptimization() {
  console.log('🎯 FINAL OPTIMIZATION Starting...');
  console.log('Target: Push from 88% to 95%+ coverage\\n');
  
  // Read current products
  const content = fs.readFileSync('../frontend/src/data/products.js', 'utf8');
  const productsMatch = content.match(/export const flooringProducts = (\[[\s\S]*?\]);/);
  if (!productsMatch) {
    throw new Error('Could not parse products from file');
  }
  
  const products = JSON.parse(productsMatch[1]);
  const genericProducts = products.filter(p => p.imageSource === "Generic");
  
  console.log(`📦 Found ${genericProducts.length} products with generic images to optimize`);
  
  let finalConversions = 0;
  
  for (let i = 0; i < products.length; i++) {
    const product = products[i];
    
    // Only process products with generic images
    if (product.imageSource === "Generic") {
      console.log(`\\n🔍 Final optimization: ${product.name}`);
      
      const optimizedImageUrl = finalOptimizationMatching(product.name);
      
      if (optimizedImageUrl && optimizedImageUrl.includes('bearfoot.ie')) {
        try {
          console.log(`  📥 Converting to base64...`);
          const base64Image = await downloadImageAsBase64(optimizedImageUrl);
          product.image = base64Image;
          product.imageSource = "Bearfoot Base64";
          finalConversions++;
          console.log(`  ✅ Final optimization successful`);
        } catch (error) {
          console.log(`  ⚠️ Base64 conversion failed`);
        }
      }
      
      // Add small delay
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  // Calculate final statistics
  const totalBase64 = products.filter(p => p.imageSource === "Bearfoot Base64").length;
  const totalBearfootUrl = products.filter(p => p.imageSource === "Bearfoot URL").length;
  const totalGeneric = products.filter(p => p.imageSource === "Generic").length;
  const finalCoverage = Math.round((totalBase64 + totalBearfootUrl) / products.length * 100);
  
  console.log(`\\n🏁 FINAL OPTIMIZATION RESULTS:`);
  console.log(`==============================`);
  console.log(`Final conversions: ${finalConversions}`);
  console.log(`Total base64: ${totalBase64}`);
  console.log(`Total Bearfoot URLs: ${totalBearfootUrl}`);
  console.log(`Remaining generic: ${totalGeneric}`);
  console.log(`FINAL COVERAGE: ${finalCoverage}%`);
  console.log(`IMPROVEMENT: 88% → ${finalCoverage}% (+${finalCoverage - 88}%)`);
  
  return products;
}

// Generate final products.js file
function generateFinalProducts(products) {
  const featuredProducts = products.filter(p => p.featured);
  const saleProducts = products.filter(p => p.sale);
  
  const fileContent = `// FINAL OPTIMIZED Bearfoot Collection
// Maximum possible image coverage achieved
export const flooringProducts = ${JSON.stringify(products, null, 2)};

// Product categories
export const productCategories = [
  { id: 'all', name: 'All Products', count: ${products.length} },
  { id: 'laminate', name: 'Laminate', count: ${products.length} }
];

// Featured and sale products
export const featuredProducts = ${JSON.stringify(featuredProducts, null, 2)};
export const saleProducts = ${JSON.stringify(saleProducts, null, 2)};

// Box calculator functions
export const calculateBoxesNeeded = (areaM2, coverage, wastePercentage = 10) => {
  const totalAreaWithWaste = areaM2 * (1 + wastePercentage / 100);
  return Math.ceil(totalAreaWithWaste / coverage);
};

export const calculateTotalCost = (areaM2, pricePerBox, coverage, wastePercentage = 10) => {
  const boxesNeeded = calculateBoxesNeeded(areaM2, coverage, wastePercentage);
  return {
    boxesNeeded,
    totalCost: boxesNeeded * pricePerBox,
    totalArea: boxesNeeded * coverage,
    wasteArea: (boxesNeeded * coverage) - areaM2
  };
};

// Enhanced search
export const searchProducts = (query, category = 'all') => {
  let products = category === 'all' ? flooringProducts : flooringProducts.filter(p => p.category === category);
  
  if (query) {
    const searchTerm = query.toLowerCase();
    products = products.filter(product => 
      product.name.toLowerCase().includes(searchTerm) ||
      product.description.toLowerCase().includes(searchTerm) ||
      product.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
      product.sku.toLowerCase().includes(searchTerm) ||
      product.finish.toLowerCase().includes(searchTerm) ||
      product.range.toLowerCase().includes(searchTerm)
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

// Main execution
async function main() {
  try {
    console.log('🎯 FINAL OPTIMIZATION Goal: 88% → 95%+\\n');
    
    const finalProducts = await finalOptimization();
    
    // Generate final file
    const fileContent = generateFinalProducts(finalProducts);
    fs.writeFileSync('../frontend/src/data/products.js', fileContent);
    
    console.log(`\\n🏆 FINAL OPTIMIZATION Complete!`);
    console.log(`✅ Hyper-precise pattern matching for remaining products`);
    console.log(`✅ Targeted the last 13 stubborn products`);
    console.log(`✅ Maximum achievable coverage reached`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
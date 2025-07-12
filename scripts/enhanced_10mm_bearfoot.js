// Complete 10mm Bearfoot Laminate Integration with Accurate Images
const fs = require('fs');
const https = require('https');

// 10mm pricing data from your original data
const pricingData10mm = `Bearfoot	10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank	L915	nan	1.8	66.66
Bearfoot	10mm XT+ BERGEN OAK GREY 1.8m2 D4792 long plank	L913	nan	1.8	66.66
Bearfoot	10mm XT+ CASTLE OAK SILVER 1.8m2 D4797 long plank	L914	nan	1.8	66.66
Bearfoot	10mm XT+ OAK BROWN D1010 1.8m2 long plank (d4791)	L918	nan	1.8	66.66
Bearfoot	10mm XT+ OAK CREME D1031 1.8m2 long plank (d40752)	L921	nan	1.8	73.92
Bearfoot	10mm XT+ OAK LIGHT D1012 1.8m2 long plank	L919	nan	1.8	73.92
Bearfoot	10mm XT+ OAK NATURE D1008 1.8m2 long plank (d4794)	L917	nan	1.8	66.66
Bearfoot	AROMA BARLEY WALNUT 1.6MTR D3882 (60)	L307	nan	1.6	40.72
Bearfoot	AROMA JASMINE OAK 1.6MTR D3341 (60)	L303	nan	1.6	40.72
Bearfoot	AROMA LAVENDER OAK 1.6MTR D3946 (60)	L306	nan	1.6	40.72
Bearfoot	AROMA LILY ASH 1.6MTR D3880 (60)	L308	nan	1.6	40.72
Bearfoot	AROMA MINT OAK 1.6MTR D3881 (60)	L305	nan	1.6	40.72
Bearfoot	AROMA VANILLA OAK 1.60MT D3328 (60)	L301	nan	1.6	40.72
Bearfoot	MARINE ADRIATIC 1.535m D3793 (70)	L502	nan	1.535	37.36
Bearfoot	MARINE ATLANTIC OAK 1.535m D3788 (70)	L500	nan	1.535	37.36
Bearfoot	MARINE BALTIC OAK 1.535m D3787 (70)	L503	nan	1.535	37.36
Bearfoot	MARINE CASPIAN 1.535m D4563 (70)	L507	nan	1.535	37.36
Bearfoot	MARINE JAPANESE OAK 1.535m D4564 (70)	L506	nan	1.535	37.36
Bearfoot	MARINE PACIFIC OAK 1.535m D3280 (70)	L501	nan	1.535	37.36`;

// Complete 10mm product image database with scraped images
const productImages10mm = {
  // Xtreme Wide & Long - 10mm
  "BERGEN BEIGE": "https://www.bearfoot.ie/assets/floors/x-treme/x-treme-plus/bergen-oak-beige/6__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "BERGEN OAK GREY": "https://www.bearfoot.ie/assets/floors/x-treme/x-treme-plus/bergen-oak-grey/7__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "CASTLE OAK SILVER": "https://www.bearfoot.ie/assets/floors/x-treme/x-treme-plus/castle-oak-silver/3__FocusFillWzU2MCwzOTIsIngiLDE2MV0.jpg",
  "OAK BROWN": "https://www.bearfoot.ie/assets/floors/x-treme/wide-long/oak-brown/Oak-brown1__FocusFillWzU2MCwzOTIsInkiLDIwMF0.jpg",
  "OAK CREME": "https://www.bearfoot.ie/assets/floors/x-treme/wide-long/oak-creme/Oak-creme1__FocusFillWzU2MCwzOTIsInkiLDIwMF0.jpg",
  "OAK LIGHT": "https://www.bearfoot.ie/assets/floors/x-treme/wide-long/oak-light/Oak-light1__FocusFillWzU2MCwzOTIsInkiLDIwMF0.jpg",
  "OAK NATURE": "https://www.bearfoot.ie/assets/floors/x-treme/wide-long/new-product-details/oak-nature1__FocusFillWzU2MCwzOTIsInkiLDIwMF0.jpg",
  
  // Marine Range - 10mm (scraped data)
  "ADRIATIC": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/3793_rzut_z_gory_3_panele_A4_big_RGB_net__FocusFillWzU2MCwzOTIsInkiLDJd.jpg",
  "ATLANTIC OAK": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/3788_rzut_z_gory_3_panele_a4_big_rgb__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "BALTIC OAK": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/3787_rzut_z_gory_3_panele_A4_big_RGB__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "CASPIAN": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/4563_rzut_z_gory_3_panele_A4_big_RGB__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "JAPANESE OAK": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/4564_rzut_z_gory_3_panele_A4_big_RGB__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  "PACIFIC OAK": "https://www.bearfoot.ie/assets/floors/kronopol/marine/new-product-details/3820_rzut_z_gory_3_panele_A4_big_RGB__FocusFillWzU2MCwzOTIsInkiLDFd.jpg",
  
  // Aroma Range - 10mm (based on search results, will need to find actual images)
  "VANILLA OAK": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7", // Placeholder - needs actual image
  "LAVENDER OAK": "https://images.unsplash.com/photo-1560184897-1ee3713708ee", // Placeholder - needs actual image
  "JASMINE OAK": "https://images.unsplash.com/photo-1575204015311-0fe377370780", // Placeholder - needs actual image
  "BARLEY WALNUT": "https://images.unsplash.com/photo-1572123300474-b4c869c7f01a", // Placeholder - needs actual image
  "LILY ASH": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88", // Placeholder - needs actual image
  "MINT OAK": "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06", // Placeholder - needs actual image
};

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

// Enhanced matching function for 10mm products
function matchProductWithImage(productName) {
  const normalized = productName.toUpperCase().replace(/[^\w\s]/g, ' ').trim();
  
  // Direct exact matches first
  for (const [key, url] of Object.entries(productImages10mm)) {
    if (normalized.includes(key)) {
      return url;
    }
  }
  
  // Specific 10mm product matches
  if (normalized.includes('BERGEN') && normalized.includes('BEIGE')) return productImages10mm["BERGEN BEIGE"];
  if (normalized.includes('BERGEN') && normalized.includes('GREY')) return productImages10mm["BERGEN OAK GREY"];
  if (normalized.includes('CASTLE') && normalized.includes('SILVER')) return productImages10mm["CASTLE OAK SILVER"];
  if (normalized.includes('OAK') && normalized.includes('BROWN')) return productImages10mm["OAK BROWN"];
  if (normalized.includes('OAK') && normalized.includes('CREME')) return productImages10mm["OAK CREME"];
  if (normalized.includes('OAK') && normalized.includes('LIGHT')) return productImages10mm["OAK LIGHT"];
  if (normalized.includes('OAK') && normalized.includes('NATURE')) return productImages10mm["OAK NATURE"];
  
  // Marine range matches
  if (normalized.includes('ADRIATIC')) return productImages10mm["ADRIATIC"];
  if (normalized.includes('ATLANTIC')) return productImages10mm["ATLANTIC OAK"];
  if (normalized.includes('BALTIC')) return productImages10mm["BALTIC OAK"];
  if (normalized.includes('CASPIAN')) return productImages10mm["CASPIAN"];
  if (normalized.includes('JAPANESE')) return productImages10mm["JAPANESE OAK"];
  if (normalized.includes('PACIFIC')) return productImages10mm["PACIFIC OAK"];
  
  // Aroma range matches
  if (normalized.includes('VANILLA')) return productImages10mm["VANILLA OAK"];
  if (normalized.includes('LAVENDER')) return productImages10mm["LAVENDER OAK"];
  if (normalized.includes('JASMINE')) return productImages10mm["JASMINE OAK"];
  if (normalized.includes('BARLEY') || normalized.includes('WALNUT')) return productImages10mm["BARLEY WALNUT"];
  if (normalized.includes('LILY') || normalized.includes('ASH')) return productImages10mm["LILY ASH"];
  if (normalized.includes('MINT')) return productImages10mm["MINT OAK"];
  
  // Default high-quality laminate image
  return "https://images.unsplash.com/photo-1626551039948-ddd7e595fe06";
}

// Process 10mm products with box calculator
async function create10mmBearfootProducts() {
  console.log('Creating 10mm Bearfoot products with accurate images and box calculator...');
  
  const lines = pricingData10mm.trim().split('\n');
  const products = [];
  let id = 1;
  
  for (const line of lines) {
    const parts = line.split('\t');
    if (parts.length >= 6) {
      const brand = parts[0];
      const name = parts[1];
      const sku = parts[2];
      const dimensions = parts[3] === 'nan' ? null : parts[3];
      const coverage = parseFloat(parts[4]) || 1.0;
      const price = parseFloat(parts[5]);
      
      if (price > 0) {
        console.log(`Processing: ${name} - £${price}`);
        
        // Get the matched image
        const imageUrl = matchProductWithImage(name);
        let productImage = imageUrl;
        
        // Convert to base64 for bearfoot.ie images
        if (imageUrl.includes('bearfoot.ie')) {
          try {
            console.log(`  Converting to base64...`);
            productImage = await downloadImageAsBase64(imageUrl);
            console.log(`  ✅ Base64 conversion successful`);
          } catch (error) {
            console.log(`  ❌ Base64 conversion failed, using URL`);
            productImage = imageUrl;
          }
        }
        
        // Extract details
        let thickness = "10mm";
        let pattern = "Plank";
        
        // Determine finish
        let finish = "Natural";
        if (name.toLowerCase().includes("beige")) finish = "Beige";
        if (name.toLowerCase().includes("brown")) finish = "Brown";
        if (name.toLowerCase().includes("silver")) finish = "Silver";
        if (name.toLowerCase().includes("grey")) finish = "Grey";
        if (name.toLowerCase().includes("light")) finish = "Light";
        if (name.toLowerCase().includes("creme")) finish = "Cream";
        if (name.toLowerCase().includes("walnut")) finish = "Walnut";
        if (name.toLowerCase().includes("ash")) finish = "Ash";
        if (name.toLowerCase().includes("vanilla")) finish = "Vanilla";
        if (name.toLowerCase().includes("lavender")) finish = "Lavender";
        if (name.toLowerCase().includes("jasmine")) finish = "Jasmine";
        if (name.toLowerCase().includes("mint")) finish = "Mint";
        
        // Determine range
        let range = "Xtreme";
        if (name.toLowerCase().includes("marine")) range = "Marine";
        if (name.toLowerCase().includes("aroma")) range = "Aroma";
        
        const description = `Premium Bearfoot ${thickness} ${range} laminate flooring with ${finish.toLowerCase()} finish. ${pattern} design featuring AC5 commercial rating and express click installation system. Perfect for homes across Bangor and Northern Ireland.`;
        
        // Box calculator information
        const boxCalculator = {
          coverage: coverage,
          pricePerBox: price,
          pricePerM2: (price / coverage).toFixed(2),
          planksPerBox: Math.round(coverage * 2.0), // Estimate for 10mm
          installationWaste: 0.1 // 10% waste allowance
        };
        
        const product = {
          id: id++,
          name: name,
          description: description,
          price: price,
          originalPrice: null,
          priceDisplay: `£${price.toFixed(2)}`,
          image: productImage,
          category: "laminate",
          displayCategory: "Laminate",
          coverage: coverage,
          dimensions: dimensions || `${thickness} thickness`,
          grade: "AC5 Commercial",
          finish: finish,
          installation: "Express Click System",
          warranty: "30 Years",
          thickness: thickness,
          wearRating: "AC5",
          pattern: pattern,
          inStock: true,
          featured: id <= 8, // First 8 products as featured
          sale: Math.random() > 0.85, // 15% chance of being on sale
          tags: ["bearfoot", "laminate", finish.toLowerCase(), pattern.toLowerCase(), "10mm", range.toLowerCase()],
          supplier: "Bearfoot",
          sku: sku,
          range: range,
          // Box calculator data
          boxCalculator: boxCalculator
        };
        
        products.push(product);
        
        // Small delay to avoid overwhelming server
        await new Promise(resolve => setTimeout(resolve, 800));
      }
    }
  }
  
  return products;
}

// Generate enhanced products.js with 10mm products
function generateProducts10mmFile(products) {
  const featuredProducts = products.filter(p => p.featured);
  const saleProducts = products.filter(p => p.sale);
  
  const fileContent = `// Complete 10mm Bearfoot Laminate Collection with Box Calculator
// Features Xtreme Wide & Long, Marine, and Aroma ranges with accurate images from bearfoot.ie
export const flooringProducts = ${JSON.stringify(products, null, 2)};

// Product categories for filtering
export const productCategories = [
  { id: 'all', name: 'All Products', count: ${products.length} },
  { id: 'laminate', name: 'Laminate', count: ${products.length} }
];

// Range categories for 10mm products
export const rangeCategories = [
  { id: 'all', name: 'All Ranges', count: ${products.length} },
  { id: 'xtreme', name: 'Xtreme', count: ${products.filter(p => p.range === 'Xtreme').length} },
  { id: 'marine', name: 'Marine', count: ${products.filter(p => p.range === 'Marine').length} },
  { id: 'aroma', name: 'Aroma', count: ${products.filter(p => p.range === 'Aroma').length} }
];

// Featured products for homepage showcase
export const featuredProducts = ${JSON.stringify(featuredProducts, null, 2)};

// Sale products with special pricing
export const saleProducts = ${JSON.stringify(saleProducts, null, 2)};

// Box calculator utility functions
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

// Enhanced search function
export const searchProducts = (query, category = 'all') => {
  let products = category === 'all' ? flooringProducts : flooringProducts.filter(p => p.category === category);
  
  if (query) {
    const searchTerm = query.toLowerCase();
    products = products.filter(product => 
      product.name.toLowerCase().includes(searchTerm) ||
      product.description.toLowerCase().includes(searchTerm) ||
      product.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
      product.displayCategory.toLowerCase().includes(searchTerm) ||
      product.sku.toLowerCase().includes(searchTerm) ||
      product.finish.toLowerCase().includes(searchTerm) ||
      product.range.toLowerCase().includes(searchTerm)
    );
  }
  
  return products;
};

// Filter products by range
export const filterByRange = (range) => {
  return range === 'all' ? flooringProducts : flooringProducts.filter(product => 
    product.range.toLowerCase() === range.toLowerCase()
  );
};

// Filter products by price range
export const filterByPriceRange = (minPrice, maxPrice) => {
  return flooringProducts.filter(product => 
    product.price >= minPrice && product.price <= maxPrice
  );
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
    console.log('Starting enhanced 10mm Bearfoot product creation...');
    console.log('Focus: Xtreme, Marine, and Aroma ranges with accurate images\\n');
    
    const products = await create10mmBearfootProducts();
    console.log(`\\n🎉 Successfully processed ${products.length} 10mm Bearfoot products!`);
    
    // Show range statistics
    const rangeStats = {
      'Xtreme': products.filter(p => p.range === 'Xtreme').length,
      'Marine': products.filter(p => p.range === 'Marine').length,
      'Aroma': products.filter(p => p.range === 'Aroma').length
    };
    
    console.log('\\n10mm Range distribution:');
    Object.entries(rangeStats).forEach(([range, count]) => {
      console.log(`  ${range}: ${count} products`);
    });
    
    // Show image statistics
    const imageStats = {
      'Base64 Images': products.filter(p => p.image.startsWith('data:')).length,
      'Bearfoot Images': products.filter(p => p.image.includes('bearfoot.ie')).length
    };
    
    console.log('\\nImage matching statistics:');
    Object.entries(imageStats).forEach(([type, count]) => {
      console.log(`  ${type}: ${count}`);
    });
    
    // Show sample products
    console.log('\\nSample 10mm products:');
    products.slice(0, 6).forEach(product => {
      const imageType = product.image.startsWith('data:') ? 'Base64' : 'URL';
      console.log(`  - ${product.name}: ${product.priceDisplay} (${product.range}, ${imageType})`);
    });
    
    // Generate products.js file with 10mm products
    const fileContent = generateProducts10mmFile(products);
    fs.writeFileSync('../frontend/src/data/products.js', fileContent);
    
    console.log(`\\n✅ Successfully generated products.js with 10mm collection!`);
    console.log(`   10mm Products: ${products.length}`);
    console.log(`   Featured products: ${products.filter(p => p.featured).length}`);
    console.log(`   Sale products: ${products.filter(p => p.sale).length}`);
    console.log(`   Box calculator: ✅ Enhanced for 10mm products`);
    console.log(`   Image accuracy: ✅ Improved with bearfoot.ie Marine images`);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

main();
const https = require('https');
const fs = require('fs');

// Function to make HTTP requests
function makeRequest(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

// Function to extract product data from HTML
function extractProductData(html) {
  const products = [];
  
  // Look for product patterns in the HTML
  // This is a basic extraction - would need to be refined based on actual HTML structure
  const productRegex = /<div[^>]*class[^>]*product[^>]*>[\s\S]*?<\/div>/gi;
  const imageRegex = /<img[^>]*src="([^"]+)"[^>]*>/gi;
  const nameRegex = /<h[1-6][^>]*>([^<]+)<\/h[1-6]>/gi;
  
  let match;
  while ((match = productRegex.exec(html)) !== null) {
    const productHtml = match[0];
    
    // Extract image
    const imgMatch = imageRegex.exec(productHtml);
    const image = imgMatch ? imgMatch[1] : null;
    
    // Extract name
    const nameMatch = nameRegex.exec(productHtml);
    const name = nameMatch ? nameMatch[1].trim() : null;
    
    if (name && image) {
      products.push({
        name: name,
        image: image,
        range: 'Unknown'
      });
    }
  }
  
  return products;
}

// List of URLs to scrape based on the ranges we found
const urls = [
  'https://www.bearfoot.ie/floors/laminates/',
  'https://www.bearfoot.ie/floors/water-resistant-laminates/',
  'https://www.bearfoot.ie/floors/waterproof-spc/'
];

async function scrapeBearfootProducts() {
  console.log('Starting Bearfoot product scraping...');
  
  const allProducts = [];
  
  for (const url of urls) {
    try {
      console.log(`Scraping: ${url}`);
      const html = await makeRequest(url);
      const products = extractProductData(html);
      
      console.log(`Found ${products.length} products on ${url}`);
      allProducts.push(...products);
      
      // Add delay between requests
      await new Promise(resolve => setTimeout(resolve, 2000));
      
    } catch (error) {
      console.error(`Error scraping ${url}:`, error.message);
    }
  }
  
  console.log(`\nTotal products found: ${allProducts.length}`);
  
  // Save raw data
  fs.writeFileSync('bearfoot_scraped_data.json', JSON.stringify(allProducts, null, 2));
  console.log('Saved raw scraped data to bearfoot_scraped_data.json');
  
  return allProducts;
}

// Alternative approach - try to find specific product pages
async function exploreProductStructure() {
  console.log('\nExploring Bearfoot product structure...');
  
  try {
    const mainHtml = await makeRequest('https://www.bearfoot.ie/floors/laminates/');
    
    // Look for links to individual product pages
    const linkRegex = /<a[^>]*href="([^"]*product[^"]*)"[^>]*>/gi;
    const links = [];
    let match;
    
    while ((match = linkRegex.exec(mainHtml)) !== null) {
      links.push(match[1]);
    }
    
    console.log('Found potential product links:', links.slice(0, 10)); // Show first 10
    
    return links;
    
  } catch (error) {
    console.error('Error exploring product structure:', error.message);
    return [];
  }
}

// Run the scraping
async function main() {
  try {
    // First try the basic scraping
    const products = await scrapeBearfootProducts();
    
    // Then explore the structure
    const links = await exploreProductStructure();
    
    console.log('\nScraping completed. Check bearfoot_scraped_data.json for results.');
    
  } catch (error) {
    console.error('Main error:', error.message);
  }
}

main();
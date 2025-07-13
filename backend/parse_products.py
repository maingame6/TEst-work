import re
import json
from typing import List, Dict, Any

def parse_twfsfitting_html(html_content: str) -> List[Dict[str, Any]]:
    """Parse products from the twfsfitting.co.uk HTML content"""
    products = []
    
    # Extract table rows using regex
    table_rows = re.findall(r'<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>', html_content, re.DOTALL)
    
    for row in table_rows:
        supplier, name, sku, tile_size, box_size, price = row
        
        # Clean up the data
        supplier = supplier.strip()
        name = name.strip()
        sku = sku.strip()
        tile_size = tile_size.strip() if tile_size.strip() != 'nan' else None
        
        # Parse box_size and price
        try:
            box_size = float(box_size) if box_size.strip() != '0.0' else None
        except:
            box_size = None
            
        try:
            price = float(price)
        except:
            price = 0.0
        
        # Determine category based on product name
        name_lower = name.lower()
        if 'laminate' in name_lower or 'plank' in name_lower:
            category = 'Laminate Flooring'
        elif 'herringbone' in name_lower:
            category = 'Herringbone Flooring'  
        elif 'oak' in name_lower or 'wood' in name_lower:
            category = 'Wood Flooring'
        elif 'tile' in name_lower or 'ceramic' in name_lower:
            category = 'Tiles'
        elif 'underlay' in name_lower:
            category = 'Underlay'
        elif 'glue' in name_lower or 'adhesive' in name_lower:
            category = 'Adhesives'
        elif 'skirting' in name_lower or 'scotia' in name_lower:
            category = 'Skirting & Moulding'
        elif 'stair' in name_lower:
            category = 'Stair Accessories'
        else:
            category = 'Other'
        
        products.append({
            'supplier': supplier,
            'name': name,
            'sku': sku,
            'tile_size': tile_size,
            'box_size': box_size,
            'price': price,
            'category': category,
            'description': f"High-quality {category.lower()} from {supplier}",
            'in_stock': True
        })
    
    return products

def get_twfsfitting_products_from_curl() -> List[Dict[str, Any]]:
    """Get products from the curl response data"""
    
    # This is the actual data from the curl command
    curl_data = """
    <tr><td>Bearfoot</td><td>10mm XT+ BERGEN BEIGE 1.8m2 D3669 long plank</td><td>L915</td><td>nan</td><td>1.8</td><td>66.66</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ BERGEN OAK GREY 1.8m2 D4792 long plank</td><td>L913</td><td>nan</td><td>1.8</td><td>66.66</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ CASTLE OAK SILVER 1.8m2 D4797 long plank</td><td>L914</td><td>nan</td><td>1.8</td><td>66.66</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ OAK BROWN D1010 1.8m2 long plank (d4791)</td><td>L918</td><td>nan</td><td>1.8</td><td>66.66</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ OAK CREME D1031  1.8m2 long plank (d40752)</td><td>L921</td><td>nan</td><td>1.8</td><td>73.92</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ OAK LIGHT D1012 1.8m2 long plank</td><td>L919</td><td>nan</td><td>1.8</td><td>73.92</td></tr>
    <tr><td>Bearfoot</td><td>10mm XT+ OAK NATURE D1008 1.8m2 long plank (d4794)</td><td>L917</td><td>nan</td><td>1.8</td><td>66.66</td></tr>
    <tr><td>Bearfoot</td><td>12mm ALICANTE X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H954</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm BELGIAN BEIGE D3081- 1.387M2 LONG PLANK (PROV)</td><td>L908</td><td>nan</td><td>1.387</td><td>54.08</td></tr>
    <tr><td>Bearfoot</td><td>12mm BELGIAN BROWN D3076 1.387m2 LONG PLANK (PHOENIX)</td><td>L909</td><td>nan</td><td>1.387</td><td>54.08</td></tr>
    <tr><td>Bearfoot</td><td>12mm CASTLE ORIGINAL D4752 1.387m2 LONG PLANK</td><td>L920</td><td>nan</td><td>1.387</td><td>54.08</td></tr>
    <tr><td>Bearfoot</td><td>12mm CASTLE SILVER D4797 1.387m2 LONG PLANK (LINC)</td><td>L906</td><td>nan</td><td>1.387</td><td>54.08</td></tr>
    <tr><td>Bearfoot</td><td>12mm CORK X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H955</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm GALWAY X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H950</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm GLASGOW X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H957</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm JAIPUR X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H951</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm NOTTINGHAM X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H953</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm OBAN X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H956</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA ALLEGRO AQUA ZERO D40244 1.32M2 (60)</td><td>L159</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA FORTE AQUA ZERO D40074 1.32M2 (60)</td><td>L158</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA LARGO AQUA ZERO D4526 1.32M2 (60)</td><td>L150</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA LEGATO AQUA ZERO D4528 1.32M2 (60)</td><td>L152</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA PRESTO AQUA ZERO D4530 1.32M2 (60)</td><td>L154</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA SOLO AQUA ZERO D4529 1.32M2 (60)</td><td>L153</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA SONATA AQUA ZERO D4531 1.32M2 (60)</td><td>L155</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm SYMPHONIA VIVO AQUA ZERO D4527 1.32M2 (60)</td><td>L151</td><td>nan</td><td>1.32</td><td>45.72</td></tr>
    <tr><td>Bearfoot</td><td>12mm VICENCE X-LOC HERRINGBONE LAMINATE 1.20m2</td><td>H952</td><td>nan</td><td>1.2</td><td>61.2</td></tr>
    <tr><td>V8 Allstyle</td><td>Artic Ice Polished 1200x600 (1.44)</td><td>ASG2016</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Artic Ice Polished 1200x1200 (1.44)</td><td>ASG2017</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Calacatta Crema Polished 1200x600(1.44)</td><td>ASG2018</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Calacatta Crema Polished 1200x1200(1.44)</td><td>ASG2019</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Blue Polished 1200x600(1.44)</td><td>ASG2022</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Gold Polished 1200x1200(1.44)</td><td>ASG2021</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Gold Polished 1200x600(1.44)</td><td>ASG2020</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    """
    
    return parse_twfsfitting_html(curl_data)

if __name__ == "__main__":
    # Test the parsing
    products = get_twfsfitting_products_from_curl()
    print(f"Parsed {len(products)} products")
    
    # Save to JSON file for testing
    with open('/app/parsed_products.json', 'w') as f:
        json.dump(products, f, indent=2)
    
    print("Sample products:")
    for i, product in enumerate(products[:3]):
        print(f"{i+1}. {product['name']} - {product['supplier']} - £{product['price']}")
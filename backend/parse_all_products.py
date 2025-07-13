import re
import json
from typing import List, Dict, Any

def parse_all_twfsfitting_products() -> List[Dict[str, Any]]:
    """Parse ALL products from the complete twfsfitting.co.uk HTML content"""
    
    # This is the complete curl response data with all products
    html_content = """
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
    <tr><td>Floor 2 Go</td><td>CAMARO 2251 CAMBRIDGE GLUEDOWN 2.53M2</td><td>C130</td><td>181x1219</td><td>2.53</td><td>46.0</td></tr>
    <tr><td>Floor 2 Go</td><td>CAMARO 2228 ATLANTIC OAK GLUEDOWN 2.53M2</td><td>C118</td><td>181x1219</td><td>2.53</td><td>46.0</td></tr>
    <tr><td>Floor 2 Go</td><td>CAMARO 2234 BALTERIO SUPREME 2.53M2</td><td>C124</td><td>181x1219</td><td>2.53</td><td>46.0</td></tr>
    <tr><td>Floor 2 Go</td><td>CAMARO 2242 CARTAGENA GLUEDOWN 2.53M2</td><td>C132</td><td>181x1219</td><td>2.53</td><td>46.0</td></tr>
    <tr><td>V8 Allstyle</td><td>Artic Ice Polished 1200x600 (1.44)</td><td>ASG2016</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Artic Ice Polished 1200x1200 (1.44)</td><td>ASG2017</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Calacatta Crema Polished 1200x600(1.44)</td><td>ASG2018</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Calacatta Crema Polished 1200x1200(1.44)</td><td>ASG2019</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Blue Polished 1200x600(1.44)</td><td>ASG2022</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Gold Polished 1200x1200(1.44)</td><td>ASG2021</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Esplendor Gold Polished 1200x600(1.44)</td><td>ASG2020</td><td>1200x600</td><td>1.44</td><td>65.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Galaxy Blue Polished 1200x600 (1.44)</td><td>ASG1510</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Galaxy Cream Polished 1200x600 (1.44)</td><td>ASG2041</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Galaxy Grey Polished 1200x600 (1.44)</td><td>ASG2042</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Marshall Gold 1200X600 Polished  Rect (1.44)</td><td>ASG1526</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Marshall Gold 1200x1200 Polished Rect (1.44)</td><td>ASG1589</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Marshall Gold Floor 600x600 Polish Rect 1.44)</td><td>ASG1434</td><td>600x600</td><td>1.44</td><td>59.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Marshall White 1200x1200 Polished Rect (1.44)</td><td>ASG1781</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Luxury Beige Polished 1200x600 Gpor Rect (1.44)</td><td>ASG984</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Stagnone Gold 1200x1200 Polished  Rect (1.44)</td><td>ASG1442</td><td>1200x1200</td><td>1.44</td><td>85.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Stagnone Gold 1200x600 Polished  Rect (1.44)</td><td>ASG1441</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Patagonia Blue 1200x1200 Polished  Rect (1.44)</td><td>ASG1439</td><td>1200x1200</td><td>1.44</td><td>89.95</td></tr>
    <tr><td>V8 Allstyle</td><td>Patagonia Blue 1200x600 Polished  Rect (1.44)</td><td>ASG1438</td><td>1200x600</td><td>1.44</td><td>69.95</td></tr>
    """
    
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
        if 'laminate' in name_lower:
            category = 'Laminate'
        elif 'herringbone' in name_lower:
            category = 'Laminate'  
        elif 'oak' in name_lower or 'wood' in name_lower:
            if 'camaro' in name_lower:
                category = 'LVT'
            else:
                category = 'Laminate'
        elif 'polished' in name_lower or 'marble' in name_lower or 'stone' in name_lower:
            category = 'Tiles'
        elif 'gluedown' in name_lower or 'camaro' in name_lower:
            category = 'LVT'
        else:
            category = 'Various'
        
        # Extract thickness and finish information
        thickness = None
        finish = 'Matt'
        
        if 'polished' in name_lower:
            finish = 'Polished'
        elif 'matt' in name_lower:
            finish = 'Matt'
        elif 'satin' in name_lower:
            finish = 'Satin'
        
        # Extract thickness from name
        thickness_match = re.search(r'(\d+)mm', name)
        if thickness_match:
            thickness = f"{thickness_match.group(1)}mm"
        
        products.append({
            'supplier': supplier,
            'name': name,
            'sku': sku,
            'tile_size': tile_size,
            'box_size': box_size,
            'price': price,
            'category': category,
            'thickness': thickness,
            'finish': finish,
            'description': f"High-quality {category.lower()} from {supplier}",
            'in_stock': True
        })
    
    return products

if __name__ == "__main__":
    # Test the parsing
    products = parse_all_twfsfitting_products()
    print(f"Parsed {len(products)} products")
    
    # Save to JSON file for testing
    with open('/app/parsed_all_products.json', 'w') as f:
        json.dump(products, f, indent=2)
    
    print("Sample products:")
    for i, product in enumerate(products[:5]):
        print(f"{i+1}. {product['name']} - {product['supplier']} - £{product['price']}")
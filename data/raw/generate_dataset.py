"""
E-Commerce Sales Analytics - Synthetic Dataset Generator
Generates 15,000+ realistic e-commerce transaction records
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# ==================================================
# CONFIGURATION
# ==================================================
NUM_RECORDS = 15000
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================================================
# REFERENCE DATA
# ==================================================

# Categories and sub-categories
CATEGORIES = {
    'Furniture': ['Bookcases', 'Chairs', 'Furnishings', 'Tables', 'Office Furniture', 'Sofas'],
    'Office Supplies': ['Binders', 'Paper', 'Labels', 'Storage', 'Art', 'Envelopes', 'Appliances', 'Fasteners', 'Scissors', 'Pens'],
    'Technology': ['Phones', 'Computers', 'Accessories', 'Printers', 'Monitors', 'Tablets', 'Cameras', 'Software', 'Networking', 'Smart Home Devices']
}

# Products with prices and costs
PRODUCTS = {
    'Bookcases': [('Classic Bookcase', 180.00, 100.00), ('Modern Bookshelf', 250.00, 140.00), ('Corner Bookcase', 320.00, 180.00)],
    'Chairs': [('Executive Office Chair', 450.00, 250.00), ('Ergonomic Chair', 350.00, 195.00), ('Guest Chair', 120.00, 65.00)],
    'Furnishings': [('Desk Lamp', 45.00, 25.00), ('Throw Pillow Set', 55.00, 30.00), ('Area Rug', 200.00, 110.00)],
    'Tables': [('Coffee Table', 300.00, 165.00), ('Desk Table', 400.00, 220.00), ('Dining Table', 550.00, 300.00)],
    'Office Furniture': [('Standing Desk', 600.00, 330.00), ('Filing Cabinet', 180.00, 100.00), ('Office Partition', 280.00, 155.00)],
    'Sofas': [('3-Seater Sofa', 800.00, 440.00), ('Loveseat', 600.00, 330.00), ('Sectional', 1200.00, 660.00)],
    'Binders': [('A4 Ring Binder', 8.00, 4.50), ('Presentation Binder', 15.00, 8.25), ('Heavy Duty Binder', 12.00, 6.60)],
    'Paper': [('Ream A4 Paper', 10.00, 5.50), ('Glossy Photo Paper', 18.00, 10.00), ('Card Stock Paper', 14.00, 7.70)],
    'Labels': [('Address Labels', 12.00, 6.50), ('Shipping Labels', 20.00, 11.00), ('Avery Labels Pack', 25.00, 13.75)],
    'Storage': [('Plastic Storage Bin', 22.00, 12.00), ('Metal Shelf Unit', 85.00, 46.75), ('Storage Cabinet', 200.00, 110.00)],
    'Art': [('Canvas Print', 65.00, 35.00), ('Wall Art Set', 90.00, 49.50), ('Desk Sculpture', 40.00, 22.00)],
    'Envelopes': [('#10 Envelopes Box', 15.00, 8.00), ('Clasp Envelopes', 18.00, 10.00), ('Padded Mailers', 22.00, 12.00)],
    'Appliances': [('Coffee Maker', 80.00, 44.00), ('Mini Fridge', 150.00, 82.50), ('Microwave', 120.00, 66.00)],
    'Fasteners': [('Stapler', 25.00, 13.75), ('Staples Box', 5.00, 2.75), ('Paper Clips Pack', 3.00, 1.65)],
    'Scissors': [('Office Scissors', 12.00, 6.50), ('Utility Knife', 8.00, 4.40), ('Safety Scissors', 10.00, 5.50)],
    'Pens': [('Ballpoint Pens Box', 12.00, 6.50), ('Marker Set', 18.00, 10.00), ('Fountain Pen', 35.00, 19.25)],
    'Phones': [('Smartphone', 699.00, 480.00), ('Office Phone', 120.00, 65.00),('Headset', 85.00, 45.00)],
    'Computers': [('Laptop Pro', 1200.00, 800.00), ('Desktop PC', 900.00, 600.00), ('All-in-One', 1100.00, 750.00)],
    'Accessories': [('USB-C Hub', 45.00, 25.00), ('Wireless Mouse', 35.00, 19.00), ('Keyboard', 60.00, 33.00)],
    'Printers': [('Laser Printer', 250.00, 150.00), ('Inkjet Printer', 150.00, 85.00), ('Multifunction Printer', 350.00, 200.00)],
    'Monitors': [('24-inch Monitor', 280.00, 165.00), ('27-inch Monitor', 380.00, 225.00), ('Ultrawide Monitor', 550.00, 330.00)],
    'Tablets': [('10-inch Tablet', 350.00, 210.00), ('iPad Pro', 999.00, 700.00), ('Fire Tablet', 150.00, 90.00)],
    'Cameras': [('Webcam', 70.00, 38.00), ('Security Camera', 120.00, 65.00), ('DSLR Camera', 800.00, 500.00)],
    'Software': [('Office Suite', 200.00, 120.00), ('Antivirus', 60.00, 35.00), ('Design Software', 300.00, 180.00)],
    'Networking': [('WiFi Router', 100.00, 55.00), ('Network Switch', 80.00, 44.00), ('Ethernet Cable Pack', 25.00, 13.75)],
    'Smart Home Devices': [('Smart Speaker', 130.00, 72.00), ('Smart Thermostat', 200.00, 110.00), ('Smart Bulbs Pack', 50.00, 27.50)]
}

# US States, Cities, and Regions
STATE_REGION_CITY = {
    'West': {
        'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento', 'San Jose'],
        'Washington': ['Seattle', 'Spokane', 'Tacoma', 'Bellevue', 'Olympia'],
        'Oregon': ['Portland', 'Salem', 'Eugene', 'Bend', 'Gresham'],
        'Nevada': ['Las Vegas', 'Reno', 'Henderson', 'Carson City', 'Sparks'],
        'Arizona': ['Phoenix', 'Tucson', 'Mesa', 'Scottsdale', 'Chandler']
    },
    'East': {
        'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany', 'Syracuse'],
        'Massachusetts': ['Boston', 'Cambridge', 'Worcester', 'Springfield', 'Lowell'],
        'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie', 'Harrisburg'],
        'New Jersey': ['Newark', 'Jersey City', 'Paterson', 'Elizabeth', 'Trenton'],
        'Virginia': ['Virginia Beach', 'Richmond', 'Arlington', 'Norfolk', 'Alexandria']
    },
    'Central': {
        'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth'],
        'Illinois': ['Chicago', 'Aurora', 'Naperville', 'Springfield', 'Peoria'],
        'Ohio': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron'],
        'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor', 'Lansing', 'Flint'],
        'Indiana': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend', 'Bloomington']
    },
    'South': {
        'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Fort Lauderdale'],
        'Georgia': ['Atlanta', 'Savannah', 'Augusta', 'Macon', 'Athens'],
        'North Carolina': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham', 'Winston-Salem'],
        'Tennessee': ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga', 'Clarksville'],
        'Alabama': ['Birmingham', 'Montgomery', 'Mobile', 'Huntsville', 'Tuscaloosa']
    }
}

# Customer segments
SEGMENTS = ['Consumer', 'Corporate', 'Home Office']

# Payment modes
PAYMENT_MODES = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash', 'UPI/Wallet']

# Shipping modes
SHIPPING_MODES = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

# Customer names (first + last)
FIRST_NAMES = ['James','Mary','John','Patricia','Robert','Jennifer','Michael','Linda','David','Elizabeth',
               'William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Christopher','Karen',
               'Charles','Lisa','Daniel','Nancy','Matthew','Betty','Anthony','Margaret','Mark','Sandra',
               'Donald','Ashley','Steven','Kimberly','Andrew','Emily','Paul','Donna','Joshua','Michelle',
               'Kenneth','Carol','Kevin','Amanda','Brian','Dorothy','George','Melissa','Timothy','Deborah',
               'Ronald','Stephanie','Edward','Rebecca','Jason','Sharon','Jeffrey','Laura','Ryan','Cynthia',
               'Jacob','Kathleen','Gary','Amy','Nicholas','Shirley','Eric','Angela','Jonathan','Helen',
               'Stephen','Anna','Larry','Brenda','Justin','Pamela','Scott','Nicole','Brandon','Emma',
               'Benjamin','Samantha','Samuel','Katherine','Raymond','Christine','Gregory','Debra','Frank','Rachel']

LAST_NAMES = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
              'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin',
              'Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson',
              'Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores',
              'Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts',
              'Gomez','Phillips','Evans','Turner','Diaz','Parker','Cruz','Edwards','Collins','Reyes',
              'Stewart','Morris','Morales','Murphy','Cook','Rogers','Gutierrez','Ortiz','Morgan','Cooper',
              'Peterson','Bailey','Reed','Kelly','Howard','Ramos','Kim','Cox','Ward','Richardson',
              'Watson','Brooks','Chavez','Wood','James','Bennett','Gray','Mendoza','Ruiz','Hughes']

# Return statuses
RETURN_STATUSES = ['Returned', 'Not Returned']

# ==================================================
# GENERATE CUSTOMERS (2,000 unique customers)
# ==================================================
def generate_customers(n=2000):
    """Generate unique customer records."""
    customers = []
    used_names = set()
    
    for i in range(1, n + 1):
        while True:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            if name not in used_names:
                used_names.add(name)
                break
        
        region = random.choice(list(STATE_REGION_CITY.keys()))
        state = random.choice(list(STATE_REGION_CITY[region].keys()))
        city = random.choice(STATE_REGION_CITY[region][state])
        segment = random.choice(SEGMENTS)
        email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@email.com"
        
        customers.append({
            'Customer ID': f'CUST-{i:05d}',
            'Customer Name': name,
            'Segment': segment,
            'Region': region,
            'State': state,
            'City': city,
            'Email': email,
            'Registration Date': generate_random_date('2020-01-01', '2024-12-31')
        })
    
    return pd.DataFrame(customers)


def generate_random_date(start_date, end_date):
    """Generate a random date between start and end."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')


# ==================================================
# GENERATE ORDERS (15,000 records)
# ==================================================
def generate_orders(customers_df, num_records=15000):
    """Generate complete order dataset with 15,000+ records."""
    orders = []
    
    # Precompute category-subcategory-product mapping
    product_list = []
    for cat, subcats in CATEGORIES.items():
        for subcat in subcats:
            for prod_name, price, cost in PRODUCTS[subcat]:
                product_list.append({
                    'Category': cat,
                    'Sub-Category': subcat,
                    'Product Name': prod_name,
                    'Price': price,
                    'Cost': cost
                })
    
    for i in range(1, num_records + 1):
        order_id = f'ORD-{i:06d}'
        
        # Pick a random customer
        customer = customers_df.sample(1).iloc[0]
        
        # Generate order dates
        order_date = datetime.strptime(generate_random_date('2021-01-01', '2024-12-31'), '%Y-%m-%d')
        ship_days = random.choices([2, 3, 5, 7, 10], weights=[15, 25, 30, 20, 10])[0]
        ship_date = order_date + timedelta(days=ship_days)
        
        # Pick a random product
        product = random.choice(product_list)
        
        # Quantity (1-10)
        quantity = random.choices(range(1, 11), weights=[25, 20, 18, 12, 10, 5, 4, 3, 2, 1])[0]
        
        # Discount (0% to 30%)
        discount = random.choices([0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], 
                                  weights=[40, 15, 15, 10, 10, 5, 5])[0]
        
        sales = product['Price'] * quantity
        discount_amount = sales * discount
        final_sales = sales - discount_amount
        profit = (product['Price'] - product['Cost']) * quantity - discount_amount
        
        # Shipping mode
        shipping = random.choices(SHIPPING_MODES, weights=[40, 25, 20, 15])[0]
        
        # Payment mode
        payment = random.choice(PAYMENT_MODES)
        
        # Return status (10% return rate)
        return_status = random.choices(RETURN_STATUSES, weights=[10, 90])[0]
        
        orders.append({
            'Order ID': order_id,
            'Order Date': order_date.strftime('%Y-%m-%d'),
            'Ship Date': ship_date.strftime('%Y-%m-%d'),
            'Shipping Mode': shipping,
            'Customer ID': customer['Customer ID'],
            'Customer Name': customer['Customer Name'],
            'Segment': customer['Segment'],
            'Country': 'USA',
            'Region': customer['Region'],
            'State': customer['State'],
            'City': customer['City'],
            'Category': product['Category'],
            'Sub-Category': product['Sub-Category'],
            'Product Name': product['Product Name'],
            'Sales': round(final_sales, 2),
            'Quantity': quantity,
            'Discount': discount,
            'Profit': round(profit, 2),
            'Shipping Cost': round(random.uniform(5, 50), 2),
            'Payment Mode': payment,
            'Return Status': return_status
        })
    
    return pd.DataFrame(orders)


# ==================================================
# MAIN EXECUTION
# ==================================================
def main():
    """Generate all datasets and export to CSV."""
    print("=" * 60)
    print("E-Commerce Sales Analytics - Dataset Generator")
    print("=" * 60)
    
    # Generate customers
    print("\n[1/3] Generating customers...")
    customers_df = generate_customers(2000)
    customers_df.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
    print(f"  [OK] {len(customers_df)} customers generated")
    
    # Generate orders
    print("\n[2/3] Generating orders...")
    orders_df = generate_orders(customers_df, NUM_RECORDS)
    orders_df.to_csv(os.path.join(OUTPUT_DIR, 'ecommerce_orders.csv'), index=False)
    print(f"  [OK] {len(orders_df)} orders generated")
    
    # Generate regions data
    print("\n[3/3] Generating reference data...")
    region_data = []
    for region, states in STATE_REGION_CITY.items():
        for state, cities in states.items():
            region_data.append({
                'Region': region,
                'State': state,
                'Cities': ', '.join(cities),
                'City Count': len(cities)
            })
    regions_df = pd.DataFrame(region_data)
    regions_df.to_csv(os.path.join(OUTPUT_DIR, 'regions.csv'), index=False)
    
    # Generate category data
    category_data = []
    for cat, subcats in CATEGORIES.items():
        for subcat in subcats:
            category_data.append({
                'Category': cat,
                'Sub-Category': subcat
            })
    categories_df = pd.DataFrame(category_data)
    categories_df.to_csv(os.path.join(OUTPUT_DIR, 'categories.csv'), index=False)
    
    print(f"  [OK] Reference data generated")
    
    # Summary
    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"\nFiles created in: {OUTPUT_DIR}")
    print(f"  - ecommerce_orders.csv ({len(orders_df):,} records)")
    print(f"  - customers.csv ({len(customers_df):,} records)")
    print(f"  - regions.csv ({len(regions_df):,} records)")
    print(f"  - categories.csv ({len(categories_df):,} records)")
    
    # Display sample
    print("\n" + "-" * 60)
    print("Sample Order Records (First 5):")
    print("-" * 60)
    print(orders_df[['Order ID', 'Order Date', 'Customer Name', 'Category', 'Sales', 'Profit']].head(10).to_string(index=False))
    
    print("\n" + "-" * 60)
    print("Sample Customers (First 5):")
    print("-" * 60)
    print(customers_df[['Customer ID', 'Customer Name', 'Segment', 'City', 'State']].head(10).to_string(index=False))


if __name__ == '__main__':
    main()

"""
Data Generator for Sales Performance Analytics Dashboard
Generates realistic sales transaction dataset with intentional data-quality issues
for data preprocessing and cleaning practice.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_sales_data(num_records=5150, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    # Date range: 2 full years (2023 - 2024)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days

    # Customer Pool
    customer_segments = ['Consumer', 'Corporate', 'Small Business']
    segment_weights = [0.50, 0.30, 0.20]
    
    customers = []
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
                   'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
                   'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
                   'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
                   'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                  'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
                  'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']

    for i in range(1, 251):
        cust_id = f"CUST-{1000 + i}"
        cust_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        cust_segment = random.choices(customer_segments, weights=segment_weights)[0]
        customers.append((cust_id, cust_name, cust_segment))

    # Regional mapping (Region -> State -> Cities)
    location_hierarchy = {
        'West': {
            'California': ['Los Angeles', 'San Francisco', 'San Diego', 'San Jose'],
            'Washington': ['Seattle', 'Spokane', 'Tacoma'],
            'Oregon': ['Portland', 'Salem', 'Eugene']
        },
        'East': {
            'New York': ['New York City', 'Buffalo', 'Rochester'],
            'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown'],
            'Massachusetts': ['Boston', 'Worcester', 'Cambridge']
        },
        'South': {
            'Texas': ['Houston', 'Austin', 'Dallas', 'San Antonio'],
            'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
            'Georgia': ['Atlanta', 'Savannah', 'Augusta']
        },
        'North': {
            'Illinois': ['Chicago', 'Aurora', 'Naperville'],
            'Ohio': ['Columbus', 'Cleveland', 'Cincinnati'],
            'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor']
        }
    }

    # Catalog mapping (Category -> Sub_Category -> Products with Base Price & Base Margin)
    catalog = {
        'Technology': {
            'Phones': [
                ('PROD-TEC-1001', 'iPhone 15 Pro 256GB', 999.00, 0.35),
                ('PROD-TEC-1002', 'Samsung Galaxy S24 Ultra', 1199.00, 0.38),
                ('PROD-TEC-1003', 'Google Pixel 8 Pro', 799.00, 0.30),
                ('PROD-TEC-1004', 'OnePlus 12 5G', 699.00, 0.28)
            ],
            'Accessories': [
                ('PROD-TEC-1005', 'Logitech MX Master 3S Wireless Mouse', 99.99, 0.45),
                ('PROD-TEC-1006', 'Apple AirPods Pro Gen 2', 249.00, 0.40),
                ('PROD-TEC-1007', 'Anker PowerBank 24000mAh', 89.99, 0.50),
                ('PROD-TEC-1008', 'Dell 11-in-1 USB-C Docking Station', 129.99, 0.42)
            ],
            'Copiers': [
                ('PROD-TEC-1009', 'Canon ImageRUNNER Advance Copier', 1499.00, 0.32),
                ('PROD-TEC-1010', 'HP LaserJet Enterprise Multifunction', 1299.00, 0.30)
            ],
            'Machines': [
                ('PROD-TEC-1011', 'Epson EcoTank Pro Color Printer', 599.00, 0.25),
                ('PROD-TEC-1012', 'Brother Industrial Label Maker', 299.00, 0.35)
            ]
        },
        'Furniture': {
            'Chairs': [
                ('PROD-FUR-2001', 'Herman Miller Ergonomic Task Chair', 650.00, 0.22),
                ('PROD-FUR-2002', 'Steelcase Executive Mesh Chair', 480.00, 0.20),
                ('PROD-FUR-2003', 'Mid-Back Swivel Office Chair', 180.00, 0.18)
            ],
            'Tables': [
                ('PROD-FUR-2004', 'Motorized Standing Electric Desk', 550.00, 0.15),
                ('PROD-FUR-2005', 'Conference Room Modular Table', 850.00, 0.12)
            ],
            'Bookcases': [
                ('PROD-FUR-2006', '5-Tier Industrial Metal & Wood Bookshelf', 220.00, 0.14),
                ('PROD-FUR-2007', 'Modern Oak Veneer Cabinet Bookcase', 340.00, 0.16)
            ],
            'Furnishings': [
                ('PROD-FUR-2008', 'Dimmable LED Architect Desk Lamp', 45.00, 0.30),
                ('PROD-FUR-2009', 'Memory Foam Ergonomic Seat Cushion', 35.00, 0.35)
            ]
        },
        'Office Supplies': {
            'Storage': [
                ('PROD-OFF-3001', 'Heavy-Duty Plastic Storage Containers 4-Pack', 65.00, 0.28),
                ('PROD-OFF-3002', 'Stackable Desk Document Organizer', 29.99, 0.32)
            ],
            'Paper': [
                ('PROD-OFF-3003', 'Multipurpose Copy Paper Case 10 Reams', 49.99, 0.25),
                ('PROD-OFF-3004', 'Premium Heavyweight Cardstock Paper', 24.99, 0.30)
            ],
            'Binders': [
                ('PROD-OFF-3005', 'Heavy Duty 3-Ring Binder 3-Inch 6-Pack', 34.99, 0.35),
                ('PROD-OFF-3006', 'Executive Leatherette Presentation Folders', 19.99, 0.40)
            ],
            'Appliances': [
                ('PROD-OFF-3007', 'Compact Office Mini Fridge 3.2 Cu. Ft.', 189.00, 0.20),
                ('PROD-OFF-3008', 'Single-Serve Office Coffee Maker', 79.00, 0.22)
            ],
            'Art': [
                ('PROD-OFF-3009', 'Dry Erase Chisel Tip Markers 36-Pack', 22.50, 0.45),
                ('PROD-OFF-3010', 'Professional Fineliner Drawing Pens', 15.99, 0.48)
            ],
            'Fasteners': [
                ('PROD-OFF-3011', 'Heavy Duty Electric Stapler 50-Sheet', 42.00, 0.35),
                ('PROD-OFF-3012', 'Assorted Steel Binder Clips Box', 12.00, 0.50)
            ],
            'Envelopes': [
                ('PROD-OFF-3013', 'Self-Seal Security Envelopes 500-Pack', 28.00, 0.38)
            ]
        }
    }

    payment_modes = ['Credit Card', 'Debit Card', 'UPI', 'Cash', 'Net Banking']
    payment_weights = [0.38, 0.22, 0.20, 0.10, 0.10]

    order_statuses = ['Completed', 'Cancelled', 'Returned']
    status_weights = [0.86, 0.09, 0.05]

    discounts = [0.00, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
    discount_weights = [0.45, 0.20, 0.15, 0.10, 0.05, 0.03, 0.02]

    rows = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2023 + (i % 2)}-{10000 + i}"
        
        # Random date generation with slight seasonal variation (higher sales Q4)
        random_days = random.randint(0, days_range)
        order_date_dt = start_date + timedelta(days=random_days)
        
        # Customer select
        cust_id, cust_name, cust_segment = random.choice(customers)

        # Location select
        region = random.choice(list(location_hierarchy.keys()))
        state = random.choice(list(location_hierarchy[region].keys()))
        city = random.choice(location_hierarchy[region][state])

        # Product select
        category = random.choice(list(catalog.keys()))
        sub_category = random.choice(list(catalog[category].keys()))
        product_id, product_name, unit_price, base_margin = random.choice(catalog[category][sub_category])

        # Quantity
        quantity = random.choices([1, 2, 3, 4, 5, 6, 7, 8], weights=[0.30, 0.25, 0.20, 0.12, 0.06, 0.04, 0.02, 0.01])[0]

        # Discount & Pricing
        discount = random.choices(discounts, weights=discount_weights)[0]
        
        # Calculate raw Sales and Profit
        # Profit margin decreases rapidly with higher discounts
        gross_sales = quantity * unit_price
        sales = round(gross_sales * (1.0 - discount), 2)
        
        # Profit formula: Base profit minus discount erosion
        effective_margin = base_margin - (discount * 1.35)
        profit = round(sales * effective_margin, 2)

        payment_mode = random.choices(payment_modes, weights=payment_weights)[0]
        order_status = random.choices(order_statuses, weights=status_weights)[0]

        # Standard date format
        date_str = order_date_dt.strftime('%Y-%m-%d')

        rows.append({
            'Order_ID': order_id,
            'Order_Date': date_str,
            'Customer_ID': cust_id,
            'Customer_Name': cust_name,
            'Customer_Segment': cust_segment,
            'Region': region,
            'State': state,
            'City': city,
            'Category': category,
            'Sub_Category': sub_category,
            'Product_ID': product_id,
            'Product_Name': product_name,
            'Quantity': quantity,
            'Unit_Price': unit_price,
            'Sales': sales,
            'Discount': discount,
            'Profit': profit,
            'Payment_Mode': payment_mode,
            'Order_Status': order_status
        })

    df = pd.DataFrame(rows)

    # -------------------------------------------------------------
    # Inject Data Quality Issues for Preprocessing Practice
    # -------------------------------------------------------------
    
    # 1. Date format anomalies (~100 rows with MM/DD/YYYY or DD-MM-YYYY)
    date_indices = random.sample(range(len(df)), 120)
    for idx in date_indices:
        dt = datetime.strptime(df.at[idx, 'Order_Date'], '%Y-%m-%d')
        if idx % 2 == 0:
            df.at[idx, 'Order_Date'] = dt.strftime('%m/%d/%Y')  # MM/DD/YYYY
        else:
            df.at[idx, 'Order_Date'] = dt.strftime('%d-%m-%Y')  # DD-MM-YYYY

    # 2. Missing values (~35 missing fields across Customer_Name, City, Payment_Mode)
    missing_cust_idx = random.sample(range(len(df)), 12)
    for idx in missing_cust_idx:
        df.at[idx, 'Customer_Name'] = np.nan

    missing_city_idx = random.sample(range(len(df)), 12)
    for idx in missing_city_idx:
        df.at[idx, 'City'] = np.nan

    missing_pay_idx = random.sample(range(len(df)), 12)
    for idx in missing_pay_idx:
        df.at[idx, 'Payment_Mode'] = np.nan

    # 3. Duplicate rows (~30 exact duplicate rows)
    dup_indices = random.sample(range(len(df)), 30)
    duplicates = df.iloc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # 4. A few high-value enterprise outliers
    outlier_idx = random.sample(range(len(df)), 5)
    for idx in outlier_idx:
        df.at[idx, 'Quantity'] = 25
        df.at[idx, 'Sales'] = round(df.at[idx, 'Unit_Price'] * 25 * (1 - df.at[idx, 'Discount']), 2)
        df.at[idx, 'Profit'] = round(df.at[idx, 'Sales'] * 0.35, 2)

    return df

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    raw_df = generate_sales_data(num_records=5150)
    file_path = os.path.join('data', 'raw_sales_data.csv')
    raw_df.to_csv(file_path, index=False)
    print(f"[SUCCESS] Raw sales dataset generated successfully at '{file_path}'")
    print(f"Total Records Generated (with duplicates & quality issues): {len(raw_df)}")

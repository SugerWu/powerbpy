"""Generate a Power BI dashboard with 5 charts for homework assignment.
Charts:
1. Monthly Sales & Orders (dual axis: columns + line)
2. Sales by Country (Top 10 bar chart)
3. Product Category (treemap)
4. Top 10 Products by Sales (horizontal bar chart)
5. Product Category Performance Over Time (stacked column)
"""

import os
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# Generate mock retail sales data
categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Home & Garden',
              'Sports', 'Toys', 'Beauty', 'Automotive', 'Office Supplies']

countries = ['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia',
             'Japan', 'China', 'Brazil', 'India', 'Mexico', 'Italy', 'Spain', 'Netherlands', 'Sweden']

products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera', 'Monitor', 'Keyboard', 'Mouse'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Dress', 'Hoodie', 'Shorts', 'Scarf'],
    'Food': ['Organic Coffee', 'Green Tea', 'Honey', 'Olive Oil', 'Pasta', 'Rice', 'Spices', 'Chocolate'],
    'Books': ['Novel', 'Textbook', 'Cookbook', 'Biography', 'Comic', 'Dictionary', 'Travel Guide', 'Journal'],
    'Home & Garden': ['Plant Pot', 'Candle', 'Throw Blanket', 'Vase', 'Picture Frame', 'Cushion', 'Lamp', 'Clock'],
    'Sports': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Water Bottle', 'Tennis Racket', 'Basketball', 'Bicycle Helmet', 'Jump Rope'],
    'Toys': ['Board Game', 'Puzzle', 'Lego Set', 'Action Figure', 'Plush Toy', 'Card Game', 'Drone', 'Art Set'],
    'Beauty': ['Moisturizer', 'Shampoo', 'Perfume', 'Lipstick', 'Sunscreen', 'Face Mask', 'Nail Polish', 'Brush Set'],
    'Automotive': ['Car Charger', 'Dash Camera', 'Air Freshener', 'Seat Cover', 'Floor Mat', 'Phone Mount', 'Wiper', 'Oil Filter'],
    'Office Supplies': ['Pen', 'Notebook', 'Stapler', 'Paper Clips', 'Whiteboard', 'Desk Organizer', 'Sticky Notes', 'Envelope']
}

# Generate 12 months of data (Jan-Dec 2024)
start_date = datetime(2024, 1, 1)
months = []
for i in range(12):
    month_date = datetime(2024, 1, 1) + timedelta(days=30 * i)
    months.append(month_date.strftime('%Y-%m'))

all_rows = []

for month in months:
    # Vary number of orders by season
    if month.startswith('12'):
        n_orders = random.randint(380, 450)
    elif month.startswith('01'):
        n_orders = random.randint(300, 380)
    else:
        n_orders = random.randint(280, 350)

    for _ in range(n_orders):
        member_id = random.randint(1000, 9999)
        category = random.choice(categories)
        product = random.choice(products[category])
        country = random.choice(countries)

        # Generate a random date within the month
        day = random.randint(1, 28)
        order_date = datetime.strptime(f'{month}-{day:02d}', '%Y-%m-%d')

        # Generate price (more expensive items for some categories)
        if category == 'Electronics':
            price = round(random.uniform(50, 2000), 2)
        elif category == 'Food':
            price = round(random.uniform(5, 100), 2)
        else:
            price = round(random.uniform(10, 500), 2)

        # Quantity
        quantity = random.randint(1, 10)

        total_sales = round(price * quantity, 2)

        all_rows.append({
            'order_id': f'ORD-{random.randint(100000, 999999)}',
            'order_date': order_date.strftime('%Y-%m-%d'),
            'month': month,
            'member_id': member_id,
            'country': country,
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': price,
            'total_sales': total_sales
        })

# Write CSV
output_csv = '/tmp/powerbpy-fork/sales_data.csv'
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'order_date', 'month', 'member_id',
                                           'country', 'category', 'product', 'quantity',
                                           'unit_price', 'total_sales'])
    writer.writeheader()
    writer.writerows(all_rows)

print(f'Generated {len(all_rows)} orders in {output_csv}')

# Now create the Power BI dashboard
from powerbpy import Dashboard

dashboard_path = '/tmp/powerbpy-fork/sales_dashboard'

# Create dashboard
dashboard = Dashboard.create(dashboard_path)
print(f'Created dashboard at {dashboard_path}')

# Add CSV data
dataset = dashboard.add_local_csv(data_path=output_csv)
print(f'Added dataset: {dataset.dataset_name}')

# Create a page
page1 = dashboard.new_page(
    page_name="Sales Dashboard",
    title="Monthly Sales Performance",
    subtitle="Key Metrics & Trends"
)

# ============ Chart 1: Monthly Sales & Orders (Dual Axis) ============
page1.add_dual_axis_chart(
    visual_id='monthly_sales_orders',
    data_source='sales_data',
    chart_title='Monthly Sales & Orders',
    x_axis_title='Month',
    y_axis_title_left='Sales ($)',
    y_axis_title_right='Orders (Count)',
    x_axis_var='month',
    col_y_axis_var='total_sales',
    col_y_axis_var_aggregation_type='Sum',
    line_y_axis_var='order_id',
    line_y_axis_var_aggregation_type='Count',
    x_position=50,
    y_position=180,
    height=350,
    width=1150,
    show_data_labels=True,
    legend_position='Bottom'
)
print('Added Chart 1: Monthly Sales & Orders (Dual Axis)')

# ============ Chart 2: Sales by Country (Top 10 Bar Chart) ============
page1.add_chart(
    visual_id='country_sales',
    data_source='sales_data',
    chart_title='Sales by Country (Top 10)',
    x_axis_title='Country',
    y_axis_title='Total Sales ($)',
    x_axis_var='country',
    y_axis_var='total_sales',
    y_axis_var_aggregation_type='Sum',
    x_position=50,
    y_position=560,
    height=300,
    width=560,
    chart_type='barChart'
)
print('Added Chart 2: Sales by Country (Bar Chart)')

# ============ Chart 3: Product Category (Treemap) ============
page1.add_treemap_chart(
    visual_id='category_treemap',
    data_source='sales_data',
    chart_title='Sales by Product Category',
    category_var='category',
    value_var='total_sales',
    value_var_aggregation_type='Sum',
    x_position=630,
    y_position=560,
    height=300,
    width=560,
    show_data_labels=True,
    show_legend=True
)
print('Added Chart 3: Product Category (Treemap)')

# ============ Chart 4: Top 10 Products (Horizontal Bar Chart) ============
page1.add_chart(
    visual_id='top_products',
    data_source='sales_data',
    chart_title='Top 10 Products by Sales',
    x_axis_title='Product',
    y_axis_title='Total Sales ($)',
    x_axis_var='product',
    y_axis_var='total_sales',
    y_axis_var_aggregation_type='Sum',
    x_position=50,
    y_position=890,
    height=300,
    width=1150,
    chart_type='barChart'
)
print('Added Chart 4: Top 10 Products (Horizontal Bar Chart)')

# ============ Chart 5: Product Category Performance Over Time (Line Chart) ============
page1.add_line_chart(
    visual_id='category_trend',
    data_source='sales_data',
    chart_title='Sales by Category Over Time',
    x_axis_title='Month',
    y_axis_title='Sales ($)',
    x_axis_var='month',
    y_axis_var='total_sales',
    y_axis_var_aggregation_type='Sum',
    x_position=50,
    y_position=1220,
    height=350,
    width=1150,
    show_data_labels=False,
    legend_position='Bottom'
)
print('Added Chart 5: Product Category Performance Over Time (Line Chart)')

# Save
dashboard_path_full = os.path.abspath(dashboard_path)
print(f'\n=== Dashboard generated at: {dashboard_path_full} ===')
print(f'Open with Power BI Desktop to view the dashboard.')

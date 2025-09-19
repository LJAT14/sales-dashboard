import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv

# Set random seed for reproducible data
np.random.seed(42)

def generate_sales_data():
    """
    Generate comprehensive sales data for the dashboard
    """
    
    # Date range - last 2 years with daily data
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Business data parameters
    products = ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 'Scanner', 'Tablet']
    categories = ['Electronics', 'Accessories', 'Peripherals']
    regions = ['North America', 'Europe', 'Asia Pacific', 'South America', 'Africa']
    sales_reps = ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'Tom Davis', 
                  'Maria Garcia', 'David Chen', 'Emma Thompson', 'Carlos Rodriguez', 'Anna Petrov']
    customers = [f'CUST_{i:05d}' for i in range(1, 1001)]  # 1000 unique customers
    
    # Product pricing
    base_prices = {
        'Laptop': 800, 'Desktop': 600, 'Monitor': 300, 'Keyboard': 50,
        'Mouse': 25, 'Printer': 150, 'Scanner': 200, 'Tablet': 400
    }
    
    # Category mapping
    product_categories = {
        'Laptop': 'Electronics', 'Desktop': 'Electronics', 'Monitor': 'Electronics',
        'Tablet': 'Electronics', 'Keyboard': 'Accessories', 'Mouse': 'Accessories',
        'Printer': 'Peripherals', 'Scanner': 'Peripherals'
    }
    
    data = []
    order_id = 1
    
    for date in dates:
        # Determine number of sales per day (varies by seasonality)
        day_of_year = date.timetuple().tm_yday
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
        
        # Holiday seasons (November, December)
        if date.month in [11, 12]:
            seasonal_factor *= 1.8
        elif date.month in [6, 7]:  # Summer sales
            seasonal_factor *= 1.3
        elif date.month in [1, 2]:  # Post-holiday slowdown
            seasonal_factor *= 0.7
        
        # Weekend vs weekday effect
        if date.weekday() < 5:  # Weekday
            daily_factor = 1.2
        else:  # Weekend
            daily_factor = 0.8
        
        # Growth trend over time
        days_since_start = (date - start_date).days
        growth_factor = 1 + (days_since_start / 365) * 0.15  # 15% annual growth
        
        # Calculate number of transactions for the day
        base_transactions = 15
        num_transactions = max(1, int(np.random.poisson(
            base_transactions * seasonal_factor * daily_factor * growth_factor
        )))
        
        for _ in range(num_transactions):
            # Select product and related attributes
            product = np.random.choice(products)
            category = product_categories[product]
            
            # Regional distribution (weighted)
            region = np.random.choice(regions, p=[0.35, 0.25, 0.20, 0.15, 0.05])
            
            # Sales rep assignment (some reps perform better)
            rep_weights = [0.15, 0.12, 0.11, 0.10, 0.10, 0.09, 0.09, 0.08, 0.08, 0.08]
            sales_rep = np.random.choice(sales_reps, p=rep_weights)
            
            # Customer selection
            customer_id = np.random.choice(customers)
            
            # Price calculation with various factors
            base_price = base_prices[product]
            
            # Regional pricing adjustment
            region_multipliers = {
                'North America': 1.2, 'Europe': 1.1, 'Asia Pacific': 0.9,
                'South America': 0.8, 'Africa': 0.7
            }
            region_multiplier = region_multipliers[region]
            
            # Sales rep performance factor
            rep_performance = {
                'John Smith': 1.15, 'Sarah Johnson': 1.12, 'Mike Wilson': 1.08,
                'Lisa Brown': 1.05, 'Tom Davis': 1.03, 'Maria Garcia': 1.10,
                'David Chen': 1.07, 'Emma Thompson': 1.06, 'Carlos Rodriguez': 1.04,
                'Anna Petrov': 1.09
            }
            rep_factor = rep_performance[sales_rep]
            
            # Random price variation
            price_variation = np.random.uniform(0.85, 1.25)
            
            # Final unit price
            unit_price = base_price * region_multiplier * rep_factor * price_variation
            
            # Quantity (most orders are 1-3 items, occasional bulk orders)
            if np.random.random() < 0.1:  # 10% chance of bulk order
                quantity = np.random.randint(5, 20)
            else:
                quantity = np.random.randint(1, 4)
            
            # Calculate totals
            revenue = unit_price * quantity
            
            # Cost calculation (40-70% of revenue)
            cost_ratio = np.random.uniform(0.4, 0.7)
            cost = revenue * cost_ratio
            profit = revenue - cost
            profit_margin = (profit / revenue) * 100
            
            # Discount calculation
            if np.random.random() < 0.2:  # 20% chance of discount
                discount_percent = np.random.uniform(5, 25)
                discount_amount = revenue * (discount_percent / 100)
            else:
                discount_percent = 0
                discount_amount = 0
            
            # Final revenue after discount
            final_revenue = revenue - discount_amount
            final_profit = final_revenue - cost
            final_margin = (final_profit / final_revenue) * 100 if final_revenue > 0 else 0
            
            # Shipping and tax
            shipping_cost = np.random.uniform(5, 25) if region != 'North America' else np.random.uniform(2, 10)
            tax_rate = 0.08 if region == 'North America' else 0.15
            tax_amount = final_revenue * tax_rate
            
            # Customer satisfaction (correlated with profit margin and rep performance)
            base_satisfaction = 3.5
            satisfaction_boost = (final_margin / 100) * 0.5 + (rep_factor - 1) * 2
            customer_satisfaction = min(5.0, max(1.0, 
                base_satisfaction + satisfaction_boost + np.random.normal(0, 0.3)
            ))
            
            # Delivery time (varies by region)
            region_delivery_days = {
                'North America': (1, 5), 'Europe': (3, 8), 'Asia Pacific': (5, 12),
                'South America': (7, 15), 'Africa': (10, 20)
            }
            min_days, max_days = region_delivery_days[region]
            delivery_days = np.random.randint(min_days, max_days + 1)
            
            # Return probability (lower for higher satisfaction)
            return_probability = max(0.01, 0.15 - (customer_satisfaction - 3) * 0.03)
            is_returned = np.random.random() < return_probability
            
            # Create record
            record = {
                'Order_ID': f'ORD_{order_id:06d}',
                'Date': date.strftime('%Y-%m-%d'),
                'Customer_ID': customer_id,
                'Product': product,
                'Category': category,
                'Region': region,
                'Sales_Rep': sales_rep,
                'Quantity': quantity,
                'Unit_Price': round(unit_price, 2),
                'Revenue': round(revenue, 2),
                'Cost': round(cost, 2),
                'Profit': round(profit, 2),
                'Profit_Margin': round(profit_margin, 2),
                'Discount_Percent': round(discount_percent, 2),
                'Discount_Amount': round(discount_amount, 2),
                'Final_Revenue': round(final_revenue, 2),
                'Final_Profit': round(final_profit, 2),
                'Final_Margin': round(final_margin, 2),
                'Shipping_Cost': round(shipping_cost, 2),
                'Tax_Amount': round(tax_amount, 2),
                'Customer_Satisfaction': round(customer_satisfaction, 2),
                'Delivery_Days': delivery_days,
                'Is_Returned': is_returned,
                'Year': date.year,
                'Month': date.month,
                'Quarter': f'Q{((date.month - 1) // 3) + 1}',
                'Day_of_Week': date.strftime('%A'),
                'Week_Number': date.isocalendar()[1]
            }
            
            data.append(record)
            order_id += 1
    
    return pd.DataFrame(data)

# Generate the data
print("Generating sales data...")
df = generate_sales_data()

# Save to CSV
df.to_csv('sales_data.csv', index=False)
print(f"Sales data generated: {len(df)} records")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Total revenue: ${df['Final_Revenue'].sum():,.2f}")
print(f"Total profit: ${df['Final_Profit'].sum():,.2f}")
print(f"Average margin: {df['Final_Margin'].mean():.2f}%")

# Display sample data
print("\nSample data (first 10 rows):")
print(df.head(10))

# Summary statistics
print("\nData Summary:")
print(f"Unique customers: {df['Customer_ID'].nunique()}")
print(f"Unique products: {df['Product'].nunique()}")
print(f"Unique regions: {df['Region'].nunique()}")
print(f"Unique sales reps: {df['Sales_Rep'].nunique()}")
print(f"Average order value: ${df['Final_Revenue'].mean():.2f}")
print(f"Return rate: {df['Is_Returned'].mean()*100:.2f}%")

# Create additional sample files
print("\nCreating additional sample files...")

# Customer data
customers_data = df.groupby('Customer_ID').agg({
    'Final_Revenue': 'sum',
    'Quantity': 'sum',
    'Order_ID': 'count',
    'Customer_Satisfaction': 'mean',
    'Is_Returned': lambda x: (x == True).sum(),
    'Region': 'first',
    'Date': ['min', 'max']
}).round(2)

customers_data.columns = ['Total_Revenue', 'Total_Quantity', 'Total_Orders', 
                         'Avg_Satisfaction', 'Returns_Count', 'Region', 
                         'First_Order_Date', 'Last_Order_Date']
customers_data.reset_index(inplace=True)
customers_data.to_csv('customer_summary.csv', index=False)

# Product performance
product_data = df.groupby('Product').agg({
    'Final_Revenue': 'sum',
    'Quantity': 'sum',
    'Order_ID': 'count',
    'Final_Margin': 'mean',
    'Customer_Satisfaction': 'mean',
    'Is_Returned': lambda x: (x == True).sum() / len(x) * 100
}).round(2)

product_data.columns = ['Total_Revenue', 'Total_Quantity', 'Total_Orders', 
                       'Avg_Margin', 'Avg_Satisfaction', 'Return_Rate']
product_data.reset_index(inplace=True)
product_data.to_csv('product_performance.csv', index=False)

# Sales rep performance
rep_data = df.groupby('Sales_Rep').agg({
    'Final_Revenue': 'sum',
    'Order_ID': 'count',
    'Final_Margin': 'mean',
    'Customer_Satisfaction': 'mean',
    'Customer_ID': 'nunique'
}).round(2)

rep_data.columns = ['Total_Revenue', 'Total_Orders', 'Avg_Margin', 
                   'Avg_Customer_Satisfaction', 'Unique_Customers']
rep_data.reset_index(inplace=True)
rep_data.to_csv('sales_rep_performance.csv', index=False)

# Monthly summary
monthly_data = df.groupby(['Year', 'Month']).agg({
    'Final_Revenue': 'sum',
    'Final_Profit': 'sum',
    'Order_ID': 'count',
    'Customer_ID': 'nunique',
    'Quantity': 'sum'
}).round(2)

monthly_data.columns = ['Revenue', 'Profit', 'Orders', 'Unique_Customers', 'Units_Sold']
monthly_data.reset_index(inplace=True)
monthly_data['Date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
monthly_data.to_csv('monthly_summary.csv', index=False)

print("Additional files created:")
print("- customer_summary.csv")
print("- product_performance.csv") 
print("- sales_rep_performance.csv")
print("- monthly_summary.csv")

print(f"\n✅ Complete! All CSV files are ready for your Sales Dashboard.")
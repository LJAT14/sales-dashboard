import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Data loading function with fallback
@st.cache_data
def load_data():
    """Load data from CSV files or generate sample data if files don't exist"""
    
    try:
        # Try to load from data folder first
        if os.path.exists('data/sales_data.csv'):
            df = pd.read_csv('data/sales_data.csv')
            st.sidebar.success("✅ Loaded data from files")
            return df
        elif os.path.exists('sales_data.csv'):
            df = pd.read_csv('sales_data.csv')
            st.sidebar.success("✅ Loaded data from files")
            return df
        else:
            # Generate sample data if no files found
            st.sidebar.info("📊 Generating sample data...")
            return generate_sample_data()
            
    except Exception as e:
        st.sidebar.warning(f"⚠️ Error loading data: {str(e)}")
        st.sidebar.info("📊 Generating sample data...")
        return generate_sample_data()

@st.cache_data
def generate_sample_data():
    """Generate sample sales data for demonstration"""
    np.random.seed(42)
    
    # Date range for sample data
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Business parameters
    products = ['Laptop', 'Desktop', 'Monitor', 'Keyboard', 'Mouse', 'Printer', 'Scanner', 'Tablet']
    categories = ['Electronics', 'Accessories', 'Peripherals']
    regions = ['North America', 'Europe', 'Asia Pacific', 'South America', 'Africa']
    sales_reps = ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Lisa Brown', 'Tom Davis']
    
    data = []
    
    # Generate sample data (smaller dataset for cloud deployment)
    for i, date in enumerate(dates[::3]):  # Every 3rd day to reduce size
        num_sales = np.random.poisson(8)  # Average 8 sales per day
        
        for _ in range(num_sales):
            product = np.random.choice(products)
            category = np.random.choice(categories)
            region = np.random.choice(regions)
            sales_rep = np.random.choice(sales_reps)
            
            # Base pricing
            base_prices = {
                'Laptop': 800, 'Desktop': 600, 'Monitor': 300, 'Keyboard': 50,
                'Mouse': 25, 'Printer': 150, 'Scanner': 200, 'Tablet': 400
            }
            
            price = base_prices[product] * np.random.uniform(0.8, 1.3)
            quantity = np.random.randint(1, 5)
            revenue = price * quantity
            
            # Add seasonality
            month_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
            year_factor = 1 + 0.1 * (date.year - 2022)
            revenue *= month_factor * year_factor
            
            data.append({
                'Date': date,
                'Product': product,
                'Category': category,
                'Region': region,
                'Sales_Rep': sales_rep,
                'Quantity': quantity,
                'Unit_Price': round(price, 2),
                'Revenue': round(revenue, 2),
                'Cost': round(revenue * 0.6, 2),
                'Profit': round(revenue * 0.4, 2),
                'Profit_Margin': 40.0,
                'Year': date.year,
                'Month': date.month,
                'Quarter': date.quarter
            })
    
    df = pd.DataFrame(data)
    return df

# Load the data
with st.spinner("Loading dashboard data..."):
    df = load_data()

# Header
st.markdown('<h1 class="main-header">📊 Sales Performance Dashboard</h1>', unsafe_allow_html=True)

# Add info about the demo
st.info("""
🎯 **Live Demo Dashboard** - This is a fully functional sales analytics dashboard showcasing:
- Interactive data visualization with Plotly
- Real-time filtering and drill-down capabilities  
- Business intelligence metrics and KPIs
- Professional dashboard design and user experience

*Note: This demo uses generated sample data to demonstrate functionality.*
""")

# Sidebar filters
st.sidebar.header("🔍 Dashboard Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=[df['Date'].min(), df['Date'].max()],
    min_value=df['Date'].min(),
    max_value=df['Date'].max()
)

if len(date_range) == 2:
    start_date, end_date = date_range
    df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & 
                     (df['Date'] <= pd.to_datetime(end_date))]
else:
    df_filtered = df

# Other filters
regions = st.sidebar.multiselect(
    "Select Regions",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

categories = st.sidebar.multiselect(
    "Select Categories", 
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

products = st.sidebar.multiselect(
    "Select Products",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

# Apply filters
df_filtered = df_filtered[
    (df_filtered['Region'].isin(regions)) &
    (df_filtered['Category'].isin(categories)) &
    (df_filtered['Product'].isin(products))
]

# Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_filtered['Revenue'].sum()
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue:,.0f}",
        delta=f"{((total_revenue / df['Revenue'].sum()) - 1) * 100:.1f}%"
    )

with col2:
    total_orders = len(df_filtered)
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}",
        delta=f"{((total_orders / len(df)) - 1) * 100:.1f}%"
    )

with col3:
    avg_order_value = df_filtered['Revenue'].mean()
    st.metric(
        label="🛒 Avg Order Value",
        value=f"${avg_order_value:.2f}",
        delta=f"{((avg_order_value / df['Revenue'].mean()) - 1) * 100:.1f}%"
    )

with col4:
    unique_products = df_filtered['Product'].nunique()
    st.metric(
        label="📊 Products Sold",
        value=f"{unique_products}",
        delta=f"{unique_products - df['Product'].nunique()}"
    )

st.markdown("---")

# Revenue trends and analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trends Over Time")
    
    # Monthly revenue trend
    monthly_revenue = df_filtered.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
    monthly_revenue['Date'] = pd.to_datetime(monthly_revenue[['Year', 'Month']].assign(day=1))
    
    fig_trend = px.line(
        monthly_revenue, 
        x='Date', 
        y='Revenue',
        title="Monthly Revenue Trend",
        template="plotly_white"
    )
    fig_trend.update_traces(line_color='#1f77b4', line_width=3)
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("🎯 Revenue by Region")
    
    region_revenue = df_filtered.groupby('Region')['Revenue'].sum().reset_index()
    
    fig_region = px.pie(
        region_revenue,
        values='Revenue',
        names='Region',
        title="Revenue Distribution by Region",
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, use_container_width=True)

# Product performance analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top Performing Products")
    
    product_performance = df_filtered.groupby('Product').agg({
        'Revenue': 'sum',
        'Quantity': 'sum'
    }).reset_index().sort_values('Revenue', ascending=False)
    
    fig_products = px.bar(
        product_performance.head(8),
        x='Revenue',
        y='Product',
        orientation='h',
        title="Revenue by Product",
        template="plotly_white",
        color='Revenue',
        color_continuous_scale='Blues'
    )
    fig_products.update_layout(height=400)
    st.plotly_chart(fig_products, use_container_width=True)

with col2:
    st.subheader("👥 Sales Rep Performance")
    
    rep_performance = df_filtered.groupby('Sales_Rep').agg({
        'Revenue': 'sum',
        'Date': 'count'
    }).reset_index()
    rep_performance.columns = ['Sales_Rep', 'Revenue', 'Orders']
    rep_performance = rep_performance.sort_values('Revenue', ascending=False)
    
    fig_reps = px.scatter(
        rep_performance,
        x='Orders',
        y='Revenue',
        size='Revenue',
        hover_name='Sales_Rep',
        title="Sales Rep Performance (Revenue vs Orders)",
        template="plotly_white",
        color='Revenue',
        color_continuous_scale='Viridis'
    )
    fig_reps.update_layout(height=400)
    st.plotly_chart(fig_reps, use_container_width=True)

# Quarterly analysis
st.markdown("---")
st.subheader("📊 Quarterly Performance Analysis")

quarterly_data = df_filtered.groupby(['Year', 'Quarter']).agg({
    'Revenue': 'sum',
    'Quantity': 'sum',
    'Date': 'count'
}).reset_index()
quarterly_data.columns = ['Year', 'Quarter', 'Revenue', 'Quantity', 'Orders']
quarterly_data['Quarter_Label'] = quarterly_data['Year'].astype(str) + ' Q' + quarterly_data['Quarter'].astype(str)

col1, col2 = st.columns(2)

with col1:
    fig_quarterly = px.bar(
        quarterly_data,
        x='Quarter_Label',
        y='Revenue',
        title="Quarterly Revenue Comparison",
        template="plotly_white",
        color='Revenue',
        color_continuous_scale='Blues'
    )
    fig_quarterly.update_layout(height=400)
    st.plotly_chart(fig_quarterly, use_container_width=True)

with col2:
    # Growth rate calculation
    quarterly_data['Revenue_Growth'] = quarterly_data['Revenue'].pct_change() * 100
    
    fig_growth = px.line(
        quarterly_data,
        x='Quarter_Label',
        y='Revenue_Growth',
        title="Quarterly Revenue Growth Rate (%)",
        template="plotly_white",
        markers=True
    )
    fig_growth.update_traces(line_color='#ff7f0e', line_width=3)
    fig_growth.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.7)
    fig_growth.update_layout(height=400)
    st.plotly_chart(fig_growth, use_container_width=True)

# Data insights and summary
st.markdown("---")
st.subheader("📋 Key Performance Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Revenue Insights**")
    top_product = product_performance.iloc[0]['Product']
    top_region = region_revenue.loc[region_revenue['Revenue'].idxmax(), 'Region']
    st.write(f"🏆 **Top Product**: {top_product}")
    st.write(f"🌍 **Leading Region**: {top_region}")
    st.write(f"💰 **Avg Order Value**: ${avg_order_value:.2f}")

with col2:
    st.markdown("**Performance Statistics**")
    st.write(f"📊 **Total Records**: {len(df_filtered):,}")
    st.write(f"📈 **Revenue Growth**: {quarterly_data['Revenue_Growth'].mean():.1f}% avg")
    st.write(f"🎯 **Top Sales Rep**: {rep_performance.iloc[0]['Sales_Rep']}")

with col3:
    st.markdown("**Data Quality**")
    completeness = (1 - df_filtered.isnull().sum().sum() / (len(df_filtered) * len(df_filtered.columns))) * 100
    st.write(f"✅ **Data Completeness**: {completeness:.1f}%")
    st.write(f"📅 **Date Range**: {(df_filtered['Date'].max() - df_filtered['Date'].min()).days} days")
    st.write(f"🏢 **Geographic Coverage**: {df_filtered['Region'].nunique()} regions")

# Data export and download options
st.markdown("---")
st.subheader("📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    # Export filtered data
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="📊 Download Filtered Data (CSV)",
        data=csv,
        file_name=f"sales_data_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    # Export summary statistics
    summary_stats = df_filtered.describe()
    summary_csv = summary_stats.to_csv()
    st.download_button(
        label="📈 Download Summary Stats (CSV)",
        data=summary_csv,
        file_name=f"sales_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col3:
    # Show data sample
    if st.button("👀 Preview Raw Data"):
        st.write("**Sample Data (Latest 10 Records):**")
        st.dataframe(df_filtered.head(10))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <h4>📊 Sales Performance Dashboard</h4>
    <p>Built with Streamlit & Plotly | Professional Data Analytics Portfolio</p>
    <p><strong>Developer:</strong> Larismar Tati | <strong>Portfolio:</strong> 
    <a href="https://maize-panda-nzgf9k.mystrikingly.com" target="_blank">Data Analysis Portfolio</a></p>
    <p><em>Demonstrating advanced data visualization, business intelligence, and dashboard development skills</em></p>
</div>
""", unsafe_allow_html=True)

# Sidebar portfolio info
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 👨‍💻 About This Dashboard

This professional sales analytics dashboard demonstrates:

✅ **Interactive Data Visualization**
✅ **Business Intelligence Metrics**  
✅ **Real-time Filtering & Analysis**
✅ **Professional UI/UX Design**
✅ **Export & Download Capabilities**

**Tech Stack:**
- Python & Streamlit
- Plotly for visualizations
- Pandas for data analysis
- Responsive design

**Developer:** Larismar Tati  
**Location:** Luanda, Angola  
**LinkedIn:** [Connect with me](https://linkedin.com/in/larismar-bacana-32b227251)
""")

# Performance info
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
### ⚡ Dashboard Performance
- **Load Time**: Optimized for cloud
- **Data Points**: {len(df_filtered):,} records
- **Cache Status**: {'✅ Active' if st.cache_data else '❌ Inactive'}
- **Last Updated**: {datetime.now().strftime('%H:%M:%S')}
""")
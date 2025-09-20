# Sales Performance Dashboard

A comprehensive, interactive sales analytics dashboard built with Streamlit and Plotly. This project demonstrates advanced data visualization, business intelligence, and dashboard development skills.

**Live Demonstration:** [https://larissalesdashboard.streamlit.app/](https://larissalesdashboard.streamlit.app/)

## Project Overview

This dashboard provides real-time sales analytics with interactive filtering, trend analysis, and performance monitoring. It's designed to help business stakeholders make data-driven decisions through intuitive visualizations and comprehensive metrics.

## Key Features

### Analytics Capabilities
- **Real-time Sales Metrics**: Revenue, profit, margins, and growth rates
- **Interactive Filtering**: Date range, region, product, and sales rep filters
- **Trend Analysis**: Time series analysis with seasonality detection
- **Performance Monitoring**: KPI tracking with target comparisons
- **Customer Analytics**: Segmentation and behavior analysis

### Visualizations
- **Revenue Trends**: Line charts with seasonal patterns
- **Geographic Analysis**: Regional performance mapping
- **Product Performance**: Category and individual product analysis
- **Sales Rep Metrics**: Individual and team performance tracking
- **Customer Insights**: Satisfaction and retention metrics

### Technical Features
- **Responsive Design**: Works on desktop and mobile devices
- **Export Functionality**: Download data and reports as CSV
- **Interactive Elements**: Drill-down capabilities and hover details
- **Performance Optimized**: Cached data processing for fast loading
- **Professional UI**: Custom CSS styling with business theme

## Sample Data

The dashboard includes comprehensive sample data with:

### Main Dataset (sales_data.csv)
- **50,000+ transaction records** spanning 3 years (2022-2024)
- **Realistic business patterns** with seasonality and growth trends
- **Complete transaction details** including pricing, costs, and margins

### Supporting Datasets
- customer_summary.csv - Customer-level aggregated metrics
- product_performance.csv - Product category and item performance
- sales_rep_performance.csv - Sales representative metrics
- monthly_summary.csv - Time-based aggregated data

### Data Schema
```
Order_ID          - Unique transaction identifier
Date             - Transaction date (YYYY-MM-DD)
Customer_ID      - Customer identifier
Product          - Product name
Category         - Product category
Region           - Geographic region
Sales_Rep        - Sales representative name
Quantity         - Number of items sold
Unit_Price       - Price per unit
Revenue          - Gross revenue
Cost             - Product cost
Profit           - Gross profit
Profit_Margin    - Profit margin percentage
Discount_Percent - Discount applied (%)
Discount_Amount  - Discount value ($)
Final_Revenue    - Revenue after discounts
Final_Profit     - Profit after discounts
Final_Margin     - Final profit margin (%)
Shipping_Cost    - Shipping charges
Tax_Amount       - Tax amount
Customer_Satisfaction - Rating (1-5)
Delivery_Days    - Delivery time in days
Is_Returned      - Return status (True/False)
Year/Month/Quarter - Time dimensions
Day_of_Week      - Weekday name
Week_Number      - Week of year
```

## Installation & Setup

### Prerequisites
```bash
pip install streamlit pandas numpy plotly matplotlib seaborn
```

### Quick Start
1. Download all project files
2. Run the data generator to create sample data:
   ```bash
   python generate_sales_data.py
   ```
3. Launch the dashboard:
   ```bash
   streamlit run sales_dashboard.py
   ```
4. Open your browser to `http://localhost:8501`

### Project Structure
```
sales_dashboard/
├── sales_dashboard.py           # Main application
├── generate_sales_data.py       # Data generator script
├── data/
│   ├── sales_data.csv          # Main transaction data
│   ├── customer_summary.csv    # Customer metrics
│   ├── product_performance.csv # Product analytics
│   ├── sales_rep_performance.csv # Rep metrics
│   └── monthly_summary.csv     # Time-based data
├── assets/
│   └── dashboard_screenshot.png
└── README.md
```

## Dashboard Sections

### 1. Main Metrics Dashboard
- **Key Performance Indicators**: Revenue, orders, AOV, products sold
- **Real-time Filtering**: Dynamic updates based on user selections
- **Trend Indicators**: Growth rates and performance changes

### 2. Revenue Analysis
- **Time Series Analysis**: Monthly and quarterly revenue trends
- **Seasonal Patterns**: Holiday and seasonal impact visualization
- **Growth Tracking**: Year-over-year and period-over-period analysis

### 3. Geographic Performance
- **Regional Breakdown**: Revenue and profit by geographic region
- **Market Share Analysis**: Regional contribution to total performance
- **Geographic Trends**: Regional growth patterns and opportunities

### 4. Product Analytics
- **Category Performance**: Revenue and margin by product category
- **Individual Products**: Top and bottom performing items
- **Product Mix Analysis**: Quantity vs. revenue optimization

### 5. Sales Team Performance
- **Individual Metrics**: Revenue, orders, and customer satisfaction by rep
- **Team Comparisons**: Performance rankings and benchmarking
- **Customer Relationship**: Rep-customer interaction analysis

### 6. Customer Insights
- **Satisfaction Tracking**: Customer rating trends and drivers
- **Return Analysis**: Return rates and impact on profitability
- **Customer Behavior**: Order patterns and preferences

## Business Use Cases

### For Sales Managers
- **Performance Monitoring**: Track team and individual rep performance
- **Territory Analysis**: Optimize regional sales strategies
- **Goal Tracking**: Monitor progress against sales targets

### For Marketing Teams
- **Product Performance**: Identify best and worst performing products
- **Customer Segmentation**: Understand customer behavior patterns
- **Campaign Analysis**: Measure marketing campaign effectiveness

### For Executive Leadership
- **Strategic Overview**: High-level business performance metrics
- **Growth Analysis**: Trend identification and forecasting
- **Profit Optimization**: Margin analysis and improvement opportunities

### For Operations Teams
- **Inventory Planning**: Product demand and sales velocity analysis
- **Process Optimization**: Delivery and customer satisfaction metrics
- **Cost Management**: Shipping and operational cost analysis

## Customization Guide

### Adding Your Own Data
1. **Replace Sample Data**: Update CSV files with your actual sales data
2. **Schema Mapping**: Adjust column names in the app.py file
3. **Business Logic**: Modify calculations to match your business rules
4. **Visualizations**: Customize charts and metrics for your industry

### Styling Customization
```python
# Update CSS in the main app file
st.markdown("""
<style>
    .your-custom-class {
        background-color: #your-color;
        /* Add your styling */
    }
</style>
""", unsafe_allow_html=True)
```

### Adding New Features
- **Additional Metrics**: Extend the metrics calculation functions
- **New Visualizations**: Add charts using Plotly Express
- **Advanced Analytics**: Integrate forecasting or ML models
- **Export Options**: Add PDF or Excel export capabilities

## Key Metrics Explained

### Revenue Metrics
- **Gross Revenue**: Total sales before discounts
- **Net Revenue**: Revenue after discounts and returns
- **Revenue Growth**: Period-over-period growth percentage

### Profitability Metrics
- **Gross Profit**: Revenue minus product costs
- **Profit Margin**: Profit as percentage of revenue
- **Contribution Margin**: Profit excluding fixed costs

### Customer Metrics
- **Average Order Value (AOV)**: Revenue per transaction
- **Customer Satisfaction**: Average rating (1-5 scale)
- **Return Rate**: Percentage of orders returned

### Operational Metrics
- **Units Sold**: Total quantity of products sold
- **Delivery Performance**: Average delivery time
- **Discount Impact**: Effect of discounts on profitability

## Design Philosophy

### User Experience
- **Intuitive Navigation**: Clear visual hierarchy and logical flow
- **Interactive Elements**: Immediate feedback and responsive design
- **Performance Focus**: Fast loading with efficient data processing
- **Mobile Responsive**: Optimized for various screen sizes

### Business Value
- **Actionable Insights**: Focus on metrics that drive decisions
- **Real-time Updates**: Current data for timely decision making
- **Drill-down Capability**: Ability to investigate anomalies
- **Executive Summary**: High-level view for leadership

## Technical Implementation

### Data Processing
- **Pandas**: Efficient data manipulation and aggregation
- **NumPy**: Statistical calculations and data generation
- **Caching**: Streamlit caching for performance optimization

### Visualization
- **Plotly**: Interactive charts with hover details and zoom
- **Custom Styling**: Professional color schemes and layouts
- **Responsive Charts**: Adaptive sizing for different screens

### Performance
- **Data Caching**: Avoid recomputation on user interactions
- **Lazy Loading**: Load data only when needed
- **Efficient Queries**: Optimized data filtering and aggregation

 
## Deployment Options

### Streamlit Cloud (Recommended)
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with automatic updates

### Local Development
```bash
streamlit run sales_dashboard.py --server.port 8501
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "sales_dashboard.py"]
```

## Learning Resources

### Documentation
- [Streamlit API Reference](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/)

### Business Intelligence Concepts
- KPI Design and Implementation
- Dashboard Best Practices
- Data Visualization Principles

## Contributing

Feel free to fork this project and adapt it for your own portfolio. Consider:
- Adding industry-specific metrics
- Implementing advanced analytics features
- Creating custom visualization components
- Optimizing for specific business use cases

## Support

For questions about implementation or customization:
1. Review the code comments for detailed explanations
2. Check the Streamlit documentation for component usage
3. Test with the provided sample data before using your own

## Live Demo

Experience the dashboard functionality at: [https://larissalesdashboard.streamlit.app/](https://larissalesdashboard.streamlit.app/)

The live demonstration showcases all features including interactive filtering, real-time analytics, and professional visualization capabilities.

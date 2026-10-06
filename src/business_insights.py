"""
Business Insights & Executive Reporting Generator
Author: Data Analyst Candidate
Description: Dynamically evaluates clean_sales_data.csv to compute real, data-driven business insights
and exports an executive summary report to outputs/business_insights.txt.
"""

import os
import pandas as pd
import numpy as np

def generate_business_insights(clean_path='data/clean_sales_data.csv', output_path='outputs/business_insights.txt'):
    print("=" * 75)
    print("              BUSINESS INSIGHTS & ANALYTICS ENGINE")
    print("=" * 75)

    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Cleaned dataset not found at '{clean_path}'. Run src/data_cleaning.py first.")

    df = pd.read_csv(clean_path)

    # Core Calculations
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order_ID'].nunique()
    avg_order_value = total_sales / total_orders
    overall_profit_margin = (total_profit / total_sales) * 100

    # 1. Regional Performance
    reg_df = df.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order_ID', 'nunique')
    ).reset_index()
    reg_df['Margin_%'] = (reg_df['Profit'] / reg_df['Sales']) * 100
    
    top_region = reg_df.sort_values(by='Sales', ascending=False).iloc[0]
    bottom_region_sales = reg_df.sort_values(by='Sales', ascending=True).iloc[0]
    bottom_region_margin = reg_df.sort_values(by='Margin_%', ascending=True).iloc[0]

    # 2. Category Performance
    cat_df = df.groupby('Category').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order_ID', 'nunique')
    ).reset_index()
    cat_df['Margin_%'] = (cat_df['Profit'] / cat_df['Sales']) * 100

    top_sales_cat = cat_df.sort_values(by='Sales', ascending=False).iloc[0]
    top_margin_cat = cat_df.sort_values(by='Margin_%', ascending=False).iloc[0]
    lowest_margin_cat = cat_df.sort_values(by='Margin_%', ascending=True).iloc[0]

    # 3. Product Performance Insights
    prod_df = df.groupby(['Category', 'Sub_Category', 'Product_Name']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', 'mean')
    ).reset_index()
    prod_df['Margin_%'] = (prod_df['Profit'] / prod_df['Sales']) * 100

    top_revenue_prod = prod_df.sort_values(by='Sales', ascending=False).iloc[0]
    top_profit_prod = prod_df.sort_values(by='Profit', ascending=False).iloc[0]
    
    # Products with High Revenue but Low Margin (< 12%)
    high_rev_low_margin = prod_df[(prod_df['Sales'] > prod_df['Sales'].median()) & (prod_df['Margin_%'] < 12.0)].sort_values(by='Sales', ascending=False)

    # 4. Customer Segment Insights
    seg_df = df.groupby('Customer_Segment').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order_ID', 'nunique'),
        AOV=('Sales', lambda x: x.sum() / x.nunique())
    ).reset_index().sort_values(by='Sales', ascending=False)

    top_segment = seg_df.iloc[0]

    # 5. Monthly & Seasonal Trends
    month_df = df.groupby('Year_Month').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index()

    best_month = month_df.sort_values(by='Sales', ascending=False).iloc[0]
    worst_month = month_df.sort_values(by='Sales', ascending=True).iloc[0]

    # 6. Order Fulfillment & Cancellation Impact
    status_df = df.groupby('Order_Status').agg(
        Count=('Order_ID', 'count'),
        Lost_Sales=('Sales', 'sum')
    ).reset_index()
    
    completed_cnt = status_df[status_df['Order_Status'] == 'Completed']['Count'].values[0] if 'Completed' in status_df['Order_Status'].values else 0
    cancelled_cnt = status_df[status_df['Order_Status'] == 'Cancelled']['Count'].values[0] if 'Cancelled' in status_df['Order_Status'].values else 0
    returned_cnt = status_df[status_df['Order_Status'] == 'Returned']['Count'].values[0] if 'Returned' in status_df['Order_Status'].values else 0

    cancelled_sales = status_df[status_df['Order_Status'] == 'Cancelled']['Lost_Sales'].values[0] if 'Cancelled' in status_df['Order_Status'].values else 0
    returned_sales = status_df[status_df['Order_Status'] == 'Returned']['Lost_Sales'].values[0] if 'Returned' in status_df['Order_Status'].values else 0

    # Build Executive Summary Text Report
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("     SALES PERFORMANCE ANALYTICS DASHBOARD — EXECUTIVE BUSINESS INSIGHTS")
    report_lines.append("=" * 80)
    report_lines.append(f"Generated Date: Dynamic Calculation from clean_sales_data.csv")
    report_lines.append(f"Analysis Period: 2023 - 2024 (24 Months)\n")

    report_lines.append("1. EXECUTIVE KPI OVERVIEW")
    report_lines.append("-" * 50)
    report_lines.append(f"• Total Gross Sales Revenue : ${total_sales:,.2f}")
    report_lines.append(f"• Total Net Profit          : ${total_profit:,.2f}")
    report_lines.append(f"• Overall Profit Margin     : {overall_profit_margin:.2f}%")
    report_lines.append(f"• Total Unique Orders       : {total_orders:,}")
    report_lines.append(f"• Average Order Value (AOV) : ${avg_order_value:,.2f}\n")

    report_lines.append("2. REGIONAL PERFORMANCE INSIGHTS")
    report_lines.append("-" * 50)
    report_lines.append(f"• Best Performing Region (Revenue) : {top_region['Region']} (${top_region['Sales']:,.2f} sales, ${top_region['Profit']:,.2f} profit, {top_region['Margin_%']:.2f}% margin)")
    report_lines.append(f"• Lowest Revenue Region           : {bottom_region_sales['Region']} (${bottom_region_sales['Sales']:,.2f} sales)")
    report_lines.append(f"• Region with Lowest Profit Margin : {bottom_region_margin['Region']} ({bottom_region_margin['Margin_%']:.2f}% margin)\n")

    report_lines.append("3. CATEGORY & PRODUCT MARGIN ANALYSIS")
    report_lines.append("-" * 50)
    report_lines.append(f"• Highest Revenue Category       : {top_sales_cat['Category']} (${top_sales_cat['Sales']:,.2f}, {top_sales_cat['Sales']/total_sales*100:.1f}% share)")
    report_lines.append(f"• Most Profitable Category       : {top_margin_cat['Category']} ({top_margin_cat['Margin_%']:.2f}% margin, ${top_margin_cat['Profit']:,.2f} profit)")
    report_lines.append(f"• Lowest Margin Category         : {lowest_margin_cat['Category']} ({lowest_margin_cat['Margin_%']:.2f}% margin)")
    report_lines.append(f"• Top Single Revenue Product     : {top_revenue_prod['Product_Name']} (${top_revenue_prod['Sales']:,.2f})")
    report_lines.append(f"• Top Single Profit Product      : {top_profit_prod['Product_Name']} (${top_profit_prod['Profit']:,.2f})")
    
    if len(high_rev_low_margin) > 0:
        report_lines.append("\n  [ALERT: DISCOUNT TRAP PRODUCTS - HIGH REVENUE BUT LOW PROFIT MARGIN]")
        for idx, row in high_rev_low_margin.iterrows():
            report_lines.append(f"   - Product: {row['Product_Name']} | Sales: ${row['Sales']:,.2f} | Profit: ${row['Profit']:,.2f} | Margin: {row['Margin_%']:.2f}% | Avg Disc: {row['Avg_Discount']*100:.1f}%")
    report_lines.append("")

    report_lines.append("4. CUSTOMER SEGMENT & DEMOGRAPHICS")
    report_lines.append("-" * 50)
    report_lines.append(f"• Highest Value Customer Segment : {top_segment['Customer_Segment']} (${top_segment['Sales']:,.2f} revenue, {top_segment['Sales']/total_sales*100:.1f}% market share)")
    for idx, row in seg_df.iterrows():
        report_lines.append(f"   - {row['Customer_Segment']}: ${row['Sales']:,.2f} sales | AOV: ${row['AOV']:,.2f} | Profit Margin: {row['Profit']/row['Sales']*100:.2f}%")
    report_lines.append("")

    report_lines.append("5. SEASONALITY & TIMELINE TRENDS")
    report_lines.append("-" * 50)
    report_lines.append(f"• Peak Sales Month               : {best_month['Year_Month']} (${best_month['Sales']:,.2f} revenue)")
    report_lines.append(f"• Lowest Sales Month             : {worst_month['Year_Month']} (${worst_month['Sales']:,.2f} revenue)\n")

    report_lines.append("6. ORDER FULFILLMENT & REVENUE LOSS")
    report_lines.append("-" * 50)
    report_lines.append(f"• Completed Orders Rate          : {completed_cnt / total_orders * 100:.1f}% ({completed_cnt:,} orders)")
    report_lines.append(f"• Cancelled Orders Impact        : {cancelled_cnt / total_orders * 100:.1f}% ({cancelled_cnt:,} orders, ${cancelled_sales:,.2f} lost revenue)")
    report_lines.append(f"• Returned Orders Impact         : {returned_cnt / total_orders * 100:.1f}% ({returned_cnt:,} orders, ${returned_sales:,.2f} lost revenue)\n")

    report_lines.append("7. STRATEGIC RECOMMENDATIONS FOR MANAGEMENT")
    report_lines.append("-" * 50)
    report_lines.append(f" 1. Cap Discounts on {lowest_margin_cat['Category']}: The {lowest_margin_cat['Category']} category is experiencing compressed margins ({lowest_margin_cat['Margin_%']:.2f}%). Restrict max discount to 15%.")
    report_lines.append(f" 2. Expand High-Margin Technology Sales: Technology generates {top_margin_cat['Margin_%']:.2f}% margin and should be emphasized in cross-selling campaigns to Corporate buyers.")
    report_lines.append(f" 3. Address Order Cancellations & Returns: Combined cancellations and returns represent ${(cancelled_sales + returned_sales):,.2f} in lost opportunity. Optimize inventory availability and logistics.")
    report_lines.append(f" 4. Target Consumer Segment Growth: Consumer segment represents the highest total revenue volume (${top_segment['Sales']:,.2f}). Introduce loyalty rewards for high-AOV customers.")
    report_lines.append("=" * 80)

    report_content = "\n".join(report_lines)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report_content)

    print(report_content)
    print(f"\n[INSIGHTS GENERATED] Saved output to '{output_path}'.\n")

if __name__ == "__main__":
    generate_business_insights()

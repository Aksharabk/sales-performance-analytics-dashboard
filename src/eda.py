"""
Exploratory Data Analysis (EDA) Script for Sales Performance Analytics Dashboard
Author: Data Analyst Candidate
Description: Performs comprehensive statistical analysis and data visualizations on clean_sales_data.csv.
Saves high-quality PNG charts in outputs/charts/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual styling for charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.labelsize'] = 11

COLORS = {
    'primary': '#1e3a8a',      # Deep navy blue
    'secondary': '#0284c7',    # Bright blue
    'accent': '#0d9488',       # Teal
    'success': '#16a34a',      # Green
    'warning': '#d97706',      # Amber
    'danger': '#dc2626',       # Red
    'neutral': '#64748b'       # Slate gray
}

PALETTE = ['#1e3a8a', '#0284c7', '#0d9488', '#16a34a', '#d97706', '#dc2626', '#8b5cf6']

def run_eda(clean_path='data/clean_sales_data.csv', output_dir='outputs/charts'):
    print("=" * 75)
    print("               EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 75)

    if not os.path.exists(clean_path):
        raise FileNotFoundError(f"Cleaned dataset not found at '{clean_path}'. Run src/data_cleaning.py first.")
    
    df = pd.read_csv(clean_path)
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------
    # 1. CORE EXECUTIVE METRICS
    # -------------------------------------------------------------
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order_ID'].nunique()
    total_quantity = df['Quantity'].sum()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    overall_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    completed_orders = (df['Order_Status'] == 'Completed').sum()
    cancelled_orders = (df['Order_Status'] == 'Cancelled').sum()
    returned_orders = (df['Order_Status'] == 'Returned').sum()

    print("\n[EXECUTIVE KPI SUMMARY]")
    print(f" Total Revenue (Sales)    : ${total_sales:,.2f}")
    print(f" Total Net Profit         : ${total_profit:,.2f}")
    print(f" Total Unique Orders      : {total_orders:,}")
    print(f" Total Units Sold         : {total_quantity:,}")
    print(f" Average Order Value (AOV): ${avg_order_value:,.2f}")
    print(f" Overall Profit Margin    : {overall_profit_margin:.2f}%")
    print(f" Completed Orders         : {completed_orders:,} ({completed_orders/len(df)*100:.1f}%)")
    print(f" Cancelled Orders         : {cancelled_orders:,} ({cancelled_orders/len(df)*100:.1f}%)")
    print(f" Returned Orders          : {returned_orders:,} ({returned_orders/len(df)*100:.1f}%)")

    # -------------------------------------------------------------
    # 2. SEGMENT & REGIONAL ANALYSIS
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("SALES & PROFIT BY REGION")
    print("-" * 55)
    region_summary = df.groupby('Region').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Orders=('Order_ID', 'nunique'),
        Avg_Order_Value=('Sales', lambda x: x.sum() / x.nunique() if x.nunique() > 0 else 0)
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    region_summary['Profit_Margin_%'] = (region_summary['Total_Profit'] / region_summary['Total_Sales'] * 100).round(2)
    print(region_summary.to_string(index=False))

    print("\n" + "-" * 55)
    print("SALES BY CUSTOMER SEGMENT")
    print("-" * 55)
    segment_summary = df.groupby('Customer_Segment').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Orders=('Order_ID', 'nunique')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    segment_summary['Profit_Margin_%'] = (segment_summary['Total_Profit'] / segment_summary['Total_Sales'] * 100).round(2)
    print(segment_summary.to_string(index=False))

    # -------------------------------------------------------------
    # 3. CATEGORY & PRODUCT ANALYSIS
    # -------------------------------------------------------------
    print("\n" + "-" * 55)
    print("SALES & PROFIT BY CATEGORY")
    print("-" * 55)
    cat_summary = df.groupby('Category').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Orders=('Order_ID', 'nunique')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    cat_summary['Profit_Margin_%'] = (cat_summary['Total_Profit'] / cat_summary['Total_Sales'] * 100).round(2)
    print(cat_summary.to_string(index=False))

    # Top 10 & Bottom 10 Products
    top_10_sales = df.groupby('Product_Name')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
    top_10_profit = df.groupby('Product_Name')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=False).head(10)
    bottom_10_profit = df.groupby('Product_Name')['Profit'].sum().reset_index().sort_values(by='Profit', ascending=True).head(10)

    print("\nTOP 5 REVENUE GENERATING PRODUCTS:")
    for idx, row in top_10_sales.head(5).iterrows():
        print(f" - {row['Product_Name']}: ${row['Sales']:,.2f}")

    print("\nTOP 5 MOST PROFITABLE PRODUCTS:")
    for idx, row in top_10_profit.head(5).iterrows():
        print(f" - {row['Product_Name']}: ${row['Profit']:,.2f}")

    print("\nLEAST PROFITABLE / LOSS-MAKING PRODUCTS:")
    for idx, row in bottom_10_profit.head(5).iterrows():
        print(f" - {row['Product_Name']}: ${row['Profit']:,.2f}")

    # -------------------------------------------------------------
    # 4. CHART GENERATION
    # -------------------------------------------------------------
    print("\n" + "=" * 75)
    print("GENERATING VISUAL CHARTS (PNG)...")
    print("=" * 75)

    # Chart 1: Sales & Profit by Region
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(region_summary))
    width = 0.35
    rects1 = ax.bar(x - width/2, region_summary['Total_Sales'], width, label='Sales ($)', color=COLORS['primary'])
    rects2 = ax.bar(x + width/2, region_summary['Total_Profit'], width, label='Profit ($)', color=COLORS['secondary'])
    ax.set_title('Total Sales & Profit by Region', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(region_summary['Region'])
    ax.legend()
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, 'sales_by_region.png')
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f" Saved: {chart1_path}")

    # Chart 2: Sales & Profit by Category
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(cat_summary))
    rects1 = ax.bar(x - width/2, cat_summary['Total_Sales'], width, label='Sales ($)', color=COLORS['primary'])
    rects2 = ax.bar(x + width/2, cat_summary['Total_Profit'], width, label='Profit ($)', color=COLORS['accent'])
    ax.set_title('Sales vs Profit by Product Category', fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(cat_summary['Category'])
    ax.legend()
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, 'sales_by_category.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f" Saved: {chart2_path}")

    # Chart 3: Monthly Sales & Profit Trend
    monthly_df = df.groupby('Year_Month').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Year_Month')

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(monthly_df['Year_Month'], monthly_df['Sales'], marker='o', color=COLORS['primary'], linewidth=2.5, label='Sales ($)')
    ax1.plot(monthly_df['Year_Month'], monthly_df['Profit'], marker='s', color=COLORS['success'], linewidth=2.5, label='Profit ($)')
    ax1.set_title('Monthly Revenue & Profit Performance (2023 - 2024)', fontweight='bold', pad=15)
    ax1.set_xlabel('Year-Month')
    ax1.set_ylabel('Amount ($)')
    ax1.yaxis.set_major_formatter('${x:,.0f}')
    plt.xticks(rotation=45)
    ax1.legend(loc='upper left')
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, 'monthly_sales_trend.png')
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f" Saved: {chart3_path}")

    # Chart 4: Top 10 Products by Revenue
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_10_sales, y='Product_Name', x='Sales', palette='Blues_r', ax=ax)
    ax.set_title('Top 10 Products by Total Revenue', fontweight='bold', pad=15)
    ax.set_xlabel('Total Revenue ($)')
    ax.set_ylabel('Product Name')
    ax.xaxis.set_major_formatter('${x:,.0f}')
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, 'top_10_products.png')
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f" Saved: {chart4_path}")

    # Chart 5: Customer Segment Sales Distribution (Donut Chart)
    fig, ax = plt.subplots(figsize=(7, 7))
    colors_list = ['#1e3a8a', '#0284c7', '#0d9488']
    wedges, texts, autotexts = ax.pie(
        segment_summary['Total_Sales'], 
        labels=segment_summary['Customer_Segment'],
        autopct='%1.1f%%',
        startangle=140,
        colors=colors_list,
        wedgeprops=dict(width=0.4, edgecolor='w')
    )
    plt.setp(autotexts, size=11, weight="bold", color="white")
    ax.set_title('Revenue Share by Customer Segment', fontweight='bold', pad=15)
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, 'customer_segment_sales.png')
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f" Saved: {chart5_path}")

    # Chart 6: Category Profitability Margin %
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cat_summary, x='Category', y='Profit_Margin_%', palette='Greens_r', ax=ax)
    ax.set_title('Profit Margin (%) by Product Category', fontweight='bold', pad=15)
    ax.set_ylabel('Profit Margin (%)')
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points', fontweight='bold')
    plt.tight_layout()
    chart6_path = os.path.join(output_dir, 'category_profitability.png')
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f" Saved: {chart6_path}")

    # Chart 7: Sub-Category Sales vs Profit
    subcat_summary = df.groupby(['Category', 'Sub_Category']).agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Sales', ascending=False)

    fig, ax = plt.subplots(figsize=(11, 6))
    sns.scatterplot(data=subcat_summary, x='Sales', y='Profit', hue='Category', s=200, palette=['#1e3a8a', '#0284c7', '#0d9488'], ax=ax)
    ax.set_title('Sales vs. Profit by Sub-Category', fontweight='bold', pad=15)
    ax.set_xlabel('Total Sales ($)')
    ax.set_ylabel('Total Profit ($)')
    ax.xaxis.set_major_formatter('${x:,.0f}')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    
    # Annotate points
    for idx, row in subcat_summary.iterrows():
        ax.annotate(row['Sub_Category'], (row['Sales'], row['Profit']), xytext=(5, 5), textcoords='offset points', fontsize=9)
    plt.tight_layout()
    chart7_path = os.path.join(output_dir, 'sales_vs_profit.png')
    plt.savefig(chart7_path, dpi=300)
    plt.close()
    print(f" Saved: {chart7_path}")

    # Chart 8: Payment Mode Distribution
    pay_summary = df.groupby('Payment_Mode').agg(
        Total_Sales=('Sales', 'sum'),
        Transaction_Count=('Order_ID', 'count')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=pay_summary, x='Payment_Mode', y='Total_Sales', palette='Blues_r', ax=ax)
    ax.set_title('Sales Revenue by Payment Mode', fontweight='bold', pad=15)
    ax.set_xlabel('Payment Mode')
    ax.set_ylabel('Total Revenue ($)')
    ax.yaxis.set_major_formatter('${x:,.0f}')
    plt.tight_layout()
    chart8_path = os.path.join(output_dir, 'payment_mode_distribution.png')
    plt.savefig(chart8_path, dpi=300)
    plt.close()
    print(f" Saved: {chart8_path}")

    print("\n[EDA COMPLETE] All charts successfully generated in 'outputs/charts/'.\n")

if __name__ == "__main__":
    run_eda()

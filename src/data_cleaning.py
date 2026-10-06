"""
Data Cleaning & Preprocessing Script for Sales Performance Analytics Dashboard
Author: Data Analyst Candidate
Description: Loads raw sales data, cleans data quality anomalies, handles missing values,
parses dates, validates numeric consistency, engineers derived features, and outputs clean CSV.
"""

import os
import pandas as pd
import numpy as np

def clean_sales_data(raw_path='data/raw_sales_data.csv', clean_path='data/clean_sales_data.csv'):
    print("=" * 70)
    print("                SALES DATA CLEANING & PREPROCESSING")
    print("=" * 70)

    # 1. Load Raw Dataset
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at '{raw_path}'. Run src/generate_data.py first.")
    
    df = pd.read_csv(raw_path)

    # 2. Display Initial Statistics
    initial_shape = df.shape
    print(f"\n1. INITIAL DATASET SHAPE: {initial_shape[0]} rows, {initial_shape[1]} columns")
    
    print("\n2. COLUMN NAMES & DATA TYPES:")
    print(df.dtypes)

    # 3. Missing Values Summary (BEFORE)
    print("\n3. MISSING VALUES SUMMARY (BEFORE CLEANING):")
    missing_before = df.isnull().sum()
    print(missing_before[missing_before > 0] if missing_before.sum() > 0 else "No missing values found.")

    # 4. Duplicate Records (BEFORE)
    duplicates_count = df.duplicated().sum()
    print(f"\n4. DUPLICATE RECORDS IDENTIFIED: {duplicates_count}")

    # 5. Remove Duplicates
    if duplicates_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print(f"   --> Removed {duplicates_count} duplicate rows.")

    # 6. Handle Missing Values
    print("\n5. HANDLING MISSING VALUES:")
    if 'Customer_Name' in df.columns:
        df['Customer_Name'] = df['Customer_Name'].fillna('Unknown Customer')
    if 'City' in df.columns:
        df['City'] = df['City'].fillna('Unknown City')
    if 'Payment_Mode' in df.columns:
        mode_payment = df['Payment_Mode'].mode()[0]
        df['Payment_Mode'] = df['Payment_Mode'].fillna(mode_payment)
        print(f"   --> Imputed missing Payment_Mode with mode value: '{mode_payment}'")

    missing_after = df.isnull().sum().sum()
    print(f"   --> Remaining missing values after imputation: {missing_after}")

    # 7. Standardize Order_Date to Datetime
    print("\n6. CONVERTING ORDER_DATE TO DATETIME:")
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], format='mixed', errors='coerce')
    
    # Check for unparseable dates
    nat_dates = df['Order_Date'].isnull().sum()
    if nat_dates > 0:
        print(f"   --> Warning: {nat_dates} dates could not be parsed. Dropping rows with NaT dates.")
        df = df.dropna(subset=['Order_Date']).reset_index(drop=True)
    else:
        print("   --> All dates successfully converted to standard datetime format.")

    # Sort dataset chronologically by Order_Date
    df = df.sort_values(by='Order_Date').reset_index(drop=True)

    # 8. Numeric Column Validation & Calculation Consistency
    print("\n7. NUMERIC COLUMN VALIDATION:")
    df['Quantity'] = df['Quantity'].apply(lambda x: max(1, int(x)) if pd.notnull(x) else 1)
    df['Unit_Price'] = df['Unit_Price'].apply(lambda x: abs(float(x)) if pd.notnull(x) else 0.0)
    df['Discount'] = df['Discount'].clip(lower=0.0, upper=1.0)

    # Re-calculate Sales to ensure strict mathematical integrity
    df['Sales'] = (df['Quantity'] * df['Unit_Price'] * (1.0 - df['Discount'])).round(2)

    # Re-verify Profit calculation
    df['Profit'] = df['Profit'].round(2)

    # 9. Derive New Feature Columns for BI & Analytics
    print("\n8. FEATURE ENGINEERING (DERIVED COLUMNS):")
    df['Year'] = df['Order_Date'].dt.year
    df['Month_Num'] = df['Order_Date'].dt.month
    df['Month_Name'] = df['Order_Date'].dt.strftime('%B')
    df['Year_Month'] = df['Order_Date'].dt.strftime('%Y-%m')
    df['Quarter'] = 'Q' + df['Order_Date'].dt.quarter.astype(str)
    df['Day_of_Week'] = df['Order_Date'].dt.strftime('%A')
    
    # Profit Margin Percentage
    df['Profit_Margin_%'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales'] * 100).round(2), 0.0)

    # Net Sales & Profit (accounting for Completed vs Cancelled/Returned)
    df['Net_Sales'] = np.where(df['Order_Status'] == 'Completed', df['Sales'], 0.0)
    df['Net_Profit'] = np.where(df['Order_Status'] == 'Completed', df['Profit'], 0.0)

    # Convert Order_Date back to YYYY-MM-DD string for clean CSV output & SQL import compatibility
    df['Order_Date'] = df['Order_Date'].dt.strftime('%Y-%m-%d')

    # 10. Save Cleaned Dataset
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)

    # 11. Final Before/After Summary
    final_shape = df.shape
    print("\n" + "=" * 70)
    print("                    DATA CLEANING SUMMARY REPORT")
    print("=" * 70)
    print(f" Initial Row Count      : {initial_shape[0]}")
    print(f" Duplicates Removed     : {duplicates_count}")
    print(f" Final Clean Row Count  : {final_shape[0]}")
    print(f" Total Columns          : {final_shape[1]}")
    print(f" Missing Values Count   : {df.isnull().sum().sum()}")
    print(f" Clean Dataset Saved To : '{clean_path}'")
    print("=" * 70 + "\n")

    return df

if __name__ == "__main__":
    clean_sales_data()

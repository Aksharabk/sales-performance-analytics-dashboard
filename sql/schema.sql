-- =============================================================================
-- Database Schema Definition for Sales Performance Analytics Dashboard
-- Target RDBMS: MySQL 8.0+ / PostgreSQL compatible syntax
-- Author: Data Analyst Candidate
-- Description: Creates database 'sales_analytics' and table 'sales_data' with optimized indexes.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

-- Drop table if re-initializing schema
DROP TABLE IF EXISTS sales_data;

CREATE TABLE sales_data (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID VARCHAR(50) NOT NULL,
    Order_Date DATE NOT NULL,
    Customer_ID VARCHAR(50) NOT NULL,
    Customer_Name VARCHAR(100) DEFAULT 'Unknown Customer',
    Customer_Segment VARCHAR(50) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    City VARCHAR(50) DEFAULT 'Unknown City',
    Category VARCHAR(50) NOT NULL,
    Sub_Category VARCHAR(50) NOT NULL,
    Product_ID VARCHAR(50) NOT NULL,
    Product_Name VARCHAR(150) NOT NULL,
    Quantity INT NOT NULL DEFAULT 1,
    Unit_Price DECIMAL(10, 2) NOT NULL,
    Sales DECIMAL(12, 2) NOT NULL,
    Discount DECIMAL(5, 4) NOT NULL DEFAULT 0.00,
    Profit DECIMAL(12, 2) NOT NULL,
    Payment_Mode VARCHAR(50) DEFAULT 'Credit Card',
    Order_Status VARCHAR(50) NOT NULL DEFAULT 'Completed',
    `Year` INT NOT NULL,
    `Month_Num` INT NOT NULL,
    `Month_Name` VARCHAR(20) NOT NULL,
    `Year_Month` VARCHAR(10) NOT NULL,
    `Quarter` VARCHAR(5) NOT NULL,
    `Day_of_Week` VARCHAR(15) NOT NULL,
    `Profit_Margin_Pct` DECIMAL(7, 2) NOT NULL,
    `Net_Sales` DECIMAL(12, 2) NOT NULL,
    `Net_Profit` DECIMAL(12, 2) NOT NULL,
    
    -- Indexes for high-performance querying
    INDEX idx_order_date (Order_Date),
    INDEX idx_region (Region),
    INDEX idx_category (Category),
    INDEX idx_segment (Customer_Segment),
    INDEX idx_product (Product_ID),
    INDEX idx_order_status (Order_Status),
    INDEX idx_year_month (`Year_Month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================================================
-- DATA IMPORT INSTRUCTIONS FOR MYSQL CLI:
-- =============================================================================
/*
LOAD DATA INFILE '/path/to/data/clean_sales_data.csv'
INTO TABLE sales_data
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(Order_ID, Order_Date, Customer_ID, Customer_Name, Customer_Segment, Region, State, City, 
 Category, Sub_Category, Product_ID, Product_Name, Quantity, Unit_Price, Sales, Discount, 
 Profit, Payment_Mode, Order_Status, Year, Month_Num, Month_Name, Year_Month, Quarter, 
 Day_of_Week, Profit_Margin_Pct, Net_Sales, Net_Profit);
*/

-- =============================================================================
-- SQL Analytical Queries for Sales Performance Analytics Dashboard
-- Target Database: MySQL 8.0+ / PostgreSQL
-- Author: Data Analyst Candidate
-- Description: 20 comprehensive business queries covering core KPIs, aggregations,
-- ranking, loss identification, segment analysis, and window function growth metrics.
-- =============================================================================

USE sales_analytics;

-- -----------------------------------------------------------------------------
-- QUERY 1: TOTAL SALES (GROSS REVENUE)
-- Description: Calculates total sales across all orders.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(Sales), 2) AS Total_Sales_Revenue
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 2: TOTAL NET PROFIT
-- Description: Calculates total profit accumulated across all orders.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(Profit), 2) AS Total_Net_Profit
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 3: TOTAL UNIQUE ORDERS COUNT
-- Description: Counts total distinct orders processed in the system.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT Order_ID) AS Total_Orders_Count
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 4: TOTAL QUANTITY SOLD
-- Description: Sums the total units of items sold across all transactions.
-- -----------------------------------------------------------------------------
SELECT 
    SUM(Quantity) AS Total_Quantity_Sold
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 5: AVERAGE ORDER VALUE (AOV)
-- Description: Measures average revenue generated per unique transaction order.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Average_Order_Value
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 6: OVERALL PROFIT MARGIN PERCENTAGE
-- Description: Evaluates total net profit as a percentage of total sales.
-- -----------------------------------------------------------------------------
SELECT 
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Overall_Profit_Margin_Pct
FROM sales_data;


-- -----------------------------------------------------------------------------
-- QUERY 7: MONTHLY SALES & PROFIT TREND
-- Description: Aggregates total sales, net profit, and order count by Month.
-- -----------------------------------------------------------------------------
SELECT 
    `Year_Month`,
    COUNT(DISTINCT Order_ID) AS Monthly_Orders,
    ROUND(SUM(Sales), 2) AS Monthly_Sales,
    ROUND(SUM(Profit), 2) AS Monthly_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Monthly_Margin_Pct
FROM sales_data
GROUP BY `Year_Month`
ORDER BY `Year_Month` ASC;


-- -----------------------------------------------------------------------------
-- QUERY 8: YEARLY SALES & PROFIT BREAKDOWN
-- Description: Compares annual performance between 2023 and 2024.
-- -----------------------------------------------------------------------------
SELECT 
    Year,
    COUNT(DISTINCT Order_ID) AS Annual_Orders,
    ROUND(SUM(Sales), 2) AS Annual_Sales,
    ROUND(SUM(Profit), 2) AS Annual_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Annual_Margin_Pct
FROM sales_data
GROUP BY Year
ORDER BY Year ASC;


-- -----------------------------------------------------------------------------
-- QUERY 9: REGIONAL SALES & PROFIT PERFORMANCE
-- Description: Groups sales and profit by geographical Region.
-- -----------------------------------------------------------------------------
SELECT 
    Region,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Regional_Sales,
    ROUND(SUM(Profit), 2) AS Regional_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Region
ORDER BY Regional_Sales DESC;


-- -----------------------------------------------------------------------------
-- QUERY 10: CATEGORY SALES PERFORMANCE
-- Description: Ranks product categories by overall revenue contribution.
-- -----------------------------------------------------------------------------
SELECT 
    Category,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Category_Sales,
    ROUND(SUM(Profit), 2) AS Category_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Category
ORDER BY Category_Sales DESC;


-- -----------------------------------------------------------------------------
-- QUERY 11: SUB-CATEGORY BREAKDOWN BY CATEGORY
-- Description: Granular view of sub-categories under main product categories.
-- -----------------------------------------------------------------------------
SELECT 
    Category,
    Sub_Category,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(SUM(Sales), 2) AS SubCategory_Sales,
    ROUND(SUM(Profit), 2) AS SubCategory_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Category, Sub_Category
ORDER BY Category ASC, SubCategory_Sales DESC;


-- -----------------------------------------------------------------------------
-- QUERY 12: TOP 10 PRODUCTS BY REVENUE
-- Description: Identifies top 10 products bringing in the highest sales volume.
-- -----------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    SUM(Quantity) AS Total_Units_Sold,
    ROUND(SUM(Sales), 2) AS Total_Revenue,
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales_data
GROUP BY Product_ID, Product_Name, Category
ORDER BY Total_Revenue DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 13: TOP 10 CUSTOMERS BY TOTAL SPEND
-- Description: Ranks customers by cumulative purchase amount.
-- -----------------------------------------------------------------------------
SELECT 
    Customer_ID,
    Customer_Name,
    Customer_Segment,
    COUNT(DISTINCT Order_ID) AS Order_Frequency,
    ROUND(SUM(Sales), 2) AS Total_Spent,
    ROUND(SUM(Profit), 2) AS Profit_Generated
FROM sales_data
GROUP BY Customer_ID, Customer_Name, Customer_Segment
ORDER BY Total_Spent DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 14: MOST PROFITABLE PRODUCTS
-- Description: Highlights products generating the highest net profit.
-- -----------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Margin_Pct
FROM sales_data
GROUP BY Product_ID, Product_Name, Category
ORDER BY Profit DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- QUERY 15: PRODUCTS WITH NEGATIVE OR LOW PROFIT MARGIN (DISCOUNT TRAP)
-- Description: Identifies products with profit margin under 10% or negative profit.
-- -----------------------------------------------------------------------------
SELECT 
    Product_ID,
    Product_Name,
    Category,
    ROUND(AVG(Discount) * 100, 2) AS Avg_Discount_Given,
    ROUND(SUM(Sales), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Net_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Product_ID, Product_Name, Category
HAVING Profit_Margin_Pct < 10.0 OR Net_Profit < 0
ORDER BY Net_Profit ASC;


-- -----------------------------------------------------------------------------
-- QUERY 16: CUSTOMER SEGMENT PERFORMANCE & AVERAGE ORDER VALUE
-- Description: Evaluates purchase behavior and AOV across Consumer, Corporate, and Small Business.
-- -----------------------------------------------------------------------------
SELECT 
    Customer_Segment,
    COUNT(DISTINCT Customer_ID) AS Unique_Customers,
    COUNT(DISTINCT Order_ID) AS Total_Orders,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Sales) / COUNT(DISTINCT Order_ID), 2) AS Segment_AOV,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct
FROM sales_data
GROUP BY Customer_Segment
ORDER BY Total_Sales DESC;


-- -----------------------------------------------------------------------------
-- QUERY 17: PAYMENT MODE ANALYSIS
-- Description: Analyzes adoption rate and revenue share by payment method.
-- -----------------------------------------------------------------------------
SELECT 
    Payment_Mode,
    COUNT(Order_ID) AS Transaction_Count,
    ROUND((COUNT(Order_ID) * 100.0 / (SELECT COUNT(*) FROM sales_data)), 2) AS Transaction_Share_Pct,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(AVG(Sales), 2) AS Avg_Transaction_Value
FROM sales_data
GROUP BY Payment_Mode
ORDER BY Total_Sales DESC;


-- -----------------------------------------------------------------------------
-- QUERY 18: REGION-WISE PROFIT MARGIN ANALYSIS
-- Description: Evaluates profitability efficiency across regions using CASE WHEN statements.
-- -----------------------------------------------------------------------------
SELECT 
    Region,
    ROUND(SUM(Sales), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    ROUND((SUM(Profit) / SUM(Sales)) * 100, 2) AS Profit_Margin_Pct,
    CASE 
        WHEN (SUM(Profit) / SUM(Sales)) >= 0.22 THEN 'High Profitability'
        WHEN (SUM(Profit) / SUM(Sales)) BETWEEN 0.15 AND 0.2199 THEN 'Moderate Profitability'
        ELSE 'Needs Margin Optimization'
    END AS Performance_Status
FROM sales_data
GROUP BY Region
ORDER BY Profit_Margin_Pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 19: CATEGORY & ORDER STATUS FULFILLMENT MATRIX
-- Description: Analyzes completed vs cancelled and returned orders by category.
-- -----------------------------------------------------------------------------
SELECT 
    Category,
    COUNT(CASE WHEN Order_Status = 'Completed' THEN 1 END) AS Completed_Orders,
    COUNT(CASE WHEN Order_Status = 'Cancelled' THEN 1 END) AS Cancelled_Orders,
    COUNT(CASE WHEN Order_Status = 'Returned' THEN 1 END) AS Returned_Orders,
    ROUND(COUNT(CASE WHEN Order_Status = 'Completed' THEN 1 END) * 100.0 / COUNT(*), 2) AS Fulfillment_Rate_Pct
FROM sales_data
GROUP BY Category
ORDER BY Fulfillment_Rate_Pct DESC;


-- -----------------------------------------------------------------------------
-- QUERY 20: MONTH-OVER-MONTH (MoM) SALES GROWTH RATE USING WINDOW FUNCTIONS (CTE)
-- Description: Uses LAG() window function to calculate month-over-month revenue growth rate.
-- -----------------------------------------------------------------------------
WITH MonthlySalesCTE AS (
    SELECT 
        `Year_Month`,
        ROUND(SUM(Sales), 2) AS Current_Month_Sales
    FROM sales_data
    GROUP BY `Year_Month`
)
SELECT 
    `Year_Month`,
    Current_Month_Sales,
    LAG(Current_Month_Sales, 1) OVER (ORDER BY `Year_Month` ASC) AS Previous_Month_Sales,
    ROUND(
        (Current_Month_Sales - LAG(Current_Month_Sales, 1) OVER (ORDER BY `Year_Month` ASC)) 
        / LAG(Current_Month_Sales, 1) OVER (ORDER BY `Year_Month` ASC) * 100, 
        2
    ) AS MoM_Growth_Pct
FROM MonthlySalesCTE
ORDER BY `Year_Month` ASC;

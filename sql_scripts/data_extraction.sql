-- AdventureWorks analytics extraction template
-- Adjust table and column names to match the exact CSV import schema.

WITH sales AS (
    SELECT *
    FROM Sales
),
product AS (
    SELECT *
    FROM Product
),
customer AS (
    SELECT *
    FROM Customer
),
territory AS (
    SELECT *
    FROM Territory
),
calendar AS (
    SELECT *
    FROM Calendar
)
SELECT
    s.OrderDate,
    s.StockDate,
    s.OrderNumber,
    s.OrderLineItem,
    s.OrderQuantity,
    s.ProductKey,
    s.CustomerKey,
    s.TerritoryKey,
    p.ProductName,
    p.ProductSKU,
    p.ProductCost,
    p.ProductPrice,
    c.FirstName,
    c.LastName,
    c.Gender,
    c.AnnualIncome,
    t.Region,
    t.Country,
    t.Continent,
    cal.Date AS CalendarDate
FROM sales s
LEFT JOIN product p
    ON s.ProductKey = p.ProductKey
LEFT JOIN customer c
    ON s.CustomerKey = c.CustomerKey
LEFT JOIN territory t
    ON s.TerritoryKey = t.TerritoryKey
LEFT JOIN calendar cal
    ON s.OrderDate = cal.Date;

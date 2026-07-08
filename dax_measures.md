# DAX Measures Template

dax : 
% of All Order = 
DIVIDE( [Total Orders],[All Orders])

% of All Returns = 
DIVIDE([Total Returns],[All Returns])

10 Days Rolling Revenue = 
    CALCULATE(
        [Total Revenue],
        DATESINPERIOD(
            'DimDate'[Date],
            MAX('DimDate'[Date]),
            -10,
            DAY
        )
    )
    
90 Day Rolling Profit = 
CALCULATE(
    [Total Profit],
    DATESINPERIOD(
        'DimDate'[Date],
        MAX('DimDate'[Date]),
        -90,
        DAY
    )
)

Adjusted Price = [Average Retail Price] * (1 + 'Price Adjusted (%)'[Price Adjusted (%) Value])

Adjusted Profit = 
    [Adjusted Revenue] - [Total Cost]

Adjusted Revenue = 
SUMX(
    'FactSales',
    'FactSales'[OrderQuantity] *
    [Adjusted Price]
    )

All Orders = 
CALCULATE(
    [Total Orders],
    ALL('FactSales')
)

All Returns = 
CALCULATE(
    [Total Returns],
    ALL('FactReturns')
)

Average Retail Price = 
AVERAGE('DimProduct'[ProductPrice])
Average Revenue Per Customer = 
DIVIDE(
    [Total Revenue],
    [Total Customers]
)

Bike Return Rate = 
    DIVIDE(
        [Bike Returns],[Bike Sales])Bike Returns = 
    CALCULATE(
        [Total Returns],
        'Product Categories Lookup'[CategoryName] = "Bikes"
    )

Bike Sales = 
    CALCULATE(
        [Quantity Sold],
        'Product Categories Lookup'[CategoryName] = "Bikes"
    )

Bulk Order = 
    CALCULATE(
        [Total Orders],
        'FactSales'[OrderQuantity] > 1 
    )

Order Gap = 
    [Total Orders] - [Order Target]
Order Target = 
[Previous Month Orders] * 1.1

Overall Average Price = 
CALCULATE(
    [Average Retail Price],
    ALL(
        'DimProduct')
)

Pervious Month Revenue = 
CALCULATE(
    [Total Revenue],
    DATEADD(
        'DimDate'[Date],
        -1,
        MONTH
    )
)
         
Previous Month Orders = 
    CALCULATE(
        [Total Orders],
        DATEADD('DimDate'[Date],
        -1,
        MONTH
        )
    )

Previous Month Profit = 
CALCULATE(
    [Total Profit],
    DATEADD(
        'DimDate'[Date],
        -1,
        MONTH
    )
)

Previous Month Return = 
CALCULATE(
    [Total Returns],
    DATEADD('DimDate'[Date],
    -1,
    MONTH
    )
)
    
Profit Gap = 
    [Total Profit] - [Profit Target]

Profit Target = 
[Previous Month Profit] * 1.1

Quantity Returned = 
sum(
    'FactReturns'[ReturnQuantity]
)

Quantity Sold = 
SUM(
    'FactSales'[OrderQuantity]
)

Return Rate = 
DIVIDE([Quantity Returned],[Quantity Sold],"No Sales")

Revenue Gap = 
    [Total Revenue] - [Revenue Target]

Revenue Target = 
[Pervious Month Revenue] * 1.1

Total Cost = 
SUMX(
    'FactSales',
    'FactSales'[OrderQuantity] *
    RELATED('DimProduct'[ProductCost])
)

Total Customers = 
DISTINCTCOUNT(
    'FactSales'[CustomerKey]
)

Total Orders (Customer Detail) = 
IF(
    HASONEVALUE('DimCustomer'[CustomerKey]),
    [Total Orders],
    "-"
)

Total Profit = 
[Total Revenue] -[Total Cost]
Total Returns = 
COUNTROWS(
    'FactReturns'
)

Total Revenue = 
SUMX(
    'FactSales',
    'FactSales'[OrderQuantity] *
    RELATED('DimProduct'[ProductPrice]
    )
)

Total Revenue (Customer Detail) = 
IF(
    HASONEVALUE('DimCustomer'[CustomerKey]),
    [Total Revenue],
    "-"
)

Weekend Orders = 
    CALCULATE(
        [Total Orders],
        'DimDate'[Weekend] = "Weekend"
    )

YTD Revenue = 
CALCULATE(
    [Total Revenue],
    DATESYTD(
        'DimDate'[Date]
    )
)


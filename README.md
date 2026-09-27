\# Future Interns Task 1 - Superstore Sales Analysis



\## Project Overview



This project analyzes the Superstore Sales dataset to understand sales performance, profitability, regional performance, product performance, monthly sales trends, loss-making products, and the relationship between discounts and profit.



This project was completed as part of the Future Interns Data Science \& Analytics Internship - Task 1.



\## Tools Used



\- Python

\- Pandas

\- Matplotlib

\- ReportLab

\- Git \& GitHub



\## Dataset



Dataset: Superstore Sales Dataset



\- Records: 9,994

\- Analysis Period: 2014-01-03 to 2017-12-30

\- Columns used: Sales, Profit, Quantity, Discount, Category, Region, Product Name, Order Date and others.



\## Key KPIs



| KPI | Value |

|---|---:|

| Total Sales | $2,297,200.86 |

| Total Profit | $286,397.02 |

| Total Quantity Sold | 37,873 |

| Average Sales per Record | $229.86 |

| Average Profit per Record | $28.66 |

| Profit Margin | 12.47% |



\## Analysis Performed



\### 1. Data Quality



\- Checked missing values

\- Checked duplicate records

\- Converted Order Date and Ship Date to datetime

\- Verified numerical fields



\### 2. Category Analysis



Analyzed sales and profit across:



\- Furniture

\- Office Supplies

\- Technology



Technology generated the highest total sales and total profit.



\### 3. Regional Analysis



Analyzed sales and profit across:



\- West

\- East

\- Central

\- South



West recorded the highest total sales and total profit.



\### 4. Monthly Sales Trend



Monthly sales were analyzed from 2014 to 2017.



\- Highest monthly sales: November 2017

\- Sales: $118,447.82

\- Lowest monthly sales: February 2014

\- Sales: $4,519.89



\### 5. Product Analysis



Products were analyzed using:



\- Sales

\- Profit

\- Quantity sold



Canon imageCLASS 2200 Advanced Copier generated the highest total sales and highest total profit among individual products.



\### 6. Loss-Making Products



The analysis identified 301 products with negative total profit.



The largest cumulative product-level loss was:



\*\*Cubify CubeX 3D Printer Double Head Print: -$8,879.97\*\*



\### 7. Discount and Profit Analysis



Average profit was calculated for different discount levels.



Several higher discount levels were associated with negative average profit, indicating that discount levels should be monitored together with product profitability.



\## Key Insights



\- Total sales were $2.30 million.

\- Total profit was approximately $286K.

\- Overall profit margin was 12.47%.

\- Technology was the highest-performing category by sales and profit.

\- West was the highest-performing region by sales and profit.

\- November 2017 recorded the highest monthly sales.

\- Canon imageCLASS 2200 Advanced Copier was the top product by sales and profit.

\- 301 products recorded negative total profit.

\- Higher discount levels were frequently associated with lower average profit.



\## Business Recommendations



\- Monitor high-discount transactions.

\- Review products with consistently negative profit.

\- Focus product and inventory analysis on profitable categories.

\- Monitor regional sales and profitability.

\- Use monthly sales trends for inventory and promotional planning.

\- Evaluate both sales volume and profitability when assessing products.



\## Project Files



```text

FutureInterns\_Task1/

│

├── charts/

│   ├── discount\_vs\_profit.png

│   ├── loss\_making\_products.png

│   ├── monthly\_sales\_trend.png

│   ├── profit\_by\_category.png

│   ├── profit\_by\_region.png

│   ├── sales\_by\_category.png

│   ├── sales\_by\_region.png

│   └── top\_10\_products\_sales.png

│

├── dataset/

│   └── Sample - Superstore.csv

│

├── create\_report.py

├── sales\_analysis.py

├── Sales\_Analytics\_Report.pdf

└── README.md


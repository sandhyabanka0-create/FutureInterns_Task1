import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    "dataset/Sample - Superstore.csv",
    encoding="latin1"
)

print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# DATA CLEANING
# ==========================================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

print("\nDate columns converted successfully.")

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


# ==========================================
# KEY SALES KPIs
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

average_sales = df["Sales"].mean()
average_profit = df["Profit"].mean()

profit_margin = (total_profit / total_sales) * 100

print("\n================================")
print("KEY SALES KPIs")
print("================================")

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Average Sales per Record: ${average_sales:,.2f}")
print(f"Average Profit per Record: ${average_profit:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")


# ==========================================
# SALES BY CATEGORY
# ==========================================

category_sales = df.groupby("Category")["Sales"].sum()

print("\n================================")
print("SALES BY CATEGORY")
print("================================")

print(category_sales)


# ==========================================
# PROFIT BY CATEGORY
# ==========================================

category_profit = df.groupby("Category")["Profit"].sum()

print("\n================================")
print("PROFIT BY CATEGORY")
print("================================")

print(category_profit)


# ==========================================
# SALES BY REGION
# ==========================================

region_sales = df.groupby("Region")["Sales"].sum()

print("\n================================")
print("SALES BY REGION")
print("================================")

print(region_sales)


# ==========================================
# PROFIT BY REGION
# ==========================================

region_profit = df.groupby("Region")["Profit"].sum()

print("\n================================")
print("PROFIT BY REGION")
print("================================")

print(region_profit)


# ==========================================
# MONTHLY SALES
# ==========================================

df["Year-Month"] = df["Order Date"].dt.to_period("M")

monthly_sales = df.groupby("Year-Month")["Sales"].sum()

print("\n================================")
print("MONTHLY SALES")
print("================================")

print(monthly_sales)


# ==========================================
# TOP 10 PRODUCTS BY SALES
# ==========================================

top_sales_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n================================")
print("TOP 10 PRODUCTS BY SALES")
print("================================")

print(top_sales_products)


# ==========================================
# TOP 10 PRODUCTS BY PROFIT
# ==========================================

top_profit_products = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n================================")
print("TOP 10 PRODUCTS BY PROFIT")
print("================================")

print(top_profit_products)


# ==========================================
# TOP 10 PRODUCTS BY QUANTITY
# ==========================================

top_quantity_products = (
    df.groupby("Product Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n================================")
print("TOP 10 PRODUCTS BY QUANTITY")
print("================================")

print(top_quantity_products)


# ==========================================
# LOSS-MAKING PRODUCTS
# ==========================================

product_profit = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
)

loss_products = product_profit[product_profit < 0]

print("\n================================")
print("LOSS-MAKING PRODUCTS")
print("================================")

print(loss_products.head(10))

print("\nNumber of loss-making products:", len(loss_products))


# ==========================================
# DISCOUNT VS PROFIT
# ==========================================

discount_profit = (
    df.groupby("Discount")["Profit"]
    .mean()
    .sort_index()
)

print("\n================================")
print("AVERAGE PROFIT BY DISCOUNT")
print("================================")

print(discount_profit)


# ==========================================
# CREATE CHARTS
# ==========================================

plt.figure(figsize=(8, 5))
plt.bar(category_sales.index, category_sales.values)
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_category.png")
plt.close()


plt.figure(figsize=(8, 5))
plt.bar(category_profit.index, category_profit.values)
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("charts/profit_by_category.png")
plt.close()


plt.figure(figsize=(8, 5))
plt.bar(region_sales.index, region_sales.values)
plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/sales_by_region.png")
plt.close()


plt.figure(figsize=(8, 5))
plt.bar(region_profit.index, region_profit.values)
plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("charts/profit_by_region.png")
plt.close()


plt.figure(figsize=(12, 6))
plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values,
    marker="o"
)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/monthly_sales_trend.png")
plt.close()


plt.figure(figsize=(10, 6))
plt.barh(
    top_sales_products.index[::-1],
    top_sales_products.values[::-1]
)
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("charts/top_10_products_sales.png")
plt.close()


worst_products = product_profit.head(10)

plt.figure(figsize=(10, 6))
plt.barh(
    worst_products.index[::-1],
    worst_products.values[::-1]
)
plt.title("10 Products with Highest Losses")
plt.xlabel("Profit")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("charts/loss_making_products.png")
plt.close()


plt.figure(figsize=(10, 6))
plt.plot(
    discount_profit.index,
    discount_profit.values,
    marker="o"
)
plt.title("Average Profit vs Discount")
plt.xlabel("Discount")
plt.ylabel("Average Profit")
plt.grid(True)
plt.tight_layout()
plt.savefig("charts/discount_vs_profit.png")
plt.close()


print("\n================================")
print("ALL ANALYSIS AND CHARTS COMPLETED")
print("================================")
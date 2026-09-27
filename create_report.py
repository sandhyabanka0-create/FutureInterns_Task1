import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
    KeepTogether
)
from reportlab.lib.utils import ImageReader


# ============================================================
# FILE PATHS
# ============================================================

DATA_FILE = "dataset/Sample - Superstore.csv"
OUTPUT_FILE = "Sales_Analytics_Report.pdf"
CHART_DIR = "charts"


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.exists(DATA_FILE):
    print("ERROR: Dataset not found!")
    print("Expected:", DATA_FILE)
    raise SystemExit

if not os.path.exists(CHART_DIR):
    print("ERROR: charts folder not found!")
    raise SystemExit


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA_FILE, encoding="latin1")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])


# ============================================================
# BASIC CLEANING
# ============================================================

rows_before = len(df)
duplicates = df.duplicated().sum()
missing_total = df.isnull().sum().sum()

# Remove duplicates if any
df = df.drop_duplicates()

rows_after = len(df)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

avg_sales = df["Sales"].mean()
avg_profit = df["Profit"].mean()

profit_margin = (total_profit / total_sales) * 100


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

category_profit = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# REGION ANALYSIS
# ============================================================

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# MONTHLY SALES
# ============================================================

df["Year-Month"] = df["Order Date"].dt.to_period("M")

monthly_sales = (
    df.groupby("Year-Month")["Sales"]
    .sum()
)


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

top_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_profit = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_quantity = (
    df.groupby("Product Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


# ============================================================
# LOSS-MAKING PRODUCTS
# ============================================================

product_profit = (
    df.groupby("Product Name")["Profit"]
    .sum()
    .sort_values()
)

loss_products = product_profit[product_profit < 0]

top_losses = loss_products.head(10)


# ============================================================
# DISCOUNT ANALYSIS
# ============================================================

discount_profit = (
    df.groupby("Discount")["Profit"]
    .mean()
    .sort_index()
)


# ============================================================
# MONTHLY INSIGHTS
# ============================================================

highest_month = monthly_sales.idxmax()
highest_month_sales = monthly_sales.max()

lowest_month = monthly_sales.idxmin()
lowest_month_sales = monthly_sales.min()


# ============================================================
# CHART PATHS
# ============================================================

charts = {
    "sales_category": os.path.join(CHART_DIR, "sales_by_category.png"),
    "profit_category": os.path.join(CHART_DIR, "profit_by_category.png"),
    "sales_region": os.path.join(CHART_DIR, "sales_by_region.png"),
    "profit_region": os.path.join(CHART_DIR, "profit_by_region.png"),
    "monthly": os.path.join(CHART_DIR, "monthly_sales_trend.png"),
    "top_sales": os.path.join(CHART_DIR, "top_10_products_sales.png"),
    "loss": os.path.join(CHART_DIR, "loss_making_products.png"),
    "discount": os.path.join(CHART_DIR, "discount_vs_profit.png"),
}


# ============================================================
# REPORT STYLES
# ============================================================

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=28,
    leading=34,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#1F4E78"),
    spaceAfter=20
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=15,
    leading=20,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#555555"),
    spaceAfter=25
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    textColor=colors.HexColor("#1F4E78"),
    spaceBefore=5,
    spaceAfter=14
)

subsection_style = ParagraphStyle(
    "Subsection",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=colors.HexColor("#2F5597"),
    spaceBefore=8,
    spaceAfter=8
)

body_style = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=16,
    spaceAfter=8
)

small_style = ParagraphStyle(
    "Small",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12
)

insight_style = ParagraphStyle(
    "Insight",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=16,
    leftIndent=10,
    spaceAfter=7
)

center_style = ParagraphStyle(
    "Center",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10,
    leading=14,
    alignment=TA_CENTER
)


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def add_page_number(canvas, doc):
    canvas.saveState()

    width, height = A4

    # Footer line
    canvas.setStrokeColor(colors.HexColor("#D9E2F3"))
    canvas.line(
        40,
        35,
        width - 40,
        35
    )

    # Footer text
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))

    canvas.drawString(
        40,
        22,
        "FutureInterns Task 1 - Superstore Sales Analysis"
    )

    canvas.drawRightString(
        width - 40,
        22,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# IMAGE FUNCTION
# ============================================================

def add_chart(path, max_width=6.7 * inch, max_height=4.8 * inch):
    """
    Add chart while preserving original aspect ratio.
    """

    if not os.path.exists(path):
        return Paragraph(
            f"<b>Chart not found:</b> {path}",
            body_style
        )

    img = Image(path)

    reader = ImageReader(path)
    width, height = reader.getSize()

    scale = min(
        max_width / width,
        max_height / height
    )

    img.drawWidth = width * scale
    img.drawHeight = height * scale

    img.hAlign = "CENTER"

    return img


# ============================================================
# TABLE FUNCTIONS
# ============================================================

def create_table(data, col_widths=None, header=True):
    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1 if header else 0
    )

    style_commands = [
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.HexColor("#B7B7B7")
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6
        ),
    ]

    if header:
        style_commands.extend([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#1F4E78")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "ALIGN",
                (0, 0),
                (-1, 0),
                "CENTER"
            ),
        ])

    table.setStyle(TableStyle(style_commands))

    return table


def money(value):
    return f"${value:,.2f}"


def number(value):
    return f"{value:,.0f}"


def percent(value):
    return f"{value:.2f}%"


# ============================================================
# DOCUMENT
# ============================================================

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=45,
    bottomMargin=45,
    title="Sales Analytics Report",
    author="FutureInterns Task 1"
)


story = []


# ============================================================
# PAGE 1 - COVER
# ============================================================

story.append(Spacer(1, 70))

story.append(
    Paragraph(
        "Sales Analytics Report",
        title_style
    )
)

story.append(
    Paragraph(
        "FutureInterns Task 1 - Superstore Sales Analysis",
        subtitle_style
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Python • Pandas • Matplotlib",
        center_style
    )
)

story.append(Spacer(1, 35))

cover_data = [
    ["Dataset", "Superstore Sales Dataset"],
    ["Records", f"{len(df):,}"],
    ["Columns", f"{len(df.columns):,}"],
    ["Analysis Period",
     f"{df['Order Date'].min().strftime('%Y-%m-%d')} to "
     f"{df['Order Date'].max().strftime('%Y-%m-%d')}"],
    ["Total Sales", money(total_sales)],
    ["Total Profit", money(total_profit)],
    ["Profit Margin", percent(profit_margin)],
]

cover_table = Table(
    cover_data,
    colWidths=[2.0 * inch, 4.0 * inch]
)

cover_table.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B7B7B7")),
    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF7")),
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))

story.append(cover_table)

story.append(Spacer(1, 50))

story.append(
    Paragraph(
        "Prepared as part of FutureInterns Task 1",
        center_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 2 - EXECUTIVE SUMMARY
# ============================================================

story.append(
    Paragraph(
        "1. Executive Summary",
        section_style
    )
)

story.append(
    Paragraph(
        "This report analyzes the Superstore sales dataset to understand "
        "overall sales performance, profitability, regional performance, "
        "product performance, monthly sales patterns and the relationship "
        "between discounts and profit.",
        body_style
    )
)

story.append(
    Paragraph(
        "The dataset contains 9,994 sales records across 21 columns. "
        "The analysis was performed using Python and Pandas, while "
        "Matplotlib was used to create the visualizations.",
        body_style
    )
)

story.append(Spacer(1, 8))

kpi_data = [
    ["KPI", "Value"],
    ["Total Sales", money(total_sales)],
    ["Total Profit", money(total_profit)],
    ["Total Quantity Sold", number(total_quantity)],
    ["Average Sales per Record", money(avg_sales)],
    ["Average Profit per Record", money(avg_profit)],
    ["Profit Margin", percent(profit_margin)],
]

story.append(
    create_table(
        kpi_data,
        [3.8 * inch, 2.2 * inch]
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Overall Performance",
        subsection_style
    )
)

summary_points = [
    f"The dataset generated total sales of <b>{money(total_sales)}</b> "
    f"and total profit of <b>{money(total_profit)}</b>.",

    f"The overall profit margin is <b>{percent(profit_margin)}</b>.",

    f"A total of <b>{number(total_quantity)}</b> units were sold across "
    f"{len(df):,} transaction records.",

    f"The average sales value per record is <b>{money(avg_sales)}</b>.",

    f"The highest monthly sales occurred in <b>{highest_month}</b>, "
    f"with sales of <b>{money(highest_month_sales)}</b>.",

    f"The lowest monthly sales occurred in <b>{lowest_month}</b>, "
    f"with sales of <b>{money(lowest_month_sales)}</b>.",
]

for point in summary_points:
    story.append(
        Paragraph(
            "• " + point,
            insight_style
        )
    )

story.append(PageBreak())


# ============================================================
# PAGE 3 - DATA QUALITY
# ============================================================

story.append(
    Paragraph(
        "2. Data Preparation and Quality",
        section_style
    )
)

story.append(
    Paragraph(
        "Before performing the analysis, the dataset was checked for "
        "missing values, duplicate records and correct data types.",
        body_style
    )
)

quality_data = [
    ["Check", "Result"],
    ["Rows before cleaning", f"{rows_before:,}"],
    ["Rows after cleaning", f"{rows_after:,}"],
    ["Columns", f"{len(df.columns):,}"],
    ["Duplicate rows", f"{duplicates:,}"],
    ["Missing values", f"{missing_total:,}"],
    ["Order Date", "Converted to datetime"],
    ["Ship Date", "Converted to datetime"],
]

story.append(
    create_table(
        quality_data,
        [3.0 * inch, 3.0 * inch]
    )
)

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Data Quality Findings",
        subsection_style
    )
)

quality_points = [
    "All 9,994 records contain complete values in the provided dataset.",
    "No duplicate rows were found.",
    "Order Date and Ship Date were converted from text to datetime format.",
    "Sales, Quantity, Discount and Profit were retained as numerical fields.",
    "The dataset is suitable for sales, profit, product and regional analysis."
]

for point in quality_points:
    story.append(
        Paragraph(
            "• " + point,
            insight_style
        )
    )

story.append(PageBreak())


# ============================================================
# PAGE 4 - CATEGORY PERFORMANCE
# ============================================================

story.append(
    Paragraph(
        "3. Category Performance",
        section_style
    )
)

story.append(
    Paragraph(
        "Sales and profit were aggregated by product category to compare "
        "the contribution of Furniture, Office Supplies and Technology.",
        body_style
    )
)

category_table = [
    ["Category", "Sales", "Profit"]
]

for category in category_sales.index:
    category_table.append([
        category,
        money(category_sales[category]),
        money(category_profit.get(category, 0))
    ])

story.append(
    create_table(
        category_table,
        [2.0 * inch, 2.0 * inch, 2.0 * inch]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        "Sales by Category",
        subsection_style
    )
)

story.append(
    add_chart(
        charts["sales_category"],
        6.5 * inch,
        3.4 * inch
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "Profit by Category",
        subsection_style
    )
)

story.append(
    add_chart(
        charts["profit_category"],
        6.5 * inch,
        3.4 * inch
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 5 - REGIONAL PERFORMANCE
# ============================================================

story.append(
    Paragraph(
        "4. Regional Performance",
        section_style
    )
)

story.append(
    Paragraph(
        "Regional analysis helps identify differences in sales and profit "
        "across the four geographic regions in the dataset.",
        body_style
    )
)

region_table = [
    ["Region", "Sales", "Profit"]
]

for region in region_sales.index:
    region_table.append([
        region,
        money(region_sales[region]),
        money(region_profit.get(region, 0))
    ])

story.append(
    create_table(
        region_table,
        [2.0 * inch, 2.0 * inch, 2.0 * inch]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        "Sales by Region",
        subsection_style
    )
)

story.append(
    add_chart(
        charts["sales_region"],
        6.5 * inch,
        3.5 * inch
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        "Profit by Region",
        subsection_style
    )
)

story.append(
    add_chart(
        charts["profit_region"],
        6.5 * inch,
        3.5 * inch
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 6 - MONTHLY SALES TREND
# ============================================================

story.append(
    Paragraph(
        "5. Monthly Sales Trend",
        section_style
    )
)

story.append(
    Paragraph(
        "Monthly sales were calculated using Order Date. The trend helps "
        "identify periods of relatively high and low sales activity.",
        body_style
    )
)

story.append(
    add_chart(
        charts["monthly"],
        6.7 * inch,
        5.5 * inch
    )
)

story.append(Spacer(1, 15))

monthly_data = [
    ["Metric", "Month", "Sales"],
    [
        "Highest Monthly Sales",
        str(highest_month),
        money(highest_month_sales)
    ],
    [
        "Lowest Monthly Sales",
        str(lowest_month),
        money(lowest_month_sales)
    ]
]

story.append(
    create_table(
        monthly_data,
        [2.2 * inch, 2.0 * inch, 2.0 * inch]
    )
)

story.append(Spacer(1, 15))

story.append(
    Paragraph(
        f"The highest monthly sales were recorded in {highest_month}, "
        f"while {lowest_month} recorded the lowest monthly sales "
        f"within the dataset.",
        body_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 7 - TOP PRODUCTS
# ============================================================

story.append(
    Paragraph(
        "6. Top Performing Products",
        section_style
    )
)

story.append(
    Paragraph(
        "Product-level analysis was performed using Sales, Profit and "
        "Quantity to identify products with strong contribution across "
        "different performance measures.",
        body_style
    )
)

story.append(
    Paragraph(
        "Top 10 Products by Sales",
        subsection_style
    )
)

top_sales_table = [["Rank", "Product", "Sales"]]

for rank, (product, value) in enumerate(top_sales.items(), 1):
    top_sales_table.append([
        rank,
        Paragraph(product, small_style),
        money(value)
    ])

story.append(
    create_table(
        top_sales_table,
        [0.5 * inch, 4.3 * inch, 1.3 * inch]
    )
)

story.append(Spacer(1, 15))

story.append(
    add_chart(
        charts["top_sales"],
        6.5 * inch,
        3.3 * inch
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 8 - TOP PROFIT AND QUANTITY
# ============================================================

story.append(
    Paragraph(
        "7. Product Profitability and Quantity",
        section_style
    )
)

story.append(
    Paragraph(
        "Sales volume does not always represent the same performance "
        "as profitability. The following tables show the leading "
        "products by profit and quantity sold.",
        body_style
    )
)

story.append(
    Paragraph(
        "Top 10 Products by Profit",
        subsection_style
    )
)

profit_table = [["Rank", "Product", "Profit"]]

for rank, (product, value) in enumerate(top_profit.items(), 1):
    profit_table.append([
        rank,
        Paragraph(product, small_style),
        money(value)
    ])

story.append(
    create_table(
        profit_table,
        [0.5 * inch, 4.3 * inch, 1.3 * inch]
    )
)

story.append(Spacer(1, 18))

story.append(
    Paragraph(
        "Top 10 Products by Quantity Sold",
        subsection_style
    )
)

quantity_table = [["Rank", "Product", "Quantity"]]

for rank, (product, value) in enumerate(top_quantity.items(), 1):
    quantity_table.append([
        rank,
        Paragraph(product, small_style),
        number(value)
    ])

story.append(
    create_table(
        quantity_table,
        [0.5 * inch, 4.3 * inch, 1.3 * inch]
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 9 - LOSS MAKING PRODUCTS
# ============================================================

story.append(
    Paragraph(
        "8. Loss-Making Products",
        section_style
    )
)

story.append(
    Paragraph(
        f"The analysis identified <b>{len(loss_products)}</b> products "
        "with negative total profit. The following table presents the "
        "10 products with the largest cumulative losses.",
        body_style
    )
)

loss_table = [
    ["Rank", "Product", "Profit"]
]

for rank, (product, value) in enumerate(top_losses.items(), 1):
    loss_table.append([
        rank,
        Paragraph(product, small_style),
        money(value)
    ])

story.append(
    create_table(
        loss_table,
        [0.5 * inch, 4.3 * inch, 1.3 * inch]
    )
)

story.append(Spacer(1, 18))

story.append(
    Paragraph(
        "Loss-Making Products Chart",
        subsection_style
    )
)

story.append(
    add_chart(
        charts["loss"],
        6.5 * inch,
        4.2 * inch
    )
)

story.append(Spacer(1, 10))

story.append(
    Paragraph(
        f"The largest product-level loss in the dataset was "
        f"<b>{money(top_losses.iloc[0])}</b> for "
        f"<b>{top_losses.index[0]}</b>.",
        body_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 10 - DISCOUNT ANALYSIS
# ============================================================

story.append(
    Paragraph(
        "9. Discount and Profit Analysis",
        section_style
    )
)

story.append(
    Paragraph(
        "Average profit was calculated for each discount level to "
        "understand how discount levels are associated with profitability.",
        body_style
    )
)

discount_table = [
    ["Discount", "Average Profit"]
]

for discount, value in discount_profit.items():
    discount_table.append([
        f"{discount * 100:.0f}%",
        money(value)
    ])

story.append(
    create_table(
        discount_table,
        [2.5 * inch, 2.5 * inch]
    )
)

story.append(Spacer(1, 15))

story.append(
    add_chart(
        charts["discount"],
        6.5 * inch,
        4.5 * inch
    )
)

story.append(Spacer(1, 12))

story.append(
    Paragraph(
        "The analysis shows that several higher discount levels are "
        "associated with negative average profit. This indicates that "
        "discount strategy should be monitored together with product "
        "margin and sales volume.",
        body_style
    )
)

story.append(PageBreak())


# ============================================================
# PAGE 11 - KEY INSIGHTS
# ============================================================

story.append(
    Paragraph(
        "10. Key Insights",
        section_style
    )
)

highest_sales_category = category_sales.idxmax()
highest_profit_category = category_profit.idxmax()
highest_sales_region = region_sales.idxmax()
highest_profit_region = region_profit.idxmax()

insights = [
    (
        "Overall Performance",
        f"Total sales were {money(total_sales)} with total profit of "
        f"{money(total_profit)}, resulting in an overall profit margin "
        f"of {percent(profit_margin)}."
    ),

    (
        "Category Performance",
        f"{highest_sales_category} generated the highest total sales "
        f"at {money(category_sales.max())}."
    ),

    (
        "Category Profitability",
        f"{highest_profit_category} generated the highest total profit "
        f"at {money(category_profit.max())}."
    ),

    (
        "Regional Sales",
        f"{highest_sales_region} recorded the highest total sales "
        f"at {money(region_sales.max())}."
    ),

    (
        "Regional Profit",
        f"{highest_profit_region} generated the highest total profit "
        f"at {money(region_profit.max())}."
    ),

    (
        "Monthly Trend",
        f"The highest monthly sales occurred in {highest_month}, "
        f"with {money(highest_month_sales)} in sales."
    ),

    (
        "Product Performance",
        f"{top_sales.index[0]} was the highest-selling product by "
        f"sales value, generating {money(top_sales.iloc[0])}."
    ),

    (
        "Product Profitability",
        f"{top_profit.index[0]} generated the highest total product "
        f"profit of {money(top_profit.iloc[0])}."
    ),

    (
        "Loss-Making Products",
        f"{len(loss_products)} products recorded negative total profit. "
        f"The largest loss was associated with {top_losses.index[0]}."
    ),

    (
        "Discount Effect",
        "Higher discount levels in the dataset are frequently associated "
        "with lower or negative average profit."
    ),
]

for title, text in insights:
    story.append(
        Paragraph(
            f"<b>{title}:</b> {text}",
            insight_style
        )
    )

story.append(PageBreak())


# ============================================================
# PAGE 12 - RECOMMENDATIONS
# ============================================================

story.append(
    Paragraph(
        "11. Business Recommendations",
        section_style
    )
)

recommendations = [
    (
        "Monitor High-Discount Transactions",
        "Review products and transactions with high discounts because "
        "some discount levels are associated with negative average profit."
    ),

    (
        "Review Loss-Making Products",
        "Investigate pricing, discounts, shipping costs and demand for "
        "products with consistently negative profit."
    ),

    (
        "Focus on Profitable Categories",
        "Use category-level profit analysis when planning product "
        "promotion and inventory strategies."
    ),

    (
        "Monitor Regional Performance",
        "Compare sales and profit by region regularly to identify "
        "differences in regional performance."
    ),

    (
        "Use Monthly Trends",
        "Use historical monthly sales patterns to support inventory "
        "planning and promotional scheduling."
    ),

    (
        "Separate Sales Volume from Profitability",
        "A product with high quantity or high sales may not necessarily "
        "generate the highest profit, so both measures should be monitored."
    ),
]

for title, text in recommendations:
    story.append(
        Paragraph(
            f"<b>{title}</b>",
            subsection_style
        )
    )

    story.append(
        Paragraph(
            text,
            body_style
        )
    )

story.append(PageBreak())


# ============================================================
# PAGE 13 - METHODOLOGY
# ============================================================

story.append(
    Paragraph(
        "12. Methodology",
        section_style
    )
)

methodology = [
    (
        "1. Data Loading",
        "The Superstore CSV dataset was loaded using Pandas."
    ),

    (
        "2. Data Cleaning",
        "Missing values and duplicate rows were checked. Date columns "
        "were converted into datetime format."
    ),

    (
        "3. KPI Calculation",
        "Total sales, total profit, total quantity, average sales, "
        "average profit and profit margin were calculated."
    ),

    (
        "4. Category Analysis",
        "Sales and profit were aggregated by product category."
    ),

    (
        "5. Regional Analysis",
        "Sales and profit were aggregated by region."
    ),

    (
        "6. Time Analysis",
        "Monthly sales were calculated using Order Date."
    ),

    (
        "7. Product Analysis",
        "Products were ranked by sales, profit and quantity."
    ),

    (
        "8. Loss Analysis",
        "Products with negative total profit were identified."
    ),

    (
        "9. Discount Analysis",
        "Average profit was calculated for each discount level."
    ),

    (
        "10. Visualization",
        "Matplotlib charts were generated to communicate the analysis "
        "clearly."
    ),
]

for title, text in methodology:
    story.append(
        Paragraph(
            f"<b>{title}</b>",
            subsection_style
        )
    )

    story.append(
        Paragraph(
            text,
            body_style
        )
    )

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Tools Used",
        subsection_style
    )
)

tools_data = [
    ["Tool", "Purpose"],
    ["Python", "Data analysis and automation"],
    ["Pandas", "Data cleaning and aggregation"],
    ["Matplotlib", "Data visualization"],
    ["ReportLab", "PDF report generation"],
]

story.append(
    create_table(
        tools_data,
        [2.0 * inch, 4.0 * inch]
    )
)

story.append(Spacer(1, 25))

story.append(
    Paragraph(
        "End of Report",
        center_style
    )
)


# ============================================================
# BUILD PDF
# ============================================================

doc.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number
)


print()
print("================================")
print("PROFESSIONAL PDF REPORT CREATED")
print("================================")
print(f"File: {OUTPUT_FILE}")
print(f"Pages: Multi-page report")
print(f"Charts included: {len([x for x in charts.values() if os.path.exists(x)])}")
print()
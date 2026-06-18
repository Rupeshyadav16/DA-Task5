import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Starting Task 2: Exploratory Data Analysis & Business Intelligence Workflow...")

# Aapke folder me jo file dikh rahi hai uska exact naam
filename = "Cleaned_Sales_Dataset.xlsx"

if not os.path.exists(filename):
    print(f"❌ Error: {filename} nahi mili folder me!")
    exit()

try:
    # Method 1: Pehle CSV backend logic se read karne ki koshish karein
    df = pd.read_csv(filename)
    print("📊 Success: Dataset successfully loaded via Smart CSV Fallback Engine!")
except Exception:
    try:
        # Method 2: Agar fail ho toh standard Excel parser se load karein
        df = pd.read_excel(filename)
        print("📊 Success: Dataset successfully loaded via Spreadsheet Engine!")
    except Exception as e:
        print(f"❌ System Breakdown: Cannot parse file format. Error: {e}")
        exit()

print(f"✅ Data Extraction Operational! Total Rows: {df.shape[0]}, Columns: {df.shape[1]}\n")

# ---------------------------------------------------------
# STEP 1: Descriptive Statistics & Univariate Analysis
# ---------------------------------------------------------
print("--- [STEP 1] GENERATING NUMERICAL DESCRIPTIVE STATISTICS ---")
print(df[['Age', 'Quantity', 'Unit_Price', 'Total_Sales']].describe())

# Save Chart 1: Distribution of Total Sales
plt.figure(figsize=(9, 5))
sns.histplot(df['Total_Sales'], kde=True, color='teal', bins=20)
plt.title('Distribution of Total Sales - Rupesh Kumar Yadav', fontsize=14, pad=15)
plt.xlabel('Total Sales Value (INR)', fontsize=12)
plt.ylabel('Transaction Count', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('1_sales_distribution_histogram.png', dpi=300)
print("💾 Saved Chart 1: 1_sales_distribution_histogram.png")
plt.close()


# ---------------------------------------------------------
# STEP 2: Business Intelligence Metric Computations
# ---------------------------------------------------------
print("\n--- [STEP 2] PROCESSING BUSINESS INTELLIGENCE QUERIES ---")

# BI Query 1: Top 5 products by revenue
top_5_products = df.groupby('Product')['Total_Sales'].sum().reset_index()
top_5_products = top_5_products.sort_values(by='Total_Sales', ascending=False).head(5)
print("\n[BI Query 1] Top 5 Products by Revenue:")
print(top_5_products.to_string(index=False))

# Save Chart 2: Top Products by Revenue
plt.figure(figsize=(9, 4.5))
sns.barplot(x='Total_Sales', y='Product', data=top_5_products, palette='viridis', hue='Product', legend=False)
plt.title('Top 5 Revenue-Generating Products - Business Matrix', fontsize=14, pad=15)
plt.xlabel('Total Revenue Generated (INR)', fontsize=12)
plt.ylabel('Product Name', fontsize=12)
plt.tight_layout()
plt.savefig('2_top_5_products_revenue.png', dpi=300)
print("💾 Saved Chart 2: 2_top_5_products_revenue.png")
plt.close()


# ---------------------------------------------------------
# STEP 3: Multivariate Analysis & Multi-Feature Correlation Matrix
# ---------------------------------------------------------
print("\n--- [STEP 3] MULTIVARIATE ANALYSIS & STRUCTURAL HEATMAP ---")

plt.figure(figsize=(7, 5))
numeric_cols = df[['Age', 'Quantity', 'Unit_Price', 'Total_Sales']]
correlation_matrix = numeric_cols.corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Features Interaction Matrix & Correlation Heatmap', fontsize=13, pad=15)
plt.tight_layout()
plt.savefig('3_multivariate_correlation_heatmap.png', dpi=300)
print("💾 Saved Chart 3: 3_multivariate_correlation_heatmap.png")
plt.close()

print("\n🎉 Task 2 Data Pipeline Execution Complete! All target deliverables successfully created.")
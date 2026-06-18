import pandas as pd
import sqlite3
import os

print("🚀 Initializing Local SQLite Business Intelligence Pipeline...")

filename = "Cleaned_Sales_Dataset.xlsx"

# Check if data file exists
if not os.path.exists(filename):
    print(f"❌ Error: {filename} nahi mili! Pehle ensure karein ki data file is folder me hai.")
    exit()

try:
    # Load dataset spreadsheet directly
    df = pd.read_excel(filename)
except Exception:
    df = pd.read_csv(filename)

# -----------------------------------------------------------------------------
# CREATE IN-MEMORY SQL DATABASE
# -----------------------------------------------------------------------------
conn = sqlite3.connect(':memory:')

# Dataframe ko sales namak SQL table me convert karte hain
df.to_sql('sales', conn, index=False, if_exists='replace')
print("✅ Dataset successfully converted into an active SQL Table: 'sales'\n")

# -----------------------------------------------------------------------------
# EXECUTE CORE BUSINESS INTELLIGENCE SQL QUERIES
# -----------------------------------------------------------------------------

print("="*60)
print("📊 [SQL QUERY 1] TOP 5 REVENUE GENERATING PRODUCTS")
print("="*60)
query1 = """
SELECT 
    Product, 
    SUM(Total_Sales) AS Total_Revenue,
    SUM(Quantity) AS Total_Units_Sold
FROM sales
GROUP BY Product
ORDER BY Total_Revenue DESC
LIMIT 5;
"""
df_query1 = pd.read_sql_query(query1, conn)
print(df_query1.to_string(index=False))


print("\n" + "="*60)
print("📈 [SQL QUERY 2] TRANSACTION SUMMARY BY CUSTOMER AGE GROUP")
print("="*60)
query2 = """
SELECT 
    Age_Group,
    COUNT(*) AS Total_Transactions,
    ROUND(AVG(Total_Sales), 2) AS Average_Order_Value,
    SUM(Total_Sales) AS Group_Total_Revenue
FROM sales
GROUP BY Age_Group
ORDER BY Group_Total_Revenue DESC;
"""
df_query2 = pd.read_sql_query(query2, conn)
print(df_query2.to_string(index=False))


print("\n" + "="*60)
print("🏙️ [SQL QUERY 3] SALES MARKET SHARE BY REGIONAL CITIES")
print("="*60)
query3 = """
SELECT 
    City, 
    COUNT(*) AS Order_Count,
    ROUND(SUM(Total_Sales), 2) AS Total_City_Revenue,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales)), 2) AS Market_Share_Percentage
FROM sales
GROUP BY City
ORDER BY Total_City_Revenue DESC;
"""
df_query3 = pd.read_sql_query(query3, conn)
print(df_query3.to_string(index=False))

# Close SQL Engine Database Connection safely
conn.close()
print("\n🎉 SQL BI Queries Execution Completed Successfully!")
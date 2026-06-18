import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Page Configuration (Widescreen layout)
st.set_page_config(page_title="ApexPlanet BI Dashboard", layout="wide")

# Title Block
st.title("📊 Executive Business Intelligence & Predictive Dashboard")
st.markdown("**Data Analyst Intern:** Rupesh Kumar Yadav | **Company:** ApexPlanet Software Pvt. Ltd.")
st.markdown("---")

filename = "Cleaned_Sales_Dataset.xlsx"

if not os.path.exists(filename):
    st.error(f"❌ '{filename}' nahi mili! Pehle script check karein.")
else:
    # Load Clean Data
    df = pd.read_excel(filename)

    # -----------------------------------------------------------------------------
    # 1. TOP DYNAMIC KPI CARDS
    # -----------------------------------------------------------------------------
    total_revenue = df['Total_Sales'].sum()
    total_orders = len(df)
    avg_basket = df['Total_Sales'].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="TOTAL SALES REVENUE", value=f"₹{total_revenue/1000000:.2f} Million")
    with col2:
        st.metric(label="TOTAL SYSTEM VOLUME", value=f"{total_orders:,} Orders")
    with col3:
        st.metric(label="AVERAGE BASKET VALUE", value=f"₹{avg_basket:,.2f}")

    st.markdown("---")

    # -----------------------------------------------------------------------------
    # 2. INTERACTIVE FILTERS (Sidebar)
    # -----------------------------------------------------------------------------
    st.sidebar.header("🎯 Live Dashboard Filters")
    selected_city = st.sidebar.multiselect("Select City/Region:", options=df['City'].unique(), default=df['City'].unique()[:3])
    
    # Filter dataset dynamically
    filtered_df = df[df['City'].isin(selected_city)]

    # -----------------------------------------------------------------------------
    # 3. GRAPHICS & DATA CLUSTERING
    # -----------------------------------------------------------------------------
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("🏙️ Regional Revenue Analysis (Filtered)")
        if not filtered_df.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            city_sales = filtered_df.groupby('City')['Total_Sales'].sum().sort_values(ascending=False)
            sns.barplot(x=city_sales.values, y=city_sales.index, ax=ax, palette="Blues_r")
            ax.set_xlabel("Revenue (INR)")
            st.pyplot(fig)
        else:
            st.warning("Please select at least one city from the sidebar.")

    with right_col:
        st.subheader("📦 Top 5 Revenue Driving Products")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        top_products = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head(5)
        sns.barplot(x=top_products.values, y=top_products.index, ax=ax2, palette="viridis")
        ax2.set_xlabel("Total Sales (INR)")
        st.pyplot(fig2)

    st.markdown("---")

    # -----------------------------------------------------------------------------
    # 4. LIVE MACHINE LEARNING PREDICTION TOOL
    # -----------------------------------------------------------------------------
    st.subheader("🔮 Real-Time Sales Prediction Engine (Task 3 Model Deployment)")
    st.markdown("Enter values below to test the active Machine Learning model live:")

    # Train a quick background OLS model for deployment demo
    X = df[['Quantity', 'Unit_Price']]
    y = df['Total_Sales']
    model = LinearRegression().fit(X, y)

    # Interactive Input Sliders for Users
    input_qty = st.slider("Select Order Quantity:", min_value=1, max_value=50, value=5)
    input_price = st.number_input("Enter Unit Price (INR):", min_value=100, max_value=50000, value=15000, step=500)

    # Live Prediction Output
    predicted_sales = model.predict([[input_qty, input_price]])[0]
    
    st.success(st.markdown(f"### 🎯 **Predicted Total Sales Value:** ₹{predicted_sales:,.2f}"))

    st.markdown("---")
    st.info("💡 **System Audit Conclusion:** This interactive app successfully deploys the full-stack analytical modules from Milestones 1, 2, and 3 into a single production-ready dashboard interface.")
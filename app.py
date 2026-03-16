import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Global Retail Sales & Profit Dashboard",
    layout="wide"
)

# ----------------------------
# CUSTOM STYLE
# ----------------------------
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }

    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: 0.2px;
    }

    [data-testid="stMetric"] {
        background-color: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 14px;
        border-radius: 14px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }

    .insight-box {
        background-color: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 18px;
        border-radius: 16px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Global Retail Sales & Profit Dashboard")
st.write(
    "Interactive dashboard built with Python, Streamlit, and Plotly to analyze sales, profit, customer value, discount impact, and geographic performance."
)

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("SuperStoreOrders - SuperStoreOrders.csv")

# Standardize column names just in case
df.columns = [col.strip().lower() for col in df.columns]

# Fix numeric columns
for col in ["sales", "profit", "discount", "quantity", "shipping_cost"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Fix date column
df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True, errors="coerce")

# Remove rows with missing key values
df = df.dropna(subset=["order_date", "sales", "profit"])

# Create time columns
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.strftime("%Y-%m")

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filter Dashboard")

selected_region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique())
)

selected_category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

selected_year = st.sidebar.multiselect(
    "Year",
    options=sorted(df["year"].dropna().unique()),
    default=sorted(df["year"].dropna().unique())
)

filtered_df = df[
    (df["region"].isin(selected_region)) &
    (df["category"].isin(selected_category)) &
    (df["year"].isin(selected_year))
].copy()

# ----------------------------
# KPI METRICS
# ----------------------------
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique() if "order_id" in filtered_df.columns else len(filtered_df)
profit_margin = (total_profit / total_sales * 100) if total_sales != 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Profit Margin", f"{profit_margin:.2f}%")

st.markdown("---")

# ----------------------------
# CHARTS ROW 1
# ----------------------------
left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    sales_category = (
        filtered_df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig1 = px.bar(
        sales_category,
        x="category",
        y="sales",
        text_auto=".2s",
        color="category",
        title="Sales by Category"
    )
    fig1.update_layout(
        template="plotly_dark",
        xaxis_title="Category",
        yaxis_title="Sales",
        title_x=0.2,
        showlegend=False
    )
    st.plotly_chart(fig1, width="stretch")

with right:
    st.subheader("Profit by Region")
    profit_region = (
        filtered_df.groupby("region", as_index=False)["profit"]
        .sum()
        .sort_values("profit", ascending=False)
    )

    fig2 = px.bar(
        profit_region,
        x="region",
        y="profit",
        text_auto=".2s",
        color="region",
        title="Profit by Region"
    )
    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Region",
        yaxis_title="Profit",
        title_x=0.2,
        showlegend=False
    )
    st.plotly_chart(fig2, width="stretch")

# ----------------------------
# MONTHLY TREND
# ----------------------------
st.subheader("Monthly Sales Trend")
monthly_sales = (
    filtered_df.groupby("month", as_index=False)["sales"]
    .sum()
    .sort_values("month")
)

fig3 = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)
fig3.update_layout(
    template="plotly_dark",
    xaxis_title="Month",
    yaxis_title="Sales",
    title_x=0.2
)
st.plotly_chart(fig3, width="stretch")

# ----------------------------
# TOP TABLES
# ----------------------------
left2, right2 = st.columns(2)

with left2:
    st.subheader("Top 10 Customers by Sales")
    top_customers = (
        filtered_df.groupby("customer_name", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )
    st.dataframe(top_customers, width="stretch")

with right2:
    st.subheader("Top 10 Products by Sales")
    top_products = (
        filtered_df.groupby("product_name", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
        .head(10)
    )
    st.dataframe(top_products, width="stretch")

# ----------------------------
# CUSTOMER REVENUE DISTRIBUTION
# ----------------------------
st.subheader("Top Customer Revenue Distribution")
customer_sales = (
    filtered_df.groupby("customer_name", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
    .head(15)
)

fig4 = px.bar(
    customer_sales,
    x="customer_name",
    y="sales",
    color="sales",
    title="Top 15 Customers by Sales"
)
fig4.update_layout(
    template="plotly_dark",
    xaxis_title="Customer",
    yaxis_title="Sales",
    title_x=0.2,
    coloraxis_showscale=False
)
st.plotly_chart(fig4, width="stretch")

# ----------------------------
# DISCOUNT VS PROFIT
# ----------------------------
st.subheader("Discount vs Profit")
scatter_cols = [c for c in ["discount", "profit", "category", "region"] if c in filtered_df.columns]
scatter_df = filtered_df[scatter_cols].dropna()
scatter_df = scatter_df.sample(min(1000, len(scatter_df)), random_state=42) if len(scatter_df) > 0 else scatter_df

if not scatter_df.empty:
    fig5 = px.scatter(
        scatter_df,
        x="discount",
        y="profit",
        color="category" if "category" in scatter_df.columns else None,
        hover_data=["region"] if "region" in scatter_df.columns else None,
        title="Discount vs Profit"
    )
    fig5.update_layout(
        template="plotly_dark",
        xaxis_title="Discount",
        yaxis_title="Profit",
        title_x=0.2
    )
    st.plotly_chart(fig5, width="stretch")
else:
    st.info("No discount/profit data available for the selected filters.")

# ----------------------------
# MAP OF SALES BY COUNTRY
# ----------------------------
st.subheader("Global Sales Map")

if "country" in filtered_df.columns:
    country_sales = (
        filtered_df.groupby("country", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig_map = px.choropleth(
        country_sales,
        locations="country",
        locationmode="country names",
        color="sales",
        hover_name="country",
        color_continuous_scale="Blues",
        title="Sales by Country"
    )
    fig_map.update_layout(
        template="plotly_dark",
        title_x=0.2,
        geo=dict(showframe=False, showcoastlines=True, projection_type="equirectangular")
    )
    st.plotly_chart(fig_map, width="stretch")
else:
    st.info("Country column not found, so the map section is skipped.")

# ----------------------------
# ANIMATED SALES OVER TIME
# ----------------------------
st.subheader("Animated Sales by Market Over Time")

if "market" in filtered_df.columns:
    animated_sales = (
        filtered_df.groupby(["month", "market"], as_index=False)["sales"]
        .sum()
        .sort_values("month")
    )

    fig_anim = px.bar(
        animated_sales,
        x="market",
        y="sales",
        color="market",
        animation_frame="month",
        title="Sales by Market Over Time"
    )
    fig_anim.update_layout(
        template="plotly_dark",
        xaxis_title="Market",
        yaxis_title="Sales",
        title_x=0.2,
        showlegend=False
    )
    st.plotly_chart(fig_anim, width="stretch")
else:
    st.info("Market column not found, so the animated chart section is skipped.")

# ----------------------------
# AI-STYLE INSIGHTS
# ----------------------------
st.subheader("AI-Style Business Insights")

if not filtered_df.empty:
    best_category = filtered_df.groupby("category")["sales"].sum().idxmax()
    best_region = filtered_df.groupby("region")["profit"].sum().idxmax()
    best_customer = filtered_df.groupby("customer_name")["sales"].sum().idxmax()
    avg_discount = filtered_df["discount"].mean() if "discount" in filtered_df.columns else 0
    loss_making = len(filtered_df[filtered_df["profit"] < 0])

    # extra insight
    worst_discount_group = None
    if "discount" in filtered_df.columns:
        discounted = filtered_df.copy()
        discounted["discount_band"] = pd.cut(
            discounted["discount"],
            bins=[-0.01, 0, 0.2, 0.5, 1.0],
            labels=["No Discount", "Low Discount", "Medium Discount", "High Discount"]
        )
        band_profit = discounted.groupby("discount_band", observed=False)["profit"].mean()
        if not band_profit.dropna().empty:
            worst_discount_group = band_profit.idxmin()

    st.markdown(
        f"""
        <div class="insight-box">
        <b>Insight 1:</b> The strongest sales category in the current view is <b>{best_category}</b>, suggesting this category drives the largest share of revenue.
        </div>

        <div class="insight-box">
        <b>Insight 2:</b> The most profitable region is <b>{best_region}</b>, which may indicate stronger pricing, lower discounts, or better product mix there.
        </div>

        <div class="insight-box">
        <b>Insight 3:</b> The top customer by sales is <b>{best_customer}</b>, showing a concentration of revenue among high-value customers.
        </div>

        <div class="insight-box">
        <b>Insight 4:</b> The average discount in the filtered data is <b>{avg_discount:.2f}</b>, and there are <b>{loss_making}</b> loss-making transactions.
        </div>
        """,
        unsafe_allow_html=True
    )

    if worst_discount_group is not None:
        st.markdown(
            f"""
            <div class="insight-box">
            <b>Insight 5:</b> Transactions in the <b>{worst_discount_group}</b> band appear to produce the weakest average profit, suggesting discount strategy may need review.
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.info("No insights available because the filters returned no data.")

# ----------------------------
# DOWNLOAD BUTTON
# ----------------------------
st.subheader("Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered dataset as CSV",
    data=csv_data,
    file_name="filtered_retail_data.csv",
    mime="text/csv"
)

# ----------------------------
# RAW DATA
# ----------------------------
with st.expander("Show Filtered Raw Data"):
    st.dataframe(filtered_df, width="stretch")
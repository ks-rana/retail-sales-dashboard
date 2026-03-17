import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Global Retail Sales & Profit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLING
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, .stSubheader {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.3px;
}

.main {
    background: #0a0f1e;
    padding-top: 1.2rem;
}

/* KPI Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 18px;
    transition: border-color 0.2s ease;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(99, 179, 237, 0.35);
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: rgba(255,255,255,0.45) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.85rem !important;
    font-weight: 700;
}
[data-testid="stMetricDelta"] {
    font-size: 0.8rem;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #63b3ed;
    margin-bottom: 4px;
    margin-top: 28px;
}

/* Insight cards */
.insight-card {
    background: linear-gradient(135deg, rgba(99,179,237,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-left: 3px solid #63b3ed;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 10px;
    font-size: 0.9rem;
    line-height: 1.6;
    color: rgba(255,255,255,0.82);
}
.insight-card.warning {
    border-left-color: #f6ad55;
    background: linear-gradient(135deg, rgba(246,173,85,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border-color: rgba(246,173,85,0.15);
}
.insight-card.positive {
    border-left-color: #68d391;
    background: linear-gradient(135deg, rgba(104,211,145,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border-color: rgba(104,211,145,0.15);
}
.insight-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.insight-title.blue  { color: #63b3ed; }
.insight-title.amber { color: #f6ad55; }
.insight-title.green { color: #68d391; }

/* Divider */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d1324 !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in ["sales", "profit", "discount", "quantity", "shipping_cost"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["order_date", "sales", "profit"])
    df["year"]  = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    df["profit_margin"] = df["profit"] / df["sales"].replace(0, np.nan) * 100
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    total_sales  = df["sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique() if "order_id" in df.columns else len(df)
    margin       = (total_profit / total_sales * 100) if total_sales else 0
    avg_order    = (total_sales / total_orders) if total_orders else 0
    return dict(
        total_sales=total_sales,
        total_profit=total_profit,
        total_orders=total_orders,
        margin=margin,
        avg_order=avg_order,
    )


def generate_insights(df: pd.DataFrame) -> list[dict]:
    """
    Returns a list of insight dicts with keys: title, text, tone (blue/amber/green).
    Each insight is derived from actual data analysis rather than simple lookups.
    """
    insights = []

    # --- 1. Trend: is last quarter accelerating or declining? ---
    monthly = df.groupby("month")["sales"].sum().sort_index()
    if len(monthly) >= 6:
        recent_avg  = monthly.iloc[-3:].mean()
        prior_avg   = monthly.iloc[-6:-3].mean()
        pct_change  = ((recent_avg - prior_avg) / prior_avg * 100) if prior_avg else 0
        direction   = "up" if pct_change > 0 else "down"
        tone        = "positive" if pct_change > 0 else "warning"
        insights.append({
            "title": "Revenue Trend",
            "tone": tone,
            "color": "green" if tone == "positive" else "amber",
            "text": (
                f"Sales are trending <b>{'up' if pct_change > 0 else 'down'} {abs(pct_change):.1f}%</b> "
                f"compared to the prior quarter. "
                + ("Momentum is positive — a good time to double down on top-performing segments."
                   if pct_change > 0
                   else "This warrants attention: investigate whether it's seasonal or structural.")
            )
        })

    # --- 2. Discount drag: high-discount orders are hurting margin ---
    if "discount" in df.columns:
        high_disc   = df[df["discount"] >= 0.3]
        low_disc    = df[df["discount"] < 0.3]
        high_margin = high_disc["profit_margin"].mean() if not high_disc.empty else 0
        low_margin  = low_disc["profit_margin"].mean()  if not low_disc.empty  else 0
        drag        = low_margin - high_margin
        pct_high    = len(high_disc) / len(df) * 100 if len(df) else 0
        tone        = "warning" if drag > 5 else "blue"
        insights.append({
            "title": "Discount Drag",
            "tone": tone,
            "color": "amber" if tone == "warning" else "blue",
            "text": (
                f"<b>{pct_high:.1f}%</b> of transactions carry a discount ≥ 30%. "
                f"These orders average a <b>{high_margin:.1f}%</b> margin vs "
                f"<b>{low_margin:.1f}%</b> for lower-discount orders — "
                f"a <b>{drag:.1f} pp gap</b>. "
                + ("Pricing discipline review is recommended." if drag > 5
                   else "The discount policy appears reasonably controlled.")
            )
        })

    # --- 3. Concentration risk: top 10 customers as % of revenue ---
    cust = df.groupby("customer_name")["sales"].sum().sort_values(ascending=False)
    top10_share = cust.head(10).sum() / cust.sum() * 100 if cust.sum() else 0
    tone = "warning" if top10_share > 40 else "positive"
    insights.append({
        "title": "Revenue Concentration",
        "tone": tone,
        "color": "amber" if tone == "warning" else "green",
        "text": (
            f"The top 10 customers account for <b>{top10_share:.1f}%</b> of total sales. "
            + (f"This level of concentration carries customer-exit risk — diversification should be a strategic priority."
               if top10_share > 40
               else "Revenue is reasonably diversified across the customer base.")
        )
    })

    # --- 4. Worst sub-category by margin ---
    if "sub_category" in df.columns:
        sub_margin = df.groupby("sub_category")["profit_margin"].mean().sort_values()
        worst_sub  = sub_margin.index[0]
        worst_val  = sub_margin.iloc[0]
        best_sub   = sub_margin.index[-1]
        best_val   = sub_margin.iloc[-1]
        insights.append({
            "title": "Sub-Category Margin Spread",
            "tone": "blue",
            "color": "blue",
            "text": (
                f"<b>{worst_sub}</b> has the lowest average margin at <b>{worst_val:.1f}%</b>, "
                f"while <b>{best_sub}</b> leads at <b>{best_val:.1f}%</b>. "
                f"A {best_val - worst_val:.0f} pp spread suggests significant opportunity "
                f"to re-price or discontinue underperforming lines."
            )
        })

    # --- 5. Loss-making orders ---
    loss_orders = df[df["profit"] < 0]
    loss_pct    = len(loss_orders) / len(df) * 100 if len(df) else 0
    loss_value  = loss_orders["profit"].sum()
    tone        = "warning" if loss_pct > 15 else "blue"
    insights.append({
        "title": "Loss-Making Transactions",
        "tone": tone,
        "color": "amber" if tone == "warning" else "blue",
        "text": (
            f"<b>{loss_pct:.1f}%</b> of orders are loss-making, "
            f"eroding <b>${abs(loss_value):,.0f}</b> in total profit. "
            + ("This is above a healthy threshold — root cause analysis by region and discount band is advised."
               if loss_pct > 15
               else "Loss-making order rate is within a manageable range.")
        )
    })

    return insights


PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="DM Sans",
    font_color="rgba(255,255,255,0.75)",
    title_font_family="Syne",
    margin=dict(l=10, r=10, t=50, b=10),
)


# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def get_data():
    return load_and_clean_data("SuperStoreOrders - SuperStoreOrders.csv")

df = get_data()


# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown('<p class="section-label">Filters</p>', unsafe_allow_html=True)

    selected_region = st.multiselect(
        "Region",
        options=sorted(df["region"].dropna().unique()),
        default=sorted(df["region"].dropna().unique())
    )
    selected_category = st.multiselect(
        "Category",
        options=sorted(df["category"].dropna().unique()),
        default=sorted(df["category"].dropna().unique())
    )
    selected_year = st.multiselect(
        "Year",
        options=sorted(df["year"].dropna().unique()),
        default=sorted(df["year"].dropna().unique())
    )

    st.markdown("---")
    st.markdown('<p style="font-size:0.72rem;color:rgba(255,255,255,0.3);letter-spacing:0.5px;">Global Retail · Superstore Dataset</p>', unsafe_allow_html=True)

filtered_df = df[
    df["region"].isin(selected_region) &
    df["category"].isin(selected_category) &
    df["year"].isin(selected_year)
].copy()


# ============================================================
# HEADER
# ============================================================
st.markdown('<p class="section-label">Performance Overview</p>', unsafe_allow_html=True)
st.title("Global Retail Sales & Profit Dashboard")
st.markdown(
    '<p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin-top:-8px;margin-bottom:24px;">'
    'Superstore dataset · Sales, profitability, discount impact, and geographic performance</p>',
    unsafe_allow_html=True
)


# ============================================================
# KPI ROW
# ============================================================
kpis = compute_kpis(filtered_df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales",     f"${kpis['total_sales']:,.0f}")
c2.metric("Total Profit",    f"${kpis['total_profit']:,.0f}")
c3.metric("Total Orders",    f"{kpis['total_orders']:,}")
c4.metric("Profit Margin",   f"{kpis['margin']:.1f}%")
c5.metric("Avg Order Value", f"${kpis['avg_order']:,.0f}")

st.markdown("---")


# ============================================================
# ROW 1 — Sales by Category  |  Profit by Region
# ============================================================
col_l, col_r = st.columns(2)

with col_l:
    st.markdown('<p class="section-label">Revenue Mix</p>', unsafe_allow_html=True)
    sales_cat = filtered_df.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    fig1 = px.bar(sales_cat, x="category", y="sales", color="category",
                  text_auto=".2s", title="Sales by Category",
                  color_discrete_sequence=["#63b3ed", "#76e4f7", "#9f7aea"])
    fig1.update_layout(**PLOTLY_THEME, showlegend=False,
                       xaxis_title="", yaxis_title="Sales ($)")
    fig1.update_traces(marker_line_width=0)
    st.plotly_chart(fig1, use_container_width=True)

with col_r:
    st.markdown('<p class="section-label">Regional Profitability</p>', unsafe_allow_html=True)
    profit_reg = filtered_df.groupby("region", as_index=False)["profit"].sum().sort_values("profit", ascending=False)
    colors = ["#68d391" if v >= 0 else "#fc8181" for v in profit_reg["profit"]]
    fig2 = px.bar(profit_reg, x="region", y="profit", text_auto=".2s",
                  title="Profit by Region")
    fig2.update_traces(marker_color=colors, marker_line_width=0)
    fig2.update_layout(**PLOTLY_THEME, showlegend=False,
                       xaxis_title="", yaxis_title="Profit ($)")
    st.plotly_chart(fig2, use_container_width=True)


# ============================================================
# ROW 2 — Monthly Trend (full width)
# ============================================================
st.markdown('<p class="section-label">Sales Trend</p>', unsafe_allow_html=True)
monthly = filtered_df.groupby("month", as_index=False)["sales"].sum().sort_values("month")
fig3 = px.area(monthly, x="month", y="sales", title="Monthly Sales Trend",
               color_discrete_sequence=["#63b3ed"])
fig3.update_traces(fill="tozeroy", fillcolor="rgba(99,179,237,0.08)", line_width=2)
fig3.update_layout(**PLOTLY_THEME, xaxis_title="", yaxis_title="Sales ($)")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# ============================================================
# ROW 3 — Profit Margin by Sub-Category  |  Profit vs Sales Quadrant
# ============================================================
st.markdown('<p class="section-label">Strategic Analysis</p>', unsafe_allow_html=True)
col_l2, col_r2 = st.columns(2)

with col_l2:
    if "sub_category" in filtered_df.columns:
        sub_perf = (
            filtered_df.groupby("sub_category")
            .agg(sales=("sales", "sum"), profit=("profit", "sum"))
            .assign(margin=lambda x: x["profit"] / x["sales"] * 100)
            .sort_values("margin")
            .reset_index()
        )
        bar_colors = ["#fc8181" if m < 0 else "#63b3ed" if m < 15 else "#68d391"
                      for m in sub_perf["margin"]]
        fig4 = go.Figure(go.Bar(
            x=sub_perf["margin"], y=sub_perf["sub_category"],
            orientation="h",
            marker_color=bar_colors,
            marker_line_width=0,
            text=[f"{m:.1f}%" for m in sub_perf["margin"]],
            textposition="outside",
            textfont=dict(size=10)
        ))
        fig4.update_layout(**PLOTLY_THEME, title="Profit Margin by Sub-Category",
                           xaxis_title="Margin (%)", yaxis_title="",
                           height=420)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Sub-category column not found.")

with col_r2:
    # BCG-style Sales vs Profit quadrant
    if "sub_category" in filtered_df.columns:
        quad_df = (
            filtered_df.groupby("sub_category")
            .agg(sales=("sales", "sum"), profit=("profit", "sum"),
                 orders=("order_id" if "order_id" in filtered_df.columns else "sales", "count"))
            .reset_index()
        )
        med_sales  = quad_df["sales"].median()
        med_profit = quad_df["profit"].median()

        fig5 = px.scatter(
            quad_df, x="sales", y="profit", text="sub_category",
            size="orders", size_max=40,
            color="profit",
            color_continuous_scale=["#fc8181", "#f6ad55", "#68d391"],
            title="Sales vs Profit by Sub-Category"
        )
        # Quadrant lines
        fig5.add_hline(y=med_profit, line_dash="dot",
                       line_color="rgba(255,255,255,0.15)", line_width=1)
        fig5.add_vline(x=med_sales, line_dash="dot",
                       line_color="rgba(255,255,255,0.15)", line_width=1)
        fig5.update_traces(textposition="top center",
                           textfont=dict(size=9, color="rgba(255,255,255,0.6)"),
                           marker_line_width=0)
        fig5.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                           xaxis_title="Sales ($)", yaxis_title="Profit ($)",
                           height=420)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        # Fallback: discount vs profit scatter
        scatter_df = filtered_df[["discount", "profit", "category"]].dropna().sample(
            min(800, len(filtered_df)), random_state=42)
        fig5 = px.scatter(scatter_df, x="discount", y="profit", color="category",
                          title="Discount vs Profit",
                          color_discrete_sequence=["#63b3ed", "#76e4f7", "#9f7aea"])
        fig5.update_layout(**PLOTLY_THEME, xaxis_title="Discount", yaxis_title="Profit ($)")
        st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")


# ============================================================
# ROW 4 — Top Tables
# ============================================================
st.markdown('<p class="section-label">Top Performers</p>', unsafe_allow_html=True)
col_t1, col_t2 = st.columns(2)

with col_t1:
    top_customers = (
        filtered_df.groupby("customer_name", as_index=False)
        .agg(Sales=("sales", "sum"), Orders=("sales", "count"),
             Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False).head(10)
        .assign(**{"Margin %": lambda x: (x["Profit"] / x["Sales"] * 100).round(1)})
        .rename(columns={"customer_name": "Customer"})
        .reset_index(drop=True)
    )
    top_customers.index += 1
    st.markdown("**Top 10 Customers by Sales**")
    st.dataframe(top_customers, use_container_width=True)

with col_t2:
    top_products = (
        filtered_df.groupby("product_name", as_index=False)
        .agg(Sales=("sales", "sum"), Qty=("quantity", "sum") if "quantity" in filtered_df.columns else ("sales", "count"),
             Profit=("profit", "sum"))
        .sort_values("Sales", ascending=False).head(10)
        .assign(**{"Margin %": lambda x: (x["Profit"] / x["Sales"] * 100).round(1)})
        .rename(columns={"product_name": "Product"})
        .reset_index(drop=True)
    )
    top_products.index += 1
    st.markdown("**Top 10 Products by Sales**")
    st.dataframe(top_products, use_container_width=True)

st.markdown("---")


# ============================================================
# ROW 5 — Discount vs Profit  |  Global Map
# ============================================================
col_d, col_m = st.columns([1, 1])

with col_d:
    st.markdown('<p class="section-label">Discount Impact</p>', unsafe_allow_html=True)
    if "discount" in filtered_df.columns:
        disc_df = filtered_df[["discount", "profit", "category"]].dropna()
        disc_df = disc_df.sample(min(800, len(disc_df)), random_state=42)
        fig6 = px.scatter(disc_df, x="discount", y="profit", color="category",
                          opacity=0.6, title="Discount vs Profit",
                          color_discrete_sequence=["#63b3ed", "#76e4f7", "#9f7aea"])
        fig6.update_layout(**PLOTLY_THEME,
                           xaxis_title="Discount Rate", yaxis_title="Profit ($)")
        fig6.update_traces(marker_size=5, marker_line_width=0)
        st.plotly_chart(fig6, use_container_width=True)

with col_m:
    st.markdown('<p class="section-label">Geographic View</p>', unsafe_allow_html=True)
    if "country" in filtered_df.columns:
        country_sales = filtered_df.groupby("country", as_index=False)["sales"].sum()
        fig_map = px.choropleth(
            country_sales, locations="country", locationmode="country names",
            color="sales", hover_name="country",
            color_continuous_scale=[[0, "#1a365d"], [0.5, "#2b6cb0"], [1, "#63b3ed"]],
            title="Sales by Country"
        )
        fig_map.update_layout(**PLOTLY_THEME,
                              geo=dict(showframe=False, showcoastlines=True,
                                       bgcolor="rgba(0,0,0,0)",
                                       projection_type="equirectangular"),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Country column not found — map unavailable.")

st.markdown("---")


# ============================================================
# ANIMATED MARKET CHART
# ============================================================
if "market" in filtered_df.columns:
    st.markdown('<p class="section-label">Animated View</p>', unsafe_allow_html=True)
    anim_df = (
        filtered_df.groupby(["month", "market"], as_index=False)["sales"]
        .sum().sort_values("month")
    )
    fig_anim = px.bar(anim_df, x="market", y="sales", color="market",
                      animation_frame="month", title="Sales by Market Over Time",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_anim.update_layout(**PLOTLY_THEME, showlegend=False,
                           xaxis_title="", yaxis_title="Sales ($)")
    st.plotly_chart(fig_anim, use_container_width=True)
    st.markdown("---")


# ============================================================
# AI-STYLE BUSINESS INSIGHTS
# ============================================================
st.markdown('<p class="section-label">Business Insights</p>', unsafe_allow_html=True)
st.markdown("### Analytical Insights")
st.markdown(
    '<p style="color:rgba(255,255,255,0.4);font-size:0.85rem;margin-top:-8px;margin-bottom:18px;">'
    'Derived from the filtered dataset — updated dynamically with your selections.</p>',
    unsafe_allow_html=True
)

if not filtered_df.empty:
    insights = generate_insights(filtered_df)
    for ins in insights:
        tone_class  = ins["tone"]
        color_class = ins["color"]
        st.markdown(f"""
        <div class="insight-card {tone_class}">
            <div class="insight-title {color_class}">{ins['title']}</div>
            {ins['text']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No data available for the current filter selection.")

st.markdown("---")


# ============================================================
# DOWNLOAD + RAW DATA
# ============================================================
st.markdown('<p class="section-label">Export</p>', unsafe_allow_html=True)
col_dl, _ = st.columns([1, 3])
with col_dl:
    st.download_button(
        label="⬇  Download Filtered Data (CSV)",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_retail_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with st.expander("Show Filtered Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)

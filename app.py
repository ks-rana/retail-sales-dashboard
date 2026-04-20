import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Universal Analytics Engine",
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

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .stSubheader { font-family: 'Syne', sans-serif !important; letter-spacing: -0.3px; }
.main { background: #0a0f1e; padding-top: 1.2rem; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px 18px;
    transition: border-color 0.2s ease;
}
[data-testid="stMetric"]:hover { border-color: rgba(99,179,237,0.35); }
[data-testid="stMetricLabel"] {
    font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.2px;
    color: rgba(255,255,255,0.45) !important; font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important; font-size: 1.85rem !important; font-weight: 700;
}

.section-label {
    font-family: 'Syne', sans-serif; font-size: 0.68rem; letter-spacing: 2px;
    text-transform: uppercase; color: #63b3ed; margin-bottom: 4px; margin-top: 28px;
}
.insight-card {
    background: linear-gradient(135deg, rgba(99,179,237,0.06) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(99,179,237,0.15); border-left: 3px solid #63b3ed;
    padding: 16px 20px; border-radius: 12px; margin-bottom: 10px;
    font-size: 0.9rem; line-height: 1.6; color: rgba(255,255,255,0.82);
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
.insight-title { font-family: 'Syne', sans-serif; font-size: 0.72rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }
.insight-title.blue  { color: #63b3ed; }
.insight-title.amber { color: #f6ad55; }
.insight-title.green { color: #68d391; }
.insight-title.red   { color: #fc8181; }

.health-ok    { color: #68d391; font-weight: 600; }
.health-warn  { color: #f6ad55; font-weight: 600; }
.health-error { color: #fc8181; font-weight: 600; }

.upload-zone {
    border: 2px dashed rgba(99,179,237,0.3); border-radius: 16px;
    padding: 40px; text-align: center; margin: 20px 0;
    background: rgba(99,179,237,0.03);
}
.filter-toggle {
    display: inline-block; padding: 5px 14px; margin: 3px;
    border: 1px solid rgba(99,179,237,0.3); border-radius: 20px;
    font-size: 0.78rem; cursor: pointer; transition: all 0.2s;
}

hr { border-color: rgba(255,255,255,0.06) !important; }
[data-testid="stSidebar"] { background: #0d1324 !important; border-right: 1px solid rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PLOTLY THEME
# ============================================================
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
# HELPER: DETECT COLUMN TYPES
# ============================================================
def detect_columns(df):
    """Auto-detect likely column roles from column names."""
    suggestions = {
        "sales":     None, "profit":    None, "date":      None,
        "category":  None, "sub_category": None, "region": None,
        "customer":  None, "product":   None, "discount":  None,
        "quantity":  None, "country":   None, "market":    None,
    }
    name_map = {
        "sales":        ["sales", "revenue", "income", "amount", "total_sales", "gmv", "turnover"],
        "profit":       ["profit", "net_profit", "earnings", "margin", "net_income", "gain"],
        "date":         ["date", "order_date", "transaction_date", "purchase_date", "created_at", "timestamp"],
        "category":     ["category", "product_category", "type", "segment", "department"],
        "sub_category": ["sub_category", "subcategory", "sub_type", "product_type"],
        "region":       ["region", "zone", "area", "territory", "district"],
        "customer":     ["customer", "customer_name", "client", "buyer", "user_name", "account"],
        "product":      ["product", "product_name", "item", "sku", "product_id"],
        "discount":     ["discount", "discount_rate", "promo", "markdown", "rebate"],
        "quantity":     ["quantity", "qty", "units", "count", "volume"],
        "country":      ["country", "nation", "country_name"],
        "market":       ["market", "channel", "platform", "source"],
    }
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for role, keywords in name_map.items():
        for kw in keywords:
            if kw in cols_lower:
                suggestions[role] = cols_lower[kw]
                break
    return suggestions

# ============================================================
# HELPER: DATA HEALTH CHECK
# ============================================================
def health_check(df, col_map):
    issues = []
    ok = []
    warn = []

    total = len(df)
    ok.append(f"✓ {total:,} rows loaded successfully")

    # Missing values
    for role, col in col_map.items():
        if col and col in df.columns:
            missing = df[col].isna().sum()
            pct = missing / total * 100
            if pct > 20:
                issues.append(f"⚠ **{col}** has {pct:.1f}% missing values — insights may be unreliable")
            elif pct > 5:
                warn.append(f"△ **{col}** has {pct:.1f}% missing values")
            else:
                ok.append(f"✓ **{col}** — {missing} nulls ({pct:.1f}%)")

    # Numeric check
    for role in ["sales", "profit", "discount", "quantity"]:
        col = col_map.get(role)
        if col and col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                issues.append(f"✕ **{col}** mapped as {role} but isn't numeric — check formatting")

    # Negative sales
    sales_col = col_map.get("sales")
    if sales_col and sales_col in df.columns:
        neg = (df[sales_col] < 0).sum()
        if neg > 0:
            warn.append(f"△ {neg} rows have negative sales values — may indicate returns/credits")

    # Date parse check
    date_col = col_map.get("date")
    if date_col and date_col in df.columns:
        parsed = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        failed = parsed.isna().sum()
        if failed > total * 0.1:
            issues.append(f"⚠ {failed} rows failed date parsing in **{date_col}** — trend charts may be incomplete")
        else:
            ok.append(f"✓ Dates parsed in **{date_col}**")

    return {"ok": ok, "warn": warn, "issues": issues}

# ============================================================
# HELPER: PREPARE DATAFRAME
# ============================================================
def prepare_df(df, col_map):
    """Rename mapped columns to standard names and coerce types."""
    rename = {v: k for k, v in col_map.items() if v and v in df.columns}
    df = df.rename(columns=rename).copy()

    for num_col in ["sales", "profit", "discount", "quantity"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["date"])
        df["year"]  = df["date"].dt.year
        df["month"] = df["date"].dt.strftime("%Y-%m")

    if "sales" in df.columns and "profit" in df.columns:
        df["profit_margin"] = df["profit"] / df["sales"].replace(0, np.nan) * 100

    return df

# ============================================================
# HELPER: KPIs
# ============================================================
def compute_kpis(df):
    total_sales  = df["sales"].sum()  if "sales"  in df.columns else 0
    total_profit = df["profit"].sum() if "profit" in df.columns else 0
    id_col = next((c for c in ["order_id","id","transaction_id"] if c in df.columns), None)
    total_orders = df[id_col].nunique() if id_col else len(df)
    margin   = (total_profit / total_sales * 100) if total_sales else 0
    avg_order = (total_sales / total_orders) if total_orders else 0
    return dict(total_sales=total_sales, total_profit=total_profit,
                total_orders=total_orders, margin=margin, avg_order=avg_order)

# ============================================================
# HELPER: INSIGHTS
# ============================================================
def generate_insights(df):
    insights = []

    # 1. Revenue trend
    if "month" in df.columns and "sales" in df.columns:
        monthly = df.groupby("month")["sales"].sum().sort_index()
        if len(monthly) >= 6:
            recent = monthly.iloc[-3:].mean()
            prior  = monthly.iloc[-6:-3].mean()
            pct    = ((recent - prior) / prior * 100) if prior else 0
            tone   = "positive" if pct > 0 else "warning"
            insights.append({
                "title": "Revenue Trend", "tone": tone,
                "color": "green" if tone == "positive" else "amber",
                "text": (
                    f"Revenue is trending <b>{'up' if pct>0 else 'down'} {abs(pct):.1f}%</b> "
                    f"vs the prior quarter. "
                    + ("Momentum is positive." if pct > 0
                       else "Worth investigating whether this is seasonal or structural.")
                )
            })

    # 2. Discount drag
    if "discount" in df.columns and "profit_margin" in df.columns:
        hi = df[df["discount"] >= 0.3]
        lo = df[df["discount"] <  0.3]
        hi_m = hi["profit_margin"].mean() if not hi.empty else 0
        lo_m = lo["profit_margin"].mean() if not lo.empty else 0
        drag = lo_m - hi_m
        pct_hi = len(hi)/len(df)*100 if len(df) else 0
        tone = "warning" if drag > 5 else "blue"
        insights.append({
            "title": "Discount Drag", "tone": tone,
            "color": "amber" if tone=="warning" else "blue",
            "text": (
                f"<b>{pct_hi:.1f}%</b> of transactions use ≥30% discount. "
                f"High-discount orders average <b>{hi_m:.1f}%</b> margin vs "
                f"<b>{lo_m:.1f}%</b> for lower-discount ones — a <b>{drag:.1f}pp gap</b>. "
                + ("Pricing review recommended." if drag > 5
                   else "Discount policy appears controlled.")
            )
        })

    # 3. Concentration risk
    if "customer" in df.columns and "sales" in df.columns:
        cust = df.groupby("customer")["sales"].sum().sort_values(ascending=False)
        top10 = cust.head(10).sum() / cust.sum() * 100 if cust.sum() else 0
        tone = "warning" if top10 > 40 else "positive"
        insights.append({
            "title": "Revenue Concentration", "tone": tone,
            "color": "amber" if tone=="warning" else "green",
            "text": (
                f"Top 10 customers account for <b>{top10:.1f}%</b> of total revenue. "
                + ("This concentration carries customer-exit risk — diversification is recommended."
                   if top10 > 40
                   else "Revenue is reasonably spread across the customer base.")
            )
        })

    # 4. Sub-category spread
    if "sub_category" in df.columns and "profit_margin" in df.columns:
        sub = df.groupby("sub_category")["profit_margin"].mean().sort_values()
        worst = sub.index[0];  worst_v = sub.iloc[0]
        best  = sub.index[-1]; best_v  = sub.iloc[-1]
        insights.append({
            "title": "Margin Spread", "tone": "blue", "color": "blue",
            "text": (
                f"<b>{worst}</b> has the lowest margin at <b>{worst_v:.1f}%</b>; "
                f"<b>{best}</b> leads at <b>{best_v:.1f}%</b>. "
                f"A {best_v-worst_v:.0f}pp spread suggests re-pricing opportunities."
            )
        })

    # 5. Loss-making rate
    if "profit" in df.columns:
        loss = df[df["profit"] < 0]
        pct  = len(loss)/len(df)*100 if len(df) else 0
        val  = loss["profit"].sum()
        tone = "warning" if pct > 15 else "blue"
        insights.append({
            "title": "Loss-Making Transactions", "tone": tone,
            "color": "amber" if tone=="warning" else "blue",
            "text": (
                f"<b>{pct:.1f}%</b> of transactions are loss-making, "
                f"eroding <b>${abs(val):,.0f}</b> in total. "
                + ("Above healthy threshold — root-cause analysis by segment recommended."
                   if pct > 15
                   else "Loss rate is within a manageable range.")
            )
        })

    return insights

# ============================================================
# SESSION STATE
# ============================================================
if "df_raw"  not in st.session_state: st.session_state.df_raw  = None
if "col_map" not in st.session_state: st.session_state.col_map = {}
if "df"      not in st.session_state: st.session_state.df      = None

# ============================================================
# SIDEBAR — UPLOAD + COLUMN MAPPING
# ============================================================
with st.sidebar:
    st.markdown('<p class="section-label">Data Source</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload your dataset (CSV or Excel)",
        type=["csv", "xlsx", "xls"],
        help="Upload any transaction-level dataset. Column mapping comes next."
    )

    # Also allow demo mode with built-in file
    use_demo = st.checkbox("Use built-in demo dataset", value=(st.session_state.df_raw is None and uploaded is None))

    if uploaded is not None:
        try:
            if uploaded.name.endswith((".xlsx", ".xls")):
                raw = pd.read_excel(uploaded)
            else:
                # Try multiple encodings
                try:
                    raw = pd.read_csv(uploaded)
                except UnicodeDecodeError:
                    uploaded.seek(0)
                    raw = pd.read_csv(uploaded, encoding="latin-1")
            st.session_state.df_raw = raw
            use_demo = False
            st.success(f"✓ Loaded {len(raw):,} rows × {len(raw.columns)} columns")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if use_demo:
        try:
            raw = pd.read_csv("SuperStoreOrders - SuperStoreOrders.csv")
            st.session_state.df_raw = raw
            st.info("Using built-in Superstore demo dataset")
        except FileNotFoundError:
            st.warning("Demo file not found. Please upload a dataset.")
            st.session_state.df_raw = None

    # ── COLUMN MAPPING ──
    if st.session_state.df_raw is not None:
        df_raw = st.session_state.df_raw
        all_cols = ["(not available)"] + list(df_raw.columns)
        detected = detect_columns(df_raw)

        st.markdown('<p class="section-label">Column Mapping</p>', unsafe_allow_html=True)
        st.caption("Map your column names to the analytics engine. Auto-detected where possible.")

        def col_select(label, role, required=False):
            default = detected.get(role)
            idx = all_cols.index(default) if default in all_cols else 0
            sel = st.selectbox(
                f"{'★ ' if required else ''}{label}",
                options=all_cols, index=idx,
                key=f"map_{role}"
            )
            return None if sel == "(not available)" else sel

        cm = {}
        cm["sales"]        = col_select("Sales / Revenue",    "sales",        required=True)
        cm["profit"]       = col_select("Profit / Net Income", "profit")
        cm["date"]         = col_select("Date",               "date")
        cm["category"]     = col_select("Category",           "category")
        cm["sub_category"] = col_select("Sub-Category",       "sub_category")
        cm["region"]       = col_select("Region / Zone",      "region")
        cm["customer"]     = col_select("Customer Name",      "customer")
        cm["product"]      = col_select("Product Name",       "product")
        cm["discount"]     = col_select("Discount Rate",      "discount")
        cm["quantity"]     = col_select("Quantity",           "quantity")
        cm["country"]      = col_select("Country",            "country")
        cm["market"]       = col_select("Market / Channel",   "market")

        st.session_state.col_map = cm

        if st.button("▶  Apply Mapping & Analyse", use_container_width=True, type="primary"):
            st.session_state.df = prepare_df(df_raw, cm)
            st.rerun()

        st.markdown("---")
        st.markdown('<p style="font-size:0.72rem;color:rgba(255,255,255,0.3);letter-spacing:0.5px;">Universal Analytics Engine</p>', unsafe_allow_html=True)

# ============================================================
# MAIN — LANDING STATE (no data yet)
# ============================================================
if st.session_state.df is None:
    st.markdown('<p class="section-label">Universal Analytics Engine</p>', unsafe_allow_html=True)
    st.title("Retail & Business Analytics Dashboard")
    st.markdown(
        '<p style="color:rgba(255,255,255,0.45);font-size:0.95rem;margin-top:-8px;margin-bottom:32px;">'
        'Upload any transaction dataset — CSV or Excel — and map your columns to unlock<br>'
        'profitability analysis, discount diagnostics, geographic views, and programmatic business insights.</p>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    for col, icon, title, desc in [
        (c1, "📤", "Upload Any Dataset",   "CSV or Excel. Your column names don't matter — you map them."),
        (c2, "🗺", "Map Your Columns",     "Tell the engine which column is Sales, Profit, Date, etc."),
        (c3, "📊", "Get Strategic Insight","Charts, KPIs, and narrative insights update instantly."),
    ]:
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                    border-radius:16px;padding:24px;text-align:center;">
            <div style="font-size:2rem;margin-bottom:12px;">{icon}</div>
            <div style="font-family:Syne,sans-serif;font-size:1rem;font-weight:600;margin-bottom:8px;">{title}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:0.82rem;line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Start by uploading your file in the sidebar, then map your columns and click **Apply Mapping**.")
    st.stop()

# ============================================================
# MAIN — DASHBOARD (data loaded)
# ============================================================
df = st.session_state.df
cm = st.session_state.col_map

# ── DATA HEALTH AUDIT ──
health = health_check(st.session_state.df_raw, cm)
if health["issues"] or health["warn"]:
    with st.expander(f"🔍 Data Health Audit — {len(health['issues'])} issue(s), {len(health['warn'])} warning(s)", expanded=len(health["issues"]) > 0):
        for msg in health["issues"]:
            st.markdown(f'<span class="health-error">{msg}</span>', unsafe_allow_html=True)
        for msg in health["warn"]:
            st.markdown(f'<span class="health-warn">{msg}</span>', unsafe_allow_html=True)
        for msg in health["ok"][:5]:
            st.markdown(f'<span class="health-ok">{msg}</span>', unsafe_allow_html=True)
else:
    st.success(f"✓ Data health check passed — {len(df):,} rows ready for analysis")

# ── HEADER ──
st.markdown('<p class="section-label">Performance Overview</p>', unsafe_allow_html=True)
dataset_name = st.session_state.get("df_raw", pd.DataFrame()).shape
st.title("Business Analytics Dashboard")
st.markdown(
    f'<p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin-top:-8px;margin-bottom:24px;">'
    f'{len(df):,} rows · {len(df.columns)} columns · '
    f'{"Sales, Profit, and Date available" if all(c in df.columns for c in ["sales","profit","date"]) else "Partial column mapping"}'
    f'</p>',
    unsafe_allow_html=True
)

# ── FILTERS ──
st.markdown('<p class="section-label">Filters</p>', unsafe_allow_html=True)

filter_cols = st.columns(4)
active_filters = {}

# Build toggle-style multiselect filters for available categorical columns
filter_candidates = [
    ("region",   "Region",   0),
    ("category", "Category", 1),
    ("market",   "Market",   2),
]
if "year" in df.columns:
    filter_candidates.append(("year", "Year", 3))

for role, label, col_idx in filter_candidates:
    if role in df.columns:
        options = sorted(df[role].dropna().unique().tolist())
        with filter_cols[col_idx % 4]:
            # "Select all" toggle
            all_key   = f"all_{role}"
            multi_key = f"multi_{role}"

            if all_key not in st.session_state:
                st.session_state[all_key] = True

            toggle = st.toggle(f"All {label}s", value=st.session_state[all_key], key=all_key)

            if toggle:
                active_filters[role] = options
            else:
                chosen = st.multiselect(
                    label, options=options,
                    default=options[:min(3, len(options))],
                    key=multi_key
                )
                active_filters[role] = chosen if chosen else options

# Apply filters
mask = pd.Series([True] * len(df), index=df.index)
for role, vals in active_filters.items():
    if role in df.columns and vals:
        mask &= df[role].isin(vals)
fdf = df[mask].copy()

st.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** rows after filters")
st.markdown("---")

if fdf.empty:
    st.warning("No data matches the current filters. Adjust your selections.")
    st.stop()

# ── KPIs ──
if "sales" in fdf.columns:
    kpis = compute_kpis(fdf)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Sales",     f"${kpis['total_sales']:,.0f}")
    c2.metric("Total Profit",    f"${kpis['total_profit']:,.0f}"    if "profit" in fdf.columns else "N/A")
    c3.metric("Total Records",   f"{kpis['total_orders']:,}")
    c4.metric("Profit Margin",   f"{kpis['margin']:.1f}%"           if "profit" in fdf.columns else "N/A")
    c5.metric("Avg Sale Value",  f"${kpis['avg_order']:,.0f}")
    st.markdown("---")

# ── ROW 1: Category + Region ──
col_l, col_r = st.columns(2)

with col_l:
    if "category" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<p class="section-label">Revenue Mix</p>', unsafe_allow_html=True)
        sc = fdf.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
        fig1 = px.bar(sc, x="category", y="sales", color="category",
                      text_auto=".2s", title="Sales by Category",
                      color_discrete_sequence=["#63b3ed","#76e4f7","#9f7aea","#f6ad55","#68d391"])
        fig1.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
        fig1.update_traces(marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

with col_r:
    if "region" in fdf.columns and "profit" in fdf.columns:
        st.markdown('<p class="section-label">Regional Profitability</p>', unsafe_allow_html=True)
        pr = fdf.groupby("region", as_index=False)["profit"].sum().sort_values("profit", ascending=False)
        colors = ["#68d391" if v >= 0 else "#fc8181" for v in pr["profit"]]
        fig2 = px.bar(pr, x="region", y="profit", text_auto=".2s", title="Profit by Region")
        fig2.update_traces(marker_color=colors, marker_line_width=0)
        fig2.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Profit")
        st.plotly_chart(fig2, use_container_width=True)
    elif "region" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<p class="section-label">Sales by Region</p>', unsafe_allow_html=True)
        sr = fdf.groupby("region", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
        fig2 = px.bar(sr, x="region", y="sales", text_auto=".2s", title="Sales by Region",
                      color_discrete_sequence=["#63b3ed"])
        fig2.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
        st.plotly_chart(fig2, use_container_width=True)

# ── ROW 2: Trend ──
if "month" in fdf.columns and "sales" in fdf.columns:
    st.markdown('<p class="section-label">Sales Trend</p>', unsafe_allow_html=True)
    monthly = fdf.groupby("month", as_index=False)["sales"].sum().sort_values("month")
    fig3 = px.area(monthly, x="month", y="sales", title="Monthly Sales Trend",
                   color_discrete_sequence=["#63b3ed"])
    fig3.update_traces(fill="tozeroy", fillcolor="rgba(99,179,237,0.08)", line_width=2)
    fig3.update_layout(**PLOTLY_THEME, xaxis_title="", yaxis_title="Sales")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("---")

# ── ROW 3: Strategic ──
if "sub_category" in fdf.columns:
    st.markdown('<p class="section-label">Strategic Analysis</p>', unsafe_allow_html=True)
    col_l2, col_r2 = st.columns(2)

    with col_l2:
        if "profit" in fdf.columns and "sales" in fdf.columns:
            sub_perf = (
                fdf.groupby("sub_category")
                .agg(sales=("sales","sum"), profit=("profit","sum"))
                .assign(margin=lambda x: x["profit"]/x["sales"]*100)
                .sort_values("margin")
                .reset_index()
            )
            bar_colors = ["#fc8181" if m < 0 else "#63b3ed" if m < 15 else "#68d391"
                          for m in sub_perf["margin"]]
            fig4 = go.Figure(go.Bar(
                x=sub_perf["margin"], y=sub_perf["sub_category"],
                orientation="h", marker_color=bar_colors, marker_line_width=0,
                text=[f"{m:.1f}%" for m in sub_perf["margin"]], textposition="outside",
                textfont=dict(size=10)
            ))
            fig4.update_layout(**PLOTLY_THEME, title="Profit Margin by Sub-Category",
                               xaxis_title="Margin (%)", yaxis_title="", height=420)
            st.plotly_chart(fig4, use_container_width=True)

    with col_r2:
        if "profit" in fdf.columns and "sales" in fdf.columns:
            id_col = next((c for c in ["order_id","id","transaction_id"] if c in fdf.columns), None)
            agg_d = {"sales":("sales","sum"), "profit":("profit","sum")}
            if id_col: agg_d["orders"] = (id_col,"count")
            quad_df = fdf.groupby("sub_category").agg(**agg_d).reset_index()
            if "orders" not in quad_df.columns:
                quad_df["orders"] = fdf.groupby("sub_category").size().values

            med_s = quad_df["sales"].median()
            med_p = quad_df["profit"].median()
            fig5 = px.scatter(
                quad_df, x="sales", y="profit", text="sub_category",
                size="orders", size_max=40, color="profit",
                color_continuous_scale=["#fc8181","#f6ad55","#68d391"],
                title="Sales vs Profit Quadrant"
            )
            fig5.add_hline(y=med_p, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)
            fig5.add_vline(x=med_s, line_dash="dot", line_color="rgba(255,255,255,0.15)", line_width=1)
            fig5.update_traces(textposition="top center",
                               textfont=dict(size=9, color="rgba(255,255,255,0.6)"),
                               marker_line_width=0)
            fig5.update_layout(**PLOTLY_THEME, coloraxis_showscale=False,
                               xaxis_title="Sales", yaxis_title="Profit", height=420)
            st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")

# ── ROW 4: Top Tables ──
has_customer = "customer" in fdf.columns and "sales" in fdf.columns
has_product  = "product"  in fdf.columns and "sales" in fdf.columns

if has_customer or has_product:
    st.markdown('<p class="section-label">Top Performers</p>', unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        if has_customer:
            agg_d = {"Sales":("sales","sum")}
            if "profit" in fdf.columns: agg_d["Profit"] = ("profit","sum")
            tc = (fdf.groupby("customer").agg(**agg_d)
                  .sort_values("Sales", ascending=False).head(10)
                  .rename_axis("Customer").reset_index())
            if "Profit" in tc.columns:
                tc["Margin %"] = (tc["Profit"]/tc["Sales"]*100).round(1)
            tc.index = range(1, len(tc)+1)
            st.markdown("**Top 10 Customers by Sales**")
            st.dataframe(tc, use_container_width=True)

    with col_t2:
        if has_product:
            agg_d = {"Sales":("sales","sum")}
            if "profit" in fdf.columns:  agg_d["Profit"]   = ("profit","sum")
            if "quantity" in fdf.columns: agg_d["Quantity"] = ("quantity","sum")
            tp = (fdf.groupby("product").agg(**agg_d)
                  .sort_values("Sales", ascending=False).head(10)
                  .rename_axis("Product").reset_index())
            if "Profit" in tp.columns:
                tp["Margin %"] = (tp["Profit"]/tp["Sales"]*100).round(1)
            tp.index = range(1, len(tp)+1)
            st.markdown("**Top 10 Products by Sales**")
            st.dataframe(tp, use_container_width=True)

    st.markdown("---")

# ── ROW 5: Discount + Map ──
col_d, col_m = st.columns([1, 1])

with col_d:
    if "discount" in fdf.columns and "profit" in fdf.columns:
        st.markdown('<p class="section-label">Discount Impact</p>', unsafe_allow_html=True)
        disc_df = fdf[["discount","profit"] + (["category"] if "category" in fdf.columns else [])].dropna()
        disc_df = disc_df.sample(min(800, len(disc_df)), random_state=42)
        fig6 = px.scatter(
            disc_df, x="discount", y="profit",
            color="category" if "category" in disc_df.columns else None,
            opacity=0.6, title="Discount Rate vs Profit",
            color_discrete_sequence=["#63b3ed","#76e4f7","#9f7aea","#f6ad55","#68d391"]
        )
        fig6.update_layout(**PLOTLY_THEME, xaxis_title="Discount Rate", yaxis_title="Profit")
        fig6.update_traces(marker_size=5, marker_line_width=0)
        st.plotly_chart(fig6, use_container_width=True)

with col_m:
    if "country" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<p class="section-label">Geographic View</p>', unsafe_allow_html=True)
        cs = fdf.groupby("country", as_index=False)["sales"].sum()
        fig_map = px.choropleth(
            cs, locations="country", locationmode="country names", color="sales",
            hover_name="country",
            color_continuous_scale=[[0,"#1a365d"],[0.5,"#2b6cb0"],[1,"#63b3ed"]],
            title="Sales by Country"
        )
        fig_map.update_layout(
            **PLOTLY_THEME,
            geo=dict(showframe=False, showcoastlines=True, bgcolor="rgba(0,0,0,0)",
                     projection_type="equirectangular"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_map, use_container_width=True)

# ── ANIMATED CHART ──
if "market" in fdf.columns and "month" in fdf.columns and "sales" in fdf.columns:
    st.markdown("---")
    st.markdown('<p class="section-label">Animated View</p>', unsafe_allow_html=True)
    anim_df = fdf.groupby(["month","market"], as_index=False)["sales"].sum().sort_values("month")
    fig_anim = px.bar(anim_df, x="market", y="sales", color="market",
                      animation_frame="month", title="Sales by Market Over Time",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_anim.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
    st.plotly_chart(fig_anim, use_container_width=True)

st.markdown("---")

# ── BUSINESS INSIGHTS ──
st.markdown('<p class="section-label">Business Insights</p>', unsafe_allow_html=True)
st.markdown("### Analytical Insights")
st.markdown(
    '<p style="color:rgba(255,255,255,0.4);font-size:0.85rem;margin-top:-8px;margin-bottom:18px;">'
    'Derived from the filtered dataset — updated dynamically with your selections.</p>',
    unsafe_allow_html=True
)
insights = generate_insights(fdf)
if insights:
    for ins in insights:
        st.markdown(f"""
        <div class="insight-card {ins['tone']}">
            <div class="insight-title {ins['color']}">{ins['title']}</div>
            {ins['text']}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Map Sales and Profit columns to generate insights.")

st.markdown("---")

# ── EXPORT ──
st.markdown('<p class="section-label">Export</p>', unsafe_allow_html=True)
col_dl, _ = st.columns([1, 3])
with col_dl:
    st.download_button(
        label="⬇  Download Filtered Data (CSV)",
        data=fdf.to_csv(index=False).encode("utf-8"),
        file_name="filtered_data.csv",
        mime="text/csv",
        use_container_width=True
    )

with st.expander("Show Filtered Raw Data"):
    st.dataframe(fdf, use_container_width=True)

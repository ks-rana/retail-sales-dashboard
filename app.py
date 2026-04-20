import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re
from datetime import datetime

st.set_page_config(
    page_title="Universal Analytics Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif;
    background-color: #0b0d11 !important;
    color: #e2dfd8 !important;
}
.main, .block-container { background-color: #0b0d11 !important; padding-top: 1rem; }
[data-testid="stAppViewContainer"] { background-color: #0b0d11 !important; }
[data-testid="stHeader"] { background-color: #0b0d11 !important; }
h1, h2, h3 { font-family: 'Fraunces', serif !important; color: #f0ece4 !important; }

[data-testid="stSidebar"] {
    background: #070910 !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span { color: #9a968e !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #111520 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
    color: #e2dfd8 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span { color: #e2dfd8 !important; }
[data-baseweb="popover"] [data-baseweb="menu"] { background-color: #111520 !important; border: 1px solid rgba(255,255,255,0.1) !important; }
[data-baseweb="popover"] [role="option"] { background-color: #111520 !important; color: #e2dfd8 !important; }
[data-baseweb="popover"] [role="option"]:hover { background-color: #1a2035 !important; color: #c8b870 !important; }

.eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #6a7a9a;
    display: block;
    margin-bottom: 4px;
}
.accent { color: #c8b870; }

/* KPI Cards */
[data-testid="stMetric"] {
    background: #111520;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 16px;
}
[data-testid="stMetric"]:hover { border-color: rgba(200,184,112,0.3); }
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 0.6rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; color: rgba(200,184,112,0.5) !important; }
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif !important; font-size: 1.8rem !important; color: #f0ece4 !important; }

/* Section label */
.slabel {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #c8b870;
    margin-bottom: 4px;
    margin-top: 24px;
    display: block;
}

/* Insight cards */
.insight-card {
    background: #111520;
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #6a7a9a;
    padding: 16px 20px;
    border-radius: 0 10px 10px 0;
    margin-bottom: 10px;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #c8c4bc;
}
.insight-card.warning { border-left-color: #c87840; background: rgba(200,120,64,0.05); }
.insight-card.positive { border-left-color: #5a9a6a; background: rgba(90,154,106,0.05); }
.insight-card.blue { border-left-color: #4a7ab8; background: rgba(74,122,184,0.05); }
.ititle { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
.ititle.amber { color: #c87840; }
.ititle.green { color: #5a9a6a; }
.ititle.blue  { color: #4a7ab8; }
.ititle.gold  { color: #c8b870; }

/* Governance badge */
.gov-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 3px;
    margin: 2px 3px 2px 0;
    background: rgba(200,184,112,0.08);
    color: #c8b870;
    border: 1px solid rgba(200,184,112,0.2);
}

/* Ticket-style finding */
.ticket {
    background: #111520;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 8px;
    display: grid;
    grid-template-columns: 4px 1fr;
    gap: 0 14px;
}
.ticket-bar { border-radius: 4px; }
.ticket-body { }
.ticket-meta { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px; }
.ticket-text { font-size: 0.88rem; color: #e2dfd8; line-height: 1.55; }

.stButton > button {
    background: #111520 !important; color: #e2dfd8 !important;
    border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 7px !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important;
    letter-spacing: 0.5px !important; padding: 9px 20px !important;
}
.stButton > button:hover { background: #1a2035 !important; border-color: rgba(200,184,112,0.4) !important; }

.stDownloadButton button { background: #1a2a18 !important; color: #7ab870 !important; border: 1px solid rgba(122,184,112,0.3) !important; border-radius: 7px !important; font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important; }

.integrity-score {
    background: #111520;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 20px 24px;
    text-align: center;
    margin-bottom: 16px;
}
.int-num { font-family: 'Fraunces', serif; font-size: 3.5rem; font-weight: 700; line-height: 1; }
.int-lbl { font-family: 'DM Mono', monospace; font-size: 0.55rem; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(200,184,112,0.4); margin-top: 4px; }

hr { border-color: rgba(255,255,255,0.05) !important; }
.streamlit-expanderHeader { background: #111520 !important; color: #e2dfd8 !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 9px !important; font-family: 'Instrument Sans', sans-serif !important; }
.streamlit-expanderContent { background: #0d1018 !important; border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 0 0 9px 9px !important; }
[data-testid="stTabs"] button { color: rgba(200,200,195,0.5) !important; font-family: 'DM Mono', monospace !important; font-size: 0.7rem !important; }
[data-testid="stTabs"] button[aria-selected="true"] { color: #e2dfd8 !important; border-bottom-color: #c8b870 !important; }

.pii-warning {
    background: rgba(200,80,64,0.06);
    border: 1px solid rgba(200,80,64,0.2);
    border-left: 3px solid #c85040;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    font-size: 0.84rem;
    color: #e0b0a8;
    line-height: 1.7;
    margin-bottom: 8px;
}

.aia-card {
    background: #111520;
    border: 1px solid rgba(200,184,112,0.15);
    border-radius: 12px;
    padding: 22px 24px;
    margin-bottom: 12px;
}
.aia-level { font-family: 'Fraunces', serif; font-size: 3rem; font-weight: 700; line-height: 1; margin: 6px 0; }
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ───────────────────────────────────────────────────────────
THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="Instrument Sans",
    font_color="rgba(220,216,210,0.75)",
    title_font_family="Fraunces",
    margin=dict(l=10, r=10, t=48, b=10),
)

# ─── PII DETECTION ──────────────────────────────────────────────────────────
PII_PATTERNS = {
    "Email addresses": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "Phone numbers":   r'\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
    "SIN / SSN":       r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
    "Postal codes":    r'\b[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d\b',
    "IP addresses":    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
}
PII_COL_NAMES = ["name", "email", "phone", "address", "dob", "birth", "sin", "ssn", "postal", "ip_address", "first_name", "last_name", "full_name"]

def detect_pii(df, sample_n=200):
    findings = []
    sample = df.sample(min(sample_n, len(df)), random_state=42)
    for col in df.columns:
        col_lower = col.lower().strip()
        # Name-based detection
        if any(kw in col_lower for kw in PII_COL_NAMES):
            findings.append({"col": col, "type": "Column name suggests PII", "risk": "high"})
            continue
        # Content-based detection on string columns
        if df[col].dtype == object:
            col_str = sample[col].dropna().astype(str).str.cat(sep=" ")
            for pii_type, pattern in PII_PATTERNS.items():
                if re.search(pattern, col_str):
                    findings.append({"col": col, "type": pii_type, "risk": "high"})
                    break
    return findings

# ─── DATA INTEGRITY SCORE ───────────────────────────────────────────────────
def integrity_score(df, col_map):
    score = 100
    deductions = []
    total = len(df)
    if total == 0:
        return 0, ["Empty dataset"]

    for role, col in col_map.items():
        if not col or col not in df.columns: continue
        miss_pct = df[col].isna().mean() * 100
        if miss_pct > 20:
            score -= 15
            deductions.append(f"–15 pts: {col} has {miss_pct:.1f}% missing values (critical)")
        elif miss_pct > 5:
            score -= 7
            deductions.append(f"–7 pts: {col} has {miss_pct:.1f}% missing values (moderate)")

    for role in ["sales", "profit", "discount", "quantity"]:
        col = col_map.get(role)
        if col and col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                score -= 10
                deductions.append(f"–10 pts: {col} is non-numeric (type mismatch)")

    if col_map.get("sales") and col_map["sales"] in df.columns:
        neg = (df[col_map["sales"]] < 0).mean() * 100
        if neg > 5:
            score -= 5
            deductions.append(f"–5 pts: {neg:.1f}% negative sales (data quality concern)")

    if col_map.get("date") and col_map["date"] in df.columns:
        parsed = pd.to_datetime(df[col_map["date"]], errors="coerce", dayfirst=True)
        fail = parsed.isna().mean() * 100
        if fail > 10:
            score -= 8
            deductions.append(f"–8 pts: {fail:.1f}% date parse failures")

    dup_pct = df.duplicated().mean() * 100
    if dup_pct > 5:
        score -= 5
        deductions.append(f"–5 pts: {dup_pct:.1f}% duplicate rows")

    return max(0, int(score)), deductions

def score_color(s):
    if s >= 85: return "#5a9a6a", "Sound"
    if s >= 65: return "#c8b870", "Adequate"
    if s >= 45: return "#c87840", "Caution"
    return "#c85040", "Unreliable"

# ─── AIA IMPACT LEVEL ───────────────────────────────────────────────────────
def aia_assessment(df, col_map):
    """Simplified AIA-style scoring based on Canada.ca Directive methodology."""
    raw_score = 0
    notes = []

    if len(df) > 10000:
        raw_score += 2
        notes.append("Large dataset scale (+2)")
    if col_map.get("customer") and col_map["customer"] in df.columns:
        raw_score += 2
        notes.append("Personal customer data present (+2)")
    if col_map.get("date") and col_map["date"] in df.columns:
        raw_score += 1
        notes.append("Temporal data — audit trail implications (+1)")
    if col_map.get("discount") and col_map["discount"] in df.columns:
        raw_score += 1
        notes.append("Pricing decisions with potential equity impact (+1)")
    if col_map.get("country") and col_map["country"] in df.columns:
        raw_score += 3
        notes.append("Cross-jurisdictional data (+3)")
    pii = detect_pii(df)
    if pii:
        raw_score += 3
        notes.append(f"PII detected in {len(pii)} column(s) (+3)")

    # Mitigation score (based on data health)
    iscore, _ = integrity_score(df, col_map)
    mitigation = int(iscore * 0.7)

    # Level determination (mirrors AIA methodology)
    if raw_score >= 10: level = 4
    elif raw_score >= 7: level = 3
    elif raw_score >= 4: level = 2
    else: level = 1

    level_labels = {1: "Minimal", 2: "Moderate", 3: "Significant", 4: "High"}
    level_colors = {1: "#5a9a6a", 2: "#c8b870", 3: "#c87840", 4: "#c85040"}

    return {
        "raw_score": raw_score,
        "mitigation": mitigation,
        "level": level,
        "label": level_labels[level],
        "color": level_colors[level],
        "notes": notes,
    }

# ─── COLUMN DETECTION ───────────────────────────────────────────────────────
def detect_columns(df):
    name_map = {
        "sales":        ["sales","revenue","income","amount","total_sales","gmv","turnover"],
        "profit":       ["profit","net_profit","earnings","net_income","gain"],
        "date":         ["date","order_date","transaction_date","purchase_date","created_at","timestamp"],
        "category":     ["category","product_category","type","segment","department"],
        "sub_category": ["sub_category","subcategory","sub_type","product_type"],
        "region":       ["region","zone","area","territory","district"],
        "customer":     ["customer","customer_name","client","buyer","user_name","account"],
        "product":      ["product","product_name","item","sku"],
        "discount":     ["discount","discount_rate","promo","markdown","rebate"],
        "quantity":     ["quantity","qty","units","count","volume"],
        "country":      ["country","nation","country_name"],
        "market":       ["market","channel","platform","source"],
    }
    cols_lower = {c.lower().strip(): c for c in df.columns}
    out = {}
    for role, kws in name_map.items():
        for kw in kws:
            if kw in cols_lower:
                out[role] = cols_lower[kw]; break
        else:
            out[role] = None
    return out

# ─── PREPARE ────────────────────────────────────────────────────────────────
def prepare_df(df, col_map):
    rename = {v: k for k, v in col_map.items() if v and v in df.columns}
    df = df.rename(columns=rename).copy()
    for nc in ["sales","profit","discount","quantity"]:
        if nc in df.columns:
            df[nc] = pd.to_numeric(df[nc], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["date"])
        df["year"]  = df["date"].dt.year
        df["month"] = df["date"].dt.strftime("%Y-%m")
    if "sales" in df.columns and "profit" in df.columns:
        df["profit_margin"] = df["profit"] / df["sales"].replace(0, np.nan) * 100
    return df

def compute_kpis(df):
    ts  = df["sales"].sum()  if "sales"  in df.columns else 0
    tp  = df["profit"].sum() if "profit" in df.columns else 0
    idc = next((c for c in ["order_id","id","transaction_id"] if c in df.columns), None)
    to  = df[idc].nunique() if idc else len(df)
    return dict(ts=ts, tp=tp, to=to,
                margin=(tp/ts*100) if ts else 0,
                avg=(ts/to) if to else 0)

def generate_insights(df):
    insights = []
    if "month" in df.columns and "sales" in df.columns:
        mo = df.groupby("month")["sales"].sum().sort_index()
        if len(mo) >= 6:
            r,p = mo.iloc[-3:].mean(), mo.iloc[-6:-3].mean()
            pct = ((r-p)/p*100) if p else 0
            tone = "positive" if pct>0 else "warning"
            insights.append({"title":"Revenue Trend","tone":tone,"color":"green" if tone=="positive" else "amber",
                "text":f"Revenue is trending <b>{'up' if pct>0 else 'down'} {abs(pct):.1f}%</b> vs prior quarter. "
                       +("Momentum positive." if pct>0 else "Investigate whether seasonal or structural.")})
    if "discount" in df.columns and "profit_margin" in df.columns:
        hi = df[df["discount"]>=0.3]; lo = df[df["discount"]<0.3]
        hm = hi["profit_margin"].mean() if not hi.empty else 0
        lm = lo["profit_margin"].mean() if not lo.empty else 0
        drag = lm-hm; pct_hi = len(hi)/len(df)*100 if len(df) else 0
        tone = "warning" if drag>5 else "blue"
        insights.append({"title":"Discount Drag","tone":tone,"color":"amber" if tone=="warning" else "blue",
            "text":f"<b>{pct_hi:.1f}%</b> of transactions use ≥30% discount. "
                   f"High-discount orders: <b>{hm:.1f}%</b> margin vs <b>{lm:.1f}%</b> — <b>{drag:.1f}pp gap</b>. "
                   +("Pricing review recommended." if drag>5 else "Discount policy controlled.")})
    if "customer" in df.columns and "sales" in df.columns:
        cu = df.groupby("customer")["sales"].sum().sort_values(ascending=False)
        t10 = cu.head(10).sum()/cu.sum()*100 if cu.sum() else 0
        tone = "warning" if t10>40 else "positive"
        insights.append({"title":"Revenue Concentration","tone":tone,"color":"amber" if tone=="warning" else "green",
            "text":f"Top 10 customers: <b>{t10:.1f}%</b> of total revenue. "
                   +("Concentration risk — diversification recommended." if t10>40 else "Revenue well-distributed.")})
    if "sub_category" in df.columns and "profit_margin" in df.columns:
        sub = df.groupby("sub_category")["profit_margin"].mean().sort_values()
        w, wv = sub.index[0], sub.iloc[0]; b, bv = sub.index[-1], sub.iloc[-1]
        insights.append({"title":"Margin Spread","tone":"blue","color":"blue",
            "text":f"<b>{w}</b> lowest margin at <b>{wv:.1f}%</b>; <b>{b}</b> leads at <b>{bv:.1f}%</b>. "
                   f"{bv-wv:.0f}pp spread signals repricing opportunity."})
    if "profit" in df.columns:
        ls = df[df["profit"]<0]; pct = len(ls)/len(df)*100 if len(df) else 0; val = ls["profit"].sum()
        tone = "warning" if pct>15 else "blue"
        insights.append({"title":"Loss-Making Transactions","tone":tone,"color":"amber" if tone=="warning" else "blue",
            "text":f"<b>{pct:.1f}%</b> of transactions loss-making, eroding <b>${abs(val):,.0f}</b>. "
                   +("Above threshold — root-cause analysis recommended." if pct>15 else "Within manageable range.")})
    return insights

# ─── SESSION STATE ───────────────────────────────────────────────────────────
for k, v in [("df_raw",None),("col_map",{}),("df",None),("redact_pii",False)]:
    if k not in st.session_state: st.session_state[k] = v

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="slabel">Data Source</span>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload dataset (CSV or Excel)", type=["csv","xlsx","xls"],
        help="Upload any transaction-level dataset.")
    use_demo = st.checkbox("Use built-in demo dataset",
        value=(st.session_state.df_raw is None and uploaded is None))

    if uploaded is not None:
        try:
            if uploaded.name.endswith((".xlsx",".xls")):
                raw = pd.read_excel(uploaded)
            else:
                try: raw = pd.read_csv(uploaded)
                except: uploaded.seek(0); raw = pd.read_csv(uploaded, encoding="latin-1")
            st.session_state.df_raw = raw
            use_demo = False
            st.success(f"✓ {len(raw):,} rows × {len(raw.columns)} cols loaded")
        except Exception as e:
            st.error(f"Read error: {e}")

    if use_demo:
        try:
            raw = pd.read_csv("SuperStoreOrders - SuperStoreOrders.csv")
            st.session_state.df_raw = raw
            st.info("Using Superstore demo dataset")
        except FileNotFoundError:
            st.warning("Demo file not found. Upload a dataset.")
            st.session_state.df_raw = None

    if st.session_state.df_raw is not None:
        df_raw = st.session_state.df_raw
        all_cols = ["(not available)"] + list(df_raw.columns)
        detected = detect_columns(df_raw)

        st.markdown('<span class="slabel">Column Mapping</span>', unsafe_allow_html=True)
        st.caption("Map your headers to the analytics engine.")

        def cs(label, role, req=False):
            d = detected.get(role)
            idx = all_cols.index(d) if d in all_cols else 0
            sel = st.selectbox(f"{'★ ' if req else ''}{label}", all_cols, index=idx, key=f"m_{role}")
            return None if sel == "(not available)" else sel

        cm = {}
        cm["sales"]        = cs("Sales / Revenue",     "sales",        req=True)
        cm["profit"]       = cs("Profit / Net Income",  "profit")
        cm["date"]         = cs("Date",                 "date")
        cm["category"]     = cs("Category",             "category")
        cm["sub_category"] = cs("Sub-Category",         "sub_category")
        cm["region"]       = cs("Region",               "region")
        cm["customer"]     = cs("Customer Name",        "customer")
        cm["product"]      = cs("Product Name",         "product")
        cm["discount"]     = cs("Discount Rate",        "discount")
        cm["quantity"]     = cs("Quantity",             "quantity")
        cm["country"]      = cs("Country",              "country")
        cm["market"]       = cs("Market / Channel",     "market")
        st.session_state.col_map = cm

        st.markdown("---")
        st.markdown('<span class="slabel">Privacy Controls</span>', unsafe_allow_html=True)
        st.session_state.redact_pii = st.toggle("Redact PII in charts", value=st.session_state.redact_pii,
            help="Replaces customer names with anonymised IDs in all visualisations.")

        if st.button("▶  Apply & Analyse", use_container_width=True, type="primary"):
            st.session_state.df = prepare_df(df_raw, cm)
            st.rerun()

        st.markdown("---")
        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.58rem;color:rgba(150,145,140,0.35);letter-spacing:1px;">Universal Analytics Engine · v2.0</p>', unsafe_allow_html=True)

# ─── LANDING ─────────────────────────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown('<span class="slabel">Universal Analytics Engine</span>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:2.8rem;font-weight:300;letter-spacing:-1px;margin-bottom:6px;">Business Analytics<br><span style="font-style:italic;color:#c8b870;">& Governance Dashboard</span></h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:rgba(200,200,190,0.5);font-size:0.92rem;margin-bottom:32px;max-width:580px;">Upload any transaction dataset — CSV or Excel — map your columns, and unlock profitability analysis, governance auditing, PII detection, and AIA-style risk scoring.</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    for c, ico, title, desc in [
        (cols[0],"◎","Upload Any Dataset","CSV or Excel. Column names don't matter — you map them."),
        (cols[1],"◈","Integrity Scorecard","Automated data health audit with a 0–100 governance score."),
        (cols[2],"◉","PII Detection","Identifies personally identifiable information before analysis."),
        (cols[3],"◻","AIA Risk Level","Canada.ca–style algorithmic impact level 1–4 assessment."),
    ]:
        c.markdown(f"""
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:20px 18px;">
            <div style="font-size:1.3rem;color:#c8b870;margin-bottom:10px;">{ico}</div>
            <div style="font-family:'Fraunces',serif;font-size:0.95rem;color:#f0ece4;margin-bottom:6px;">{title}</div>
            <div style="font-size:0.78rem;color:rgba(200,200,190,0.45);line-height:1.5;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Upload your file in the sidebar, map columns, and click **Apply & Analyse**.")
    st.stop()

# ─── DASHBOARD ───────────────────────────────────────────────────────────────
df = st.session_state.df
cm = st.session_state.col_map
df_raw = st.session_state.df_raw

# Apply redaction
if st.session_state.redact_pii and "customer" in df.columns:
    cust_map = {v: f"Customer_{i+1:04d}" for i, v in enumerate(df["customer"].dropna().unique())}
    df = df.copy(); df["customer"] = df["customer"].map(cust_map).fillna("Unknown")

# ── GOVERNANCE HEADER ────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Governance Overview</span>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size:2.2rem;font-weight:300;letter-spacing:-0.8px;margin-bottom:4px;">Business Analytics Dashboard</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-bottom:20px;font-family:\'DM Mono\',monospace;letter-spacing:0.5px;">{len(df):,} rows · {len(df.columns)} columns · {datetime.today().strftime("%B %d, %Y")}</p>', unsafe_allow_html=True)

# Governance summary row
iscore, ideductions = integrity_score(df_raw, cm)
pii_hits = detect_pii(df_raw)
aia = aia_assessment(df_raw, cm)
sc_color, sc_label = score_color(iscore)

g1, g2, g3, g4 = st.columns(4)
for col, val, lbl, color, sub in [
    (g1, f"{iscore}", "Data Integrity Score", sc_color, sc_label),
    (g2, f"{len(pii_hits)}", "PII Risk Columns", "#c85040" if pii_hits else "#5a9a6a", "Detected" if pii_hits else "Clean"),
    (g3, f"{aia['raw_score']}", "AIA Raw Impact", aia["color"], f"Level {aia['level']} · {aia['label']}"),
    (g4, "OSFI E-23", "Framework Ref", "#c8b870", "Model Risk Alignment"),
]:
    col.markdown(f"""
    <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:18px 16px;text-align:center;">
        <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:600;color:{color};">{val}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:2px;text-transform:uppercase;color:rgba(200,184,112,0.4);margin:4px 0 2px;">{lbl}</div>
        <div style="font-size:0.75rem;color:rgba(200,200,190,0.5);">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────────────────
tab_analytics, tab_governance, tab_aia = st.tabs(["◎  Analytics", "◈  Governance Audit", "◻  AIA Assessment"])

with tab_analytics:
    # Filters
    st.markdown('<span class="slabel">Filters</span>', unsafe_allow_html=True)
    fc = st.columns(4)
    active = {}
    for (role, label, ci) in [("region","Region",0),("category","Category",1),("market","Market",2)]:
        if role in df.columns:
            opts = sorted(df[role].dropna().unique().tolist())
            with fc[ci]:
                all_key = f"all_{role}"
                if all_key not in st.session_state: st.session_state[all_key] = True
                tog = st.toggle(f"All {label}s", value=st.session_state[all_key], key=all_key)
                if tog: active[role] = opts
                else:
                    ch = st.multiselect(label, opts, default=opts[:min(3,len(opts))], key=f"ms_{role}")
                    active[role] = ch if ch else opts
    if "year" in df.columns:
        opts = sorted(df["year"].dropna().unique().tolist())
        with fc[3]:
            all_key = "all_year"
            if all_key not in st.session_state: st.session_state[all_key] = True
            tog = st.toggle("All Years", value=st.session_state[all_key], key=all_key)
            if tog: active["year"] = opts
            else:
                ch = st.multiselect("Year", opts, default=opts, key="ms_year")
                active["year"] = ch if ch else opts

    mask = pd.Series([True]*len(df), index=df.index)
    for role, vals in active.items():
        if role in df.columns and vals: mask &= df[role].isin(vals)
    fdf = df[mask].copy()
    st.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** rows")
    st.markdown("---")

    if fdf.empty:
        st.warning("No data matches current filters.")
        st.stop()

    # KPIs
    if "sales" in fdf.columns:
        kpis = compute_kpis(fdf)
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Sales",    f"${kpis['ts']:,.0f}")
        c2.metric("Total Profit",   f"${kpis['tp']:,.0f}"    if "profit" in fdf.columns else "N/A")
        c3.metric("Total Records",  f"{kpis['to']:,}")
        c4.metric("Profit Margin",  f"{kpis['margin']:.1f}%" if "profit" in fdf.columns else "N/A")
        c5.metric("Avg Sale Value", f"${kpis['avg']:,.0f}")
        st.markdown("---")

    col_l, col_r = st.columns(2)
    with col_l:
        if "category" in fdf.columns and "sales" in fdf.columns:
            st.markdown('<span class="slabel">Revenue Mix</span>', unsafe_allow_html=True)
            sc2 = fdf.groupby("category",as_index=False)["sales"].sum().sort_values("sales",ascending=False)
            fig = px.bar(sc2,x="category",y="sales",color="category",text_auto=".2s",
                         title="Sales by Category",
                         color_discrete_sequence=["#c8b870","#7ab8d0","#9a7ab8","#c87840","#5a9a6a"])
            fig.update_layout(**THEME,showlegend=False,xaxis_title="",yaxis_title="Sales")
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
    with col_r:
        if "region" in fdf.columns and "profit" in fdf.columns:
            st.markdown('<span class="slabel">Regional Profitability</span>', unsafe_allow_html=True)
            pr = fdf.groupby("region",as_index=False)["profit"].sum().sort_values("profit",ascending=False)
            colors = ["#5a9a6a" if v>=0 else "#c85040" for v in pr["profit"]]
            fig = px.bar(pr,x="region",y="profit",text_auto=".2s",title="Profit by Region")
            fig.update_traces(marker_color=colors,marker_line_width=0)
            fig.update_layout(**THEME,showlegend=False,xaxis_title="",yaxis_title="Profit")
            st.plotly_chart(fig, use_container_width=True)

    if "month" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<span class="slabel">Sales Trend</span>', unsafe_allow_html=True)
        mo = fdf.groupby("month",as_index=False)["sales"].sum().sort_values("month")
        fig = px.area(mo,x="month",y="sales",title="Monthly Sales Trend",color_discrete_sequence=["#c8b870"])
        fig.update_traces(fill="tozeroy",fillcolor="rgba(200,184,112,0.06)",line_width=2)
        fig.update_layout(**THEME,xaxis_title="",yaxis_title="Sales")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    if "sub_category" in fdf.columns:
        st.markdown('<span class="slabel">Strategic Analysis</span>', unsafe_allow_html=True)
        cl2, cr2 = st.columns(2)
        with cl2:
            if "profit" in fdf.columns and "sales" in fdf.columns:
                sp = (fdf.groupby("sub_category").agg(sales=("sales","sum"),profit=("profit","sum"))
                      .assign(margin=lambda x: x["profit"]/x["sales"]*100).sort_values("margin").reset_index())
                bc = ["#c85040" if m<0 else "#6a7a9a" if m<15 else "#5a9a6a" for m in sp["margin"]]
                fig = go.Figure(go.Bar(x=sp["margin"],y=sp["sub_category"],orientation="h",
                                       marker_color=bc,marker_line_width=0,
                                       text=[f"{m:.1f}%" for m in sp["margin"]],textposition="outside",
                                       textfont=dict(size=10)))
                fig.update_layout(**THEME,title="Profit Margin by Sub-Category",
                                  xaxis_title="Margin (%)",yaxis_title="",height=420)
                st.plotly_chart(fig, use_container_width=True)
        with cr2:
            if "profit" in fdf.columns and "sales" in fdf.columns:
                idc = next((c for c in ["order_id","id","transaction_id"] if c in fdf.columns),None)
                ad = {"sales":("sales","sum"),"profit":("profit","sum")}
                if idc: ad["orders"] = (idc,"count")
                qd = fdf.groupby("sub_category").agg(**ad).reset_index()
                if "orders" not in qd.columns: qd["orders"] = fdf.groupby("sub_category").size().values
                fig = px.scatter(qd,x="sales",y="profit",text="sub_category",size="orders",size_max=40,
                                 color="profit",color_continuous_scale=["#c85040","#c87840","#5a9a6a"],
                                 title="Sales vs Profit Quadrant")
                fig.add_hline(y=qd["profit"].median(),line_dash="dot",line_color="rgba(255,255,255,0.1)")
                fig.add_vline(x=qd["sales"].median(),line_dash="dot",line_color="rgba(255,255,255,0.1)")
                fig.update_traces(textposition="top center",textfont=dict(size=9,color="rgba(200,200,190,0.6)"),marker_line_width=0)
                fig.update_layout(**THEME,coloraxis_showscale=False,xaxis_title="Sales",yaxis_title="Profit",height=420)
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

    # Top tables
    hc = "customer" in fdf.columns and "sales" in fdf.columns
    hp = "product" in fdf.columns and "sales" in fdf.columns
    if hc or hp:
        st.markdown('<span class="slabel">Top Performers</span>', unsafe_allow_html=True)
        ct1, ct2 = st.columns(2)
        with ct1:
            if hc:
                ad = {"Sales":("sales","sum")}
                if "profit" in fdf.columns: ad["Profit"] = ("profit","sum")
                tc = (fdf.groupby("customer").agg(**ad).sort_values("Sales",ascending=False).head(10)
                      .rename_axis("Customer").reset_index())
                if "Profit" in tc.columns: tc["Margin %"] = (tc["Profit"]/tc["Sales"]*100).round(1)
                tc.index = range(1, len(tc)+1)
                st.markdown("**Top 10 Customers**")
                st.dataframe(tc, use_container_width=True)
        with ct2:
            if hp:
                ad = {"Sales":("sales","sum")}
                if "profit" in fdf.columns: ad["Profit"] = ("profit","sum")
                if "quantity" in fdf.columns: ad["Qty"] = ("quantity","sum")
                tp = (fdf.groupby("product").agg(**ad).sort_values("Sales",ascending=False).head(10)
                      .rename_axis("Product").reset_index())
                if "Profit" in tp.columns: tp["Margin %"] = (tp["Profit"]/tp["Sales"]*100).round(1)
                tp.index = range(1, len(tp)+1)
                st.markdown("**Top 10 Products**")
                st.dataframe(tp, use_container_width=True)
        st.markdown("---")

    cd, cm2 = st.columns(2)
    with cd:
        if "discount" in fdf.columns and "profit" in fdf.columns:
            st.markdown('<span class="slabel">Discount Impact</span>', unsafe_allow_html=True)
            dd = fdf[["discount","profit"]+(['category'] if 'category' in fdf.columns else [])].dropna()
            dd = dd.sample(min(800,len(dd)),random_state=42)
            fig = px.scatter(dd,x="discount",y="profit",color="category" if "category" in dd.columns else None,
                             opacity=0.6,title="Discount Rate vs Profit",
                             color_discrete_sequence=["#c8b870","#7ab8d0","#9a7ab8","#c87840","#5a9a6a"])
            fig.update_layout(**THEME,xaxis_title="Discount Rate",yaxis_title="Profit")
            fig.update_traces(marker_size=5,marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
    with cm2:
        if "country" in fdf.columns and "sales" in fdf.columns:
            st.markdown('<span class="slabel">Geographic View</span>', unsafe_allow_html=True)
            cs3 = fdf.groupby("country",as_index=False)["sales"].sum()
            fig = px.choropleth(cs3,locations="country",locationmode="country names",color="sales",
                                hover_name="country",color_continuous_scale=[[0,"#1a1f2a"],[0.5,"#3a4a6a"],[1,"#c8b870"]],
                                title="Sales by Country")
            fig.update_layout(**THEME,geo=dict(showframe=False,showcoastlines=True,bgcolor="rgba(0,0,0,0)",
                              projection_type="equirectangular"),coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

    if "market" in fdf.columns and "month" in fdf.columns and "sales" in fdf.columns:
        st.markdown("---")
        adf = fdf.groupby(["month","market"],as_index=False)["sales"].sum().sort_values("month")
        fig = px.bar(adf,x="market",y="sales",color="market",animation_frame="month",
                     title="Sales by Market Over Time",color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(**THEME,showlegend=False,xaxis_title="",yaxis_title="Sales")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown('<span class="slabel">Analytical Insights</span>', unsafe_allow_html=True)
    st.markdown("### Business Insights")
    st.markdown('<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:16px;">Derived programmatically from filtered dataset. Updated with each filter change.</p>', unsafe_allow_html=True)
    for ins in generate_insights(fdf):
        st.markdown(f"""<div class="insight-card {ins['tone']}">
            <div class="ititle {ins['color']}">{ins['title']}</div>{ins['text']}</div>""",
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">Export</span>', unsafe_allow_html=True)
    cdl, _ = st.columns([1,3])
    with cdl:
        st.download_button("⬇  Download Filtered Data (CSV)",
            data=fdf.to_csv(index=False).encode("utf-8"),
            file_name="filtered_data.csv", mime="text/csv", use_container_width=True)
    with st.expander("Show Raw Data"):
        st.dataframe(fdf, use_container_width=True)

# ─── GOVERNANCE TAB ──────────────────────────────────────────────────────────
with tab_governance:
    st.markdown('<span class="slabel">Data Integrity Scorecard</span>', unsafe_allow_html=True)
    st.markdown("### Data Governance Assessment")
    st.markdown('<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:20px;">Automated pre-analysis health check aligned to OSFI E-23 model soundness expectations.</p>', unsafe_allow_html=True)

    ci1, ci2 = st.columns([1,2])
    with ci1:
        st.markdown(f"""
        <div class="integrity-score">
            <div class="int-lbl">Integrity Score</div>
            <div class="int-num" style="color:{sc_color};">{iscore}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;letter-spacing:1.5px;text-transform:uppercase;color:{sc_color};margin-top:6px;">{sc_label}</div>
            <div style="font-size:0.75rem;color:rgba(200,200,190,0.35);margin-top:8px;">out of 100</div>
        </div>
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:14px 16px;">
            <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:2px;text-transform:uppercase;color:#c8b870;margin-bottom:10px;">Frameworks</div>
            <span class="gov-badge">OSFI E-23</span><span class="gov-badge">ISO 42001</span>
            <span class="gov-badge">NIST AI RMF</span><span class="gov-badge">GC AIA</span>
        </div>
        """, unsafe_allow_html=True)

    with ci2:
        st.markdown('<span class="slabel">Deductions Log</span>', unsafe_allow_html=True)
        if ideductions:
            for d in ideductions:
                color = "#c85040" if "critical" in d else "#c87840"
                st.markdown(f"""
                <div class="ticket">
                    <div style="background:{color};border-radius:3px;"></div>
                    <div class="ticket-body">
                        <div class="ticket-meta" style="color:{color};">Integrity Issue</div>
                        <div class="ticket-text">{d}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("✓ No data integrity issues detected. All mapped columns meet quality thresholds.")

    st.markdown("---")
    st.markdown('<span class="slabel">PII Detection</span>', unsafe_allow_html=True)
    st.markdown("### Privacy Audit")
    st.markdown('<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:16px;">Scans column names and content for personally identifiable information. Aligned to PIPEDA and Canada\'s Privacy Act obligations.</p>', unsafe_allow_html=True)

    if pii_hits:
        st.markdown(f'<div class="pii-warning"><b style="color:#e05040;">⚠ {len(pii_hits)} PII risk column(s) detected.</b> Review before sharing or publishing this analysis. Enable the "Redact PII" toggle in the sidebar to anonymise customer identifiers in charts.</div>', unsafe_allow_html=True)
        for p in pii_hits:
            risk_color = "#c85040" if p["risk"]=="high" else "#c87840"
            st.markdown(f"""
            <div class="ticket">
                <div style="background:{risk_color};border-radius:3px;"></div>
                <div class="ticket-body">
                    <div class="ticket-meta" style="color:{risk_color};">PII · {p['risk'].upper()} RISK · Column: <b>{p['col']}</b></div>
                    <div class="ticket-text">{p['type']}</div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.success("✓ No PII patterns detected in mapped columns.")

    if st.session_state.redact_pii:
        st.info("🔒 PII redaction is active — customer names replaced with anonymised IDs in charts.")

    st.markdown("---")
    st.markdown('<span class="slabel">Model Transparency</span>', unsafe_allow_html=True)
    st.markdown("### Analytical Method Documentation")
    st.markdown('<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:16px;">Plain-language explanation of how each insight is calculated. Fulfils AIA Level 2 transparency requirements.</p>', unsafe_allow_html=True)

    methods = [
        ("Revenue Trend", "Compares the 3-month rolling average of sales against the prior 3-month period. Flags acceleration (positive) or deceleration (negative). Formula: (recent_avg − prior_avg) / prior_avg × 100.", "#4a7ab8"),
        ("Discount Drag", "Splits transactions at the 30% discount threshold. Calculates average profit margin for each cohort and reports the gap in percentage points. Flags if high-discount margin is >5pp below low-discount margin.", "#c87840"),
        ("Revenue Concentration", "Ranks customers by total sales. Sums top-10 share as % of total. Flags if top-10 exceeds 40% — a heuristic for customer dependency risk (aligned to concentration risk concepts in OSFI E-23).", "#5a9a6a"),
        ("Margin Spread", "Groups transactions by sub-category. Calculates mean profit margin per group. Reports the min and max performers and the spread. Identifies repricing or discontinuation opportunities.", "#4a7ab8"),
        ("Loss-Making Rate", "Counts transactions where profit < 0 as a percentage of total. Reports total value destroyed. Flags if rate exceeds 15% — a threshold above which root-cause investigation is warranted.", "#c87840"),
    ]
    for title, method, color in methods:
        st.markdown(f"""
        <div style="background:#111520;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:16px 20px;margin-bottom:8px;">
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:{color};margin-bottom:6px;">{title}</div>
            <div style="font-size:0.85rem;color:rgba(200,200,190,0.7);line-height:1.65;">{method}</div>
        </div>""", unsafe_allow_html=True)

# ─── AIA TAB ──────────────────────────────────────────────────────────────────
with tab_aia:
    st.markdown('<span class="slabel">Algorithmic Impact Assessment</span>', unsafe_allow_html=True)
    st.markdown("### Canada AIA — Impact Level Estimate")
    st.markdown('<p style="color:rgba(200,200,190,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:20px;">Methodology adapted from the Government of Canada\'s Directive on Automated Decision-Making (Treasury Board Secretariat). This is an educational estimate, not a formal AIA determination.</p>', unsafe_allow_html=True)

    a1, a2 = st.columns([1,2])
    with a1:
        st.markdown(f"""
        <div class="aia-card" style="text-align:center;border-color:{aia['color']}33;">
            <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;color:rgba(200,184,112,0.5);margin-bottom:8px;">Impact Level</div>
            <div class="aia-level" style="color:{aia['color']};">{aia['level']}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.75rem;letter-spacing:1.5px;text-transform:uppercase;color:{aia['color']};margin-bottom:16px;">{aia['label']}</div>
            <div style="display:flex;justify-content:space-around;margin-top:12px;">
                <div>
                    <div style="font-family:'Fraunces',serif;font-size:1.8rem;color:#f0ece4;">{aia['raw_score']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:1.5px;text-transform:uppercase;color:rgba(200,200,190,0.35);">Raw Score</div>
                </div>
                <div style="width:1px;background:rgba(255,255,255,0.06);"></div>
                <div>
                    <div style="font-family:'Fraunces',serif;font-size:1.8rem;color:#f0ece4;">{aia['mitigation']}</div>
                    <div style="font-family:'DM Mono',monospace;font-size:0.52rem;letter-spacing:1.5px;text-transform:uppercase;color:rgba(200,200,190,0.35);">Mitigation</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        level_reqs = {
            1: ["Plain-language notice","Basic explanation of outputs","ADM approval"],
            2: ["All Level 1 requirements","Detailed plain-language explanation on adverse decisions","Peer review by qualified expert","GBA+ assessment","Role-based training"],
            3: ["All Level 2 requirements","Third-party algorithmic audit","Mandatory human review before decision","Bias testing across demographic groups","Deputy Head approval"],
            4: ["All Level 3 requirements","Full independent audit","Parliamentary / public disclosure","Explicit legal authority","Ongoing quality assurance monitoring"],
        }
        st.markdown('<span class="slabel" style="margin-top:16px;">Level Requirements</span>', unsafe_allow_html=True)
        for req in level_reqs[aia["level"]]:
            st.markdown(f'<div style="font-size:0.8rem;color:rgba(200,200,190,0.6);padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04);">◉ {req}</div>', unsafe_allow_html=True)

    with a2:
        st.markdown('<span class="slabel">Score Breakdown</span>', unsafe_allow_html=True)
        for note in aia["notes"]:
            pts = note.split("(")[1].replace(")","") if "(" in note else ""
            desc = note.split(" (+")[0].split(" (+")[0]
            st.markdown(f"""
            <div class="ticket">
                <div style="background:#c8b870;border-radius:3px;"></div>
                <div class="ticket-body">
                    <div class="ticket-meta" style="color:#c8b870;">Impact Factor · {pts}</div>
                    <div class="ticket-text">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<span class="slabel">AIA Scoring Reference</span>', unsafe_allow_html=True)
        ref_rows = [
            ("Raw Score 0–3",   "Level 1 — Minimal",     "#5a9a6a"),
            ("Raw Score 4–6",   "Level 2 — Moderate",    "#c8b870"),
            ("Raw Score 7–9",   "Level 3 — Significant", "#c87840"),
            ("Raw Score 10+",   "Level 4 — High",        "#c85040"),
        ]
        for rng, lbl, col in ref_rows:
            is_current = aia["label"] in lbl
            st.markdown(f"""
            <div style="background:{'#1a2035' if is_current else '#111520'};border:1px solid {'rgba(200,184,112,0.25)' if is_current else 'rgba(255,255,255,0.05)'};
                         border-radius:8px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
                <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:rgba(200,200,190,0.5);">{rng}</div>
                <div style="font-family:'DM Mono',monospace;font-size:0.65rem;color:{col};font-weight:500;">{lbl} {'◀' if is_current else ''}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="background:rgba(200,184,112,0.05);border:1px solid rgba(200,184,112,0.15);border-left:3px solid rgba(200,184,112,0.4);border-radius:0 10px 10px 0;padding:14px 18px;font-size:0.8rem;color:rgba(200,200,190,0.6);line-height:1.75;">
        <b style="color:#c8b870;font-family:'DM Mono',monospace;font-size:0.58rem;letter-spacing:2px;text-transform:uppercase;display:block;margin-bottom:6px;">Important Disclaimer</b>
        This AIA estimate is generated for educational and portfolio demonstration purposes only. It is not a formal AIA determination under the Government of Canada's Directive on Automated Decision-Making. For real automated decision systems, complete the official AIA at <b>canada.ca/aia-tool</b> and consult your institution's legal services.
        </div>""", unsafe_allow_html=True)

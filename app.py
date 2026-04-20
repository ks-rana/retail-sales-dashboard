import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

st.set_page_config(
    page_title="Universal Analytics Engine",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.3px; }
.main { background: #07090f; padding-top: 1rem; }
[data-testid="stAppViewContainer"] { background: #07090f; }
[data-testid="stHeader"] { background: #07090f; }

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 16px;
}
[data-testid="stMetricLabel"] { font-family: 'DM Mono', monospace !important; font-size: 0.62rem !important; letter-spacing: 1.8px !important; text-transform: uppercase !important; color: rgba(255,255,255,0.38) !important; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-size: 1.8rem !important; font-weight: 700 !important; color: #e8e4dc !important; }

.slabel { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 2.5px; text-transform: uppercase; color: #4a7ab8; margin-bottom: 4px; margin-top: 28px; display: block; }

.hero { background: #0d1220; border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 40px 40px 34px; margin-bottom: 22px; }
.hero-tag { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #4a7ab8; border: 1px solid rgba(74,122,184,0.25); background: rgba(74,122,184,0.08); padding: 4px 12px; border-radius: 4px; display: inline-block; margin-bottom: 16px; }
.hero h1 { font-family: 'Syne', sans-serif !important; font-size: 2.2rem !important; font-weight: 800 !important; color: #f0ece4 !important; margin: 0 0 10px 0 !important; letter-spacing: -1px; line-height: 1.1; }
.hero p { color: rgba(232,228,220,0.55) !important; font-size: 0.88rem; margin: 0; line-height: 1.75; max-width: 620px; }

.gov-score-card { background: #0d1220; border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 22px 24px; }
.gov-score-num { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; line-height: 1; }
.gov-score-lbl { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 2px; text-transform: uppercase; color: rgba(232,228,220,0.35); margin-bottom: 6px; }

.ticket { background: #0d1220; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 14px 18px; margin-bottom: 8px; border-left: 3px solid; }
.ticket-id { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 1.5px; text-transform: uppercase; color: rgba(232,228,220,0.35); margin-bottom: 5px; }
.ticket-title { font-size: 0.88rem; color: #e8e4dc; font-weight: 500; line-height: 1.5; margin-bottom: 6px; }
.ticket-meta { font-family: 'DM Mono', monospace; font-size: 0.6rem; color: rgba(232,228,220,0.4); }

.insight-card { background: rgba(74,122,184,0.06); border: 1px solid rgba(74,122,184,0.15); border-left: 3px solid #4a7ab8; padding: 14px 18px; border-radius: 10px; margin-bottom: 8px; font-size: 0.88rem; line-height: 1.65; color: rgba(232,228,220,0.82); }
.insight-card.warning { border-left-color: #d4903a; background: rgba(212,144,58,0.06); border-color: rgba(212,144,58,0.15); }
.insight-card.positive { border-left-color: #4a9a6a; background: rgba(74,154,106,0.06); border-color: rgba(74,154,106,0.15); }
.insight-card.critical { border-left-color: #b83a3a; background: rgba(184,58,58,0.06); border-color: rgba(184,58,58,0.15); }
.insight-title { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
.insight-title.blue { color: #4a7ab8; } .insight-title.amber { color: #d4903a; } .insight-title.green { color: #4a9a6a; } .insight-title.red { color: #b83a3a; }

.pii-banner { background: rgba(212,144,58,0.08); border: 1px solid rgba(212,144,58,0.2); border-left: 3px solid #d4903a; border-radius: 0 10px 10px 0; padding: 14px 18px; margin: 12px 0; font-size: 0.84rem; color: rgba(232,228,220,0.8); line-height: 1.7; }
.pii-banner-title { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #d4903a; margin-bottom: 5px; }

.method-box { background: #0d1220; border: 1px solid rgba(255,255,255,0.07); border-radius: 10px; padding: 18px 20px; margin-bottom: 10px; }
.method-title { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 1.5px; text-transform: uppercase; color: #4a7ab8; margin-bottom: 8px; }
.method-formula { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #7aacde; background: rgba(74,122,184,0.08); border: 1px solid rgba(74,122,184,0.15); border-radius: 6px; padding: 10px 14px; margin: 8px 0; line-height: 1.8; }
.method-desc { font-size: 0.82rem; color: rgba(232,228,220,0.55); line-height: 1.7; }

.reg-tag { display: inline-block; font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 1px; text-transform: uppercase; padding: 3px 8px; border-radius: 4px; margin: 2px 3px 2px 0; background: rgba(74,122,184,0.1); color: #7aacde; border: 1px solid rgba(74,122,184,0.2); }

hr { border-color: rgba(255,255,255,0.06) !important; }
[data-testid="stSidebar"] { background: #080b14 !important; border-right: 1px solid rgba(255,255,255,0.05); }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #c0bcb4 !important; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background: #101520 !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #e0dcd4 !important; border-radius: 6px !important; }
[data-baseweb="popover"] [data-baseweb="menu"] { background: #101520 !important; }
[data-baseweb="popover"] [role="option"] { background: #101520 !important; color: #e0dcd4 !important; }
[data-baseweb="popover"] [role="option"]:hover { background: #1a2540 !important; color: #7aacde !important; }
.stButton > button { background: #0d1220 !important; color: #e0dcd4 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 6px !important; font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.5px !important; }
.stButton > button:hover { background: #141d30 !important; border-color: rgba(74,122,184,0.4) !important; }
.stDownloadButton > button { background: #1a2e52 !important; color: #7aacde !important; border: 1px solid rgba(74,122,184,0.3) !important; border-radius: 6px !important; font-family: 'DM Mono', monospace !important; font-size: 0.72rem !important; }
.streamlit-expanderHeader { background: #0d1220 !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 8px !important; color: #c0bcb4 !important; font-family: 'DM Sans', sans-serif !important; }
.streamlit-expanderContent { background: #0a0e1a !important; border: 1px solid rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)

PLOTLY_THEME = dict(
    template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font_family="DM Sans", font_color="rgba(232,228,220,0.7)", title_font_family="Syne",
    margin=dict(l=10, r=10, t=44, b=10),
)

# ── PII DETECTION ──────────────────────────────────────────────────────────────
PII_PATTERNS = {
    "Full Name":    r"^(customer|client|name|full_name|buyer|person)$",
    "Email":        r"^(email|email_address|contact_email|user_email)$",
    "Phone":        r"^(phone|telephone|mobile|cell|contact_number)$",
    "Address":      r"^(address|street|location|postal|zip|postcode)$",
    "Date of Birth":r"^(dob|date_of_birth|birthdate|birth_date)$",
    "SIN / SSN":    r"^(sin|ssn|social_insurance|social_security)$",
}

def detect_pii(df):
    found = {}
    for col in df.columns:
        c = col.lower().strip()
        for label, pat in PII_PATTERNS.items():
            if re.match(pat, c):
                found[col] = label
                break
    return found

def redact_pii(df, pii_cols):
    df = df.copy()
    for col, label in pii_cols.items():
        if col in df.columns:
            df[col] = [f"{label.split()[0]}_{i+1:04d}" for i in range(len(df))]
    return df

# ── COLUMN DETECTION ───────────────────────────────────────────────────────────
def detect_columns(df):
    suggestions = {k: None for k in ["sales","profit","date","category","sub_category",
                                       "region","customer","product","discount","quantity","country","market"]}
    name_map = {
        "sales":        ["sales","revenue","income","amount","total_sales","gmv","turnover","gross_sales"],
        "profit":       ["profit","net_profit","earnings","net_income","gain","margin_amount"],
        "date":         ["date","order_date","transaction_date","purchase_date","created_at","timestamp","invoice_date"],
        "category":     ["category","product_category","type","segment","department","class"],
        "sub_category": ["sub_category","subcategory","sub_type","product_type","subclass"],
        "region":       ["region","zone","area","territory","district","division"],
        "customer":     ["customer","customer_name","client","buyer","user_name","account","client_name"],
        "product":      ["product","product_name","item","sku","product_id","item_name","product_description"],
        "discount":     ["discount","discount_rate","promo","markdown","rebate","discount_pct"],
        "quantity":     ["quantity","qty","units","count","volume","pieces"],
        "country":      ["country","nation","country_name","geography"],
        "market":       ["market","channel","platform","source","segment_market"],
    }
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for role, keywords in name_map.items():
        for kw in keywords:
            if kw in cols_lower:
                suggestions[role] = cols_lower[kw]
                break
    return suggestions

# ── GOVERNANCE / DATA INTEGRITY SCORECARD ────────────────────────────────────
def governance_score(df, col_map, pii_cols):
    """
    Score out of 100 assessing data integrity and governance readiness.
    Mirrors OSFI E-23 Model Risk / AIA data quality expectations.
    """
    score = 100
    deductions = []
    total = len(df)

    # 1. Missing values
    for role, col in col_map.items():
        if col and col in df.columns:
            pct = df[col].isna().sum() / total * 100
            if pct > 20:
                score -= 15
                deductions.append(("critical", f"MISS-{role.upper()[:6]}", f"**{col}** — {pct:.1f}% missing values (>20% threshold). Insights derived from this column are unreliable.", "Data Completeness"))
            elif pct > 5:
                score -= 6
                deductions.append(("warning", f"MISS-{role.upper()[:6]}", f"**{col}** — {pct:.1f}% missing values (5–20%). Review data collection at source.", "Data Completeness"))

    # 2. Numeric type mismatches
    for role in ["sales","profit","discount","quantity"]:
        col = col_map.get(role)
        if col and col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            score -= 12
            deductions.append(("critical", f"TYPE-{role.upper()[:6]}", f"**{col}** is mapped as numeric ({role}) but contains non-numeric values. Charts and KPIs will be inaccurate.", "Data Type Integrity"))

    # 3. Negative sales
    sales_col = col_map.get("sales")
    if sales_col and sales_col in df.columns:
        _s = pd.to_numeric(df[sales_col], errors="coerce")
        neg = (_s < 0).sum() if pd.api.types.is_numeric_dtype(_s) else 0
        if neg > 0:
            score -= 5
            deductions.append(("warning", "NEG-SALES", f"{neg} rows have negative sales values — may indicate unprocessed returns, credits, or data entry errors. Verify before aggregating.", "Data Validity"))

    # 4. Date parsing
    date_col = col_map.get("date")
    if date_col and date_col in df.columns:
        parsed = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
        failed = parsed.isna().sum()
        if failed > total * 0.1:
            score -= 10
            deductions.append(("critical", "DATE-PARSE", f"{failed} rows ({failed/total*100:.1f}%) failed date parsing. Trend and seasonality analysis will be incomplete.", "Temporal Integrity"))

    # 4b. Discount outlier check
    disc_col = col_map.get("discount")
    if disc_col and disc_col in df.columns:
        _d = pd.to_numeric(df[disc_col], errors="coerce").dropna()
        if len(_d) > 0:
            over100 = int((_d > 1.0).sum())
            over50  = int((_d > 0.5).sum())
            if over100 > 0:
                score -= 8
                deductions.append(("critical", "DISC-OVER", f"{over100} rows have discount >100% — likely data entry errors corrupting Discount Drag analysis.", "Discount Integrity"))
            elif over50 > 0:
                score -= 4
                deductions.append(("warning", "DISC-HIGH", f"{over50} rows have discount >50% — verify these are intentional before drawing pricing conclusions.", "Discount Integrity"))

    # 4c. Proxy column detection
    proxy_hits = detect_proxy_cols(df)
    if proxy_hits:
        score -= 3
        proxy_names = ", ".join(proxy_hits.keys())
        deductions.append(("warning", "PROXY-COL", f"Columns that may proxy for protected characteristics: {proxy_names}. Review under AIA GBA+ and Canadian Human Rights Act.", "Bias & Fairness"))

    # 5. PII exposure
    if pii_cols:
        score -= min(15, len(pii_cols) * 5)
        cols_list = ", ".join(f"**{c}** ({v})" for c, v in pii_cols.items())
        deductions.append(("warning", "PII-EXPOSE", f"Detected likely PII columns: {cols_list}. Consider redacting before sharing or publishing outputs. Privacy by Design principle (PIPEDA / OSFI E-23).", "Privacy & PII"))

    # 6. Concentration: single value dominance
    for role in ["region","category","market"]:
        col = col_map.get(role)
        if col and col in df.columns:
            top_pct = df[col].value_counts(normalize=True).iloc[0] * 100 if len(df[col].dropna()) > 0 else 0
            if top_pct > 80:
                score -= 4
                deductions.append(("warning", f"SKEW-{role.upper()[:5]}", f"**{col}** is dominated by one value ({top_pct:.0f}%). Filters may produce misleading segment comparisons.", "Representativeness"))

    score = max(0, min(100, score))
    return score, deductions

def score_rating(score):
    if score >= 90: return "High Integrity",  "#4a9a6a", "Data meets governance thresholds for reliable analysis."
    if score >= 70: return "Adequate",        "#d4b83a", "Minor issues detected. Review flagged items before sharing results."
    if score >= 50: return "Needs Review",    "#d4903a", "Several data quality issues may affect insight reliability."
    return                  "At Risk",         "#b83a3a", "Significant data quality gaps. Address before using for decisions."
PROXY_COLUMNS = {
    "postal":        "Postal code is a geographic proxy — may encode socioeconomic or ethnic characteristics.",
    "postcode":      "Postal code is a geographic proxy — may encode socioeconomic or ethnic characteristics.",
    "zip":           "ZIP/postal code is a geographic proxy — may encode socioeconomic characteristics.",
    "province":      "Province/state can proxy for demographic groups — flag under Canadian fairness standards.",
    "fsa":           "Forward sortation area is a geographic proxy for demographic composition.",
    "neighbourhood": "Neighbourhood data may proxy for race or income under AIA fairness checks.",
    "neighborhood":  "Neighbourhood data may proxy for race or income under AIA fairness checks.",
}

def detect_proxy_cols(df):
    found = {}
    for col in df.columns:
        c = col.lower().strip()
        for kw, reason in PROXY_COLUMNS.items():
            if kw in c:
                found[col] = reason
                break
    return found

def estimate_aia_level(col_map, pii_cols, df_shape):
    raw = 0
    if col_map.get("customer"): raw += 2
    if col_map.get("country"):  raw += 3
    if col_map.get("date"):     raw += 1
    if pii_cols:                raw += 3
    if df_shape[0] > 10000:    raw += 2
    if raw >= 10: return 4
    if raw >= 7:  return 3
    if raw >= 4:  return 2
    return 1

def build_compliance_report(meta, gov_sc, rat_lbl, gov_issues, pii_cols, proxy_cols, col_map, df_shape, aia_level):
    import datetime
    date = datetime.datetime.today().strftime("%B %d, %Y")
    crit = sum(1 for s,_,_,_ in gov_issues if s=="critical")
    warn = sum(1 for s,_,_,_ in gov_issues if s=="warning")
    lines = [
        "=" * 68,
        "OSFI E-23 / CANADIAN AIA COMPLIANCE REPORT",
        "Universal Analytics Engine — Retail & Business Dashboard",
        "=" * 68,
        f"Model ID       : {meta.get('model_id','RS-DASH-001')}",
        f"Model Version  : {meta.get('version','2.0')}",
        f"Model Owner    : {meta.get('owner','—')}",
        f"Last Validated : {meta.get('validated','—')}",
        f"Currency       : {meta.get('currency','CAD')}",
        f"Report Date    : {date}",
        f"Dataset Shape  : {df_shape[0]:,} rows x {df_shape[1]} columns",
        "",
        "DISCLAIMER",
        "-" * 68,
        "This report is generated by an educational tool and is not a formal",
        "compliance determination or legal opinion. For real model risk management",
        "in federally regulated financial institutions, engage your Model Risk",
        "Officer and consult OSFI Guidelines E-23 and B-13.",
        "",
        "-" * 68,
        "SECTION 1 - DATA GOVERNANCE SCORECARD",
        "-" * 68,
        f"  Score        : {gov_sc} / 100",
        f"  Rating       : {rat_lbl}",
        f"  Issues Found : {len(gov_issues)} ({crit} critical, {warn} warnings)",
        "",
    ]
    if gov_issues:
        lines.append("  Issue Log:")
        for sev, tid, msg, cat in gov_issues:
            lines.append(f"    [{sev.upper()}] {tid} ({cat}): {msg.replace('**','')}")
    else:
        lines.append("  All data quality checks passed.")
    lines += [
        "",
        "-" * 68,
        "SECTION 2 - PRIVACY & PII STATUS",
        "-" * 68,
        f"  PII Columns Detected : {len(pii_cols)}",
    ]
    if pii_cols:
        for col, label in pii_cols.items():
            lines.append(f"    . {col} ({label})")
        lines.append("  Action: Redact before sharing externally (PIPEDA s.4.5).")
    else:
        lines.append("  No PII columns detected.")
    lines += [
        "",
        "-" * 68,
        "SECTION 3 - BIAS PROXY ASSESSMENT",
        "-" * 68,
        f"  Proxy Columns Detected : {len(proxy_cols)}",
    ]
    if proxy_cols:
        for col, reason in proxy_cols.items():
            lines.append(f"    . {col}: {reason}")
        lines.append("  Review under Canadian Human Rights Act and AIA GBA+ requirements.")
    else:
        lines.append("  No geographic or demographic proxy columns detected.")
    lines += [
        "",
        "-" * 68,
        "SECTION 4 - COLUMN MAPPING INVENTORY (OSFI E-23 s.1.1)",
        "-" * 68,
    ]
    for role, col in col_map.items():
        lines.append(f"  {role:<16} -> {col if col else '(not mapped)'}")
    lines += [
        "",
        "-" * 68,
        "SECTION 5 - AIA IMPACT LEVEL ESTIMATE",
        "-" * 68,
        f"  Estimated Level : {aia_level}",
        "  Methodology     : Adapted from GC Directive on Automated Decision-Making",
        "  Note            : This is an educational estimate only.",
        "                    Complete the official AIA at canada.ca/aia-tool.",
        "",
        "-" * 68,
        "SECTION 6 - ANALYTICAL METHODS INVENTORY",
        "-" * 68,
        "  Revenue Trend         | 3-month rolling comparison (quarter-on-quarter)",
        "  Discount Drag         | Margin gap: discount >= 30% vs < 30% cohorts",
        "  Revenue Concentration | Top 10 customer share of total revenue",
        "  Margin Spread         | Best vs worst sub-category by avg profit margin",
        "  Loss-Making Rate      | % transactions where profit < 0",
        "  BCG Quadrant          | Sales vs profit scatter with median quadrant lines",
        "  Integrity Score       | Penalisation model for data quality gaps",
        "",
        "-" * 68,
        "SECTION 7 - VALIDATION SIGN-OFF",
        "-" * 68,
        "",
        "  Model Risk Officer / Independent Reviewer:",
        "",
        "  Name:        _______________________________________________",
        "",
        "  Signature:   _______________________________________________",
        "",
        "  Date:        _______________________________________________",
        "",
        "  Outcome:     [ ] Approved    [ ] Approved with conditions    [ ] Rejected",
        "",
        "  Comments:",
        "  _______________________________________________________________",
        "  _______________________________________________________________",
        "",
        "=" * 68,
        "END OF COMPLIANCE REPORT",
        "=" * 68,
    ]
    return "\n".join(lines)


# ── DATA PREP ─────────────────────────────────────────────────────────────────
def prepare_df(df, col_map):
    rename = {v: k for k, v in col_map.items() if v and v in df.columns}
    df = df.rename(columns=rename).copy()
    for c in ["sales","profit","discount","quantity"]:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
        df = df.dropna(subset=["date"])
        df["year"]  = df["date"].dt.year
        df["month"] = df["date"].dt.strftime("%Y-%m")
    if "sales" in df.columns and "profit" in df.columns:
        df["profit_margin"] = df["profit"] / df["sales"].replace(0, np.nan) * 100
    return df

def compute_kpis(df):
    ts = df["sales"].sum()  if "sales"  in df.columns else 0
    tp = df["profit"].sum() if "profit" in df.columns else 0
    id_col = next((c for c in ["order_id","id","transaction_id"] if c in df.columns), None)
    to = df[id_col].nunique() if id_col else len(df)
    return dict(total_sales=ts, total_profit=tp, total_orders=to,
                margin=(tp/ts*100) if ts else 0, avg_order=(ts/to) if to else 0)

def generate_insights(df):
    insights = []
    if "month" in df.columns and "sales" in df.columns:
        monthly = df.groupby("month")["sales"].sum().sort_index()
        if len(monthly) >= 6:
            recent = monthly.iloc[-3:].mean(); prior = monthly.iloc[-6:-3].mean()
            pct = ((recent-prior)/prior*100) if prior else 0
            tone = "positive" if pct>0 else "warning"
            insights.append({"title":"Revenue Trend","tone":tone,"color":"green" if tone=="positive" else "amber",
                "text":f"Revenue is trending <b>{'up' if pct>0 else 'down'} {abs(pct):.1f}%</b> vs the prior quarter. " +
                       ("Momentum is positive — double down on top segments." if pct>0 else "Investigate whether seasonal or structural.")})
    if "discount" in df.columns and "profit_margin" in df.columns:
        hi = df[df["discount"]>=0.3]; lo = df[df["discount"]<0.3]
        hi_m = hi["profit_margin"].mean() if not hi.empty else 0
        lo_m = lo["profit_margin"].mean() if not lo.empty else 0
        drag = lo_m-hi_m; pct_hi = len(hi)/len(df)*100 if len(df) else 0
        tone = "warning" if drag>5 else "blue"
        insights.append({"title":"Discount Drag","tone":tone,"color":"amber" if tone=="warning" else "blue",
            "text":f"<b>{pct_hi:.1f}%</b> of transactions use ≥30% discount. High-discount orders average <b>{hi_m:.1f}%</b> margin vs <b>{lo_m:.1f}%</b> for lower-discount — a <b>{drag:.1f}pp gap</b>. " +
                   ("Pricing discipline review recommended." if drag>5 else "Discount policy appears controlled.")})
    if "customer" in df.columns and "sales" in df.columns:
        cust = df.groupby("customer")["sales"].sum().sort_values(ascending=False)
        top10 = cust.head(10).sum()/cust.sum()*100 if cust.sum() else 0
        tone = "warning" if top10>40 else "positive"
        insights.append({"title":"Revenue Concentration","tone":tone,"color":"amber" if tone=="warning" else "green",
            "text":f"Top 10 customers account for <b>{top10:.1f}%</b> of total revenue. " +
                   ("Concentration carries customer-exit risk — diversification recommended." if top10>40 else "Revenue is reasonably spread across the customer base.")})
    if "sub_category" in df.columns and "profit_margin" in df.columns:
        sub = df.groupby("sub_category")["profit_margin"].mean().sort_values()
        if len(sub) >= 2:
            worst=sub.index[0]; worst_v=sub.iloc[0]; best=sub.index[-1]; best_v=sub.iloc[-1]
            insights.append({"title":"Margin Spread","tone":"blue","color":"blue",
                "text":f"<b>{worst}</b> has the lowest average margin at <b>{worst_v:.1f}%</b>; <b>{best}</b> leads at <b>{best_v:.1f}%</b>. "
                       f"A {best_v-worst_v:.0f}pp spread signals re-pricing opportunities."})
    if "profit" in df.columns:
        loss = df[df["profit"]<0]; pct = len(loss)/len(df)*100 if len(df) else 0; val = loss["profit"].sum()
        tone = "warning" if pct>15 else "blue"
        insights.append({"title":"Loss-Making Transactions","tone":tone,"color":"amber" if tone=="warning" else "blue",
            "text":f"<b>{pct:.1f}%</b> of orders are loss-making, eroding <b>${abs(val):,.0f}</b> in total. " +
                   ("Above healthy threshold — root-cause by segment and discount band advised." if pct>15 else "Loss rate within a manageable range.")})
    return insights

# ── SESSION STATE ──────────────────────────────────────────────────────────────
for k, v in [("df_raw",None),("col_map",{}),("df",None),("pii_redacted",False)]:
    if k not in st.session_state: st.session_state[k] = v

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<span class="slabel">Model Registry</span>', unsafe_allow_html=True)
    st.caption("OSFI E-23 §1.1 — Model identification and ownership.")
    if "meta" not in st.session_state:
        st.session_state.meta = {"model_id":"RS-DASH-001","version":"2.0","owner":"","validated":"","currency":"CAD"}
    _meta = st.session_state.meta
    _meta["model_id"]  = st.text_input("Model ID",       value=_meta.get("model_id","RS-DASH-001"), key="meta_id")
    _meta["version"]   = st.text_input("Version",        value=_meta.get("version","2.0"),          key="meta_ver")
    _meta["owner"]     = st.text_input("Model Owner",    value=_meta.get("owner",""),               key="meta_own", placeholder="e.g. Khushi Rana")
    _meta["validated"] = st.text_input("Last Validated", value=_meta.get("validated",""),           key="meta_val", placeholder="YYYY-MM-DD")
    _meta["currency"]  = st.selectbox("Currency", ["CAD","USD","GBP","EUR","AUD","Other"],          key="meta_cur",
                           index=["CAD","USD","GBP","EUR","AUD","Other"].index(_meta.get("currency","CAD")))
    st.session_state.meta = _meta
    st.markdown("---")
    st.markdown('<span class="slabel">Data Source</span>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload dataset (CSV or Excel)", type=["csv","xlsx","xls"],
                                help="Upload any transaction-level dataset. Column mapping follows.")
    use_demo = st.checkbox("Use built-in demo dataset", value=(st.session_state.df_raw is None and uploaded is None))

    if uploaded is not None:
        try:
            raw = pd.read_excel(uploaded) if uploaded.name.endswith((".xlsx",".xls")) else pd.read_csv(uploaded)
            st.session_state.df_raw = raw; use_demo = False
            st.success(f"✓ {len(raw):,} rows × {len(raw.columns)} columns loaded")
        except UnicodeDecodeError:
            uploaded.seek(0)
            raw = pd.read_csv(uploaded, encoding="latin-1")
            st.session_state.df_raw = raw; use_demo = False
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

    if st.session_state.df_raw is not None:
        df_raw = st.session_state.df_raw
        all_cols = ["(not available)"] + list(df_raw.columns)
        detected = detect_columns(df_raw)
        pii_cols = detect_pii(df_raw)

        st.markdown('<span class="slabel">Column Mapping</span>', unsafe_allow_html=True)
        st.caption("Map your columns to the engine. Auto-detected where possible.")

        if pii_cols:
            st.markdown(f'<div class="pii-banner"><div class="pii-banner-title">⚠ PII Detected</div>'
                        f'Likely personal data in: {", ".join(pii_cols.keys())}. '
                        f'Enable redaction below before sharing outputs.</div>', unsafe_allow_html=True)

        def col_select(label, role, required=False):
            default = detected.get(role)
            idx = all_cols.index(default) if default in all_cols else 0
            sel = st.selectbox(f"{'★ ' if required else ''}{label}", options=all_cols, index=idx, key=f"map_{role}")
            return None if sel=="(not available)" else sel

        cm = {}
        cm["sales"]        = col_select("Sales / Revenue",     "sales",        required=True)
        cm["profit"]       = col_select("Profit / Net Income",  "profit")
        cm["date"]         = col_select("Date",                 "date")
        cm["category"]     = col_select("Category",             "category")
        cm["sub_category"] = col_select("Sub-Category",         "sub_category")
        cm["region"]       = col_select("Region / Zone",        "region")
        cm["customer"]     = col_select("Customer Name",        "customer")
        cm["product"]      = col_select("Product Name",         "product")
        cm["discount"]     = col_select("Discount Rate",        "discount")
        cm["quantity"]     = col_select("Quantity",             "quantity")
        cm["country"]      = col_select("Country",              "country")
        cm["market"]       = col_select("Market / Channel",     "market")
        st.session_state.col_map = cm

        if pii_cols:
            st.markdown("---")
            st.markdown('<span class="slabel">Privacy Controls</span>', unsafe_allow_html=True)
            st.session_state.pii_redacted = st.toggle("Redact PII for presentation", value=st.session_state.pii_redacted)
            if st.session_state.pii_redacted:
                st.caption("✓ Names and identifiers will be replaced with anonymised IDs in all outputs.")

        st.markdown("---")
        if st.button("▶  Apply Mapping & Analyse", use_container_width=True, type="primary"):
            df_proc = prepare_df(df_raw, cm)
            if st.session_state.pii_redacted and pii_cols:
                df_proc = redact_pii(df_proc, {k: v for k, v in pii_cols.items() if k in df_proc.columns})
            st.session_state.df = df_proc
            st.rerun()

        st.markdown('<p style="font-family:\'DM Mono\',monospace;font-size:0.58rem;color:rgba(200,196,188,0.25);margin-top:16px;letter-spacing:0.5px;">Universal Analytics Engine · v2.0</p>', unsafe_allow_html=True)

# ── LANDING ────────────────────────────────────────────────────────────────────
if st.session_state.df is None:
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">◈ Business Intelligence · Governance-Ready</div>
        <h1>Universal Analytics Engine</h1>
        <p>Upload any transaction dataset and map your columns to unlock profitability analysis, discount diagnostics, geographic views, and programmatic business insights — with built-in data governance scoring, PII detection, and OSFI-aligned data health auditing.</p>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,icon,title,desc in [
        (c1,"◈","Upload Any Dataset","CSV or Excel. Column names don't matter — you map them."),
        (c2,"◎","Map Your Columns","Sales, Profit, Date, Region — auto-detected where possible."),
        (c3,"◻","Governance Scorecard","Data integrity audit before any analysis runs."),
        (c4,"◉","Strategic Insight","BCG quadrant, discount drag, concentration risk — all programmatic."),
    ]:
        col.markdown(f"""
        <div style="background:#0d1220;border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:1.2rem;color:#4a7ab8;margin-bottom:10px;">{icon}</div>
            <div style="font-family:'Syne',sans-serif;font-size:0.88rem;font-weight:700;color:#f0ece4;margin-bottom:6px;">{title}</div>
            <div style="font-size:0.76rem;color:rgba(232,228,220,0.4);line-height:1.6;">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="reg-tag">OSFI E-23 Aligned</span><span class="reg-tag">PIPEDA / GDPR</span><span class="reg-tag">AIA-Aware</span><span class="reg-tag">Privacy by Design</span>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Upload your file in the sidebar, map columns, and click **Apply Mapping & Analyse**.")
    st.stop()

# ── DASHBOARD ──────────────────────────────────────────────────────────────────
df = st.session_state.df
cm = st.session_state.col_map
df_raw_ref = st.session_state.df_raw
pii_cols = detect_pii(df_raw_ref) if df_raw_ref is not None else {}

# ── GOVERNANCE SCORECARD ──────────────────────────────────────────────────────
gov_sc, gov_issues = governance_score(df_raw_ref, cm, pii_cols)
rat_lbl, rat_col, rat_desc = score_rating(gov_sc)

crit_count = sum(1 for s,_,_,_ in gov_issues if s=="critical")
warn_count = sum(1 for s,_,_,_ in gov_issues if s=="warning")

with st.expander(
    f"{'🔴' if crit_count>0 else '🟡' if warn_count>0 else '🟢'} "
    f"Data Governance Scorecard — {gov_sc}/100 · {rat_lbl} · "
    f"{crit_count} critical · {warn_count} warnings",
    expanded=(crit_count > 0)
):
    gc1, gc2, gc3 = st.columns([1, 2, 2])
    with gc1:
        st.markdown(f"""
        <div class="gov-score-card" style="text-align:center;">
            <div class="gov-score-lbl">Integrity Score</div>
            <div class="gov-score-num" style="color:{rat_col};">{gov_sc}</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;letter-spacing:1.5px;text-transform:uppercase;color:{rat_col};margin:6px 0 14px;">{rat_lbl}</div>
            <div style="font-size:0.76rem;color:rgba(232,228,220,0.5);line-height:1.6;">{rat_desc}</div>
        </div>""", unsafe_allow_html=True)
    with gc2:
        st.markdown('<span class="slabel">Issue Log</span>', unsafe_allow_html=True)
        if not gov_issues:
            st.success("All data quality checks passed.")
        for sev, tid, msg, cat in gov_issues:
            border = "#b83a3a" if sev=="critical" else "#d4903a"
            sev_lbl = "CRITICAL" if sev=="critical" else "WARNING"
            st.markdown(f"""
            <div class="ticket" style="border-left-color:{border};">
                <div class="ticket-id">{tid} · {cat} · <span style="color:{border};">{sev_lbl}</span></div>
                <div class="ticket-title">{msg}</div>
            </div>""", unsafe_allow_html=True)
    with gc3:
        st.markdown('<span class="slabel">Regulatory Context</span>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.8rem;color:rgba(232,228,220,0.55);line-height:1.85;background:#0d1220;border:1px solid rgba(255,255,255,0.07);border-radius:10px;padding:16px 18px;">
        <b style="color:#e8e4dc;">OSFI E-23</b> (Model Risk Management, 2027 update) requires models — including analytical dashboards supporting strategic decisions — to maintain documented data quality processes, centralized model inventories, and independent validation pathways.<br><br>
        <b style="color:#e8e4dc;">PIPEDA / GDPR</b> mandate data minimization and PII protection by design. Any column containing personal identifiers should be redacted before outputs are shared externally.<br><br>
        <b style="color:#e8e4dc;">AIA (Canada)</b> Level 2+ systems require audit trails and quality assurance documentation for data used in automated processing.
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── HEADER ──────────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Performance Overview</span>', unsafe_allow_html=True)
st.title("Business Analytics Dashboard")
_meta_hdr = st.session_state.get("meta", {})
_currency = _meta_hdr.get("currency", "CAD")
st.markdown(f'<p style="color:rgba(232,228,220,0.4);font-size:0.82rem;margin-top:-6px;margin-bottom:8px;">'
            f'{len(df):,} rows · {len(df.columns)} columns · '
            f'{"Full mapping" if all(c in df.columns for c in ["sales","profit","date"]) else "Partial mapping"} · '
            f'{"PII Redacted" if st.session_state.pii_redacted else "Standard view"} · Currency: {_currency}</p>', unsafe_allow_html=True)
if _currency == "Other":
    st.warning("Currency set to 'Other' — verify all monetary columns share a single currency. Mixed currencies will cause incorrect KPI totals.")

# ── FILTERS ──────────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Filters</span>', unsafe_allow_html=True)
fcols = st.columns(4)
active_filters = {}
filter_candidates = [("region","Region",0),("category","Category",1),("market","Market",2)]
if "year" in df.columns: filter_candidates.append(("year","Year",3))

for role, label, ci in filter_candidates:
    if role in df.columns:
        options = sorted(df[role].dropna().unique().tolist())
        with fcols[ci % 4]:
            if f"all_{role}" not in st.session_state: st.session_state[f"all_{role}"] = True
            toggle = st.toggle(f"All {label}s", value=st.session_state[f"all_{role}"], key=f"all_{role}")
            if toggle:
                active_filters[role] = options
            else:
                chosen = st.multiselect(label, options=options, default=options[:min(3,len(options))], key=f"multi_{role}")
                active_filters[role] = chosen if chosen else options

mask = pd.Series([True]*len(df), index=df.index)
for role, vals in active_filters.items():
    if role in df.columns and vals: mask &= df[role].isin(vals)
fdf = df[mask].copy()
st.caption(f"Showing **{len(fdf):,}** of **{len(df):,}** rows after filters")
st.markdown("---")

if fdf.empty:
    st.warning("No data matches the current filters."); st.stop()

# ── KPIs ───────────────────────────────────────────────────────────────────────
if "sales" in fdf.columns:
    kpis = compute_kpis(fdf)
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Sales",    f"${kpis['total_sales']:,.0f}")
    c2.metric("Total Profit",   f"${kpis['total_profit']:,.0f}" if "profit" in fdf.columns else "—")
    c3.metric("Total Records",  f"{kpis['total_orders']:,}")
    c4.metric("Profit Margin",  f"{kpis['margin']:.1f}%" if "profit" in fdf.columns else "—")
    c5.metric("Avg Sale Value", f"${kpis['avg_order']:,.0f}")
    st.markdown("---")

# ── ROW 1 ──────────────────────────────────────────────────────────────────────
col_l, col_r = st.columns(2)
with col_l:
    if "category" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<span class="slabel">Revenue Mix</span>', unsafe_allow_html=True)
        sc = fdf.groupby("category",as_index=False)["sales"].sum().sort_values("sales",ascending=False)
        fig1 = px.bar(sc, x="category", y="sales", color="category", text_auto=".2s", title="Sales by Category",
                      color_discrete_sequence=["#4a7ab8","#7aacde","#9f7aea","#d4903a","#4a9a6a"])
        fig1.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
        fig1.update_traces(marker_line_width=0)
        st.plotly_chart(fig1, use_container_width=True)

with col_r:
    if "region" in fdf.columns and "profit" in fdf.columns:
        st.markdown('<span class="slabel">Regional Profitability</span>', unsafe_allow_html=True)
        pr = fdf.groupby("region",as_index=False)["profit"].sum().sort_values("profit",ascending=False)
        fig2 = px.bar(pr, x="region", y="profit", text_auto=".2s", title="Profit by Region")
        fig2.update_traces(marker_color=["#4a9a6a" if v>=0 else "#b83a3a" for v in pr["profit"]], marker_line_width=0)
        fig2.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Profit")
        st.plotly_chart(fig2, use_container_width=True)
    elif "region" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<span class="slabel">Sales by Region</span>', unsafe_allow_html=True)
        sr = fdf.groupby("region",as_index=False)["sales"].sum().sort_values("sales",ascending=False)
        fig2 = px.bar(sr, x="region", y="sales", text_auto=".2s", title="Sales by Region",
                      color_discrete_sequence=["#4a7ab8"])
        fig2.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
        st.plotly_chart(fig2, use_container_width=True)

# ── TREND ──────────────────────────────────────────────────────────────────────
if "month" in fdf.columns and "sales" in fdf.columns:
    st.markdown('<span class="slabel">Sales Trend</span>', unsafe_allow_html=True)
    monthly = fdf.groupby("month",as_index=False)["sales"].sum().sort_values("month")
    fig3 = px.area(monthly, x="month", y="sales", title="Monthly Sales Trend",
                   color_discrete_sequence=["#4a7ab8"])
    fig3.update_traces(fill="tozeroy", fillcolor="rgba(74,122,184,0.08)", line_width=2)
    fig3.update_layout(**PLOTLY_THEME, xaxis_title="", yaxis_title="Sales")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("---")

# ── STRATEGIC ──────────────────────────────────────────────────────────────────
if "sub_category" in fdf.columns:
    st.markdown('<span class="slabel">Strategic Analysis</span>', unsafe_allow_html=True)
    cl2, cr2 = st.columns(2)
    with cl2:
        if "profit" in fdf.columns and "sales" in fdf.columns:
            sub_perf = (fdf.groupby("sub_category").agg(sales=("sales","sum"),profit=("profit","sum"))
                        .assign(margin=lambda x: x["profit"]/x["sales"]*100).sort_values("margin").reset_index())
            bc = ["#b83a3a" if m<0 else "#4a7ab8" if m<15 else "#4a9a6a" for m in sub_perf["margin"]]
            fig4 = go.Figure(go.Bar(x=sub_perf["margin"], y=sub_perf["sub_category"], orientation="h",
                                    marker_color=bc, marker_line_width=0,
                                    text=[f"{m:.1f}%" for m in sub_perf["margin"]], textposition="outside",
                                    textfont=dict(size=9)))
            fig4.update_layout(**PLOTLY_THEME, title="Profit Margin by Sub-Category",
                               xaxis_title="Margin (%)", yaxis_title="", height=420)
            st.plotly_chart(fig4, use_container_width=True)
    with cr2:
        if "profit" in fdf.columns and "sales" in fdf.columns:
            id_col = next((c for c in ["order_id","id","transaction_id"] if c in fdf.columns), None)
            agg_d = {"sales":("sales","sum"),"profit":("profit","sum")}
            if id_col: agg_d["orders"] = (id_col,"count")
            quad_df = fdf.groupby("sub_category").agg(**agg_d).reset_index()
            if "orders" not in quad_df.columns: quad_df["orders"] = fdf.groupby("sub_category").size().values
            fig5 = px.scatter(quad_df, x="sales", y="profit", text="sub_category",
                              size="orders", size_max=40, color="profit",
                              color_continuous_scale=["#b83a3a","#d4903a","#4a9a6a"],
                              title="Sales vs Profit Quadrant (BCG-style)")
            fig5.add_hline(y=quad_df["profit"].median(), line_dash="dot", line_color="rgba(255,255,255,0.12)", line_width=1)
            fig5.add_vline(x=quad_df["sales"].median(),  line_dash="dot", line_color="rgba(255,255,255,0.12)", line_width=1)
            fig5.update_traces(textposition="top center", textfont=dict(size=9,color="rgba(232,228,220,0.55)"), marker_line_width=0)
            fig5.update_layout(**PLOTLY_THEME, coloraxis_showscale=False, xaxis_title="Sales", yaxis_title="Profit", height=420)
            st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")

# ── TOP TABLES ─────────────────────────────────────────────────────────────────
if "customer" in fdf.columns or "product" in fdf.columns:
    st.markdown('<span class="slabel">Top Performers</span>', unsafe_allow_html=True)
    ct1, ct2 = st.columns(2)
    with ct1:
        if "customer" in fdf.columns and "sales" in fdf.columns:
            agg_d = {"Sales":("sales","sum")}
            if "profit" in fdf.columns: agg_d["Profit"]=("profit","sum")
            tc = (fdf.groupby("customer").agg(**agg_d).sort_values("Sales",ascending=False)
                  .head(10).rename_axis("Customer").reset_index())
            if "Profit" in tc.columns: tc["Margin %"]=(tc["Profit"]/tc["Sales"]*100).round(1)
            tc.index = range(1,len(tc)+1)
            st.markdown("**Top 10 Customers by Sales**")
            st.dataframe(tc, use_container_width=True)
    with ct2:
        if "product" in fdf.columns and "sales" in fdf.columns:
            agg_d = {"Sales":("sales","sum")}
            if "profit" in fdf.columns: agg_d["Profit"]=("profit","sum")
            if "quantity" in fdf.columns: agg_d["Qty"]=("quantity","sum")
            tp = (fdf.groupby("product").agg(**agg_d).sort_values("Sales",ascending=False)
                  .head(10).rename_axis("Product").reset_index())
            if "Profit" in tp.columns: tp["Margin %"]=(tp["Profit"]/tp["Sales"]*100).round(1)
            tp.index = range(1,len(tp)+1)
            st.markdown("**Top 10 Products by Sales**")
            st.dataframe(tp, use_container_width=True)
    st.markdown("---")

# ── DISCOUNT + MAP ─────────────────────────────────────────────────────────────
cd, cm2 = st.columns(2)
with cd:
    if "discount" in fdf.columns and "profit" in fdf.columns:
        st.markdown('<span class="slabel">Discount Impact</span>', unsafe_allow_html=True)
        disc_df = fdf[["discount","profit"]+( ["category"] if "category" in fdf.columns else [])].dropna()
        disc_df = disc_df.sample(min(800,len(disc_df)),random_state=42)
        fig6 = px.scatter(disc_df, x="discount", y="profit",
                          color="category" if "category" in disc_df.columns else None,
                          opacity=0.6, title="Discount Rate vs Profit",
                          color_discrete_sequence=["#4a7ab8","#7aacde","#9f7aea","#d4903a","#4a9a6a"])
        fig6.update_layout(**PLOTLY_THEME, xaxis_title="Discount Rate", yaxis_title="Profit")
        fig6.update_traces(marker_size=5, marker_line_width=0)
        st.plotly_chart(fig6, use_container_width=True)
with cm2:
    if "country" in fdf.columns and "sales" in fdf.columns:
        st.markdown('<span class="slabel">Geographic View</span>', unsafe_allow_html=True)
        cs = fdf.groupby("country",as_index=False)["sales"].sum()
        fig_map = px.choropleth(cs, locations="country", locationmode="country names", color="sales",
                                hover_name="country",
                                color_continuous_scale=[[0,"#0d1a2e"],[0.5,"#1e4080"],[1,"#4a7ab8"]],
                                title="Sales by Country")
        fig_map.update_layout(**PLOTLY_THEME,
                              geo=dict(showframe=False,showcoastlines=True,bgcolor="rgba(0,0,0,0)",
                                       projection_type="equirectangular"),
                              coloraxis_showscale=False)
        st.plotly_chart(fig_map, use_container_width=True)

if "market" in fdf.columns and "month" in fdf.columns and "sales" in fdf.columns:
    st.markdown("---")
    st.markdown('<span class="slabel">Animated Market View</span>', unsafe_allow_html=True)
    anim_df = fdf.groupby(["month","market"],as_index=False)["sales"].sum().sort_values("month")
    fig_anim = px.bar(anim_df, x="market", y="sales", color="market", animation_frame="month",
                      title="Sales by Market Over Time",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_anim.update_layout(**PLOTLY_THEME, showlegend=False, xaxis_title="", yaxis_title="Sales")
    st.plotly_chart(fig_anim, use_container_width=True)

st.markdown("---")

# ── INSIGHTS ──────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Analytical Insights</span>', unsafe_allow_html=True)
st.markdown("### Business Intelligence Summary")
st.markdown('<p style="color:rgba(232,228,220,0.38);font-size:0.82rem;margin-top:-6px;margin-bottom:16px;">Programmatically derived from the filtered dataset — logic documented in the Explainability tab below.</p>',
            unsafe_allow_html=True)

insights = generate_insights(fdf)
for ins in insights:
    st.markdown(f"""
    <div class="insight-card {ins['tone']}">
        <div class="insight-title {ins['color']}">{ins['title']}</div>
        {ins['text']}
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── EXPLAINABILITY TAB ────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Analytical Transparency</span>', unsafe_allow_html=True)
st.markdown("### Logic Documentation")
st.markdown('<p style="color:rgba(232,228,220,0.38);font-size:0.82rem;margin-top:-6px;margin-bottom:16px;">All analytical methods are documented below in plain language and formula, aligned to AIA Level 2 explainability requirements.</p>',
            unsafe_allow_html=True)

methods = [
    ("Revenue Trend", "Compares last 3 months vs prior 3 months to identify acceleration or decline.",
     "pct_change = (avg(last 3 months) − avg(prior 3 months)) / avg(prior 3 months) × 100\nFlag: positive → momentum; negative → investigate"),
    ("Discount Drag", "Identifies margin gap between high-discount (≥30%) and low-discount orders.",
     "drag = avg_margin(discount < 0.3) − avg_margin(discount ≥ 0.3)\nFlag: drag > 5pp → pricing discipline review"),
    ("Revenue Concentration", "Calculates % of total revenue from top 10 customers.",
     "concentration = sum(top 10 customer sales) / total_sales × 100\nFlag: > 40% → customer-exit risk"),
    ("Margin Spread", "Identifies best and worst performing sub-categories by average profit margin.",
     "sub_margin = profit / sales × 100, aggregated by sub_category\nFlag: spread > 30pp → re-pricing opportunity"),
    ("Loss-Making Rate", "Calculates proportion of transactions with negative profit.",
     "loss_rate = count(profit < 0) / total_transactions × 100\nFlag: > 15% → root-cause by segment"),
    ("BCG Quadrant", "Plots sub-categories by sales (x) and profit (y) with median lines as quadrant boundaries.",
     "axes: x = total_sales, y = total_profit, per sub_category\nQuadrant lines: median(sales) and median(profit)\nStars = high sales + high profit · Dogs = low both"),
    ("Data Integrity Score", "Penalises dataset for missing values, type errors, PII exposure, and skew.",
     "score starts at 100\n−15 if missing > 20% · −6 if 5–20% · −12 for type mismatch\n−10 for date parse failure · −5 for PII detected · −4 for column skew > 80%"),
]

ec1, ec2 = st.columns(2)
for i, (title, desc, formula) in enumerate(methods):
    col = ec1 if i % 2 == 0 else ec2
    col.markdown(f"""
    <div class="method-box">
        <div class="method-title">{title}</div>
        <div class="method-desc">{desc}</div>
        <div class="method-formula">{formula}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── EXPORT ────────────────────────────────────────────────────────────────────
st.markdown('<span class="slabel">Export & Compliance</span>', unsafe_allow_html=True)

_meta_exp   = st.session_state.get("meta", {})
_proxy_exp  = detect_proxy_cols(df_raw_ref) if df_raw_ref is not None else {}
_aia_lvl    = estimate_aia_level(cm, pii_cols, df_raw_ref.shape if df_raw_ref is not None else (0,0))
_compliance = build_compliance_report(
    _meta_exp, gov_sc, rat_lbl, gov_issues, pii_cols,
    _proxy_exp, cm,
    df_raw_ref.shape if df_raw_ref is not None else (0,0),
    _aia_lvl
)
_fname_comp = f"compliance_report_{_meta_exp.get('model_id','RS-DASH-001')}_{__import__('datetime').datetime.today().strftime('%Y%m%d')}.txt"

exp_c1, exp_c2 = st.columns(2)
with exp_c1:
    st.download_button("⬇  Download Filtered Data (CSV)",
                       data=fdf.to_csv(index=False).encode("utf-8"),
                       file_name="filtered_data.csv", mime="text/csv", use_container_width=True)
with exp_c2:
    st.download_button("⬇  Download Compliance Report (.txt)",
                       data=_compliance.encode("utf-8"),
                       file_name=_fname_comp, mime="text/plain", use_container_width=True)

with st.expander("Show Filtered Raw Data"):
    st.dataframe(fdf, use_container_width=True)

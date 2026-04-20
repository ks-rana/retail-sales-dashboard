# Universal Analytics Engine — RegTech BI Platform

> **Live Dashboard →** [https://retail-sales-dashboard-2glrgrkfmhd5py98ah7jbc.streamlit.app/](https://retail-sales-dashboard-2glrgrkfmhd5py98ah7jbc.streamlit.app/)
> *(Hosted on Streamlit Cloud — may take ~30s to wake up on first load)*

---

## What This Is

This started as a retail analytics dashboard. It's now a **dataset-agnostic Business Intelligence platform** with a built-in Model Risk Governance layer — designed to demonstrate how analytical tools should be built when the outputs support real business decisions.

The tool accepts any CSV or Excel file, maps columns intelligently, runs a pre-analysis data health audit, and generates strategic insights alongside a downloadable compliance report with AIA Impact Level scoring.

---

## Why It Was Built This Way

Raw dashboards tell you *what happened*. This tool asks *why it matters* — and then checks whether the data feeding those conclusions can actually be trusted.

The governance layer exists because of a simple problem: in professional settings, a dashboard is only as reliable as the data behind it. Flagging missing values, type mismatches, and PII exposure *before* charts render prevents decisions made on compromised data.

---

## Key Features

### Analytics Engine
- **Dataset-agnostic ingestion** — upload any CSV or Excel file; the tool auto-detects column roles using heuristic keyword matching (`revenue`, `income`, `gmv` → Sales, etc.)
- **Column mapping sidebar** — 12 roles (Sales, Profit, Date, Category, Sub-Category, Region, Customer, Product, Discount, Quantity, Country, Market); unmapped roles gracefully disappear rather than breaking charts
- **Toggle-style filters** — "All X" toggle per dimension; flip off to expose multiselect. Reduces cognitive load for broad-view users
- **BCG-style Sales vs. Profit Quadrant** — scatter plot with median-line quadrant boundaries; Stars, Cash Cows, Question Marks, Dogs
- **Profit Margin by Sub-Category** — horizontal bar chart colour-coded by performance tier (loss-making / below average / strong)
- **Discount Drag analysis** — quantifies margin gap between high-discount (≥30%) and low-discount orders; identifies the tipping point where discounting destroys margin
- **Revenue Concentration** — flags customer dependency risk if top 10 customers exceed 40% of total sales
- **Choropleth world map** — sales by country
- **Animated market bar chart** — sales by market segment over time
- **Five programmatic insights** — generated from live filtered data, not hardcoded text

### Model Risk Governance Layer

**Model Registry (OSFI E-23 §1.1)**
A sidebar registration form captures Model ID, Version, Model Owner, Last Validated date, and Currency. Treats the dashboard as a registered analytical asset with traceable metadata — the baseline requirement for OSFI model inventory.

**Data Governance Scorecard**
Automated pre-analysis audit scored out of 100. Deductions for:
- Missing values (>5% → warning, >20% → critical, –6 to –15 pts)
- Non-numeric columns mapped to numeric roles (type mismatch, –12 pts)
- Negative sales values (potential return/credit data, –5 pts)
- Date parse failures (affects trend analysis, –10 pts)
- PII column detection (–5 pts per identified column, max –15)
- Single-value column dominance / segment skew (–4 pts)
- Discount outliers >100% (data entry errors, –8 pts critical)
- Bias proxy columns detected (–3 pts)

Results display as ticket-style issue cards with severity labels (CRITICAL / WARNING), category tags, and plain-language explanations of why each issue matters.

**PII Detection & Redaction**
Scans column names against a pattern library (Full Name, Email, Phone, Address, Date of Birth, SIN/SSN). When PII columns are detected, a warning banner appears in the sidebar. A "Redact PII for presentation" toggle replaces all customer names with anonymised IDs (`Full Name_0001`, `Full Name_0002`, etc.) across all charts and tables before rendering — Privacy by Design.

**Bias Proxy Detection**
Flags columns containing `postal`, `postcode`, `zip`, `province`, `fsa`, `neighbourhood` — geographic variables that may proxy for protected demographic characteristics under Canadian Human Rights Act and AIA GBA+ requirements.

**AIA Impact Level Estimation**
Calculates a proxy Raw Impact Score and Mitigation Score using logic adapted from the Government of Canada's Directive on Automated Decision-Making. Outputs an estimated Impact Level 1–4. Not a formal AIA determination — see canada.ca/aia-tool for real deployments.

**Analytical Transparency Documentation**
A "Logic Documentation" section explains how every insight is calculated — formula, threshold, and flag condition — in plain language. Fulfils AIA Level 2 explainability requirements for automated analytical outputs.

**Compliance Report Export**
A downloadable `.txt` report containing:
- Model registry metadata (ID, version, owner, validated date, currency)
- Data Governance Scorecard (score, issue log, regulatory context)
- PII status (detected columns, redaction state)
- Bias proxy assessment
- Column mapping inventory
- AIA Impact Level estimate
- Analytical methods inventory
- Model Risk Officer + Chief Privacy Officer sign-off block with Name, Signature, Date, and Approve/Reject checkboxes

---

## Regulatory Alignment

| Feature | Framework Reference |
|---|---|
| Model Registry | OSFI E-23 §1.1 — Model Inventory |
| Data Quality Audit | OSFI E-23 §2.1 — Conceptual Soundness |
| PII Detection & Redaction | PIPEDA §4.5 · AIA Q58 · Quebec Law 25 |
| Bias Proxy Flagging | Canadian Human Rights Act · AIA GBA+ |
| AIA Impact Level | GC Directive on Automated Decision-Making |
| Explainability Documentation | AIA Level 2 §Explanation |
| Compliance Report Sign-off | OSFI E-23 §4 — Model Ownership |
| Discount Outlier Check | OSFI E-23 §2.1 — Conceptual Soundness |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web application framework |
| Plotly | Interactive charts and maps |
| Pandas | Data ingestion, cleaning, aggregation |
| NumPy | Margin and statistical calculations |
| re | PII pattern matching |

---

## Dataset (Demo Mode)

When no file is uploaded, the tool falls back to the **Superstore Orders** dataset — a widely used retail analytics dataset of ~50,000 orders across product categories, customer segments, regions, and markets globally. The live deployment works without any setup; the CSV is bundled in the repository.

---

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/ks-rana/retail-sales-dashboard.git
cd retail-sales-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

The demo CSV is included. No additional setup needed.

---

## About

Built by **Khushi Rana** — Psychology × AI Governance, University of Waterloo. Currently AI Risk Governance Intern at Rogers Communications.

This project was built to develop hands-on fluency with business intelligence tooling and model risk governance principles — bridging the gap between raw transaction data, strategic decision-making, and Canadian regulatory standards.

[LinkedIn](https://www.linkedin.com/in/khushi-rana-00764223a) · [Portfolio](https://khushi-rana-website.vercel.app/)

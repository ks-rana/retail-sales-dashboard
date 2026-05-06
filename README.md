# Universal Analytics Engine — RegTech BI Platform

A dataset-agnostic business intelligence platform with a built-in OSFI E-23 Model Risk Governance layer. Upload any tabular dataset and receive both standard exploratory analytics and a regulatory governance report aligned to Canadian model risk expectations.

**Live tool:** https://retail-sales-dashboard-2glrgrkfmhd5py98ah7jbc.streamlit.app/
*(Hosted on Streamlit Community Cloud — may take 30 seconds to load on first visit.)*

---

## What this tool does

The platform takes a generic dataset and produces two parallel outputs:

**Analytics layer** — standard exploratory data analysis, summary statistics, and visualizations of the kind you would expect from a BI tool.

**Governance layer** — a Model Risk Governance assessment of the dataset and any modeling done on it, including:

- Automated PII detection across columns
- Canada AIA Impact Level scoring for decisions the dataset could support
- Conceptual soundness audit
- Proxy bias flagging across protected attribute candidates
- Data integrity scorecard
- Downloadable compliance report with sign-off structure

The combination — analytics plus governance — is the differentiator. The point is that *the moment you start analyzing data with any view to model deployment, governance review should be embedded, not bolted on later.*

---

## What I designed

The governance architecture of this tool is mine. I designed:

- **The PII detection logic** — what counts, how to surface it, how to handle ambiguous cases
- **The AIA Impact Level scoring methodology** — proxy mapping of dataset characteristics to Canada AIA Levels I–IV
- **The proxy bias detection approach** — which fields raise flags, the reasoning behind which proxies for protected attributes warrant attention
- **The data integrity scorecard structure** — what dimensions are scored, how scores combine
- **The compliance report format** — sections, sign-off structure, evidence pack expectations
- **The conceptual soundness audit framework** — drawn from OSFI E-23 expectations

## What I did not build from scratch

The Python/Streamlit/Pandas/Plotly implementation was built using AI-assisted development. The code handles file upload, runs the governance checks I designed, generates the visualizations, and assembles the report. The standard analytics layer uses common Pandas/Plotly patterns; the governance layer is the original contribution.

I am being explicit about this because the regulatory thinking is the part of the tool that took expertise. The implementation, while functional, is the kind of thing AI-assisted development handles routinely now.

---

## Why this matters

OSFI Guideline E-23 takes effect for federally regulated financial institutions in 2027. Most BI and analytics tools today have no concept of model risk governance built in — risk review happens after-the-fact, by a different team, often using a different tool. This is a sketch of what it looks like to embed Canadian regulatory expectations into an analytics workflow from the first upload.

The tool is a proof of concept, not an enterprise solution. It demonstrates the architecture of regulation-embedded analytics for a Canadian financial-sector context. A production version would require integration with model inventories, identity and access management, formal validation processes, and actual regulatory review.

---

## Standards referenced

- **OSFI Guideline E-23** — Model Risk Management (Office of the Superintendent of Financial Institutions, 2025)
- **Canada AIA** — Directive on Automated Decision-Making
- **NIST AI Risk Management Framework 1.0**

---

## Contact

Designed and architected by Khushi Rana — Psychology × AI Governance @ University of Waterloo.

- ks2rana@uwaterloo.ca
- linkedin.com/in/khushi-rana
- khushi-rana-website.vercel.app

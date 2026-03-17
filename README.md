Global Retail Sales & Profit Dashboard
An interactive business intelligence dashboard analyzing sales performance, profitability, discount strategy, and geographic distribution across a global retail dataset.
→ View Live Dashboard <!-- https://retail-sales-dashboard-2glrgrkfmhd5py98ah7jbc.streamlit.app/ -->

The Business Problem
Retail organizations generate enormous transaction-level data, but raw data alone doesn't drive decisions. This project asks: where is value being created, where is it being destroyed, and why?
The dashboard is designed to help a business analyst or strategy team answer questions like:

Which product categories and regions are driving — or dragging — profitability?
Are discounts actually growing revenue, or just eroding margin?
Is revenue concentrated in a small number of customers, creating dependency risk?
Which sub-categories should be re-priced, promoted, or discontinued?


Dashboard Features
KPI Overview
Five headline metrics update dynamically with every filter selection: Total Sales, Total Profit, Total Orders, Profit Margin, and Average Order Value.
Revenue & Profitability Analysis

Sales breakdown by product category
Profit by region, with loss-making regions highlighted in red
Monthly sales trend (area chart) showing seasonality and growth trajectory

Strategic Analysis

Profit Margin by Sub-Category — horizontal bar chart colour-coded by performance tier (loss-making, below average, strong), equivalent to a product portfolio review
Sales vs Profit Quadrant — scatter plot positioning each sub-category by revenue size and profitability, styled after BCG-style strategic frameworks

Discount Impact Analysis

Scatter analysis of discount rate vs profit at the transaction level
Insight logic that quantifies the margin gap between high-discount and low-discount orders

Geographic View

Choropleth world map showing sales concentration by country
Animated bar chart showing how sales by market shift over time

Analytical Insights (Dynamic)
Five business insights are generated programmatically from the filtered dataset — not hardcoded text. Each one runs actual logic:
InsightMethodRevenue TrendCompares last 3 months vs prior 3 months, flags acceleration or declineDiscount DragCalculates margin gap between high (≥30%) and low discount ordersRevenue ConcentrationFlags customer concentration risk if top 10 customers exceed 40% of salesSub-Category Margin SpreadIdentifies the best and worst performing lines by average marginLoss-Making RateCalculates % of transactions with negative profit and total value destroyed

Tech Stack
ToolPurposePythonCore languageStreamlitWeb app frameworkPlotlyInteractive charts and mapsPandasData cleaning and aggregationNumPyMargin and statistical calculations

Dataset
Superstore Orders — a widely used retail analytics dataset containing ~50,000 orders across product categories, customer segments, regions, and markets globally. Fields include order date, sales, profit, discount, quantity, shipping cost, customer name, and product details.
Source: commonly distributed via Kaggle as a business analytics teaching dataset.

How to Run Locally
bash# 1. Clone the repo
git clone https://github.com/ks-rana/retail-sales-dashboard.git
cd retail-sales-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
The CSV file is included in the repository — no additional setup needed.

Key Takeaways
A few findings from the full dataset (unfiltered):

High-discount orders (≥ 30% off) consistently produce lower margins than low-discount orders — in some categories, discounting above a threshold flips orders from profitable to loss-making
Revenue concentration in the top customer segment signals dependency risk that would warrant attention in a real business context
Sub-category margin spread is wide, suggesting the product portfolio contains both strong performers and value-destroying lines that a pricing or portfolio review could address


About
Built by Khushi Rana — studying the intersection of Psychology, AI Governance, and data-driven strategy.
This project was built to develop hands-on fluency with business intelligence tooling and to practice translating raw transactional data into structured, decision-relevant insight — skills directly applicable to roles in data analytics, strategy, and risk assurance.
www.linkedin.com/in/khushi-rana-00764223a · [Personal Website: https://khushi-rana-website.vercel.app/ ]

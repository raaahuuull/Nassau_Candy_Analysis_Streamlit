#  Nassau Candy Sales Analysis Dashboard

An interactive data analytics dashboard built using **Python, Streamlit, and Plotly** to analyze sales performance, profitability, and business risks for Nassau Candy products.

---

##  Live Demo
 [https://your-streamlit-link.streamlit.app](https://nassaucandyanalysis-2mplw2rljda4r2uq2tyh3z.streamlit.app/)

---

##  Project Overview

This dashboard provides a complete business analysis of product-level and division-level performance. It enables users to explore revenue trends, profit contribution, and identify high-risk products using interactive visualizations.

---

##  Objectives

- Analyze overall sales and profit performance
- Identify top-performing products using Pareto Analysis
- Detect high-risk products based on margin and sales
- Evaluate cost efficiency across products
- Provide actionable business insights

---

##  Tech Stack

- **Python**
- **Streamlit** (Frontend & App Framework)
- **Pandas** (Data Processing)
- **Plotly** (Interactive Visualizations)

---

##  Features

### Interactive Filters
- Filter data by product division (Chocolate, Sugar, Other)

### Key Performance Indicators (KPIs)
- Total Revenue
- Total Profit
- Overall Margin %

### Division Performance Analysis
- Compare gross margins across divisions

### Pareto Analysis (80/20 Rule)
- Identify top profit-contributing products
- Understand revenue concentration

### Cost vs Sales Diagnostics
- Visualize cost efficiency using scatter plot
- Detect potential loss-making products
- Reference diagonal line for break-even analysis

### High Risk Product Detection
- **Basic Mode** → Low margin (<20%)
- **Advanced Mode** → Low margin + low sales
- Dynamic risk identification with toggle

### Automated Key Insights
- Best performing division
- Weakest division
- Top product
- Profit concentration summary

### Business Recommendations
- Actionable suggestions based on analysis

---

##  Dataset

- Source: Nassau Candy Distributor Dataset
- Loaded via:
  - GitHub (default dataset)
  - Optional CSV upload by user

---

## How to Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/Nassau_Candy_Analysis_Streamlit.git

# Navigate to project folder
cd Nassau_Candy_Analysis_Streamlit

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

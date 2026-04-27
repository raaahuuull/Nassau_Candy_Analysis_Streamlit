import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

# -----------------------------
# LOAD DATA (HYBRID)
# -----------------------------
DEFAULT_URL = "https://raw.githubusercontent.com/raaahuuull/Nassau_Candy_Analysis/refs/heads/main/Nassau%20Candy%20Distributor.csv"

st.sidebar.title("Data Source")

uploaded_file = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.sidebar.success("Using uploaded dataset")
else:
    df = load_data(DEFAULT_URL)
    st.sidebar.info("Using default dataset")

# -----------------------------
# CLEANING
# -----------------------------
numeric_cols = ['Total_Sales', 'Total_Profit', 'Total_Units',
                'Gross_Margin_Pct', 'Profit_per_Unit']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.markdown("### Filters")

divisions = st.sidebar.multiselect(
    "Select Division",
    df['Division'].unique(),
    default=df['Division'].unique()
)

filtered_df = df[df['Division'].isin(divisions)]

# -----------------------------
# CONTROLS (TOGGLES)
# -----------------------------
st.sidebar.markdown("### Analysis Controls")

risk_mode = st.sidebar.radio(
    "High Risk Definition",
    ["Basic (Margin < 20%)", "Advanced (Low Margin + Low Sales)"]
)

pareto_threshold = st.sidebar.slider(
    "Pareto Threshold (%)",
    60, 95, 80
)

# -----------------------------
# SAFE CHECK
# -----------------------------
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -----------------------------
# KPI METRICS
# -----------------------------
total_revenue = filtered_df['Total_Sales'].sum()
total_profit = filtered_df['Total_Profit'].sum()
overall_margin = (total_profit / total_revenue) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Overall Margin", f"{overall_margin:.2f}%")

# -----------------------------
# DIVISION PERFORMANCE
# -----------------------------
st.subheader("Division Performance")

division = filtered_df.groupby('Division').agg({
    'Total_Sales': 'sum',
    'Total_Profit': 'sum'
}).reset_index()

division['Margin %'] = (division['Total_Profit'] / division['Total_Sales']) * 100

fig = px.bar(
    division,
    x='Division',
    y='Margin %',
    text=division['Margin %'].round(2),
    color='Division'
)

fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# PARETO ANALYSIS
# -----------------------------
st.subheader("Pareto Analysis")

prod = filtered_df.groupby('Product Name').agg({
    'Total_Profit': 'sum'
}).reset_index()

prod = prod.sort_values(by='Total_Profit', ascending=False)

prod['Cumulative'] = prod['Total_Profit'].cumsum()
prod['Cumulative %'] = (prod['Cumulative'] / prod['Total_Profit'].sum()) * 100

cutoff = prod[prod['Cumulative %'] <= pareto_threshold]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=prod['Product Name'],
    y=prod['Total_Profit'],
    name="Profit"
))

fig.add_trace(go.Scatter(
    x=prod['Product Name'],
    y=prod['Cumulative %'],
    name="Cumulative %",
    yaxis="y2"
))

fig.update_layout(
    yaxis=dict(title="Profit"),
    yaxis2=dict(title="Cumulative %", overlaying="y", side="right", range=[0,100])
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# HIGH RISK PRODUCTS
# -----------------------------
st.subheader("High Risk Products")

prod_full = filtered_df.groupby('Product Name').agg({
    'Total_Sales': 'sum',
    'Total_Profit': 'sum',
    'Total_Units': 'sum'
}).reset_index()

prod_full['Margin %'] = (prod_full['Total_Profit'] / prod_full['Total_Sales']) * 100

if risk_mode == "Basic (Margin < 20%)":
    high_risk = prod_full[prod_full['Margin %'] < 20]
else:
    high_risk = prod_full[
        (prod_full['Margin %'] < 50) &
        (prod_full['Total_Sales'] < prod_full['Total_Sales'].quantile(0.4))
    ]

if high_risk.empty:
    st.info("No high-risk products found.")
else:
    st.dataframe(high_risk.sort_values(by='Margin %'))

# -----------------------------
# KEY INSIGHTS
# -----------------------------
best_div = division.loc[division['Margin %'].idxmax()]
worst_div = division.loc[division['Margin %'].idxmin()]

top_product = prod.iloc[0]

st.subheader("Key Insights")

st.write(f"Best Division: {best_div['Division']} ({best_div['Margin %']:.2f}%)")
st.write(f"Weak Division: {worst_div['Division']} ({worst_div['Margin %']:.2f}%)")
st.write(f"Top Product: {top_product['Product Name']}")
st.write(f"{len(cutoff)} products contribute ~{pareto_threshold}% of total profit")

# -----------------------------
# AUTO GENERATED EXEC SUMMARY
# -----------------------------
st.subheader("Executive Summary")

summary = f"""
The business generated total revenue of ${total_revenue:,.0f} and profit of ${total_profit:,.0f},
resulting in an overall margin of {overall_margin:.2f}%.

The {best_div['Division']} division leads performance with the highest profitability,
while {worst_div['Division']} shows comparatively weaker margins and may require attention.

Profit contribution is concentrated, with {len(cutoff)} products accounting for approximately
{pareto_threshold}% of total profit, indicating a strong Pareto effect.

The top-performing product is {top_product['Product Name']}, contributing significantly to overall profit.

Risk analysis highlights {len(high_risk)} products that may require pricing, cost, or inventory optimization.
"""

st.write(summary)

# -----------------------------
# RECOMMENDATIONS
# -----------------------------
st.subheader("Business Recommendations")

st.markdown("""
- Focus marketing and inventory on high-profit products
- Optimize pricing or reduce costs for low-margin products
- Reduce dependency on a small set of products (Pareto risk)
- Improve operational efficiency in low-performing divisions
""")

import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

# -----------------------------
# DARK THEME (FORCE)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
[data-testid="stMetric"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
h1, h2, h3 {
    color: #e6edf3;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
uploaded_file = st.file_uploader("Upload your dataset", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a dataset to continue")
    st.stop()

df = pd.read_csv(uploaded_file)

# -----------------------------
# DATA CLEANING
# -----------------------------
df.columns = df.columns.str.strip()

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filters")

divisions = df['Division'].unique()
selected_div = st.sidebar.multiselect(
    "Select Division",
    divisions,
    default=divisions
)

df = df[df['Division'].isin(selected_div)]

if df.empty:
    st.error("No data available for selected filters")
    st.stop()

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_revenue = df['Sales'].sum()
total_profit = df['Gross Profit'].sum()
overall_margin = (total_profit / total_revenue) * 100

# -----------------------------
# KPI DISPLAY
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Overall Margin", f"{overall_margin:.2f}%")

st.divider()

# -----------------------------
# DIVISION ANALYSIS
# -----------------------------
st.subheader("Division Performance")

division = df.groupby('Division').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum'
}).reset_index()

division['Margin %'] = (division['Gross Profit'] / division['Sales']) * 100

fig_div = px.bar(
    division,
    x='Division',
    y='Margin %',
    color='Division',
    title="Gross Margin by Division",
    height=400
)

st.plotly_chart(fig_div, use_container_width=True)

# -----------------------------
# PARETO ANALYSIS
# -----------------------------
st.subheader("Pareto Analysis")

prod = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum'
}).reset_index()

pareto = prod.sort_values('Gross Profit', ascending=False)
pareto['Cumulative %'] = pareto['Gross Profit'].cumsum() / pareto['Gross Profit'].sum() * 100

top_n = pareto.head(5)

fig_pareto = px.bar(
    top_n,
    x='Product Name',
    y='Gross Profit',
    title="Top Profit-Contributing Products",
    height=400
)

st.plotly_chart(fig_pareto, use_container_width=True)

# -----------------------------
# HIGH RISK PRODUCTS (FIXED)
# -----------------------------
st.subheader("High Risk Products")

prod['Margin %'] = (prod['Gross Profit'] / prod['Sales']) * 100

risk_products = prod[(prod['Margin %'] < 10) & (prod['Sales'] > prod['Sales'].mean())]

if risk_products.empty:
    st.info("No high-risk products found based on current criteria.")
else:
    st.dataframe(risk_products)

# -----------------------------
# KEY INSIGHTS (FIXED LOGIC)
# -----------------------------
st.subheader("Key Insights")

if len(division) > 1:
    best_div = division.loc[division['Margin %'].idxmax()]
    worst_div = division.loc[division['Margin %'].idxmin()]

    st.write(f"Best Division: {best_div['Division']} ({best_div['Margin %']:.2f}%)")
    st.write(f"Weak Division: {worst_div['Division']} ({worst_div['Margin %']:.2f}%)")
else:
    only_div = division.iloc[0]
    st.write(f"Selected Division: {only_div['Division']} ({only_div['Margin %']:.2f}%)")

best_product = pareto.iloc[0]
cutoff_80 = pareto[pareto['Cumulative %'] <= 80]

st.write(f"Top Product: {best_product['Product Name']}")
st.write(f"{len(cutoff_80)} products generate 80% of total profit")

# -----------------------------
# BUSINESS RECOMMENDATIONS
# -----------------------------
st.subheader("Business Recommendations")

st.markdown("""
- Focus marketing and inventory on high-profit products  
- Reprice or optimize cost for low-margin products  
- Reduce dependency on a small set of products (Pareto risk)  
- Improve efficiency in low-performing divisions  
""")

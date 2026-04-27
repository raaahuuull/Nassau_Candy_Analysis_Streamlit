import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    layout="wide"
)

# -------------------------------
# FIXED PLOTLY THEME (IMPORTANT)
# -------------------------------
PLOT_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#9090b8'),
    margin=dict(l=20, r=20, t=50, b=20)
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")
    df = df.dropna()

    df['Sales'] = pd.to_numeric(df['Sales'])
    df['Cost'] = pd.to_numeric(df['Cost'])
    df['Gross Profit'] = pd.to_numeric(df['Gross Profit'])
    df['Units'] = pd.to_numeric(df['Units'])

    df['Gross_Margin_Pct'] = (df['Gross Profit'] / df['Sales']) * 100

    return df

df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("Filters")

division_filter = st.sidebar.multiselect(
    "Division",
    df['Division'].unique(),
    default=df['Division'].unique()
)

df = df[df['Division'].isin(division_filter)]

# -------------------------------
# KPIs
# -------------------------------
total_revenue = df['Sales'].sum()
total_profit = df['Gross Profit'].sum()
margin = (total_profit / total_revenue) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Revenue", f"${total_revenue:,.0f}")
col2.metric("Profit", f"${total_profit:,.0f}")
col3.metric("Margin", f"{margin:.2f}%")

st.divider()

# -------------------------------
# DIVISION ANALYSIS
# -------------------------------
division = df.groupby('Division').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum'
}).reset_index()

division['Margin %'] = (division['Gross Profit'] / division['Sales']) * 100

st.subheader("Division Performance")

fig = px.bar(
    division,
    x='Division',
    y='Margin %',
    color='Division',
    title="Margin by Division"
)
fig.update_layout(**PLOT_THEME)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# PARETO
# -------------------------------
prod = df.groupby('Product Name').agg({
    'Sales': 'sum',
    'Gross Profit': 'sum'
}).reset_index()

prod['Total_Profit'] = prod['Gross Profit']

pareto = prod.sort_values('Total_Profit', ascending=False)
pareto['Cumulative %'] = pareto['Total_Profit'].cumsum() / pareto['Total_Profit'].sum() * 100

st.subheader("Pareto Analysis")

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Bar(x=pareto['Product Name'], y=pareto['Total_Profit'], name="Profit"),
    secondary_y=False
)

fig2.add_trace(
    go.Scatter(x=pareto['Product Name'], y=pareto['Cumulative %'], name="Cumulative %"),
    secondary_y=True
)

fig2.update_layout(title="Pareto Chart")
fig2.update_layout(**PLOT_THEME)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# RISK ANALYSIS
# -------------------------------
df['Cost_to_Sales_Ratio'] = (df['Cost'] / df['Sales']) * 100

df['Risk_Flag'] = np.where(
    (df['Cost_to_Sales_Ratio'] > 60) & (df['Gross_Margin_Pct'] < 50),
    'High Risk',
    'OK'
)

st.subheader("High Risk Products")

risk_df = df[df['Risk_Flag'] == 'High Risk']

st.dataframe(risk_df[['Product Name', 'Sales', 'Gross Profit']])

# -------------------------------
# INSIGHTS
# -------------------------------
st.subheader("Key Insights")

best_div = division.loc[division['Margin %'].idxmax()]
worst_div = division.loc[division['Margin %'].idxmin()]
best_product = pareto.iloc[0]

cutoff_80 = pareto[pareto['Cumulative %'] <= 80]

st.write(f"Best Division: {best_div['Division']} ({best_div['Margin %']:.2f}%)")
st.write(f"Weak Division: {worst_div['Division']} ({worst_div['Margin %']:.2f}%)")
st.write(f"Top Product: {best_product['Product Name']}")
st.write(f"{len(cutoff_80)} products generate 80% of profit")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy | Profitability Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0a0a0f;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e;
}
section[data-testid="stSidebar"] * {
    color: #c8c8d8 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
    color: #7878a0 !important;
    font-size: 11px !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Header ── */
.dash-header {
    background: linear-gradient(135deg, #0f0f18 0%, #1a0a2e 50%, #0a1a2e 100%);
    border: 1px solid #2a1a4e;
    border-radius: 16px;
    padding: 36px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(130,80,255,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.dash-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(0,180,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.header-label {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #8250ff;
    font-weight: 600;
    margin-bottom: 8px;
}
.header-title {
    font-family: 'DM Serif Display', serif;
    font-size: 38px;
    color: #f0f0ff;
    line-height: 1.15;
    margin: 0 0 8px 0;
}
.header-sub {
    font-size: 14px;
    color: #6868a0;
    font-weight: 300;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-card.purple::before { background: linear-gradient(90deg, #8250ff, #b07aff); }
.kpi-card.teal::before   { background: linear-gradient(90deg, #00c4a7, #00e8c6); }
.kpi-card.blue::before   { background: linear-gradient(90deg, #0099ff, #66ccff); }
.kpi-card.amber::before  { background: linear-gradient(90deg, #f5a623, #ffd166); }
.kpi-label {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a5a80;
    font-weight: 600;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 30px;
    color: #e8e8ff;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-delta {
    font-size: 12px;
    color: #4a4a70;
    font-weight: 400;
}

/* ── Section Headers ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 22px;
    color: #d8d8f0;
    margin: 32px 0 4px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #1e1e2e;
}
.section-sub {
    font-size: 12px;
    color: #5a5a80;
    margin-bottom: 20px;
    letter-spacing: 0.04em;
}

/* ── Plotly chart containers ── */
.chart-card {
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    padding: 6px;
    margin-bottom: 16px;
}

/* ── Risk badge ── */
.badge-risk {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
}
.badge-risk.high { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-risk.ok   { background: rgba(0,196,167,0.12); color: #2dd4bf; border: 1px solid rgba(0,196,167,0.25); }

/* ── Divider ── */
hr { border-color: #1e1e2e; }

/* ── Streamlit overrides ── */
div[data-testid="stMetric"] {
    background: #0f0f18;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    padding: 16px 20px;
}
div[data-testid="stMetric"] label { color: #5a5a80 !important; font-size: 11px !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #e8e8ff !important; font-family: 'DM Serif Display', serif !important; font-size: 28px !important; }
.stTabs [data-baseweb="tab-list"] { background: #0f0f18; border-radius: 10px; padding: 4px; gap: 4px; border: 1px solid #1e1e2e; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 8px; color: #6868a0; font-size: 13px; font-weight: 500; padding: 8px 20px; }
.stTabs [aria-selected="true"] { background: #1e1e38 !important; color: #d8d8ff !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none; }
div[data-testid="stDataFrame"] { border: 1px solid #1e1e2e; border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ─────────────────────────────────────────────────────────────
PLOT_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans', color='#9090b8', size=12),
    xaxis=dict(gridcolor='#1a1a2a', linecolor='#2a2a3e', tickcolor='#2a2a3e'),
    yaxis=dict(gridcolor='#1a1a2a', linecolor='#2a2a3e', tickcolor='#2a2a3e'),
    margin=dict(l=16, r=16, t=48, b=16),
    colorway=['#8250ff','#00c4a7','#0099ff','#f5a623','#ef4444','#a855f7'],
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#2a2a3e', borderwidth=1,
                font=dict(color='#8080a8', size=11)),
    title=dict(font=dict(family='DM Serif Display', color='#d8d8f0', size=17), x=0.0, xanchor='left', pad=dict(l=10, t=8))
)

DIV_COLORS = {'Chocolate':'#8250ff', 'Sugar':'#00c4a7', 'Other':'#f5a623'}
FACTORY_COLORS = {"Lot's O' Nuts":'#8250ff', "Wicked Choccy's":'#0099ff',
                  'Sugar Shack':'#00c4a7', 'Secret Factory':'#f5a623', 'The Other Factory':'#ef4444'}

# ── Data loader ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('Nassau Candy Distributor.csv')
    df = df.drop_duplicates()
    for c in ['Sales','Cost','Gross Profit','Units']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df = df.dropna(subset=['Sales','Cost','Gross Profit','Units'])
    df = df[(df['Sales'] > 0) & (df['Units'] > 0)].copy()
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)
    df['Product Name'] = df['Product Name'].str.strip()
    df['Month']   = df['Order Date'].dt.to_period('M').astype(str)
    df['Quarter'] = df['Order Date'].dt.to_period('Q').astype(str)
    df['Year']    = df['Order Date'].dt.year
    df['Gross_Margin_Pct'] = (df['Gross Profit'] / df['Sales'] * 100).round(2)
    df['Profit_per_Unit']  = (df['Gross Profit'] / df['Units']).round(2)
    factory_map = {
        'Wonka Bar - Nutty Crunch Surprise': "Lot's O' Nuts",
        'Wonka Bar - Fudge Mallows':         "Lot's O' Nuts",
        'Wonka Bar -Scrumdiddlyumptious':    "Lot's O' Nuts",
        'Wonka Bar - Milk Chocolate':        "Wicked Choccy's",
        'Wonka Bar - Triple Dazzle Caramel': "Wicked Choccy's",
        'Laffy Taffy':            'Sugar Shack',
        'SweeTARTS':              'Sugar Shack',
        'Nerds':                  'Sugar Shack',
        'Fun Dip':                'Sugar Shack',
        'Fizzy Lifting Drinks':   'Sugar Shack',
        'Everlasting Gobstopper': 'Secret Factory',
        'Lickable Wallpaper':     'Secret Factory',
        'Wonka Gum':              'Secret Factory',
        'Hair Toffee':            'The Other Factory',
        'Kazookles':              'The Other Factory',
    }
    df['Factory'] = df['Product Name'].map(factory_map)
    return df

@st.cache_data
def build_aggregates(df):
    total_sales  = df['Sales'].sum()
    total_profit = df['Gross Profit'].sum()

    prod = df.groupby(['Division','Product Name','Factory']).agg(
        Total_Sales  =('Sales','sum'),
        Total_Profit =('Gross Profit','sum'),
        Total_Cost   =('Cost','sum'),
        Total_Units  =('Units','sum'),
        Orders       =('Row ID','count')
    ).reset_index()
    prod['Gross_Margin_Pct']      = (prod['Total_Profit'] / prod['Total_Sales'] * 100).round(2)
    prod['Profit_per_Unit']       = (prod['Total_Profit'] / prod['Total_Units']).round(2)
    prod['Revenue_Contribution_%']= (prod['Total_Sales']  / total_sales  * 100).round(2)
    prod['Profit_Contribution_%'] = (prod['Total_Profit'] / total_profit * 100).round(2)
    prod['Cost_to_Sales_Ratio']   = (prod['Total_Cost']   / prod['Total_Sales'] * 100).round(2)
    prod['Risk_Flag'] = prod.apply(
        lambda r: 'High Risk' if r['Cost_to_Sales_Ratio'] > 60 and r['Gross_Margin_Pct'] < 50 else 'OK', axis=1)

    div = df.groupby('Division').agg(
        Total_Sales =('Sales','sum'),
        Total_Profit=('Gross Profit','sum'),
        Total_Units =('Units','sum')
    ).reset_index()
    div['Margin_%']        = (div['Total_Profit'] / div['Total_Sales'] * 100).round(2)
    div['Revenue_Share_%'] = (div['Total_Sales']  / div['Total_Sales'].sum()  * 100).round(2)
    div['Profit_Share_%']  = (div['Total_Profit'] / div['Total_Profit'].sum() * 100).round(2)

    factory = df.groupby('Factory').agg(
        Total_Sales =('Sales','sum'),
        Total_Profit=('Gross Profit','sum'),
        Total_Units =('Units','sum')
    ).reset_index()
    factory['Avg_Margin_%'] = (factory['Total_Profit'] / factory['Total_Sales'] * 100).round(2)

    geo = df.groupby(['State/Province','Region']).agg(
        Total_Sales =('Sales','sum'),
        Total_Profit=('Gross Profit','sum')
    ).reset_index()
    geo['Margin_%'] = (geo['Total_Profit'] / geo['Total_Sales'] * 100).round(2)

    monthly = df.groupby(['Month','Division']).agg(
        Sales =('Sales','sum'),
        Profit=('Gross Profit','sum')
    ).reset_index()
    monthly['Margin_%'] = (monthly['Profit'] / monthly['Sales'] * 100).round(2)

    pareto = prod.sort_values('Total_Profit', ascending=False).reset_index(drop=True)
    pareto['Cumulative_Profit_%']  = (pareto['Total_Profit'].cumsum() / pareto['Total_Profit'].sum() * 100).round(2)
    pareto['Cumulative_Revenue_%'] = (pareto['Total_Sales'].cumsum()  / pareto['Total_Sales'].sum()  * 100).round(2)

    return prod, div, factory, geo, monthly, pareto


# ════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════════════════════════
df_raw = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 12px 0;'>
      <div style='font-size:11px;letter-spacing:0.2em;text-transform:uppercase;color:#5a5a80;margin-bottom:4px;'>Dashboard</div>
      <div style='font-family:"DM Serif Display",serif;font-size:20px;color:#d8d8f0;line-height:1.2;'>Nassau Candy<br>Intelligence</div>
    </div>
    <hr style='border-color:#1e1e2e;margin:0 0 20px 0;'/>
    """, unsafe_allow_html=True)

    divisions = st.multiselect("Division", options=df_raw['Division'].unique().tolist(),
                                default=df_raw['Division'].unique().tolist())
    regions   = st.multiselect("Region",   options=df_raw['Region'].unique().tolist(),
                                default=df_raw['Region'].unique().tolist())

    year_min, year_max = int(df_raw['Year'].min()), int(df_raw['Year'].max())
    if year_min < year_max:
        year_range = st.slider("Year Range", year_min, year_max, (year_min, year_max))
    else:
        year_range = (year_min, year_max)
        st.info(f"Single year: {year_min}")

    margin_threshold = st.slider("Min Gross Margin %", 0, 100, 0,
                                  help="Filter products above this margin threshold")

    st.markdown("<hr style='border-color:#1e1e2e;'/>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;color:#3a3a60;text-align:center;'>Nassau Candy Distributor<br>Profitability Analysis v1.0</div>", unsafe_allow_html=True)

# ── Filter data ───────────────────────────────────────────────────────────────
df = df_raw[
    df_raw['Division'].isin(divisions) &
    df_raw['Region'].isin(regions) &
    df_raw['Year'].between(year_range[0], year_range[1])
].copy()

prod, div, factory, geo, monthly, pareto = build_aggregates(df)
prod_filtered = prod[prod['Gross_Margin_Pct'] >= margin_threshold]

total_revenue  = df['Sales'].sum()
total_profit   = df['Gross Profit'].sum()
total_cost     = df['Cost'].sum()
overall_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_units    = df['Units'].sum()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='dash-header'>
  <div class='header-label'>Profitability Intelligence Platform</div>
  <div class='header-title'>Product Line &amp; Margin<br>Performance Analysis</div>
  <div class='header-sub'>Nassau Candy Distributor &nbsp;·&nbsp; {df['Order Date'].min().strftime('%b %Y')} – {df['Order Date'].max().strftime('%b %Y')} &nbsp;·&nbsp; {df.shape[0]:,} transactions</div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total Revenue",    f"${total_revenue:,.0f}",  delta=None)
with k2:
    st.metric("Total Gross Profit", f"${total_profit:,.0f}", delta=None)
with k3:
    st.metric("Overall Margin",   f"{overall_margin:.1f}%",  delta=None)
with k4:
    st.metric("Units Sold",       f"{total_units:,.0f}",     delta=None)

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Product Profitability", "Division Performance",
    "Pareto Analysis", "Cost & Risk Diagnostics",
    "Geographic & Trends", "Factory Intelligence"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — PRODUCT PROFITABILITY
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-title'>Product-Level Profitability</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Gross profit and margin ranked by product. Red bars indicate margin below 50% threshold.</div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])

    with c1:
        top_prod = prod_filtered.sort_values('Total_Profit', ascending=True)
        colors   = ['#ef4444' if m < 50 else '#00c4a7' for m in top_prod['Gross_Margin_Pct']]
        fig = go.Figure(go.Bar(
            x=top_prod['Total_Profit'], y=top_prod['Product Name'],
            orientation='h', marker_color=colors,
            text=[f"${v:,.0f}" for v in top_prod['Total_Profit']],
            textposition='outside', textfont=dict(size=10, color='#7070a0'),
            hovertemplate='<b>%{y}</b><br>Profit: $%{x:,.0f}<extra></extra>'
        ))
        fig.update_layout(**PLOT_THEME, title='Gross Profit by Product',
                          xaxis_title='Gross Profit ($)', yaxis_title='',
                          height=460, bargap=0.25)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.scatter(prod_filtered, x='Total_Sales', y='Gross_Margin_Pct',
                          size='Total_Profit', color='Division',
                          hover_name='Product Name', text='Product Name',
                          color_discrete_map=DIV_COLORS,
                          labels={'Total_Sales':'Total Sales ($)', 'Gross_Margin_Pct':'Gross Margin %'})
        fig2.update_traces(textposition='top center', textfont_size=8)
        fig2.add_hline(y=50, line_dash='dash', line_color='#ef4444',
                       annotation_text='50% Threshold', annotation_font_color='#ef4444')
        fig2.update_layout(**PLOT_THEME, title='Sales vs Gross Margin % (Bubble = Profit)', height=460)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-title'>Product Leaderboard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Full breakdown of all KPIs per product. Sort by any column.</div>", unsafe_allow_html=True)

    display_cols = ['Division','Product Name','Total_Sales','Total_Profit',
                    'Gross_Margin_Pct','Profit_per_Unit','Revenue_Contribution_%',
                    'Profit_Contribution_%','Risk_Flag']
    leaderboard = prod_filtered.sort_values('Total_Profit', ascending=False)[display_cols].reset_index(drop=True)
    leaderboard.columns = ['Division','Product','Revenue ($)','Profit ($)','Margin %',
                           'Profit/Unit','Rev Contrib %','Profit Contrib %','Risk']
    st.dataframe(leaderboard.style.format({
        'Revenue ($)': '${:,.0f}', 'Profit ($)': '${:,.0f}',
        'Margin %': '{:.1f}%', 'Profit/Unit': '${:.2f}',
        'Rev Contrib %': '{:.1f}%', 'Profit Contrib %': '{:.1f}%'
    }).background_gradient(subset=['Margin %'], cmap='RdYlGn', vmin=0, vmax=100),
    use_container_width=True, height=360)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DIVISION PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-title'>Division-Level Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Revenue, profit share, and margin efficiency compared across business divisions.</div>", unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    best_div  = div.loc[div['Margin_%'].idxmax()]
    worst_div = div.loc[div['Margin_%'].idxmin()]

    with d1:
        st.metric("Best Division",  f"{best_div['Division']}",  f"{best_div['Margin_%']:.1f}% margin")
    with d2:
        st.metric("Weakest Division", f"{worst_div['Division']}", f"{worst_div['Margin_%']:.1f}% margin")
    with d3:
        st.metric("Divisions Analyzed", str(len(div)))

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        fig = go.Figure(go.Pie(
            labels=div['Division'], values=div['Revenue_Share_%'],
            hole=0.52, marker_colors=[DIV_COLORS.get(d,'#888') for d in div['Division']],
            textfont_size=12, hovertemplate='<b>%{label}</b><br>Revenue Share: %{value:.1f}%<extra></extra>'
        ))
        fig.update_layout(**PLOT_THEME, title='Revenue Share', height=300,
                          showlegend=True, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure(go.Pie(
            labels=div['Division'], values=div['Profit_Share_%'],
            hole=0.52, marker_colors=[DIV_COLORS.get(d,'#888') for d in div['Division']],
            textfont_size=12, hovertemplate='<b>%{label}</b><br>Profit Share: %{value:.1f}%<extra></extra>'
        ))
        fig.update_layout(**PLOT_THEME, title='Profit Share', height=300,
                          showlegend=True, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        fig = go.Figure(go.Bar(
            x=div['Division'], y=div['Margin_%'],
            marker_color=[DIV_COLORS.get(d,'#888') for d in div['Division']],
            text=[f"{v:.1f}%" for v in div['Margin_%']],
            textposition='outside', textfont=dict(size=13, color='#b0b0d8'),
            hovertemplate='<b>%{x}</b><br>Margin: %{y:.1f}%<extra></extra>'
        ))
        fig.add_hline(y=50, line_dash='dot', line_color='#ef4444',
                      annotation_text='50% target', annotation_font_color='#ef4444')
        fig.update_layout(**PLOT_THEME, title='Gross Margin %', height=300,
                          yaxis_title='Gross Margin %', xaxis_title='')
        st.plotly_chart(fig, use_container_width=True)

    # Revenue vs Profit grouped
    st.markdown("<div class='section-title'>Revenue vs Profit Comparison</div>", unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Total Revenue', x=div['Division'], y=div['Total_Sales'],
                         marker_color='#8250ff', opacity=0.85,
                         hovertemplate='Revenue: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Total Profit',  x=div['Division'], y=div['Total_Profit'],
                         marker_color='#00c4a7', opacity=0.85,
                         hovertemplate='Profit: $%{y:,.0f}<extra></extra>'))
    fig.update_layout(**PLOT_THEME, title='Revenue vs Profit by Division',
                      barmode='group', yaxis_title='Amount ($)', height=380)
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — PARETO ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-title'>Pareto (80/20) Profit Concentration</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Identifying the critical few products that drive the majority of total profit.</div>", unsafe_allow_html=True)

    cutoff_80 = pareto[pareto['Cumulative_Profit_%'] <= 80]
    p1, p2, p3 = st.columns(3)
    with p1:
        st.metric("Products Driving 80% Profit", f"{len(cutoff_80)} of {len(pareto)}")
    with p2:
        st.metric("Top Product Profit Share", f"{pareto.iloc[0]['Profit_Contribution_%']:.1f}%",
                  pareto.iloc[0]['Product Name'])
    with p3:
        concentration = pareto.head(3)['Profit_Contribution_%'].sum()
        st.metric("Top 3 Products Combined", f"{concentration:.1f}% of profit")

    st.markdown("<br>", unsafe_allow_html=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = ['#8250ff' if i < len(cutoff_80) else '#2a1a4e' for i in range(len(pareto))]
    fig.add_trace(go.Bar(
        x=pareto['Product Name'], y=pareto['Total_Profit'],
        name='Gross Profit', marker_color=bar_colors,
        hovertemplate='<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>'
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=pareto['Product Name'], y=pareto['Cumulative_Profit_%'],
        name='Cumulative Profit %', mode='lines+markers',
        line=dict(color='#00c4a7', width=2.5),
        marker=dict(size=7, color='#00c4a7'),
        hovertemplate='Cumulative: %{y:.1f}%<extra></extra>'
    ), secondary_y=True)
    fig.add_hline(y=80, line_dash='dash', line_color='#ef4444',
                  annotation_text='80% threshold', secondary_y=True,
                  annotation_font_color='#ef4444')
    fig.update_layout(**PLOT_THEME, title='Pareto Chart — Profit Concentration by Product',
                      height=440, xaxis_tickangle=-35)
    fig.update_yaxes(title_text='Gross Profit ($)', secondary_y=False,
                     gridcolor='#1a1a2a', color='#9090b8')
    fig.update_yaxes(title_text='Cumulative Profit %', secondary_y=True,
                     range=[0, 115], gridcolor='rgba(0,0,0,0)', color='#9090b8')
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Top 5 Products by Profit**")
        top5 = pareto.head(5)[['Product Name','Division','Total_Profit','Gross_Margin_Pct','Profit_Contribution_%']]
        top5.columns = ['Product','Division','Profit ($)','Margin %','Profit Contrib %']
        st.dataframe(top5.style.format({'Profit ($)':'${:,.0f}','Margin %':'{:.1f}%','Profit Contrib %':'{:.1f}%'}),
                     use_container_width=True, hide_index=True)
    with c2:
        st.markdown("**Bottom 5 Products by Profit**")
        bot5 = pareto.tail(5)[['Product Name','Division','Total_Profit','Gross_Margin_Pct','Profit_Contribution_%']]
        bot5.columns = ['Product','Division','Profit ($)','Margin %','Profit Contrib %']
        st.dataframe(bot5.style.format({'Profit ($)':'${:,.0f}','Margin %':'{:.1f}%','Profit Contrib %':'{:.1f}%'}),
                     use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — COST & RISK DIAGNOSTICS
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-title'>Cost Structure & Margin Risk Diagnostics</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Products flagged as High Risk have cost-to-sales ratio above 60% AND gross margin below 50%.</div>", unsafe_allow_html=True)

    high_risk = prod[prod['Risk_Flag'] == 'High Risk']
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("High Risk Products", str(len(high_risk)))
    with r2:
        avg_cost_ratio = prod['Cost_to_Sales_Ratio'].mean()
        st.metric("Avg Cost-to-Sales Ratio", f"{avg_cost_ratio:.1f}%")
    with r3:
        low_margin = prod[prod['Gross_Margin_Pct'] < 50]
        st.metric("Products Below 50% Margin", str(len(low_margin)))

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.3, 1])

    with c1:
        max_val = max(prod['Total_Sales'].max(), prod['Total_Cost'].max()) * 1.08
        fig = px.scatter(prod, x='Total_Cost', y='Total_Sales',
                         color='Risk_Flag', size='Total_Profit',
                         hover_name='Product Name',
                         color_discrete_map={'High Risk':'#ef4444', 'OK':'#00c4a7'},
                         labels={'Total_Cost':'Total Cost ($)','Total_Sales':'Total Sales ($)','Risk_Flag':'Risk'},
                         size_max=40)
        fig.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val], mode='lines',
            line=dict(dash='dash', color='#5a5a80', width=1.5),
            name='Break-Even Line', hoverinfo='skip'
        ))
        fig.update_layout(**PLOT_THEME, title='Cost vs Sales — Risk Identification', height=420)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(prod.sort_values('Cost_to_Sales_Ratio', ascending=True),
                     x='Cost_to_Sales_Ratio', y='Product Name', orientation='h',
                     color='Gross_Margin_Pct', color_continuous_scale='RdYlGn',
                     range_color=[0, 100],
                     labels={'Cost_to_Sales_Ratio':'Cost-to-Sales Ratio (%)','Product Name':''},
                     hover_data=['Division','Gross_Margin_Pct'])
        fig.add_vline(x=60, line_dash='dash', line_color='#ef4444',
                      annotation_text='Risk threshold', annotation_font_color='#ef4444')
        fig.update_layout(**PLOT_THEME, title='Cost-to-Sales Ratio by Product',
                          height=420, coloraxis_colorbar=dict(title='Margin %', tickfont=dict(color='#7070a0')))
        st.plotly_chart(fig, use_container_width=True)

    if len(high_risk) > 0:
        st.markdown("<div class='section-title'>High Risk Products — Action Required</div>", unsafe_allow_html=True)
        risk_display = high_risk[['Division','Product Name','Total_Sales','Total_Profit',
                                   'Gross_Margin_Pct','Cost_to_Sales_Ratio']].copy()
        risk_display.columns = ['Division','Product','Revenue ($)','Profit ($)','Margin %','Cost/Sales %']
        st.dataframe(risk_display.style.format({
            'Revenue ($)':'${:,.0f}','Profit ($)':'${:,.0f}',
            'Margin %':'{:.1f}%','Cost/Sales %':'{:.1f}%'
        }).applymap(lambda _: 'color: #f87171', subset=['Margin %','Cost/Sales %']),
        use_container_width=True, hide_index=True)
    else:
        st.success("No high-risk products detected with current filters.")

    # Margin distribution
    st.markdown("<div class='section-title'>Margin Distribution</div>", unsafe_allow_html=True)
    fig = go.Figure()
    for div_name in prod['Division'].unique():
        subset = prod[prod['Division'] == div_name]['Gross_Margin_Pct']
        fig.add_trace(go.Histogram(
            x=subset, name=div_name, nbinsx=20, opacity=0.75,
            marker_color=DIV_COLORS.get(div_name, '#888'),
            hovertemplate=f'{div_name}: %{{x:.1f}}%<extra></extra>'
        ))
    fig.add_vline(x=50, line_dash='dash', line_color='#ef4444',
                  annotation_text='50% target', annotation_font_color='#ef4444')
    fig.update_layout(**PLOT_THEME, title='Gross Margin % Distribution by Division',
                      barmode='overlay', height=340,
                      xaxis_title='Gross Margin %', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — GEOGRAPHIC & TRENDS
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown("<div class='section-title'>Geographic Performance</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Top states by gross profit. Color intensity reflects gross margin efficiency.</div>", unsafe_allow_html=True)

    top_n = st.slider("Number of states to display", 5, 30, 15)
    top_states = geo.sort_values('Total_Profit', ascending=False).head(top_n)

    fig = px.bar(top_states, x='State/Province', y='Total_Profit',
                 color='Margin_%', color_continuous_scale='RdYlGn',
                 range_color=[30, 80],
                 labels={'Total_Profit':'Gross Profit ($)', 'Margin_%':'Margin %'},
                 text='Margin_%')
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                      textfont=dict(size=10, color='#9090b8'))
    fig.update_layout(**PLOT_THEME, title=f'Top {top_n} States by Gross Profit',
                      height=420, xaxis_tickangle=-35,
                      coloraxis_colorbar=dict(title='Margin %', tickfont=dict(color='#7070a0')))
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        region_data = df.groupby('Region').agg(
            Total_Sales=('Sales','sum'), Total_Profit=('Gross Profit','sum')).reset_index()
        region_data['Margin_%'] = (region_data['Total_Profit'] / region_data['Total_Sales'] * 100).round(2)
        fig = px.bar(region_data, x='Region', y='Total_Profit',
                     color='Margin_%', color_continuous_scale='RdYlGn',
                     text=[f"${v:,.0f}" for v in region_data['Total_Profit']],
                     labels={'Total_Profit':'Gross Profit ($)'})
        fig.update_traces(textposition='outside', textfont=dict(size=10, color='#9090b8'))
        fig.update_layout(**PLOT_THEME, title='Gross Profit by Region', height=340,
                          coloraxis_colorbar=dict(title='Margin %', tickfont=dict(color='#7070a0')))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ship_data = df.groupby('Ship Mode').agg(
            Orders=('Row ID','count'), Total_Sales=('Sales','sum')).reset_index()
        fig = go.Figure(go.Pie(
            labels=ship_data['Ship Mode'], values=ship_data['Orders'],
            hole=0.5, marker_colors=['#8250ff','#00c4a7','#0099ff','#f5a623'],
            hovertemplate='<b>%{label}</b><br>Orders: %{value:,}<extra></extra>'
        ))
        fig.update_layout(**PLOT_THEME, title='Orders by Ship Mode', height=340)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Monthly Margin Trend</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Tracking gross margin % over time across all divisions.</div>", unsafe_allow_html=True)

    fig = go.Figure()
    for div_name in monthly['Division'].unique():
        subset = monthly[monthly['Division'] == div_name].sort_values('Month')
        fig.add_trace(go.Scatter(
            x=subset['Month'], y=subset['Margin_%'], name=div_name,
            mode='lines+markers', line=dict(width=2.5, color=DIV_COLORS.get(div_name,'#888')),
            marker=dict(size=6), hovertemplate=f'<b>{div_name}</b><br>%{{x}}: %{{y:.1f}}%<extra></extra>'
        ))
    fig.add_hline(y=50, line_dash='dot', line_color='#ef4444',
                  annotation_text='50% target', annotation_font_color='#ef4444')
    fig.update_layout(**PLOT_THEME, title='Monthly Gross Margin % by Division',
                      height=400, yaxis_title='Gross Margin %', xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — FACTORY INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown("<div class='section-title'>Factory Performance Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Revenue, profit, and margin efficiency benchmarked across all manufacturing facilities.</div>", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    best_factory  = factory.loc[factory['Avg_Margin_%'].idxmax()]
    worst_factory = factory.loc[factory['Avg_Margin_%'].idxmin()]
    with f1:
        st.metric("Top Factory (Margin)", best_factory['Factory'],  f"{best_factory['Avg_Margin_%']:.1f}%")
    with f2:
        st.metric("Weakest Factory",      worst_factory['Factory'], f"{worst_factory['Avg_Margin_%']:.1f}%")
    with f3:
        st.metric("Factories Active", str(len(factory)))

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(factory.sort_values('Avg_Margin_%', ascending=True),
                     x='Avg_Margin_%', y='Factory', orientation='h',
                     color='Avg_Margin_%', color_continuous_scale='RdYlGn',
                     range_color=[0, 100], text='Avg_Margin_%',
                     labels={'Avg_Margin_%':'Avg Gross Margin %', 'Factory':''})
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                          textfont=dict(size=11, color='#9090b8'))
        fig.add_vline(x=50, line_dash='dash', line_color='#ef4444',
                      annotation_text='50% target', annotation_font_color='#ef4444')
        fig.update_layout(**PLOT_THEME, title='Average Gross Margin % by Factory', height=360,
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Revenue', x=factory['Factory'], y=factory['Total_Sales'],
                             marker_color='#8250ff', opacity=0.8,
                             hovertemplate='Revenue: $%{y:,.0f}<extra></extra>'))
        fig.add_trace(go.Bar(name='Profit',  x=factory['Factory'], y=factory['Total_Profit'],
                             marker_color='#00c4a7', opacity=0.8,
                             hovertemplate='Profit: $%{y:,.0f}<extra></extra>'))
        fig.update_layout(**PLOT_THEME, title='Revenue vs Profit by Factory',
                          barmode='group', height=360, xaxis_tickangle=-20,
                          yaxis_title='Amount ($)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='section-title'>Product–Factory Breakdown</div>", unsafe_allow_html=True)
    prod_factory = prod[['Factory','Division','Product Name','Total_Sales','Total_Profit',
                          'Gross_Margin_Pct','Profit_per_Unit','Risk_Flag']].sort_values(
        ['Factory','Total_Profit'], ascending=[True,False])
    prod_factory.columns = ['Factory','Division','Product','Revenue ($)','Profit ($)',
                             'Margin %','Profit/Unit','Risk']
    st.dataframe(prod_factory.style.format({
        'Revenue ($)':'${:,.0f}', 'Profit ($)':'${:,.0f}',
        'Margin %':'{:.1f}%', 'Profit/Unit':'${:.2f}'
    }).background_gradient(subset=['Margin %'], cmap='RdYlGn', vmin=0, vmax=100),
    use_container_width=True, height=380, hide_index=True)

    # Factory profitability radar
    st.markdown("<div class='section-title'>Factory Multi-Metric Comparison</div>", unsafe_allow_html=True)
    factory_norm = factory.copy()
    for col in ['Total_Sales','Total_Profit','Avg_Margin_%','Total_Units']:
        factory_norm[col+'_norm'] = (factory_norm[col] - factory_norm[col].min()) / \
                                    (factory_norm[col].max() - factory_norm[col].min() + 1e-9)
    categories = ['Revenue','Profit','Margin','Volume']
    fig = go.Figure()
    for _, row in factory_norm.iterrows():
        vals = [row['Total_Sales_norm'], row['Total_Profit_norm'],
                row['Avg_Margin_%_norm'], row['Total_Units_norm']]
        vals += [vals[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=categories + [categories[0]],
            fill='toself', name=row['Factory'],
            line_color=FACTORY_COLORS.get(row['Factory'], '#888'),
            opacity=0.65
        ))
    fig.update_layout(**PLOT_THEME, title='Factory Performance Radar (Normalized)',
                      polar=dict(bgcolor='rgba(0,0,0,0)',
                                 radialaxis=dict(gridcolor='#1a1a2a', color='#5a5a80', showticklabels=False),
                                 angularaxis=dict(gridcolor='#1a1a2a', color='#8080a8')),
                      height=420)
    st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#2a2a50; font-size:11px; letter-spacing:0.1em; padding:20px 0 10px;'>
NASSAU CANDY DISTRIBUTOR &nbsp;·&nbsp; PRODUCT LINE PROFITABILITY INTELLIGENCE &nbsp;·&nbsp; CONFIDENTIAL
</div>
""", unsafe_allow_html=True)

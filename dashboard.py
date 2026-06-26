import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =====================================================================
# 1. STREAMLIT CONFIGURATION & BRANDING DESIGN
# =====================================================================
st.set_page_config(page_title="Naivas Kahawa Sukari LP Center", layout="wide")

st.markdown("""
    <style>
    h1 { color: #1b4d3e !important; font-weight: 800 !important; }
    h2, h3 { color: #e67e22 !important; font-weight: 700 !important; }
    
    section[data-testid="stSidebar"] {
        background-color: #0f2b23 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    div[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: bold;
    }
    hr { border-top: 2px solid #e67e22 !important; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. DATA ENGINE
# =====================================================================
@st.cache_data
def load_clean_data():
    np.random.seed(42)
    random.seed(42)
    
    skus = {
        'FRESH': ['Beef_Prime_Cuts_1kg', 'Chicken_Full_Capon', 'Fresh_Produce_Combo', 'Kienyeji_Chicken'],
        'FMCG': ['Brookside_Milk_500ml', 'Cooking_Oil_5L', 'Sugar_2kg', 'Rice_5kg', 'Detergent_5L', 'Soap_Bar'],
        'GM': ['TV_43in', 'Headphones', 'Whiskey_750ml', 'Wine_750ml', 'Bio_Oil', 'Face_Cream', 'Tissue_12pack']
    }
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # RE-NAMED: Admin_Error changed entirely to Receiving_Error
    causes = ['Theft', 'Damage', 'Receiving_Error', 'Spoilage', 'Supplier_Short']

    raw = []
    for _ in range(500):
        cls = random.choice(['GM', 'FMCG', 'FRESH'])
        sku = random.choice(skus[cls])
        hour = random.randint(0, 23)
        day = random.choice(days)
        
        if cls == 'FRESH':
            val, cause = random.randint(2000, 15000), random.choice(['Spoilage', 'Spoilage', 'Receiving_Error', 'Supplier_Short', 'Damage'])
        elif cls == 'FMCG':
            val, cause = random.randint(500, 8000), random.choice(['Theft', 'Receiving_Error', 'Spoilage', 'Supplier_Short', 'Damage'])
        else:
            val, cause = random.randint(15000, 75000), random.choice(['Theft', 'Theft', 'Theft', 'Receiving_Error', 'Damage'])

        if day == 'Friday' and hour in (19, 20, 21):
            val = int(val * 2.5)
            if cls == 'GM': 
                cause = 'Theft'

        raw.append({'classification': cls, 'sku': sku, 'units_lost': random.randint(1, 4), 'kes_value': val, 'cause': cause, 'hour': hour, 'day': day})
    return pd.DataFrame(raw)

df = load_clean_data()

# =====================================================================
# 3. SIDEBAR CONTROL PANEL (VERIFIED OFFLINE LOCAL STORAGE FIRST)
# =====================================================================
import os

# First check if you successfully saved the png image to your directory folder
if os.path.exists("naivas_logo.png"):
    st.sidebar.image("naivas_logo.png", use_container_width=True)
else:
    # If file is missing, display a clean, fallback text header instead of a broken box token
    st.sidebar.markdown("<h1 style='text-align: center; color: #ffffff !important; letter-spacing: 2px;'>NAIVAS</h1>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: center; color: #e67e22 !important;'>LP Control Center</h3>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("Navigation Matrix")
nav = st.sidebar.radio(
    "Select Store Division:", 
    ["Total Branch View (Combined)", "GM", "FMCG", "FRESH"]
)

cause_filter = st.sidebar.selectbox("Filter by Root Cause:", ["All Causes"] + list(df['cause'].unique()))

st.sidebar.markdown("---")
st.sidebar.subheader("Strategic ROI Simulator")
allocated_budget = st.sidebar.number_input("Proposed Capital Expense (KES):", min_value=1000, value=35000, step=5000)
target_reduction = st.sidebar.slider("Target Shrink Reduction (%):", min_value=5, max_value=80, value=25, step=5)

# =====================================================================
# 4. RUNTIME DATA FILTER PROCESSING
# =====================================================================
if nav == "Total Branch View (Combined)":
    f_df = df.copy()
else:
    f_df = df[df['classification'] == nav]

if cause_filter != "All Causes":
    f_df = f_df[f_df['cause'] == cause_filter]

# =====================================================================
# 5. MAIN DISPLAY INTERFACE
# =====================================================================
st.title("Naivas Kahawa Sukari Shrinkage Analysis")
st.markdown(f"### Operational Command Matrix: **{nav}** — Active Root Filter: *{cause_filter}*")
st.markdown("---")

total_division_loss = f_df['kes_value'].sum()
if total_division_loss > 8000000 and cause_filter == "All Causes":
    st.error(f"🚨 **CRITICAL EXCEPTION ALERT**: Total branch audited loss has broken upper limit constraints (KES {total_division_loss:,}). Immediate supervisor auditing is recommended.")
elif not f_df.empty and f_df.groupby('sku')['kes_value'].sum().max() > 1500000:
    st.warning(f"⚠️ **SKU ANOMALY DETECTED**: A single inventory line item is currently driving disproportionate drain inside the layout grid.")

if f_df.empty:
    st.warning("No records match the active filter criteria combination.")
else:
    # 6. LIVE METRIC CARDS
    c1, c2, c3 = st.columns(3)
    c1.metric(label=f"Audited Financial Drain Scope", value=f"KES {total_division_loss:,}")
    c2.metric(label="Aggregated Units Deficit", value=f"{f_df['units_lost'].sum():,} Units")
    c3.metric(label="Top Margin-Bleeding SKU Line", value=f_df.groupby('sku')['kes_value'].sum().idxmax())
    st.markdown("---")

    # 7. WHAT LAYER: INTERACTIVE BRANDED PARETO CHART
    st.subheader("1. Margin Drain Concentration Portfolio (WHAT is Walking Out?)")
    s_loss = f_df.groupby('sku')['kes_value'].sum().reset_index().sort_values('kes_value', ascending=False).reset_index(drop=True)
    s_loss['cum_p'] = (s_loss['kes_value'].cumsum() / total_division_loss) * 100

    fig_p = go.Figure([
        go.Bar(x=s_loss['sku'], y=s_loss['kes_value'], name='KES Loss', marker_color='#1b4d3e', hovertemplate='Loss: KES %{y:,.0f}'),
        go.Scatter(x=s_loss['sku'], y=s_loss['cum_p'], name='Cumulative Weight %', yaxis='y2', mode='lines+markers', marker_color='#e67e22')
    ])
    fig_p.update_layout(template="plotly_white", margin=dict(t=20, b=20, l=40, r=40), height=360,
                        yaxis=dict(title="Aggregated Loss (KES)", tickformat=","),
                        yaxis2=dict(title="Cumulative Weight Summary (%)", overlaying='y', side='right', range=[0, 105]), legend=dict(x=0.01, y=0.99))
    st.plotly_chart(fig_p, use_container_width=True)
    st.markdown("---")

       # 8. WHEN LAYER: CORPORATE HIGH-CONTRAST GREEN & BLACK HEATMAP
    st.subheader("2. 24-Hour Operational Vulnerability Hotspots (WHEN Do We Bleed?)")
    st.markdown("*Absolute black matrix blocks represent safe windows. Luminous green configurations expose active branch vulnerabilities.*")
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Strictly maps a full, solid 24-hour retail cycle index array (0 to 23)
    all_hours = list(range(0, 24))
    h_temp = pd.DataFrame(0, index=all_hours, columns=days_order)
    
    pivot_table = f_df.pivot_table(values='kes_value', index='hour', columns='day', aggfunc=np.sum).fillna(0)
    h_temp.update(pivot_table)

    # BRAND CONTRAST FIX: 0 loss sits at pitch black, scaling up into Naivas Dark Green and vivid orange flashpoints
    naivas_green_black_scale = [
        [0.0, '#000000'],   # Pure matte black backdrop for quiet operational hours (drops the blue glare completely)
        [0.1, '#0b1f19'],   # Low level bleed trace (Muted Dark Green)
        [0.4, '#1b4d3e'],   # Base Naivas Corporate Dark Green for standard risk blocks
        [0.7, '#e67e22'],   # Elevated vulnerability indicator (Naivas Orange)
        [1.0, '#00ff66']    # Critical branch threat targets glow in crisp fluorescent neon green
    ]

    fig_h = px.imshow(h_temp, labels=dict(x="Day of Week", y="Hour of Day", color="Loss Index"), x=days_order, y=all_hours,
                      color_continuous_scale=naivas_green_black_scale)
    
    fig_h.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=520,
        # FIXED: Changed dtick=1 and tickmode='linear' to force the rendering of all 24 individual hours on screen
        yaxis=dict(autorange="reversed", title="24-Hour Shift Cycle Tracking", tickmode='linear', dtick=1), 
        xaxis=dict(title="Weekly Operational Timeline View Matrix")
    )
    st.plotly_chart(fig_h, use_container_width=True)
    st.markdown("---")


    # 9. INTEGRATED SIMULATOR ROI OUTPUT DISPLAY BLOCK
    st.subheader("3. Capital Expenditure Recovery Model (Live Capital Simulation Results)")
    projected_savings = int(total_division_loss * (target_reduction / 100.0))
    net_return = projected_savings - allocated_budget
    payback_months = (allocated_budget / (projected_savings / 12.0)) if projected_savings > 0 else 0
    
    sim1, sim2, sim3 = st.columns(3)
    sim1.info(f"**Gross Annual Savings**: KES {projected_savings:,}")
    sim2.success(f"**Net First-Year Return**: KES {net_return:,}")
    sim3.warning(f"**Estimated Payback Horizon**: {payback_months:.1f} Months")
    
# =====================================================================
# 10. ADVANCED RETAIL ANALYTICS WORKSPACE LAYER (FIXED INDEX LOGIC)
# =====================================================================
st.markdown("---")
st.subheader("4. Advanced Retail Analytics Framework (LP Predictive Intelligence Models)")

# MODEL A: OPERATIONAL VALUE LOSS BREAKDOWN INDEX (WITH DRILL-DOWN)
st.markdown("#### Model A: Operational Value Loss Breakdown Index")
if not f_df.empty:
    # 1. Core Summary Calculation
    cause_summary = f_df.groupby('cause')['kes_value'].agg(['sum', 'count', 'mean']).reset_index()
    cause_summary.columns = ['Root Cause Trigger', 'Total Loss (KES)', 'Incident Frequency Count', 'Average Loss Cost per Incident']
    cause_summary = cause_summary.sort_values(by='Total Loss (KES)', ascending=False).reset_index(drop=True)
    cause_summary.index = cause_summary.index + 1
    
    # Render the main summary matrix table
    st.dataframe(cause_summary.style.format({
        'Total Loss (KES)': 'KES {:,}',
        'Incident Frequency Count': '{:,}',
        'Average Loss Cost per Incident': 'KES {:,.2f}'
    }), use_container_width=True)
    
    # 2. FEATURE UPGRADE: Interactive Product Drill-Down
    st.markdown("🔍 **Deep-Dive Explorer**")
    selected_drill_cause = st.selectbox(
        "Select a cause above to isolate the exact bleeding SKUs:", 
        options=list(cause_summary['Root Cause Trigger']),
        key="drill_down_selector"
    )
    
    # Filter dataset down to the selected cause to identify the culprit products
    drill_df = f_df[f_df['cause'] == selected_drill_cause]
    sku_drill = drill_df.groupby('sku')['kes_value'].agg(['sum', 'count']).reset_index()
    sku_drill.columns = ['Culprit Product SKU', 'Total Leaked Value (KES)', 'Loss Event Count']
    sku_drill = sku_drill.sort_values(by='Total Leaked Value (KES)', ascending=False).reset_index(drop=True)
    sku_drill.index = sku_drill.index + 1
    
    st.markdown(f"*Displaying top SKUs leaking via **{selected_drill_cause}**:*")
    st.dataframe(sku_drill.style.format({
        'Total Leaked Value (KES)': 'KES {:,}',
        'Loss Event Count': '{:,}'
    }), use_container_width=True)

else:
    st.info("Insufficient data traces inside the current active filter scope to run modeling loops.")

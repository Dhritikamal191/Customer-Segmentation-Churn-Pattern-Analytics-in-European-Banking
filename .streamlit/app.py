import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #F5F7FA;
    color: #1F2937;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #F5F7FA;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #1F2937;
}

/* Headers */
h1, h2, h3, h4 {
    color: #2563EB;
}

/* KPI Cards */
.kpi-box {
    background: linear-gradient(135deg, #FFFFFF, #E5E7EB);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: #1F2937;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}

/* KPI Title */
.kpi-title {
    font-size: 14px;
    color: #6B7280;
}

/* KPI Value */
.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: #2563EB;
}

/* Buttons */
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    border: none;
}

.stButton>button:hover {
    background-color: #1D4ED8;
    color: white;
}

/* DataFrame */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    color: #1F2937;
    border-radius: 10px;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}

/* Input widgets */
input, textarea, select {
    background-color: #FFFFFF !important;
    color: #1F2937 !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #2563EB;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Remove top white header */
header[data-testid="stHeader"] {
    background-color: transparent;
}

/* Remove top padding space */
.block-container {
    padding-top: 1rem;
}

/* Remove toolbar white background */
div[data-testid="stToolbar"] {
    background-color: transparent;
}

/* Optional: hide Streamlit branding (top right icons area background) */
div[data-testid="stDecoration"] {
    background: transparent;
}

/* Make full page smooth */
.stApp {
    background-color: #F5F7FA;
}

.header-box {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.header-title {
    font-size: 28px;
    font-weight: bold;
}

.header-subtitle {
    font-size: 14px;
    opacity: 0.9;
}


/*  Slider color */
.stSlider > div > div > div > div {
    background-color: #2563EB !important;  /* Blue */
}

/*  Slider handle */
.stSlider > div > div > div > div > div {
    background-color: #1D4ED8 !important;
    border: 2px solid #2563EB !important;
}

/*  Multiselect selected items (chips) */
span[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: white !important;
}

/*  Dropdown focus border */
div[data-baseweb="select"] > div {
    border-color: #2563EB !important;
}

/*  Sidebar headers (optional styling) */
section[data-testid="stSidebar"] h3 {
    color: #2563EB !important;
}


</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <div class="header-title">
        📊 Customer Segmentation & Churn Pattern Analytics in European Banking
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.image("Images/unified.png",width=150)
st.set_page_config(layout="wide")

st.divider()

#Load Dataset
df= pd.read_csv("Data/European_Bank.csv")

df["Geography"]=df["Geography"].fillna("Unknown")
df["ValueSegment"]=pd.cut(df["Balance"],bins=[0,50000,100000,df["Balance"].max()],labels=["Low Value","Medium Value","High Value"])
df["EstimatedSalary"]=df["EstimatedSalary"].astype(float)
df["Balance"]=df["Balance"].astype(float)

bins = [0, 30, 45, 60, 100]
labels = ["<30", "30-45", "46-60", "60+"]
df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels)

st.sidebar.header("Segment Filters")

salary_min, salary_max=st.sidebar.slider("Salary Range", float(df["EstimatedSalary"].min()), float(df["EstimatedSalary"].max()), (float(df["EstimatedSalary"].min()),float(df["EstimatedSalary"].max())))
balance_min, balance_max=st.sidebar.slider("Balance Range", float(df["Balance"].min()), float(df["Balance"].max()),(float(df["Balance"].min()),float(df["Balance"].max())))

value_filter=st.sidebar.selectbox("Customer Value Segment",["All","Low Value","Medium Value","High Value"])

geo_filter = st.sidebar.multiselect(
    "Select Geography",
    options=sorted(df["Geography"].dropna().unique()),
    default=[]
)

gender_filter=st.sidebar.selectbox("Gender",["All"]+list(df["Gender"].unique()))

active_filter = st.sidebar.selectbox("Active Membership",["All", "Active", "Inactive"])

card_filter = st.sidebar.selectbox("Credit Card Status",["All", "Has Card", "No Card"])

product_filter = st.sidebar.selectbox("Number of Products",["All"] + sorted(df["NumOfProducts"].dropna().unique()))

age_filter = st.sidebar.selectbox("Age Group",["All"] + labels)

tenure_filter=st.sidebar.selectbox("Tenure",["All"]+sorted(df["Tenure"].unique()))

filtered_df=df.copy()

if value_filter !="All":
   filtered_df=filtered_df[filtered_df["ValueSegment"]==value_filter]
 
if geo_filter:
    filtered_df = filtered_df[filtered_df["Geography"].isin(geo_filter)]

if gender_filter !="All":
   filtered_df=filtered_df[filtered_df["Gender"]==gender_filter]

if active_filter != "All":
    if active_filter == "Active":
        filtered_df = filtered_df[filtered_df["IsActiveMember"] == 1]
    else:
        filtered_df = filtered_df[filtered_df["IsActiveMember"] == 0]

if card_filter != "All":
    if card_filter == "Has Card":
        filtered_df = filtered_df[filtered_df["HasCrCard"] == 1]
    else:
        filtered_df = filtered_df[filtered_df["HasCrCard"] == 0]

if product_filter != "All":
    filtered_df = filtered_df[filtered_df["NumOfProducts"] == product_filter]

if age_filter != "All":
    filtered_df = filtered_df[filtered_df["AgeGroup"] == age_filter]

if tenure_filter !="All":
   filtered_df=filtered_df[filtered_df["Tenure"]==tenure_filter]
    
filtered_df=filtered_df[(filtered_df["EstimatedSalary"]>=salary_min) & (filtered_df["EstimatedSalary"]<=salary_max) & (filtered_df["Balance"]>=balance_min) & (filtered_df["Balance"]<=balance_max)]


# =============================
# Overall Churn Rate
# ===============================
overall_churn_rate=(df["Exited"].sum()/df.shape[0])*100
if pd.isna(overall_churn_rate):
   overall_churn_rate=0

# ===============================
# Segment Churn Rate
# ===============================
if filtered_df.shape[0] > 0:
    segment_rate = (filtered_df["Exited"].sum() / filtered_df.shape[0]) * 100
else:
    segment_rate = 0

# ===============================
# High Value Churn
# ===============================
high_value=filtered_df[filtered_df["ValueSegment"]=="High Value"]
if high_value.shape[0]>0:
   high_value_churn_ratio=(high_value["Exited"].sum()/high_value.shape[0])*100
else:
     high_value_churn_ratio=0
# ============================
# Engagement Risk Indicator
# ============================
engagement_drop=filtered_df[filtered_df["IsActiveMember"]==0]["Exited"].mean()
if pd.isna(engagement_drop):
   engagement_drop=0
engagement_drop *=100
# ============================
# Geo Risk Index
# ============================

geo_risk=filtered_df.groupby("Geography")["Exited"].mean()*100
if geo_risk.empty:
   highest_geo="No Data"
   highest_rate=0
else:
     highest_geo=geo_risk.idxmax()
     highest_rate=geo_risk.max()

col1, col2, col3, col4, col5 = st.columns(5)

def kpi_card(title, value):
    return f"""
    <div class="kpi-box">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """

with col1:
    st.markdown(kpi_card("📊 Overall Churn Rate",
                         f"{overall_churn_rate:.2f}%"),
                unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card("📈 Segment Churn Rate",
                         f"{segment_rate:.2f}%"),
                unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card("📶 High Value Churn Ratio",
                         f"{high_value_churn_ratio:.2f}%"),
                unsafe_allow_html=True)

with col4:
    st.markdown(kpi_card("🧑‍🧑‍🧒‍🧒 Engagement Drop Indicator",
                         f"{engagement_drop:.2f}%"),
                unsafe_allow_html=True)

with col5:
    st.markdown(kpi_card("🌍 Geographic Risk Index",
                         f"{highest_rate:.2f}%"),
                unsafe_allow_html=True)

st.divider()

st.subheader("Overall Customer Distribution")
col1, col2=st.columns(2)
with col1:
     drill_option=st.selectbox("Drill Down By",["Geography","Gender","AgeGroup","NumOfProducts","HasCrCard","Tenure","Balance","EstimatedSalary"],key="drill_main")
     distribution= filtered_df[drill_option].value_counts()
     st.subheader(f"Customer Distribution by {drill_option}")
     st.scatter_chart(distribution)
with col2:
     next_options=["Geography","Gender","AgeGroup","NumOfProducts","HasCrCard","Tenure","Balance","EstimatedSalary"]
     next_options.remove(drill_option)
     next_drill=st.selectbox("Further Drill Down By",next_options,key="drill_sub")
     cross_distribution=filtered_df[next_drill].value_counts()
     st.subheader(f"{next_drill} Distribution in {drill_option}")
     st.bar_chart(cross_distribution)

st.subheader("Overall Customer Churn Summary")

col1, col2=st.columns(2)
with col1:
     drill_option=st.selectbox("Drill Down By",["Geography","Gender","AgeGroup","EstimatedSalary","NumOfProducts","HasCrCard","Balance","Tenure"],key="hv_drill")
     segment_churn=filtered_df.groupby(drill_option)["Exited"].mean()*100
     st.subheader(f"Churn Rate by {drill_option}")
     st.line_chart(segment_churn)
with col2:
     st.subheader(f"Customer Count vs Churn in {drill_option}")
     count_df=filtered_df.groupby(drill_option)["Exited"].agg(["count","sum"])
     count_df.columns=["Total Customers","Churned Customers"]
     st.bar_chart(count_df)
    
col1, col2=st.columns(2) 
with col1:
     st.subheader("Churn Rate Distribution")
     churn_dist=filtered_df["Exited"].value_counts(normalize=True)*100
     st.bar_chart(churn_dist)
with col2:
     st.subheader("Average Balance vs Churn")
     balance_churn=filtered_df.groupby("Exited")["Balance"].mean()
     st.bar_chart(balance_churn)

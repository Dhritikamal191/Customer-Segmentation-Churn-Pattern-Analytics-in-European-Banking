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

product_filter = st.sidebar.selectbox(
    "Number of Products",
    ["All"] + sorted(df["NumOfProducts"].dropna().unique())
)

age_filter = st.sidebar.selectbox(
    "Age Group",
    ["All"] + labels
)

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


st.subheader("Customer Distribution (Drill-Down)")

# ---------- STEP 1: AGE ----------
selected_age = st.selectbox(
    "Select Age Group",
    ["All"] + sorted(filtered_df["AgeGroup"].dropna().unique())
)

age_df = filtered_df.copy()

if selected_age != "All":
    age_df = age_df[age_df["AgeGroup"] == selected_age]


# ---------- STEP 2: GENDER ----------
selected_gender = st.selectbox(
    "Select Gender",
    ["All"] + sorted(age_df["Gender"].dropna().unique())
)

gender_df = age_df.copy()

if selected_gender != "All":
    gender_df = gender_df[gender_df["Gender"] == selected_gender]


# ---------- STEP 3: GEOGRAPHY ----------
selected_geo = st.selectbox(
    "Select Geography",
    ["All"] + sorted(gender_df["Geography"].dropna().unique())
)

final_df = gender_df.copy()

if selected_geo != "All":
    final_df = final_df[final_df["Geography"] == selected_geo]


# ---------- SAFETY CHECK ----------
if final_df.empty:
    st.warning(" No data for selected combination")
    st.stop()


# ---------- VISUALIZATION ----------
st.markdown("###  Distribution Overview")

fig = px.histogram(
    final_df,
    x="AgeGroup",
    color="Gender",
    title="Customer Distribution by Age & Gender",
    barmode="group"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Overall Customer Churn Summary")

drill_option=st.selectbox("Drill Down By",["Geography","Gender","AgeGroup"],key="hv_drill")

segment_churn=filtered_df.groupby(drill_option)["Exited"].mean()*100

st.subheader(f"Churn Rate by {drill_option}")
st.bar_chart(segment_churn)

selected_segment=st.selectbox(f"Select {drill_option}",filtered_df[drill_option].dropna().unique())

segment_df=filtered_df[filtered_df[drill_option]==selected_segment]

tenure_churn=segment_df.groupby("Tenure")["Exited"].mean()*100

st.subheader(f"Tenure Churn in {selected_segment}")

st.line_chart(tenure_churn)


st.markdown("### High Value Customer Churn Explorer")

df["Gender"]=df["Gender"].fillna("Unknown")
df["Exited"]=df["Exited"].map({0:0,1:1,"Yes":1,"No":0})
     
high_value_df=df[(df["Balance"]>df["Balance"].median()) | (df["EstimatedSalary"]>df["EstimatedSalary"].median())]

st.subheader("High Value Customer Churn by Geography")
geo_churn_group=high_value_df.groupby("Geography")["Exited"].mean().reset_index()
     

selected_geo=st.selectbox("Select Geography",options=geo_churn_group["Geography"].dropna().unique(),key="geo_select")
geo_churn_df=high_value_df[high_value_df["Geography"]==selected_geo]
st.subheader(f"Gender in {selected_geo}")
gender_churn_group=geo_churn_df.groupby("Gender")["Exited"].mean().reset_index()
st.bar_chart(gender_churn_group.set_index("Gender"))
   
st.subheader(f"Age Group in {selected_geo}")
age_group_df=geo_churn_df.groupby("AgeGroup")["Exited"].mean().reset_index()
st.area_chart(age_group_df.set_index("AgeGroup")) 

st.subheader("High Value Customer Churn by Balance")
    
high_value = df[df["Balance"] > df["Balance"].median()]
     
df["SalarySegment"] = pd.cut(df["EstimatedSalary"],bins=[0, 50000, 100000, df["EstimatedSalary"].max()],labels=["Low", "Medium", "High"])

df["BalanceSegment"] = df["Balance"].apply(lambda x: "Zero" if x == 0 else ("Low" if x <= 100000 else "High"))

salary_filter = st.selectbox("Select Salary Segment",["All"] + list(high_value["EstimatedSalary"].dropna().unique()))

activity_filter = st.selectbox("Active Member",["All", 1, 0])

product_filter = st.selectbox("Number of Products",["All"] + sorted(high_value["NumOfProducts"].unique()))
filtered_df = high_value.copy()

if salary_filter != "All":
   filtered_df = filtered_df[filtered_df["EstimatedSalary"] == salary_filter]

if activity_filter != "All":
   filtered_df = filtered_df[filtered_df["IsActiveMember"] == activity_filter]

if product_filter != "All":
   filtered_df = filtered_df[filtered_df["NumOfProducts"] == product_filter]

salary_churn = filtered_df.groupby("EstimatedSalary")["Exited"].mean() * 100

fig1 = go.Figure()

fig1.add_trace(go.Bar(x=salary_churn.index,y=salary_churn.values,name="Churn Rate"))

fig1.update_layout(title="Churn Rate by Salary Segment",xaxis_title="Salary Segment",yaxis_title="Churn Rate (%)")

st.plotly_chart(fig1, use_container_width=True)

engagement_churn = filtered_df.groupby("IsActiveMember")["Exited"].mean() * 100

fig2 = go.Figure()

fig2.add_trace(go.Bar(x=["Inactive", "Active"],y=engagement_churn.values,name="Churn Rate"))

fig2.update_layout(title="Churn by Activity Status",xaxis_title="Customer Activity",yaxis_title="Churn Rate (%)")

st.plotly_chart(fig2, use_container_width=True)

product_churn = filtered_df.groupby("NumOfProducts")["Exited"].mean() * 100

fig3 = go.Figure()

fig3.add_trace(go.Bar(x=product_churn.index,y=product_churn.values,name="Churn Rate"))

fig3.update_layout(title="Churn by Number of Products",xaxis_title="Products",yaxis_title="Churn Rate (%)")

st.plotly_chart(fig3, use_container_width=True)
       

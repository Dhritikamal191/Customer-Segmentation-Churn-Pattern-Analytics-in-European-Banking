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

st.markdown("""
<style>

/* Main selectbox field */
div[data-baseweb="select"] > div {
    background-color: #e6f0ff !important;  /* Light blue */
    border: 1px solid #3399ff !important;
    border-radius: 10px !important;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: #e6f0ff !important;  /* Same color as box */
    border-radius: 10px !important;
}

/* Dropdown options */
div[role="option"] {
    background-color: #e6f0ff !important;
    color: black !important;
}

/* Hover effect */
div[role="option"]:hover {
    background-color: #cce0ff !important;  /* Slight darker blue */
}

/* Selected option */
div[aria-selected="true"] {
    background-color: #99ccff !important;
    color: black !important;
}

/* Target the dropdown container */
.dropdown-options-container {
    background-color: #d1e9ff; 
    border: 1px solid #7cb9e8; 
    border-radius: 8px;       
    overflow: hidden;          
}

/* Target the individual items */
.dropdown-item {
    background-color: transparent;
    color: #333;
    padding: 10px;
}

/* Style the hover state to stay within the blue family */
.dropdown-item:hover {
    background-color: #b0d4ff; /* Slightly darker blue on hover */
}

/* This targets almost every common naming convention for dropdown lists */
[class*="dropdown"], [class*="select-items"], [class*="menu"], ul, li {
    background-color: #d1e9ff !important; /* Forces the blue */
    border-color: #7cb9e8 !important;
}

.PASTE_THE_CLASS_NAME_HERE {
    background-color: #d1e9ff !important;
}

</style>
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
segment_churn_rate=(filtered_df["Exited"].sum()/df.shape[0])*100
if pd.isna(segment_churn_rate):
   segment_churn_rate=0
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
                         f"{segment_churn_rate:.2f}%"),
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
tab1, tab2, tab3,tab4=st.tabs(["Distribution","Churn Rates","Churn Drivers","Engagement Analysis"])
with tab1:
     st.subheader("Overall Customer Distribution")

     if filtered_df.empty:
        st.warning("No data available for selected filters")
        st.stop()

     col1, col2=st.columns(2)
     with col1:
          drill_option=st.selectbox("Drill Down By",["Geography","Gender","AgeGroup","NumOfProducts","HasCrCard","Tenure","Balance","EstimatedSalary","IsActiveMember"],key="drill_main")
          distribution= filtered_df[drill_option].value_counts()
          st.subheader(f"Customer Distribution by {drill_option}")
          st.bar_chart(distribution)
     with col2:
          next_options=["Geography","Gender","AgeGroup","NumOfProducts","HasCrCard","Tenure","Balance","EstimatedSalary","IsActiveMember"]
          next_options.remove(drill_option)
          next_drill=st.selectbox("Further Drill Down By",next_options,key="drill_sub")
          cross_distribution=filtered_df[next_drill].value_counts()
          st.subheader(f"{next_drill} Distribution in {drill_option}")
          st.bar_chart(cross_distribution)

     st.subheader("📊 Overall Customer Distribution Insights")

     total_customers = filtered_df.shape[0]

     # Geography
     geo_dist = filtered_df["Geography"].value_counts(normalize=True) * 100
     top_geo = geo_dist.idxmax()
     top_geo_val = geo_dist.max()

     # Gender
     gender_dist = filtered_df["Gender"].value_counts(normalize=True) * 100
     top_gender = gender_dist.idxmax()
     top_gender_val = gender_dist.max()

     # Age Group
     age_dist = filtered_df["AgeGroup"].value_counts(normalize=True) * 100
     top_age = age_dist.idxmax()
     top_age_val = age_dist.max()

     # Credit Card
     card_dist = filtered_df["HasCrCard"].value_counts(normalize=True) * 100
     top_card = card_dist.idxmax()

     # Tenure
     avg_tenure = filtered_df["Tenure"].mean()

     # Financials
     avg_balance = filtered_df["Balance"].mean()
     avg_salary = filtered_df["EstimatedSalary"].mean()

     st.markdown(f"""
     ### 🔍 Key Observations

     - The dataset consists of **{total_customers} customers** after applying filters.  

     - **{top_geo}** accounts for the largest share of customers (**{top_geo_val:.2f}%**), indicating the bank’s strongest geographic presence.  

     - The customer base is predominantly **{top_gender} ({top_gender_val:.2f}%)**, showing demographic concentration.  

     - The most common age group is **{top_age} ({top_age_val:.2f}%)**, representing the core customer segment.  

     - Most customers **{'have' if top_card == 1 else 'do not have'} a credit card**, reflecting adoption of banking services.  

     - The average tenure is **{avg_tenure:.2f} years**, indicating the typical customer relationship duration.  

     - The average balance is **{avg_balance:.2f}**, while the average estimated salary is **{avg_salary:.2f}**, showing the financial profile of customers.  
     """)

     st.markdown("""
     ### 🔎 Distribution Pattern Insight

     - Customer distribution is uneven across geographic and demographic dimensions, indicating varying market penetration.  

     - A dominant age group suggests that the bank primarily serves a specific life-stage segment.  

     - Credit card ownership indicates the level of product adoption among customers.  

     - Tenure distribution reflects a mix of new and long-term customers, suggesting varying levels of loyalty.  

     - Financial attributes such as balance and salary highlight diversity in customer value and purchasing power.  
     """)

     st.markdown("""
     ### 💡 Business Interpretation

     - Strong presence in specific geographies highlights key markets for retention and expansion.  

     - Demographic concentration enables targeted marketing and personalized service offerings.  

     - Encouraging credit card adoption can improve customer engagement and revenue streams.  

     - Customers with lower tenure may require onboarding and engagement strategies to improve retention.  

     - Financial diversity suggests the need for customized financial products for different income and balance groups.  
     """)

with tab2:
     st.subheader("Overall Customer Churn Summary")

     if filtered_df.empty:
        st.warning("No data available for selected filters")
        st.stop()

     col1, col2=st.columns(2)
     with col1:
          drill_option=st.selectbox("Drill Down By",["Geography","Gender","AgeGroup","EstimatedSalary","NumOfProducts","HasCrCard","Balance","Tenure","IsActiveMember"],key="hv_drill")
          segment_churn=filtered_df.groupby(drill_option)["Exited"].mean()*100
          st.subheader(f"Churn Rate by {drill_option}")
          st.bar_chart(segment_churn)
         
     with col2:
          further_options=["Geography","Gender","AgeGroup","NumOfProducts","HasCrCard","Tenure","Balance","EstimatedSalary","IsActiveMember"]
          further_options.remove(drill_option)
          further_drill=st.selectbox("Further Drill Down By",further_options,key="drill_further")
          churn_dist=filtered_df.groupby(further_drill)["Exited"].mean()*100
          st.subheader(f"{further_drill} comparison with {drill_option}")
          st.bar_chart(churn_dist)

     st.subheader(f"Customer Count vs Churn in {drill_option}")
     count_df=filtered_df.groupby(drill_option)["Exited"].agg(["count","sum"])
     count_df.columns=["Total Customers","Churned Customers"]
     st.bar_chart(count_df)
    
     col1, col2=st.columns(2) 
     with col1:
          st.subheader("Churn Rate Distribution")

          churn_counts = filtered_df["Exited"].value_counts().reset_index()
          churn_counts.columns = ["Exited", "Count"]
          churn_counts["Exited"] = churn_counts["Exited"].map({0: "Retained",1: "Churned"})
          fig = px.pie(churn_counts,names="Exited",values="Count",hole=0.5,title="Customer Churn Distribution")
          fig.update_traces(textinfo="percent+label",marker=dict(colors=["#A3D5FF","#FF9AA2"]))
          st.plotly_chart(fig, use_container_width=True)
         
     with col2:
          st.subheader("Average Balance vs Churn")

          balance_churn = (filtered_df.groupby("Exited")["Balance"].mean().reset_index())
          balance_churn["Exited"] = balance_churn["Exited"].map({0: "Retained",1: "Churned"})
          fig = px.pie(balance_churn,names="Exited",values="Balance",hole=0.5,title="Average Balance Distribution (Churn vs Retained)")
          fig.update_traces(textinfo="percent+label",marker=dict(colors=["#A3D5FF","#FF9AA2"]))
          st.plotly_chart(fig, use_container_width=True)
 
     st.subheader("📊 Overall Churn Summary Insights")

     # Overall churn
     overall_churn = filtered_df["Exited"].mean() * 100

     # Geography churn
     geo_churn = filtered_df.groupby("Geography")["Exited"].mean() * 100
     top_geo = geo_churn.idxmax()
     top_geo_val = geo_churn.max()

     # Gender churn
     gender_churn = filtered_df.groupby("Gender")["Exited"].mean() * 100
     top_gender = gender_churn.idxmax()
     top_gender_val = gender_churn.max()

     # Age churn
     age_churn = filtered_df.groupby("AgeGroup")["Exited"].mean() * 100
     top_age = age_churn.idxmax()
     top_age_val = age_churn.max()

     # Credit card
     card_churn = filtered_df.groupby("HasCrCard")["Exited"].mean() * 100
     high_card = card_churn.idxmax()
     high_card_val = card_churn.max()

     # Tenure
     tenure_churn = filtered_df.groupby("Tenure")["Exited"].mean() * 100
     top_tenure = tenure_churn.idxmax()
     top_tenure_val = tenure_churn.max()

     # Balance impact
     balance_churn = filtered_df.groupby("Exited")["Balance"].mean()
     retained_balance = balance_churn.get(0, 0)
     churned_balance = balance_churn.get(1, 0)

     # Salary impact
     salary_churn = filtered_df.groupby("Exited")["EstimatedSalary"].mean()
     retained_salary = salary_churn.get(0, 0)
     churned_salary = salary_churn.get(1, 0)

     st.markdown(f"""
     ### 🔍 Key Observations

     - Overall churn rate is **{overall_churn:.2f}%**, representing total customer attrition.  

     - **{top_geo}** shows the highest churn (**{top_geo_val:.2f}%**), indicating a high-risk geographic region.  

     - Churn is highest among **{top_gender} customers ({top_gender_val:.2f}%)**, showing demographic influence.  

     - The **{top_age} age group** has the highest churn (**{top_age_val:.2f}%**), indicating age-related behavioral patterns.  

     - Customers who **{'have' if high_card == 1 else 'do not have'} a credit card** show higher churn (**{high_card_val:.2f}%**).  

     - Peak churn occurs at **tenure = {top_tenure} years ({top_tenure_val:.2f}%)**, highlighting critical lifecycle stage.
     """)

     st.markdown("""
     ### 🔎 Churn Distribution Insight

     - Churn is not evenly distributed and varies significantly across demographic and behavioral factors.  

     - Certain groups contribute disproportionately to churn, indicating targeted retention opportunities.  

     - Customer lifecycle (tenure) plays a key role in determining churn behavior.
     """)

     st.markdown(f"""
     ### 💰 Financial Insight

     - Average balance of retained customers is **{retained_balance:.2f}**, while churned customers have **{churned_balance:.2f}**.  

     - Average estimated salary for retained customers is **{retained_salary:.2f}**, compared to **{churned_salary:.2f}** for churned customers.  

     - This suggests that {'higher-value customers are at risk' if churned_balance > retained_balance else 'lower balance customers are more prone to churn'},impacting overall revenue.
     """)

     st.markdown("""
     ### 💡 Business Interpretation

     - Churn is influenced by multiple factors including geography, demographics, and customer behavior.  

     - High-risk regions and customer groups should be prioritized for retention strategies.  

     - Early tenure stages may require stronger onboarding and engagement efforts.  

     - Financial insights highlight the need to protect high-value customers from churn.  

     - Personalized strategies based on customer profile can significantly reduce churn.
     """)
        
with tab3:
     st.subheader("Churn Drivers Analysis")

     if filtered_df.empty:
        st.warning("No data available for selected filters")
        st.stop()

     col1, col2 = st.columns(2)
         
     with col1:
          driver_option = st.selectbox("Analyze Churn By",["Geography", "Gender", "AgeGroup", "NumOfProducts", "IsActiveMember", "HasCrCard"],key="churn_driver_main")
          churn_driver = filtered_df.groupby(driver_option)["Exited"].mean() * 100
          st.subheader(f"Churn Rate by {driver_option}")
          st.area_chart(churn_driver)

     with col2:
          next_options = ["Geography", "Gender", "AgeGroup", "NumOfProducts", "IsActiveMember", "HasCrCard"]
          next_options.remove(driver_option)
          sub_driver = st.selectbox("Drill Down Further By",next_options,key="churn_driver_sub")
          cross_churn = (filtered_df.groupby([driver_option, sub_driver])["Exited"].mean() * 100).unstack()

          st.subheader(f"{sub_driver} Impact within {driver_option}")
          st.bar_chart(cross_churn)
     
     st.subheader("🔍 Churn Driver Insights")

     # Main driver insight
     top_driver = churn_driver.idxmax()
     top_value = churn_driver.max()

     # Lowest driver
     low_driver = churn_driver.idxmin()
     low_value = churn_driver.min()

     st.markdown(f"""
     ###  Key Observations

     - Highest churn is observed in **{top_driver} ({top_value:.2f}%)**, indicating this segment is most at risk.  

     - Lowest churn is seen in **{low_driver} ({low_value:.2f}%)**, suggesting better customer retention in this group.  
     """)

     # From cross churn (2-level drill)
     try:
         max_combination = cross_churn.stack().idxmax()
         max_value = cross_churn.max().max()

         st.markdown(f"""
         ### 🔎 Deep Dive Insight

         - The highest churn occurs in **{max_combination[0]} → {max_combination[1]} ({max_value:.2f}%)**,highlighting a critical high-risk customer segment.
     """)
     except:
            st.info("Not enough data for deeper insights")

     st.markdown("""
     ###  Business Interpretation

     - Certain customer segments show significantly higher churn, indicating targeted retention strategies are required.  

     - Behavioral factors like **activity status and product usage** strongly influence churn.  

     - Demographic differences suggest that churn patterns vary across regions and customer groups.  
     """)

with tab4:
     st.subheader("Engagement Analysis")
                     
     if filtered_df.empty:
        st.warning("No data available for selected filters")
        st.stop()

     col1, col2 = st.columns(2)

     with col1:
          engagement_driver = st.selectbox("Analyze Engagement By",["IsActiveMember", "NumOfProducts", "AgeGroup", "Geography", "Gender"],key="engagement_main")

          engagement_rate = filtered_df.groupby(engagement_driver)["Exited"].mean() * 100

          st.subheader(f"Churn Rate by {engagement_driver}")
          st.area_chart(engagement_rate)

     with col2:
          next_options = ["IsActiveMember", "NumOfProducts", "AgeGroup", "Geography", "Gender"]
          next_options.remove(engagement_driver)

          engagement_sub = st.selectbox("Drill Down Further By",next_options,key="engagement_sub")

          cross_engagement = (filtered_df.groupby([engagement_driver, engagement_sub])["Exited"].mean() * 100).unstack()

          st.subheader(f"{engagement_sub} Impact within {engagement_driver}")
          st.bar_chart(cross_engagement)

     st.subheader("🔍 Engagement Insights")

     # Active vs Inactive churn
     active_churn = filtered_df[filtered_df["IsActiveMember"] == 1]["Exited"].mean() * 100
     inactive_churn = filtered_df[filtered_df["IsActiveMember"] == 0]["Exited"].mean() * 100

     st.markdown(f"""
     ### 📊 Key Observations

     - Active customers have a churn rate of **{active_churn:.2f}%**, while inactive customers churn at **{inactive_churn:.2f}%**.  

     - This indicates that **inactive customers are significantly more likely to churn**, making engagement a critical factor in retention.  
     """)

     top_engagement = engagement_rate.idxmax()
     top_value = engagement_rate.max()

     st.markdown(f"""
     - The highest churn within engagement analysis is observed in **{top_engagement} ({top_value:.2f}%)**,highlighting a key risk group.
     """)

     try:
         max_combo = cross_engagement.stack().idxmax()
         max_val = cross_engagement.max().max()

         st.markdown(f"""
         ### 🔎 Deep Dive Insight

         - The most critical segment is **{max_combo[0]} → {max_combo[1]} ({max_val:.2f}%)**,indicating where engagement strategies should be focused.
     """)
     except:
            st.info("Not enough data for deeper insights")

     st.markdown("""
     ### 💡 Business Interpretation

     - Customer engagement plays a major role in churn behavior.  

     - Inactive customers are more likely to leave due to lack of interaction or perceived value.  

     - Increasing product usage and customer activity can significantly reduce churn.  

     - Targeted engagement strategies such as personalized offers and communication can improve retention.
     """)

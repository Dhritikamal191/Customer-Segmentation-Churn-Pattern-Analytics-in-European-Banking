import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #F5F7FA;
    color: #1F2937;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
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


st.sidebar.image("Images/unified.png",width=150)
st.set_page_config(layout="wide")
col1,col2=st.columns([0.5,6])

with col1:
     st.image("Images/bank.png",width=100)
with col2:
     st.title("Customer Segmentation & Churn Pattern Analytics in European Banking")

st.divider()

#Load Dataset
df= pd.read_csv("Data/European_Bank.csv")

df["Geography"]=df["Geography"].fillna("Unknown")
df["ValueSegment"]=pd.cut(df["Balance"],bins=[0,50000,100000,df["Balance"].max()],labels=["Low Value","Medium Value","High Value"])

st.sidebar.header("Segment Filters")

value_filter=st.sidebar.selectbox("Customer Value Segment",["All","Low Value","Medium Value","High Value"])

geo_filter=st.sidebar.selectbox("Geography",["All"]+list(df["Geography"].unique()))

gender_filter=st.sidebar.selectbox("Gender",["All"]+list(df["Gender"].unique()))

filtered_df=df.copy()

if value_filter !="All":
   filtered_df=filtered_df[filtered_df["ValueSegment"]==value_filter]

if geo_filter !="All":
   filtered_df=filtered_df[filtered_df["Geography"]==geo_filter]

if gender_filter  !="All":
   filtered_df=filtered_df[filtered_df["Gender"]==gender_filter]

 
# =============================
# Overall Churn Rate
# ===============================
overall_churn_rate=(filtered_df["Exited"].sum()/filtered_df.shape[0])*100

# ===============================
# Segment Churn Rate
# ===============================
segment_churn_rate=filtered_df[filtered_df["ValueSegment"]=="High Value"]

high_segment=filtered_df[filtered_df["ValueSegment"]=="High Value"]

if high_segment.shape[0]>0:
   segment_rate=(high_segment["Exited"].sum()/high_segment.shape[0])*100
else:
     segment_rate=0

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
inactive=filtered_df[filtered_df["IsActiveMember"]==0]

engagement_drop=(inactive["Exited"].sum()/inactive.shape[0])*100
# ============================
# Geo Risk Index
# ============================

geo_risk=filtered_df.groupby("Geography")["Exited"].mean()*100

highest_geo=geo_risk.idxmax()
highest_rate=geo_risk.max()

col1,col2,col3,col4,col5=st.columns(5)

with col1:
     icon,metric=st.columns([1,3])
     with icon:
          st.image("Images/overall.png",width=50)
     with metric:
          st.metric("Overall Churn Rate",f"{overall_churn_rate:.2f}%")

with col2:
     icon,metric=st.columns([1,3])
     with icon:
          st.image("Images/segment.png",width=50)
     with metric:
          st.metric("Segment Churn Rate",f"{segment_rate:.2f}%")

with col3:
     icon,metric=st.columns([1,3])
     with icon:
          st.image("Images/high.png",width=50)
     with metric:
          st.metric("High Value Churn Ratio",f"{high_value_churn_ratio:.2f}%")

with col4:
     icon,metric=st.columns([1,3])
     with icon:
          st.image("Images/indicator.png",width=50)
     with metric:
          st.metric("Engagement Drop Indicator",f"{engagement_drop:.2f}%")    

with col5:
     icon,metric=st.columns([1,3])
     with icon:
          st.image("Images/globe.png",width=50)
     with metric:
          st.metric("Geographic Risk Index",f"{highest_rate:.2f}%")

st.divider()

tab1,tab2,tab3,tab4,tab5=st.tabs(["Age vs Balance Distribution","Overall Churn Summary","Geography-wise Churn Visualization","Age-Tenure Churn Comparison","High-Value Customer Churn Explorer"]) 

with tab1:
     st.subheader("AGE DISTRIBUTION VS BALANCE DISTRIBUTION")

     filtered_df["AgeGroup"]=pd.cut(filtered_df["Age"],bins=[18,30,40,50,60,100],labels=["18-30","31-40","41-50","51-60","60+"])

     age_dist=filtered_df["AgeGroup"].value_counts().sort_index()

     st.subheader("Customer Distribution by Age Group")
     st.bar_chart(age_dist, use_container_width=True)

     selected_age=st.selectbox("Drill Down:Select Age Group",filtered_df["AgeGroup"].dropna().unique())

     age_df=filtered_df[filtered_df["AgeGroup"]==selected_age]
     st.subheader(f"Balance Distribution for Age Group {selected_age}")
     st.line_chart(age_df["Balance"].sort_values())


with tab2:
     overall_churn=filtered_df["Exited"].mean()*100

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

with tab3:
     st.header("Geography-wise churn visualization")

     selected_country=st.sidebar.multiselect("Select Geography",options=df["Geography"].unique())

     if selected_country:
        filtered_df=df[df["Geography"].isin(selected_country)]
     else:
          filtered_df=df.copy()

     geo_churn=filtered_df.groupby("Geography")["Exited"].mean()*100

     st.subheader("Churn Rate by Geography")
     st.bar_chart(geo_churn) 


     selected_geo=st.selectbox("Drill Down:Select Geography",filtered_df["Geography"].unique())

     geo_df=filtered_df[filtered_df["Geography"]==selected_geo]
     segment_churn=geo_df.groupby("ValueSegment")["Exited"].mean()*100
     st.subheader(f"Segment Churn in {selected_geo}")
     st.bar_chart(segment_churn)

with tab4:
     st.header("Age and Tenure Churn Comparison")

     filtered_df["AgeGroup"]=pd.cut(filtered_df["Age"],bins=[18,30,40,50,60,100],labels=["18-30","31-40","41-50","51-60","60+"])

     age_churn=filtered_df.groupby("AgeGroup")["Exited"].mean()*100

     st.subheader("Churn Rate by Age Group")
     st.bar_chart(age_churn)

     selected_age=st.selectbox("Drill Down:Select Age Group",filtered_df["AgeGroup"].unique())

     age_df=filtered_df[filtered_df["AgeGroup"]==selected_age]

     tenure_churn=age_df.groupby("Tenure")["Exited"].mean()*100
     st.subheader(f"Tenure Churn for Age Group {selected_age}")
     st.line_chart(tenure_churn)

with tab5:
     st.markdown("### High Value Customer Churn Explorer")

     df["Gender"]=df["Gender"].fillna("Unknown")
     df["Exited"]=df["Exited"].map({0:0,1:1,"Yes":1,"No":0})
     df["AgeGroup"]=pd.cut(df["Age"],bins=[18,30,40,50,60,100],labels=["18-30","31-40","41-50","51-60","60+"])
     high_value_df=df[(df["Balance"]>df["Balance"].median()) | (df["EstimatedSalary"]>df["EstimatedSalary"].median())]

     st.subheader("High Value Customer Churn by Geography")
     geo_churn_group=high_value_df.groupby("Geography")["Exited"].mean().reset_index()
     st.bar_chart(geo_churn_group.set_index("Geography"))

     selected_geo=st.selectbox("Select Geography",options=geo_churn_group["Geography"].dropna().unique(),key="geo_select")
     geo_churn_df=high_value_df[high_value_df["Geography"]==selected_geo]
     st.subheader(f"Gender in {selected_geo}")
     gender_churn_group=geo_churn_df.groupby("Gender")["Exited"].mean().reset_index()
     st.bar_chart(gender_churn_group.set_index("Gender"))
   
     st.subheader(f"Age Group in {selected_geo}")

     age_group_df=geo_churn_df.groupby("AgeGroup")["Exited"].mean().reset_index()
     st.line_chart(age_group_df.set_index("AgeGroup")) 

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
       

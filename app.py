import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Lulu UAE Performance Dashboard", layout="wide")

# Title
st.title("📊 Lulu UAE Performance Dashboard")

# Load your CSV
df = pd.read_csv("lulu_uae_master_2000.csv")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

city = st.sidebar.multiselect("City", df["city"].unique(), default=df["city"].unique())
channel = st.sidebar.multiselect("Channel", df["channel"].unique(), default=df["channel"].unique())
department = st.sidebar.multiselect("Department", df["department"].unique(), default=df["department"].unique())
gender = st.sidebar.multiselect("Gender", df["gender"].unique(), default=df["gender"].unique())
loyalty = st.sidebar.selectbox("Loyalty Member", ["All", "Yes", "No"], index=0)

# Apply filters
filtered_df = df[
    (df["city"].isin(city)) &
    (df["channel"].isin(channel)) &
    (df["department"].isin(department)) &
    (df["gender"].isin(gender))
]

if loyalty != "All":
    filtered_df = filtered_df[filtered_df["loyalty_member"] == (1 if loyalty == "Yes" else 0)]

# KPIs
st.subheader("📌 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

total_revenue = f"AED {filtered_df['line_value_aed'].sum():,.0f}"
avg_order_value = f"AED {filtered_df['line_value_aed'].mean():,.0f}"
return_rate = round((filtered_df["returned"].sum() / filtered_df.shape[0]) * 100, 1) if "returned" in filtered_df else 0
loyalty_pct = round((filtered_df[filtered_df["loyalty_member"] == 1].shape[0] / filtered_df.shape[0]) * 100, 1) if "loyalty_member" in filtered_df else 0
total_discounts = f"AED {filtered_df['discount_aed'].sum():,.0f}"

col1.metric("Total Revenue", total_revenue)
col2.metric("Avg Order Value", avg_order_value)
col3.metric("Return Rate", f"{return_rate}%")
col4.metric("Loyalty %", f"{loyalty_pct}%")
col5.metric("Total Discounts", total_discounts)

# Tabs for deeper analysis
tab1, tab2, tab3 = st.tabs(["Geography & Channels", "Products & Brands", "Customer Demographics"])

with tab1:
    st.subheader("🌍 Revenue by City")
    city_summary = filtered_df.groupby("city")["line_value_aed"].sum().reset_index()
    fig_city = px.bar(city_summary, x="city", y="line_value_aed", text="line_value_aed", color="city",
                      title="Revenue by City", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_city, use_container_width=True)

    st.subheader("📡 Channel Split")
    channel_summary = filtered_df.groupby("channel")["line_value_aed"].sum().reset_index()
    fig_channel = px.pie(channel_summary, names="channel", values="line_value_aed", hole=0.4,
                         title="Revenue by Channel", color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig_channel, use_container_width=True)

with tab2:
    st.subheader("🏷️ Sales by Brand")
    brand_summary = filtered_df.groupby("brand")["line_value_aed"].sum().reset_index()
    fig_brand = px.bar(brand_summary, x="brand", y="line_value_aed", text="line_value_aed", color="brand",
                       title="Sales by Brand", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_brand, use_container_width=True)

with tab3:
    st.subheader("👥 Customer Age Distribution")
    fig_age = px.histogram(filtered_df, x="age", nbins=20, color="gender",
                           title="Customer Age Distribution", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_age, use_container_width=True)

    st.subheader("🌐 Nationality Group Split")
    nationality_summary = filtered_df.groupby("nationality_group")["line_value_aed"].sum().reset_index()
    fig_nat = px.pie(nationality_summary, names="nationality_group", values="line_value_aed", hole=0.3,
                     title="Revenue by Nationality Group", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig_nat, use_container_width=True)

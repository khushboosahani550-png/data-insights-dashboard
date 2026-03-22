import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.helpers import compute_kpis

st.set_page_config(page_title="Data Dashboard", layout="wide")

# Title
st.title("📊 Interactive Data Analytics Dashboard")

# Load Data
df = load_data("lulu_uae_master_2000.csv")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

columns = df.columns.tolist()
selected_column = st.sidebar.selectbox("Select Column", columns)

unique_values = df[selected_column].unique()
selected_value = st.sidebar.selectbox("Select Value", unique_values)

filtered_df = df[df[selected_column] == selected_value]

# KPIs
st.subheader("📌 Key Performance Indicators")
kpis = compute_kpis(filtered_df)

col1, col2, col3 = st.columns(3)

for i, (key, value) in enumerate(kpis.items()):
    if i % 3 == 0:
        col1.metric(key, value)
    elif i % 3 == 1:
        col2.metric(key, value)
    else:
        col3.metric(key, value)

# Data Preview
st.subheader("📄 Data Preview")
st.dataframe(filtered_df)

# Visualization
st.subheader("📈 Data Visualization")

numeric_cols = filtered_df.select_dtypes(include='number').columns

if len(numeric_cols) >= 2:
    x_axis = st.selectbox("X-axis", numeric_cols)
    y_axis = st.selectbox("Y-axis", numeric_cols)

    fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=selected_column)
    st.plotly_chart(fig, use_container_width=True)

# Correlation Heatmap
st.subheader("🔥 Correlation Analysis")

corr = filtered_df.select_dtypes(include='number').corr()
fig_corr = px.imshow(corr, text_auto=True)
st.plotly_chart(fig_corr, use_container_width=True)
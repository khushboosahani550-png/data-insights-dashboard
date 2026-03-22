import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 My First Data Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Data Preview")
    st.dataframe(df)

    # Select columns
    numeric_cols = df.select_dtypes(include='number').columns

    if len(numeric_cols) >= 2:
        x = st.selectbox("Select X-axis", numeric_cols)
        y = st.selectbox("Select Y-axis", numeric_cols)

        fig = px.scatter(df, x=x, y=y)
        st.plotly_chart(fig)

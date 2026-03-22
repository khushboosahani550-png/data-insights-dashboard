import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)

    # Basic Cleaning
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    df.fillna(method='ffill', inplace=True)

    # Convert object columns to category where useful
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('category')

    return df
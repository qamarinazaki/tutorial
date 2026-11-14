
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Scientific Visualisation",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.header("Scientific Visualisation Dashboard", divider="gray")

st.write("""
This dashboard explores the relationship between household income,
consumer prices and marriage rates in Malaysia.

The analysis focuses on three selected years, which are 2020, 2022 and 2024.
""")

# Load merged dataset
try:
    df = pd.read_csv("merged_dataset.csv")

    # Dataset information
    total_records = len(df)
    total_states = df["state"].nunique()
    total_years = df["year"].nunique()

    # Dashboard metrics
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label="Total Records",
        value=f"{total_records:,}"
    )

    col2.metric(
        label="Total States",
        value=total_states
    )

    col3.metric(
        label="Selected Years",
        value=total_years
    )

    # Dataset preview
    st.subheader("Merged Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # Variables information
    st.subheader("Variables Used")

    variables = pd.DataFrame({
        "Variable": [
            "state",
            "year",
            "income_median",
            "cpi_index",
            "sex",
            "marriage_rate"
        ],
        "Description": [
            "State in Malaysia",
            "Selected year",
            "Median household income",
            "Consumer Price Index",
            "Male or Female",
            "Marriage rate"
        ]
    })

    st.dataframe(variables, use_container_width=True)

except Exception as e:
    st.error(f"Error loading dataset: {e}")

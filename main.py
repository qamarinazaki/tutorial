import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Visualising the Relationship Between Marriage Rates, Household Income and Consumer Prices in Malaysia",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title(
    "Visualising the Relationship Between Marriage Rates, "
    "Household Income and Consumer Prices in Malaysia"
)

st.write("""
Welcome to the Scientific Visualisation Dashboard.

This dashboard explores the relationship between household
income, consumer prices and marriage rates in Malaysia.

The analysis focuses on three selected years:
2020, 2022 and 2024.
""")

st.divider()

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")

try:
    df = load_data()

    # Dataset overview
    st.subheader("Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("States Covered", df["state"].nunique())
    col3.metric("Years Analysed", df["year"].nunique())

    st.divider()

    # Research objectives
    st.subheader("Research Objectives")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📈 Objective 1")
        st.write("Socio-Economic Trends")
        st.caption(
            "Examine trends in marriage rates, household "
            "income and consumer prices."
        )

    with col2:
        st.markdown("### 📊 Objective 2")
        st.write("Income vs Consumer Prices")
        st.caption(
            "Compare household income growth against "
            "consumer prices."
        )

    with col3:
        st.markdown("### 🔍 Objective 3")
        st.write("Marriage and Cost of Living")
        st.caption(
            "Evaluate the relationship between consumer "
            "prices and marriage rates."
        )

    st.divider()

    # Dataset preview
    st.subheader("Merged Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

except Exception as e:
    st.error(f"Error loading dataset: {e}")

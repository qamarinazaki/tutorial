
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Objective 1 | Scientific Visualisation",
    page_icon="📈",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .main-title {
        font-size: 30px;
        font-weight: 700;
        color: #2563eb;
    }
    .subtitle {
        color: #64748b;
        font-size: 15px;
    }
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 18px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<p class="main-title">📈 Objective 1: Socio-Economic Trends</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Analysis of household income, consumer prices and marriage rates in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# Objective
st.subheader("Research Objective")

st.info(
    "To examine the trends in marriage rates, household income, "
    "and consumer prices over the selected years (2020, 2022, and 2024)."
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")

try:
    df = load_data()

    # Filter selected years
    df = df[df["year"].isin([2020, 2022, 2024])].copy()

    # National-level averages
    df_trends = df.groupby("year").agg({
        "income_median": "mean",
        "cpi_index": "mean",
        "marriage_rate": "mean"
    }).reset_index()

    # Check base year
    if 2020 not in df_trends["year"].values:
        st.error("2020 data is not available.")
        st.stop()

    base_2020 = df_trends[
        df_trends["year"] == 2020
    ].iloc[0]

    # Normalize values to base year 2020 = 100
    df_trends["income_normalized"] = (
        df_trends["income_median"] /
        base_2020["income_median"]
    ) * 100

    df_trends["cpi_normalized"] = (
        df_trends["cpi_index"] /
        base_2020["cpi_index"]
    ) * 100

    df_trends["marriage_normalized"] = (
        df_trends["marriage_rate"] /
        base_2020["marriage_rate"]
    ) * 100

    # KPI Cards
    st.subheader("Key Indicators")

    col1, col2, col3 = st.columns(3)

    latest = df_trends.iloc[-1]

    col1.metric(
        "Median Household Income",
        f"RM {latest['income_median']:,.2f}"
    )

    col2.metric(
        "Consumer Price Index",
        f"{latest['cpi_index']:.2f}"
    )

    col3.metric(
        "Marriage Rate",
        f"{latest['marriage_rate']:.2f}"
    )

    st.caption(f"Latest selected year: {int(latest['year'])}")

    st.divider()

    # Chart section
    st.subheader("Trend Analysis")

    st.write(
        "The line chart compares changes in three socio-economic "
        "indicators using 2020 as the base year (2020 = 100)."
    )

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=df_trends,
        x="year",
        y="income_normalized",
        marker="o",
        linewidth=2.5,
        label="Household Income",
        ax=ax
    )

    sns.lineplot(
        data=df_trends,
        x="year",
        y="cpi_normalized",
        marker="s",
        linewidth=2.5,
        label="Consumer Price Index",
        ax=ax
    )

    sns.lineplot(
        data=df_trends,
        x="year",
        y="marriage_normalized",
        marker="^",
        linewidth=2.5,
        label="Marriage Rate",
        ax=ax
    )

    ax.set_title(
        "Trends in Socio-Economic Indicators (2020 = 100)",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Index Value (2020 = 100)", fontsize=12)

    ax.set_xticks([2020, 2022, 2024])
    ax.legend(title="Indicators", loc="best")

    sns.despine()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Note: Normalized values allow indicators with different "
        "measurement units to be compared on the same scale."
    )

    st.divider()

    # Raw data table
    st.subheader("Annual Data Summary")

    display_data = df_trends[
        ["year", "income_median", "cpi_index", "marriage_rate"]
    ].copy()

    display_data.columns = [
        "Year",
        "Median Household Income (RM)",
        "CPI Index",
        "Marriage Rate"
    ]

    st.dataframe(
        display_data.style.format({
            "Median Household Income (RM)": "{:,.2f}",
            "CPI Index": "{:.2f}",
            "Marriage Rate": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Interpretation
    st.subheader("Visualization Interpretation")

    st.write("""
    The line chart illustrates the changes in household income,
    consumer prices and marriage rates across the selected years.
    The normalized values make it easier to compare the relative
    changes in all three indicators.

    Values above 100 indicate an increase compared with 2020,
    while values below 100 indicate a decrease.
    """)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")

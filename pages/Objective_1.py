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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<p class="main-title">Objective 1: Socio-Economic Trends</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Analysis of household income, consumer prices and marriage rates in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# Research Objective
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

    # Remove duplicated economic records
    df_economic = df.drop_duplicates(
        subset=["state", "year", "income_median", "cpi_index"]
    )

    # Calculate annual averages
    df_trends = df_economic.groupby("year").agg({
        "income_median": "mean",
        "cpi_index": "mean"
    })

    # Calculate marriage rate separately
    df_marriage = df.groupby("year").agg({
        "marriage_rate": "mean"
    })

    df_trends = df_trends.join(df_marriage).reset_index()

    # Check required years
    required_years = [2020, 2022, 2024]

    if not set(required_years).issubset(set(df_trends["year"])):
        st.error("Data for 2020, 2022 and 2024 must be available.")
        st.stop()

    df_trends = df_trends.sort_values("year")

    # Normalize values to 2020 = 100
    base_2020 = df_trends[df_trends["year"] == 2020].iloc[0]

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

    # Line Chart
    st.subheader("Trend Analysis")

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(11, 6))

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
        "Socio-Economic Trends (2020 = 100)",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Index Value (2020 = 100)", fontsize=12)
    ax.set_xticks([2020, 2022, 2024])
    ax.legend(title="Indicators")

    sns.despine()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Note: All indicators are normalized to 2020 = 100 "
        "to allow comparison of their relative changes."
    )

    # Key Observation
    st.subheader("Key Observation")

    latest = df_trends[df_trends["year"] == 2024].iloc[0]

    for indicator, value in [
        ("Household Income", latest["income_normalized"]),
        ("Consumer Price Index", latest["cpi_normalized"]),
        ("Marriage Rate", latest["marriage_normalized"])
    ]:

        change = value - 100

        if change > 0:
            st.write(
                f"{indicator} increased by {change:.2f}% "
                "compared with 2020."
            )

        elif change < 0:
            st.write(
                f"{indicator} decreased by {abs(change):.2f}% "
                "compared with 2020."
            )

        else:
            st.write(
                f"{indicator} remained at the same level as 2020."
            )

except Exception as e:
    st.error(f"Error loading or processing data: {e}")

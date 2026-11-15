import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Objective 2 | Income vs CPI",
    page_icon="📊",
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
    '<p class="main-title">Objective 2: Household Income vs CPI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Comparing household income growth against consumer price increases in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# Research Objective
st.subheader("Research Objective")

st.info(
    "To compare household income growth against consumer prices "
    "to identify periods where price increases outpace income."
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")


try:
    df = load_data()

    # Filter selected years
    df = df[df["year"].isin([2020, 2022, 2024])].copy()

    # Remove duplicated economic records caused by separate sex rows
    df_economic = df.drop_duplicates(
        subset=["state", "year", "income_median", "cpi_index"]
    )

    # Calculate annual average values
    df_trends = df_economic.groupby("year").agg({
        "income_median": "mean",
        "cpi_index": "mean"
    })

    required_years = [2020, 2022, 2024]

    if not set(required_years).issubset(df_trends.index):
        st.error("Data for 2020, 2022 and 2024 must be available.")
        st.stop()

    # Calculate percentage growth
    income_growth_20_22 = (
        (df_trends.loc[2022, "income_median"] -
         df_trends.loc[2020, "income_median"])
        / df_trends.loc[2020, "income_median"]
    ) * 100

    income_growth_22_24 = (
        (df_trends.loc[2024, "income_median"] -
         df_trends.loc[2022, "income_median"])
        / df_trends.loc[2022, "income_median"]
    ) * 100

    cpi_growth_20_22 = (
        (df_trends.loc[2022, "cpi_index"] -
         df_trends.loc[2020, "cpi_index"])
        / df_trends.loc[2020, "cpi_index"]
    ) * 100

    cpi_growth_22_24 = (
        (df_trends.loc[2024, "cpi_index"] -
         df_trends.loc[2022, "cpi_index"])
        / df_trends.loc[2022, "cpi_index"]
    ) * 100

    # Prepare chart data
    growth_data = pd.DataFrame({
        "Period": [
            "2020 to 2022",
            "2022 to 2024",
            "2020 to 2022",
            "2022 to 2024"
        ],
        "Growth Rate (%)": [
            income_growth_20_22,
            income_growth_22_24,
            cpi_growth_20_22,
            cpi_growth_22_24
        ],
        "Indicator": [
            "Household Income",
            "Household Income",
            "CPI",
            "CPI"
        ]
    })

    # Grouped Bar Chart
    st.subheader("Growth Rate Comparison")

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(11, 6))

    sns.barplot(
        data=growth_data,
        x="Period",
        y="Growth Rate (%)",
        hue="Indicator",
        palette={
            "Household Income": "#3B82F6",
            "CPI": "#E85D75"
        },
        ax=ax
    )

    # Add value labels
    for container in ax.containers:
        ax.bar_label(
            container,
            fmt="%.2f%%",
            padding=4,
            fontsize=10,
            fontweight="bold"
        )

    ax.set_title(
        "Household Income vs CPI Growth Rates",
        fontsize=15,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Period", fontsize=12)
    ax.set_ylabel("Percentage Growth (%)", fontsize=12)
    ax.legend(title="Indicator")

    # Adjust axis limits
    y_min = min(0, growth_data["Growth Rate (%)"].min())
    y_max = max(0, growth_data["Growth Rate (%)"].max())
    padding = max((y_max - y_min) * 0.20, 1)

    ax.set_ylim(y_min - padding * 0.3, y_max + padding)

    sns.despine()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Key Observation
    st.subheader("Key Observation")

    for period, income_growth, cpi_growth in [
        ("2020 to 2022", income_growth_20_22, cpi_growth_20_22),
        ("2022 to 2024", income_growth_22_24, cpi_growth_22_24)
    ]:

        if cpi_growth > income_growth:
            st.write(
                f"During {period}, CPI growth ({cpi_growth:.2f}%) "
                f"was higher than household income growth "
                f"({income_growth:.2f}%). This suggests that "
                "consumer prices increased faster than household income."
            )

        elif income_growth > cpi_growth:
            st.write(
                f"During {period}, household income growth "
                f"({income_growth:.2f}%) was higher than CPI growth "
                f"({cpi_growth:.2f}%). This suggests that household "
                "income increased faster than consumer prices."
            )

        else:
            st.write(
                f"During {period}, household income and CPI recorded "
                "the same percentage growth."
            )

    st.caption(
        "Note: Growth rates are calculated using average annual values. "
        "A higher CPI growth rate indicates that consumer prices increased "
        "faster than household income."
    )

except Exception as e:
    st.error(f"Error loading or processing data: {e}")

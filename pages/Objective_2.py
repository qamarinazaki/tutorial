import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Objective 2 | Income vs CPI",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

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

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<p class="main-title">📊 Objective 2: Household Income vs CPI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Comparing household income growth against consumer price increases in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# RESEARCH OBJECTIVE
# ==========================================

st.subheader("Research Objective")

st.info(
    "To compare household income growth against consumer prices "
    "to identify periods where price increases outpace income."
)

# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")


try:

    df = load_data()

    # Filter selected years
    df = df[df["year"].isin([2020, 2022, 2024])].copy()

    # Aggregate annual values
    df_trends = df.groupby("year").agg({
        "income_median": "mean",
        "cpi_index": "mean"
    }).reset_index()

    # Check required years
    required_years = [2020, 2022, 2024]

    if not set(required_years).issubset(set(df_trends["year"])):
        st.error("Data for 2020, 2022 and 2024 must be available.")
        st.stop()

    # Arrange values by year
    df_trends = df_trends.set_index("year").sort_index()

    val_2020 = df_trends.loc[2020]
    val_2022 = df_trends.loc[2022]
    val_2024 = df_trends.loc[2024]

    # ==========================================
    # CALCULATE GROWTH RATES
    # ==========================================

    income_growth_20_22 = (
        (val_2022["income_median"] - val_2020["income_median"])
        / val_2020["income_median"]
    ) * 100

    income_growth_22_24 = (
        (val_2024["income_median"] - val_2022["income_median"])
        / val_2022["income_median"]
    ) * 100

    cpi_growth_20_22 = (
        (val_2022["cpi_index"] - val_2020["cpi_index"])
        / val_2020["cpi_index"]
    ) * 100

    cpi_growth_22_24 = (
        (val_2024["cpi_index"] - val_2022["cpi_index"])
        / val_2022["cpi_index"]
    ) * 100

    # ==========================================
    # PREPARE CHART DATA
    # ==========================================

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

    # ==========================================
    # KEY INDICATORS
    # ==========================================

    st.subheader("Growth Rate Overview")

    col1, col2 = st.columns(2)

    col1.metric(
        "Household Income Growth (2020 to 2022)",
        f"{income_growth_20_22:.2f}%"
    )

    col2.metric(
        "CPI Growth (2020 to 2022)",
        f"{cpi_growth_20_22:.2f}%"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Household Income Growth (2022 to 2024)",
        f"{income_growth_22_24:.2f}%"
    )

    col4.metric(
        "CPI Growth (2022 to 2024)",
        f"{cpi_growth_22_24:.2f}%"
    )

    st.divider()

    # ==========================================
    # GROUPED BAR CHART
    # ==========================================

    st.subheader("Growth Rate Comparison")

    st.write("""
    This grouped bar chart compares the percentage growth
    of household income and Consumer Price Index (CPI)
    across the two selected periods.
    """)

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

    # Chart styling
    ax.set_title(
        "Comparison of Household Income and CPI Growth Rates",
        fontsize=15,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel("Period", fontsize=12)
    ax.set_ylabel("Percentage Growth (%)", fontsize=12)

    ax.legend(
        title="Indicators",
        fontsize=10,
        title_fontsize=11
    )

    # Dynamic axis limits, including negative values
    y_min = min(0, growth_data["Growth Rate (%)"].min())
    y_max = max(0, growth_data["Growth Rate (%)"].max())

    padding = max((y_max - y_min) * 0.20, 1)

    ax.set_ylim(y_min - padding * 0.3, y_max + padding)

    sns.despine()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Note: Growth rates are calculated based on the average "
        "annual values for the selected years."
    )

    st.divider()

    # ==========================================
    # GROWTH DATA TABLE
    # ==========================================

    st.subheader("Growth Rate Data")

    st.dataframe(
        growth_data.pivot(
            index="Period",
            columns="Indicator",
            values="Growth Rate (%)"
        ).style.format("{:.2f}%"),
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # VISUALIZATION INTERPRETATION
    # ==========================================

    st.subheader("Visualization Interpretation")

    for period, income_growth, cpi_growth in [
        ("2020 to 2022", income_growth_20_22, cpi_growth_20_22),
        ("2022 to 2024", income_growth_22_24, cpi_growth_22_24)
    ]:

        st.markdown(f"**{period}**")

        if cpi_growth > income_growth:
            st.write(
                f"CPI growth ({cpi_growth:.2f}%) was higher than "
                f"household income growth ({income_growth:.2f}%). "
                "This indicates that consumer prices increased "
                "faster than household income during this period."
            )

        elif income_growth > cpi_growth:
            st.write(
                f"Household income growth ({income_growth:.2f}%) "
                f"was higher than CPI growth ({cpi_growth:.2f}%). "
                "This indicates that household income increased "
                "faster than consumer prices during this period."
            )

        else:
            st.write(
                "Household income and CPI recorded the same "
                "percentage growth during this period."
            )

except Exception as e:

    st.error(f"Error loading or processing data: {e}")

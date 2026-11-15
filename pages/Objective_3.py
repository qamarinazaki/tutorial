import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Objective 3 | CPI and Marriage Rates",
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
    '<p class="main-title">Objective 3: CPI and Marriage Rates</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Exploring the relationship between consumer prices and marriage rates in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# Research Objective
st.subheader("Research Objective")

st.info(
    "To evaluate the impact of rising consumer prices and "
    "the increasing cost of living on marriage decisions."
)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")


try:
    df = load_data()

    # Filter selected years
    df = df[
        df["year"].isin([2020, 2022, 2024])
    ].copy()

    # Remove missing values
    df = df.dropna(
        subset=["state", "year", "cpi_index", "marriage_rate"]
    )

    # Get unique economic records
    economic_data = df[
        ["state", "year", "cpi_index"]
    ].drop_duplicates(
        subset=["state", "year"]
    )

    # Calculate average marriage rate for Male and Female
    marriage_data = (
        df.groupby(
            ["state", "year"],
            as_index=False
        )["marriage_rate"]
        .mean()
    )

    # Merge economic and marriage data
    scatter_data = pd.merge(
        economic_data,
        marriage_data,
        on=["state", "year"],
        how="inner"
    )

    scatter_data = scatter_data.dropna(
        subset=["cpi_index", "marriage_rate"]
    )

    scatter_data["year_str"] = scatter_data["year"].astype(str)

    if scatter_data.empty:
        st.warning("No data available for the selected years.")

    else:

        # ==================================
        # SUMMARY BOX
        # ==================================

        st.subheader("Summary Box")

        average_cpi = scatter_data["cpi_index"].mean()
        average_marriage = scatter_data["marriage_rate"].mean()

        correlation = scatter_data[
            ["cpi_index", "marriage_rate"]
        ].corr(method="pearson").iloc[0, 1]

        # Determine relationship
        if pd.isna(correlation):
            relationship = "Insufficient Data"
        elif correlation > 0:
            relationship = "Positive"
        elif correlation < 0:
            relationship = "Negative"
        else:
            relationship = "No Linear Relationship"

        # Display summary metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average CPI",
            f"{average_cpi:.2f}"
        )

        col2.metric(
            "Average Marriage Rate",
            f"{average_marriage:.2f}"
        )

        col3.metric(
            "Pearson Correlation",
            f"{correlation:.2f}" if pd.notna(correlation) else "N/A"
        )

        # Key Insight
        st.info(
            f"**Key Insight:** The relationship between CPI and "
            f"marriage rates is {relationship.lower()}, based on "
            f"the Pearson correlation."
        )

        st.divider()

        # ==================================
        # SCATTER PLOT
        # ==================================

        st.subheader("Relationship Between CPI and Marriage Rates")

        sns.set_theme(style="whitegrid")

        fig, ax = plt.subplots(figsize=(11, 6))

        sns.scatterplot(
            data=scatter_data,
            x="cpi_index",
            y="marriage_rate",
            hue="year_str",
            hue_order=["2020", "2022", "2024"],
            palette={
                "2020": "#3B82F6",
                "2022": "#F59E0B",
                "2024": "#16A085"
            },
            s=100,
            alpha=0.8,
            edgecolor="white",
            linewidth=0.8,
            ax=ax
        )

        # Overall trendline
        x_vals = scatter_data["cpi_index"]
        y_vals = scatter_data["marriage_rate"]

        if len(scatter_data) >= 2 and x_vals.nunique() >= 2:
            m, c = np.polyfit(x_vals, y_vals, 1)

            x_range = np.linspace(
                x_vals.min(),
                x_vals.max(),
                100
            )

            ax.plot(
                x_range,
                m * x_range + c,
                color="black",
                linestyle="--",
                linewidth=2,
                label="Trendline"
            )

        # Chart formatting
        ax.set_title(
            "CPI vs Marriage Rates (2020, 2022, 2024)",
            fontsize=15,
            fontweight="bold",
            pad=15
        )

        ax.set_xlabel(
            "Consumer Price Index (CPI)",
            fontsize=12
        )

        ax.set_ylabel(
            "Marriage Rate",
            fontsize=12
        )

        ax.legend(title="Year")
        sns.despine()

        fig.tight_layout()

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # ==================================
        # INTERPRETATION
        # ==================================

        st.subheader("Key Observation")

        if pd.isna(correlation):
            st.write(
                "There is insufficient variation in the data "
                "to calculate a Pearson correlation."
            )

        elif correlation > 0:
            st.write(
                f"The chart indicates a positive relationship "
                f"between CPI and marriage rates, with a "
                f"Pearson correlation of {correlation:.2f}."
            )

        elif correlation < 0:
            st.write(
                f"The chart indicates a negative relationship "
                f"between CPI and marriage rates, with a "
                f"Pearson correlation of {correlation:.2f}."
            )

        else:
            st.write(
                "The chart indicates no linear relationship "
                "between CPI and marriage rates."
            )

        st.caption(
            "Note: Correlation indicates an association and "
            "does not prove causation."
        )

except Exception as e:
    st.error(f"Error loading dataset: {e}")

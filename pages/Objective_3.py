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

# Research objective
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
    scatter_data = df[
        df["year"].isin([2020, 2022, 2024])
    ].dropna(
        subset=["cpi_index", "marriage_rate"]
    ).copy()

    scatter_data["year_str"] = scatter_data["year"].astype(str)

    # Scatter plot
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

    ax.set_xlabel("Consumer Price Index (CPI)", fontsize=12)
    ax.set_ylabel("Marriage Rate", fontsize=12)

    ax.legend(title="Year")
    sns.despine()

    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    # Short interpretation
    correlation = scatter_data[
        ["cpi_index", "marriage_rate"]
    ].corr(method="pearson").iloc[0, 1]

    st.subheader("Key Observation")

    if pd.isna(correlation):
        st.write("There is insufficient variation in the data to calculate a correlation.")
    elif correlation > 0:
        st.write(
            f"The chart indicates a positive relationship between CPI "
            f"and marriage rates, with a Pearson correlation of {correlation:.2f}."
        )
    elif correlation < 0:
        st.write(
            f"The chart indicates a negative relationship between CPI "
            f"and marriage rates, with a Pearson correlation of {correlation:.2f}."
        )
    else:
        st.write(
            "The chart indicates no linear relationship between CPI and marriage rates."
        )

    st.caption(
        "Note: Correlation indicates an association and does not prove causation."
    )

except Exception as e:
    st.error(f"Error loading dataset: {e}")

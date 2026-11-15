import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Objective 3 | CPI and Marriage Rates",
    page_icon="🔍",
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
    '<p class="main-title">🔍 Objective 3: CPI and Marriage Rates</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Exploring the relationship between consumer prices and marriage rates in Malaysia</p>',
    unsafe_allow_html=True
)

st.divider()

# ==========================================
# RESEARCH OBJECTIVE
# ==========================================

st.subheader("Research Objective")

st.info(
    "To evaluate the impact of rising consumer prices and "
    "the increasing cost of living on marriage decisions."
)

# ==========================================
# LOAD DATASET
# ==========================================

@st.cache_data
def load_data():
    return pd.read_csv("merged_dataset.csv")


try:

    df = load_data()

    # Filter selected years and required columns
    scatter_data = df[
        df["year"].isin([2020, 2022, 2024])
    ].dropna(
        subset=["cpi_index", "marriage_rate"]
    ).copy()

    # Convert year to string
    scatter_data["year_str"] = (
        scatter_data["year"].astype(str)
    )

    # ==========================================
    # KPI CARDS
    # ==========================================

    st.subheader("Data Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Observations",
        f"{len(scatter_data):,}"
    )

    col2.metric(
        "Average CPI",
        f"{scatter_data['cpi_index'].mean():.2f}"
    )

    col3.metric(
        "Average Marriage Rate",
        f"{scatter_data['marriage_rate'].mean():.2f}"
    )

    st.divider()

    # ==========================================
    # SCATTER PLOT
    # ==========================================

    st.subheader("Relationship Analysis")

    st.write("""
    This scatter plot examines the relationship between
    Consumer Price Index (CPI) and marriage rates across
    Malaysian states in 2020, 2022 and 2024.
    """)

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Scatter points
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

    # Regression trendline
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
            color="#263238",
            linestyle="--",
            linewidth=2,
            label="Overall Trendline"
        )

    # Chart formatting
    ax.set_title(
        "Relationship Between CPI and Marriage Rates",
        fontsize=15,
        fontweight="bold",
        pad=18
    )

    ax.set_xlabel(
        "Consumer Price Index (CPI)",
        fontsize=12
    )

    ax.set_ylabel(
        "Marriage Rate",
        fontsize=12
    )

    ax.legend(
        title="Year",
        fontsize=10,
        title_fontsize=11,
        loc="best"
    )

    sns.despine()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Each point represents a state and year. "
        "The dashed line represents the overall linear trend."
    )

    st.divider()

    # ==========================================
    # CORRELATION RESULT
    # ==========================================

    st.subheader("Correlation Analysis")

    correlation = scatter_data[
        ["cpi_index", "marriage_rate"]
    ].corr(method="pearson").iloc[0, 1]

    col1, col2 = st.columns(2)

    col1.metric(
        "Pearson Correlation",
        f"{correlation:.3f}"
    )

    if correlation > 0:
        relationship = "Positive"
        strength_value = abs(correlation)
    elif correlation < 0:
        relationship = "Negative"
        strength_value = abs(correlation)
    else:
        relationship = "No linear correlation"
        strength_value = 0

    col2.metric(
        "Relationship Direction",
        relationship
    )

    st.write(
        f"The Pearson correlation coefficient is {correlation:.3f}. "
        f"This indicates a {relationship.lower()} linear association "
        "between CPI and marriage rates."
    )

    st.divider()

    # ==========================================
    # DATA PREVIEW
    # ==========================================

    st.subheader("Scatter Plot Data")

    st.dataframe(
        scatter_data[
            ["state", "year", "cpi_index", "marriage_rate"]
        ].sort_values(["year", "state"]),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # INTERPRETATION
    # ==========================================

    st.subheader("Visualization Interpretation")

    if correlation >= 0.7:
        strength = "strong positive"
    elif correlation >= 0.3:
        strength = "moderate positive"
    elif correlation > 0:
        strength = "weak positive"
    elif correlation <= -0.7:
        strength = "strong negative"
    elif correlation <= -0.3:
        strength = "moderate negative"
    elif correlation < 0:
        strength = "weak negative"
    else:
        strength = "no linear"

    st.write(
        f"The scatter plot shows a {strength} relationship "
        "between consumer prices and marriage rates based "
        "on the Pearson correlation result."
    )

    st.write("""
    The overall trendline helps illustrate the direction
    of the relationship. However, correlation does not
    establish that rising consumer prices directly cause
    changes in marriage decisions.
    """)

except Exception as e:

    st.error(f"Error loading or processing data: {e}")

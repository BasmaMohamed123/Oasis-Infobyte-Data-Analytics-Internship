
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🛍️",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"

st.title("🛍️ Customer Segmentation Dashboard")
st.markdown(
    "Explore customer behavior, RFM metrics, and K-Means segmentation results."
)

@st.cache_data
def load_data():
    customers = pd.read_csv(OUTPUTS_DIR / "customer_segments.csv")
    summary = pd.read_csv(OUTPUTS_DIR / "cluster_summary.csv")
    return customers, summary

try:
    customers, summary = load_data()
except Exception as e:
    st.error(f"Could not load project data: {e}")
    st.stop()

st.sidebar.header("Dashboard Filters")

segment_options = sorted(customers["Cluster"].unique())
selected_segments = st.sidebar.multiselect(
    "Select Customer Segments",
    options=segment_options,
    default=segment_options
)

filtered = customers[customers["Cluster"].isin(selected_segments)]

if filtered.empty:
    st.warning("Please select at least one customer segment.")
    st.stop()

total_customers = len(filtered)
total_revenue = filtered["Monetary"].sum()
avg_recency = filtered["Recency"].mean()
avg_frequency = filtered["Frequency"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Revenue", f"£{total_revenue:,.2f}")
col3.metric("Average Recency", f"{avg_recency:.1f} days")
col4.metric("Average Frequency", f"{avg_frequency:.2f}")

st.divider()

st.subheader("Customer Segment Distribution")

segment_counts = (
    filtered["Cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)
segment_counts.columns = ["Cluster", "Customers"]

fig_segments = px.pie(
    segment_counts,
    names="Cluster",
    values="Customers",
    hole=0.45,
    title="Customers by Segment"
)
st.plotly_chart(fig_segments, use_container_width=True)

st.subheader("RFM Analysis")

rfm_col1, rfm_col2 = st.columns(2)

with rfm_col1:
    fig_frequency = px.box(
        filtered,
        x="Cluster",
        y="Frequency",
        color="Cluster",
        title="Purchase Frequency by Segment"
    )
    st.plotly_chart(fig_frequency, use_container_width=True)

with rfm_col2:
    fig_monetary = px.box(
        filtered,
        x="Cluster",
        y="Monetary",
        color="Cluster",
        title="Monetary Value by Segment"
    )
    st.plotly_chart(fig_monetary, use_container_width=True)

fig_recency = px.box(
    filtered,
    x="Cluster",
    y="Recency",
    color="Cluster",
    title="Recency by Segment"
)
st.plotly_chart(fig_recency, use_container_width=True)

st.divider()

st.subheader("Customer Segments Comparison")

st.dataframe(summary, use_container_width=True)

st.subheader("Customer Records")

st.dataframe(
    filtered.head(100),
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Data source: UCI Online Retail Dataset | "
    "Segmentation method: RFM Analysis and K-Means Clustering"
)

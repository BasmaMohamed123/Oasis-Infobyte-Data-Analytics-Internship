
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================
# Dashboard Color Palette
# =========================

NAVY = "#243B5A"
TEAL = "#2A9D8F"
BLUE = "#5B8DB8"
LIGHT_BLUE = "#A8C5D8"
PALE = "#E8F0F4"
WHITE = "#FFFFFF"

CATEGORY_COLORS = {
    "Electronics": NAVY,
    "Clothing": TEAL,
    "Home & Kitchen": BLUE,
    "Sports": LIGHT_BLUE,
    "Beauty": "#6C8F83",
    "Toys": "#D9A441",
    "Books": "#8C9AA8",
}

GENDER_COLORS = {
    "Female": TEAL,
    "Male": NAVY,
    "Other": LIGHT_BLUE,
}

CHANNEL_COLORS = {
    "Mobile App": TEAL,
    "Physical Store": NAVY,
    "Website": BLUE,
}

# =========================
# 1. Page Configuration
# =========================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# 2. Custom Styling
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FA;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    color: #172B4D;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background-color: #172B4D;
    min-width: 310px;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

section[data-testid="stSidebar"] label {
    color: #E6EDF7 !important;
    font-size: 15px;
    font-weight: 600;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] {
    background-color: #FFFFFF;
    border-radius: 8px;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #172B4D;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #2A9D8F !important;
    border-color: #2A9D8F !important;
}

section[data-testid="stSidebar"] span[data-baseweb="tag"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] [role="option"] {
    background-color: #FFFFFF !important;
    color: #172B4D !important;
}

section[data-testid="stSidebar"] [role="option"] * {
    color: #172B4D !important;
}

section[data-testid="stSidebar"] [role="option"][aria-selected="true"] {
    background-color: #E8F0FC !important;
    color: #172B4D !important;
}

section[data-testid="stSidebar"] input[type="checkbox"] {
    accent-color: #2A9D8F !important;
}

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E1E7EF;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 3px 8px rgba(23,43,77,0.06);
    min-height: 125px;
}

div[data-testid="stMetricLabel"] {
    font-size: 15px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #172B4D !important;
}

div[data-testid="stTabs"] {
    background-color: #FFFFFF;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #E1E7EF;
    margin-top: 15px;
    margin-bottom: 20px;
}

div[data-testid="stTabs"] button {
    font-size: 20px !important;
    font-weight: 700 !important;
    padding: 16px 26px !important;
    min-height: 60px !important;
    color: #44546A;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2A9D8F !important;
    border-bottom: 3px solid #2A9D8F;
}

div[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border: 1px solid #E1E7EF;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 15px;
}

div[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #E1E7EF;
    border-radius: 12px;
    padding: 8px;
}

div[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #E1E7EF;
    border-radius: 12px;
}

hr {
    border-color: #E1E7EF;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 3. Load Dataset
# =========================

@st.cache_data
def load_data():

    project_path = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "retail_sales_dataset.csv"
)

    data = pd.read_csv(project_path)

    data["order_date"] = pd.to_datetime(data["order_date"])

    data["year"] = data["order_date"].dt.year
    data["month"] = data["order_date"].dt.month
    data["quarter"] = data["order_date"].dt.to_period("Q").astype(str)

    data["age_group"] = pd.cut(
        data["customer_age"],
        bins=[17, 25, 35, 45, 55, 65, 100],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
    )

    return data


df = load_data()

# =========================
# 4. Sidebar Filters
# =========================

st.sidebar.title("📊 Dashboard Filters")

st.sidebar.caption(
    "Customize the dashboard using the filters below."
)

years = sorted(df["year"].unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

regions = sorted(df["region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    regions,
    default=regions
)

categories = sorted(df["product_category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    categories,
    default=categories
)

st.sidebar.divider()

st.sidebar.caption(
    "Data Source: Retail Sales Dataset"
)

# =========================
# 5. Apply Filters
# =========================

filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["region"].isin(selected_regions)) &
    (df["product_category"].isin(selected_categories))
]

# =========================
# 6. Dashboard Header
# =========================

st.html("""
<div style="
    background: linear-gradient(120deg, #243B5A, #2A9D8F);
    padding: 32px 35px;
    border-radius: 16px;
    margin-bottom: 25px;
">
    <div style="
        color: #BBD3F5;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 2px;
    ">
        OASIS INFOBYTE | DATA ANALYTICS
    </div>

    <h1 style="
        color: white;
        font-size: 34px;
        margin: 12px 0 8px 0;
    ">
        Retail Sales Dashboard
    </h1>

    <p style="
        color: #E0EAF8;
        font-size: 16px;
        margin: 0;
    ">
        Explore sales performance, customer behavior,
        product trends and business profitability.
    </p>
</div>
""")

# =========================
# 7. KPI Calculations
# =========================

total_sales = filtered_df["total_amount"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
total_customers = filtered_df["customer_id"].nunique()

# =========================
# 8. KPI Cards
# =========================

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"{total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"{total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Total Customers",
    f"{total_customers:,}"
)

st.divider()

# =========================
# 9. Dashboard Tabs
# =========================

tab_overview, tab_sales, tab_customers, tab_products, tab_profit, tab_recommendations = st.tabs(
    [
        "Overview",
        "Sales",
        "Customers",
        "Products",
        "Profitability",
        "Recommendations"
    ]
)

# =========================
# 10. Overview Tab
# =========================

with tab_overview:

    st.header("Dashboard Overview")

    st.markdown(
        "A summary of the selected retail sales data."
    )

    if filtered_df.empty:

        st.warning(
            "No data available for the selected filters. "
            "Please adjust your filters."
        )

    else:

        col1, col2 = st.columns(2)

        # Sales by Year
        yearly_sales = (
            filtered_df.groupby("year")
            .agg(
                Total_Sales=("total_amount", "sum"),
                Total_Orders=("order_id", "nunique")
            )
            .reset_index()
        )

        fig_yearly = px.bar(
            yearly_sales,
            x="year",
            y="Total_Sales",
            text_auto=".2s",
            title="Sales by Year",
            template="plotly_white"
        )

        fig_yearly.update_traces(
            marker_color=NAVY
        )

        fig_yearly.update_layout(
            xaxis_title="Year",
            yaxis_title="Total Sales",
            showlegend=False
        )

        col1.plotly_chart(
            fig_yearly,
            use_container_width=True
        )

        # Sales by Region
        region_sales = (
            filtered_df.groupby("region")
            .agg(
                Total_Sales=("total_amount", "sum")
            )
            .reset_index()
            .sort_values("Total_Sales", ascending=False)
        )

        fig_region = px.bar(
            region_sales,
            x="region",
            y="Total_Sales",
            text_auto=".2s",
            title="Sales by Region",
            template="plotly_white"
        )

        fig_region.update_traces(
            marker_color=TEAL
        )

        fig_region.update_layout(
            xaxis_title="Region",
            yaxis_title="Total Sales",
            showlegend=False
        )

        col2.plotly_chart(
            fig_region,
            use_container_width=True
        )

        # Overview Insights
        best_region = region_sales.iloc[0]

        st.info(
            f"**Overview Insight:** {best_region['region']} "
            f"generated the highest sales among the selected regions, "
            f"with total sales of {best_region['Total_Sales']:,.2f}."
        )

    st.divider()

    st.caption(
        "Note: Total Sales represents the dataset's total_amount "
        "field, which includes shipping costs."
    )

# =========================
# 11. Sales Tab
# =========================

with tab_sales:

    st.header("Sales Performance")

    if filtered_df.empty:

        st.warning("No data available for the selected filters.")

    else:

        # Monthly Sales
        monthly_sales = (
            filtered_df.groupby(
                filtered_df["order_date"].dt.to_period("M")
            )
            .agg(
                Total_Sales=("total_amount", "sum"),
                Total_Orders=("order_id", "nunique")
            )
            .reset_index()
        )

        monthly_sales["Month"] = (
            monthly_sales["order_date"].dt.to_timestamp()
        )

        fig_monthly = px.line(
            monthly_sales,
            x="Month",
            y="Total_Sales",
            markers=True,
            title="Monthly Sales Trend",
            hover_data=["Total_Orders"],
            template="plotly_white"
        )

        fig_monthly.update_traces(
            line_color=NAVY,
            line_width=3,
            marker_color=TEAL,
            marker_size=7
        )

        fig_monthly.update_layout(
            xaxis_title="Month",
            yaxis_title="Total Sales",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

        # Quarterly Sales
        quarterly_sales = (
            filtered_df.groupby("quarter")
            .agg(
                Total_Sales=("total_amount", "sum"),
                Total_Orders=("order_id", "nunique")
            )
            .reset_index()
        )

        fig_quarterly = px.bar(
            quarterly_sales,
            x="quarter",
            y="Total_Sales",
            text_auto=".2s",
            title="Quarterly Sales Trend",
            template="plotly_white"
        )

        fig_quarterly.update_traces(
            marker_color=TEAL
        )

        fig_quarterly.update_layout(
            xaxis_title="Quarter",
            yaxis_title="Total Sales"
        )

        st.plotly_chart(
            fig_quarterly,
            use_container_width=True
        )

        # Sales Insight
        best_month = monthly_sales.loc[
            monthly_sales["Total_Sales"].idxmax()
        ]

        st.info(
            f"**Key Insight:** The highest sales month was "
            f"{best_month['Month'].strftime('%B %Y')}, "
            f"with total sales of "
            f"{best_month['Total_Sales']:,.2f}."
        )

# =========================
# 12. Customers Tab
# =========================

with tab_customers:

    st.header("Customer Insights")

    if filtered_df.empty:

        st.warning("No data available for the selected filters.")

    else:

        col1, col2 = st.columns(2)

        # Orders by Age Group
        age_analysis = (
            filtered_df.groupby("age_group", observed=False)
            .agg(
                Total_Orders=("order_id", "nunique"),
                Total_Sales=("total_amount", "sum")
            )
            .reset_index()
        )

        fig_age = px.bar(
            age_analysis,
            x="age_group",
            y="Total_Orders",
            title="Orders by Customer Age Group",
            text_auto=True,
            template="plotly_white"
        )

        fig_age.update_traces(
            marker_color=TEAL
        )

        fig_age.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Number of Orders",
            showlegend=False
        )

        col1.plotly_chart(
            fig_age,
            use_container_width=True
        )

        # Sales by Gender
        gender_analysis = (
            filtered_df.groupby("gender")
            .agg(
                Total_Orders=("order_id", "nunique"),
                Total_Sales=("total_amount", "sum"),
                Average_Sales=("total_amount", "mean")
            )
            .reset_index()
        )

        fig_gender = px.bar(
            gender_analysis,
            x="gender",
            y="Total_Sales",
            color="gender",
            color_discrete_map=GENDER_COLORS,
            title="Total Sales by Gender",
            text_auto=".2s",
            template="plotly_white"
        )

        fig_gender.update_layout(
            xaxis_title="Gender",
            yaxis_title="Total Sales",
            showlegend=False
        )

        col2.plotly_chart(
            fig_gender,
            use_container_width=True
        )

        # Orders by Gender
        fig_gender_orders = px.pie(
            gender_analysis,
            names="gender",
            values="Total_Orders",
            title="Order Distribution by Gender",
            hole=0.5,
            color="gender",
            color_discrete_map=GENDER_COLORS,
            template="plotly_white"
        )

        st.plotly_chart(
            fig_gender_orders,
            use_container_width=True
        )

        # Customer Insights
        if not age_analysis.empty and not gender_analysis.empty:

            top_age = age_analysis.loc[
                age_analysis["Total_Orders"].idxmax()
            ]

            top_gender = gender_analysis.loc[
                gender_analysis["Total_Sales"].idxmax()
            ]

            st.info(
                f"**Customer Insights:** The {top_age['age_group']} "
                f"age group generated the highest number of orders "
                f"({top_age['Total_Orders']:,}). "
                f"{top_gender['gender']} customers generated the "
                f"highest total sales "
                f"({top_gender['Total_Sales']:,.2f})."
            )

# =========================
# 13. Products Tab
# =========================

with tab_products:

    st.header("Product Performance")

    if filtered_df.empty:

        st.warning("No data available for the selected filters.")

    else:

        col1, col2 = st.columns(2)

        # Top 10 Best-Selling Products
        top_products = (
            filtered_df.groupby("product_name")
            .agg(
                Total_Quantity=("quantity", "sum"),
                Total_Revenue=("total_amount", "sum")
            )
            .sort_values("Total_Quantity", ascending=False)
            .head(10)
            .reset_index()
        )

        fig_products = px.bar(
            top_products.sort_values("Total_Quantity"),
            x="Total_Quantity",
            y="product_name",
            orientation="h",
            title="Top 10 Best-Selling Products",
            text_auto=True,
            template="plotly_white"
        )

        fig_products.update_traces(
            marker_color=TEAL
        )

        fig_products.update_layout(
            xaxis_title="Units Sold",
            yaxis_title="Product",
            showlegend=False
        )

        col1.plotly_chart(
            fig_products,
            use_container_width=True
        )

        # Revenue by Product Category
        category_analysis = (
            filtered_df.groupby("product_category")
            .agg(
                Total_Quantity=("quantity", "sum"),
                Total_Sales=("total_amount", "sum"),
                Total_Profit=("profit", "sum")
            )
            .reset_index()
        )

        fig_category = px.pie(
            category_analysis,
            names="product_category",
            values="Total_Sales",
            title="Revenue Share by Product Category",
            hole=0.5,
            color="product_category",
            color_discrete_map=CATEGORY_COLORS,
            template="plotly_white"
        )

        col2.plotly_chart(
            fig_category,
            use_container_width=True
        )

        # Profit Margin by Category
        category_analysis["Profit_Margin"] = (
            category_analysis["Total_Profit"]
            / category_analysis["Total_Sales"] * 100
        )

        margin_data = category_analysis.sort_values(
            "Profit_Margin"
        )

        fig_margin = px.bar(
            margin_data,
            x="Profit_Margin",
            y="product_category",
            orientation="h",
            title="Profit Margin by Product Category",
            text=margin_data["Profit_Margin"].round(2).astype(str) + "%",
            template="plotly_white"
        )

        fig_margin.update_traces(
            marker_color=TEAL
        )

        fig_margin.update_layout(
            xaxis_title="Profit Margin (%)",
            yaxis_title="Product Category",
            showlegend=False
        )

        st.plotly_chart(
            fig_margin,
            use_container_width=True
        )

        # Product Insights
        if not top_products.empty and not category_analysis.empty:

            best_product = top_products.iloc[0]

            top_revenue_category = category_analysis.loc[
                category_analysis["Total_Sales"].idxmax()
            ]

            top_margin_category = category_analysis.loc[
                category_analysis["Profit_Margin"].idxmax()
            ]

            st.info(
                f"**Product Insights:** {best_product['product_name']} "
                f"was the best-selling product with "
                f"{best_product['Total_Quantity']:,} units sold. "
                f"{top_revenue_category['product_category']} generated "
                f"the highest revenue, while "
                f"{top_margin_category['product_category']} achieved "
                f"the highest profit margin."
            )

# =========================
# 14. Profitability Tab
# =========================

with tab_profit:

    st.header("Profitability & Sales Channels")

    if filtered_df.empty:

        st.warning("No data available for the selected filters.")

    else:

        col1, col2 = st.columns(2)

        # Profit by Order Channel
        channel_analysis = (
            filtered_df.groupby("order_channel")
            .agg(
                Total_Orders=("order_id", "nunique"),
                Total_Profit=("profit", "sum"),
                Average_Profit=("profit", "mean")
            )
            .reset_index()
        )

        fig_channel_profit = px.bar(
            channel_analysis,
            x="order_channel",
            y="Total_Profit",
            color="order_channel",
            color_discrete_map=CHANNEL_COLORS,
            text_auto=".2s",
            title="Total Profit by Order Channel",
            template="plotly_white"
        )

        fig_channel_profit.update_layout(
            xaxis_title="Order Channel",
            yaxis_title="Total Profit",
            showlegend=False
        )

        col1.plotly_chart(
            fig_channel_profit,
            use_container_width=True
        )

        # Average Profit by Channel
        fig_average_profit = px.bar(
            channel_analysis,
            x="order_channel",
            y="Average_Profit",
            color="order_channel",
            color_discrete_map=CHANNEL_COLORS,
            text_auto=".2f",
            title="Average Profit per Order by Channel",
            template="plotly_white"
        )

        fig_average_profit.update_layout(
            xaxis_title="Order Channel",
            yaxis_title="Average Profit",
            showlegend=False
        )

        col2.plotly_chart(
            fig_average_profit,
            use_container_width=True
        )

        # Correlation Heatmap
        st.subheader("Correlation Analysis")

        correlation_columns = [
            "customer_age",
            "unit_price",
            "quantity",
            "discount_pct",
            "shipping_cost",
            "delivery_days",
            "customer_rating",
            "total_amount",
            "profit"
        ]

        numeric_data = filtered_df[
            correlation_columns
        ]

        correlation_matrix = numeric_data.corr()

        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=".2f",
            color_continuous_scale=[
                [0, NAVY],
                [0.5, "#F5F7FA"],
                [1, TEAL]
            ],
            zmin=-1,
            zmax=1,
            title="Correlation Heatmap",
            aspect="auto"
        )

        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )

        # Profitability Insights
        if not channel_analysis.empty:

            best_channel = channel_analysis.loc[
                channel_analysis["Total_Profit"].idxmax()
            ]

            best_average_channel = channel_analysis.loc[
                channel_analysis["Average_Profit"].idxmax()
            ]

            st.info(
                f"**Profitability Insights:** "
                f"{best_channel['order_channel']} generated the "
                f"highest total profit "
                f"({best_channel['Total_Profit']:,.2f}), while "
                f"{best_average_channel['order_channel']} achieved "
                f"the highest average profit per order "
                f"({best_average_channel['Average_Profit']:.2f})."
            )

# =========================
# 15. Recommendations Tab
# =========================

with tab_recommendations:

    st.header("Business Recommendations")

    st.markdown(
        """
        The following recommendations are based on the overall
        dataset analysis and aim to improve business performance.
        """
    )

    st.divider()

    # Recommendation 1
    st.subheader("1. Improve Electronics Profitability")

    st.write(
        "Electronics generated the highest revenue share (45.37%), "
        "but had the lowest profit margin (17.93%). "
        "The business should review supplier costs, pricing strategies, "
        "and discount policies to improve profitability."
    )

    st.divider()

    # Recommendation 2
    st.subheader("2. Focus on High-Margin Categories")

    st.write(
        "Beauty and Clothing achieved the highest profit margins "
        "(50.79% and 46.88%, respectively). "
        "Consider investing in targeted promotions and inventory "
        "for these categories while monitoring demand."
    )

    st.divider()

    # Recommendation 3
    st.subheader("3. Strengthen the Mobile App Channel")

    st.write(
        "The Mobile App generated the highest number of orders "
        "and the highest total profit among the sales channels. "
        "Improving the app experience and running targeted marketing "
        "campaigns may help maintain customer engagement and growth."
    )

    st.divider()

    st.success(
        "These recommendations are based on patterns observed "
        "in the complete dataset."
    )

# =========================
# 16. Footer
# =========================

st.divider()

st.caption(
    "Retail Sales Dashboard | Data Analytics Project | "
    "Oasis Infobyte Internship"
)

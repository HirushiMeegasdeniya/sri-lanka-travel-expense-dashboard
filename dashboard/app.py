# Import pandas so we can load, filter, and summarize the travel expense data.
import pandas as pd

# Import Streamlit so we can create the interactive web dashboard.
import streamlit as st

# Import Plotly Express so we can create interactive charts.
import plotly.express as px

# Import Path so our file paths work correctly on Windows, Mac, and Linux.
from pathlib import Path


# Get the main project folder path.
BASE_DIR = Path(__file__).resolve().parents[1]

# Create the path to the cleaned expense-level dataset.
CLEAN_FILE = BASE_DIR / "outputs" / "cleaned_travel_expenses.csv"

# Create the path to the trip-level summary dataset.
TRIP_SUMMARY_FILE = BASE_DIR / "outputs" / "trip_summary.csv"

# Create the path to the folder that contains saved chart images.
CHARTS_FOLDER = BASE_DIR / "charts"


# Configure the Streamlit page title, icon, and layout.
st.set_page_config(
    page_title="Sri Lanka Travel Expense Intelligence",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --- Custom CSS for professional styling ---
st.markdown(
    """
    <style>
        /* Main background and font - NUDE/BEIGE COLOR */
        .main {
            background-color: #f5ebe0 !important;  /* Nude/beige base color */
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
        
        /* Ensure all main containers use nude background */
        .stApp {
            background-color: #f5ebe0 !important;
        }
        
        .stApp > header {
            background-color: #f5ebe0 !important;
        }

        /* Sidebar styling - slightly darker nude for contrast */
        .css-1d391kg, .css-12oz5g7 {
            background-color: #edddd4 !important;  /* Slightly darker nude */
            border-right: 1px solid #d4c5b8 !important;
        }

        /* --- KPI CARD STYLING --- */
        /* Target the metric container directly */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #faf5f0 0%, #f5ebe0 100%) !important;
            border-radius: 12px !important;
            padding: 20px 24px 18px 24px !important;
            border: 1.5px solid #d4c5b8 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            height: 100% !important;
            min-height: 120px !important;
            position: relative !important;
            overflow: visible !important;
        }

        /* Card hover effect */
        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.10) !important;
            border-color: #b8a394 !important;
        }

        /* Left accent bar */
        div[data-testid="metric-container"]::before {
            content: '' !important;
            position: absolute !important;
            left: -1px !important;
            top: 15% !important;
            height: 70% !important;
            width: 4px !important;
            border-radius: 0 4px 4px 0 !important;
            transition: all 0.3s ease !important;
        }

        /* Accent colors for each card */
        div[data-testid="metric-container"]:nth-child(1)::before {
            background: linear-gradient(180deg, #2563eb, #3b82f6) !important;
        }
        div[data-testid="metric-container"]:nth-child(2)::before {
            background: linear-gradient(180deg, #059669, #34d399) !important;
        }
        div[data-testid="metric-container"]:nth-child(3)::before {
            background: linear-gradient(180deg, #7c3aed, #a78bfa) !important;
        }
        div[data-testid="metric-container"]:nth-child(4)::before {
            background: linear-gradient(180deg, #dc2626, #f87171) !important;
        }

        /* Accent bar expands on hover */
        div[data-testid="metric-container"]:hover::before {
            width: 6px !important;
            top: 10% !important;
            height: 80% !important;
        }

        /* Metric label (title) */
        div[data-testid="metric-container"] label {
            font-weight: 600 !important;
            font-size: 0.8rem !important;
            color: #5c4d3e !important;
            letter-spacing: 0.03em !important;
            text-transform: uppercase !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
            margin-bottom: 6px !important;
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }

        /* Metric value (number) */
        div[data-testid="metric-container"] div[data-testid="metric-value"] {
            font-weight: 700 !important;
            font-size: 2rem !important;
            color: #2c241c !important;
            line-height: 1.2 !important;
            letter-spacing: -0.02em !important;
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
            padding: 2px 0 !important;
        }

        /* Metric delta (if present) */
        div[data-testid="metric-container"] div[data-testid="metric-delta"] {
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            margin-top: 4px !important;
        }

        /* Custom caption below metric */
        .metric-caption-wrapper {
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            margin-top: 8px !important;
            padding-top: 8px !important;
            border-top: 1.5px solid #e8dbd0 !important;
        }

        .metric-caption {
            font-size: 0.7rem !important;
            color: #8a7a6a !important;
            font-weight: 500 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase !important;
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }

        .metric-icon {
            font-size: 0.8rem !important;
            opacity: 0.7 !important;
        }

        /* Cost per day badge */
        .metric-badge {
            display: inline-flex !important;
            align-items: center !important;
            gap: 10px !important;
            background: #faf5f0 !important;
            padding: 10px 20px 10px 18px !important;
            border-radius: 8px !important;
            border: 1.5px solid #d4c5b8 !important;
            box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            color: #3d3228 !important;
            transition: all 0.2s ease !important;
            font-family: 'Inter', 'Segoe UI', sans-serif !important;
        }

        .metric-badge:hover {
            border-color: #b8a394 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
            transform: translateY(-1px) !important;
        }

        .metric-badge strong {
            color: #2c241c !important;
            font-weight: 700 !important;
        }

        .metric-badge .badge-icon {
            opacity: 0.7 !important;
        }

        /* --- END KPI CARD STYLING --- */

        /* Headings */
        h1, h2, h3 {
            font-weight: 600;
            color: #2c241c;
            letter-spacing: -0.01em;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        h1 {
            font-size: 2.2rem !important;
            border-bottom: 3px solid #d4c5b8;
            padding-bottom: 0.4rem;
            margin-bottom: 1.2rem;
        }

        h2 {
            font-size: 1.5rem !important;
            margin-top: 0.8rem;
            margin-bottom: 1rem;
        }

        /* Sidebar title */
        .css-1offfwp h1, .css-1offfwp h2, .css-1offfwp h3 {
            color: #2c241c;
            font-weight: 600;
        }

        /* Divider */
        hr {
            border: none;
            border-top: 2px solid #d4c5b8;
            margin: 1.8rem 0;
        }

        /* Caption / footer text */
        .caption-text {
            font-size: 0.9rem;
            color: #6b5d4f;
            background: #ede0d5;
            padding: 8px 16px;
            border-radius: 8px;
            display: inline-block;
        }

        /* Dataframe */
        .stDataFrame {
            border-radius: 12px;
            border: 1px solid #d4c5b8;
            overflow: hidden;
        }

        .stDataFrame thead tr th {
            background-color: #ede0d5 !important;
            color: #2c241c !important;
            font-weight: 600 !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            font-weight: 500;
            color: #3d3228;
            background-color: #f5ebe0;
            border-radius: 8px;
            border: 1px solid #d4c5b8;
        }

        .streamlit-expanderContent {
            border-radius: 0 0 8px 8px;
            border: 1px solid #d4c5b8;
            border-top: none;
            padding: 1rem;
            background-color: #faf5f0;
        }

        /* Buttons / widgets */
        .stSelectbox, .stMultiSelect {
            border-radius: 8px;
        }

        /* Footer */
        .footer {
            color: #6b5d4f;
            font-size: 0.85rem;
            padding-top: 0.5rem;
            border-top: 1px solid #d4c5b8;
            margin-top: 2rem;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        /* Tabs (if used) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background: #ede0d5;
            border-radius: 8px 8px 0 0;
            padding: 8px 20px;
            font-weight: 500;
            color: #5c4d3e;
        }

        .stTabs [aria-selected="true"] {
            background: #faf5f0;
            border: 1px solid #d4c5b8;
            border-bottom: 2px solid #2563eb;
            color: #2c241c;
        }

        /* Badge / chip */
        .badge {
            background: #dbeafe;
            color: #1e40af;
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            display: inline-block;
        }

        /* Ensure consistent spacing in columns */
        .row-widget.stColumns {
            gap: 1rem;
        }

        /* Fix for column spacing */
        .stColumn {
            padding: 0 4px !important;
        }

        /* Ensure cards are visible */
        .element-container:has(div[data-testid="metric-container"]) {
            padding: 0 !important;
        }
        
        /* Chart container backgrounds */
        .stPlotlyChart {
            background-color: #faf5f0 !important;
            border-radius: 12px !important;
            padding: 10px !important;
            border: 1px solid #d4c5b8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Define a function to format Sri Lankan Rupee values.
def format_lkr(value):
    # Check whether the value is missing.
    if pd.isna(value):
        # Return zero rupees if the value is missing.
        return "LKR 0"

    # Return the value formatted with commas and no decimal places.
    return f"LKR {value:,.0f}"


# Cache the data loading function so the dashboard runs faster.
@st.cache_data
def load_data():
    # Load the cleaned expense-level dataset.
    df = pd.read_csv(CLEAN_FILE)

    # Load the trip-level summary dataset.
    trip_summary = pd.read_csv(TRIP_SUMMARY_FILE)

    # Convert the Date column in the expense-level dataset into datetime format.
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert the Date column in the trip-level dataset into datetime format.
    trip_summary["Date"] = pd.to_datetime(trip_summary["Date"])

    # Return both datasets.
    return df, trip_summary


# Load the datasets by calling the load_data function.
df, trip_summary = load_data()


# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("Refine the dashboard data using the filters below.")

    # Create a list of available destinations.
    destination_options = sorted(df["Destination"].dropna().unique())

    # Create a multi-select filter for destinations.
    selected_destinations = st.multiselect(
        "📍 Destination",
        options=destination_options,
        default=destination_options,
        placeholder="Select destinations..."
    )

    # Create a list of available seasons.
    season_options = sorted(df["Season"].dropna().unique())

    # Create a multi-select filter for seasons.
    selected_seasons = st.multiselect(
        "🌤️ Season",
        options=season_options,
        default=season_options,
        placeholder="Select seasons..."
    )

    # Create a list of available traveler types.
    traveler_type_options = sorted(df["Traveler_Type"].dropna().unique())

    # Create a multi-select filter for traveler type.
    selected_traveler_types = st.multiselect(
        "👤 Traveler Type",
        options=traveler_type_options,
        default=traveler_type_options,
        placeholder="Select traveler types..."
    )

    st.divider()
    st.markdown("### 📊 Data Summary")
    st.markdown("Use the filters above to explore travel expense patterns across Sri Lanka.")


# Filter the expense-level dataset based on selected dashboard filters.
filtered_df = df[
    (df["Destination"].isin(selected_destinations))
    & (df["Season"].isin(selected_seasons))
    & (df["Traveler_Type"].isin(selected_traveler_types))
]

# Filter the trip-level dataset based on selected dashboard filters.
filtered_trip_summary = trip_summary[
    (trip_summary["Destination"].isin(selected_destinations))
    & (trip_summary["Season"].isin(selected_seasons))
    & (trip_summary["Traveler_Type"].isin(selected_traveler_types))
]


# Check whether the filtered data is empty.
if filtered_df.empty or filtered_trip_summary.empty:
    # Show a warning message if no data matches the selected filters.
    st.warning("⚠️ No data available for the selected filters. Please adjust your filter selection.")
    st.stop()


# --- Calculate key metrics ---
total_trips = filtered_trip_summary["Trip_ID"].nunique()
total_spending = filtered_df["Amount_LKR"].sum()
average_trip_cost = filtered_trip_summary["Total_Trip_Cost_LKR"].mean()
average_cost_per_day = filtered_trip_summary["Cost_Per_Day_LKR"].mean()

# Calculate average trip cost by destination.
destination_cost = filtered_trip_summary.groupby("Destination", as_index=False)[
    "Total_Trip_Cost_LKR"
].mean()
destination_cost = destination_cost.rename(
    columns={"Total_Trip_Cost_LKR": "Average_Trip_Cost_LKR"}
)
destination_cost = destination_cost.sort_values(
    by="Average_Trip_Cost_LKR",
    ascending=False
)
most_expensive_destination = destination_cost.iloc[0]["Destination"] if not destination_cost.empty else "N/A"


# --- Main Dashboard ---
st.title("🇱🇰 Sri Lanka Travel Expense Intelligence")

st.markdown(
    """
    <p style="font-size:1.05rem; color:#3d3228; margin-top:-0.2rem;">
    Analyze travel expense patterns across popular Sri Lankan destinations. 
    Compare trip costs, daily spending, categories, traveler types, and seasonal trends.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# --- KPI METRIC CARDS ROW ---
st.subheader("📈 Key Metrics")

# Create columns for the KPI cards
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(
        label="✈️ Total Trips", 
        value=f"{total_trips:,}",
        delta=None,
        help="Number of unique trips in the filtered dataset"
    )
    st.markdown(
        """
        <div class="metric-caption-wrapper">
            <span class="metric-icon">📋</span>
            <span class="metric-caption">Unique trip records</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col2:
    st.metric(
        label="💰 Total Spending", 
        value=format_lkr(total_spending),
        delta=None,
        help="Aggregate expense amount across all trips"
    )
    st.markdown(
        """
        <div class="metric-caption-wrapper">
            <span class="metric-icon">💳</span>
            <span class="metric-caption">Total expenditure</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col3:
    st.metric(
        label="📊 Average Trip Cost", 
        value=format_lkr(average_trip_cost),
        delta=None,
        help="Mean cost per trip in the filtered dataset"
    )
    st.markdown(
        """
        <div class="metric-caption-wrapper">
            <span class="metric-icon">📈</span>
            <span class="metric-caption">Per trip average</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with metric_col4:
    st.metric(
        label="🏆 Most Expensive", 
        value=most_expensive_destination,
        delta=None,
        help="Destination with the highest average trip cost"
    )
    st.markdown(
        """
        <div class="metric-caption-wrapper">
            <span class="metric-icon">⭐</span>
            <span class="metric-caption">Highest avg. trip cost</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# Additional metric row (cost per day) - Card style badge
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 12px; margin-top: 12px; flex-wrap: wrap;">
        <span class="metric-badge">
            <span class="badge-icon">📅</span>
            Average cost per day: <strong>{format_lkr(average_cost_per_day)}</strong>
        </span>
        <span style="color: #8a7a6a; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.02em; font-weight: 500;">
            Based on filtered trip data
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# --- Row 1: Charts ---
chart_col1, chart_col2 = st.columns(2, gap="large")

# Chart 1: Average trip cost by destination
with chart_col1:
    fig_destination = px.bar(
        destination_cost,
        x="Destination",
        y="Average_Trip_Cost_LKR",
        title="Average Trip Cost by Destination",
        labels={
            "Destination": "Destination",
            "Average_Trip_Cost_LKR": "Average Trip Cost (LKR)"
        },
        color="Destination",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto=",.0f"
    )
    fig_destination.update_layout(
        xaxis_tickangle=-45,
        height=450,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3d3228"),
        title_font=dict(size=16, weight=600),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig_destination.update_traces(
        marker_line_width=1,
        marker_line_color="#faf5f0",
        textposition="outside"
    )
    chart_col1.plotly_chart(fig_destination, use_container_width=True)

# Chart 2: Spending by category
with chart_col2:
    category_spending = filtered_df.groupby("Category", as_index=False)["Amount_LKR"].sum()
    category_spending = category_spending.sort_values(by="Amount_LKR", ascending=False)

    fig_category = px.pie(
        category_spending,
        names="Category",
        values="Amount_LKR",
        title="Spending Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        hole=0.35,
    )
    fig_category.update_layout(
        height=450,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3d3228"),
        title_font=dict(size=16, weight=600),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    fig_category.update_traces(
        textinfo="percent+label",
        textposition="outside",
        pull=[0.02 if i == 0 else 0 for i in range(len(category_spending))]
    )
    chart_col2.plotly_chart(fig_category, use_container_width=True)


# --- Chart 3: Monthly Spending Trend ---
st.subheader("📅 Monthly Spending Trend")

monthly_spending = filtered_df.groupby("Month", as_index=False)["Amount_LKR"].sum()
monthly_spending = monthly_spending.sort_values(by="Month")

fig_monthly = px.line(
    monthly_spending,
    x="Month",
    y="Amount_LKR",
    markers=True,
    title="Total Spending by Month",
    labels={
        "Month": "Month",
        "Amount_LKR": "Total Spending (LKR)"
    },
    color_discrete_sequence=["#2563eb"],
    line_shape="spline"
)
fig_monthly.update_layout(
    xaxis_tickangle=-45,
    height=420,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#3d3228"),
    title_font=dict(size=16, weight=600),
    margin=dict(l=10, r=10, t=40, b=10),
)
fig_monthly.update_traces(
    marker=dict(size=10, line=dict(width=2, color="#faf5f0")),
    line=dict(width=3)
)
st.plotly_chart(fig_monthly, use_container_width=True)

st.divider()


# --- Row 2: Charts ---
chart_col3, chart_col4 = st.columns(2, gap="large")

# Chart 4: Destination × Category heatmap
with chart_col3:
    heatmap_data = filtered_df.pivot_table(
        values="Amount_LKR",
        index="Destination",
        columns="Category",
        aggfunc="sum",
        fill_value=0
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        text_auto=".0f",
        aspect="auto",
        title="Destination × Category Spending Heatmap",
        labels={
            "x": "Expense Category",
            "y": "Destination",
            "color": "Spending (LKR)"
        },
        color_continuous_scale="Blues",
    )
    fig_heatmap.update_layout(
        height=480,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3d3228"),
        title_font=dict(size=16, weight=600),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig_heatmap.update_xaxes(tickangle=-30)
    chart_col3.plotly_chart(fig_heatmap, use_container_width=True)

# Chart 5: Expense distribution boxplot
with chart_col4:
    fig_boxplot = px.box(
        filtered_df,
        x="Destination",
        y="Amount_LKR",
        title="Expense Distribution by Destination",
        labels={
            "Destination": "Destination",
            "Amount_LKR": "Expense Amount (LKR)"
        },
        color="Destination",
        color_discrete_sequence=px.colors.qualitative.Set3,
        points="all",
        notched=True,
    )
    fig_boxplot.update_layout(
        xaxis_tickangle=-45,
        height=480,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#3d3228"),
        title_font=dict(size=16, weight=600),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    fig_boxplot.update_traces(
        marker=dict(size=4, opacity=0.6),
        line=dict(width=1.5)
    )
    chart_col4.plotly_chart(fig_boxplot, use_container_width=True)

st.divider()


# --- Data Preview ---
st.subheader("📋 Filtered Data Preview")
st.caption("First 20 rows of the expense-level dataset based on your selected filters.")
st.dataframe(filtered_df.head(20), use_container_width=True, height=300)

st.divider()


# --- Insights Template ---
st.subheader("💡 Insights & Recommendations")
st.markdown(
    """
    <div style="background:#f5ebe0; border-left:4px solid #2563eb; padding:1rem 1.5rem; border-radius:8px;">
        <p style="font-weight:600; margin:0 0 0.25rem 0;">Finding + Evidence + Meaning + Recommendation</p>
        <p style="color:#3d3228; margin:0;">
            <strong>Example:</strong> Accommodation was the largest expense category in the selected data.
            This suggests that lodging is a major cost driver in Sri Lankan travel budgets.
            Travelers who want to reduce total trip cost should compare hotels, guest houses,
            hostels, and off-peak booking options.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# --- Saved Charts ---
with st.expander("📁 View Saved Chart Images (Step 5)"):

    chart_files = [
        "average_trip_cost_by_destination.png",
        "spending_by_category_pie_chart.png",
        "monthly_spending_trend.png",
        "destination_category_spending_heatmap.png",
        "expense_distribution_by_destination.png",
    ]

    col1, col2 = st.columns(2)

    for idx, chart_file in enumerate(chart_files):
        chart_path = CHARTS_FOLDER / chart_file
        with (col1 if idx % 2 == 0 else col2):
            if chart_path.exists():
                st.markdown(f"**{chart_file}**")
                st.image(str(chart_path), use_container_width=True)
            else:
                st.warning(f"⚠️ {chart_file} not found in the charts folder.")


# --- Footer ---
st.divider()
st.markdown(
    """
    <div class="footer">
        <strong>🇱🇰 Sri Lanka Travel Expense Intelligence Dashboard</strong> &nbsp;·&nbsp;
        Built with Python, Pandas, Plotly &amp; Streamlit &nbsp;·&nbsp;
        <span style="color:#8a7a6a;">Beginner-friendly data analysis portfolio project</span>
    </div>
    """,
    unsafe_allow_html=True
)